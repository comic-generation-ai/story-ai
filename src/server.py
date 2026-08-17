import os
import sys
import time
import traceback
import logging
import json
import asyncio
from typing import List, Literal, Optional
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
# pyrefly: ignore [missing-import]
import openai
# pyrefly: ignore [missing-import]
import httpx

# Ensure console handles Unicode characters on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.llm import prompt_template, parser, folklore

# --- Structured Logging Setup ---
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)

logger = logging.getLogger("story-ai")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = JsonFormatter(datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

Config.validate()

openai_client = None
if Config.API_KEY:
    # verify=False bypasses SSL cert check (needed on Windows with corporate proxy / self-signed CA)
    openai_client = openai.AsyncOpenAI(
        api_key=Config.API_KEY,
        base_url=Config.BASE_URL,
        http_client=httpx.AsyncClient(verify=False),
    )

app = FastAPI(
    title="Story AI Service",
    description="HTTP API for generating comic stories using LLM",
    version="1.3.0"
)

# Add CORS Middleware to allow requests from frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Schemas ---
class GenerateStoryRequest(BaseModel):
    job_id: str
    summary: str
    num_panels: Optional[int] = 4
    style: Optional[str] = "comic book style, vibrant colors"
    language: Optional[str] = "vi"

class CharacterDetail(BaseModel):
    name: str
    visual_tag: str

class PanelScript(BaseModel):
    panel_number: int
    panel_type: Optional[str] = "dialogue"
    image_prompt: str
    scene_description: Optional[str] = ""
    speaker: Optional[str] = None
    dialogue: Optional[str] = None
    speaker_position: Optional[Literal["left", "center", "right"]] = "center"
    character_ids: List[str] = Field(default_factory=list)

class GenerateStoryResponse(BaseModel):
    job_id: str
    story_title: str
    characters: dict[str, CharacterDetail] = Field(default_factory=dict)
    panels: List[PanelScript]
    is_fallback: bool = False

class HealthResponse(BaseModel):
    is_alive: bool
    model_id: str
    versions: dict

# --- Mock Data for Fallback ---
_MOCK_PANELS = [
    ("Người kể chuyện", "story starting in vibrant setting, comic book style, detailed line art"),
    ("Nhân vật chính",  "protagonist standing determined, facing challenge, dynamic pose, comic book style"),
    ("Người kể chuyện", "sudden conflict, dramatic lighting, comic book style"),
    ("Nhân vật chính",  "hero overcoming obstacle, triumphant moment, vibrant colors, comic book style"),
    ("Người kể chuyện", "journey continuing into the unknown, wide establishing shot, comic book style"),
    ("Nhân vật chính",  "new discovery, close-up reaction shot, comic book style"),
]

def _get_mock_fallback(request: GenerateStoryRequest, error_msg: str) -> GenerateStoryResponse:
    logger.warning(f"FALLBACK: {error_msg}")

    num_panels = request.num_panels if request.num_panels and request.num_panels > 0 else 4
    summary_clean = request.summary.strip() or "Cuộc phiêu lưu kì thú"
    summary_short = summary_clean[:150].rstrip() + ("..." if len(summary_clean) > 150 else "")

    characters = {
        "char_001": CharacterDetail(
            name="Nhân vật chính",
            visual_tag="protagonist standing determined, comic book style"
        )
    }

    panels = []
    for i in range(num_panels):
        speaker, img_prompt = _MOCK_PANELS[i % len(_MOCK_PANELS)]
        panels.append(PanelScript(
            panel_number=i + 1,
            panel_type="narration" if speaker == "Người kể chuyện" else "dialogue",
            image_prompt=img_prompt,
            scene_description=f"Scene with {speaker}",
            speaker=speaker,
            dialogue=f"[Khung {i+1}] {summary_short}",
            speaker_position="center",
            character_ids=[] if speaker == "Người kể chuyện" else ["char_001"],
        ))

    return GenerateStoryResponse(
        job_id=request.job_id,
        characters=characters,
        panels=panels,
        story_title=f"Hành trình {summary_clean[:30]} (Fallback)",
        is_fallback=True,
    )

CANCELLED_JOBS: set[str] = set()
ACTIVE_TASKS: dict[str, asyncio.Task] = {}

@app.post("/cancel-story/{job_id}")
async def cancel_story_endpoint(job_id: str):
    logger.info(f"CancelStory received for job_id={job_id}")
    CANCELLED_JOBS.add(job_id)
    task = ACTIVE_TASKS.get(job_id)
    if task:
        logger.info(f"Aborting active LLM task for job_id={job_id}")
        task.cancel()
    return {"job_id": job_id, "status": "CANCELLED"}

# --- Routes ---
@app.post("/generate-story", response_model=GenerateStoryResponse)
async def generate_story_endpoint(request: GenerateStoryRequest):
    logger.info(f"GenerateStory | job_id={request.job_id} | panels={request.num_panels}")
    logger.info(f"Summary: {request.summary}")

    current_task = asyncio.current_task()
    if current_task:
        ACTIVE_TASKS[request.job_id] = current_task

    try:
        if request.job_id in CANCELLED_JOBS:
            logger.info(f"Job {request.job_id} was cancelled before execution.")
            raise HTTPException(status_code=499, detail="Story generation cancelled by user")

        if not request.summary.strip():
            return _get_mock_fallback(request, "Request summary is empty.")

        if not openai_client:
            return _get_mock_fallback(request, "API key is not configured.")

        num_panels = request.num_panels if request.num_panels and request.num_panels > 0 else 4
        style = request.style or "comic book style, vibrant colors"
        language = request.language or "vi"

        folklore_data = folklore.get_folklore_context(request.summary)
        folklore_context = None
        if folklore_data:
            logger.info(f"Detected Vietnamese folktale: {folklore_data['canonical_title']}")
            folklore_context = folklore_data["context"]

        system_prompt = prompt_template.get_system_prompt()
        user_prompt = prompt_template.get_user_prompt(
            summary=request.summary,
            style=style,
            num_panels=num_panels,
            language=language,
            folklore_context=folklore_context
        )

        primary_model = Config.MODEL_NAME
        fallback_models = [m for m in ["qwen3.6-flash", "qwen3.7-max-2026-06-08"] if m != primary_model]
        models_to_try = [primary_model] + fallback_models
        model_index = 0
        model_to_use = models_to_try[model_index]

        max_retries = 3
        attempt = 1
        while attempt <= max_retries:
            if request.job_id in CANCELLED_JOBS:
                raise asyncio.CancelledError()

            try:
                logger.info(f"Calling DashScope API ({model_to_use}), attempt {attempt}/{max_retries}...")
                start_time = time.time()

                completion = await openai_client.chat.completions.create(
                    model=model_to_use,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                )

                latency = time.time() - start_time
                logger.info(f"Response received in {latency:.2f}s.")

                if not completion.choices:
                    raise ValueError(f"Model returned empty choices. Full response: {completion!r}")

                msg = completion.choices[0].message
                raw_response = msg.content
                if not raw_response:
                    raw_response = getattr(msg, "reasoning_content", None)
                if not raw_response:
                    raise ValueError(f"Model returned empty content. Message: {msg!r}")

                logger.info(f"Raw response preview: {raw_response[:200]!r}")

                parsed_data = parser.parse_llm_json(raw_response)

                characters_raw = parsed_data.get("characters", {})
                characters = {
                    cid: CharacterDetail(name=cinfo["name"], visual_tag=cinfo["visual_tag"])
                    for cid, cinfo in characters_raw.items()
                }

                panels = []
                for panel_data in parsed_data.get("panels", []):
                    panels.append(PanelScript(
                        panel_number=panel_data["panel_number"],
                        panel_type=panel_data.get("panel_type", "dialogue"),
                        image_prompt=panel_data["image_prompt"],
                        scene_description=panel_data.get("scene_description", ""),
                        speaker=panel_data.get("speaker"),
                        dialogue=panel_data.get("dialogue"),
                        speaker_position=panel_data.get("speaker_position", "center"),
                        character_ids=panel_data.get("character_ids", []),
                    ))

                logger.info(f"Successfully generated {len(panels)} panels.")
                return GenerateStoryResponse(
                    job_id=request.job_id,
                    characters=characters,
                    panels=panels,
                    story_title=parsed_data.get("story_title", f"Câu chuyện {request.job_id[:8]}")
                )

            except asyncio.CancelledError:
                logger.info(f"LLM call aborted for cancelled job {request.job_id}")
                raise HTTPException(status_code=499, detail="Story generation cancelled by user")

            except (openai.RateLimitError, openai.APIError) as e:
                if model_index < len(models_to_try) - 1:
                    logger.warning(f"Model ({model_to_use}) failed with API/Rate Limit error: {e}")
                    model_index += 1
                    model_to_use = models_to_try[model_index]
                    logger.info(f"Switching to fallback model: {model_to_use}")
                    continue

                wait = 15
                if isinstance(e, openai.RateLimitError):
                    try:
                        meta = e.body.get("error", {}).get("metadata", {})
                        wait = int(meta.get("retry_after_seconds", 15)) + 2
                    except Exception:
                        pass
                wait = min(wait, 20)
                if attempt < max_retries:
                    logger.warning(f"Rate limited (429) or API error. Waiting {wait}s before retry...")
                    await asyncio.sleep(wait)
                    attempt += 1
                else:
                    logger.error(f"ERROR detail:\n{traceback.format_exc()}")
                    return _get_mock_fallback(request, f"Rate limited / API error after {max_retries} attempts: {e}")

            except Exception as e:
                if model_index < len(models_to_try) - 1:
                    logger.warning(f"Model ({model_to_use}) failed with parse/validation error: {e}")
                    model_index += 1
                    model_to_use = models_to_try[model_index]
                    logger.info(f"Switching to fallback model: {model_to_use}")
                    continue

                logger.error(f"ERROR detail:\n{traceback.format_exc()}")
                return _get_mock_fallback(request, f"LLM/parse error: {e}")
    finally:
        ACTIVE_TASKS.pop(request.job_id, None)

@app.get("/health", response_model=HealthResponse)
async def health_endpoint():
    logger.info("CheckHealth")
    return HealthResponse(
        is_alive=True,
        model_id=Config.MODEL_NAME if Config.API_KEY else "mock",
        versions={
            "http_server": "1.3.0",
            "python": sys.version.split()[0],
            "llm_provider": "DashScope"
        }
    )

def serve():
    # pyrefly: ignore [missing-import]
    import uvicorn
    port = Config.PORT
    logger.info(f"story-ai FastAPI service starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    serve()

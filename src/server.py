import os
import sys
import time
import traceback
import re as _re
from typing import List, Optional
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
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

Config.validate()

# Initialize OpenAI client pointing to OpenRouter if API key exists
openai_client = None
if Config.API_KEY:
    # verify=False bypasses SSL cert check (needed on Windows with corporate proxy / self-signed CA)
    openai_client = openai.OpenAI(
        api_key=Config.API_KEY,
        base_url=Config.BASE_URL,
        http_client=httpx.Client(verify=False),
    )

app = FastAPI(
    title="Story AI Service",
    description="HTTP API for generating comic stories using LLM",
    version="1.2.0"
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

class PanelScript(BaseModel):
    panel_number: int
    panel_type: Optional[str] = "dialogue"
    image_prompt: str
    speaker: Optional[str] = None
    dialogue: Optional[str] = None

class GenerateStoryResponse(BaseModel):
    job_id: str
    story_title: str
    panels: List[PanelScript]

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
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] FALLBACK: {error_msg}")

    num_panels = request.num_panels if request.num_panels and request.num_panels > 0 else 4
    summary_clean = request.summary.strip() or "Cuộc phiêu lưu kì thú"

    panels = []
    for i in range(num_panels):
        speaker, img_prompt = _MOCK_PANELS[i % len(_MOCK_PANELS)]
        panels.append(PanelScript(
            panel_number=i + 1,
            panel_type="narration" if speaker == "Người kể chuyện" else "dialogue",
            image_prompt=img_prompt,
            speaker=speaker,
            dialogue=f"[Khung {i+1}] {summary_clean}.",
        ))

    return GenerateStoryResponse(
        job_id=request.job_id,
        panels=panels,
        story_title=f"Hành trình {summary_clean[:30]} (Fallback)"
    )

# --- Routes ---
@app.post("/generate-story", response_model=GenerateStoryResponse)
def generate_story_endpoint(request: GenerateStoryRequest):
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] GenerateStory | job_id={request.job_id} | panels={request.num_panels}")
    print(f"  Summary: {request.summary}")

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
        print(f"  Detected Vietnamese folktale: {folklore_data['canonical_title']}")
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
    fallback_model = "qwen3.7-max-2026-06-08"
    model_to_use = primary_model

    max_retries = 3
    attempt = 1
    while attempt <= max_retries:
        try:
            print(f"  Calling OpenRouter API ({model_to_use}), attempt {attempt}/{max_retries}...")
            start_time = time.time()

            completion = openai_client.chat.completions.create(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )

            latency = time.time() - start_time
            print(f"  Response received in {latency:.2f}s.")
            print(f"  completion.choices = {completion.choices!r}")

            if not completion.choices:
                raise ValueError(f"Model returned empty choices. Full response: {completion!r}")

            msg = completion.choices[0].message
            raw_response = msg.content
            if not raw_response:
                # Qwen3 thinking models may separate reasoning from output
                raw_response = getattr(msg, "reasoning_content", None)
            if not raw_response:
                raise ValueError(f"Model returned empty content. Message: {msg!r}")

            print(f"  Raw response preview: {raw_response[:200]!r}")

            parsed_data = parser.parse_llm_json(raw_response)

            panels = []
            for panel_data in parsed_data.get("panels", []):
                panels.append(PanelScript(
                    panel_number=panel_data["panel_number"],
                    panel_type=panel_data.get("panel_type", "dialogue"),
                    image_prompt=panel_data["image_prompt"],
                    speaker=panel_data.get("speaker"),
                    dialogue=panel_data.get("dialogue"),
                ))

            print(f"  Successfully generated {len(panels)} panels.")
            return GenerateStoryResponse(
                job_id=request.job_id,
                panels=panels,
                story_title=parsed_data.get("story_title", f"Câu chuyện {request.job_id[:8]}")
            )

        except (openai.RateLimitError, openai.APIError) as e:
            if model_to_use == primary_model and primary_model != fallback_model:
                print(f"  Primary model ({primary_model}) failed with API/Rate Limit error: {e}")
                print(f"  Switching to fallback model: {fallback_model}")
                model_to_use = fallback_model
                continue

            # Extract retry-after from error metadata if available
            wait = 30
            if isinstance(e, openai.RateLimitError):
                try:
                    meta = e.body.get("error", {}).get("metadata", {})
                    wait = int(meta.get("retry_after_seconds", 30)) + 2
                except Exception:
                    pass
            if attempt < max_retries:
                print(f"  Rate limited (429) or API error. Waiting {wait}s before retry...")
                time.sleep(wait)
                attempt += 1
            else:
                print(f"  ERROR detail:\n{traceback.format_exc()}")
                return _get_mock_fallback(request, f"Rate limited / API error after {max_retries} attempts: {e}")

        except Exception as e:
            if model_to_use == primary_model and primary_model != fallback_model:
                print(f"  Primary model ({primary_model}) failed with parse/validation error: {e}")
                print(f"  Switching to fallback model: {fallback_model}")
                model_to_use = fallback_model
                continue

            print(f"  ERROR detail:\n{traceback.format_exc()}")
            return _get_mock_fallback(request, f"LLM/parse error: {e}")

@app.get("/health", response_model=HealthResponse)
def health_endpoint():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] CheckHealth")
    return HealthResponse(
        is_alive=True,
        model_id=Config.MODEL_NAME if Config.API_KEY else "mock",
        versions={
            "http_server": "1.2.0",
            "python": sys.version.split()[0],
            "llm_provider": "OpenRouter"
        }
    )

def serve():
    # pyrefly: ignore [missing-import]
    import uvicorn
    port = Config.PORT
    print(f"story-ai FastAPI service starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    serve()

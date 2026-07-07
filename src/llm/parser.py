import json
import logging
import re
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional

logger = logging.getLogger(__name__)

# Prompt đã yêu cầu LLM viết dialogue ≤ 120 ký tự nhưng LLM không tuân thủ 100%.
# Mức 150 là biên dự phòng: image-ai reject cứng caption_text > 500 ký tự
# (CAPTION_MAX_LENGTH) nên phải chặn trước khi thoại rời story-ai.
MAX_DIALOGUE_CHARS = 150


class PanelScriptModel(BaseModel):
    panel_number: int
    panel_type: Optional[Literal["action", "dialogue", "narration"]] = "dialogue"
    image_prompt: str
    speaker: Optional[str] = None
    dialogue: Optional[str] = None

    @field_validator("dialogue")
    @classmethod
    def _truncate_dialogue(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value) > MAX_DIALOGUE_CHARS:
            logger.warning(
                "dialogue dài %d ký tự vượt giới hạn %d, cắt bớt",
                len(value), MAX_DIALOGUE_CHARS,
            )
            return value[: MAX_DIALOGUE_CHARS - 1].rstrip() + "…"
        return value


class StoryResponseModel(BaseModel):
    story_title: str
    panels: List[PanelScriptModel]


def parse_llm_json(raw_text: str) -> dict:
    cleaned = raw_text.strip()

    # Qwen3 thinking models prepend <think>...</think> before the JSON output
    cleaned = re.sub(r"<think>.*?</think>", "", cleaned, flags=re.DOTALL).strip()

    # Strip markdown code fences if present
    if cleaned.startswith("```"):
        match = re.search(r"^(?:```[a-zA-Z0-9-]*\n)(.*?)(?:\n```)$", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
        else:
            cleaned = re.sub(r"^```[a-zA-Z0-9-]*\n?|```$", "", cleaned).strip()

    parsed_dict = json.loads(cleaned)
    validated = StoryResponseModel(**parsed_dict)
    result = validated.model_dump()

    # LLM đôi khi trả panel_number trùng lặp hoặc nhảy số (vd: 1, 2, 4).
    # Orchestrator dùng panel_number - 1 làm index truy cập list nên số nhảy/trùng
    # sẽ gây IndexError hoặc ghi đè panel. Chuẩn hóa lại thành dãy liên tục 1..N.
    panels = sorted(result.get("panels", []), key=lambda p: p["panel_number"])
    for i, panel in enumerate(panels):
        panel["panel_number"] = i + 1
    result["panels"] = panels

    return result

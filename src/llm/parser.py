import json
import logging
import re
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Literal, Optional

logger = logging.getLogger(__name__)

MAX_DIALOGUE_CHARS = 150

NARRATOR_LABEL = "Người kể chuyện"
FALLBACK_NARRATION_TEXT = "Câu chuyện tiếp diễn..."


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

    @model_validator(mode="after")
    def _ensure_dialogue_present(self) -> "PanelScriptModel":
        if not self.dialogue or not self.dialogue.strip():
            logger.warning(
                "panel_number=%s thiếu dialogue dù prompt đã bắt buộc — vá thành lời người dẫn truyện",
                self.panel_number,
            )
            self.panel_type = "narration"
            self.speaker = NARRATOR_LABEL
            self.dialogue = FALLBACK_NARRATION_TEXT
        elif not self.speaker or not self.speaker.strip():
            self.speaker = NARRATOR_LABEL
        return self


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

    panels = sorted(result.get("panels", []), key=lambda p: p["panel_number"])
    for i, panel in enumerate(panels):
        panel["panel_number"] = i + 1
    result["panels"] = panels

    return result

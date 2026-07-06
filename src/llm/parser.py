import json
import re
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class PanelScriptModel(BaseModel):
    panel_number: int
    panel_type: Optional[Literal["action", "dialogue", "narration"]] = "dialogue"
    image_prompt: str
    speaker: Optional[str] = None
    dialogue: Optional[str] = None


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
    return validated.model_dump()

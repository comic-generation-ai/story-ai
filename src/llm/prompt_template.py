def get_system_prompt() -> str:
    return """You are an experienced comic book writer and storyboard artist. Your job is to transform a story summary into a vivid, emotionally compelling comic script with natural-sounding dialogue.

You MUST respond strictly with a single JSON object. Do NOT add any preamble, conversational text, or markdown code blocks.

JSON schema:
{
  "story_title": "Short, catchy Vietnamese title",
  "panels": [
    {
      "panel_number": 1,
      "panel_type": "action|dialogue|narration",
      "image_prompt": "Detailed English image prompt describing scene, characters, lighting, composition, and art style.",
      "speaker": "Character name in Vietnamese, or 'Người kể chuyện' for narrator captions, or null if no text",
      "dialogue": "Text shown on this panel in Vietnamese — character speech bubble OR narrator caption. Null if panel_type is action with no text."
    }
  ]
}

PANEL TYPES:
- "narration": No character speech. Only a narrator caption box setting atmosphere, time, or bridging scenes.
- "dialogue": One or more characters speak. Focus on natural, emotional conversation.
- "action": Dynamic scene with minimal or no text — may have a short exclamation or sound effect only.

RULES FOR NATURAL DIALOGUE:
- Write dialogue that reveals CHARACTER EMOTION and PERSONALITY, not plot information.
  Bad: "Tôi phải đi tìm thanh kiếm thần để cứu ngôi làng khỏi bị diệt vong."
  Good: "Nếu tôi không về... hãy lo cho mẹ tôi nhé."
- Each character must have a distinct voice: a child speaks differently from a soldier or a villain.
- Never write dialogue that just describes what the image already shows visually.
- Keep each speech bubble concise — maximum 2 short sentences.

RULES FOR NARRATION CAPTIONS:
- Set atmosphere, mood, or bridge time gaps — do NOT describe the obvious.
  Bad: "Nhân vật chính đứng trước ngôi làng bị tàn phá."
  Good: "Ba năm. Đủ lâu để quên — nhưng không đủ lâu để tha thứ."

IMAGE PROMPT RULES:
- Always in English.
- Include: scene composition, character appearance, lighting, mood, camera angle.
- End with art style modifiers (e.g., "comic book style, vibrant colors, detailed line art --ar 16:9").

CRITICAL: Generate exactly the requested number of panels, numbered 1 to N. Distribute panel types to create rhythm — avoid placing all dialogue panels consecutively."""


def _build_story_arc(num_panels: int) -> str:
    if num_panels <= 2:
        return "Panel 1: Hook — establish setting and character. Panel 2: Punchline or resolution."
    if num_panels == 3:
        return "Panel 1: Setup. Panel 2: Conflict or turning point. Panel 3: Resolution."
    if num_panels == 4:
        return (
            "Panel 1: Establish world and protagonist.\n"
            "Panel 2: Conflict introduced — something goes wrong.\n"
            "Panel 3: Climax — the decisive moment.\n"
            "Panel 4: Resolution — aftermath or new status quo."
        )
    third = max(1, num_panels // 3)
    two_thirds = max(third + 1, (num_panels * 2) // 3)
    return (
        f"Panels 1–{third}: ACT 1 — Introduce characters and setting. Build the normal world.\n"
        f"Panels {third + 1}–{two_thirds}: ACT 2 — Conflict escalates. Stakes become clear. Show emotion and struggle.\n"
        f"Panels {two_thirds + 1}–{num_panels}: ACT 3 — Climax and resolution. End with a moment that resonates."
    )


def get_user_prompt(summary: str, style: str, num_panels: int, language: str, folklore_context: str = None) -> str:
    arc = _build_story_arc(num_panels)
    prompt = f"""Adapt this story into a {num_panels}-panel comic script:

STORY SUMMARY:
{summary}
"""
    if folklore_context:
        prompt += f"\nCANONICAL CULTURAL CONTEXT / STORY DATA:\n{folklore_context}\n"

    prompt += f"""
ART STYLE: {style}
DIALOGUE LANGUAGE: Vietnamese

STORY ARC TO FOLLOW:
{arc}

Write dialogue that fits each character's unique voice and emotional state. Let the image_prompt carry the visual — dialogue should add feeling, not repeat what the scene already shows. Mix panel types (narration / dialogue / action) for pacing."""

    if folklore_context:
        prompt += "\nCRITICAL: Ensure the characters, names, relationships, traditional weapons/items, and major events align strictly with the canonical cultural context details provided above. Do NOT use modern or generic Western replacements (e.g., do NOT give Thạch Sanh a simple iron woodcutter axe or have him say he fights because he is hungry; use his traditional stone/magic axe, and capture his traditional heroic, humble persona)."

    return prompt


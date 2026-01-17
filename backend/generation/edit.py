"""
Wireframe Edit Pipeline

Edits existing WireframeLayout (pixel-based) using natural language instructions.
Returns a full replacement (not patches).
"""
from __future__ import annotations
import json
from typing import Optional, Tuple

from backend.config import ENABLE_SCRAPER_DEFAULT
from backend.llm.client import LlmClient
from backend.llm.json_repair import parse_json, JsonParseError
from backend.llm.prompts import EDIT_SYSTEM_PROMPT
from backend.models.wireframe import WireframeLayout
from backend.scraper.scrape import scrape_context


class EditError(Exception):
    pass


def edit_wireframe(
    layout: WireframeLayout,
    instruction: str,
    webscraper_context: Optional[str] = None,
    use_scraper: Optional[bool] = None,
) -> Tuple[WireframeLayout, Optional[str]]:
    """
    Edit an existing wireframe using natural language instruction.
    
    Returns:
        Tuple of (updated WireframeLayout, used_webscraper_context)
        
    This returns a FULL REPLACEMENT, not a patch.
    """
    should_scrape = ENABLE_SCRAPER_DEFAULT if use_scraper is None else use_scraper
    used_ctx = (webscraper_context or "").strip()

    if not used_ctx and should_scrape:
        try:
            used_ctx = scrape_context(instruction.strip())
        except Exception:
            used_ctx = ""

    layout_json = json.dumps(layout.model_dump(), ensure_ascii=False)

    prompt = (
        EDIT_SYSTEM_PROMPT
        + "\n\n"
        + (f"Web research context:\n{used_ctx}\n\n" if used_ctx else "")
        + "Existing wireframe JSON:\n"
        + layout_json
        + "\n\nInstruction:\n"
        + instruction.strip()
        + "\n\nReturn the updated wireframe JSON now:"
    )

    raw = LlmClient().generate(prompt)

    try:
        data = parse_json(raw)
    except JsonParseError as e:
        raise EditError(f"Model returned invalid JSON: {e}") from e

    try:
        new_layout = WireframeLayout.model_validate(data)
    except Exception as e:
        raise EditError(f"JSON did not match WireframeLayout schema: {e}") from e

    return new_layout, (used_ctx or None)

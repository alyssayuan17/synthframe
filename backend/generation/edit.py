"""
Wireframe Edit Pipeline

Edits existing WireframeLayout (pixel-based) using natural language instructions.
Returns a full replacement (not patches).
Supports device-specific editing.
"""
from __future__ import annotations
import json
from typing import Optional, Tuple

from backend.config import ENABLE_SCRAPER_DEFAULT, DEFAULT_DEVICE_TYPE
from backend.llm.client import LlmClient
from backend.llm.json_repair import parse_json, JsonParseError
from backend.llm.prompts import get_edit_system_prompt, EDIT_USER_TEMPLATE, get_canvas_for_device
from backend.models.wireframe import WireframeLayout, Size
from backend.scraper.scrape import scrape_context


class EditError(Exception):
    pass


def edit_wireframe(
    layout: WireframeLayout,
    instruction: str,
    webscraper_context: Optional[str] = None,
    use_scraper: Optional[bool] = None,
    device_type: Optional[str] = None,
) -> Tuple[WireframeLayout, Optional[str]]:
    """
    Edit an existing wireframe using natural language instruction.
    
    Args:
        layout: Current wireframe layout
        instruction: Edit instruction in natural language
        webscraper_context: Pre-fetched context from web scraping
        use_scraper: Whether to scrape web for context
        device_type: Target device type (preserves existing if None)
    
    Returns:
        Tuple of (updated WireframeLayout, used_webscraper_context)
        
    This returns a FULL REPLACEMENT, not a patch.
    """
    # Detect device from existing layout or use provided/default
    device = device_type or DEFAULT_DEVICE_TYPE
    canvas = get_canvas_for_device(device)
    
    should_scrape = ENABLE_SCRAPER_DEFAULT if use_scraper is None else use_scraper
    used_ctx = (webscraper_context or "").strip()

    if not used_ctx and should_scrape:
        try:
            used_ctx = scrape_context(instruction.strip())
        except Exception:
            used_ctx = ""

    layout_json = json.dumps(layout.model_dump(), ensure_ascii=False)

    # Use device-specific edit prompt
    system_prompt = get_edit_system_prompt(device)
    
    prompt = (
        system_prompt
        + "\n\n"
        + EDIT_USER_TEMPLATE.format(
            webscraper_context=used_ctx,
            wireframe_json=layout_json,
            instruction=instruction.strip(),
        )
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

    # Ensure canvas matches device
    new_layout.canvas_size = Size(width=canvas["width"], height=canvas["height"])

    return new_layout, (used_ctx or None)

"""
Text-to-Wireframe Generation Pipeline

Generates WireframeLayout (pixel-based) from natural language prompts.
Uses the same schema as the CV pipeline for frontend compatibility.
Supports device-specific generation (laptop, tablet, phone).
"""
from __future__ import annotations
from typing import Optional, Tuple

from backend.config import ENABLE_SCRAPER_DEFAULT, DEVICE_CANVAS_SIZES, DEFAULT_DEVICE_TYPE
from backend.llm.client import LlmClient
from backend.llm.prompts import get_system_prompt, USER_PROMPT_TEMPLATE, get_canvas_for_device
from backend.llm.json_repair import parse_json, JsonParseError
from backend.models.wireframe import WireframeLayout, Size
from backend.scraper.scrape import scrape_context


class GenerationError(Exception):
    pass


def generate_wireframe(
    user_input: str,
    webscraper_context: Optional[str] = None,
    use_scraper: Optional[bool] = None,
    device_type: Optional[str] = None,
) -> Tuple[WireframeLayout, Optional[str]]:
    """
    Generate a wireframe from natural language input.
    
    Args:
        user_input: Natural language description of the UI
        webscraper_context: Pre-fetched context from web scraping
        use_scraper: Whether to scrape web for context
        device_type: Target device (laptop, tablet, phone, etc.)
    
    Returns:
        Tuple of (WireframeLayout, used_webscraper_context)
        
    The WireframeLayout uses pixel-based positioning (x, y, width, height),
    same format as the CV pipeline.
    """
    user_input = user_input.strip()
    device = device_type or DEFAULT_DEVICE_TYPE
    canvas = get_canvas_for_device(device)

    should_scrape = ENABLE_SCRAPER_DEFAULT if use_scraper is None else use_scraper
    used_ctx = (webscraper_context or "").strip()

    if not used_ctx and should_scrape:
        try:
            # Include device type in scraper query for device-specific patterns
            scraper_query = f"{user_input} {device} design"
            used_ctx = scrape_context(scraper_query)
        except Exception:
            # hackathon-safe: scraper failure shouldn't kill generation
            used_ctx = ""

    # Use device-specific system prompt
    system_prompt = get_system_prompt(device)
    
    prompt = system_prompt + "\n\n" + USER_PROMPT_TEMPLATE.format(
        webscraper_context=used_ctx,
        user_input=user_input,
    )

    raw = LlmClient().generate(prompt)

    try:
        data = parse_json(raw)
    except JsonParseError as e:
        raise GenerationError(f"Model returned invalid JSON: {e}") from e

    try:
        # Parse into WireframeLayout
        layout = WireframeLayout.model_validate(data)
    except Exception as e:
        raise GenerationError(f"JSON did not match WireframeLayout schema: {e}") from e

    # Set source_type and ensure canvas size matches device
    layout.source_type = "prompt"
    layout.canvas_size = Size(width=canvas["width"], height=canvas["height"])

    return layout, (used_ctx or None)

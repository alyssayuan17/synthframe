"""
Text-to-Wireframe Generation Pipeline

Generates WireframeLayout (pixel-based) from natural language prompts.
Uses the same schema as the CV pipeline for frontend compatibility.
"""
from __future__ import annotations
from typing import Optional, Tuple

from backend.config import ENABLE_SCRAPER_DEFAULT
from backend.llm.client import LlmClient
from backend.llm.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from backend.llm.json_repair import parse_json, JsonParseError
from backend.models.wireframe import WireframeLayout
from backend.scraper.scrape import scrape_context


class GenerationError(Exception):
    pass


def generate_wireframe(
    user_input: str,
    webscraper_context: Optional[str] = None,
    use_scraper: Optional[bool] = None,
) -> Tuple[WireframeLayout, Optional[str]]:
    """
    Generate a wireframe from natural language input.
    
    Returns:
        Tuple of (WireframeLayout, used_webscraper_context)
        
    The WireframeLayout uses pixel-based positioning (x, y, width, height),
    same format as the CV pipeline.
    """
    user_input = user_input.strip()

    should_scrape = ENABLE_SCRAPER_DEFAULT if use_scraper is None else use_scraper
    used_ctx = (webscraper_context or "").strip()

    if not used_ctx and should_scrape:
        try:
            used_ctx = scrape_context(user_input)
        except Exception:
            # hackathon-safe: scraper failure shouldn't kill generation
            used_ctx = ""

    prompt = SYSTEM_PROMPT + "\n\n" + USER_PROMPT_TEMPLATE.format(
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

    # Set source_type to "prompt" for LLM-generated layouts
    layout.source_type = "prompt"

    return layout, (used_ctx or None)

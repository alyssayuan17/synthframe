"""
Text-to-Wireframe Generation Pipeline

Generates WireframeLayout (pixel-based) from natural language prompts.
Uses the same schema as the CV pipeline for frontend compatibility.
Supports device-specific generation (laptop, tablet, phone).
"""
from __future__ import annotations
from typing import Optional, Tuple

from backend.config import ENABLE_SCRAPER_DEFAULT, DEVICE_CANVAS_SIZES, DEFAULT_DEVICE_TYPE
from backend.llm.client import LlmClient, LlmError
from backend.llm.prompts import get_system_prompt, USER_PROMPT_TEMPLATE, get_canvas_for_device
from backend.llm.json_repair import parse_json, JsonParseError
from backend.models.wireframe import WireframeLayout, Size, WireframeComponent
from backend.scraper.scrape import scrape_context
import logging

logger = logging.getLogger(__name__)


class GenerationError(Exception):
    pass


def fix_overlapping_components(layout: WireframeLayout) -> WireframeLayout:
    """
    Post-process wireframe to fix overlapping components.

    Sorts components by Y position and ensures proper vertical spacing.
    This is a safety net for when the LLM generates overlapping layouts.

    Args:
        layout: The wireframe layout to fix

    Returns:
        Layout with fixed positions (no overlaps)
    """
    if not layout.components:
        return layout

    SPACING = 0  # Edge-to-edge for seamless webpage look

    # Separate full-width components (stack vertically) from positioned ones (like sidebar)
    full_width_components = []
    positioned_components = []

    canvas_width = layout.canvas_size.width if layout.canvas_size else 1440

    for comp in layout.components:
        # Consider component "full width" if it spans > 70% of canvas
        comp_width = comp.size.get("width", 200) if comp.size else 200
        comp_x = comp.position.get("x", 0) if comp.position else 0

        if comp_width > canvas_width * 0.7 or comp_x == 0 and comp_width > canvas_width * 0.5:
            full_width_components.append(comp)
        else:
            positioned_components.append(comp)

    # Sort full-width components by Y position
    full_width_components.sort(key=lambda c: c.position.get("y", 0) if c.position else 0)

    # Fix overlaps in full-width components
    current_y = 0
    for comp in full_width_components:
        comp_y = comp.position.get("y", 0) if comp.position else 0
        comp_height = comp.size.get("height", 100) if comp.size else 100

        # If this component starts before the current_y, it's overlapping
        if comp_y < current_y:
            logger.info(f"Fixing overlap: {comp.id} moved from y={comp_y} to y={current_y}")
            comp.position["y"] = current_y

        # Update current_y for next component
        actual_y = comp.position.get("y", 0)
        current_y = actual_y + comp_height + SPACING

    # Combine and return
    layout.components = full_width_components + positioned_components

    return layout


def _create_default_wireframe(device_type: str, user_input: str) -> WireframeLayout:
    """
    Create a minimal but functional default wireframe when Gemini fails.
    Returns a device-appropriate basic layout.
    
    Args:
        device_type: Target device (macbook or iphone)
        user_input: Original user request (for naming)
    
    Returns:
        A minimal WireframeLayout with basic components
    """
    canvas = get_canvas_for_device(device_type)
    components = []
    
    if device_type == "iphone":
        # iPhone layout: navbar + content section + bottom nav
        components = [
            WireframeComponent(
                id="default-nav",
                type="NAVBAR",
                position={"x": 0, "y": 0},
                size={"width": canvas["width"], "height": 56},
                props={"logo": "App", "links": []},
                source="llm",
            ),
            WireframeComponent(
                id="default-content",
                type="SECTION",
                position={"x": 16, "y": 72},
                size={"width": canvas["width"] - 32, "height": canvas["height"] - 150},
                props={"title": "Content", "content": user_input[:100]},
                source="llm",
            ),
            WireframeComponent(
                id="default-bottom-nav",
                type="BOTTOM_NAV",
                position={"x": 0, "y": canvas["height"] - 60},
                size={"width": canvas["width"], "height": 60},
                props={"items": ["Home", "Search", "Profile"]},
                source="llm",
            ),
        ]
    else:
        # MacBook layout: navbar + sidebar + main content
        components = [
            WireframeComponent(
                id="default-nav",
                type="NAVBAR",
                position={"x": 0, "y": 0},
                size={"width": canvas["width"], "height": 64},
                props={"logo": "App", "links": ["Home", "About", "Contact"], "cta": "Get Started"},
                source="llm",
            ),
            WireframeComponent(
                id="default-sidebar",
                type="SIDEBAR",
                position={"x": 0, "y": 64},
                size={"width": 240, "height": canvas["height"] - 64},
                props={"items": ["Dashboard", "Settings", "Help"]},
                source="llm",
            ),
            WireframeComponent(
                id="default-content",
                type="SECTION",
                position={"x": 260, "y": 94},
                size={"width": canvas["width"] - 280, "height": canvas["height"] - 114},
                props={"title": "Main Content", "content": user_input[:150]},
                source="llm",
            ),
        ]
    
    return WireframeLayout(
        name=f"Default Layout - {user_input[:30]}",
        canvas_size=Size(width=canvas["width"], height=canvas["height"]),
        background_color="#ffffff",
        source_type="prompt",
        components=components,
    )


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
        device_type: Target device (macbook, iphone)
    
    Returns:
        Tuple of (WireframeLayout, used_webscraper_context)
        
    The WireframeLayout uses pixel-based positioning (x, y, width, height),
    same format as the CV pipeline. Falls back to default wireframe if Gemini fails.
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

    try:
        raw = LlmClient().generate(prompt)
    except LlmError as e:
        logger.warning(f"Gemini API failed, using default wireframe: {e}")
        return _create_default_wireframe(device, user_input), (used_ctx or None)

    try:
        data = parse_json(raw)
    except JsonParseError as e:
        logger.warning(f"Gemini returned invalid JSON, using default wireframe: {e}")
        return _create_default_wireframe(device, user_input), (used_ctx or None)

    try:
        # Parse into WireframeLayout
        layout = WireframeLayout.model_validate(data)
    except Exception as e:
        logger.warning(f"JSON validation failed, using default wireframe: {e}")
        return _create_default_wireframe(device, user_input), (used_ctx or None)

    # Set source_type and ensure canvas size matches device
    layout.source_type = "prompt"
    layout.canvas_size = Size(width=canvas["width"], height=canvas["height"])

    # Fix any overlapping components (safety net for LLM mistakes)
    layout = fix_overlapping_components(layout)

    return layout, (used_ctx or None)


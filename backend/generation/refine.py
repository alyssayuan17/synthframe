"""
CV-Gemini Refinement Pipeline

Takes raw CV-detected components and uses Gemini to:
1. Improve component type classification
2. Add appropriate props
3. Optimize layout for target device
4. Suggest missing common components
"""
from __future__ import annotations
import json
import logging
from typing import Optional, List

from backend.llm.client import LlmClient, LlmError
from backend.llm.prompts import get_cv_refinement_prompt, get_canvas_for_device
from backend.llm.json_repair import parse_json, JsonParseError
from backend.models.wireframe import WireframeComponent, WireframeLayout, Size, COMPONENT_TEMPLATES
from backend.config import DEFAULT_DEVICE_TYPE

logger = logging.getLogger(__name__)


class RefinementError(Exception):
    pass


def refine_cv_components(
    detected_components: List[WireframeComponent],
    device_type: Optional[str] = None,
    original_size: Optional[tuple] = None,
) -> WireframeLayout:
    """
    Use Gemini to refine CV-detected components.
    
    Args:
        detected_components: Raw components from CV pipeline
        device_type: Target device (laptop, tablet, phone)
        original_size: Original image size (width, height)
    
    Returns:
        Refined WireframeLayout with improved component classification
    """
    device = device_type or DEFAULT_DEVICE_TYPE
    canvas = get_canvas_for_device(device)
    
    # Format detected shapes for the prompt
    shapes_data = []
    for comp in detected_components:
        shapes_data.append({
            "id": comp.id,
            "detected_type": comp.type,
            "position": {"x": comp.position.x, "y": comp.position.y},
            "size": {"width": comp.size.width, "height": comp.size.height},
            "confidence": comp.confidence or 0.5,
        })
    
    # Get device-specific refinement prompt
    prompt_template = get_cv_refinement_prompt(device)
    prompt = prompt_template.format(detected_shapes=json.dumps(shapes_data, indent=2))
    
    try:
        raw = LlmClient().generate(prompt)
        data = parse_json(raw)
    except LlmError as e:
        logger.warning(f"Gemini refinement failed, using original components: {e}")
        # Fall back to original components without refinement
        return _create_layout_from_components(detected_components, device, canvas)
    except JsonParseError as e:
        logger.warning(f"Gemini returned invalid JSON, using original: {e}")
        return _create_layout_from_components(detected_components, device, canvas)
    
    # Parse refined components
    try:
        refined_components = []
        for comp_data in data.get("components", []):
            # Add default props if not provided
            comp_type = comp_data.get("type", "SECTION")
            default_props = COMPONENT_TEMPLATES.get(comp_type, {})
            props = {**default_props, **comp_data.get("props", {})}
            
            comp = WireframeComponent(
                id=comp_data.get("id", f"comp_{len(refined_components)}"),
                type=comp_type,
                position=comp_data.get("position", {"x": 0, "y": 0}),
                size=comp_data.get("size", {"width": 100, "height": 100}),
                props=props,
                source="cv",
                confidence=comp_data.get("confidence", 0.8),
            )
            refined_components.append(comp)
        
        layout = WireframeLayout(
            name="Refined Sketch",
            canvas_size=Size(width=canvas["width"], height=canvas["height"]),
            source_type="sketch",
            components=refined_components,
        )
        
        # Log suggestions if any
        if data.get("suggested_additions"):
            logger.info(f"Gemini suggests adding: {data['suggested_additions']}")
        if data.get("layout_notes"):
            logger.info(f"Layout notes: {data['layout_notes']}")
        
        return layout
        
    except Exception as e:
        logger.warning(f"Failed to parse refined components: {e}")
        return _create_layout_from_components(detected_components, device, canvas)


def _create_layout_from_components(
    components: List[WireframeComponent],
    device: str,
    canvas: dict,
) -> WireframeLayout:
    """Create a WireframeLayout from raw components without refinement."""
    # Add default props to components
    for comp in components:
        if not comp.props:
            comp.props = COMPONENT_TEMPLATES.get(comp.type, {})
    
    return WireframeLayout(
        name="Sketch Detection",
        canvas_size=Size(width=canvas["width"], height=canvas["height"]),
        source_type="sketch",
        components=components,
    )

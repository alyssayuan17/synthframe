"""
Hybrid Text + Image Wireframe Generation

Combines CV-detected components (spatial layout) with text description (semantic meaning).
Uses Gemini to intelligently merge both inputs.
"""
from __future__ import annotations
import logging
from typing import Optional, List
import base64

from backend.config import DEFAULT_DEVICE_TYPE
from backend.llm.client import LlmClient, LlmError
from backend.llm.prompts import get_hybrid_refinement_prompt, get_canvas_for_device, get_system_prompt
from backend.llm.json_repair import parse_json, JsonParseError
from backend.models.wireframe import WireframeLayout, WireframeComponent, Size, COMPONENT_TEMPLATES
from backend.generation.generate import _create_default_wireframe

logger = logging.getLogger(__name__)


def generate_from_text_and_image(
    user_text: str,
    image_data: bytes,
    device_type: Optional[str] = None,
) -> WireframeLayout:
    """
    Generate wireframe from both text description and sketch image.
    
    Strategy:
    1. CV extracts spatial layout from image (positions, sizes)
    2. Gemini refines CV components using text for semantic guidance
    3. Multi-level fallback cascade if anything fails
    
    Args:
        user_text: Natural language description of the desired UI
        image_data: Image bytes (sketch/wireframe drawing)
        device_type: Target device (macbook or iphone)
    
    Returns:
        WireframeLayout combining spatial accuracy from image and
        semantic clarity from text description
        
    Fallback cascade:
    - Best: CV components + text refinement (Gemini)
    - Good: Raw CV components (if refinement fails)
    - Okay: Text-only generation (if CV fails)
    - Safe: Device default (if everything fails)
    """
    device = device_type or DEFAULT_DEVICE_TYPE
    canvas = get_canvas_for_device(device)
    user_text = user_text.strip()
    
    # Step 1: Try CV pipeline on image
    cv_components = None
    try:
        logger.info("Running CV pipeline on image...")
        from backend.vision.image_to_text import analyze_sketch
        import base64
        
        # Encode image to base64 as expected by analyze_sketch
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Analyze sketch
        result = analyze_sketch(image_b64, device_type=device)
        
        if result and result.wireframe and result.wireframe.components:
            # Convert Component to WireframeComponent format
            from backend.models.wireframe import WireframeComponent
            cv_components = []
            for comp in result.wireframe.components:
                wf_comp = WireframeComponent(
                    id=comp.id,
                    type=comp.type,
                    position={"x": comp.position.x, "y": comp.position.y},
                    size={"width": comp.size.width, "height": comp.size.height},
                    props=comp.props or {},
                    source="cv",
                    confidence=0.7,
                )
                cv_components.append(wf_comp)
            
            logger.info(f"CV detected {len(cv_components)} components")
        else:
            logger.warning("CV analysis returned no components")
            cv_components = None
        
    except Exception as e:
        logger.warning(f"CV pipeline failed: {e}")
        cv_components = None
    
    # Step 2: Choose strategy based on CV success
    if cv_components:
        # Strategy A: CV succeeded → Refine with text guidance
        try:
            logger.info("Refining CV components with text guidance via Gemini...")
            refined_layout = _refine_cv_with_text(cv_components, user_text, device)
            logger.info("Successfully merged CV + text via Gemini")
            return refined_layout
            
        except Exception as e:
            logger.warning(f"Gemini refinement failed: {e}")
            # Fallback: Return raw CV components
            logger.info("Falling back to raw CV components")
            return _create_layout_from_cv_components(cv_components, device, canvas)
    
    else:
        # Strategy B: CV failed → Try text-only generation
        logger.info("CV failed, attempting text-only generation...")
        try:
            from backend.generation.generate import generate_wireframe
            layout, _ = generate_wireframe(user_text, device_type=device)
            logger.info("Successfully generated from text only")
            return layout
            
        except Exception as e:
            logger.warning(f"Text-only generation also failed: {e}")
            # Final fallback: Device default
            logger.info("Falling back to device default wireframe")
            return _create_default_wireframe(device, user_text)


def _refine_cv_with_text(
    cv_components: List[WireframeComponent],
    user_text: str,
    device: str,
) -> WireframeLayout:
    """
    Use Gemini to refine CV components with text guidance.
    
    Args:
        cv_components: Components detected by CV
        user_text: User's text description
        device: Target device type
    
    Returns:
        Refined WireframeLayout
    """
    canvas = get_canvas_for_device(device)
    
    # Format CV components for prompt
    import json
    cv_data = []
    for comp in cv_components:
        cv_data.append({
            "id": comp.id,
            "detected_type": comp.type,
            "position": {"x": comp.position.x, "y": comp.position.y},
            "size": {"width": comp.size.width, "height": comp.size.height},
            "confidence": comp.confidence or 0.5,
        })
    
    # Get hybrid refinement prompt
    prompt_template = get_hybrid_refinement_prompt(device)
    prompt = prompt_template.format(
        user_text=user_text,
        detected_components=json.dumps(cv_data, indent=2)
    )
    
    # Call Gemini
    raw = LlmClient().generate(prompt)
    data = parse_json(raw)
    
    # Parse refined components
    refined_components = []
    for comp_data in data.get("components", []):
        comp_type = comp_data.get("type", "SECTION")
        default_props = COMPONENT_TEMPLATES.get(comp_type, {})
        props = {**default_props, **comp_data.get("props", {})}
        
        comp = WireframeComponent(
            id=comp_data.get("id", f"comp_{len(refined_components)}"),
            type=comp_type,
            position=comp_data.get("position", {"x": 0, "y": 0}),
            size=comp_data.get("size", {"width": 100, "height": 100}),
            props=props,
            source="hybrid",
            confidence=comp_data.get("confidence", 0.8),
        )
        refined_components.append(comp)
    
    layout = WireframeLayout(
        name=data.get("name", "Hybrid Wireframe"),
        canvas_size=Size(width=canvas["width"], height=canvas["height"]),
        source_type="hybrid",
        components=refined_components,
    )
    
    return layout


def _create_layout_from_cv_components(
    components: List[WireframeComponent],
    device: str,
    canvas: dict,
) -> WireframeLayout:
    """Create WireframeLayout from raw CV components without refinement."""
    for comp in components:
        if not comp.props:
            comp.props = COMPONENT_TEMPLATES.get(comp.type, {})
        comp.source = "cv"
    
    return WireframeLayout(
        name="CV Detection",
        canvas_size=Size(width=canvas["width"], height=canvas["height"]),
        source_type="sketch",
        components=components,
    )

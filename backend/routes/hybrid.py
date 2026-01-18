"""
Hybrid Text + Image Generation Route

Accepts both text description and sketch image simultaneously.
"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional
import logging

from backend.generation.hybrid import generate_from_text_and_image
from backend.models.responses import WireframeResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/hybrid", response_model=WireframeResponse)
async def generate_hybrid(
    text: str = Form(..., description="Text description of the desired UI"),
    image: UploadFile = File(..., description="Hand-drawn sketch or wireframe image"),
    device_type: Optional[str] = Form("macbook", description="Target device (macbook or iphone)"),
):
    """
    Generate wireframe from both text and image.
    
    **Strategy:**
    - CV extracts spatial layout from the sketch (positions, sizes)
    - Gemini refines using text for semantic meaning (types, props)
    - Result combines best of both: accurate positioning + clear semantics
    
    **Fallback Cascade:**
    1. CV + Text refinement (best)
    2. Raw CV components (if refinement fails)
    3. Text-only generation (if CV fails)
    4. Device default (if everything fails)
    
    Returns a WireframeResponse with the merged result.
    """
    try:
        # Read image data
        image_bytes = await image.read()
        
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Image file is empty")
        
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Text description cannot be empty")
        
        # Generate hybrid wireframe
        logger.info(f"Generating hybrid wireframe for device: {device_type}")
        layout = generate_from_text_and_image(
            user_text=text,
            image_data=image_bytes,
            device_type=device_type,
        )
        
        return WireframeResponse(wireframe=layout)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Hybrid generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

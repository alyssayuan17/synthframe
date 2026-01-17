"""
Generate Route - POST /generate
Text prompt to wireframe generation with optional webscraper context.
"""
from fastapi import APIRouter, HTTPException

from backend.generation.generate import generate_wireframe, GenerationError
from backend.models.requests import GenerateRequest
from backend.models.responses import GenerateResponse, ErrorResponse

router = APIRouter(tags=["Generation"])


@router.post(
    "/generate",
    response_model=GenerateResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Generate wireframe from text prompt"
)
async def generate(request: GenerateRequest):
    """
    Generate a UI wireframe from a natural language description.
    
    - **user_input**: Description like "create a SaaS dashboard" or "make a login page"
    - **webscraper_context**: Optional pre-fetched context (e.g., "like Airbnb")
    - **use_scraper**: If True, scrape web for design patterns. Default from config.
    - **device_type**: Target device (laptop, tablet, phone). Defaults to laptop.
    
    Returns a WireframeLayout with pixel-based positioning (same format as CV pipeline).
    """
    try:
        layout, used_context = generate_wireframe(
            user_input=request.user_input,
            webscraper_context=request.webscraper_context,
            use_scraper=request.use_scraper,
            device_type=request.device_type,
        )
        
        return GenerateResponse(
            success=True,
            wireframe_layout=layout,
            used_webscraper_context=used_context,
            message=f"Generated wireframe with {len(layout.components)} components"
        )
        
    except GenerationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

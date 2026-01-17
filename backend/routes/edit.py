"""
Edit Route - POST /edit
Edit existing wireframe with natural language instruction (full replacement).
"""
from fastapi import APIRouter, HTTPException

from backend.generation.edit import edit_wireframe, EditError
from backend.models.requests import EditWireframeRequest
from backend.models.responses import EditWireframeResponse, ErrorResponse

router = APIRouter(tags=["Edit"])


@router.post(
    "/edit",
    response_model=EditWireframeResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Edit wireframe with instruction"
)
async def edit(request: EditWireframeRequest):
    """
    Edit an existing wireframe using natural language instruction.
    
    - **wireframe_layout**: The current wireframe layout to modify
    - **instruction**: Edit instruction like "add a settings tab" or "move sidebar to right"
    - **webscraper_context**: Optional context for design patterns
    - **use_scraper**: Whether to scrape web for context
    - **device_type**: Target device for the edited wireframe
    
    Returns a FULL REPLACEMENT wireframe (not a patch).
    """
    try:
        new_layout, used_context = edit_wireframe(
            layout=request.wireframe_layout,
            instruction=request.instruction,
            webscraper_context=request.webscraper_context,
            use_scraper=request.use_scraper,
            device_type=request.device_type,
        )
        
        return EditWireframeResponse(
            success=True,
            wireframe_layout=new_layout,
            used_webscraper_context=used_context,
            message="Wireframe edited successfully"
        )
        
    except EditError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Edit failed: {str(e)}")

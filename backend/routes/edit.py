"""
Edit Route - POST /edit
Edit existing wireframe with natural language instruction (full replacement).
Updates MongoDB if project_id provided.
"""
from fastapi import APIRouter, HTTPException

from backend.generation.edit import edit_wireframe, EditError
from backend.models.requests import EditWireframeRequest
from backend.models.responses import EditWireframeResponse, ErrorResponse
from backend.database.operations import update_project, get_project, DatabaseError
from backend.database.models import ProjectUpdate

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
    
    - **project_id**: Optional MongoDB project ID (if provided, updates that project)
    - **wireframe_layout**: The current wireframe layout to modify
    - **instruction**: Edit instruction like "add a settings tab" or "move sidebar to right"
    - **webscraper_context**: Optional context for design patterns
    - **use_scraper**: Whether to scrape web for context
    - **device_type**: Target device for the edited wireframe
    
    Returns a FULL REPLACEMENT wireframe (not a patch).
    If project_id provided, updates MongoDB project.
    """
    try:
        new_layout, used_context = edit_wireframe(
            layout=request.wireframe_layout,
            instruction=request.instruction,
            webscraper_context=request.webscraper_context,
            use_scraper=request.use_scraper,
            device_type=request.device_type,
        )
        
        # Update MongoDB if project_id provided
        project_id = request.project_id
        if project_id:
            try:
                existing_project = await get_project(project_id)
                if existing_project:
                    update_data = ProjectUpdate(
                        wireframe=new_layout,
                        device_type=request.device_type
                    )
                    await update_project(
                        project_id,
                        update_data,
                        add_to_history=True,
                        history_instruction=request.instruction
                    )
                else:
                    # Project not found, return wireframe without saving
                    project_id = None
            except DatabaseError as db_err:
                # If database fails, still return wireframe
                print(f"Warning: Failed to update project in MongoDB: {db_err}")
        
        return EditWireframeResponse(
            success=True,
            project_id=project_id,
            wireframe_layout=new_layout,
            used_webscraper_context=used_context,
            message="Wireframe edited successfully"
        )
        
    except EditError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Edit failed: {str(e)}")

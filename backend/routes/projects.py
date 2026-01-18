"""
Projects Route - Project Management Endpoints
==============================================

Endpoints for CRUD operations on wireframe projects:
- GET /projects - List all projects
- GET /projects/{id} - Get specific project
- POST /projects/{id}/save - Manual save (Option B)
- PATCH /projects/{id}/rename - Rename project
- DELETE /projects/{id} - Delete project
- GET /projects/stats - Get stats (count, etc.)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional

from backend.database.operations import (
    get_project,
    list_projects,
    update_project,
    delete_project,
    rename_project,
    count_projects,
    DatabaseError
)
from backend.database.models import Project, ProjectSummary, ProjectUpdate
from backend.models.responses import ErrorResponse
from backend.models.wireframe import WireframeLayout


router = APIRouter(prefix="/projects", tags=["Projects"])


# =============================================================================
# REQUEST MODELS
# =============================================================================

class SaveProjectRequest(BaseModel):
    """Request body for manual save"""
    name: Optional[str] = Field(None, description="Updated project name")
    wireframe: WireframeLayout = Field(..., description="Current wireframe state")
    instruction: Optional[str] = Field(None, description="What changed (for history)")


class RenameRequest(BaseModel):
    """Request body for rename"""
    name: str = Field(..., description="New project name")


# =============================================================================
# LIST PROJECTS
# =============================================================================

@router.get(
    "",
    response_model=List[ProjectSummary],
    summary="List all projects"
)
async def get_projects(
    limit: int = Query(50, description="Max results to return"),
    skip: int = Query(0, description="Number to skip (pagination)"),
    sort_by: str = Query("updated_at", description="Field to sort by"),
    sort_order: int = Query(-1, description="-1 for newest first, 1 for oldest")
):
    """
    Get list of all projects (lightweight - no full wireframe data).
    
    Returns project summaries with:
    - ID, name, timestamps
    - Generation method, device type
    - Component count
    
    For full wireframe data, use GET /projects/{id}
    """
    try:
        projects = await list_projects(
            limit=limit,
            skip=skip,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return projects
        
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# GET PROJECT BY ID
# =============================================================================

@router.get(
    "/{project_id}",
    response_model=Project,
    responses={404: {"model": ErrorResponse}},
    summary="Get project by ID"
)
async def get_project_by_id(project_id: str):
    """
    Get full project data including complete wireframe.
    
    This is what the frontend calls on page load to restore state.
    """
    try:
        project = await get_project(project_id)
        
        if project is None:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        
        return project
        
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# MANUAL SAVE (OPTION B)
# =============================================================================

@router.post(
    "/{project_id}/save",
    response_model=Project,
    responses={404: {"model": ErrorResponse}},
    summary="Manual save (Option B)"
)
async def save_project(project_id: str, request: SaveProjectRequest):
    """
    Manually save project changes.
    
    The frontend calls this when user clicks "Save" button.
    Updates the wireframe and optionally the name.
    """
    try:
        # Check if project exists
        existing = await get_project(project_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        
        # Build update
        update_data = ProjectUpdate(
            wireframe=request.wireframe,
            name=request.name if request.name else existing.name
        )
        
        # Update in database
        updated = await update_project(
            project_id,
            update_data,
            add_to_history=True,
            history_instruction=request.instruction or "Manual save"
        )
        
        return updated
        
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# RENAME PROJECT
# =============================================================================

@router.patch(
    "/{project_id}/rename",
    response_model=Project,
    responses={404: {"model": ErrorResponse}},
    summary="Rename project"
)
async def rename_project_endpoint(project_id: str, request: RenameRequest):
    """
    Rename a project.
    
    The frontend can call this when user edits the project name field.
    """
    try:
        project = await rename_project(project_id, request.name)
        
        if project is None:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        
        return project
        
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# DELETE PROJECT
# =============================================================================

@router.delete(
    "/{project_id}",
    responses={404: {"model": ErrorResponse}},
    summary="Delete project"
)
async def delete_project_endpoint(project_id: str):
    """
    Delete a project permanently.
    """
    try:
        deleted = await delete_project(project_id)
        
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        
        return {"success": True, "message": f"Project {project_id} deleted"}
        
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# PROJECT STATS
# =============================================================================

@router.get(
    "/stats/summary",
    summary="Get project statistics"
)
async def get_project_stats():
    """
    Get aggregate statistics about projects.
    
    Returns:
    - Total project count
    - Other stats (can expand later)
    """
    try:
        total = await count_projects()
        
        return {
            "total_projects": total,
            "status": "ok"
        }
        
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

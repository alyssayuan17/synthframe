"""
Database CRUD Operations
=========================

All MongoDB operations for projects.

USAGE:
    from backend.database.operations import create_project, get_project
    
    project_id = await create_project(wireframe, "My Dashboard")
    project = await get_project(project_id)
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pymongo.errors import DuplicateKeyError

from backend.database import get_projects_collection
from backend.database.models import Project, ProjectSummary, ProjectUpdate, EditHistoryEntry
from backend.models.wireframe import WireframeLayout


class DatabaseError(Exception):
    """Raised when database operations fail"""
    pass


async def create_project(
    wireframe: WireframeLayout,
    name: Optional[str] = None,
    generation_method: str = "text_prompt",
    device_type: str = "laptop",
    original_prompt: Optional[str] = None,
    webscraper_context: Optional[str] = None,
    user_id: Optional[str] = None
) -> Project:
    """
    Create a new project in MongoDB.
    
    Args:
        wireframe: The WireframeLayout object
        name: Project name (auto-generated if None)
        generation_method: How it was created
        device_type: Target device
        original_prompt: User's input text
        webscraper_context: Scraped context used
        user_id: Optional user ID for multi-user
        
    Returns:
        Created Project object with ID
        
    Raises:
        DatabaseError: If creation fails
    """
    try:
        # Auto-generate name if not provided
        if not name:
            name = f"Untitled Project {datetime.utcnow().strftime('%m/%d %H:%M')}"
        
        # Create project object
        project = Project(
            name=name,
            wireframe=wireframe,
            generation_method=generation_method,
            device_type=device_type,
            original_prompt=original_prompt,
            webscraper_context=webscraper_context,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        # Insert into MongoDB
        collection = get_projects_collection()
        
        # Convert to dict and handle _id alias
        project_dict = project.model_dump(by_alias=True)
        
        await collection.insert_one(project_dict)
        
        return project
        
    except DuplicateKeyError:
        raise DatabaseError("Project with this ID already exists")
    except Exception as e:
        raise DatabaseError(f"Failed to create project: {str(e)}")


async def get_project(project_id: str) -> Optional[Project]:
    """
    Get a project by ID.
    
    Args:
        project_id: Project UUID
        
    Returns:
        Project object or None if not found
    """
    try:
        collection = get_projects_collection()
        doc = await collection.find_one({"_id": project_id})
        
        if doc is None:
            return None
        
        return Project(**doc)
        
    except Exception as e:
        raise DatabaseError(f"Failed to get project: {str(e)}")


async def list_projects(
    user_id: Optional[str] = None,
    limit: int = 50,
    skip: int = 0,
    sort_by: str = "updated_at",
    sort_order: int = -1  # -1 = descending, 1 = ascending
) -> List[ProjectSummary]:
    """
    List all projects (or filter by user_id).
    
    Args:
        user_id: Filter by user (None = all projects)
        limit: Max results to return
        skip: Number to skip (for pagination)
        sort_by: Field to sort by
        sort_order: -1 (newest first) or 1 (oldest first)
        
    Returns:
        List of ProjectSummary objects
    """
    try:
        collection = get_projects_collection()
        
        # Build query filter
        query = {}
        if user_id:
            query["user_id"] = user_id
        
        # Query with projection to exclude full wireframe
        cursor = collection.find(
            query,
            {
                "_id": 1,
                "name": 1,
                "generation_method": 1,
                "device_type": 1,
                "created_at": 1,
                "updated_at": 1,
                "wireframe.components": 1  # Only get component count
            }
        ).sort(sort_by, sort_order).skip(skip).limit(limit)
        
        projects = []
        async for doc in cursor:
            # Count components
            component_count = len(doc.get("wireframe", {}).get("components", []))
            
            summary = ProjectSummary(
                _id=doc["_id"],
                name=doc.get("name", "Untitled"),
                generation_method=doc.get("generation_method", "unknown"),
                device_type=doc.get("device_type", "laptop"),
                created_at=doc.get("created_at", datetime.utcnow()),
                updated_at=doc.get("updated_at", datetime.utcnow()),
                component_count=component_count
            )
            projects.append(summary)
        
        return projects
        
    except Exception as e:
        raise DatabaseError(f"Failed to list projects: {str(e)}")


async def update_project(
    project_id: str,
    update_data: ProjectUpdate,
    add_to_history: bool = True,
    history_instruction: Optional[str] = None
) -> Optional[Project]:
    """
    Update a project's fields.
    
    Args:
        project_id: Project UUID
        update_data: Fields to update
        add_to_history: Whether to log this change
        history_instruction: Description of change
        
    Returns:
        Updated Project or None if not found
    """
    try:
        collection = get_projects_collection()
        
        # Build update document
        update_dict = update_data.model_dump(exclude_unset=True, by_alias=True)
        
        if not update_dict:
            # Nothing to update
            return await get_project(project_id)
        
        # Always update timestamp
        update_dict["updated_at"] = datetime.utcnow()
        
        # Add to edit history if requested
        if add_to_history and history_instruction:
            history_entry = EditHistoryEntry(
                timestamp=datetime.utcnow(),
                instruction=history_instruction,
                components_changed=len(update_data.wireframe.components) if update_data.wireframe else 0,
                method="edit"
            )
            
            await collection.update_one(
                {"_id": project_id},
                {
                    "$set": update_dict,
                    "$push": {"edit_history": history_entry.model_dump()}
                }
            )
        else:
            await collection.update_one(
                {"_id": project_id},
                {"$set": update_dict}
            )
        
        # Return updated project
        return await get_project(project_id)
        
    except Exception as e:
        raise DatabaseError(f"Failed to update project: {str(e)}")


async def delete_project(project_id: str) -> bool:
    """
    Delete a project.
    
    Args:
        project_id: Project UUID
        
    Returns:
        True if deleted, False if not found
    """
    try:
        collection = get_projects_collection()
        result = await collection.delete_one({"_id": project_id})
        return result.deleted_count > 0
        
    except Exception as e:
        raise DatabaseError(f"Failed to delete project: {str(e)}")


async def rename_project(project_id: str, new_name: str) -> Optional[Project]:
    """
    Rename a project (convenience method).
    
    Args:
        project_id: Project UUID
        new_name: New project name
        
    Returns:
        Updated Project or None if not found
    """
    update_data = ProjectUpdate(name=new_name)
    return await update_project(project_id, update_data, add_to_history=False)


async def count_projects(user_id: Optional[str] = None) -> int:
    """
    Count total projects.
    
    Args:
        user_id: Filter by user (None = all)
        
    Returns:
        Number of projects
    """
    try:
        collection = get_projects_collection()
        query = {"user_id": user_id} if user_id else {}
        return await collection.count_documents(query)
        
    except Exception as e:
        raise DatabaseError(f"Failed to count projects: {str(e)}")

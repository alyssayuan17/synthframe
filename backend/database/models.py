"""
Database Models
===============

Pydantic models for MongoDB documents.

MongoDB stores BSON (similar to JSON), so we use Pydantic models
to validate and serialize data between FastAPI and MongoDB.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
import uuid

from backend.models.wireframe import WireframeLayout


def generate_project_id() -> str:
    """Generate unique project ID"""
    return str(uuid.uuid4())


class EditHistoryEntry(BaseModel):
    """Single entry in edit history"""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    instruction: str = Field(..., description="What the user asked for")
    components_changed: int = Field(default=0, description="Number of components modified")
    method: str = Field(default="edit", description="How it was changed (edit, generate, etc.)")


class Project(BaseModel):
    """
    Project document stored in MongoDB.
    
    Each project represents one wireframe with metadata and history.
    """
    id: str = Field(default_factory=generate_project_id, alias="_id")
    name: str = Field(default="Untitled Project", description="User-editable project name")
    
    # The actual wireframe data
    wireframe: WireframeLayout = Field(..., description="The wireframe layout with all components")
    
    # Metadata
    generation_method: Literal["text_prompt", "cv_sketch", "mockup", "edit"] = Field(
        default="text_prompt",
        description="How this wireframe was created"
    )
    device_type: str = Field(default="laptop", description="Target device type")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Edit history for undo/redo (future feature)
    edit_history: List[EditHistoryEntry] = Field(default_factory=list)
    
    # Optional: User context if you add auth later
    user_id: Optional[str] = Field(default=None, description="Owner user ID (for multi-user)")
    
    # Original prompt/context for reference
    original_prompt: Optional[str] = Field(default=None, description="Original user input")
    webscraper_context: Optional[str] = Field(default=None, description="Context from web scraper")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "name": "Student Club Dashboard",
                "wireframe": {
                    "id": "wireframe-uuid",
                    "name": "Student Club Dashboard",
                    "canvas_size": {"width": 1440, "height": 900},
                    "source_type": "prompt",
                    "components": []
                },
                "generation_method": "text_prompt",
                "device_type": "laptop",
                "created_at": "2026-01-17T10:30:00",
                "updated_at": "2026-01-17T11:45:00",
                "edit_history": [],
                "original_prompt": "Create a dashboard for a student club"
            }
        }


class ProjectSummary(BaseModel):
    """
    Lightweight project info for listing (doesn't include full wireframe).
    """
    id: str = Field(alias="_id")
    name: str
    generation_method: str
    device_type: str
    created_at: datetime
    updated_at: datetime
    component_count: int = Field(default=0, description="Number of components in wireframe")
    thumbnail_url: Optional[str] = Field(default=None, description="Preview image (future)")
    
    class Config:
        populate_by_name = True


class ProjectUpdate(BaseModel):
    """
    Model for updating project fields.
    All fields optional so you can update only what's needed.
    """
    name: Optional[str] = None
    wireframe: Optional[WireframeLayout] = None
    device_type: Optional[str] = None
    original_prompt: Optional[str] = None
    
    class Config:
        populate_by_name = True

"""
Response Models for the Wireframe API
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .wireframe import WireframeLayout, CVDetectionResult


class WireframeResponse(BaseModel):
    """Standard response containing a wireframe"""
    success: bool = True
    project_id: Optional[str] = Field(None, description="MongoDB project ID for persistence")
    wireframe: WireframeLayout
    message: Optional[str] = None
    processing_time_ms: float = 0


class CVDetectionResponse(BaseModel):
    """Response for CV detection (raw results before wireframe conversion)"""
    success: bool = True
    detection: CVDetectionResult
    message: Optional[str] = None


class CritiqueItem(BaseModel):
    """Single critique/suggestion item"""
    category: str = Field(..., description="Category: spacing, contrast, alignment, etc.")
    severity: str = Field(..., description="low, medium, high")
    component_id: Optional[str] = Field(default=None, description="Affected component")
    message: str = Field(..., description="Description of the issue")
    suggestion: str = Field(..., description="How to fix it")


class CritiqueResponse(BaseModel):
    """Response for design critique"""
    success: bool = True
    wireframe_id: str
    overall_score: float = Field(..., ge=0, le=100, description="Overall design score")
    critiques: List[CritiqueItem] = Field(default_factory=list)
    summary: str = Field(default="", description="Summary of the design review")


class EditResponse(BaseModel):
    """Response for edit operations"""
    success: bool = True
    wireframe: WireframeLayout
    changes_made: List[str] = Field(default_factory=list, description="List of changes applied")
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str = "0.1.0"
    services: Dict[str, bool] = Field(default_factory=dict)


# =============================================================================
# LLM TEXT-TO-WIREFRAME PIPELINE RESPONSES
# =============================================================================

class GenerateResponse(BaseModel):
    """Response from text-to-wireframe generation"""
    success: bool = True
    project_id: Optional[str] = Field(None, description="MongoDB project ID for persistence")
    wireframe_layout: WireframeLayout
    used_webscraper_context: Optional[str] = None
    message: Optional[str] = None


class EditWireframeResponse(BaseModel):
    """Response from wireframe edit operation"""
    success: bool = True
    project_id: Optional[str] = Field(None, description="MongoDB project ID for persistence")
    wireframe_layout: WireframeLayout
    used_webscraper_context: Optional[str] = None
    message: Optional[str] = None


class ScrapeResponse(BaseModel):
    """Debug response for webscraper testing"""
    success: bool = True
    context: str
    pages_scraped: int = 0

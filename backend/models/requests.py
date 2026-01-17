"""
Request Models for the Wireframe API
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field

from .wireframe import WireframeLayout


class ImageUploadRequest(BaseModel):
    """Request for image-based wireframe generation (CV pipeline)"""
    image_base64: str = Field(..., description="Base64 encoded image data")
    image_type: Optional[Literal["sketch", "mockup", "auto"]] = Field(
        default="auto", 
        description="Type of image being uploaded"
    )
    detect_text: bool = Field(default=True, description="Whether to run OCR")
    min_component_area: int = Field(default=500, description="Minimum area for component detection")
    name: str = Field(default="Untitled Wireframe", description="Name for the wireframe")


class TextPromptRequest(BaseModel):
    """Request for text-based wireframe generation (legacy)"""
    prompt: str = Field(..., description="Natural language description")
    context: Optional[str] = Field(default=None, description="Additional context")
    style: Optional[str] = Field(default="modern", description="Design style preference")


class GenerateRequest(BaseModel):
    """Request for text-to-wireframe generation with webscraper support"""
    user_input: str = Field(..., description="Natural language description of the UI")
    webscraper_context: Optional[str] = Field(
        default=None, 
        description="Pre-fetched context from web scraping"
    )
    use_scraper: Optional[bool] = Field(
        default=None, 
        description="Whether to scrape web for context. None = use default setting"
    )


class EditWireframeRequest(BaseModel):
    """Request to edit existing wireframe (full replacement)"""
    wireframe_layout: WireframeLayout = Field(..., description="Current wireframe layout")
    instruction: str = Field(..., description="Edit instruction in natural language")
    webscraper_context: Optional[str] = Field(default=None)
    use_scraper: Optional[bool] = Field(default=None)


class ScrapeRequest(BaseModel):
    """Debug endpoint to test webscraper"""
    query: str = Field(..., description="Search query for scraper")
    max_pages: Optional[int] = Field(default=None, description="Override max pages to scrape")


class EditRequest(BaseModel):
    """Request to edit an existing wireframe (legacy CV-based)"""
    wireframe_id: str = Field(..., description="ID of wireframe to edit")
    instruction: str = Field(..., description="Edit instruction")
    component_id: Optional[str] = Field(default=None, description="Specific component to edit")


class CritiqueRequest(BaseModel):
    """Request for design critique/suggestions"""
    wireframe_id: str = Field(..., description="ID of wireframe to critique")
    focus_areas: Optional[List[str]] = Field(
        default=None, 
        description="Areas to focus critique on",
        examples=[["spacing", "contrast", "alignment", "consistency"]]
    )

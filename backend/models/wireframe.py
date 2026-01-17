"""
Wireframe Component Schema - The standard format for all UI components.
This is what the CV/Image processing outputs and what the frontend expects.
"""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from enum import Enum


class ComponentType(str, Enum):
    """All supported wireframe component types"""
    # Layout Components
    CONTAINER = "container"
    ROW = "row"
    COLUMN = "column"
    GRID = "grid"
    
    # Navigation
    NAVBAR = "navbar"
    SIDEBAR = "sidebar"
    FOOTER = "footer"
    BREADCRUMB = "breadcrumb"
    TABS = "tabs"
    
    # Content
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    IMAGE = "image"
    ICON = "icon"
    DIVIDER = "divider"
    CARD = "card"
    
    # Interactive
    BUTTON = "button"
    LINK = "link"
    INPUT = "input"
    TEXTAREA = "textarea"
    SELECT = "select"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    TOGGLE = "toggle"
    SLIDER = "slider"
    
    # Forms
    FORM = "form"
    LOGIN_FORM = "login_form"
    SIGNUP_FORM = "signup_form"
    SEARCH_BAR = "search_bar"
    
    # Data Display
    TABLE = "table"
    LIST = "list"
    CALENDAR = "calendar"
    CHART = "chart"
    PROGRESS_BAR = "progress_bar"
    BADGE = "badge"
    AVATAR = "avatar"
    
    # Feedback
    MODAL = "modal"
    TOAST = "toast"
    TOOLTIP = "tooltip"
    ALERT = "alert"
    
    # Unknown/Generic
    BOX = "box"
    TEXT = "text"
    UNKNOWN = "unknown"


class Position(BaseModel):
    """Position of a component on the canvas"""
    x: float = Field(..., description="X coordinate (pixels from left)")
    y: float = Field(..., description="Y coordinate (pixels from top)")


class Size(BaseModel):
    """Size of a component"""
    width: float = Field(..., description="Width in pixels or percentage")
    height: float = Field(..., description="Height in pixels or percentage")


class BoundingBox(BaseModel):
    """Bounding box detected from CV"""
    x: float
    y: float
    width: float
    height: float
    confidence: float = Field(default=1.0, ge=0, le=1)


class DetectedText(BaseModel):
    """Text detected within a component"""
    content: str
    bounding_box: BoundingBox
    confidence: float = Field(default=1.0, ge=0, le=1)


class WireframeComponent(BaseModel):
    """A single UI component in the wireframe"""
    id: str = Field(..., description="Unique identifier for the component")
    type: ComponentType = Field(..., description="Type of UI component")
    position: Position = Field(..., description="Position on canvas")
    size: Size = Field(..., description="Size of component")
    props: Dict[str, Any] = Field(default_factory=dict, description="Component-specific properties")
    children: List[str] = Field(default_factory=list, description="IDs of child components")
    detected_text: Optional[str] = Field(default=None, description="Text detected in this component")
    confidence: float = Field(default=1.0, ge=0, le=1, description="Detection confidence")
    source: Literal["cv", "llm", "user"] = Field(default="cv", description="How this component was created")


class WireframeLayout(BaseModel):
    """Complete wireframe layout with all components"""
    id: str = Field(..., description="Unique layout identifier")
    name: str = Field(default="Untitled Wireframe")
    canvas_size: Size = Field(..., description="Total canvas dimensions")
    background_color: str = Field(default="#ffffff")
    components: List[WireframeComponent] = Field(default_factory=list)
    
    # Metadata
    source_type: Literal["sketch", "mockup", "prompt", "manual"] = Field(default="sketch")
    original_image_path: Optional[str] = None
    created_at: Optional[str] = None


class CVDetectionResult(BaseModel):
    """Raw output from CV detection before component classification"""
    bounding_boxes: List[BoundingBox] = Field(default_factory=list)
    detected_texts: List[DetectedText] = Field(default_factory=list)
    image_dimensions: Size
    processing_time_ms: float = 0


# Component templates with default properties
COMPONENT_TEMPLATES: Dict[ComponentType, Dict[str, Any]] = {
    ComponentType.NAVBAR: {
        "default_size": {"width": "100%", "height": 64},
        "props": {"logo": "Logo", "links": ["Home", "About", "Contact"]}
    },
    ComponentType.BUTTON: {
        "default_size": {"width": 120, "height": 40},
        "props": {"label": "Button", "variant": "primary"}
    },
    ComponentType.HEADING: {
        "default_size": {"width": 300, "height": 40},
        "props": {"text": "Heading", "level": 1}
    },
    ComponentType.INPUT: {
        "default_size": {"width": 250, "height": 40},
        "props": {"placeholder": "Enter text...", "type": "text"}
    },
    ComponentType.CARD: {
        "default_size": {"width": 300, "height": 200},
        "props": {"title": "Card Title", "content": "Card content goes here"}
    },
    ComponentType.IMAGE: {
        "default_size": {"width": 200, "height": 150},
        "props": {"alt": "Image", "src": ""}
    },
    ComponentType.CALENDAR: {
        "default_size": {"width": 300, "height": 300},
        "props": {"view": "month"}
    },
    ComponentType.TABLE: {
        "default_size": {"width": 500, "height": 300},
        "props": {"columns": ["Column 1", "Column 2", "Column 3"], "rows": 5}
    },
    ComponentType.CHART: {
        "default_size": {"width": 400, "height": 300},
        "props": {"type": "bar", "title": "Chart"}
    },
    ComponentType.LOGIN_FORM: {
        "default_size": {"width": 350, "height": 300},
        "props": {"fields": ["email", "password"], "submit_label": "Login"}
    },
    ComponentType.SIDEBAR: {
        "default_size": {"width": 250, "height": "100%"},
        "props": {"items": ["Dashboard", "Settings", "Profile"]}
    },
    ComponentType.FOOTER: {
        "default_size": {"width": "100%", "height": 80},
        "props": {"copyright": "© 2025", "links": ["Privacy", "Terms"]}
    }
}


# =============================================================================
# LLM-GENERATED WIREFRAME SCHEMA (12-column grid)
# Coexists with the CV-based WireframeLayout above
# =============================================================================

class GridPosition(BaseModel):
    """12-column grid position for LLM-generated components"""
    row: int = 0
    col: int = Field(ge=0, lt=12, default=0)
    colSpan: int = Field(ge=1, le=12, default=12)


class Layout(BaseModel):
    """Layout configuration for wireframe document"""
    type: Literal["full-width", "sidebar-main", "dashboard", "landing", "form-page"]
    direction: str = "horizontal"


class Theme(BaseModel):
    """Theme configuration"""
    style: str = "modern"
    primaryColor: str = "#6366f1"


class Endpoint(BaseModel):
    """Connection endpoint reference"""
    componentId: str
    anchor: Literal["top", "right", "bottom", "left"]


class Connection(BaseModel):
    """Connection between components (for interaction flows)"""
    id: str = ""
    from_: Endpoint = Field(alias="from")
    to: Endpoint
    type: Literal["triggers", "navigates", "links", "opens", "submits"]
    label: str = ""

    class Config:
        populate_by_name = True


class Component(BaseModel):
    """LLM-generated component using 12-column grid positioning"""
    id: str = ""
    type: str
    position: Optional[GridPosition] = None
    props: Dict[str, Any] = Field(default_factory=dict)
    children: List["Component"] = Field(default_factory=list)


# Enable forward reference for nested children
Component.model_rebuild()


class WireframeDoc(BaseModel):
    """Complete wireframe document from LLM text-to-wireframe generation"""
    layout: Layout
    components: List[Component] = Field(default_factory=list)
    connections: List[Connection] = Field(default_factory=list)
    theme: Optional[Theme] = None

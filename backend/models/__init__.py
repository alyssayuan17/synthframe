"""
Data Models for the Wireframe Generation System
"""
from .wireframe import (
    ComponentType,
    Position,
    Size,
    BoundingBox,
    DetectedText,
    WireframeComponent,
    WireframeLayout,
    CVDetectionResult,
    COMPONENT_TEMPLATES
)

__all__ = [
    "ComponentType",
    "Position",
    "Size", 
    "BoundingBox",
    "DetectedText",
    "WireframeComponent",
    "WireframeLayout",
    "CVDetectionResult",
    "COMPONENT_TEMPLATES"
]

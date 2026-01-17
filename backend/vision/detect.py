"""
Shape Detection Module
======================

Finds rectangles and shapes in preprocessed sketch images,
then maps them to UI component types based on position and size.

THE FLOW:
    Preprocessed Binary Image
         │
         ▼
    1. Find Contours - Detect all shapes
         │
         ▼
    2. Filter Contours - Remove noise, keep rectangles
         │
         ▼
    3. Extract Bounding Boxes - Get position/size of each shape
         │
         ▼
    4. Map to Components - Decide what type based on rules
         │
         ▼
    List of Component objects
    
MAPPING LOGIC:
- Rectangle at TOP spanning full width → NAVBAR
- Large rectangle near top → HERO
- Rectangle at BOTTOM spanning full width → FOOTER
- Tall narrow rectangle on LEFT → SIDEBAR
- Medium rectangles in grid pattern → CARDS
- Small rectangles → BUTTONS
- Default → SECTION
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass

from config import settings, DETECTION_RULES
from models.wireframe import Component, ComponentType, Position, Size


@dataclass
class DetectedShape:
    """
    Intermediate representation of a detected shape before mapping to Component.
    """
    x: int              # Top-left x coordinate
    y: int              # Top-left y coordinate
    width: int          # Width in pixels
    height: int         # Height in pixels
    contour: np.ndarray # Original contour points
    area: float         # Area in pixels
    
    @property
    def center(self) -> Tuple[int, int]:
        """Center point of shape"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    @property
    def aspect_ratio(self) -> float:
        """Width / Height ratio"""
        if self.height == 0:
            return 0
        return self.width / self.height


def find_contours(binary_image: np.ndarray) -> List[np.ndarray]:
    """
    Find all contours (closed shapes) in a binary image.
    
    HOW IT WORKS:
    OpenCV traces along the boundaries of white regions in the binary image.
    Each contour is a numpy array of (x, y) points.
    
    Args:
        binary_image: Preprocessed binary image (white shapes on black)
        
    Returns:
        List of contours (each contour is array of points)
    """
    # RETR_EXTERNAL: Only get outermost contours (ignore nested shapes)
    # CHAIN_APPROX_SIMPLE: Compress contours (only keep corner points)
    contours, _ = cv2.findContours(
        binary_image.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    return list(contours)


def filter_contours(
    contours: List[np.ndarray], 
    image_area: int,
    min_area: int = None
) -> List[np.ndarray]:
    """
    Filter out noise and non-rectangular contours.
    
    WHY:
    - Small contours are usually noise (specks, texture)
    - Very large contours might be the paper edge
    - Non-closed shapes are probably incomplete lines
    
    Args:
        contours: List of detected contours
        image_area: Total image area (for ratio calculations)
        min_area: Minimum contour area to keep
        
    Returns:
        Filtered list of valid contours
    """
    if min_area is None:
        min_area = settings.min_contour_area
    
    filtered = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        # Skip if too small (noise)
        if area < min_area:
            continue
        
        # Skip if too large (probably paper edge)
        if area > image_area * 0.95:
            continue
        
        # Check if roughly rectangular by approximating polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Rectangles have ~4 corners, but allow 3-8 for hand-drawn shapes
        if 3 <= len(approx) <= 8:
            filtered.append(contour)
    
    return filtered


def contours_to_shapes(contours: List[np.ndarray]) -> List[DetectedShape]:
    """
    Convert raw contours to DetectedShape objects with bounding boxes.
    
    Args:
        contours: List of valid contours
        
    Returns:
        List of DetectedShape with position, size, and metadata
    """
    shapes = []
    
    for contour in contours:
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        
        shape = DetectedShape(
            x=x,
            y=y,
            width=w,
            height=h,
            contour=contour,
            area=area
        )
        shapes.append(shape)
    
    # Sort by y position (top to bottom), then x (left to right)
    shapes.sort(key=lambda s: (s.y, s.x))
    
    return shapes


def map_shape_to_component_type(
    shape: DetectedShape,
    image_width: int,
    image_height: int
) -> Tuple[ComponentType, float]:
    """
    Determine what UI component type a shape represents based on its
    position and size relative to the image.
    
    RULES (from config.py):
    - Top + full width → NAVBAR
    - Top + large → HERO
    - Bottom + full width → FOOTER
    - Left + tall → SIDEBAR
    - Small grids → CARDS
    - Very small → BUTTONS
    - Default → SECTION
    
    Args:
        shape: Detected shape with position/size
        image_width: Total image width
        image_height: Total image height
        
    Returns:
        Tuple of (ComponentType, confidence_score)
    """
    # Calculate ratios for rule matching
    x_ratio = shape.x / image_width
    y_ratio = shape.y / image_height
    width_ratio = shape.width / image_width
    height_ratio = shape.height / image_height
    area_ratio = shape.area / (image_width * image_height)
    
    # Check each component type rule
    
    # NAVBAR: Top of page, wide
    if (y_ratio < 0.12 and 
        width_ratio > 0.7 and 
        height_ratio < 0.15):
        return ComponentType.NAVBAR, 0.9
    
    # FOOTER: Bottom of page, wide
    if (y_ratio + height_ratio > 0.85 and 
        width_ratio > 0.7):
        return ComponentType.FOOTER, 0.85
    
    # SIDEBAR: Left side, tall
    if (x_ratio < 0.3 and 
        height_ratio > 0.5 and 
        width_ratio < 0.35):
        return ComponentType.SIDEBAR, 0.85
    
    # HERO: Large section near top
    if (y_ratio < 0.35 and 
        area_ratio > 0.15):
        return ComponentType.HERO, 0.8
    
    # BUTTON: Very small rectangles
    if (area_ratio < 0.03 and 
        1.5 < shape.aspect_ratio < 6.0):
        return ComponentType.BUTTON, 0.7
    
    # CARD: Medium-sized, roughly square
    if (area_ratio < 0.15 and 
        0.5 < shape.aspect_ratio < 2.0):
        return ComponentType.CARD, 0.7
    
    # Default: SECTION
    return ComponentType.SECTION, 0.5


def shapes_to_components(
    shapes: List[DetectedShape],
    image_width: int,
    image_height: int,
    canvas_width: int = None,
    canvas_height: int = None
) -> List[Component]:
    """
    Convert detected shapes to UI Components with proper types.
    
    Scales positions from image coordinates to canvas coordinates
    so React frontend can render at consistent size.
    
    Args:
        shapes: List of detected shapes
        image_width: Source image width
        image_height: Source image height
        canvas_width: Target canvas width (default from settings)
        canvas_height: Target canvas height (default from settings)
        
    Returns:
        List of Component objects ready for React frontend
    """
    if canvas_width is None:
        canvas_width = settings.default_canvas_width
    if canvas_height is None:
        canvas_height = settings.default_canvas_height
    
    # Scale factors for converting image coords to canvas coords
    scale_x = canvas_width / image_width
    scale_y = canvas_height / image_height
    
    components = []
    
    for shape in shapes:
        # Determine component type
        comp_type, confidence = map_shape_to_component_type(
            shape, image_width, image_height
        )
        
        # Scale position and size to canvas coordinates
        scaled_x = shape.x * scale_x
        scaled_y = shape.y * scale_y
        scaled_width = shape.width * scale_x
        scaled_height = shape.height * scale_y
        
        # Create Component
        component = Component(
            type=comp_type,
            position=Position(x=scaled_x, y=scaled_y),
            size=Size(width=scaled_width, height=scaled_height),
            confidence=confidence,
            props=_get_default_props(comp_type)
        )
        
        components.append(component)
    
    return components


def _get_default_props(comp_type: ComponentType) -> dict:
    """
    Get default props for a component type.
    These provide placeholder content for React to render.
    """
    defaults = {
        ComponentType.NAVBAR: {
            "logo": "Logo",
            "links": ["Home", "About", "Contact"]
        },
        ComponentType.HERO: {
            "headline": "Your Headline Here",
            "subheadline": "Supporting text goes here",
            "cta": "Get Started"
        },
        ComponentType.SECTION: {
            "title": "Section Title",
            "content": "Section content..."
        },
        ComponentType.CARD: {
            "title": "Card Title",
            "description": "Card description"
        },
        ComponentType.BUTTON: {
            "text": "Button",
            "variant": "primary"
        },
        ComponentType.FOOTER: {
            "links": ["Privacy", "Terms", "Contact"],
            "copyright": "© 2024"
        },
        ComponentType.SIDEBAR: {
            "items": ["Dashboard", "Settings", "Help"]
        },
        ComponentType.FORM: {
            "fields": ["Name", "Email", "Message"],
            "submitText": "Submit"
        },
        ComponentType.TABLE: {
            "columns": ["Column 1", "Column 2", "Column 3"],
            "rows": 5
        },
        ComponentType.CALENDAR: {
            "view": "month"
        },
        ComponentType.CHART: {
            "type": "bar"
        },
    }
    
    return defaults.get(comp_type, {})


def detect_components(
    binary_image: np.ndarray,
    original_image: np.ndarray = None
) -> Tuple[List[Component], np.ndarray]:
    """
    Main entry point: detect UI components from preprocessed sketch.
    
    Args:
        binary_image: Preprocessed binary image from preprocess.py
        original_image: Optional original image for debug visualization
        
    Returns:
        Tuple of (components, debug_image)
        - components: List of detected Component objects
        - debug_image: Original image with detected shapes drawn (for debugging)
    """
    image_height, image_width = binary_image.shape[:2]
    image_area = image_width * image_height
    
    # Step 1: Find all contours
    contours = find_contours(binary_image)
    
    # Step 2: Filter valid contours
    valid_contours = filter_contours(contours, image_area)
    
    # Step 3: Convert to shape objects
    shapes = contours_to_shapes(valid_contours)
    
    # Step 4: Map to components
    components = shapes_to_components(shapes, image_width, image_height)
    
    # Create debug visualization
    if original_image is not None:
        debug_img = original_image.copy()
    else:
        # Convert binary back to color for visualization
        debug_img = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
    
    # Draw detected shapes with labels
    for shape, component in zip(shapes, components):
        color = _get_component_color(component.type)
        cv2.rectangle(
            debug_img,
            (shape.x, shape.y),
            (shape.x + shape.width, shape.y + shape.height),
            color,
            2
        )
        cv2.putText(
            debug_img,
            f"{component.type.value} ({component.confidence:.0%})",
            (shape.x, shape.y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1
        )
    
    return components, debug_img


def _get_component_color(comp_type: ComponentType) -> Tuple[int, int, int]:
    """Get BGR color for component type visualization."""
    colors = {
        ComponentType.NAVBAR: (255, 0, 0),    # Blue
        ComponentType.HERO: (0, 255, 0),      # Green
        ComponentType.FOOTER: (0, 0, 255),    # Red
        ComponentType.SIDEBAR: (255, 255, 0), # Cyan
        ComponentType.CARD: (255, 0, 255),    # Magenta
        ComponentType.BUTTON: (0, 255, 255),  # Yellow
        ComponentType.SECTION: (128, 128, 128),# Gray
    }
    return colors.get(comp_type, (200, 200, 200))

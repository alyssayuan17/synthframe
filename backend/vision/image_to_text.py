"""
Vision Module - Main Entry Point
=================================

This is the main interface for the CV/image processing pipeline.
Call analyze_sketch() with a base64 image and get Component objects back.

USAGE:
    from vision import analyze_sketch
    
    result = analyze_sketch(base64_image_string)
    # result.components = [Component, Component, ...]
    # result.debug_image = base64 image with detected shapes drawn
"""

from dataclasses import dataclass
from typing import List, Optional
import cv2

from models.wireframe import Component, Wireframe
from vision.preprocess import (
    decode_base64_image,
    encode_image_to_base64,
    preprocess_image,
    resize_for_processing
)
from vision.detect import detect_components


@dataclass
class SketchAnalysisResult:
    """
    Result from analyzing a hand-drawn sketch.
    
    Attributes:
        wireframe: Complete Wireframe object with detected components
        components: List of detected Component objects (same as wireframe.components)
        debug_image_base64: Original image with detected shapes drawn (for debugging)
        original_size: (width, height) of original image
        processing_notes: Any warnings or notes about the processing
    """
    wireframe: Wireframe
    components: List[Component]
    debug_image_base64: Optional[str]
    original_size: tuple
    processing_notes: List[str]
    
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict for API response."""
        return {
            "wireframe": self.wireframe.to_json(),
            "components": [c.model_dump() for c in self.components],
            "debug_image": self.debug_image_base64,
            "original_size": {
                "width": self.original_size[0],
                "height": self.original_size[1]
            },
            "processing_notes": self.processing_notes
        }


def analyze_sketch(
    image_base64: str,
    return_debug_image: bool = True,
    wireframe_name: str = "Sketch Wireframe"
) -> SketchAnalysisResult:
    """
    Main entry point: Analyze a hand-drawn sketch and extract UI components.
    
    This runs the full pipeline:
    1. Decode base64 image
    2. Resize if too large
    3. Preprocess (grayscale, blur, threshold, morphology)
    4. Detect shapes and map to component types
    5. Package into Wireframe object
    
    Args:
        image_base64: Base64 encoded image (with or without data URI prefix)
        return_debug_image: Include debug visualization in response
        wireframe_name: Name for the generated wireframe
        
    Returns:
        SketchAnalysisResult with Wireframe, components, and debug info
        
    Example:
        # From API route
        result = analyze_sketch(request.image_base64)
        return {"wireframe": result.wireframe.to_json()}
    """
    notes = []
    
    # Step 1: Decode base64 to OpenCV image
    try:
        original_image = decode_base64_image(image_base64)
    except Exception as e:
        raise ValueError(f"Could not decode image: {str(e)}")
    
    original_height, original_width = original_image.shape[:2]
    notes.append(f"Original size: {original_width}x{original_height}")
    
    # Step 2: Resize if too large
    resized_image, scale_factor = resize_for_processing(original_image)
    if scale_factor != 1.0:
        notes.append(f"Resized by factor {scale_factor:.2f}")
    
    # Step 3: Preprocess
    binary_image, edges = preprocess_image(resized_image)
    
    # Step 4: Detect components
    components, debug_image = detect_components(binary_image, resized_image)
    
    notes.append(f"Detected {len(components)} components")
    
    # Log component types found
    type_counts = {}
    for comp in components:
        type_name = comp.type.value
        type_counts[type_name] = type_counts.get(type_name, 0) + 1
    notes.append(f"Types: {type_counts}")
    
    # Step 5: Package into Wireframe
    wireframe = Wireframe(
        name=wireframe_name,
        components=components
    )
    
    # Encode debug image if requested
    debug_base64 = None
    if return_debug_image and debug_image is not None:
        debug_base64 = encode_image_to_base64(debug_image)
    
    return SketchAnalysisResult(
        wireframe=wireframe,
        components=components,
        debug_image_base64=debug_base64,
        original_size=(original_width, original_height),
        processing_notes=notes
    )


def analyze_sketch_simple(image_base64: str) -> dict:
    """
    Simplified version for quick API responses.
    Returns just the wireframe JSON without debug info.
    """
    result = analyze_sketch(image_base64, return_debug_image=False)
    return result.wireframe.to_json()

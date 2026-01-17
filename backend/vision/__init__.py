"""
Vision Module
=============

Analyzes hand-drawn sketches and converts them to UI component structures.

USAGE:
    from vision import analyze_sketch
    
    result = analyze_sketch(base64_image_string)
    wireframe = result.wireframe  # Wireframe object with components
"""

from vision.image_to_text import analyze_sketch, analyze_sketch_simple, SketchAnalysisResult
from vision.preprocess import decode_base64_image, encode_image_to_base64, preprocess_image
from vision.detect import detect_components

__all__ = [
    "analyze_sketch",
    "analyze_sketch_simple", 
    "SketchAnalysisResult",
    "decode_base64_image",
    "encode_image_to_base64",
    "preprocess_image",
    "detect_components"
]

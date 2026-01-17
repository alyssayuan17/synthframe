"""
Image Preprocessing Module
==========================

Takes raw images (photos of hand-drawn sketches) and prepares them for shape detection.

THE PIPELINE:
    Raw Image (color, noisy, variable lighting)
         │
         ▼
    1. Grayscale - Remove color information
         │
         ▼
    2. Gaussian Blur - Reduce noise
         │
         ▼
    3. Adaptive Threshold - Handle variable lighting
         │
         ▼
    4. Morphological Operations - Clean up edges
         │
         ▼
    Preprocessed Image (binary, clean edges)

WHY EACH STEP:
- Grayscale: Edge detection only needs intensity, not color
- Blur: Smooths out pencil texture and paper grain
- Threshold: Converts to black/white for clear edge detection
- Morphology: Closes small gaps in lines, removes specks
"""

import cv2
import numpy as np
from typing import Tuple
import base64

from config import settings


def decode_base64_image(base64_string: str) -> np.ndarray:
    """
    Convert base64 string to OpenCV image array.
    
    This is what you'll receive from the frontend when user uploads a sketch.
    The frontend sends: "data:image/png;base64,iVBORw0KGgo..."
    
    Args:
        base64_string: Base64 encoded image, optionally with data URI prefix
        
    Returns:
        OpenCV image as numpy array (BGR format)
        
    Example:
        # From frontend upload
        image = decode_base64_image(request.image_base64)
    """
    # Remove data URI prefix if present
    # "data:image/png;base64,iVBORw0KGgo..." → "iVBORw0KGgo..."
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    
    # Decode base64 to bytes
    image_bytes = base64.b64decode(base64_string)
    
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    
    # Decode numpy array to OpenCV image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Could not decode image from base64 string")
    
    return image


def encode_image_to_base64(image: np.ndarray, format: str = "png") -> str:
    """
    Convert OpenCV image back to base64 (for sending debug images to frontend).
    
    Args:
        image: OpenCV image array
        format: Output format ("png" or "jpg")
        
    Returns:
        Base64 encoded string with data URI prefix
    """
    # Encode image to bytes
    success, buffer = cv2.imencode(f".{format}", image)
    if not success:
        raise ValueError(f"Could not encode image to {format}")
    
    # Convert to base64
    base64_string = base64.b64encode(buffer).decode("utf-8")
    
    # Add data URI prefix
    mime_type = "image/png" if format == "png" else "image/jpeg"
    return f"data:{mime_type};base64,{base64_string}"


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert color image to grayscale.
    
    WHY: Edge detection algorithms work on intensity gradients.
    Color information is not needed and would complicate processing.
    
    Args:
        image: BGR color image
        
    Returns:
        Single-channel grayscale image
    """
    if len(image.shape) == 2:
        # Already grayscale
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_blur(image: np.ndarray, kernel_size: int = None) -> np.ndarray:
    """
    Apply Gaussian blur to reduce noise.
    
    WHY: Hand-drawn sketches have pencil texture, paper grain, and small
    imperfections. Blurring smooths these out so edge detection doesn't
    pick them up as edges.
    
    Args:
        image: Grayscale image
        kernel_size: Size of blur kernel (must be odd). Larger = more blur.
        
    Returns:
        Blurred image
    """
    if kernel_size is None:
        kernel_size = settings.blur_kernel_size
    
    # Kernel must be odd
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def apply_threshold(image: np.ndarray, adaptive: bool = True) -> np.ndarray:
    """
    Convert grayscale to binary (black and white only).
    
    WHY: After this, every pixel is either 0 (black/background) or 
    255 (white/foreground). This makes edge detection cleaner.
    
    We use ADAPTIVE thresholding because:
    - Photos of sketches have uneven lighting
    - Shadow on one side, bright on other
    - Adaptive adjusts threshold locally
    
    Args:
        image: Grayscale blurred image
        adaptive: Use adaptive threshold (True) or global (False)
        
    Returns:
        Binary image (only 0 and 255 values)
    """
    if adaptive:
        # Adaptive threshold - calculates threshold for small regions
        # Good for uneven lighting (shadows, camera flash, etc)
        binary = cv2.adaptiveThreshold(
            image,
            255,                          # Max value (white)
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # Use Gaussian-weighted mean
            cv2.THRESH_BINARY_INV,        # Invert: lines become white
            11,                           # Block size for local threshold
            2                             # Constant subtracted from mean
        )
    else:
        # Global threshold - one value for entire image
        _, binary = cv2.threshold(
            image,
            settings.binary_threshold,
            255,
            cv2.THRESH_BINARY_INV
        )
    
    return binary


def apply_morphology(image: np.ndarray) -> np.ndarray:
    """
    Apply morphological operations to clean up the binary image.
    
    WHY: After thresholding, we might have:
    - Small gaps in lines (pen lifted slightly)
    - Small noise specks (paper texture)
    
    MORPHOLOGICAL CLOSE: Fills small gaps
    MORPHOLOGICAL OPEN: Removes small specks
    
    Args:
        image: Binary image
        
    Returns:
        Cleaned binary image
    """
    # Create a small rectangular kernel
    kernel = np.ones((3, 3), np.uint8)
    
    # Close: dilate then erode (fills small gaps in lines)
    closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Open: erode then dilate (removes small noise specks)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=1)
    
    return opened


def preprocess_image(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Full preprocessing pipeline for sketch images.
    
    Takes a raw photo of a hand-drawn sketch and prepares it for
    shape/contour detection.
    
    Args:
        image: Raw BGR image from camera/upload
        
    Returns:
        Tuple of (preprocessed_binary_image, edge_image)
        - preprocessed: Binary image for contour detection
        - edges: Canny edge image (for visualization/debugging)
        
    Example:
        raw_image = decode_base64_image(base64_string)
        binary, edges = preprocess_image(raw_image)
        contours = find_contours(binary)
    """
    # Step 1: Convert to grayscale
    gray = to_grayscale(image)
    
    # Step 2: Apply Gaussian blur
    blurred = apply_blur(gray)
    
    # Step 3: Apply adaptive threshold
    binary = apply_threshold(blurred, adaptive=True)
    
    # Step 4: Clean up with morphology
    cleaned = apply_morphology(binary)
    
    # Also compute Canny edges for visualization
    edges = cv2.Canny(
        blurred, 
        settings.canny_low_threshold, 
        settings.canny_high_threshold
    )
    
    return cleaned, edges


def resize_for_processing(image: np.ndarray, max_dimension: int = 1200) -> Tuple[np.ndarray, float]:
    """
    Resize large images to reasonable size for processing.
    
    WHY: 
    - Large images slow down processing
    - We don't need 4K resolution to detect rectangles
    - Consistent size = consistent detection thresholds
    
    Args:
        image: Input image
        max_dimension: Maximum width or height
        
    Returns:
        Tuple of (resized_image, scale_factor)
        - scale_factor: Multiply detected coordinates by this to get original size
    """
    height, width = image.shape[:2]
    
    # Check if resize needed
    if max(height, width) <= max_dimension:
        return image, 1.0
    
    # Calculate scale factor
    if width > height:
        scale = max_dimension / width
    else:
        scale = max_dimension / height
    
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return resized, scale

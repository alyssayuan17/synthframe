"""
Vision Route - POST /vision/analyze
Analyze uploaded sketch/mockup images using CV pipeline.
Auto-saves to MongoDB.
"""
from fastapi import APIRouter, HTTPException

from backend.models.requests import ImageUploadRequest
from backend.models.responses import WireframeResponse, ErrorResponse
from backend.database.operations import create_project, DatabaseError

router = APIRouter(prefix="/vision", tags=["Vision"])


@router.post(
    "/analyze",
    response_model=WireframeResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Analyze sketch or mockup image"
)
async def analyze_image(request: ImageUploadRequest):
    """
    Analyze an uploaded sketch or mockup image using CV pipeline.
    
    - **image_base64**: Base64 encoded image (PNG, JPG, etc.)
    - **image_type**: "sketch", "mockup", or "auto"
    - **detect_text**: Whether to run OCR
    
    Returns a WireframeLayout with detected components.
    """
    try:
        # Import here to avoid circular imports
        from backend.vision.image_to_text import analyze_sketch
        
        result = analyze_sketch(
            image_base64=request.image_base64,
            return_debug_image=True,
            wireframe_name=request.name
        )
        
        # Convert to WireframeLayout format
        from backend.models.wireframe import WireframeLayout, WireframeComponent, Size
        from backend.config import DEVICE_CANVAS_SIZES, DEFAULT_DEVICE_TYPE
        
        # Get canvas size for device type
        device = request.device_type or DEFAULT_DEVICE_TYPE
        canvas = DEVICE_CANVAS_SIZES.get(device, DEVICE_CANVAS_SIZES[DEFAULT_DEVICE_TYPE])
        
        components = []
        for comp in result.wireframe.components:
            components.append(WireframeComponent(
                id=comp.id,
                type=comp.type.value,  # Convert enum to string
                position=comp.position.model_dump(),
                size=comp.size.model_dump(),
                props=comp.props,
                confidence=comp.confidence,
                source="cv"
            ))
        
        layout = WireframeLayout(
            id=result.wireframe.id,
            name=result.wireframe.name,
            canvas_size=Size(width=canvas["width"], height=canvas["height"]),
            source_type="sketch" if request.image_type == "sketch" else "mockup",
            components=components
        )
        
        # Auto-save to MongoDB
        try:
            project = await create_project(
                wireframe=layout,
                name=request.name,
                generation_method="cv_sketch" if request.image_type == "sketch" else "mockup",
                device_type=request.device_type or DEFAULT_DEVICE_TYPE,
                original_prompt=f"CV analysis: {request.image_type}"
            )
            project_id = project.id
        except DatabaseError as db_err:
            # If database fails, still return wireframe (hackathon-safe)
            print(f"Warning: Failed to save project to MongoDB: {db_err}")
            project_id = None
        
        return WireframeResponse(
            success=True,
            project_id=project_id,
            wireframe=layout,
            message=f"Detected {len(components)} components"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision analysis failed: {str(e)}")


@router.get("/status")
async def vision_status():
    """Check if CV pipeline dependencies are available."""
    status = {"cv2": False, "numpy": False}
    
    try:
        import cv2
        status["cv2"] = True
    except ImportError:
        pass
    
    try:
        import numpy
        status["numpy"] = True
    except ImportError:
        pass
    
    return {"available": all(status.values()), "dependencies": status}

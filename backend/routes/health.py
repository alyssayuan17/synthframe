"""
Health Check Route
"""
from fastapi import APIRouter
from ..models.responses import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health and service availability"""
    services = {
        "cv_pipeline": True,
        "ocr": True,
    }
    
    # Check optional services
    try:
        import pytesseract
        services["tesseract"] = True
    except ImportError:
        services["tesseract"] = False
    
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        services=services
    )

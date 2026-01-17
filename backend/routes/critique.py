"""
Critique Route - POST /critique
Analyze wireframe design and provide suggestions.

NOTE: This is a stub. Full implementation requires:
- Design rules engine
- Accessibility checks
- Layout analysis
"""
from fastapi import APIRouter, HTTPException

from backend.models.requests import CritiqueRequest
from backend.models.responses import CritiqueResponse, CritiqueItem, ErrorResponse

router = APIRouter(tags=["Critique"])


@router.post(
    "/critique",
    response_model=CritiqueResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get design critique for wireframe (stub)"
)
async def critique_wireframe(request: CritiqueRequest):
    """
    Analyze a wireframe and provide design critique/suggestions.
    
    - **wireframe_id**: ID of the wireframe to critique
    - **focus_areas**: Optional list of areas to focus on (spacing, contrast, etc.)
    
    ⚠️ This is a STUB. Returns mock suggestions.
    """
    # Mock critique response for now
    mock_critiques = [
        CritiqueItem(
            category="spacing",
            severity="low",
            component_id=None,
            message="Consider adding more whitespace between cards",
            suggestion="Increase card gap from 20px to 32px"
        ),
        CritiqueItem(
            category="hierarchy",
            severity="medium",
            component_id=None,
            message="Heading could be more prominent",
            suggestion="Increase heading font size or add more vertical margin"
        ),
    ]
    
    return CritiqueResponse(
        success=True,
        wireframe_id=request.wireframe_id,
        overall_score=78.5,
        critiques=mock_critiques,
        summary="Overall good structure. Minor spacing and hierarchy improvements suggested."
    )


@router.get("/critique/rules")
async def get_critique_rules():
    """Get available critique rules and categories."""
    return {
        "categories": [
            "spacing",
            "contrast", 
            "alignment",
            "hierarchy",
            "consistency",
            "accessibility"
        ],
        "severity_levels": ["low", "medium", "high"],
        "status": "stub - full implementation pending"
    }

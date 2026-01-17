"""
Scrape Route - POST /scrape
Debug endpoint to test the webscraper pipeline.
"""
from fastapi import APIRouter, HTTPException

from backend.scraper.scrape import scrape_context
from backend.models.requests import ScrapeRequest
from backend.models.responses import ScrapeResponse, ErrorResponse

router = APIRouter(tags=["Scraper"])


@router.post(
    "/scrape",
    response_model=ScrapeResponse,
    responses={500: {"model": ErrorResponse}},
    summary="Test webscraper (debug endpoint)"
)
async def scrape(request: ScrapeRequest):
    """
    Debug endpoint to test the webscraper.
    
    - **query**: Search query like "Airbnb landing page" or "Stripe dashboard"
    - **max_pages**: Override max pages to scrape (optional)
    
    Returns the extracted context that would be injected into generation prompts.
    """
    try:
        context = scrape_context(
            user_input=request.query,
            max_pages=request.max_pages,
        )
        
        return ScrapeResponse(
            success=True,
            context=context,
            pages_scraped=len(context.split("- Source:")) - 1 if context else 0
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

"""
SynthFrame API - Main FastAPI Application
==========================================

This is the MCP server that Athena AI will connect to.
It exposes all wireframe generation, editing, and analysis endpoints.

Run with:
    cd backend
    uvicorn main:app --reload --port 8000

Or for production:
    uvicorn main:app --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import health, generate, edit, scrape, vision, critique
from backend.config import settings

# =============================================================================
# CREATE APP
# =============================================================================

app = FastAPI(
    title="SynthFrame API",
    description="""
    Multi-modal wireframe generation tool for UI/UX designers.
    
    ## Features
    - **Text → Wireframe**: Describe a UI and get a wireframe
    - **Sketch → Wireframe**: Upload a hand-drawn sketch
    - **Edit**: Modify wireframes with natural language
    - **Critique**: Get design suggestions (coming soon)
    
    ## Integration
    This API is designed to be called by Athena AI via MCP protocol.
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# =============================================================================
# CORS MIDDLEWARE (for frontend/widget access)
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# REGISTER ROUTES
# =============================================================================

# Health check
app.include_router(health.router)

# Text-to-wireframe generation
app.include_router(generate.router)

# Edit existing wireframe
app.include_router(edit.router)

# Web scraper (design research)
app.include_router(scrape.router)

# Vision/CV pipeline (sketch analysis)
app.include_router(vision.router)

# Design critique (stub for now)
app.include_router(critique.router)

# =============================================================================
# ROOT ENDPOINT
# =============================================================================

@app.get("/")
async def root():
    """API root - returns basic info"""
    return {
        "name": "SynthFrame API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "health": "GET /health",
            "generate": "POST /generate",
            "edit": "POST /edit",
            "scrape": "POST /scrape",
            "vision": "POST /vision/analyze",
            "critique": "POST /critique",
        }
    }


# =============================================================================
# STARTUP EVENT
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("=" * 60)
    print("🚀 SynthFrame API Starting...")
    print("=" * 60)
    
    # Pre-populate scraper cache
    from backend.scraper.cache import get_cache
    cache = get_cache()
    stats = cache.stats()
    print(f"📦 Scraper cache: {stats['active_entries']} patterns pre-loaded")
    
    # Check LLM configuration
    import os
    if os.getenv("MOCK_LLM", "0") == "1":
        print("🤖 LLM: Mock mode (no API calls)")
    elif settings.gemini_api_key:
        print("🤖 LLM: Gemini API configured")
    else:
        print("⚠️  LLM: No API key (set GEMINI_API_KEY or MOCK_LLM=1)")
    
    print("=" * 60)
    print(f"📍 API ready at http://localhost:{settings.port}")
    print(f"📚 Docs at http://localhost:{settings.port}/docs")
    print("=" * 60)


# =============================================================================
# FOR DIRECT EXECUTION
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

"""
SynthFrame MCP Server for Athena AI
====================================

Provides 3 MCP tools for Athena AI:
1. analyze_sketch - Convert hand-drawn sketches to digital wireframes
2. generate_wireframe - Generate wireframes from text descriptions
3. update_component - Modify existing wireframe components

This is the integration layer with Athena AI.
The actual Gemini/scraper implementations are separate.

Usage:
    python server.py
"""

import json
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from mcp.server.stdio import stdio_server

# Import CV pipeline (already implemented)
from vision import analyze_sketch as cv_analyze_sketch

from llm.client import LlmClient
from llm.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, EDIT_SYSTEM_PROMPT
from llm.json_repair import parse_json

# Initialize MCP server
app = FastMCP("synthframe")

# Initialize LLM Client
llm_client = LlmClient()

# In-memory storage for wireframes
wireframes_db = {}


# ============================================================================
# PLACEHOLDER FUNCTIONS (Replace these with your actual implementations)
# ============================================================================

def generate_with_gemini(prompt: str, context: str = "") -> dict:
    """
    Generate wireframe from text description using LLM.
    """
    # 1. Build prompt
    user_content = USER_PROMPT_TEMPLATE.format(
        webscraper_context=context,
        user_input=prompt
    )
    
    full_prompt = f"{SYSTEM_PROMPT}\n\nUSER REQUEST:\n{user_content}"
    
    # 2. Call LLM
    print(f"Generating wireframe for: {prompt}")
    response_text = llm_client.generate(full_prompt)
    
    # 3. Parse JSON
    try:
        wireframe = parse_json(response_text)
        # Ensure it has an ID
        if "id" not in wireframe:
            wireframe["id"] = f"wf_{hash(prompt)}"
        return wireframe
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        # Fallback to a basic valid wireframe on error
        return {
            "id": f"wf_error_{hash(prompt)}",
            "name": "Error Generating Wireframe",
            "canvas_size": {"width": 1440, "height": 900},
            "components": [],
            "error": str(e)
        }


def refine_with_gemini(detected_components: list, prompt: str = "") -> dict:
    """
    Refine CV-detected components using LLM.
    """
    # Create a string representation of detected components for the LLM
    components_str = json.dumps(detected_components, indent=2)
    
    refine_prompt = f"""
    {SYSTEM_PROMPT}
    
    TASK: Refine these raw computer-vision detected components into a clean wireframe.
    - Fix alignment issues.
    - Assign better component types if clear.
    - Add reasonable props based on the component type.
    - User's description of sketch: "{prompt}"
    
    RAW DETECTED COMPONENTS:
    {components_str}
    
    OUTPUT JSON:
    """
    
    print(f"Refining {len(detected_components)} components with LLM")
    response_text = llm_client.generate(refine_prompt)
    
    try:
        return parse_json(response_text)
    except Exception as e:
        print(f"Error refining components: {e}")
        # Return basic structure with original detected components if LLM fails
        return {
            "id": "wf_cv_refined_fallback",
            "name": "Sketch Wireframe (Unrefined)", 
            "canvas_size": {"width": 1440, "height": 900},
            "components": detected_components
        }


def update_with_gemini(current_wireframe: dict, instruction: str) -> dict:
    """
    Update existing wireframe based on instruction.
    """
    current_json = json.dumps(current_wireframe, indent=2)
    
    update_prompt = f"""
    {EDIT_SYSTEM_PROMPT}
    
    INSTRUCTION: {instruction}
    
    CURRENT WIREFRAME:
    {current_json}
    
    UPDATED WIREFRAME JSON:
    """
    
    print(f"Updating wireframe with instruction: {instruction}")
    response_text = llm_client.generate(update_prompt)
    
    try:
        return parse_json(response_text)
    except Exception as e:
        print(f"Error updating wireframe: {e}")
        return current_wireframe





from scraper.scrape import scrape_similar_sites

@app.tool()
async def analyze_sketch(image_base64: str, prompt: str = "") -> dict:
    """
    Analyze a hand-drawn sketch and convert it to a digital wireframe.

    Steps:
    1. Run CV pipeline (already implemented in vision/)
    2. Refine with Gemini AI
    3. Return wireframe JSON

    Args:
        image_base64: Base64 encoded sketch image
        prompt: Optional text description

    Returns:
        {
            "wireframe_id": "wf_abc123",
            "name": "Sketch Wireframe",
            "components": [...],
            "message": "Detected 5 components"
        }
    """
    try:
        # Step 1: Run CV pipeline (your existing code)
        cv_result = cv_analyze_sketch(image_base64, return_debug_image=False)

        # Step 2: Convert to format for Gemini
        detected_components = [
            {
                "id": comp.id,
                "type": comp.type.value.lower(),
                "position": {"x": comp.position.x, "y": comp.position.y},
                "size": {"width": comp.size.width, "height": comp.size.height},
                "props": comp.props,
                "confidence": comp.confidence,
                "source": "cv",
                "children": []
            }
            for comp in cv_result.components
        ]

        # Step 3: Refine with Gemini (placeholder - you implement this)
        refined_wireframe = refine_with_gemini(detected_components, prompt)

        # Step 4: Save wireframe
        wireframe_id = refined_wireframe.get("id")
        wireframes_db[wireframe_id] = refined_wireframe

        return {
            "wireframe_id": wireframe_id,
            "name": refined_wireframe.get("name"),
            "components": refined_wireframe.get("components"),
            "canvas_size": refined_wireframe.get("canvas_size"),
            "message": f"Analyzed sketch and detected {len(cv_result.components)} components",
            "component_count": len(refined_wireframe.get("components", [])),
            "cv_notes": cv_result.processing_notes
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": f"Failed to analyze sketch: {str(e)}"
        }


@app.tool()
async def generate_wireframe(
    prompt: str,
    use_scraper: bool = True
) -> dict:
    """
    Generate a wireframe from a text description.

    Steps:
    1. Optionally scrape similar sites for inspiration
    2. Call Gemini to generate components
    3. Return wireframe JSON

    Args:
        prompt: User's description (e.g., "Create a landing page for my student club")
        use_scraper: Whether to scrape similar sites (default: True)

    Returns:
        {
            "wireframe_id": "wf_xyz789",
            "name": "Generated Wireframe",
            "components": [...],
            "message": "Generated 8 components"
        }
    """
    try:
        scraper_context = ""

        # Step 1: Web scraper (placeholder - you implement this)
        if use_scraper:
            try:
                scraper_result = scrape_similar_sites(prompt)
                patterns = scraper_result.get("patterns", [])
                if patterns:
                    scraper_context = f"Similar sites use: {', '.join(patterns)}"
            except Exception as e:
                print(f"Scraper failed: {e}")

        # Step 2: Generate with Gemini (placeholder - you implement this)
        wireframe_json = generate_with_gemini(prompt, scraper_context)

        # Step 3: Save wireframe
        wireframe_id = wireframe_json.get("id")
        wireframes_db[wireframe_id] = wireframe_json

        return {
            "wireframe_id": wireframe_id,
            "name": wireframe_json.get("name"),
            "components": wireframe_json.get("components"),
            "canvas_size": wireframe_json.get("canvas_size"),
            "message": f"Generated wireframe with {len(wireframe_json.get('components', []))} components",
            "component_count": len(wireframe_json.get("components", [])),
            "scraper_context": scraper_context if scraper_context else None
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": f"Failed to generate wireframe: {str(e)}"
        }


@app.tool()
async def update_component(
    wireframe_id: str,
    instruction: str
) -> dict:
    """
    Update an existing wireframe based on natural language instruction.

    Examples:
    - "Make the hero section bigger"
    - "Add a pricing section"
    - "Move the footer down"

    Args:
        wireframe_id: ID of wireframe to update
        instruction: What to change

    Returns:
        {
            "wireframe_id": "wf_abc123",
            "components": [...],
            "message": "Updated hero section"
        }
    """
    try:
        # Step 1: Get existing wireframe
        if wireframe_id not in wireframes_db:
            return {
                "error": "Wireframe not found",
                "message": f"No wireframe with ID {wireframe_id}"
            }

        current_wireframe = wireframes_db[wireframe_id]

        # Step 2: Update with Gemini (placeholder - you implement this)
        updated_wireframe = update_with_gemini(current_wireframe, instruction)

        # Step 3: Save updated wireframe
        wireframes_db[wireframe_id] = updated_wireframe

        return {
            "wireframe_id": wireframe_id,
            "name": updated_wireframe.get("name"),
            "components": updated_wireframe.get("components"),
            "canvas_size": updated_wireframe.get("canvas_size"),
            "message": f"Updated based on: '{instruction}'",
            "component_count": len(updated_wireframe.get("components", []))
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": f"Failed to update: {str(e)}"
        }


# ============================================================================
# REST API (for frontend to fetch wireframes)
# ============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

rest_api = FastAPI(title="SynthFrame API")

rest_api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@rest_api.get("/api/wireframes/{wireframe_id}")
async def get_wireframe(wireframe_id: str):
    """Get wireframe by ID (for frontend)"""
    if wireframe_id not in wireframes_db:
        raise HTTPException(status_code=404, detail="Wireframe not found")
    return wireframes_db[wireframe_id]


@rest_api.post("/api/wireframes/{wireframe_id}")
async def save_wireframe(wireframe_id: str, wireframe: dict):
    """Save/update wireframe (for frontend)"""
    wireframes_db[wireframe_id] = wireframe
    return {"status": "saved", "wireframe_id": wireframe_id}


@rest_api.get("/api/wireframes")
async def list_wireframes():
    """List all wireframes"""
    return {
        "wireframes": [
            {"id": wf_id, "name": wf.get("name", "Untitled")}
            for wf_id, wf in wireframes_db.items()
        ]
    }


@rest_api.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "mcp_tools": ["analyze_sketch", "generate_wireframe", "update_component"],
        "wireframes_count": len(wireframes_db)
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import asyncio
    import uvicorn
    from threading import Thread

    print("=" * 60)
    print("SynthFrame MCP Server for Athena AI")
    print("=" * 60)
    print("\nMCP Tools available:")
    print("  1. analyze_sketch - Convert sketches to wireframes (CV + AI)")
    print("  2. generate_wireframe - Generate from text prompts (AI + scraper)")
    print("  3. update_component - Modify existing wireframes (AI)")
    print("\nREST API running on http://localhost:8000")
    print("  GET  /api/wireframes/{id} - Fetch wireframe")
    print("  POST /api/wireframes/{id} - Save wireframe")
    print("  GET  /health - Health check")
    print("\n" + "=" * 60)

    # Run REST API in background thread
    Thread(target=lambda: uvicorn.run(
        rest_api,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    ), daemon=True).start()

    # Run MCP server in main thread (stdio for Athena)
    asyncio.run(stdio_server(app))

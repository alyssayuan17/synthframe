"""
LLM Client - Supports Mock and Gumloop providers.

For Gumloop integration, set these environment variables:
- GUMLOOP_API_KEY: Your Gumloop API key
- GUMLOOP_USER_ID: Your Gumloop user ID
- GUMLOOP_PIPELINE_ID: The saved pipeline ID for wireframe generation

The Gumloop pipeline should accept "prompt" as input and return generated JSON.
"""
from __future__ import annotations
import os
import httpx
from typing import Optional


class LlmError(Exception):
    pass


class LlmClient:
    """
    LLM client supporting mock mode and Gumloop integration.
    
    Provider priority:
    1. If MOCK_LLM=1, use mock (always returns sample dashboard)
    2. If GUMLOOP_API_KEY is set, use Gumloop
    3. Otherwise, raise error
    """
    
    GUMLOOP_API_URL = "https://api.gumloop.com/api/v1/start_pipeline"
    
    def __init__(self) -> None:
        self.mock = os.getenv("MOCK_LLM", "0") == "1"
        self.gumloop_api_key = os.getenv("GUMLOOP_API_KEY")
        self.gumloop_user_id = os.getenv("GUMLOOP_USER_ID")
        self.gumloop_pipeline_id = os.getenv("GUMLOOP_PIPELINE_ID")
    
    def generate(self, prompt: str) -> str:
        """Generate wireframe JSON from prompt."""
        if self.mock:
            return self._mock_generate()
        
        if self.gumloop_api_key:
            return self._gumloop_generate(prompt)
        
        raise LlmError(
            "LLM client not configured. Options:\n"
            "  1. Set MOCK_LLM=1 for local testing\n"
            "  2. Set GUMLOOP_API_KEY, GUMLOOP_USER_ID, GUMLOOP_PIPELINE_ID for Gumloop"
        )
    
    def _gumloop_generate(self, prompt: str) -> str:
        """Call Gumloop API to generate wireframe."""
        if not self.gumloop_user_id or not self.gumloop_pipeline_id:
            raise LlmError(
                "Gumloop requires GUMLOOP_USER_ID and GUMLOOP_PIPELINE_ID environment variables"
            )
        
        headers = {
            "Authorization": f"Bearer {self.gumloop_api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "user_id": self.gumloop_user_id,
            "saved_item_id": self.gumloop_pipeline_id,
            "pipeline_inputs": [
                {"input_name": "prompt", "value": prompt}
            ],
        }
        
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    self.GUMLOOP_API_URL,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                
                run_id = data.get("run_id")
                if run_id:
                    return self._poll_gumloop_result(run_id)
                
                return data.get("output", str(data))
                
        except httpx.HTTPError as e:
            raise LlmError(f"Gumloop API error: {e}") from e
    
    def _poll_gumloop_result(self, run_id: str, max_attempts: int = 30) -> str:
        """Poll Gumloop for pipeline result."""
        import time
        
        poll_url = f"https://api.gumloop.com/api/v1/get_pl_run"
        headers = {
            "Authorization": f"Bearer {self.gumloop_api_key}",
        }
        params = {
            "run_id": run_id,
            "user_id": self.gumloop_user_id,
        }
        
        with httpx.Client(timeout=30.0) as client:
            for _ in range(max_attempts):
                response = client.get(poll_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                state = data.get("state", "")
                if state == "DONE":
                    outputs = data.get("outputs", {})
                    if outputs:
                        for key, value in outputs.items():
                            if isinstance(value, str):
                                return value
                    return str(outputs)
                
                if state in ("FAILED", "CANCELLED"):
                    raise LlmError(f"Gumloop pipeline {state}: {data.get('error', 'Unknown error')}")
                
                time.sleep(2)
        
        raise LlmError("Gumloop pipeline timed out after 60 seconds")
    
    def _mock_generate(self) -> str:
        """Return a sample dashboard in WireframeLayout format (pixel-based)."""
        return """{
  "id": "layout-mock-001",
  "name": "SaaS Dashboard",
  "canvas_size": {"width": 1440, "height": 900},
  "background_color": "#f5f5f5",
  "source_type": "prompt",
  "components": [
    {
      "id": "nav-1",
      "type": "navbar",
      "position": {"x": 0, "y": 0},
      "size": {"width": 1440, "height": 64},
      "props": {"logo": "Logo", "links": ["Home", "Docs", "Pricing"], "cta": "Sign Up"},
      "children": [],
      "source": "llm"
    },
    {
      "id": "sidebar-1",
      "type": "sidebar",
      "position": {"x": 0, "y": 64},
      "size": {"width": 250, "height": 836},
      "props": {"items": ["Dashboard", "Settings", "Profile"]},
      "children": [],
      "source": "llm"
    },
    {
      "id": "heading-1",
      "type": "heading",
      "position": {"x": 280, "y": 94},
      "size": {"width": 400, "height": 48},
      "props": {"text": "Dashboard", "level": 1},
      "children": [],
      "source": "llm"
    },
    {
      "id": "card-1",
      "type": "card",
      "position": {"x": 280, "y": 170},
      "size": {"width": 350, "height": 150},
      "props": {"title": "Total Users", "content": "1,234"},
      "children": [],
      "source": "llm"
    },
    {
      "id": "card-2",
      "type": "card",
      "position": {"x": 660, "y": 170},
      "size": {"width": 350, "height": 150},
      "props": {"title": "Revenue", "content": "$12,345"},
      "children": [],
      "source": "llm"
    },
    {
      "id": "card-3",
      "type": "card",
      "position": {"x": 1040, "y": 170},
      "size": {"width": 350, "height": 150},
      "props": {"title": "Active Sessions", "content": "42"},
      "children": [],
      "source": "llm"
    },
    {
      "id": "chart-1",
      "type": "chart",
      "position": {"x": 280, "y": 350},
      "size": {"width": 730, "height": 300},
      "props": {"type": "line", "title": "User Growth"},
      "children": [],
      "source": "llm"
    },
    {
      "id": "table-1",
      "type": "table",
      "position": {"x": 280, "y": 680},
      "size": {"width": 1110, "height": 200},
      "props": {"columns": ["Name", "Email", "Status", "Actions"], "rows": 5},
      "children": [],
      "source": "llm"
    }
  ]
}"""

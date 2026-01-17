"""
LLM Client - Gemini API Integration

Uses Google's Gemini API for wireframe generation.
Supports mock mode for local testing without API calls.

Environment Variables:
- GEMINI_API_KEY: Your Google AI API key
- MOCK_LLM: Set to "1" to use mock responses (no API calls)
"""
from __future__ import annotations
import os
import json
import logging
from typing import Optional

import google.generativeai as genai

from backend.config import settings

logger = logging.getLogger(__name__)


class LlmError(Exception):
    """Exception raised for LLM-related errors."""
    pass


class LlmClient:
    """
    LLM client using Google Gemini API.
    
    Provider priority:
    1. If MOCK_LLM=1, use mock (always returns sample dashboard)
    2. Otherwise, use Gemini API
    
    Example:
        client = LlmClient()
        json_response = client.generate("create a SaaS dashboard")
    """
    
    def __init__(self) -> None:
        self.mock = os.getenv("MOCK_LLM", "0") == "1"
        
        if not self.mock:
            api_key = settings.gemini_api_key
            if not api_key:
                raise LlmError(
                    "GEMINI_API_KEY not configured. Options:\n"
                    "  1. Set GEMINI_API_KEY in .env file\n"
                    "  2. Set MOCK_LLM=1 for local testing without API"
                )
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name=settings.gemini_model,
                generation_config={
                    "temperature": settings.temperature,
                    "max_output_tokens": settings.max_tokens,
                    "response_mime_type": "application/json",
                }
            )
    
    def generate(self, prompt: str) -> str:
        """
        Generate wireframe JSON from prompt.
        
        Args:
            prompt: Full prompt including system instructions
            
        Returns:
            Raw JSON string from the model
        """
        if self.mock:
            logger.info("Using mock LLM response")
            return self._mock_generate()
        
        return self._gemini_generate(prompt)
    
    def _gemini_generate(self, prompt: str) -> str:
        """
        Call Gemini API to generate wireframe.
        
        Args:
            prompt: Full prompt with system + user instructions
            
        Returns:
            JSON string response from Gemini
        """
        try:
            logger.info(f"Calling Gemini API with model: {settings.gemini_model}")
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise LlmError("Gemini returned empty response")
            
            logger.debug(f"Gemini response length: {len(response.text)} chars")
            return response.text
            
        except genai.types.BlockedPromptException as e:
            raise LlmError(f"Prompt was blocked by safety filters: {e}") from e
        except genai.types.StopCandidateException as e:
            raise LlmError(f"Generation stopped unexpectedly: {e}") from e
        except Exception as e:
            raise LlmError(f"Gemini API error: {e}") from e
    
    def _mock_generate(self) -> str:
        """
        Return a sample dashboard in WireframeLayout format (pixel-based).
        Uses UPPERCASE component types to match CV pipeline.
        """
        return json.dumps({
            "id": "layout-mock-001",
            "name": "SaaS Dashboard",
            "canvas_size": {"width": 1440, "height": 900},
            "background_color": "#f5f5f5",
            "source_type": "prompt",
            "components": [
                {
                    "id": "nav-1",
                    "type": "NAVBAR",
                    "position": {"x": 0, "y": 0},
                    "size": {"width": 1440, "height": 64},
                    "props": {"logo": "Logo", "links": ["Home", "Docs", "Pricing"], "cta": "Sign Up"},
                    "children": [],
                    "source": "llm"
                },
                {
                    "id": "sidebar-1",
                    "type": "SIDEBAR",
                    "position": {"x": 0, "y": 64},
                    "size": {"width": 250, "height": 836},
                    "props": {"items": ["Dashboard", "Settings", "Profile"]},
                    "children": [],
                    "source": "llm"
                },
                {
                    "id": "heading-1",
                    "type": "HEADING",
                    "position": {"x": 280, "y": 94},
                    "size": {"width": 400, "height": 48},
                    "props": {"text": "Dashboard", "level": 1},
                    "children": [],
                    "source": "llm"
                },
                {
                    "id": "card-1",
                    "type": "CARD",
                    "position": {"x": 280, "y": 170},
                    "size": {"width": 350, "height": 150},
                    "props": {"title": "Total Users", "content": "1,234"},
                    "children": [],
                    "source": "llm"
                },
                {
                    "id": "card-2",
                    "type": "CARD",
                    "position": {"x": 660, "y": 170},
                    "size": {"width": 350, "height": 150},
                    "props": {"title": "Revenue", "content": "$12,345"},
                    "children": [],
                    "source": "llm"
                },
                {
                    "id": "card-3",
                    "type": "CARD",
                    "position": {"x": 1040, "y": 170},
                    "size": {"width": 350, "height": 150},
                    "props": {"title": "Active Sessions", "content": "42"},
                    "children": [],
                    "source": "llm"
                },
                {
                    "id": "chart-1",
                    "type": "CHART",
                    "position": {"x": 280, "y": 350},
                    "size": {"width": 730, "height": 300},
                    "props": {"type": "line", "title": "User Growth"},
                    "children": [],
                    "source": "llm"
                },
                {
                    "id": "table-1",
                    "type": "TABLE",
                    "position": {"x": 280, "y": 680},
                    "size": {"width": 1110, "height": 200},
                    "props": {"columns": ["Name", "Email", "Status", "Actions"], "rows": 5},
                    "children": [],
                    "source": "llm"
                }
            ]
        }, indent=2)

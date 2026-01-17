"""
Web Context Extraction
======================

Transform scraped pages into LLM-friendly context strings.
Optimized for Gemini prompts with structured pattern information.
"""
from __future__ import annotations
from typing import List, Dict, Set


def build_web_context(pages: List[Dict[str, str]], max_chars: int = 2500) -> str:
    """
    Turn scraped pages into a tight, model-friendly context blob.
    Optimized for Gemini to understand common design patterns.
    
    Args:
        pages: List of {"url", "title", "text"} dicts from scraper
        max_chars: Maximum context length to avoid prompt bloat
        
    Returns:
        Formatted context string for injection into LLM prompt
    """
    if not pages:
        return ""
    
    # Extract patterns and sources
    patterns = extract_patterns(pages)
    sources = extract_sources(pages)
    
    # Build structured context
    parts: List[str] = []
    
    # Add pattern summary
    if patterns:
        parts.append("Common design patterns found:")
        for pattern in sorted(patterns):
            parts.append(f"  - {pattern}")
    
    # Add source notes
    for p in pages:
        title = p.get("title", "").strip()
        text = p.get("text", "").strip()
        if text and text != title:
            # Truncate long text
            if len(text) > 300:
                text = text[:300] + "..."
            parts.append(f"\nFrom '{title}':")
            parts.append(f"  {text}")
    
    ctx = "\n".join(parts).strip()
    
    # Truncate if too long
    if len(ctx) > max_chars:
        ctx = ctx[:max_chars] + "\n..."
    
    return ctx


def extract_patterns(pages: List[Dict[str, str]]) -> Set[str]:
    """
    Extract UI component patterns mentioned across all pages.
    Returns a set of pattern names for deduplication.
    """
    # Keywords that represent UI components/sections
    component_keywords = {
        "navbar": ["navbar", "navigation", "nav bar", "top nav", "header nav"],
        "header": ["header", "top bar"],
        "hero": ["hero", "hero section", "banner", "hero banner"],
        "sidebar": ["sidebar", "side nav", "left nav", "side bar"],
        "footer": ["footer", "bottom bar"],
        "cards": ["card", "cards", "card grid", "card layout"],
        "table": ["table", "data table", "grid view"],
        "chart": ["chart", "graph", "visualization", "analytics"],
        "form": ["form", "input form", "contact form"],
        "button": ["button", "cta", "call to action"],
        "modal": ["modal", "popup", "dialog"],
        "tabs": ["tabs", "tab bar", "tabbed"],
        "dropdown": ["dropdown", "select", "menu"],
        "search": ["search", "search bar"],
        "pricing": ["pricing", "pricing table", "plans"],
        "testimonials": ["testimonial", "reviews", "quotes"],
        "features": ["features", "feature grid", "benefits"],
        "stats": ["stats", "statistics", "metrics", "kpi"],
    }
    
    found_patterns: Set[str] = set()
    all_text = " ".join(
        (p.get("text", "") + " " + p.get("title", "")).lower() 
        for p in pages
    )
    
    for pattern_name, keywords in component_keywords.items():
        for keyword in keywords:
            if keyword in all_text:
                found_patterns.add(pattern_name)
                break
    
    return found_patterns


def extract_sources(pages: List[Dict[str, str]]) -> List[str]:
    """
    Extract source URLs from pages.
    """
    return [p.get("url", "") for p in pages if p.get("url")]


def format_for_gemini(query: str, pages: List[Dict[str, str]]) -> str:
    """
    Format scraped data specifically for Gemini wireframe generation.
    
    Returns a structured prompt section that Gemini can use for context.
    """
    if not pages:
        return ""
    
    patterns = extract_patterns(pages)
    
    parts = [
        f"Design research for '{query}':",
        ""
    ]
    
    if patterns:
        parts.append("Typical UI patterns for this type of design:")
        for pattern in sorted(patterns):
            parts.append(f"  • {pattern}")
        parts.append("")
    
    parts.append("Key insights from research:")
    for p in pages[:3]:  # Limit to 3 sources
        title = p.get("title", "Design reference")
        text = p.get("text", "").strip()
        if text:
            # Take first 150 chars
            snippet = text[:150] + "..." if len(text) > 150 else text
            parts.append(f"  - {title}: {snippet}")
    
    return "\n".join(parts)

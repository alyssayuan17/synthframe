"""
Web Scraper Module
==================

Provides context for wireframe generation by matching user queries to proper UI patterns.
In a full production version, this would search the web.
For this hackathon version, we use a rich knowledge base of design patterns 
and basic URL metadata extraction.
"""

import re
from typing import Dict, List, Any

# Common UI patterns for different page types
PATTERN_KNOWLEDGE_BASE = {
    "landing": {
        "patterns": ["Hero Section", "Value Proposition", "Feature Grid", "Testimonials", "CTA Footer"],
        "layout": "single-column",
        "description": "Standard high-conversion landing page structure"
    },
    "dashboard": {
        "patterns": ["Sidebar Navigation", "Header with Search", "Stats Cards", "Data Table", "Charts"],
        "layout": "sidebar-left",
        "description": "Data-heavy dashboard with navigation"
    },
    "marketplace": {
        "patterns": ["Search Bar Hero", "Category Filters", "Product Grid", "Featured Items"],
        "layout": "single-column",
        "description": "E-commerce or marketplace listing style"
    },
    "profile": {
        "patterns": ["User Avatar Header", "Bio Section", "Activity Feed", "Settings Tabs"],
        "layout": "two-column",
        "description": "User profile or settings page"
    },
    "login": {
        "patterns": ["Centered Form", "Social Login", "Forgot Password Link"],
        "layout": "centered",
        "description": "Simple authentication flow"
    },
    "feed": {
        "patterns": ["Create Post Widget", "Infinite Scroll Feed", "Right Sidebar Trends"],
        "layout": "three-column",
        "description": "Social media style feed"
    }
}

def extract_keywords(query: str) -> List[str]:
    """Extract known page types from query."""
    query = query.lower()
    found = []
    for key in PATTERN_KNOWLEDGE_BASE:
        if key in query:
            found.append(key)
    
    # Defaults
    if "app" in query and not found:
        found.append("dashboard")
    if "site" in query or "web" in query and not found:
        found.append("landing")
        
    return found

def scrape_similar_sites(query: str) -> Dict[str, Any]:
    """
    Simulate web scraping by finding relevant design patterns.
    
    Args:
        query: User's prompt (e.g., "Student club landing page")
        
    Returns:
        Dict with identified patterns and context
    """
    # 1. Identify page type
    page_types = extract_keywords(query)
    primary_type = page_types[0] if page_types else "landing"
    
    # 2. Get knowledge base data
    data = PATTERN_KNOWLEDGE_BASE.get(primary_type, PATTERN_KNOWLEDGE_BASE["landing"])
    
    # 3. Simulate "scraping" result
    return {
        "patterns": data["patterns"],
        "suggested_layout": data["layout"],
        "design_notes": data["description"],
        "source": "knowledge_base",
        "detected_type": primary_type
    }

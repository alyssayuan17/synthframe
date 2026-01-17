"""
Pre-populated Design Patterns
=============================

Curated UI patterns for common design requests.
These provide reliable fallback when live scraping fails or for demo reliability.

Based on research from Dribbble, Behance, and UI-Patterns.com
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class DesignPattern:
    """A design pattern extracted from research."""
    name: str
    common_sections: List[str]
    style_hints: List[str] = field(default_factory=list)
    example_sources: List[str] = field(default_factory=list)


# Pre-populated patterns for common queries (demo reliability)
COMMON_PATTERNS: Dict[str, DesignPattern] = {
    # Dashboard patterns
    "dashboard": DesignPattern(
        name="Dashboard",
        common_sections=["sidebar", "top navbar", "stat cards", "charts", "data table", "activity feed"],
        style_hints=["dark mode popular", "card-based layout", "minimal icons"],
        example_sources=["dribbble.com/tags/dashboard"]
    ),
    "saas dashboard": DesignPattern(
        name="SaaS Dashboard",
        common_sections=["sidebar navigation", "metric cards (3-4)", "line/bar charts", "recent activity", "user avatar dropdown"],
        style_hints=["clean whitespace", "purple/blue gradients", "rounded corners"],
        example_sources=["dribbble.com/search/saas-dashboard"]
    ),
    "admin panel": DesignPattern(
        name="Admin Panel",
        common_sections=["collapsible sidebar", "breadcrumbs", "data tables with pagination", "filters", "action buttons"],
        style_hints=["functional over aesthetic", "dense information", "icon + text nav"],
        example_sources=["dribbble.com/search/admin-panel"]
    ),
    "analytics dashboard": DesignPattern(
        name="Analytics Dashboard",
        common_sections=["KPI cards", "time range selector", "multiple chart types", "comparison metrics", "export button"],
        style_hints=["data-dense", "chart-focused", "subtle colors"],
        example_sources=["dribbble.com/search/analytics"]
    ),
    
    # Landing page patterns
    "landing page": DesignPattern(
        name="Landing Page",
        common_sections=["navbar with CTA", "hero with headline", "features grid", "testimonials", "pricing table", "FAQ", "footer"],
        style_hints=["bold hero text", "gradient backgrounds", "social proof"],
        example_sources=["dribbble.com/tags/landing-page"]
    ),
    "saas landing": DesignPattern(
        name="SaaS Landing Page",
        common_sections=["sticky navbar", "hero with product screenshot", "feature highlights", "integration logos", "pricing tiers", "testimonial carousel"],
        style_hints=["product mockups", "trust badges", "free trial CTA"],
        example_sources=["dribbble.com/search/saas-landing"]
    ),
    "startup landing": DesignPattern(
        name="Startup Landing",
        common_sections=["minimal navbar", "bold hero statement", "how it works", "team section", "investor logos", "waitlist form"],
        style_hints=["modern typography", "animations", "gradient CTAs"],
        example_sources=["dribbble.com/search/startup-landing"]
    ),
    
    # E-commerce patterns
    "e-commerce": DesignPattern(
        name="E-commerce",
        common_sections=["search bar", "category navigation", "product grid", "filters sidebar", "cart icon", "promotions banner"],
        style_hints=["product images prominent", "price visibility", "add to cart buttons"],
        example_sources=["dribbble.com/tags/ecommerce"]
    ),
    "product page": DesignPattern(
        name="Product Page",
        common_sections=["product gallery", "price and variants", "add to cart", "description tabs", "reviews", "related products"],
        style_hints=["large product images", "clear pricing", "trust signals"],
        example_sources=["dribbble.com/search/product-page"]
    ),
    "checkout": DesignPattern(
        name="Checkout Flow",
        common_sections=["progress steps", "order summary", "shipping form", "payment form", "promo code input", "place order CTA"],
        style_hints=["minimal distractions", "security badges", "clear totals"],
        example_sources=["dribbble.com/search/checkout"]
    ),
    
    # Authentication patterns
    "login": DesignPattern(
        name="Login Page",
        common_sections=["logo", "email/password inputs", "remember me", "forgot password link", "login button", "social login options", "signup link"],
        style_hints=["centered card", "split screen with image", "minimal"],
        example_sources=["dribbble.com/search/login"]
    ),
    "signup": DesignPattern(
        name="Signup Page",
        common_sections=["logo", "name/email/password inputs", "terms checkbox", "signup button", "social signup", "login link"],
        style_hints=["progress indicator for multi-step", "benefit highlights"],
        example_sources=["dribbble.com/search/signup"]
    ),
    
    # Other common patterns
    "portfolio": DesignPattern(
        name="Portfolio",
        common_sections=["hero with name", "about section", "project gallery", "skills", "contact form", "social links"],
        style_hints=["personal branding", "project thumbnails", "minimal"],
        example_sources=["dribbble.com/search/portfolio"]
    ),
    "blog": DesignPattern(
        name="Blog",
        common_sections=["header", "featured post", "post grid/list", "categories sidebar", "newsletter signup", "author bio"],
        style_hints=["readable typography", "thumbnail images", "tags"],
        example_sources=["dribbble.com/search/blog"]
    ),
    "pricing": DesignPattern(
        name="Pricing Page",
        common_sections=["plan comparison cards", "feature checklist", "toggle monthly/yearly", "popular badge", "CTA buttons", "FAQ"],
        style_hints=["highlight recommended plan", "clear pricing", "feature tooltips"],
        example_sources=["dribbble.com/search/pricing"]
    ),
    "settings": DesignPattern(
        name="Settings Page",
        common_sections=["settings sidebar/tabs", "profile section", "notification toggles", "security settings", "billing info", "save button"],
        style_hints=["grouped settings", "form-heavy", "confirmation modals"],
        example_sources=["dribbble.com/search/settings"]
    ),
}


def get_pattern(query: str) -> Optional[DesignPattern]:
    """
    Find a matching pattern for the query.
    Uses fuzzy matching on keywords.
    """
    query_lower = query.lower().strip()
    
    # Direct match
    if query_lower in COMMON_PATTERNS:
        return COMMON_PATTERNS[query_lower]
    
    # Partial match (any keyword in query matches a pattern key)
    for key, pattern in COMMON_PATTERNS.items():
        key_words = set(key.split())
        query_words = set(query_lower.split())
        if key_words & query_words:  # intersection
            return pattern
    
    return None


def pattern_to_context(pattern: DesignPattern) -> str:
    """
    Convert a DesignPattern to a context string for the LLM.
    """
    sections = ", ".join(pattern.common_sections)
    hints = ", ".join(pattern.style_hints) if pattern.style_hints else "modern, clean"
    
    return (
        f"Common patterns for '{pattern.name}':\n"
        f"  Typical sections: {sections}\n"
        f"  Style trends: {hints}"
    )


def get_cached_context(query: str) -> Optional[str]:
    """
    Get pre-populated context for a query if available.
    Returns None if no cached pattern exists.
    """
    pattern = get_pattern(query)
    if pattern:
        return pattern_to_context(pattern)
    return None

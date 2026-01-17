"""
Scraper Client
==============

Pluggable scraper backend with support for:
- mock: Returns hardcoded test data
- httpx: Real HTTP scraping of Dribbble search results

Set SCRAPER_PROVIDER environment variable to choose provider.
"""
from __future__ import annotations
from typing import List, Dict, Optional
import os
import re
import httpx
from bs4 import BeautifulSoup

from backend.scraper.cache import get_cache
from backend.scraper.patterns import get_cached_context


class ScraperError(Exception):
    """Raised when scraping fails."""
    pass


class ScraperClient:
    """
    Pluggable scraper backend: mock | httpx
    Returns list of pages: [{"url":..., "title":..., "text":...}, ...]
    
    Usage:
        client = ScraperClient()
        results = client.scrape("SaaS dashboard", max_pages=3)
    """
    
    # Dribbble search URL template
    DRIBBBLE_SEARCH_URL = "https://dribbble.com/search?q={query}"
    
    # User agent to avoid being blocked
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) SynthFrame/1.0"
    
    def __init__(self) -> None:
        self.provider = os.getenv("SCRAPER_PROVIDER", "mock")
        self._cache = get_cache()

    def scrape(
        self, 
        query: str, 
        max_pages: int = 3, 
        timeout_s: float = 10.0,
        use_cache: bool = True
    ) -> List[Dict[str, str]]:
        """
        Scrape design inspiration for the given query.
        
        Args:
            query: Search query like "SaaS dashboard"
            max_pages: Maximum number of results to return
            timeout_s: HTTP timeout in seconds
            use_cache: Whether to use cached results
            
        Returns:
            List of dicts with url, title, and text keys
        """
        # Check cache first
        if use_cache:
            cached = self._cache.get(query)
            if cached:
                return cached[:max_pages]
        
        # Select provider
        if self.provider == "mock":
            results = self._mock_scrape(query)
        elif self.provider == "httpx":
            results = self._httpx_scrape(query, max_pages, timeout_s)
        else:
            # Unknown provider - try httpx, fall back to mock
            try:
                results = self._httpx_scrape(query, max_pages, timeout_s)
            except Exception:
                results = self._mock_scrape(query)
        
        # Cache results
        if results and use_cache:
            self._cache.set(query, results)
        
        return results[:max_pages]

    def _mock_scrape(self, query: str) -> List[Dict[str, str]]:
        """
        Return mock data for testing.
        First tries pre-populated patterns, then generic fallback.
        """
        # Try pre-populated patterns first
        context = get_cached_context(query)
        if context:
            return [{
                "url": "https://pre-populated/patterns",
                "title": f"Design patterns for: {query}",
                "text": context
            }]
        
        # Generic fallback
        return [{
            "url": "https://example.com/patterns",
            "title": "Common UI patterns",
            "text": (
                f"Query='{query}'. Typical layout: navbar + hero + feature cards + "
                "pricing section + footer. For dashboards: sidebar + top nav + "
                "stat cards + table + chart."
            )
        }]

    def _httpx_scrape(
        self, 
        query: str, 
        max_pages: int, 
        timeout_s: float
    ) -> List[Dict[str, str]]:
        """
        Scrape Dribbble search results via HTTP.
        
        Extracts:
        - Shot titles
        - Designer names
        - Tags/keywords
        """
        url = self.DRIBBBLE_SEARCH_URL.format(query=query.replace(" ", "+"))
        
        try:
            with httpx.Client(timeout=timeout_s) as client:
                response = client.get(
                    url,
                    headers={
                        "User-Agent": self.USER_AGENT,
                        "Accept": "text/html",
                        "Accept-Language": "en-US,en;q=0.9",
                    },
                    follow_redirects=True
                )
                response.raise_for_status()
                
        except httpx.TimeoutException:
            # Timeout - fall back to pre-populated patterns
            return self._mock_scrape(query)
        except httpx.HTTPError as e:
            # HTTP error - fall back to pre-populated patterns
            return self._mock_scrape(query)
        
        # Parse HTML
        return self._parse_dribbble_html(response.text, query, max_pages)

    def _parse_dribbble_html(
        self, 
        html: str, 
        query: str, 
        max_results: int
    ) -> List[Dict[str, str]]:
        """
        Parse Dribbble search results HTML.
        Extracts shot titles and descriptions.
        """
        soup = BeautifulSoup(html, "html.parser")
        results: List[Dict[str, str]] = []
        
        # Find shot cards (Dribbble uses various class names)
        # Try multiple selectors for robustness
        shots = (
            soup.select("li.shot-thumbnail") or
            soup.select("[data-thumbnail]") or
            soup.select(".shot-thumbnail-base") or
            soup.select("figure")  # Fallback
        )
        
        for shot in shots[:max_results]:
            title = ""
            text = ""
            url = ""
            
            # Try to extract title
            title_elem = (
                shot.select_one(".shot-title") or
                shot.select_one("a[data-shot-title]") or
                shot.select_one("a") or
                shot.select_one("figcaption")
            )
            if title_elem:
                title = title_elem.get_text(strip=True)
                # Get URL if available
                href = title_elem.get("href", "")
                if href:
                    url = f"https://dribbble.com{href}" if href.startswith("/") else href
            
            # Try to extract additional text (description, tags)
            desc_elem = shot.select_one(".shot-desc") or shot.select_one("p")
            if desc_elem:
                text = desc_elem.get_text(strip=True)
            
            # Skip empty results
            if not title:
                continue
            
            results.append({
                "url": url or f"https://dribbble.com/search?q={query}",
                "title": title,
                "text": text or f"Design inspiration for {query}"
            })
        
        # If no results found, return pre-populated patterns
        if not results:
            return self._mock_scrape(query)
        
        return results

    def scrape_with_patterns(
        self, 
        query: str, 
        max_pages: int = 3
    ) -> Dict[str, any]:
        """
        Scrape and return both raw results and extracted patterns.
        
        Returns:
            {
                "results": [...],
                "patterns": ["navbar", "hero", ...],
                "source": "httpx" | "mock" | "cache"
            }
        """
        # Check cache
        cached = self._cache.get(query)
        if cached:
            return {
                "results": cached[:max_pages],
                "patterns": self._extract_patterns_from_results(cached),
                "source": "cache"
            }
        
        # Scrape
        results = self.scrape(query, max_pages)
        
        return {
            "results": results,
            "patterns": self._extract_patterns_from_results(results),
            "source": self.provider
        }
    
    def _extract_patterns_from_results(
        self, 
        results: List[Dict[str, str]]
    ) -> List[str]:
        """
        Extract common UI patterns mentioned in results.
        """
        # Keywords to look for
        component_keywords = [
            "navbar", "nav", "header", "hero", "sidebar", "footer",
            "card", "cards", "grid", "table", "chart", "form",
            "button", "modal", "dropdown", "tabs", "menu",
            "login", "signup", "dashboard", "profile", "settings",
            "pricing", "testimonial", "feature", "cta", "banner"
        ]
        
        found_patterns = set()
        all_text = " ".join(r.get("text", "") + " " + r.get("title", "") for r in results)
        all_text_lower = all_text.lower()
        
        for keyword in component_keywords:
            if keyword in all_text_lower:
                found_patterns.add(keyword)
        
        return list(found_patterns)

from __future__ import annotations
from typing import List, Dict
import os


class ScraperError(Exception):
    pass


class ScraperClient:
    """
    Pluggable backend: mock | firecrawl | playwright
    Returns list of pages: [{"url":..., "title":..., "text":...}, ...]
    """
    def __init__(self) -> None:
        self.provider = os.getenv("SCRAPER_PROVIDER", "mock")

    def scrape(self, query: str, max_pages: int, timeout_s: float) -> List[Dict[str, str]]:
        if self.provider == "mock":
            return self._mock(query)
        # TODO: implement real provider
        raise ScraperError(f"Scraper provider not configured: {self.provider}")

    def _mock(self, query: str) -> List[Dict[str, str]]:
        return [
            {
                "url": "https://example.com/patterns",
                "title": "Common UI patterns",
                "text": f"Query='{query}'. Typical layout: navbar + hero + feature cards + pricing section + footer. "
                        "For dashboards: sidebar + top nav + stat cards + table + chart."
            }
        ]

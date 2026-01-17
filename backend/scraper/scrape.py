from __future__ import annotations
from typing import Optional

from backend.config import SCRAPER_MAX_PAGES, SCRAPER_TIMEOUT_S, SCRAPER_ALLOWLIST
from backend.scraper.client import ScraperClient
from backend.scraper.extract import build_web_context
from backend.scraper.policies import ScrapePolicies


def scrape_context(user_input: str, max_pages: Optional[int] = None) -> str:
    policies = ScrapePolicies(
        max_pages=max_pages or SCRAPER_MAX_PAGES,
        timeout_s=SCRAPER_TIMEOUT_S,
        allowlist=SCRAPER_ALLOWLIST or None,
    )

    client = ScraperClient()
    pages = client.scrape(user_input, max_pages=policies.max_pages, timeout_s=policies.timeout_s)

    # (Optional) enforce allowlist if your scraper returns URLs
    filtered = [p for p in pages if policies.domain_allowed(p.get("url", ""))]

    return build_web_context(filtered)

"""
Scraper Cache
=============

In-memory cache with TTL support for scraped results.
Pre-populates with common patterns on import.
"""
from __future__ import annotations
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass, field
import time


@dataclass
class CacheEntry:
    """A cached scrape result with expiration."""
    data: List[dict]
    created_at: float
    ttl_seconds: float = 3600  # 1 hour default
    
    @property
    def is_expired(self) -> bool:
        return time.time() > (self.created_at + self.ttl_seconds)


class SimpleCache:
    """
    In-memory cache with TTL and pre-population support.
    
    Usage:
        cache = SimpleCache()
        cache.set("query", [{"url": "...", "title": "...", "text": "..."}])
        result = cache.get("query")  # Returns None if expired
    """
    
    DEFAULT_TTL = 3600  # 1 hour
    
    def __init__(self, default_ttl: float = DEFAULT_TTL) -> None:
        self._store: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl
        self._pre_populate()

    def get(self, key: str) -> Optional[List[dict]]:
        """Get cached data if exists and not expired."""
        key_lower = key.lower().strip()
        entry = self._store.get(key_lower)
        
        if entry is None:
            return None
        
        if entry.is_expired:
            del self._store[key_lower]
            return None
        
        return entry.data

    def set(self, key: str, value: List[dict], ttl: Optional[float] = None) -> None:
        """Cache data with optional custom TTL."""
        key_lower = key.lower().strip()
        self._store[key_lower] = CacheEntry(
            data=value,
            created_at=time.time(),
            ttl_seconds=ttl or self._default_ttl
        )
    
    def has(self, key: str) -> bool:
        """Check if key exists and is not expired."""
        return self.get(key) is not None
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._store.clear()
    
    def stats(self) -> dict:
        """Get cache statistics."""
        total = len(self._store)
        expired = sum(1 for e in self._store.values() if e.is_expired)
        return {
            "total_entries": total,
            "expired_entries": expired,
            "active_entries": total - expired
        }
    
    def _pre_populate(self) -> None:
        """
        Pre-populate cache with common design pattern queries.
        Uses patterns from patterns.py for reliability.
        """
        from backend.scraper.patterns import COMMON_PATTERNS, pattern_to_context
        
        # Set very long TTL for pre-populated entries (24 hours)
        pre_pop_ttl = 86400
        
        for query_key, pattern in COMMON_PATTERNS.items():
            context = pattern_to_context(pattern)
            # Store as list of page-like dicts for compatibility
            self.set(
                query_key,
                [{
                    "url": f"https://pre-populated/{query_key.replace(' ', '-')}",
                    "title": pattern.name,
                    "text": context
                }],
                ttl=pre_pop_ttl
            )


# Global cache instance
_cache: Optional[SimpleCache] = None


def get_cache() -> SimpleCache:
    """Get or create the global cache instance."""
    global _cache
    if _cache is None:
        _cache = SimpleCache()
    return _cache

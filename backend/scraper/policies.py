from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ScrapePolicies:
    max_pages: int = 3
    timeout_s: float = 10.0
    allowlist: Optional[List[str]] = None  # domains allowed; None/empty = allow all (not recommended)

    def domain_allowed(self, url: str) -> bool:
        if not self.allowlist:
            return True
        return any(d in url for d in self.allowlist)

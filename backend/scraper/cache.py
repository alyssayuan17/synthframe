from __future__ import annotations
from typing import Dict, Tuple, List


class SimpleCache:
    def __init__(self) -> None:
        self._store: Dict[str, Tuple[float, List[dict]]] = {}

    def get(self, key: str):
        return self._store.get(key)

    def set(self, key: str, value):
        self._store[key] = value

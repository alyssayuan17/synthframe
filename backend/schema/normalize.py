from __future__ import annotations
from typing import List
import uuid

from backend.models.wireframe import WireframeDoc, Component, Connection


def _ensure_component_ids(components: List[Component], prefix: str = "cmp") -> None:
    stack = list(components)
    while stack:
        c = stack.pop()
        if not c.id:
            c.id = f"{prefix}-{uuid.uuid4().hex[:8]}"
        if c.children:
            stack.extend(c.children)


def _ensure_connection_ids(connections: List[Connection], prefix: str = "conn") -> None:
    for conn in connections:
        if not conn.id:
            conn.id = f"{prefix}-{uuid.uuid4().hex[:8]}"


def normalize_wireframe(doc: WireframeDoc) -> WireframeDoc:
    _ensure_component_ids(doc.components)
    _ensure_connection_ids(doc.connections)
    return doc

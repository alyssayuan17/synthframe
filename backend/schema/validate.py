from __future__ import annotations
from typing import List, Set, Tuple

from backend.models.wireframe import WireframeDoc, Component


class ValidationError(Exception):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.details = details or {}


def _walk_components(components: List[Component]) -> List[Component]:
    out: List[Component] = []
    stack = list(components)
    while stack:
        c = stack.pop()
        out.append(c)
        if c.children:
            stack.extend(c.children)
    return out


def validate_wireframe(doc: WireframeDoc) -> None:
    all_components = _walk_components(doc.components)

    # Unique IDs
    seen: Set[str] = set()
    dupes: Set[str] = set()
    for c in all_components:
        if c.id in seen:
            dupes.add(c.id)
        seen.add(c.id)
    if dupes:
        raise ValidationError("Duplicate component ids found.", {"duplicate_ids": sorted(dupes)})

    # Grid sanity
    bad_positions: List[Tuple[str, int, int]] = []
    for c in all_components:
        if c.position is None:
            continue
        if c.position.col + c.position.colSpan > 12:
            bad_positions.append((c.id, c.position.col, c.position.colSpan))
    if bad_positions:
        raise ValidationError(
            "Some components exceed the 12-column grid (col + colSpan > 12).",
            {"bad_positions": [{"id": i, "col": col, "colSpan": span} for (i, col, span) in bad_positions]},
        )

    # Connections reference real components
    missing: List[dict] = []
    for conn in doc.connections:
        if conn.from_.componentId not in seen:
            missing.append({"connection_id": conn.id, "missing_component_id": conn.from_.componentId, "side": "from"})
        if conn.to.componentId not in seen:
            missing.append({"connection_id": conn.id, "missing_component_id": conn.to.componentId, "side": "to"})
    if missing:
        raise ValidationError("Some connections reference missing component IDs.", {"missing_references": missing})

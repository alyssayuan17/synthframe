from __future__ import annotations
from typing import List, Dict


def build_web_context(pages: List[Dict[str, str]], max_chars: int = 2500) -> str:
    """
    Turn scraped pages into a tight, model-friendly context blob.
    Keep short and action-oriented (patterns/components/copy ideas).
    """
    parts: List[str] = []
    for p in pages:
        url = p.get("url", "")
        title = p.get("title", "")
        text = p.get("text", "").strip()
        if not text:
            continue
        parts.append(f"- Source: {title} ({url})\n  Notes: {text}")

    ctx = "\n".join(parts).strip()
    if len(ctx) > max_chars:
        ctx = ctx[:max_chars] + "..."
    return ctx

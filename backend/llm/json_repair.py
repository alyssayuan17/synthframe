from __future__ import annotations
import json
from typing import Any, Dict


class JsonParseError(Exception):
    pass


def extract_json_object(text: str) -> str:
    t = text.strip()

    # Remove ``` fences if present
    if t.startswith("```"):
        t = "\n".join([line for line in t.splitlines() if not line.strip().startswith("```")]).strip()

    start = t.find("{")
    end = t.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise JsonParseError("Could not locate a JSON object in model output.")
    return t[start : end + 1]


def parse_json(text: str) -> Dict[str, Any]:
    raw = extract_json_object(text)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise JsonParseError(f"Invalid JSON: {e.msg} at line {e.lineno} col {e.colno}") from e

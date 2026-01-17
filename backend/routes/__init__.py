"""
Route handlers for the Wireframe Designer API
"""
from . import vision
from . import health
from . import generate
from . import edit
from . import scrape

__all__ = ["vision", "health", "generate", "edit", "scrape"]

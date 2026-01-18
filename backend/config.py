"""
Configuration Management
========================

Centralizes all configuration: API keys, settings, constants.

HOW TO USE:
1. Create a .env file in the backend folder with:
   GEMINI_API_KEY=your_key_here
   
2. Import settings anywhere:
   from config import settings
   settings.gemini_api_key
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file from backend directory
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Create a .env file with these values.
    """
    
    # ===========================================
    # API KEYS
    # ===========================================
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    # ===========================================
    # DATABASE
    # ===========================================
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_db_name: str = os.getenv("MONGODB_DB_NAME", "synthframe")
    
    # ===========================================
    # CV/IMAGE PROCESSING SETTINGS
    # ===========================================
    
    # Canny edge detection thresholds
    canny_low_threshold: int = 50
    canny_high_threshold: int = 150
    
    # Minimum contour area to consider (filters out noise)
    min_contour_area: int = 500
    
    # Gaussian blur kernel size (must be odd)
    blur_kernel_size: int = 5
    
    # Threshold for binary conversion
    binary_threshold: int = 127
    
    # ===========================================
    # WIREFRAME DEFAULTS
    # ===========================================
    default_canvas_width: int = 1440
    default_canvas_height: int = 900
    default_device_type: str = "laptop"
    
    # ===========================================
    # LLM SETTINGS
    # ===========================================
    gemini_model: str = "gemini-2.0-flash"
    max_tokens: int = 4096
    temperature: float = 0.7
    mock_llm: bool = False  # Set to True to use mock responses instead of real API
    
    # ===========================================
    # SERVER SETTINGS
    # ===========================================
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance - import this elsewhere
settings = Settings()

# ===========================================
# SCRAPER SETTINGS (module-level constants)
# ===========================================
SCRAPER_MAX_PAGES: int = 3
SCRAPER_TIMEOUT_S: float = 10.0
SCRAPER_ALLOWLIST: list = ["dribbble.com", "behance.net", "awwwards.com"]
ENABLE_SCRAPER_DEFAULT: bool = True


# ===========================================
# DEVICE TYPE CANVAS SIZES
# ===========================================
# Canvas dimensions for different device types
# Used by both CV pipeline and Gemini generation
DEVICE_CANVAS_SIZES: dict = {
    "macbook": {"width": 1440, "height": 900},
    "iphone": {"width": 393, "height": 852},  # iPhone 14/15 Pro dimensions
}

# Default device type if not specified
DEFAULT_DEVICE_TYPE: str = "macbook"


# ===========================================
# COMPONENT DETECTION RULES
# ===========================================
# These rules help CV map detected shapes to component types
# based on position and size ratios

DETECTION_RULES = {
    # If a rectangle is at y < 10% of image height and spans > 80% width → NAVBAR
    "NAVBAR": {
        "y_ratio_max": 0.12,      # Top 12% of image
        "width_ratio_min": 0.7,   # At least 70% of image width
        "height_ratio_max": 0.15  # Not too tall
    },
    # If rectangle is large (> 30% of image) and near top → HERO
    "HERO": {
        "y_ratio_max": 0.35,      # In top 35%
        "area_ratio_min": 0.15,   # At least 15% of image area
    },
    # If at bottom of image → FOOTER
    "FOOTER": {
        "y_ratio_min": 0.85,      # In bottom 15%
        "width_ratio_min": 0.7,   # Wide
    },
    # If tall and narrow on left side → SIDEBAR
    "SIDEBAR": {
        "x_ratio_max": 0.3,       # On left 30%
        "height_ratio_min": 0.5,  # At least 50% of image height
        "width_ratio_max": 0.35,  # Narrow
    },
    # Small rectangles in a grid pattern → CARD
    "CARD": {
        "area_ratio_max": 0.15,   # Smaller boxes
        "aspect_ratio_range": (0.5, 2.0),  # Roughly square-ish
    },
    # Very small rectangles → BUTTON
    "BUTTON": {
        "area_ratio_max": 0.03,   # Very small
        "aspect_ratio_range": (1.5, 6.0),  # Wide and short
    }
}

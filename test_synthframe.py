r"""
SynthFrame Comprehensive Test Suite
====================================

Tests the full pipeline for both TEXT and IMAGE input paths.
Run ONE test at a time using command-line flags.

USAGE:
------

1. SETUP (run once):
   cd c:\Users\leo8j\project\synthframe
   pip install -r backend/requirements.txt

2. TEST TEXT PIPELINE (Gemini):
   python test_synthframe.py --text

3. TEST IMAGE PIPELINE (CV):
   python test_synthframe.py --image

4. TEST DEVICE TYPES:
   python test_synthframe.py --devices

5. TEST SPECIFIC DEVICE:
   python test_synthframe.py --text --device phone

6. RUN ALL TESTS:
   python test_synthframe.py --all

ENVIRONMENT VARIABLES:
----------------------
- MOCK_LLM=1         Use mock responses (no API calls)
- MOCK_LLM=0         Use real Gemini API (requires GEMINI_API_KEY)
- GEMINI_API_KEY     Your Gemini API key

EXAMPLES:
---------
# Quick test with mock (no API key needed)
$env:MOCK_LLM = "1"
python test_synthframe.py --text

# Test with real Gemini API
$env:MOCK_LLM = "0"
$env:GEMINI_API_KEY = "your-api-key"
python test_synthframe.py --text

"""

import sys
import os
import argparse
import json
import base64
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Load environment variables from backend/.env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / "backend" / ".env"
    load_dotenv(env_path)
    print(f"Loaded config from {env_path}")
except ImportError:
    print("Warning: python-dotenv not installed, skipping .env load")

# Set default to mock mode only if not already set
if "MOCK_LLM" not in os.environ:
    os.environ["MOCK_LLM"] = "1"


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(name: str, passed: bool, details: str = ""):
    """Print a test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status}  {name}")
    if details:
        for line in details.split("\n"):
            print(f"         {line}")


def create_test_sketch_base64() -> str:
    """
    Create a simple black-and-white test image as base64.
    Simulates a hand-drawn sketch with rectangles.
    """
    try:
        import cv2
        import numpy as np
        
        # Create white canvas
        img = np.ones((600, 800, 3), dtype=np.uint8) * 255
        
        # Draw black rectangles to simulate sketch
        # Navbar at top
        cv2.rectangle(img, (10, 10), (790, 60), (0, 0, 0), 3)
        cv2.putText(img, "NAVBAR", (350, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Hero section
        cv2.rectangle(img, (10, 80), (790, 250), (0, 0, 0), 3)
        cv2.putText(img, "HERO", (370, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Three cards
        for i in range(3):
            x = 20 + i * 260
            cv2.rectangle(img, (x, 270), (x + 240, 420), (0, 0, 0), 3)
            cv2.putText(img, f"CARD {i+1}", (x + 80, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        # Footer
        cv2.rectangle(img, (10, 540), (790, 590), (0, 0, 0), 3)
        cv2.putText(img, "FOOTER", (350, 575), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Encode to base64
        _, buffer = cv2.imencode('.png', img)
        base64_str = base64.b64encode(buffer).decode('utf-8')
        return f"data:image/png;base64,{base64_str}"
        
    except ImportError:
        # Fallback: return a minimal valid PNG as base64 (1x1 white pixel)
        minimal_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        return f"data:image/png;base64,{minimal_png}"


# =============================================================================
# TEXT PIPELINE TESTS
# =============================================================================

def test_text_pipeline(device_type: str = None) -> bool:
    """
    Test the text-to-wireframe generation pipeline.
    
    Flow: Text prompt → Gemini → WireframeLayout JSON
    """
    print_header(f"TEXT PIPELINE TEST (device: {device_type or 'laptop'})")
    
    all_passed = True
    
    # Test 1: Import check
    try:
        from backend.generation.generate import generate_wireframe, GenerationError
        from backend.models.wireframe import WireframeLayout
        print_result("Import generation module", True)
    except ImportError as e:
        print_result("Import generation module", False, str(e))
        return False
    
    # Test 2: Basic generation
    try:
        layout, context = generate_wireframe(
            user_input="Create a simple dashboard with a navbar, sidebar, and two cards",
            use_scraper=False,
            device_type=device_type,
        )
        
        passed = isinstance(layout, WireframeLayout) and len(layout.components) > 0
        details = f"Generated {len(layout.components)} components"
        if device_type:
            details += f", canvas: {layout.canvas_size.width}x{layout.canvas_size.height}"
        print_result("Generate wireframe from text", passed, details)
        all_passed = all_passed and passed
        
    except Exception as e:
        print_result("Generate wireframe from text", False, str(e))
        all_passed = False
        return all_passed
    
    # Test 3: Component type validation
    try:
        valid_types = ["NAVBAR", "SIDEBAR", "CARD", "HERO", "FOOTER", "HEADING", 
                       "BUTTON", "FORM", "TABLE", "CHART", "SECTION", "TEXT", "IMAGE"]
        all_valid = all(comp.type in valid_types for comp in layout.components)
        
        types_found = [comp.type for comp in layout.components]
        print_result("Component types are valid", all_valid, f"Types: {types_found}")
        all_passed = all_passed and all_valid
        
    except Exception as e:
        print_result("Component types are valid", False, str(e))
        all_passed = False
    
    # Test 4: Position/size validation
    try:
        all_have_position = all(
            hasattr(comp.position, 'x') and hasattr(comp.position, 'y')
            for comp in layout.components
        )
        all_have_size = all(
            hasattr(comp.size, 'width') and hasattr(comp.size, 'height')
            for comp in layout.components
        )
        passed = all_have_position and all_have_size
        print_result("Components have position and size", passed)
        all_passed = all_passed and passed
        
    except Exception as e:
        print_result("Components have position and size", False, str(e))
        all_passed = False
    
    return all_passed


# =============================================================================
# IMAGE PIPELINE TESTS
# =============================================================================

def test_image_pipeline(device_type: str = None) -> bool:
    """
    Test the CV/image analysis pipeline.
    
    Flow: Image → OpenCV → Component detection → WireframeLayout
    """
    print_header(f"IMAGE PIPELINE TEST (device: {device_type or 'laptop'})")
    
    all_passed = True
    
    # Test 1: CV dependencies
    try:
        import cv2
        import numpy as np
        print_result("CV2 and NumPy available", True, f"OpenCV version: {cv2.__version__}")
    except ImportError as e:
        print_result("CV2 and NumPy available", False, str(e))
        print("         → Install with: pip install opencv-python numpy")
        return False
    
    # Test 2: Import vision module
    try:
        from backend.vision.image_to_text import analyze_sketch
        print_result("Import vision module", True)
    except ImportError as e:
        print_result("Import vision module", False, str(e))
        return False
    
    # Test 3: Create test image
    try:
        test_image = create_test_sketch_base64()
        passed = test_image.startswith("data:image/png;base64,")
        print_result("Create test sketch image", passed, f"Length: {len(test_image)} chars")
        all_passed = all_passed and passed
    except Exception as e:
        print_result("Create test sketch image", False, str(e))
        return False
    
    # Test 4: Analyze sketch
    try:
        result = analyze_sketch(
            image_base64=test_image,
            return_debug_image=True,
            wireframe_name="Test Sketch"
        )
        
        passed = len(result.components) > 0
        types_found = [c.type.value for c in result.components]
        print_result("Analyze sketch image", passed, f"Detected: {types_found}")
        all_passed = all_passed and passed
        
    except Exception as e:
        print_result("Analyze sketch image", False, str(e))
        all_passed = False
        return all_passed
    
    # Test 5: Wireframe output structure
    try:
        wireframe = result.wireframe
        has_id = hasattr(wireframe, 'id') and wireframe.id
        has_components = hasattr(wireframe, 'components') and len(wireframe.components) > 0
        
        passed = has_id and has_components
        print_result("Wireframe has valid structure", passed, f"ID: {wireframe.id}")
        all_passed = all_passed and passed
        
    except Exception as e:
        print_result("Wireframe has valid structure", False, str(e))
        all_passed = False
    
    # Test 6: Debug image generated
    try:
        passed = result.debug_image_base64 is not None
        print_result("Debug image generated", passed)
        all_passed = all_passed and passed
    except Exception as e:
        print_result("Debug image generated", False, str(e))
        all_passed = False

    # Test 7: Gemini Refinement (if not in mock mode or explicit request)
    mock_mode = os.getenv("MOCK_LLM", "0") == "1"
    if not mock_mode:
        print("\n  [Testing Gemini Refinement]")
        try:
            from backend.generation.refine import refine_cv_components
            from backend.models.wireframe import WireframeComponent, Size
            
            # Convert to WireframeComponents
            cv_components = []
            for comp in result.wireframe.components:
                # Use model_dump() to avoid Pydantic class mismatch issues
                # (imported as backend.models vs models)
                cv_components.append(WireframeComponent(
                    id=comp.id,
                    type=comp.type.value,
                    position=comp.position.model_dump(),
                    size=comp.size.model_dump(),
                    props=comp.props,
                    confidence=comp.confidence,
                    source="cv"
                ))
            
            refined_layout = refine_cv_components(
                detected_components=cv_components,
                device_type=device_type,
                original_size=result.original_size
            )
            
            passed = len(refined_layout.components) > 0
            print_result("Gemini refinement successful", passed, f"Refined: {len(refined_layout.components)} components")
            all_passed = all_passed and passed
            
        except Exception as e:
            print_result("Gemini refinement successful", False, str(e))
            all_passed = False
    
    return all_passed


# =============================================================================
# DEVICE TYPE TESTS
# =============================================================================

def test_device_types() -> bool:
    """
    Test that different device types produce appropriate canvas sizes.
    """
    print_header("DEVICE TYPE TESTS")
    
    try:
        from backend.config import DEVICE_CANVAS_SIZES, DEFAULT_DEVICE_TYPE
        from backend.llm.prompts import get_canvas_for_device, get_system_prompt
    except ImportError as e:
        print_result("Import config and prompts", False, str(e))
        return False
    
    print_result("Import config and prompts", True)
    
    all_passed = True
    
    # Test each device type
    for device, expected_canvas in DEVICE_CANVAS_SIZES.items():
        try:
            canvas = get_canvas_for_device(device)
            passed = (
                canvas["width"] == expected_canvas["width"] and
                canvas["height"] == expected_canvas["height"]
            )
            details = f"{canvas['width']}x{canvas['height']}"
            print_result(f"Device '{device}'", passed, details)
            all_passed = all_passed and passed
            
        except Exception as e:
            print_result(f"Device '{device}'", False, str(e))
            all_passed = False
    
    # Test default device
    try:
        default_canvas = get_canvas_for_device(None)
        expected_default = DEVICE_CANVAS_SIZES[DEFAULT_DEVICE_TYPE]
        passed = (
            default_canvas["width"] == expected_default["width"] and
            default_canvas["height"] == expected_default["height"]
        )
        print_result(f"Default device is '{DEFAULT_DEVICE_TYPE}'", passed)
        all_passed = all_passed and passed
        
    except Exception as e:
        print_result("Default device handling", False, str(e))
        all_passed = False
    
    # Test prompt contains device info
    try:
        phone_prompt = get_system_prompt("phone")
        passed = "PHONE" in phone_prompt.upper() and "375" in phone_prompt
        print_result("Prompt includes device info", passed)
        all_passed = all_passed and passed
        
    except Exception as e:
        print_result("Prompt includes device info", False, str(e))
        all_passed = False
    
    return all_passed


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="SynthFrame Comprehensive Test Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_synthframe.py --text          # Test text pipeline only
  python test_synthframe.py --image         # Test image pipeline only
  python test_synthframe.py --devices       # Test device type configurations
  python test_synthframe.py --text --device phone  # Test text with phone device
  python test_synthframe.py --all           # Run all tests
        """
    )
    
    parser.add_argument("--text", action="store_true", help="Test text-to-wireframe pipeline")
    parser.add_argument("--image", action="store_true", help="Test image/CV pipeline")
    parser.add_argument("--devices", action="store_true", help="Test device type configurations")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--device", type=str, default=None, 
                       choices=["laptop", "desktop", "tablet", "tablet_landscape", "phone", "phone_small"],
                       help="Device type to test with")
    
    args = parser.parse_args()
    
    # Default to showing help if no args
    if not any([args.text, args.image, args.devices, args.all]):
        parser.print_help()
        print("\n⚠️  Please specify at least one test: --text, --image, --devices, or --all")
        return 1
    
    # Print environment info
    print_header("ENVIRONMENT")
    mock_mode = os.getenv("MOCK_LLM", "0") == "1"
    has_key = bool(os.getenv("GEMINI_API_KEY"))
    print(f"  Mock Mode: {'ON (no API calls)' if mock_mode else 'OFF (using real API)'}")
    print(f"  API Key: {'Set' if has_key else 'Not set'}")
    print(f"  Device: {args.device or 'laptop (default)'}")
    
    results = []
    
    # Run requested tests
    if args.text or args.all:
        passed = test_text_pipeline(args.device)
        results.append(("Text Pipeline", passed))
    
    if args.image or args.all:
        passed = test_image_pipeline(args.device)
        results.append(("Image Pipeline", passed))
    
    if args.devices or args.all:
        passed = test_device_types()
        results.append(("Device Types", passed))
    
    # Summary
    print_header("SUMMARY")
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {name}")
        all_passed = all_passed and passed
    
    print()
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED - Check output above")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

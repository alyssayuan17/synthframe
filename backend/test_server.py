"""
Test Script for MCP Server
===========================

Tests that the MCP server works correctly even with placeholder Gemini/scraper functions.

Usage:
    source venv/bin/activate
    python test_server.py
"""

import sys
import json
import base64
from pathlib import Path

# Add backend and project root to path
backend_path = Path(__file__).parent
project_root = backend_path.parent
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(project_root))

def test_health_check():
    """Test that server modules can be imported"""
    print("\n[TEST] Health Check")
    print("-" * 40)

    try:
        from config import settings
        print(f"  [OK] Config loaded")
        print(f"       Canvas size: {settings.default_canvas_width}x{settings.default_canvas_height}")

        from models.wireframe import Component, Wireframe, ComponentType
        print(f"  [OK] Wireframe models imported")
        print(f"       Component types available: {len(ComponentType)}")

        from llm.prompts import SYSTEM_PROMPT
        print(f"  [OK] LLM prompts imported")

        print("\n  Result: PASS ✓")
        return True

    except Exception as e:
        print(f"\n  Result: FAIL ✗")
        print(f"  Error: {e}")
        return False


def test_placeholder_functions():
    """Test that placeholder Gemini/scraper functions return valid data"""
    print("\n[TEST] Placeholder Functions")
    print("-" * 40)

    try:
        # Import the placeholder functions
        import importlib.util
        import os
        
        # Proper path resolution relative to this test file
        server_path = Path(__file__).parent / "server.py"
        spec = importlib.util.spec_from_file_location("server", str(server_path))
        server_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(server_module)

        # Test generate_with_gemini
        print("  Testing generate_with_gemini...")
        result = server_module.generate_with_gemini("test prompt")
        assert "id" in result, "Missing wireframe id"
        assert "components" in result, "Missing components"
        assert len(result["components"]) > 0, "No components generated"
        print(f"    [OK] Returns valid wireframe with {len(result['components'])} components")

        # Test refine_with_gemini
        print("  Testing refine_with_gemini...")
        test_components = [
            {"type": "navbar", "position": {"x": 0, "y": 0}, "size": {"width": 100, "height": 50}}
        ]
        result = server_module.refine_with_gemini(test_components)
        assert "components" in result, "Missing components"
        print(f"    [OK] Returns refined wireframe")

        # Test update_with_gemini
        print("  Testing update_with_gemini...")
        test_wireframe = {"id": "test", "components": []}
        result = server_module.update_with_gemini(test_wireframe, "make it bigger")
        assert result is not None, "No result returned"
        print(f"    [OK] Returns updated wireframe")

        # Test scrape_similar_sites
        print("  Testing scrape_similar_sites...")
        result = server_module.scrape_similar_sites("student club")
        assert "patterns" in result, "Missing patterns"
        print(f"    [OK] Returns patterns: {result['patterns']}")

        print("\n  Result: PASS ✓")
        return True

    except Exception as e:
        print(f"\n  Result: FAIL ✗")
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_wireframe_models():
    """Test wireframe data models"""
    print("\n[TEST] Wireframe Models")
    print("-" * 40)

    try:
        from models.wireframe import Component, Wireframe, ComponentType, Position, Size

        # Create a component
        comp = Component(
            type=ComponentType.NAVBAR,
            position=Position(x=0, y=0),
            size=Size(width=1200, height=64),
            props={"logo": "Test"}
        )
        print(f"  [OK] Component created: {comp.type.value}")

        # Create a wireframe
        wireframe = Wireframe(
            name="Test Wireframe",
            components=[comp]
        )
        print(f"  [OK] Wireframe created: {wireframe.name}")

        # Test JSON serialization
        json_data = wireframe.to_json()
        assert json_data["name"] == "Test Wireframe"
        assert len(json_data["components"]) == 1
        print(f"  [OK] JSON serialization works")

        print("\n  Result: PASS ✓")
        return True

    except Exception as e:
        print(f"\n  Result: FAIL ✗")
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cv_pipeline():
    """Test CV pipeline with a simple test image"""
    print("\n[TEST] CV Pipeline")
    print("-" * 40)

    try:
        from vision import analyze_sketch
        import numpy as np
        import cv2

        # Create a simple test image (white background with black rectangle)
        img = np.ones((400, 600, 3), dtype=np.uint8) * 255
        cv2.rectangle(img, (50, 50), (550, 100), (0, 0, 0), 3)  # Top navbar
        cv2.rectangle(img, (50, 120), (550, 300), (0, 0, 0), 3)  # Hero section

        # Convert to base64
        _, buffer = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        img_base64 = f"data:image/png;base64,{img_base64}"

        print("  Testing sketch analysis...")
        result = analyze_sketch(img_base64, return_debug_image=False)

        print(f"    [OK] Detected {len(result.components)} components")
        for comp in result.components:
            print(f"         - {comp.type.value} at ({comp.position.x:.0f}, {comp.position.y:.0f})")

        print("\n  Result: PASS ✓")
        return True

    except Exception as e:
        print(f"\n  Result: FAIL ✗")
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("SYNTHFRAME MCP SERVER TEST SUITE")
    print("=" * 60)

    results = []

    # Run all tests
    results.append(("Health Check", test_health_check()))
    results.append(("Wireframe Models", test_wireframe_models()))
    results.append(("Placeholder Functions", test_placeholder_functions()))
    results.append(("CV Pipeline", test_cv_pipeline()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "PASS ✓" if result else "FAIL ✗"
        print(f"  {test_name:30} {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Your MCP server is ready.")
        print("\nNext steps:")
        print("  1. Add GEMINI_API_KEY to .env")
        print("  2. Implement real Gemini functions")
        print("  3. Run: python server.py")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")

    print("=" * 60)


if __name__ == "__main__":
    main()

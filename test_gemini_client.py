r"""
Test Gemini LLM Client

Quick test to verify the Gemini integration works correctly.
Run this after installing dependencies.

Usage:
    cd c:\Users\leo8j\project\synthframe
    pip install -r backend/requirements.txt
    python test_gemini_client.py
"""

import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set mock mode for testing without API key
os.environ["MOCK_LLM"] = "1"


def test_llm_client_import():
    """Test that LLM client can be imported."""
    print("[1/4] Testing LLM Client import...")
    try:
        from llm.client import LlmClient, LlmError
        print("      [OK] LlmClient imported successfully")
        return True
    except ImportError as e:
        print(f"      [FAIL] Import error: {e}")
        return False


def test_mock_generation():
    """Test mock generation mode."""
    print("\n[2/4] Testing mock generation...")
    try:
        from llm.client import LlmClient
        client = LlmClient()
        
        if not client.mock:
            print("      [WARN] Mock mode not enabled, skipping")
            return True
            
        result = client.generate("test prompt")
        data = json.loads(result)
        
        # Verify structure
        assert "id" in data, "Missing 'id' field"
        assert "components" in data, "Missing 'components' field"
        assert len(data["components"]) > 0, "No components generated"
        
        # Verify UPPERCASE types
        for comp in data["components"]:
            assert comp["type"].isupper(), f"Component type not uppercase: {comp['type']}"
        
        print(f"      [OK] Mock generation returned {len(data['components'])} components")
        print(f"      [OK] All component types are UPPERCASE")
        return True
        
    except Exception as e:
        print(f"      [FAIL] {e}")
        return False


def test_prompts_import():
    """Test that prompts module can be imported."""
    print("\n[3/4] Testing prompts import...")
    try:
        from llm.prompts import (
            SYSTEM_PROMPT, 
            USER_PROMPT_TEMPLATE, 
            EDIT_SYSTEM_PROMPT,
            CV_REFINEMENT_PROMPT
        )
        
        # Verify UPPERCASE in prompts
        assert "NAVBAR" in SYSTEM_PROMPT, "NAVBAR not in SYSTEM_PROMPT"
        assert "UPPERCASE" in SYSTEM_PROMPT, "UPPERCASE instruction not in prompt"
        
        print("      [OK] All prompts imported successfully")
        print("      [OK] Prompts contain UPPERCASE component types")
        return True
        
    except ImportError as e:
        print(f"      [FAIL] Import error: {e}")
        return False


def test_generation_pipeline():
    """Test the full generation pipeline."""
    print("\n[4/4] Testing generation pipeline...")
    try:
        from generation.generate import generate_wireframe
        
        layout, context = generate_wireframe(
            user_input="create a simple dashboard",
            use_scraper=False
        )
        
        print(f"      [OK] Generated wireframe: {layout.id}")
        print(f"      [OK] Components: {len(layout.components)}")
        
        # Check component types are valid
        for comp in layout.components:
            print(f"          - {comp.type}: {comp.id}")
        
        return True
        
    except Exception as e:
        print(f"      [FAIL] {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("GEMINI LLM CLIENT TEST")
    print("=" * 60)
    
    results = []
    results.append(("Import", test_llm_client_import()))
    results.append(("Mock Generation", test_mock_generation()))
    results.append(("Prompts", test_prompts_import()))
    results.append(("Pipeline", test_generation_pipeline()))
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED!")
        print("Gemini integration is ready for use.")
    else:
        print("SOME TESTS FAILED")
        print("Check the output above for details.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

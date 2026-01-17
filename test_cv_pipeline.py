"""
Test CV Pipeline
================

Creates a synthetic sketch image and validates the entire CV pipeline.
Run this to confirm your vision module works correctly.

Usage:
    cd /Users/alyssayuan/synthframe
    python test_cv_pipeline.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import cv2
import numpy as np
import base64
from vision import analyze_sketch


def create_test_sketch(width=800, height=600):
    """
    Create a synthetic hand-drawn sketch with common UI elements.

    Simulates what a user might draw:
    - Top navbar (full width)
    - Hero section (large, center-top)
    - Three cards in a row
    - Footer at bottom
    """
    # Create white canvas
    image = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Draw rectangles with pencil-like thickness (simulate hand-drawn)
    color = (0, 0, 0)  # Black
    thickness = 3

    # 1. NAVBAR - top, full width
    cv2.rectangle(image, (10, 10), (width-10, 60), color, thickness)
    cv2.putText(image, "NAVBAR", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # 2. HERO - large section below navbar
    cv2.rectangle(image, (10, 80), (width-10, 250), color, thickness)
    cv2.putText(image, "HERO", (width//2 - 40, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # 3. CARDS - three in a row
    card_width = (width - 60) // 3
    card_y = 280
    card_height = 150

    for i in range(3):
        x = 20 + i * (card_width + 10)
        cv2.rectangle(image, (x, card_y), (x + card_width - 10, card_y + card_height), color, thickness)
        cv2.putText(image, f"CARD {i+1}", (x + 10, card_y + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # 4. FOOTER - bottom, full width
    cv2.rectangle(image, (10, height-60), (width-10, height-10), color, thickness)
    cv2.putText(image, "FOOTER", (20, height-30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return image


def image_to_base64(image):
    """Convert OpenCV image to base64 string."""
    _, buffer = cv2.imencode('.png', image)
    base64_str = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/png;base64,{base64_str}"


def main():
    print("=" * 60)
    print("CV PIPELINE TEST")
    print("=" * 60)

    # Step 1: Create test sketch
    print("\n[1/4] Creating synthetic sketch...")
    sketch_image = create_test_sketch()
    print(f"      [OK] Created {sketch_image.shape[1]}x{sketch_image.shape[0]} test image")

    # Save test image for inspection
    test_image_path = "/Users/alyssayuan/synthframe/test_sketch.png"
    cv2.imwrite(test_image_path, sketch_image)
    print(f"      [OK] Saved to: {test_image_path}")

    # Step 2: Convert to base64
    print("\n[2/4] Encoding to base64...")
    base64_image = image_to_base64(sketch_image)
    print(f"      [OK] Encoded ({len(base64_image)} chars)")

    # Step 3: Run CV pipeline
    print("\n[3/4] Running CV pipeline...")
    try:
        result = analyze_sketch(base64_image, return_debug_image=True, wireframe_name="Test Wireframe")
        print(f"      [OK] Pipeline completed successfully")
    except Exception as e:
        print(f"      [ERROR] {e}")
        import traceback
        traceback.print_exc()
        return

    # Step 4: Validate results
    print("\n[4/4] Validating results...")
    print(f"\n      Components detected: {len(result.components)}")
    print(f"      Processing notes: {result.processing_notes}")

    print("\n      Component breakdown:")
    for i, comp in enumerate(result.components, 1):
        print(f"        {i}. {comp.type.value:12} @ ({comp.position.x:6.1f}, {comp.position.y:6.1f}) "
              f"size=({comp.size.width:6.1f}x{comp.size.height:6.1f}) "
              f"confidence={comp.confidence:.0%}")

    # Save debug image
    if result.debug_image_base64:
        print("\n[DEBUG] Saving debug visualization...")
        debug_data = result.debug_image_base64.split(',')[1]
        debug_bytes = base64.b64decode(debug_data)
        debug_path = "/Users/alyssayuan/synthframe/test_debug.png"
        with open(debug_path, 'wb') as f:
            f.write(debug_bytes)
        print(f"        [OK] Saved to: {debug_path}")
        print(f"        (Open this to see detected components with labels)")

    # Validate wireframe structure
    print("\n[WIREFRAME] Structure:")
    wireframe_json = result.wireframe.to_json()
    print(f"        ID: {wireframe_json['id']}")
    print(f"        Name: {wireframe_json['name']}")
    print(f"        Layout: {wireframe_json['layout']}")
    print(f"        Canvas: {wireframe_json['canvas_size']}")
    print(f"        Components: {len(wireframe_json['components'])} items")

    # Expected components (roughly)
    print("\n[VALIDATION] Expected vs Actual:")
    expected_types = ["NAVBAR", "HERO", "CARD", "CARD", "CARD", "FOOTER"]
    actual_types = [c.type.value for c in result.components]

    print(f"        Expected: {expected_types}")
    print(f"        Actual:   {actual_types}")

    # Check if major components detected
    has_navbar = any(c.type.value == "NAVBAR" for c in result.components)
    has_hero = any(c.type.value == "HERO" for c in result.components)
    has_footer = any(c.type.value == "FOOTER" for c in result.components)
    card_count = sum(1 for c in result.components if c.type.value == "CARD")

    print("\n[RESULTS]")
    print(f"        NAVBAR detected:  {'YES' if has_navbar else 'NO'}")
    print(f"        HERO detected:    {'YES' if has_hero else 'NO'}")
    print(f"        FOOTER detected:  {'YES' if has_footer else 'NO'}")
    print(f"        CARDs detected:   {card_count} (expected ~3)")

    # Overall status
    if has_navbar and has_hero and has_footer and card_count >= 2:
        print("\n" + "=" * 60)
        print("CV PIPELINE WORKING CORRECTLY!")
        print("=" * 60)
        print("\nYour pipeline successfully:")
        print("  1. Decoded base64 image")
        print("  2. Preprocessed (grayscale, blur, threshold, morphology)")
        print("  3. Detected contours")
        print("  4. Mapped shapes to component types")
        print("  5. Generated Wireframe JSON")
        print("\nReady for integration with Athena AI + React frontend!")
    else:
        print("\n" + "=" * 60)
        print("PIPELINE WORKS BUT DETECTION MAY NEED TUNING")
        print("=" * 60)
        print("\nThe pipeline runs, but component detection could be improved.")
        print("Check the debug image and adjust thresholds in config.py")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

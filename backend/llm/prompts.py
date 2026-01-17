"""
LLM Prompts for Wireframe Generation

These prompts instruct Gemini to generate WireframeLayout JSON with pixel-based positioning
that matches the same schema used by the CV pipeline.

IMPORTANT: Component types use UPPERCASE to match the ComponentType enum in models/wireframe.py
"""

from backend.config import DEVICE_CANVAS_SIZES, DEFAULT_DEVICE_TYPE


def get_canvas_for_device(device_type: str = None) -> dict:
    """Get canvas dimensions for a device type."""
    device = device_type or DEFAULT_DEVICE_TYPE
    return DEVICE_CANVAS_SIZES.get(device, DEVICE_CANVAS_SIZES[DEFAULT_DEVICE_TYPE])


def get_system_prompt(device_type: str = None) -> str:
    """Generate system prompt with device-specific canvas size."""
    canvas = get_canvas_for_device(device_type)
    device = device_type or DEFAULT_DEVICE_TYPE
    
    # Device-specific layout hints
    layout_hints = {
        "laptop": "Use horizontal layouts, sidebars are common, multi-column grids work well.",
        "desktop": "Large canvas allows for complex layouts with multiple sections side by side.",
        "tablet": "Portrait orientation - stack elements vertically, avoid wide sidebars.",
        "tablet_landscape": "Landscape tablet - horizontal layouts work, but keep touch targets large.",
        "phone": "Mobile-first design - single column, large touch targets, bottom navigation is common.",
        "phone_small": "Compact mobile - prioritize essential content, minimize text, large buttons.",
    }
    
    hint = layout_hints.get(device, layout_hints["laptop"])
    
    return f"""You are a UI/UX wireframe generator.
Given a user's request and optional web research context, output ONLY a JSON object representing a wireframe layout.

TARGET DEVICE: {device.upper()}
CANVAS SIZE: {canvas['width']}x{canvas['height']} pixels
DESIGN HINTS: {hint}

OUTPUT FORMAT:
{{
  "id": "layout-<unique>",
  "name": "<descriptive name>",
  "canvas_size": {{"width": {canvas['width']}, "height": {canvas['height']}}},
  "background_color": "#ffffff",
  "source_type": "prompt",
  "device_type": "{device}",
  "components": [
    {{
      "id": "<unique id>",
      "type": "<COMPONENT_TYPE>",
      "position": {{"x": <pixels from left>, "y": <pixels from top>}},
      "size": {{"width": <pixels>, "height": <pixels>}},
      "props": {{<component-specific properties>}},
      "children": [],
      "source": "llm"
    }}
  ]
}}

COMPONENT TYPES (use UPPERCASE string values):
- NAVBAR: {{logo: string, links: string[], cta: string}}
- SIDEBAR: {{items: string[]}}
- FOOTER: {{copyright: string, links: string[]}}
- HEADING: {{text: string, level: 1-6}}
- TEXT: {{text: string}}
- CARD: {{title: string, content: string}}
- BUTTON: {{label: string, variant: "primary"|"secondary"}}
- FORM: {{fields: [{{label, type, placeholder}}]}}
- INPUT: {{placeholder: string, type: string}}
- TABLE: {{columns: string[], rows: number}}
- CHART: {{type: "bar"|"line"|"pie", title: string}}
- IMAGE: {{alt: string, src: string}}
- HERO: {{headline: string, subheadline: string, cta: string}}
- SECTION: {{title: string, content: string}}
- CALENDAR: {{view: "month"|"week"}}
- BOTTOM_NAV: {{items: string[]}}  # For mobile designs

DEVICE-SPECIFIC GUIDELINES:
- For PHONE/mobile: Use single column layouts, avoid sidebars, use bottom navigation
- For TABLET: Can use 2 columns, touch-friendly buttons (min 44px height)
- For LAPTOP/DESKTOP: Full layouts with sidebars, multi-column grids, hover states

RULES:
- ONLY output valid JSON. No markdown. No explanation.
- Every component must have a unique id (e.g., "nav-1", "card-1").
- Use realistic pixel positions and sizes for the target device.
- props should be minimal and realistic.
- source should always be "llm".
- type MUST be UPPERCASE (e.g., "NAVBAR", not "navbar").
- Ensure components fit within the canvas dimensions.
"""


SYSTEM_PROMPT = get_system_prompt()  # Default laptop prompt for backwards compatibility


USER_PROMPT_TEMPLATE = """Web research context (may be empty):
{webscraper_context}

User request:
{user_input}

Generate the wireframe JSON now:
"""


def get_edit_system_prompt(device_type: str = None) -> str:
    """Generate edit prompt with device-specific context."""
    canvas = get_canvas_for_device(device_type)
    device = device_type or DEFAULT_DEVICE_TYPE
    
    return f"""You are a UI/UX wireframe editor.
You will be given an existing wireframe JSON and an instruction.
Return ONLY the full updated wireframe JSON.

TARGET DEVICE: {device.upper()}
CANVAS SIZE: {canvas['width']}x{canvas['height']} pixels

RULES:
- ONLY output valid JSON. No markdown. No explanation.
- Keep unrelated parts unchanged unless required by the instruction.
- Preserve existing ids whenever possible.
- Use the same format as the input (pixel-based positioning).
- Maintain realistic pixel values for the target device.
- Component types MUST be UPPERCASE (e.g., "NAVBAR", "CARD", "HERO").
- source should remain "llm" for components you modify or add.
- Ensure all components fit within the canvas: {canvas['width']}x{canvas['height']}.
"""


EDIT_SYSTEM_PROMPT = get_edit_system_prompt()  # Default for backwards compatibility


EDIT_USER_TEMPLATE = """Web research context (may be empty):
{webscraper_context}

Existing wireframe JSON:
{wireframe_json}

Instruction:
{instruction}

Return the updated wireframe JSON now:
"""


# Prompt for refining CV-detected components with Gemini
def get_cv_refinement_prompt(device_type: str = None) -> str:
    """Generate CV refinement prompt with device context."""
    canvas = get_canvas_for_device(device_type)
    device = device_type or DEFAULT_DEVICE_TYPE
    
    return f"""You are a UI component classifier and layout optimizer.
You will be given a list of shapes detected from a hand-drawn sketch with their positions and sizes.
Your job is to:
1. Classify each shape into the correct UI component type
2. Add appropriate default props for each component type
3. Optimize positions and sizes for the target device
4. Add any missing common components (like Footer if not detected)
5. Return the refined component list as JSON

TARGET DEVICE: {device.upper()}
CANVAS SIZE: {canvas['width']}x{canvas['height']} pixels

COMPONENT TYPES (UPPERCASE):
- NAVBAR: Navigation bar (logo, links) - typically at top
- SIDEBAR: Vertical navigation menu - left side on laptop/desktop, avoid on mobile
- HERO: Large banner section - below navbar
- CARD: Content card - use in grids
- BUTTON: Clickable button - ensure touch-friendly size on mobile (min 44px)
- FORM: Input form - stack fields vertically on mobile
- TABLE: Data table - may need horizontal scroll on mobile
- FOOTER: Bottom section - always include
- HEADING: Title/heading text
- TEXT: Paragraph text
- IMAGE: Image placeholder
- CHART: Chart/graph
- SECTION: Generic content section
- BOTTOM_NAV: Mobile bottom navigation - use instead of sidebar on phone

DETECTED SHAPES:
{{detected_shapes}}

Return a JSON object with:
{{{{
  "components": [
    {{{{
      "id": "comp_xxx",
      "type": "COMPONENT_TYPE",
      "position": {{{{"x": number, "y": number}}}},
      "size": {{{{"width": number, "height": number}}}},
      "props": {{{{...}}}},
      "source": "cv",
      "confidence": 0.0-1.0
    }}}}
  ],
  "suggested_additions": ["FOOTER", ...],  // Components you think are missing
  "layout_notes": "Brief description of detected layout pattern"
}}}}
"""


CV_REFINEMENT_PROMPT = get_cv_refinement_prompt()  # Default for backwards compatibility

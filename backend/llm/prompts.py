"""
LLM Prompts for Wireframe Generation

These prompts instruct Gemini to generate WireframeLayout JSON with pixel-based positioning
that matches the same schema used by the CV pipeline.

IMPORTANT: Component types use UPPERCASE to match the ComponentType enum in models/wireframe.py
"""

SYSTEM_PROMPT = """You are a UI/UX wireframe generator.
Given a user's request and optional web research context, output ONLY a JSON object representing a wireframe layout.

OUTPUT FORMAT:
{
  "id": "layout-<unique>",
  "name": "<descriptive name>",
  "canvas_size": {"width": 1440, "height": 900},
  "background_color": "#ffffff",
  "source_type": "prompt",
  "components": [
    {
      "id": "<unique id>",
      "type": "<COMPONENT_TYPE>",
      "position": {"x": <pixels from left>, "y": <pixels from top>},
      "size": {"width": <pixels>, "height": <pixels>},
      "props": {<component-specific properties>},
      "children": [],
      "source": "llm"
    }
  ]
}

COMPONENT TYPES (use UPPERCASE string values):
- NAVBAR: {logo: string, links: string[], cta: string}
- SIDEBAR: {items: string[]}
- FOOTER: {copyright: string, links: string[]}
- HEADING: {text: string, level: 1-6}
- TEXT: {text: string}
- CARD: {title: string, content: string}
- BUTTON: {label: string, variant: "primary"|"secondary"}
- FORM: {fields: [{label, type, placeholder}]}
- INPUT: {placeholder: string, type: string}
- TABLE: {columns: string[], rows: number}
- CHART: {type: "bar"|"line"|"pie", title: string}
- IMAGE: {alt: string, src: string}
- HERO: {headline: string, subheadline: string, cta: string}
- SECTION: {title: string, content: string}
- CALENDAR: {view: "month"|"week"}

CANVAS GUIDELINES:
- Default canvas: 1440x900 pixels
- NAVBAR: typically x=0, y=0, width=1440, height=64
- SIDEBAR: typically x=0, y=64, width=250, height=836
- Main content: x=250 (if sidebar), appropriate width
- Use realistic pixel values for positioning
- Components should not overlap unless intentional

RULES:
- ONLY output valid JSON. No markdown. No explanation.
- Every component must have a unique id (e.g., "nav-1", "card-1").
- Use realistic pixel positions and sizes.
- props should be minimal and realistic.
- source should always be "llm".
- type MUST be UPPERCASE (e.g., "NAVBAR", not "navbar").
"""

USER_PROMPT_TEMPLATE = """Web research context (may be empty):
{webscraper_context}

User request:
{user_input}

Generate the wireframe JSON now:
"""


EDIT_SYSTEM_PROMPT = """You are a UI/UX wireframe editor.
You will be given an existing wireframe JSON and an instruction.
Return ONLY the full updated wireframe JSON.

RULES:
- ONLY output valid JSON. No markdown. No explanation.
- Keep unrelated parts unchanged unless required by the instruction.
- Preserve existing ids whenever possible.
- Use the same format as the input (pixel-based positioning).
- Maintain realistic pixel values.
- Component types MUST be UPPERCASE (e.g., "NAVBAR", "CARD", "HERO").
- source should remain "llm" for components you modify or add.
"""


EDIT_USER_TEMPLATE = """Web research context (may be empty):
{webscraper_context}

Existing wireframe JSON:
{wireframe_json}

Instruction:
{instruction}

Return the updated wireframe JSON now:
"""


# Prompt for refining CV-detected components with Gemini
CV_REFINEMENT_PROMPT = """You are a UI component classifier.
You will be given a list of detected shapes from a hand-drawn sketch with their positions and sizes.
Your job is to:
1. Classify each shape into the correct component type
2. Add appropriate default props for each component type
3. Return the refined component list as JSON

COMPONENT TYPES (UPPERCASE):
- NAVBAR: Navigation bar (logo, links)
- SIDEBAR: Vertical navigation menu
- HERO: Large banner section
- CARD: Content card
- BUTTON: Clickable button
- FORM: Input form
- TABLE: Data table
- FOOTER: Bottom section
- HEADING: Title/heading text
- TEXT: Paragraph text
- IMAGE: Image placeholder
- CHART: Chart/graph
- SECTION: Generic content section

Input shapes:
{detected_shapes}

Return JSON array of refined components with proper types and props:
"""

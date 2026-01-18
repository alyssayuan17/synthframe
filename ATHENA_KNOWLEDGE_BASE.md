# SynthFrame Wireframe Knowledge Base

## Wireframe JSON Format

All wireframes use this structure:

```json
{
  "id": "layout-unique-id",
  "name": "Descriptive Name",
  "canvas_size": {"width": 1440, "height": 900},
  "background_color": "#ffffff",
  "source_type": "prompt",
  "components": [...]
}
```

## Component Types (UPPERCASE)

| Type | Props | Description |
|------|-------|-------------|
| NAVBAR | `{logo: string, links: string[], cta: string}` | Top navigation bar |
| SIDEBAR | `{items: string[]}` | Vertical side menu |
| FOOTER | `{copyright: string, links: string[]}` | Bottom section |
| HEADING | `{text: string, level: 1-6}` | Title text |
| TEXT | `{text: string}` | Paragraph text |
| CARD | `{title: string, content: string}` | Content card |
| BUTTON | `{label: string, variant: "primary"\|"secondary"}` | Clickable button |
| FORM | `{fields: [{label, type, placeholder}]}` | Input form |
| INPUT | `{placeholder: string, type: string}` | Single input field |
| TABLE | `{columns: string[], rows: number}` | Data table |
| CHART | `{type: "bar"\|"line"\|"pie", title: string}` | Chart/graph |
| IMAGE | `{alt: string, src: string}` | Image placeholder |
| HERO | `{headline: string, subheadline: string, cta: string}` | Large banner section |
| SECTION | `{title: string, content: string}` | Generic section |
| CALENDAR | `{view: "month"\|"week"}` | Calendar widget |
| BOTTOM_NAV | `{items: string[]}` | Mobile bottom navigation |

## Component Structure

Each component has:
```json
{
  "id": "unique-id",
  "type": "NAVBAR",
  "position": {"x": 0, "y": 0},
  "size": {"width": 1440, "height": 64},
  "props": {...},
  "children": [],
  "source": "llm"
}
```

## Canvas Sizes by Device

| Device | Width | Height |
|--------|-------|--------|
| laptop | 1440 | 900 |
| desktop | 1920 | 1080 |
| tablet | 768 | 1024 |
| tablet_landscape | 1024 | 768 |
| phone | 390 | 844 |
| phone_small | 320 | 568 |

## Layout Patterns

**Landing Page**: NAVBAR → HERO → SECTION/CARD grid → FOOTER
**Dashboard**: NAVBAR + SIDEBAR → HEADING → CARD stats → TABLE/CHART → FOOTER
**Mobile App**: NAVBAR → content sections → BOTTOM_NAV
**Login/Signup**: Centered FORM with HEADING
**Profile Page**: NAVBAR → IMAGE (avatar) → HEADING → SECTION → FOOTER

## Rules

1. Component types are UPPERCASE ("NAVBAR" not "navbar")
2. All positions/sizes are in pixels
3. Components must fit within canvas dimensions
4. Every component needs a unique id (e.g., "nav-1", "card-1")
5. source is "llm" for AI-generated, "cv" for sketch-detected

## MCP Tools Available

1. **analyze_sketch**: Upload hand-drawn sketch → returns wireframe JSON
2. **generate_wireframe**: Text description → returns wireframe JSON
3. **update_component**: Instruction + wireframe_id → returns modified wireframe JSON

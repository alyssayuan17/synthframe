# SynthFrame Wireframe Knowledge Base

This document defines the component specification for Athena AI to generate wireframes.

## Wireframe JSON Format

All wireframes use this structure:

```json
{
  "id": "layout-unique-id",
  "name": "Descriptive Name",
  "canvas_size": {"width": 1440, "height": 900},
  "background_color": "#ffffff",
  "source_type": "prompt",
  "device_type": "macbook",
  "components": [...]
}
```

## Component Types (17 types - UPPERCASE)

### Navigation Components

| Type | Props | Description |
|------|-------|-------------|
| NAVBAR | `{logo: string, links: string[], cta: string}` | Top navigation bar |
| SIDEBAR | `{items: string[]}` | Vertical side menu (desktop) |
| FOOTER | `{copyright: string, links: string[]}` | Bottom section |
| BOTTOM_NAV | `{items: string[]}` | Mobile bottom navigation |

### Content Section Components

| Type | Props | Description |
|------|-------|-------------|
| HERO | `{headline: string, subheadline: string, cta: string}` | Large banner section |
| SECTION | `{title: string, content: string}` | Generic content section |
| CARD | `{title: string, content: string}` | Content card |

### Interactive Components

| Type | Props | Description |
|------|-------|-------------|
| FORM | `{fields: [{label, type, placeholder}], submit: string}` | Input form |
| BUTTON | `{label: string, variant: "primary"\|"secondary"}` | Clickable button |
| INPUT | `{placeholder: string, type: string}` | Single input field |

### Text Components

| Type | Props | Description |
|------|-------|-------------|
| TEXT | `{content: string}` | Paragraph text |
| HEADING | `{text: string, level: 1-6}` | Title/heading text |

### Media & Data Components

| Type | Props | Description |
|------|-------|-------------|
| IMAGE | `{alt: string, src: string}` | Image placeholder |
| TABLE | `{columns: string[], rows: number}` | Data table |
| CALENDAR | `{view: "month"\|"week"}` | Calendar widget |
| CHART | `{type: "bar"\|"line"\|"pie", title: string}` | Chart/graph |

### Frame Components

| Type | Props | Description |
|------|-------|-------------|
| FRAME | `{device: string, width: number, height: number}` | Device container |

## Component Structure

Each component has this structure:

```json
{
  "id": "nav-1",
  "type": "NAVBAR",
  "position": {"x": 0, "y": 0},
  "size": {"width": 1440, "height": 64},
  "props": {"logo": "AppName", "links": ["Home", "About"], "cta": "Sign Up"},
  "children": [],
  "source": "llm"
}
```

## Canvas Sizes by Device

| Device | Width | Height |
|--------|-------|--------|
| macbook | 1440 | 900 |
| desktop | 1920 | 1080 |
| tablet | 768 | 1024 |
| tablet_landscape | 1024 | 768 |
| iphone | 393 | 852 |
| phone_small | 320 | 568 |

## Layout Patterns

**Landing Page**: NAVBAR -> HERO -> SECTION/CARD grid -> FOOTER

**Dashboard**: NAVBAR + SIDEBAR -> HEADING -> CARD stats -> TABLE/CHART -> FOOTER

**Mobile App**: NAVBAR -> content sections -> BOTTOM_NAV

**Login/Signup**: Centered FORM with HEADING

**Profile Page**: NAVBAR -> IMAGE (avatar) -> HEADING -> SECTION -> FOOTER

## Rules

1. Component types are UPPERCASE ("NAVBAR" not "navbar" or "navigation-bar")
2. All positions/sizes are in pixels (integers, not floats)
3. Components must fit within canvas dimensions
4. Every component needs a unique id (e.g., "nav-1", "card-1", "hero-main")
5. source is "llm" for AI-generated, "cv" for sketch-detected
6. children array is empty [] for now
7. For mobile (iphone): Use BOTTOM_NAV instead of SIDEBAR, single column layout
8. For desktop (macbook): SIDEBAR is common, multi-column layouts work

## MCP Tools Available

1. **analyze_sketch**: Upload hand-drawn sketch -> returns wireframe JSON
   - Input: `{image_base64: string, prompt?: string}`
   - Output: `{wireframe_id: string, components: [], component_count: number}`

2. **generate_wireframe**: Text description -> returns wireframe JSON
   - Input: `{prompt: string, device_type?: string}`
   - Output: `{wireframe_id: string, components: [], component_count: number}`

3. **update_component**: Instruction + wireframe_id -> returns modified wireframe JSON
   - Input: `{wireframe_id: string, instruction: string}`
   - Output: `{wireframe_id: string, components: [], component_count: number}`

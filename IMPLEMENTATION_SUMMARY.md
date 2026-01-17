# Athena AI Integration - Implementation Summary

### 1. MCP Server (`backend/server.py`)

Complete MCP server with 3 tools for Athena AI:

- **analyze_sketch** - Takes base64 image, runs CV pipeline, refines with Gemini
- **generate_wireframe** - Takes text prompt, optionally scrapes sites, generates with Gemini
- **update_component** - Takes instruction, updates existing wireframe with Gemini

**Status**: Structure complete, has placeholders for Gemini/scraper (marked with TODO)

### 2. Widgets (`widgets/`)

Two React components for Athena chat:

- **UploadWidget.jsx** - Beautiful file upload interface for sketches
- **StatusWidget.jsx** - Shows processing status and results

**Status**: Complete and ready to use

### 3. Documentation

- **ATHENA_SETUP.md** - Complete setup guide for connecting to Athena
- **.env.example** - Environment configuration template

**Status**: Complete

### 4. REST API

Backend also includes REST endpoints for your frontend:

- `GET /api/wireframes/{id}` - Fetch wireframe
- `POST /api/wireframes/{id}` - Save wireframe
- `GET /health` - Health check

---

## What You Need to Do Next

### PRIORITY 1: Implement Gemini Functions (Your Task)

In `backend/server.py`, replace these 3 placeholder functions:

#### 1. `generate_with_gemini(prompt, context)`
```python
def generate_with_gemini(prompt: str, context: str = "") -> dict:
    # TODO: Implement Gemini generation
    # Should:
    # 1. Build prompt with user request + scraper context
    # 2. Call Gemini API
    # 3. Parse JSON response
    # 4. Return wireframe JSON
    pass
```

#### 2. `refine_with_gemini(detected_components, prompt)`
```python
def refine_with_gemini(detected_components: list, prompt: str = "") -> dict:
    # TODO: Implement Gemini refinement
    # Should:
    # 1. Take CV-detected components
    # 2. Ask Gemini to improve them (better types, add props, fix layout)
    # 3. Return refined wireframe JSON
    pass
```

#### 3. `update_with_gemini(current_wireframe, instruction)`
```python
def update_with_gemini(current_wireframe: dict, instruction: str) -> dict:
    # TODO: Implement Gemini update
    # Should:
    # 1. Take existing wireframe + instruction
    # 2. Gemini figures out what to change
    # 3. Return updated wireframe JSON
    pass
```

**Hint**: You already have prompt templates in `backend/llm/prompts.py`

### PRIORITY 2: Implement Web Scraper (Your Task)

In `backend/server.py`, replace this function:

```python
def scrape_similar_sites(query: str) -> dict:
    # TODO: Implement web scraper
    # Should:
    # 1. Extract keywords from query
    # 2. Find similar websites
    # 3. Scrape their structure
    # 4. Return common UI patterns
    pass
```

### PRIORITY 3: Test Locally

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create `.env` file (copy from `.env.example`)

3. Run server:
```bash
python server.py
```

4. Test health endpoint:
```bash
curl http://localhost:8000/health
```

### PRIORITY 4: Connect to Athena AI

Follow `ATHENA_SETUP.md` step-by-step to:
1. Create agent on create-bot.com
2. Register MCP tools
3. Upload widgets
4. Configure agent behavior

---

## How It Works (For Your Understanding)

### User Flow:

```
1. User opens your webapp
2. Clicks chat button
3. Athena chat panel slides out
4. User uploads sketch OR types description
5. Athena calls your MCP server
6. MCP server:
   - Runs CV pipeline (already done)
   - Calls Gemini (you implement this)
   - Returns JSON
7. Canvas updates with components
8. User can edit manually OR chat more with Athena
```

### Architecture:

```
Webapp (Next.js)
  |
  +-- Canvas ---------> Displays components
  |
  +-- Athena Chat ----> Embedded chat panel
       |
       +-- UploadWidget
       +-- StatusWidget
       |
       v
  Athena AI Platform
       |
       v
  Your MCP Server (server.py)
       |
       +-- analyze_sketch
       |    |
       |    +-- CV Pipeline (DONE)
       |    +-- Gemini Refine (TODO)
       |
       +-- generate_wireframe
       |    |
       |    +-- Web Scraper (TODO)
       |    +-- Gemini Generate (TODO)
       |
       +-- update_component
            |
            +-- Gemini Update (TODO)
```

---

## Files Created/Modified

**Created:**
- `backend/server.py` - MCP server with 3 tools
- `widgets/UploadWidget.jsx` - Upload widget for Athena
- `widgets/StatusWidget.jsx` - Status widget for Athena
- `ATHENA_SETUP.md` - Setup documentation
- `backend/.env.example` - Environment template
- `IMPLEMENTATION_SUMMARY.md` - This file

**Already Exists (Don't Touch):**
- `backend/vision/` - CV pipeline (complete)
- `backend/models/wireframe.py` - Data models (complete)
- `backend/config.py` - Configuration (complete)
- `backend/llm/prompts.py` - Prompt templates (use these)

---

## Judging Criteria - How You Score

### Utility & Adoption (20%)
- **Your edge**: Students can wireframe 10x faster
- **Demo**: Show creating club page, marketplace, dashboard

### Creativity (20%)
- **Your edge**: Only tool combining sketch + AI + drag-drop
- **Demo**: Upload hand-drawn sketch, watch it become digital

### User Experience (20%)
- **Your edge**: Seamless chat integration, instant updates
- **Demo**: Chat with AI while canvas updates in real-time

### Design (20%)
- **Your edge**: Polished widgets, professional interface
- **Demo**: Show beautiful upload/status widgets

### Technical Depth (20%)
- **Your edge**: Complex CV pipeline + MCP + Gemini
- **Demo**: Explain the 3-tool architecture

---

## Quick Start (Minimal Working Version)

Want to get something working ASAP for testing?

1. For now, keep the placeholder functions (they return basic wireframes)
2. Focus on connecting to Athena first
3. Test that chat → MCP → canvas flow works
4. Then implement Gemini properly

---

## Need Help?

Check these in order:
1. Server logs: `python server.py` output
2. Health endpoint: http://localhost:8000/health
3. ATHENA_SETUP.md for connection issues
4. MCP server source code comments

---

## Summary

**Done:**
- MCP server structure
- 3 tools (with placeholders)
- 2 widgets
- REST API
- Documentation

**Your Tasks:**
1. Implement 3 Gemini functions
2. Implement web scraper
3. Test locally
4. Connect to Athena
5. Test end-to-end
6. Polish for demo

**Time Estimate:**
- Gemini implementation: 1-2 hours
- Scraper implementation: 1 hour
- Athena connection: 30 minutes
- Testing: 1 hour
- **Total: 3-4 hours to working demo**

Good luck with your hackathon!

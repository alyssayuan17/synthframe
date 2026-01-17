# SynthFrame Project - Current Status

## WORKING

### Dependencies
- All Python packages installed in `backend/venv/`
- OpenCV, FastAPI, MCP SDK, Pydantic, Google Generative AI - all ready

### Core Modules
- [OK] Wireframe models (`models/wireframe.py`)
- [OK] Configuration (`config.py`)
- [OK] LLM prompts (`llm/prompts.py`)
- [OK] CV pipeline structure (`vision/`)

### MCP Server
- [OK] Server structure (`server.py`)
- [OK] 3 MCP tools defined:
  1. `analyze_sketch` - CV + Gemini refinement
  2. `generate_wireframe` - Text → wireframe
  3. `update_component` - Modify existing wireframe
- [OK] REST API endpoints for frontend

### Widgets
- [OK] UploadWidget.jsx - File upload for sketches
- [OK] StatusWidget.jsx - Processing status display

---

## NEXT STEPS (Your Tasks)

### 1. Create .env File (2 minutes)
```bash
cd /Users/alyssayuan/synthframe/backend
cp .env.example .env
```

Then edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_key_here
```

Get key from: https://aistudio.google.com/app/apikey

### 2. Implement 3 Gemini Functions (1-2 hours)

Open `backend/server.py` and implement these functions:

**Line 40**: `generate_with_gemini(prompt, context)`
- Takes user prompt + optional scraper context
- Calls Gemini API
- Returns wireframe JSON

**Line 68**: `refine_with_gemini(detected_components, prompt)`
- Takes CV-detected components
- Asks Gemini to improve them
- Returns refined wireframe JSON

**Line 86**: `update_with_gemini(current_wireframe, instruction)`
- Takes existing wireframe + instruction
- Gemini figures out what to change
- Returns updated wireframe JSON

Use the prompts in `backend/llm/prompts.py` for reference.

### 3. Implement Web Scraper (1 hour)

**Line 99**: `scrape_similar_sites(query)`
- Extract keywords from query
- Find similar websites
- Return common UI patterns

For hackathon speed: You can hardcode patterns based on keywords.

### 4. Test Server (15 minutes)

```bash
cd backend
./venv/bin/python server.py
```

Should see:
```
SynthFrame MCP Server for Athena AI
MCP Tools available:
  1. analyze_sketch
  2. generate_wireframe
  3. update_component
REST API running on http://localhost:8000
```

Test health check:
```bash
curl http://localhost:8000/health
```

### 5. Connect to Athena AI (30 minutes)

Follow `ATHENA_SETUP.md`:
1. Go to https://create-bot.com
2. Create agent "SynthFrame"
3. Register MCP tools
4. Upload widgets
5. Test end-to-end

---

## How to Use Virtual Environment

Always activate venv first:

```bash
cd /Users/alyssayuan/synthframe/backend
source venv/bin/activate  # Activates virtual environment
python server.py          # Run server
deactivate               # When done
```

---

## Files You Need to Edit

1. `backend/.env` - Add GEMINI_API_KEY
2. `backend/server.py` - Implement 3 Gemini functions + scraper

**Don't edit:**
- `backend/vision/` - CV pipeline (complete)
- `backend/models/wireframe.py` - Models (complete)
- `widgets/` - Widgets (complete)

---

## Quick Commands

```bash
# Activate environment
cd /Users/alyssayuan/synthframe/backend
source venv/bin/activate

# Run server
python server.py

# Test health
curl http://localhost:8000/health

# Deactivate when done
deactivate
```

---

## Summary

**Status**: 80% Complete

**Ready:**
- Dependencies
- CV pipeline
- MCP server structure
- Widgets
- Documentation

**TODO:**
- Add GEMINI_API_KEY to .env
- Implement 3 Gemini functions
- Implement web scraper
- Connect to Athena AI

**Time to working demo:** 2-3 hours

You're ready to start implementing the Gemini functions!

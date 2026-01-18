# MongoDB Integration - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           USER BROWSER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │              FRONTEND (Widget/Canvas)                         │       │
│  │                                                                │       │
│  │  1. User types: "Create a dashboard"                          │       │
│  │  2. User uploads sketch image                                 │       │
│  │  3. User edits wireframe                                      │       │
│  │  4. User clicks "Save" button                                 │       │
│  │                                                                │       │
│  │  📦 localStorage: {currentProjectId: "abc-123"}              │       │
│  │  🔗 URL: ?project=abc-123                                    │       │
│  └───────────────────┬──────────────────────────────────────────┘       │
│                       │                                                   │
└───────────────────────┼───────────────────────────────────────────────────┘
                        │ HTTP Requests
                        │
┌───────────────────────▼───────────────────────────────────────────────────┐
│                     SYNTHFRAME BACKEND                                     │
│                     FastAPI (Port 8000)                                    │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │                    ROUTES (API Endpoints)                         │    │
│  │                                                                    │    │
│  │  POST /generate                                                   │    │
│  │  ├─> generate_wireframe()                                        │    │
│  │  ├─> ✅ create_project() → MongoDB                              │    │
│  │  └─> Return {project_id, wireframe_layout}                      │    │
│  │                                                                    │    │
│  │  POST /vision/analyze                                             │    │
│  │  ├─> analyze_sketch()                                            │    │
│  │  ├─> ✅ create_project() → MongoDB                              │    │
│  │  └─> Return {project_id, wireframe}                             │    │
│  │                                                                    │    │
│  │  POST /edit                                                       │    │
│  │  ├─> edit_wireframe()                                            │    │
│  │  ├─> ✅ update_project() → MongoDB                              │    │
│  │  └─> Return {project_id, wireframe_layout}                      │    │
│  │                                                                    │    │
│  │  GET /projects                                                    │    │
│  │  └─> ✅ list_projects() ← MongoDB                               │    │
│  │                                                                    │    │
│  │  GET /projects/{id}                                               │    │
│  │  └─> ✅ get_project() ← MongoDB                                 │    │
│  │                                                                    │    │
│  │  POST /projects/{id}/save                                         │    │
│  │  └─> ✅ update_project() → MongoDB                              │    │
│  │                                                                    │    │
│  │  PATCH /projects/{id}/rename                                      │    │
│  │  └─> ✅ rename_project() → MongoDB                              │    │
│  │                                                                    │    │
│  │  DELETE /projects/{id}                                            │    │
│  │  └─> ✅ delete_project() → MongoDB                              │    │
│  └────────────────────────┬───────────────────────────────────────────┘    │
│                            │                                                │
│  ┌─────────────────────────▼──────────────────────────────────────┐       │
│  │              DATABASE OPERATIONS (CRUD)                          │       │
│  │                                                                   │       │
│  │  • create_project(wireframe) → Project                          │       │
│  │  • get_project(id) → Project                                    │       │
│  │  • list_projects() → [ProjectSummary]                           │       │
│  │  • update_project(id, data) → Project                           │       │
│  │  • rename_project(id, name) → Project                           │       │
│  │  • delete_project(id) → bool                                    │       │
│  │  • count_projects() → int                                       │       │
│  └────────────────────────┬───────────────────────────────────────┘       │
│                            │                                                │
│  ┌─────────────────────────▼──────────────────────────────────────┐       │
│  │            DATABASE CONNECTION (Motor)                           │       │
│  │                                                                   │       │
│  │  • get_mongo_client() → AsyncIOMotorClient                      │       │
│  │  • get_projects_collection() → Collection                       │       │
│  │  • ping_database() → bool                                       │       │
│  │  • close_mongo_connection()                                     │       │
│  └────────────────────────┬───────────────────────────────────────┘       │
│                            │                                                │
└────────────────────────────┼────────────────────────────────────────────────┘
                             │ MongoDB Wire Protocol
                             │
┌────────────────────────────▼────────────────────────────────────────────────┐
│                         MONGODB DATABASE                                     │
│                  (Atlas Cloud or Local)                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Database: synthframe                                                        │
│  └─> Collection: projects                                                    │
│       └─> Document:                                                          │
│           {                                                                  │
│             "_id": "abc-123-def-456",                                       │
│             "name": "Student Club Dashboard",                               │
│             "wireframe": {                                                  │
│               "canvas_size": {"width": 1440, "height": 900},               │
│               "components": [                                               │
│                 {"type": "NAVBAR", "position": {...}, ...},                │
│                 {"type": "HERO", "position": {...}, ...},                  │
│                 {"type": "CARD", "position": {...}, ...}                   │
│               ]                                                              │
│             },                                                               │
│             "generation_method": "text_prompt",                             │
│             "device_type": "laptop",                                        │
│             "created_at": "2026-01-17T10:30:00Z",                          │
│             "updated_at": "2026-01-17T11:45:00Z",                          │
│             "edit_history": [...]                                           │
│           }                                                                  │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                              DATA FLOW EXAMPLES
═══════════════════════════════════════════════════════════════════════════════


FLOW 1: GENERATE WIREFRAME
───────────────────────────
User: Types "Create a dashboard"
  │
  ├─> POST /generate {"user_input": "Create a dashboard"}
  │
  ├─> Backend: Gemini generates WireframeLayout
  │
  ├─> Backend: create_project(wireframe) → MongoDB
  │            MongoDB saves: {_id: "abc-123", wireframe: {...}}
  │
  └─> Response: {
        "project_id": "abc-123",  ← Frontend saves this!
        "wireframe_layout": {
          "components": [...]
        }
      }

Frontend: 
  localStorage.setItem('currentProjectId', 'abc-123')
  renderWireframe(data.wireframe_layout)


FLOW 2: PAGE REFRESH (RESTORE PROJECT)
────────────────────────────────────────
User: Refreshes page
  │
  ├─> Frontend: projectId = localStorage.getItem('currentProjectId')
  │             projectId = 'abc-123'
  │
  ├─> GET /projects/abc-123
  │
  ├─> Backend: get_project("abc-123") ← MongoDB
  │            MongoDB returns: {_id: "abc-123", wireframe: {...}, ...}
  │
  └─> Response: {
        "_id": "abc-123",
        "name": "Student Club Dashboard",
        "wireframe": {
          "components": [...]  ← Full wireframe restored!
        }
      }

Frontend:
  renderWireframe(project.wireframe)
  ✅ Data restored!


FLOW 3: EDIT WIREFRAME
───────────────────────
User: "Add a settings tab"
  │
  ├─> POST /edit {
        "project_id": "abc-123",  ← Include to update MongoDB
        "wireframe_layout": {...},
        "instruction": "Add a settings tab"
      }
  │
  ├─> Backend: edit_wireframe() → Gemini generates new layout
  │
  ├─> Backend: update_project("abc-123", new_wireframe)
  │            MongoDB: db.projects.updateOne(
  │              {_id: "abc-123"},
  │              {$set: {wireframe: {...}, updated_at: now}}
  │            )
  │            Also adds to edit_history
  │
  └─> Response: {
        "project_id": "abc-123",
        "wireframe_layout": {
          "components": [...]  ← New wireframe with settings tab
        }
      }

Frontend:
  renderWireframe(data.wireframe_layout)


FLOW 4: MANUAL SAVE
────────────────────
User: Clicks "Save" button
  │
  ├─> POST /projects/abc-123/save {
        "wireframe": getCurrentCanvasState(),
        "name": "My Dashboard v2"
      }
  │
  ├─> Backend: update_project("abc-123", {...})
  │            MongoDB: db.projects.updateOne(...)
  │
  └─> Response: {
        "success": true,
        "name": "My Dashboard v2",
        "updated_at": "2026-01-17T12:00:00Z"
      }

Frontend:
  showNotification("Saved!")


FLOW 5: LIST PROJECTS (PROJECT GALLERY)
─────────────────────────────────────────
User: Opens project gallery
  │
  ├─> GET /projects?limit=50&sort_by=updated_at&sort_order=-1
  │
  ├─> Backend: list_projects()
  │            MongoDB: db.projects.find().sort({updated_at: -1}).limit(50)
  │
  └─> Response: [
        {
          "_id": "abc-123",
          "name": "Student Club Dashboard",
          "component_count": 5,
          "device_type": "laptop",
          "updated_at": "2026-01-17T11:45:00Z"
        },
        {
          "_id": "xyz-789",
          "name": "Login Page",
          "component_count": 3,
          ...
        }
      ]

Frontend:
  renderProjectList(projects)


═══════════════════════════════════════════════════════════════════════════════
                            KEY DESIGN DECISIONS
═══════════════════════════════════════════════════════════════════════════════

1. AUTO-SAVE ON GENERATION
   • Every /generate and /vision/analyze automatically creates MongoDB project
   • Frontend doesn't need to call save separately
   • User gets project_id immediately

2. PROJECT_ID IN RESPONSES
   • All generation endpoints return project_id
   • Frontend stores in localStorage + URL
   • Enables page refresh restoration

3. EDIT WITH PROJECT_ID
   • /edit accepts optional project_id
   • If provided → updates existing project
   • If omitted → just returns new wireframe (no save)

4. MANUAL SAVE OPTION
   • Separate /projects/{id}/save endpoint
   • User control over when to save
   • Your "Option B" requirement

5. HACKATHON-SAFE
   • If MongoDB fails → still returns wireframe
   • Generation never breaks
   • Just loses persistence
   • Allows demo without database

6. SINGLE-USER MODE
   • No authentication required
   • All projects shared
   • Easy to add user_id later for multi-user

7. EDIT HISTORY
   • Tracks all changes
   • Foundation for undo/redo
   • Useful for debugging

8. EDITABLE NAMES
   • Auto-generated but user can rename
   • Separate rename endpoint
   • Updates on blur in UI


═══════════════════════════════════════════════════════════════════════════════
                              BENEFITS RECAP
═══════════════════════════════════════════════════════════════════════════════

FOR USERS:
  ✅ No data loss on page refresh
  ✅ Share project URLs (?project=abc-123)
  ✅ Browse all past projects
  ✅ See when projects were created/updated
  ✅ Rename projects anytime
  ✅ Delete old projects

FOR DEVELOPMENT:
  ✅ Easy to add features (undo/redo, versioning, collaboration)
  ✅ Structured data (easy queries)
  ✅ Audit trail (edit history)
  ✅ Multi-user ready (just add user_id field)

FOR HACKATHON:
  ✅ Impressive feature ("Your work is automatically saved!")
  ✅ Demo-friendly (share URLs)
  ✅ Works even if MongoDB unavailable
  ✅ Free hosting (MongoDB Atlas free tier)
  ✅ Professional architecture
```

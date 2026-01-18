# MongoDB Integration Setup Guide

## 🎯 What Was Added

MongoDB persistence layer for SynthFrame - now all wireframes are automatically saved and survive page refreshes!

---

## 📦 New Files Created

```
backend/
  database/
    __init__.py          ✅ MongoDB connection manager
    models.py            ✅ Project schema (Pydantic models)
    operations.py        ✅ CRUD operations (create, read, update, delete)
  routes/
    projects.py          ✅ NEW: /projects endpoints
```

---

## 🔧 Modified Files

- ✅ `backend/requirements.txt` - Added motor & pymongo
- ✅ `backend/config.py` - Added MongoDB URL settings
- ✅ `backend/models/responses.py` - Added `project_id` field
- ✅ `backend/models/requests.py` - Added `project_id` to EditRequest
- ✅ `backend/routes/generate.py` - Auto-saves to MongoDB
- ✅ `backend/routes/vision.py` - Auto-saves to MongoDB
- ✅ `backend/routes/edit.py` - Updates MongoDB projects
- ✅ `backend/main.py` - Registers projects router + lifecycle events

---

## 🚀 Setup Instructions

### **1. Install Dependencies**

```bash
cd /Users/alexandersheng/projects/synthframe/backend
pip3 install -r requirements.txt
```

This installs:
- `motor>=3.3.0` - Async MongoDB driver for FastAPI
- `pymongo>=4.6.0` - Sync MongoDB driver

---

### **2. Setup MongoDB Atlas (Recommended)**

#### **Create Free Cluster:**
1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create account (or sign in with Google)
3. Click **"Build a Database"**
4. Choose **"M0 FREE"** tier
5. Pick a cloud provider (AWS/GCP/Azure) and region
6. Click **"Create"**

#### **Get Connection String:**
1. Click **"Connect"** on your cluster
2. Choose **"Connect your application"**
3. Copy the connection string:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

#### **Create Database User:**
1. Go to **Database Access** → **Add New Database User**
2. Username: `synthframe`
3. Password: (auto-generate or create strong password)
4. Give **Read and write to any database** permission
5. Click **Add User**

#### **Whitelist Your IP:**
1. Go to **Network Access** → **Add IP Address**
2. Click **"Allow Access from Anywhere"** (for development)
   - Or add your specific IP for security
3. Click **Confirm**

---

### **3. Configure Environment Variables**

Create `.env` file in `/Users/alexandersheng/projects/synthframe/backend/`:

```bash
# backend/.env

# Your Gemini API key
GEMINI_API_KEY=your_gemini_key_here

# MongoDB Connection (Atlas)
MONGODB_URL=mongodb+srv://synthframe:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=synthframe

# Or for local MongoDB (if you installed it locally):
# MONGODB_URL=mongodb://localhost:27017
# MONGODB_DB_NAME=synthframe
```

**Replace:**
- `YOUR_PASSWORD` with the password you created
- `cluster0.xxxxx` with your actual cluster address

---

### **4. Test the Setup**

Start the server:

```bash
cd /Users/alexandersheng/projects/synthframe/backend
python3 -m uvicorn main:app --reload --port 8000
```

You should see:
```
🚀 SynthFrame API Starting...
✅ MongoDB connected          <-- THIS IS GOOD!
📦 Scraper cache: 15 patterns pre-loaded
🤖 LLM: Gemini API configured
📍 API ready at http://localhost:8000
📚 Docs at http://localhost:8000/docs
```

If you see `⚠️ MongoDB not connected`, check your connection string in `.env`.

---

## 📡 New API Endpoints

### **GET /projects**
List all saved projects (lightweight)

```bash
curl http://localhost:8000/projects
```

Response:
```json
[
  {
    "_id": "uuid-here",
    "name": "Untitled Project 01/17 10:30",
    "generation_method": "text_prompt",
    "device_type": "laptop",
    "created_at": "2026-01-17T10:30:00",
    "updated_at": "2026-01-17T11:45:00",
    "component_count": 5
  }
]
```

---

### **GET /projects/{id}**
Get full project (including complete wireframe)

```bash
curl http://localhost:8000/projects/your-project-id
```

Response:
```json
{
  "_id": "uuid",
  "name": "Student Club Dashboard",
  "wireframe": {
    "id": "wireframe-uuid",
    "components": [...]  // Full wireframe data
  },
  "created_at": "...",
  "edit_history": []
}
```

---

### **POST /projects/{id}/save**
Manual save (Option B - when user clicks "Save")

```bash
curl -X POST http://localhost:8000/projects/{id}/save \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Updated Project",
    "wireframe": {...},
    "instruction": "Added footer"
  }'
```

---

### **PATCH /projects/{id}/rename**
Rename a project

```bash
curl -X PATCH http://localhost:8000/projects/{id}/rename \
  -H "Content-Type: application/json" \
  -d '{"name": "Cool Dashboard v2"}'
```

---

### **DELETE /projects/{id}**
Delete a project

```bash
curl -X DELETE http://localhost:8000/projects/{id}
```

---

## 🔄 How Auto-Save Works

### **When User Generates Wireframe:**

**Before (no persistence):**
```
User → POST /generate → Returns JSON → Lost on refresh
```

**After (with MongoDB):**
```
User → POST /generate → Saves to MongoDB → Returns JSON + project_id
Frontend saves project_id → Page refresh → Loads from MongoDB
```

### **Response Now Includes `project_id`:**

```json
{
  "success": true,
  "project_id": "abc-123-def-456",  // ← NEW!
  "wireframe_layout": {...},
  "message": "Generated 5 components"
}
```

### **All Generation Endpoints Auto-Save:**
- ✅ `POST /generate` (text prompt)
- ✅ `POST /vision/analyze` (sketch/mockup)
- ✅ `POST /edit` (if `project_id` provided)

---

## 🎨 Frontend Integration

### **Minimal Frontend Code (MVP):**

```javascript
// 1. After generation - save project_id
const response = await fetch('/generate', {
  method: 'POST',
  body: JSON.stringify({user_input: "Create a dashboard"})
});
const data = await response.json();

// Save to localStorage
localStorage.setItem('currentProject', data.project_id);

// 2. On page load - restore project
window.addEventListener('DOMContentLoaded', async () => {
  const projectId = localStorage.getItem('currentProject');
  
  if (projectId) {
    const project = await fetch(`/projects/${projectId}`).then(r => r.json());
    renderWireframe(project.wireframe);
  }
});

// 3. Manual save button
document.getElementById('saveBtn').onclick = async () => {
  const projectId = localStorage.getItem('currentProject');
  const wireframe = getCurrentWireframeState();
  
  await fetch(`/projects/${projectId}/save`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({wireframe})
  });
  
  alert('Saved!');
};
```

---

## 📊 Database Schema

### **Collection: `projects`**

Each project document looks like:

```json
{
  "_id": "uuid-string",
  "name": "Student Club Dashboard",
  "wireframe": {
    "id": "wireframe-uuid",
    "name": "Student Club Dashboard",
    "canvas_size": {"width": 1440, "height": 900},
    "source_type": "prompt",
    "components": [
      {
        "id": "comp-1",
        "type": "NAVBAR",
        "position": {"x": 0, "y": 0},
        "size": {"width": 1440, "height": 80},
        "props": {"text": "Logo"},
        "confidence": 1.0,
        "source": "gemini"
      }
    ]
  },
  "generation_method": "text_prompt",
  "device_type": "laptop",
  "created_at": "2026-01-17T10:30:00Z",
  "updated_at": "2026-01-17T11:45:00Z",
  "edit_history": [
    {
      "timestamp": "2026-01-17T11:45:00Z",
      "instruction": "Add a settings tab",
      "components_changed": 2,
      "method": "edit"
    }
  ],
  "original_prompt": "Create a dashboard for a student club",
  "webscraper_context": "..."
}
```

---

## ⚡️ Quick Test

### **1. Generate a wireframe:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Create a simple login page"}'
```

Copy the `project_id` from response.

### **2. Load it back:**
```bash
curl http://localhost:8000/projects/YOUR_PROJECT_ID
```

You should see the full wireframe!

### **3. List all projects:**
```bash
curl http://localhost:8000/projects
```

---

## 🐛 Troubleshooting

### **"MongoDB not connected"**

1. Check `.env` file exists in `backend/` folder
2. Verify connection string is correct
3. Check IP whitelist in Atlas
4. Try connection string in MongoDB Compass to test

### **"Module 'motor' not found"**

```bash
pip3 install motor pymongo
```

### **Projects not saving but server runs**

This is "hackathon-safe" behavior - if MongoDB fails, generation still works but data isn't persisted. Check the server logs for warnings.

---

## 🎯 Features Implemented

✅ Auto-save on generation  
✅ Auto-save on vision/sketch upload  
✅ Manual save button (Option B)  
✅ Project listing  
✅ Load project by ID  
✅ Rename project  
✅ Delete project  
✅ Edit history tracking  
✅ Auto-generated project names (editable)  
✅ Graceful fallback if MongoDB unavailable  

---

## 🔮 Future Enhancements (Post-Hackathon)

- [ ] User authentication (multi-user support)
- [ ] Project thumbnails (screenshot previews)
- [ ] Undo/redo using edit history
- [ ] Project templates/sharing
- [ ] Version history
- [ ] Collaborative editing

---

## 📞 Need Help?

Check MongoDB connection:
```bash
curl http://localhost:8000/health
```

View API docs:
```
http://localhost:8000/docs
```

Happy hacking! 🚀

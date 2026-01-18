# MongoDB Integration - Quick Reference

## ✅ IMPLEMENTATION COMPLETE

All MongoDB integration is done and ready to use!

---

## 🎯 What You Got

### **Backend Changes**
- ✅ MongoDB connection using Motor (async driver)
- ✅ Auto-save on `/generate` (text prompts)
- ✅ Auto-save on `/vision/analyze` (sketches)
- ✅ Auto-update on `/edit` (with project_id)
- ✅ Manual save endpoint: `POST /projects/{id}/save`
- ✅ Full CRUD: list, get, update, rename, delete projects
- ✅ Edit history tracking
- ✅ Hackathon-safe: Works even if MongoDB fails

### **New API Endpoints**
```
GET    /projects              - List all projects
GET    /projects/{id}         - Get specific project (for page restore)
POST   /projects/{id}/save    - Manual save
PATCH  /projects/{id}/rename  - Rename project
DELETE /projects/{id}         - Delete project
GET    /projects/stats/summary - Get statistics
```

### **Updated Responses**
All generation endpoints now return `project_id`:
```json
{
  "success": true,
  "project_id": "abc-123-def-456",  // ← NEW!
  "wireframe_layout": {...}
}
```

---

## 🚀 Next Steps

### 1. Install MongoDB Dependencies
```bash
cd backend
pip3 install -r requirements.txt
```

### 2. Set Up MongoDB

**Option A: MongoDB Atlas (Cloud) - RECOMMENDED**
- Sign up: https://www.mongodb.com/cloud/atlas
- Create free cluster
- Get connection string
- Add to `.env`

**Option B: Local MongoDB**
```bash
brew install mongodb-community
brew services start mongodb-community
```

### 3. Configure Environment

Create `backend/.env`:
```bash
# MongoDB (choose one)
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
# OR
MONGODB_URL=mongodb://localhost:27017

MONGODB_DB_NAME=synthframe

# Your existing keys
GEMINI_API_KEY=your_key_here
```

### 4. Start Server
```bash
cd backend
python3 -m uvicorn main:app --reload --port 8000
```

Look for:
```
✅ MongoDB connected
```

---

## 🎨 Frontend Integration (3 Simple Changes)

### 1. Save Project ID After Generation
```javascript
const response = await fetch('/generate', {...});
const data = await response.json();
localStorage.setItem('currentProjectId', data.project_id);
```

### 2. Restore on Page Load
```javascript
const projectId = localStorage.getItem('currentProjectId') || 
                  new URLSearchParams(window.location.search).get('project');

if (projectId) {
  const project = await fetch(`/projects/${projectId}`).then(r => r.json());
  renderWireframe(project.wireframe);
}
```

### 3. Manual Save Button
```javascript
document.getElementById('save').onclick = async () => {
  await fetch(`/projects/${localStorage.getItem('currentProjectId')}/save`, {
    method: 'POST',
    body: JSON.stringify({wireframe: getCurrentWireframe()})
  });
};
```

**That's it!** Your data now persists across page refreshes.

---

## 📁 Files Created/Modified

### Created:
- `backend/database/__init__.py` - Connection manager
- `backend/database/models.py` - Project schema
- `backend/database/operations.py` - CRUD functions
- `backend/routes/projects.py` - Project endpoints

### Modified:
- `backend/requirements.txt` - Added motor, pymongo
- `backend/config.py` - Added MongoDB settings
- `backend/models/responses.py` - Added project_id field
- `backend/models/requests.py` - Added project_id to EditRequest
- `backend/routes/generate.py` - Auto-save to MongoDB
- `backend/routes/vision.py` - Auto-save to MongoDB
- `backend/routes/edit.py` - Update MongoDB on edit
- `backend/main.py` - Register projects router + lifecycle

---

## 🧪 Quick Test

```bash
# 1. Generate wireframe
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Create a login page"}'

# Look for project_id in response

# 2. List projects
curl http://localhost:8000/projects

# 3. Get specific project
curl http://localhost:8000/projects/{project_id}
```

---

## 📚 Full Documentation

See `MONGODB_SETUP.md` for complete guide including:
- Detailed API documentation
- Database schema
- Troubleshooting
- Advanced features

---

## 💡 Key Benefits

1. **No Data Loss** - Page refresh doesn't lose work
2. **Project Gallery** - List all saved projects
3. **Share URLs** - `?project=abc-123` loads that project
4. **Edit History** - Track what changed
5. **Auto-Save** - No manual save needed (but option available)
6. **Hackathon-Safe** - Works without MongoDB (just won't persist)

---

**Ready to test! 🚀**

# 🚀 Backend Startup & MongoDB Testing Guide

## 📋 OVERVIEW

This guide will walk you through:
1. **Setting up MongoDB** (local or cloud)
2. **Starting the backend server**
3. **Testing MongoDB integration** step-by-step
4. **Verifying everything works**

---

## ⚙️ PART 1: MONGODB SETUP (Choose One Option)

### **OPTION A: Local MongoDB (Fastest for Development)**

#### Step 1: Install MongoDB
```bash
# macOS
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb-community

# Verify it's running
brew services list | grep mongodb
# Should show: mongodb-community started
```

#### Step 2: Verify MongoDB is Running
```bash
# Try connecting with mongosh
mongosh

# You should see:
# Current Mongosh Log ID: ...
# Connecting to: mongodb://127.0.0.1:27017/...
# test>

# Type: exit
```

**Your connection string:** `mongodb://localhost:27017`

---

### **OPTION B: MongoDB Atlas (Cloud - Recommended for Sharing)**

#### Step 1: Create Free Account
1. Go to: https://www.mongodb.com/cloud/atlas
2. Click "Try Free"
3. Sign up (no credit card required)

#### Step 2: Create Cluster
1. Choose "M0 Sandbox" (FREE)
2. Select cloud provider (AWS recommended)
3. Choose region closest to you
4. Name cluster: "synthframe"
5. Click "Create Deployment" (takes ~3-5 minutes)

#### Step 3: Create Database User
1. Choose "Username and Password"
2. Username: `synthframe_user`
3. Password: Generate strong password (save it!)
4. Click "Create Database User"

#### Step 4: Add IP to Allowlist
1. Click "Add IP Address"
2. Click "Add Current IP Address"
3. Or click "Allow Access from Anywhere" (0.0.0.0/0) for hackathon
4. Click "Confirm"

#### Step 5: Get Connection String
1. Click "Connect"
2. Choose "Connect your application"
3. Driver: Python, Version: 3.12 or later
4. Copy the connection string:
   ```
   mongodb+srv://synthframe_user:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password

**Your connection string:** `mongodb+srv://synthframe_user:YOUR_PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority`

---

## 📝 PART 2: CONFIGURE BACKEND

### Step 1: Create .env File

```bash
cd /Users/alexandersheng/projects/synthframe/backend

# Copy the example file
cp .env.example .env

# Now edit .env with your favorite editor
nano .env
# or
code .env
# or
open .env
```

### Step 2: Add MongoDB Configuration

Open `.env` and add these lines:

**For Local MongoDB:**
```bash
# MongoDB Configuration (LOCAL)
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=synthframe

# Gemini API (if you have it)
GEMINI_API_KEY=your_gemini_key_here

# OR use mock mode for testing without Gemini
MOCK_LLM=1
```

**For MongoDB Atlas (Cloud):**
```bash
# MongoDB Configuration (ATLAS)
MONGODB_URL=mongodb+srv://synthframe_user:YOUR_PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=synthframe

# Gemini API (if you have it)
GEMINI_API_KEY=your_gemini_key_here

# OR use mock mode for testing without Gemini
MOCK_LLM=1
```

### Step 3: Verify Environment Variables

```bash
# Check .env file exists
ls -la .env

# Should see something like:
# -rw-r--r--  1 user  staff  XXX Jan 17 12:00 .env
```

---

## 🚀 PART 3: START THE BACKEND

### Step 1: Open Terminal in Backend Directory

```bash
cd /Users/alexandersheng/projects/synthframe/backend

# Verify you're in the right place
pwd
# Should output: /Users/alexandersheng/projects/synthframe/backend
```

### Step 2: Activate Virtual Environment (If Using)

```bash
# If you have a venv
source venv/bin/activate

# OR if using conda
conda activate synthframe
```

### Step 3: Start the Server

```bash
python3 -m uvicorn main:app --reload --port 8000
```

### Step 4: Look for Success Messages

You should see output like this:

```
INFO:     Will watch for changes in these directories: ['/Users/alexandersheng/projects/synthframe/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXXX] using WatchFiles
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
============================================================
🚀 SynthFrame API Starting...
============================================================
✅ MongoDB connected                    ← IMPORTANT: Look for this!
📦 Scraper cache: X patterns pre-loaded
🤖 LLM: Gemini API configured (or Mock mode)
============================================================
📍 API ready at http://localhost:8000
📚 Docs at http://localhost:8000/docs
============================================================
INFO:     Application startup complete.
```

**KEY INDICATORS:**
- ✅ **"MongoDB connected"** - MongoDB is working!
- ⚠️  **"MongoDB not connected"** - Check your connection string

### Step 5: Keep This Terminal Open

**DO NOT CLOSE THIS TERMINAL** - the server needs to keep running while you test.

---

## 🧪 PART 4: TESTING MONGODB INTEGRATION

Now that the server is running, **open a NEW terminal** for testing.

### Quick Health Check (Browser)

Open in browser: http://localhost:8000/docs

You should see:
- FastAPI interactive documentation
- List of all endpoints
- Green "Authorize" button

---

## 🔍 PART 5: UNDERSTANDING THE TEST PROCESS

### What We'll Test

The test file (`test_mongodb.py`) will verify:

1. **Health Check** - Is server responding?
2. **Generate Wireframe** - Does it return project_id?
3. **Save to MongoDB** - Is project actually saved?
4. **Retrieve Project** - Can we get it back?
5. **Page Refresh Simulation** - Does persistence work?
6. **Edit Wireframe** - Does update work?
7. **Manual Save** - Does save endpoint work?
8. **List Projects** - Can we see all projects?
9. **Rename Project** - Does rename work?
10. **Delete Project** - Does delete work?

### How Testing Works

```
┌─────────────────────────────────────────────────────────────┐
│                    TESTING PROCESS                           │
└─────────────────────────────────────────────────────────────┘

Step 1: Start Backend Server
   └─> Terminal 1: python3 -m uvicorn main:app --reload
   └─> Server starts on port 8000
   └─> MongoDB connection established

Step 2: Run Test Script
   └─> Terminal 2: python3 test_mongodb.py
   └─> Script sends HTTP requests to localhost:8000
   
Step 3: Test Flow
   ┌────────────────────────────────────────────────────┐
   │ 1. Health Check                                     │
   │    GET /health                                      │
   │    ✅ Verify server is running                     │
   └────────────────────────────────────────────────────┘
   
   ┌────────────────────────────────────────────────────┐
   │ 2. Generate Wireframe                               │
   │    POST /generate {"user_input": "login page"}     │
   │    ✅ Returns: {project_id: "abc-123", ...}        │
   │    ✅ Backend auto-saves to MongoDB                │
   └────────────────────────────────────────────────────┘
   
   ┌────────────────────────────────────────────────────┐
   │ 3. Get Project (Simulate Page Refresh)             │
   │    GET /projects/abc-123                            │
   │    ✅ MongoDB returns full wireframe               │
   │    ✅ Same as what was generated                   │
   └────────────────────────────────────────────────────┘
   
   ┌────────────────────────────────────────────────────┐
   │ 4. List All Projects                                │
   │    GET /projects                                    │
   │    ✅ Returns array with our project               │
   └────────────────────────────────────────────────────┘
   
   ┌────────────────────────────────────────────────────┐
   │ 5. Edit Wireframe                                   │
   │    POST /edit with project_id                       │
   │    ✅ MongoDB updates project                      │
   │    ✅ Edit history recorded                        │
   └────────────────────────────────────────────────────┘
   
   ┌────────────────────────────────────────────────────┐
   │ 6. Manual Save                                      │
   │    POST /projects/abc-123/save                      │
   │    ✅ MongoDB updates with new data                │
   └────────────────────────────────────────────────────┘
   
   ┌────────────────────────────────────────────────────┐
   │ 7. Rename Project                                   │
   │    PATCH /projects/abc-123/rename                   │
   │    ✅ Name updated in MongoDB                      │
   └────────────────────────────────────────────────────┘
   
   ┌────────────────────────────────────────────────────┐
   │ 8. Delete Project                                   │
   │    DELETE /projects/abc-123                         │
   │    ✅ Project removed from MongoDB                 │
   │    ✅ GET returns 404                              │
   └────────────────────────────────────────────────────┘

Step 4: View Results
   └─> Terminal 2 shows: ✅ X/10 tests passed
   └─> Backend logs show all requests
```

---

## 📝 PART 6: WHAT EACH TEST VERIFIES

### Test 1: Health Check
- **Purpose:** Verify server is responding
- **What it does:** GET /health
- **Success:** Returns {"status": "healthy"}
- **If fails:** Server not running or crashed

### Test 2: Generate Wireframe
- **Purpose:** Verify generation + auto-save
- **What it does:** POST /generate with text prompt
- **Success:** Returns project_id + wireframe
- **Verifies:** 
  - Gemini/mock generation works
  - MongoDB auto-save works
  - project_id is returned

### Test 3: Get Project
- **Purpose:** Verify persistence (page refresh scenario)
- **What it does:** GET /projects/{id}
- **Success:** Returns full project from MongoDB
- **Verifies:**
  - MongoDB stored the project
  - Can retrieve by ID
  - Wireframe data is intact

### Test 4: List Projects
- **Purpose:** Verify query capabilities
- **What it does:** GET /projects
- **Success:** Returns array with our project
- **Verifies:**
  - MongoDB queries work
  - Projects are findable

### Test 5: Edit Wireframe
- **Purpose:** Verify edit updates MongoDB
- **What it does:** POST /edit with project_id
- **Success:** Project updated in MongoDB
- **Verifies:**
  - Edit endpoint works
  - MongoDB update works
  - Edit history recorded

### Test 6: Manual Save
- **Purpose:** Verify Option B (manual save)
- **What it does:** POST /projects/{id}/save
- **Success:** Project updated with new data
- **Verifies:**
  - Save endpoint works
  - Frontend can trigger saves

### Test 7: Rename Project
- **Purpose:** Verify name editing
- **What it does:** PATCH /projects/{id}/rename
- **Success:** Name updated in MongoDB
- **Verifies:**
  - Rename endpoint works
  - Partial updates work

### Test 8: Delete Project
- **Purpose:** Verify cleanup
- **What it does:** DELETE /projects/{id}
- **Success:** Project removed, GET returns 404
- **Verifies:**
  - Delete endpoint works
  - MongoDB deletion works

---

## 🎯 SUCCESS CRITERIA

### ✅ Everything Works If:
1. Server starts with "✅ MongoDB connected"
2. All 8 tests pass (8/8)
3. No error messages in server logs
4. Projects visible in MongoDB

### ⚠️ Troubleshooting

#### Issue: "MongoDB not connected"
**Solution:**
1. Check MONGODB_URL in .env
2. For local: Is MongoDB running? `brew services list`
3. For Atlas: Is IP allowlisted? Check Atlas dashboard
4. Check .env file is in correct location (backend/.env)

#### Issue: "Connection refused"
**Solution:**
1. Is server running? Check Terminal 1
2. Is it on port 8000? Check uvicorn output
3. Try: http://localhost:8000/docs in browser

#### Issue: Tests timeout
**Solution:**
1. Increase timeout in test file
2. Check Gemini API if using real API
3. Use MOCK_LLM=1 for faster testing

#### Issue: "Project not found"
**Solution:**
1. MongoDB might not have saved
2. Check server logs for errors
3. Verify MONGODB_DB_NAME in .env

---

## 📊 EXPECTED OUTPUT

### Server Terminal (Terminal 1)
```
✅ MongoDB connected
📍 API ready at http://localhost:8000
INFO:     127.0.0.1:xxxxx - "POST /generate HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "GET /projects/abc-123 HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /edit HTTP/1.1" 200 OK
...
```

### Test Terminal (Terminal 2)
```
🧪 Starting MongoDB Integration Tests...
============================================================

✅ PASS - Health Check
✅ PASS - Generate Wireframe
   └─> project_id: abc-123-def-456
✅ PASS - Get Project
   └─> Retrieved: "Test Project"
✅ PASS - List Projects
   └─> Found 1 project(s)
✅ PASS - Edit Wireframe
   └─> Edit recorded in history
✅ PASS - Manual Save
   └─> Saved at: 2026-01-17 23:45:00
✅ PASS - Rename Project
   └─> New name: "Updated Name"
✅ PASS - Delete Project
   └─> Confirmed deleted

============================================================
📊 Results: 8/8 tests passed (100%)
🎉 MongoDB integration is working perfectly!
============================================================
```

---

## 🚦 NEXT STEPS AFTER TESTING

### If All Tests Pass ✅
1. Keep server running
2. Integrate with frontend
3. Test from browser/Postman
4. Deploy for demo

### If Tests Fail ⚠️
1. Check error messages
2. Review troubleshooting section
3. Check server logs in Terminal 1
4. Verify .env configuration
5. Try simple test: curl http://localhost:8000/health

---

## 📱 QUICK REFERENCE COMMANDS

### Start Server
```bash
cd /Users/alexandersheng/projects/synthframe/backend
python3 -m uvicorn main:app --reload --port 8000
```

### Run Tests (in new terminal)
```bash
cd /Users/alexandersheng/projects/synthframe
python3 test_mongodb.py
```

### Stop Server
```
Press CTRL+C in Terminal 1
```

### Check MongoDB (local)
```bash
mongosh
use synthframe
db.projects.find()
```

### View API Docs
```
http://localhost:8000/docs
```

---

## 🎓 UNDERSTANDING THE FLOW

### What Happens When You Generate:
```
1. Frontend/Test sends: POST /generate
2. Backend calls Gemini (or mock)
3. Backend gets WireframeLayout
4. Backend calls: create_project(wireframe)
5. MongoDB saves: {_id: "abc", wireframe: {...}}
6. Backend returns: {project_id: "abc", wireframe: {...}}
7. Frontend saves: localStorage.setItem('projectId', 'abc')
```

### What Happens on Page Refresh:
```
1. Frontend reads: localStorage.getItem('projectId') → "abc"
2. Frontend sends: GET /projects/abc
3. Backend queries: MongoDB.find({_id: "abc"})
4. MongoDB returns: {_id: "abc", wireframe: {...}, ...}
5. Backend returns: Full project
6. Frontend renders: Wireframe on canvas
7. ✅ User's work is restored!
```

---

**Ready to start? Follow PART 1 to set up MongoDB! 🚀**

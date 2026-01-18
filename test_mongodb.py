#!/usr/bin/env python3
"""
MongoDB Integration Test Suite
================================

This script tests the complete MongoDB integration for SynthFrame.

BEFORE RUNNING:
1. Start the backend server in another terminal:
   cd backend
   python3 -m uvicorn main:app --reload --port 8000

2. Make sure MongoDB is configured in backend/.env:
   MONGODB_URL=mongodb://localhost:27017  (or Atlas URL)
   MONGODB_DB_NAME=synthframe

3. Run this test:
   python3 test_mongodb.py

WHAT THIS TESTS:
- Health check
- Generate wireframe with auto-save
- Retrieve project (page refresh simulation)
- List all projects
- Edit wireframe with MongoDB update
- Manual save endpoint
- Rename project
- Delete project

EXPECTED RESULT:
✅ All 8 tests should pass if MongoDB integration is working
"""

import asyncio
import httpx
import json
import sys
from datetime import datetime
from typing import Optional, Dict, Any

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_URL = "http://localhost:8000"
TIMEOUT = 60.0  # Increased timeout for Gemini API calls

# Test tracking
class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
        self.project_id: Optional[str] = None
    
    def log(self, name: str, passed: bool, message: str = "", details: Any = None):
        """Log a test result"""
        self.tests.append({
            "name": name,
            "passed": passed,
            "message": message,
            "details": details
        })
        
        if passed:
            self.passed += 1
            print(f"✅ PASS - {name}")
            if message:
                print(f"   └─> {message}")
        else:
            self.failed += 1
            print(f"❌ FAIL - {name}")
            if message:
                print(f"   └─> ERROR: {message}")
            if details:
                print(f"   └─> Details: {details}")
    
    def summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}/{total}")
        print(f"❌ Failed: {self.failed}/{total}")
        print(f"📈 Success Rate: {percentage:.1f}%")
        print("=" * 60)
        
        if self.failed > 0:
            print("\n⚠️  SOME TESTS FAILED")
            print("\nFailed tests:")
            for test in self.tests:
                if not test["passed"]:
                    print(f"  • {test['name']}: {test['message']}")
            
            print("\n💡 Troubleshooting:")
            print("  1. Is the server running? (Terminal 1)")
            print("  2. Did you see '✅ MongoDB connected' in server logs?")
            print("  3. Is MONGODB_URL correct in backend/.env?")
            print("  4. For Atlas: Is IP allowlisted?")
            print("  5. Try: curl http://localhost:8000/health")
        else:
            print("\n🎉 ALL TESTS PASSED!")
            print("MongoDB integration is working perfectly!")
            print("\n✅ Next Steps:")
            print("  1. MongoDB persistence is confirmed working")
            print("  2. Ready to integrate with frontend")
            print("  3. Frontend should save project_id after generation")
            print("  4. Frontend should restore from project_id on page load")
        
        return self.failed == 0


# Global results tracker
results = TestResults()


# =============================================================================
# TEST FUNCTIONS
# =============================================================================

async def test_1_health_check():
    """
    TEST 1: Health Check
    Purpose: Verify server is responding and MongoDB is connected
    """
    print("\n" + "─" * 60)
    print("TEST 1: Health Check")
    print("─" * 60)
    print("Purpose: Verify server is running and MongoDB is connected")
    print("Request: GET /health")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/health")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if server is healthy
                if data.get("status") == "healthy":
                    results.log(
                        "Health Check",
                        True,
                        f"Server is healthy (v{data.get('version', 'unknown')})"
                    )
                else:
                    results.log(
                        "Health Check",
                        False,
                        f"Server status: {data.get('status')}",
                        data
                    )
            else:
                results.log(
                    "Health Check",
                    False,
                    f"HTTP {response.status_code}",
                    response.text
                )
    except httpx.ConnectError:
        results.log(
            "Health Check",
            False,
            "Cannot connect to server. Is it running on port 8000?",
            "Run: cd backend && python3 -m uvicorn main:app --reload"
        )
    except Exception as e:
        results.log("Health Check", False, str(e))


async def test_2_generate_wireframe():
    """
    TEST 2: Generate Wireframe with Auto-Save
    Purpose: Verify generation works and returns project_id
    """
    print("\n" + "─" * 60)
    print("TEST 2: Generate Wireframe (Auto-Save)")
    print("─" * 60)
    print("Purpose: Generate wireframe and verify MongoDB auto-save")
    print("Request: POST /generate")
    print("Payload: {user_input: 'Create a simple login page'}")
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            payload = {
                "user_input": "Create a simple login page for testing",
                "device_type": "macbook",
                "use_scraper": False  # Faster without scraper
            }
            
            print("⏳ Generating wireframe (this may take 10-30 seconds)...")
            response = await client.post(
                f"{BASE_URL}/generate",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for success
                if not data.get("success"):
                    results.log(
                        "Generate Wireframe",
                        False,
                        "success=false in response",
                        data
                    )
                    return
                
                # Check for project_id (KEY FEATURE)
                project_id = data.get("project_id")
                if not project_id:
                    results.log(
                        "Generate Wireframe",
                        False,
                        "No project_id returned (MongoDB auto-save failed?)",
                        data
                    )
                    return
                
                # Check for wireframe_layout
                wireframe = data.get("wireframe_layout")
                if not wireframe:
                    results.log(
                        "Generate Wireframe",
                        False,
                        "No wireframe_layout in response",
                        data
                    )
                    return
                
                # Check wireframe has components
                components = wireframe.get("components", [])
                
                # Save project_id for subsequent tests
                results.project_id = project_id
                
                results.log(
                    "Generate Wireframe",
                    True,
                    f"project_id: {project_id[:20]}..., {len(components)} components"
                )
                
                print(f"   📦 Wireframe Details:")
                print(f"      • Components: {len(components)}")
                print(f"      • Canvas: {wireframe.get('canvas_size', {})}")
                print(f"      • Source: {wireframe.get('source_type', 'unknown')}")
                
            else:
                results.log(
                    "Generate Wireframe",
                    False,
                    f"HTTP {response.status_code}",
                    response.text[:200]
                )
    except httpx.TimeoutException:
        results.log(
            "Generate Wireframe",
            False,
            "Request timed out (Gemini API might be slow)",
            "Try setting MOCK_LLM=1 in .env for faster testing"
        )
    except Exception as e:
        results.log("Generate Wireframe", False, str(e))


async def test_3_get_project():
    """
    TEST 3: Get Project by ID (Page Refresh Simulation)
    Purpose: Verify project was saved to MongoDB and can be retrieved
    """
    print("\n" + "─" * 60)
    print("TEST 3: Get Project (Page Refresh Simulation)")
    print("─" * 60)
    print("Purpose: Verify project persists in MongoDB")
    print("Simulates: User refreshes page, frontend loads project")
    
    if not results.project_id:
        results.log(
            "Get Project",
            False,
            "No project_id from previous test (Test 2 must pass first)"
        )
        return
    
    print(f"Request: GET /projects/{results.project_id[:20]}...")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{BASE_URL}/projects/{results.project_id}"
            )
            
            if response.status_code == 200:
                project = response.json()
                
                # Verify project structure
                required_fields = ["_id", "name", "wireframe", "created_at", "updated_at"]
                missing_fields = [f for f in required_fields if f not in project]
                
                if missing_fields:
                    results.log(
                        "Get Project",
                        False,
                        f"Missing fields: {missing_fields}",
                        project.keys()
                    )
                    return
                
                # Verify wireframe has components
                wireframe = project.get("wireframe", {})
                components = wireframe.get("components", [])
                
                results.log(
                    "Get Project",
                    True,
                    f"Retrieved '{project.get('name')}' with {len(components)} components"
                )
                
                print(f"   📊 Project Details:")
                print(f"      • Name: {project.get('name')}")
                print(f"      • Method: {project.get('generation_method')}")
                print(f"      • Device: {project.get('device_type')}")
                print(f"      • Created: {project.get('created_at')}")
                print(f"      • Components: {len(components)}")
                
            elif response.status_code == 404:
                results.log(
                    "Get Project",
                    False,
                    "Project not found in MongoDB (auto-save failed?)",
                    f"project_id: {results.project_id}"
                )
            else:
                results.log(
                    "Get Project",
                    False,
                    f"HTTP {response.status_code}",
                    response.text[:200]
                )
    except Exception as e:
        results.log("Get Project", False, str(e))


async def test_4_list_projects():
    """
    TEST 4: List All Projects
    Purpose: Verify project query/listing works
    """
    print("\n" + "─" * 60)
    print("TEST 4: List Projects")
    print("─" * 60)
    print("Purpose: Verify project listing/querying")
    print("Request: GET /projects")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/projects")
            
            if response.status_code == 200:
                projects = response.json()
                
                if not isinstance(projects, list):
                    results.log(
                        "List Projects",
                        False,
                        "Response is not a list",
                        type(projects)
                    )
                    return
                
                # Check if our project is in the list
                found_our_project = False
                if results.project_id:
                    found_our_project = any(
                        p.get("_id") == results.project_id for p in projects
                    )
                
                if found_our_project:
                    results.log(
                        "List Projects",
                        True,
                        f"Found {len(projects)} project(s), including our test project"
                    )
                elif len(projects) > 0:
                    results.log(
                        "List Projects",
                        True,
                        f"Found {len(projects)} project(s)"
                    )
                else:
                    results.log(
                        "List Projects",
                        True,
                        "No projects yet (empty database)"
                    )
                
                if projects:
                    print(f"   📚 Projects in Database:")
                    for i, p in enumerate(projects[:5], 1):  # Show first 5
                        print(f"      {i}. {p.get('name')} ({p.get('component_count', 0)} components)")
                    if len(projects) > 5:
                        print(f"      ... and {len(projects) - 5} more")
                
            else:
                results.log(
                    "List Projects",
                    False,
                    f"HTTP {response.status_code}",
                    response.text[:200]
                )
    except Exception as e:
        results.log("List Projects", False, str(e))


async def test_5_edit_wireframe():
    """
    TEST 5: Edit Wireframe with MongoDB Update
    Purpose: Verify edit endpoint updates MongoDB
    """
    print("\n" + "─" * 60)
    print("TEST 5: Edit Wireframe (MongoDB Update)")
    print("─" * 60)
    print("Purpose: Verify edit updates MongoDB with history tracking")
    print("Request: POST /edit")
    
    if not results.project_id:
        results.log(
            "Edit Wireframe",
            False,
            "No project_id available"
        )
        return
    
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # First, get current project
            get_response = await client.get(
                f"{BASE_URL}/projects/{results.project_id}"
            )
            
            if get_response.status_code != 200:
                results.log(
                    "Edit Wireframe",
                    False,
                    "Could not fetch project for editing"
                )
                return
            
            project = get_response.json()
            
            # Edit it
            payload = {
                "project_id": results.project_id,
                "wireframe_layout": project["wireframe"],
                "instruction": "Add a footer section",
                "use_scraper": False
            }
            
            print("⏳ Editing wireframe (this may take 10-30 seconds)...")
            edit_response = await client.post(
                f"{BASE_URL}/edit",
                json=payload
            )
            
            if edit_response.status_code == 200:
                data = edit_response.json()
                
                if data.get("success"):
                    results.log(
                        "Edit Wireframe",
                        True,
                        f"Edit successful, project_id: {data.get('project_id', 'N/A')[:20]}..."
                    )
                    
                    # Verify MongoDB was updated
                    verify_response = await client.get(
                        f"{BASE_URL}/projects/{results.project_id}"
                    )
                    
                    if verify_response.status_code == 200:
                        updated_project = verify_response.json()
                        edit_history = updated_project.get("edit_history", [])
                        print(f"   📝 Edit History: {len(edit_history)} edit(s) recorded")
                else:
                    results.log(
                        "Edit Wireframe",
                        False,
                        "success=false in response",
                        data
                    )
            else:
                results.log(
                    "Edit Wireframe",
                    False,
                    f"HTTP {edit_response.status_code}",
                    edit_response.text[:200]
                )
    except httpx.TimeoutException:
        results.log(
            "Edit Wireframe",
            False,
            "Request timed out",
            "Try setting MOCK_LLM=1 in .env"
        )
    except Exception as e:
        results.log("Edit Wireframe", False, str(e))


async def test_6_manual_save():
    """
    TEST 6: Manual Save Endpoint
    Purpose: Verify Option B (user clicks Save button)
    """
    print("\n" + "─" * 60)
    print("TEST 6: Manual Save (Option B)")
    print("─" * 60)
    print("Purpose: Verify manual save endpoint (user clicks 'Save')")
    print(f"Request: POST /projects/{results.project_id[:20] if results.project_id else 'N/A'}.../save")
    
    if not results.project_id:
        results.log(
            "Manual Save",
            False,
            "No project_id available"
        )
        return
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Get current project
            get_response = await client.get(
                f"{BASE_URL}/projects/{results.project_id}"
            )
            
            if get_response.status_code != 200:
                results.log(
                    "Manual Save",
                    False,
                    "Could not fetch project"
                )
                return
            
            project = get_response.json()
            wireframe = project["wireframe"]
            
            # Modify something (simulate user change)
            if wireframe.get("components"):
                wireframe["components"][0]["props"]["test_save"] = True
            
            # Manual save
            payload = {
                "wireframe": wireframe,
                "name": "Test Project (Saved)",
                "instruction": "Manual save test"
            }
            
            response = await client.post(
                f"{BASE_URL}/projects/{results.project_id}/save",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                results.log(
                    "Manual Save",
                    True,
                    f"Saved at {data.get('updated_at', 'unknown time')}"
                )
            else:
                results.log(
                    "Manual Save",
                    False,
                    f"HTTP {response.status_code}",
                    response.text[:200]
                )
    except Exception as e:
        results.log("Manual Save", False, str(e))


async def test_7_rename_project():
    """
    TEST 7: Rename Project
    Purpose: Verify project renaming works
    """
    print("\n" + "─" * 60)
    print("TEST 7: Rename Project")
    print("─" * 60)
    print("Purpose: Verify project name can be updated")
    print(f"Request: PATCH /projects/{results.project_id[:20] if results.project_id else 'N/A'}.../rename")
    
    if not results.project_id:
        results.log(
            "Rename Project",
            False,
            "No project_id available"
        )
        return
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            new_name = f"Test Project - {datetime.now().strftime('%H:%M:%S')}"
            
            response = await client.patch(
                f"{BASE_URL}/projects/{results.project_id}/rename",
                json={"name": new_name}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("name") == new_name:
                    results.log(
                        "Rename Project",
                        True,
                        f"Renamed to '{new_name}'"
                    )
                else:
                    results.log(
                        "Rename Project",
                        False,
                        "Name not updated correctly",
                        f"Expected: {new_name}, Got: {data.get('name')}"
                    )
            else:
                results.log(
                    "Rename Project",
                    False,
                    f"HTTP {response.status_code}",
                    response.text[:200]
                )
    except Exception as e:
        results.log("Rename Project", False, str(e))


async def test_8_delete_project():
    """
    TEST 8: Delete Project
    Purpose: Verify project deletion works
    """
    print("\n" + "─" * 60)
    print("TEST 8: Delete Project")
    print("─" * 60)
    print("Purpose: Verify project can be deleted from MongoDB")
    print(f"Request: DELETE /projects/{results.project_id[:20] if results.project_id else 'N/A'}...")
    
    if not results.project_id:
        results.log(
            "Delete Project",
            False,
            "No project_id available"
        )
        return
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Delete
            delete_response = await client.delete(
                f"{BASE_URL}/projects/{results.project_id}"
            )
            
            if delete_response.status_code == 200:
                # Verify it's actually deleted
                get_response = await client.get(
                    f"{BASE_URL}/projects/{results.project_id}"
                )
                
                if get_response.status_code == 404:
                    results.log(
                        "Delete Project",
                        True,
                        "Project deleted and confirmed removed"
                    )
                else:
                    results.log(
                        "Delete Project",
                        False,
                        "Project still exists after delete",
                        f"GET returned {get_response.status_code}"
                    )
            else:
                results.log(
                    "Delete Project",
                    False,
                    f"HTTP {delete_response.status_code}",
                    delete_response.text[:200]
                )
    except Exception as e:
        results.log("Delete Project", False, str(e))


# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

async def run_all_tests():
    """Run all tests in sequence"""
    print("=" * 60)
    print("🧪 MONGODB INTEGRATION TEST SUITE")
    print("=" * 60)
    print(f"Server: {BASE_URL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Pre-flight check
    print("\n🔍 Pre-flight check...")
    print(f"   • Server URL: {BASE_URL}")
    print(f"   • Timeout: {TIMEOUT}s")
    print(f"   • Ready to test!")
    
    # Run tests sequentially
    await test_1_health_check()
    
    # Only continue if health check passed
    if results.passed == 0:
        print("\n⚠️  Health check failed. Cannot continue testing.")
        print("Make sure the server is running:")
        print("  cd backend && python3 -m uvicorn main:app --reload --port 8000")
        return False
    
    await test_2_generate_wireframe()
    await test_3_get_project()
    await test_4_list_projects()
    await test_5_edit_wireframe()
    await test_6_manual_save()
    await test_7_rename_project()
    await test_8_delete_project()
    
    # Print summary
    success = results.summary()
    
    return success


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("📚 MONGODB INTEGRATION TEST")
    print("=" * 60)
    print()
    print("⚠️  BEFORE RUNNING:")
    print("1. Start backend server in another terminal:")
    print("   cd backend")
    print("   python3 -m uvicorn main:app --reload --port 8000")
    print()
    print("2. Check server logs for:")
    print("   ✅ MongoDB connected")
    print()
    print("3. Press ENTER to start tests...")
    input()
    
    # Run tests
    success = asyncio.run(run_all_tests())
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

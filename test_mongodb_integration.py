"""
MongoDB Integration Tests
=========================

Run these tests to verify MongoDB integration works correctly.

SETUP FIRST:
1. pip install -r requirements.txt
2. Set MONGODB_URL in .env (or use local MongoDB)
3. Start server: uvicorn main:app --reload

Then run: python3 test_mongodb_integration.py
"""

import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

# Test results tracking
tests_passed = 0
tests_failed = 0
test_results = []


def log_test(name, passed, message=""):
    """Log test result"""
    global tests_passed, tests_failed
    
    status = "✅ PASS" if passed else "❌ FAIL"
    result = {"test": name, "passed": passed, "message": message}
    test_results.append(result)
    
    if passed:
        tests_passed += 1
        print(f"{status} - {name}")
    else:
        tests_failed += 1
        print(f"{status} - {name}: {message}")


async def test_health_check():
    """Test 1: Health check endpoint works"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/health")
            
            if response.status_code == 200:
                data = response.json()
                log_test("Health Check", data.get("status") == "healthy")
            else:
                log_test("Health Check", False, f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Health Check", False, str(e))


async def test_generate_with_mongodb():
    """Test 2: Generate wireframe and check if project_id is returned"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "user_input": "Create a simple login page",
                "device_type": "laptop",
                "use_scraper": False  # Faster for testing
            }
            
            response = await client.post(
                f"{BASE_URL}/generate",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                has_project_id = "project_id" in data and data["project_id"] is not None
                has_wireframe = "wireframe_layout" in data
                
                if has_project_id and has_wireframe:
                    log_test("Generate with MongoDB", True)
                    return data["project_id"]  # Return for next test
                else:
                    log_test("Generate with MongoDB", False, 
                           f"Missing fields: project_id={has_project_id}, wireframe={has_wireframe}")
                    return None
            else:
                log_test("Generate with MongoDB", False, 
                       f"Status: {response.status_code}, Body: {response.text}")
                return None
    except Exception as e:
        log_test("Generate with MongoDB", False, str(e))
        return None


async def test_get_project(project_id):
    """Test 3: Retrieve project by ID"""
    if not project_id:
        log_test("Get Project by ID", False, "No project_id from previous test")
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/projects/{project_id}")
            
            if response.status_code == 200:
                data = response.json()
                has_wireframe = "wireframe" in data
                has_metadata = "name" in data and "created_at" in data
                
                if has_wireframe and has_metadata:
                    log_test("Get Project by ID", True)
                    return True
                else:
                    log_test("Get Project by ID", False, "Missing expected fields")
                    return False
            elif response.status_code == 404:
                log_test("Get Project by ID", False, "Project not found - MongoDB not saving?")
                return False
            else:
                log_test("Get Project by ID", False, f"Status: {response.status_code}")
                return False
    except Exception as e:
        log_test("Get Project by ID", False, str(e))
        return False


async def test_list_projects():
    """Test 4: List all projects"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/projects")
            
            if response.status_code == 200:
                data = response.json()
                is_list = isinstance(data, list)
                
                if is_list and len(data) > 0:
                    # Check first project has expected fields
                    first = data[0]
                    has_fields = "_id" in first and "name" in first and "created_at" in first
                    log_test("List Projects", has_fields)
                elif is_list and len(data) == 0:
                    log_test("List Projects", True, "Empty list (no projects yet)")
                else:
                    log_test("List Projects", False, "Response not a list")
            else:
                log_test("List Projects", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("List Projects", False, str(e))


async def test_rename_project(project_id):
    """Test 5: Rename a project"""
    if not project_id:
        log_test("Rename Project", False, "No project_id available")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            new_name = f"Test Project - {datetime.now().strftime('%H:%M:%S')}"
            response = await client.patch(
                f"{BASE_URL}/projects/{project_id}/rename",
                json={"name": new_name}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("name") == new_name:
                    log_test("Rename Project", True)
                else:
                    log_test("Rename Project", False, "Name not updated")
            else:
                log_test("Rename Project", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("Rename Project", False, str(e))


async def test_manual_save(project_id):
    """Test 6: Manual save endpoint"""
    if not project_id:
        log_test("Manual Save", False, "No project_id available")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            # First get the project
            get_response = await client.get(f"{BASE_URL}/projects/{project_id}")
            if get_response.status_code != 200:
                log_test("Manual Save", False, "Could not fetch project for save test")
                return
            
            project = get_response.json()
            wireframe = project["wireframe"]
            
            # Modify something
            if wireframe.get("components"):
                wireframe["components"][0]["props"]["test_modified"] = True
            
            # Save it
            save_response = await client.post(
                f"{BASE_URL}/projects/{project_id}/save",
                json={
                    "wireframe": wireframe,
                    "instruction": "Test save"
                }
            )
            
            if save_response.status_code == 200:
                log_test("Manual Save", True)
            else:
                log_test("Manual Save", False, f"Status: {save_response.status_code}")
    except Exception as e:
        log_test("Manual Save", False, str(e))


async def test_edit_with_project_id(project_id):
    """Test 7: Edit endpoint updates MongoDB"""
    if not project_id:
        log_test("Edit with Project ID", False, "No project_id available")
        return
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Get current project
            get_response = await client.get(f"{BASE_URL}/projects/{project_id}")
            if get_response.status_code != 200:
                log_test("Edit with Project ID", False, "Could not fetch project")
                return
            
            project = get_response.json()
            
            # Edit it
            edit_response = await client.post(
                f"{BASE_URL}/edit",
                json={
                    "project_id": project_id,
                    "wireframe_layout": project["wireframe"],
                    "instruction": "Add a footer",
                    "use_scraper": False
                }
            )
            
            if edit_response.status_code == 200:
                data = edit_response.json()
                if data.get("project_id") == project_id:
                    log_test("Edit with Project ID", True)
                else:
                    log_test("Edit with Project ID", False, "project_id mismatch")
            else:
                log_test("Edit with Project ID", False, 
                       f"Status: {edit_response.status_code}")
    except Exception as e:
        log_test("Edit with Project ID", False, str(e))


async def test_project_stats():
    """Test 8: Project statistics endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/projects/stats/summary")
            
            if response.status_code == 200:
                data = response.json()
                has_total = "total_projects" in data
                log_test("Project Statistics", has_total)
            else:
                log_test("Project Statistics", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("Project Statistics", False, str(e))


async def test_delete_project(project_id):
    """Test 9: Delete a project"""
    if not project_id:
        log_test("Delete Project", False, "No project_id available")
        return
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{BASE_URL}/projects/{project_id}")
            
            if response.status_code == 200:
                # Verify it's actually deleted
                get_response = await client.get(f"{BASE_URL}/projects/{project_id}")
                if get_response.status_code == 404:
                    log_test("Delete Project", True)
                else:
                    log_test("Delete Project", False, "Project still exists after delete")
            else:
                log_test("Delete Project", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("Delete Project", False, str(e))


async def test_vision_with_mongodb():
    """Test 10: Vision endpoint returns project_id"""
    try:
        # Simple 1x1 white PNG in base64
        test_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "image_base64": test_image,
                "name": "Test Vision Project",
                "device_type": "laptop"
            }
            
            response = await client.post(
                f"{BASE_URL}/vision/analyze",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                has_project_id = "project_id" in data
                log_test("Vision with MongoDB", has_project_id)
            else:
                log_test("Vision with MongoDB", False, 
                       f"Status: {response.status_code}, Body: {response.text}")
    except Exception as e:
        log_test("Vision with MongoDB", False, str(e))


async def run_all_tests():
    """Run all tests in sequence"""
    print("=" * 60)
    print("🧪 MongoDB Integration Test Suite")
    print("=" * 60)
    print(f"Testing server at: {BASE_URL}")
    print()
    
    # Test 1: Health check
    await test_health_check()
    
    # Test 2: Generate and save
    project_id = await test_generate_with_mongodb()
    
    # Test 3: Get project
    await test_get_project(project_id)
    
    # Test 4: List projects
    await test_list_projects()
    
    # Test 5: Rename
    await test_rename_project(project_id)
    
    # Test 6: Manual save
    await test_manual_save(project_id)
    
    # Test 7: Edit with project_id
    await test_edit_with_project_id(project_id)
    
    # Test 8: Stats
    await test_project_stats()
    
    # Test 10: Vision endpoint
    await test_vision_with_mongodb()
    
    # Test 9: Delete (last because it removes the project)
    await test_delete_project(project_id)
    
    # Summary
    print()
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"✅ Passed: {tests_passed}")
    print(f"❌ Failed: {tests_failed}")
    print(f"📈 Success Rate: {tests_passed}/{tests_passed + tests_failed} ({100 * tests_passed / (tests_passed + tests_failed) if (tests_passed + tests_failed) > 0 else 0:.1f}%)")
    print("=" * 60)
    
    if tests_failed > 0:
        print("\n⚠️  Some tests failed. Check:")
        print("1. Is the server running? (uvicorn main:app --reload)")
        print("2. Is MongoDB connected? (check startup logs)")
        print("3. Is MONGODB_URL set in .env?")
    else:
        print("\n🎉 All tests passed! MongoDB integration is working perfectly.")
    
    return tests_failed == 0


if __name__ == "__main__":
    print("\n⏳ Starting tests...\n")
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)

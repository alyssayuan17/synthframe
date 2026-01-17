
import os
# Set MOCK_LLM to 1 to avoid needing API keys for tests
os.environ["MOCK_LLM"] = "1"

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

print("=" * 60)
print("🚀 API ROUTE INTEGRATION TESTS")
print("=" * 60)

# 1. Health Check
print("\n🏥 1. Testing /health")
response = client.get("/health")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Status: {data['status']}")
    print(f"✅ Version: {data['version']}")
else:
    print(f"❌ Failed: {response.text}")

# 2. Scrape
print("\n🔍 2. Testing /scrape")
payload = {"query": "SaaS dashboard", "max_pages": 1}
response = client.post("/scrape", json=payload)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Success: {data['success']}")
    print(f"✅ Context length: {len(data['context'])} chars")
else:
    print(f"❌ Failed: {response.status_code} - {response.text}")

# 3. Generate (Text-to-Wireframe)
print("\n🤖 3. Testing /generate")
payload = {
    "user_input": "Create a login page",
    "use_scraper": False  # Skip scraper to make test faster
}
response = client.post("/generate", json=payload)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Success: {data['success']}")
    if data['success']:
        print(f"✅ Wireframe ID: {data['wireframe_layout']['id']}")
        print(f"✅ Component count: {len(data['wireframe_layout']['components'])}")
else:
    print(f"❌ Failed: {response.status_code} - {response.text}")

# 4. Edit (Stub/Mock)
print("\n✏️ 4. Testing /edit")
# Need a valid layout first. Let's use the one from generate if successful, or a dummy one.
dummy_layout = {
    "id": "test-layout",
    "name": "Test",
    "source_type": "prompt",
    "components": [],
    "canvas_size": {"width": 100, "height": 100}
}
# If generation worked, use that layout structure (though specific content might mock)
if response.status_code == 200:
    dummy_layout = response.json()['wireframe_layout']

payload = {
    "wireframe_layout": dummy_layout,
    "instruction": "Make the background dark",
    "use_scraper": False
}
response = client.post("/edit", json=payload)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Success: {data['success']}")
    print(f"✅ Message: {data['message']}")
else:
    print(f"❌ Failed: {response.status_code} - {response.text}")

# 5. Vision (Status check only since we don't have an image easily)
print("\n👁️ 5. Testing /vision/status")
response = client.get("/vision/status")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Available: {data['available']}")
    print(f"✅ Deps: {data['dependencies']}")
else:
    # It's possible the route might be 404 if not registered correctly or logic differs
    # But we implemented /vision/status in the previous turn
    print(f"❌ Failed: {response.status_code} - {response.text}")

# 6. Critique (Stub)
print("\n⚖️ 6. Testing /critique")
payload = {
    "wireframe_id": "wf_123", 
    "focus_areas": ["spacing"]
}
response = client.post("/critique", json=payload)
if response.status_code == 200:
    data = response.json()
    print(f"✅ Success: {data['success']}")
    print(f"✅ Score: {data['overall_score']}")
else:
    print(f"❌ Failed: {response.status_code} - {response.text}")

print("\n" + "=" * 60)
print("🎉 TESTS COMPLETE")
print("=" * 60)

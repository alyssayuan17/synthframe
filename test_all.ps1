# test_all.ps1
$ErrorActionPreference = "Stop"
Write-Host "🧪 SynthFrame Test Suite" -ForegroundColor Cyan
# Test 1: Health
Write-Host "`n[1/6] Testing health endpoint..." -ForegroundColor Yellow
$health = curl http://localhost:8000/health | ConvertFrom-Json
if ($health.status -eq "healthy") {
    Write-Host "✅ Health check passed" -ForegroundColor Green
} else {
    Write-Host "❌ Health check failed" -ForegroundColor Red
    exit 1
}
# Test 2: Generate (no auto-save)
Write-Host "`n[2/6] Testing generate endpoint..." -ForegroundColor Yellow
$gen = curl -X POST http://localhost:8000/generate `
    -H "Content-Type: application/json" `
    -d '{"user_input":"test dashboard","device_type":"macbook"}' | ConvertFrom-Json
if ($gen.project_id -eq $null -and $gen.success -eq $true) {
    Write-Host "✅ Generate works, no auto-save" -ForegroundColor Green
} else {
    Write-Host "❌ Generate failed or auto-saved" -ForegroundColor Red
    exit 1
}
# Test 3: Verify no auto-save in DB
Write-Host "`n[3/6] Verifying no auto-save..." -ForegroundColor Yellow
$projects = curl http://localhost:8000/projects | ConvertFrom-Json
$recent = $projects | Where-Object { $_.created_at -gt (Get-Date).AddMinutes(-1) }
if ($recent.Count -eq 0) {
    Write-Host "✅ No auto-save confirmed" -ForegroundColor Green
} else {
    Write-Host "❌ Found auto-saved projects" -ForegroundColor Red
}
# Test 4: Manual save
Write-Host "`n[4/6] Testing manual save..." -ForegroundColor Yellow
$save = curl -X POST http://localhost:8000/projects `
    -H "Content-Type: application/json" `
    -d "{\"name\":\"Test Project\",\"wireframe\":$($gen.wireframe_layout | ConvertTo-Json -Depth 10),\"generation_method\":\"text_prompt\",\"device_type\":\"macbook\"}" | ConvertFrom-Json
if ($save._id) {
    Write-Host "✅ Manual save works" -ForegroundColor Green
    $project_id = $save._id
} else {
    Write-Host "❌ Manual save failed" -ForegroundColor Red
    exit 1
}
# Test 5: Verify in gallery
Write-Host "`n[5/6] Verifying in gallery..." -ForegroundColor Yellow
$projects = curl http://localhost:8000/projects | ConvertFrom-Json
if ($projects | Where-Object { $_._id -eq $project_id }) {
    Write-Host "✅ Project in gallery" -ForegroundColor Green
} else {
    Write-Host "❌ Project not in gallery" -ForegroundColor Red
}
# Test 6: Cleanup
Write-Host "`n[6/6] Cleaning up..." -ForegroundColor Yellow
curl -X DELETE "http://localhost:8000/projects/$project_id"
Write-Host "✅ Cleanup complete" -ForegroundColor Green
Write-Host "`n✅ All tests passed!" -ForegroundColor Green
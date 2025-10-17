# Dialogue TTS Editor - Start Script
# Encoding: UTF-8

Write-Host "Starting Dialogue TTS Editor..." -ForegroundColor Cyan

# Check if in correct directory
if (-not (Test-Path "app.py")) {
    Write-Host "ERROR: Please run this script in dialogue_editor directory" -ForegroundColor Red
    exit 1
}

# Check .env file
if (-not (Test-Path "../.env")) {
    Write-Host "WARNING: .env file not found" -ForegroundColor Yellow
    Write-Host "Please copy .env.template to parent directory and rename to .env" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Continue anyway? (y/n)"
    if ($response -ne "y") {
        exit 0
    }
}

# Check Python dependencies
Write-Host "Checking dependencies..." -ForegroundColor Cyan
$packages = @("fastapi", "uvicorn", "pydantic")
$missing = @()

foreach ($pkg in $packages) {
    python -c "import $pkg" 2>$null
    if ($LASTEXITCODE -ne 0) {
        $missing += $pkg
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Missing dependencies: $($missing -join ', ')" -ForegroundColor Yellow
    Write-Host "Installing..." -ForegroundColor Cyan
    pip install -r requirements.txt
}

# Check FFmpeg
Write-Host "Checking FFmpeg..." -ForegroundColor Cyan
$ffmpegExists = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpegExists) {
    Write-Host "WARNING: FFmpeg not found, audio merging will not work" -ForegroundColor Yellow
    Write-Host "Please download from https://ffmpeg.org" -ForegroundColor Yellow
}

# Create necessary directories
Write-Host "Creating directories..." -ForegroundColor Cyan
$dirs = @("projects", "dialogue_output", "static")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Service URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Documentation: README.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start service
python app.py

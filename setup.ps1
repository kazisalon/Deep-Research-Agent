# Setup script for Deep Research Agent
# Run this after creating your .env file with API keys

Write-Host "🚀 Deep Research Agent - Setup Script" -ForegroundColor Cyan
Write-Host "======================================`n" -ForegroundColor Cyan

# Check Python version
Write-Host "📌 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "   $pythonVersion" -ForegroundColor Gray

if ($pythonVersion -match "Python 3\.([0-9]+)") {
    $minorVersion = [int]$matches[1]
    if ($minorVersion -lt 10) {
        Write-Host "   ⚠️  WARNING: Python 3.10+ recommended. You have an older version." -ForegroundColor Red
        Write-Host "   Consider upgrading to Python 3.11 or 3.12 for best compatibility.`n" -ForegroundColor Red
    } else {
        Write-Host "   ✅ Python version OK`n" -ForegroundColor Green
    }
}

# Check if .env exists
Write-Host "📌 Checking environment file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✅ .env file found`n" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "   ✅ Created .env file. Please edit it and add your API keys!`n" -ForegroundColor Green
}

# Install dependencies
Write-Host "📌 Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env and add your API keys" -ForegroundColor White
Write-Host "2. Run: python main.py`n" -ForegroundColor White

# AI Call Summarization System Startup Script
# PowerShell script for Windows

Write-Host "🎙️ AI Call Summarization System" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  No .env file found" -ForegroundColor Yellow
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "🔑 IMPORTANT: Please edit .env and add your OpenAI API key!" -ForegroundColor Red
    Write-Host "   Open .env file and replace 'your_openai_api_key_here' with your actual key" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter after updating your API key to continue"
}

# Check if Docker is running
Write-Host "🐳 Checking Docker..." -ForegroundColor Blue
try {
    docker version | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Build and start the system
Write-Host ""
Write-Host "🚀 Building and starting the AI Call Summarization system..." -ForegroundColor Blue
Write-Host ""

try {
    # Build images
    Write-Host "📦 Building Docker images..." -ForegroundColor Yellow
    docker-compose build

    # Start services
    Write-Host "🔄 Starting services..." -ForegroundColor Yellow
    docker-compose up -d

    # Wait for services to be healthy
    Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10

    # Check service status
    Write-Host ""
    Write-Host "📊 Service Status:" -ForegroundColor Green
    docker-compose ps

    Write-Host ""
    Write-Host "🎉 System is starting up!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 Access Points:" -ForegroundColor Cyan
    Write-Host "   Frontend (Streamlit): http://localhost:8501" -ForegroundColor White
    Write-Host "   Backend API:          http://localhost:8000" -ForegroundColor White
    Write-Host "   API Documentation:    http://localhost:8000/docs" -ForegroundColor White
    Write-Host "   MongoDB:              localhost:27017" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 To stop the system: docker-compose down" -ForegroundColor Yellow
    Write-Host "💡 To view logs: docker-compose logs -f" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opening frontend in browser..." -ForegroundColor Blue
    Start-Process "http://localhost:8501"

} catch {
    Write-Host "❌ Error starting system: $_" -ForegroundColor Red
    Write-Host "💡 Try: docker-compose down && docker-compose up -d" -ForegroundColor Yellow
    exit 1
}

"""
CallGist - Zimbabwe Call Center Hackathon Main Application
Production-ready FastAPI app with unified endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

# Import hackathon-specific modules
from app.api.hackathon_endpoints import router as hackathon_router
from app.services.hackathon_database import HackathonDatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global database manager
db_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global db_manager
    
    # Startup
    logger.info("🎯 Starting CallGist - Zimbabwe Call Center Hackathon System")
    
    try:
        # Initialize database connection
        db_manager = HackathonDatabaseManager()
        await db_manager.connect()
        logger.info("✅ Database connected successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    finally:
        # Shutdown
        if db_manager:
            await db_manager.disconnect()
        logger.info("🔄 CallGist shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="CallGist - Zimbabwe Call Center AI",
    description="""
    🎯 **CallGist** - AI-Powered Call Intelligence for Zimbabwe Call Centers
    
    ## Features
    - **Instant Audio Processing**: Upload .mp3/.wav/.webm files for immediate AI analysis
    - **Zimbabwe-Specific Categories**: Billing, Technical, Bundles, Complaints, General Inquiries
    - **Actionable Insights**: Sentiment analysis, action items, customer requests, priority assessment
    - **Advanced Search**: Filter by category, sentiment, date, tags, resolution status
    - **Call Center Analytics**: Performance metrics, resolution rates, agent assessments
    - **Monetizable APIs**: Usage tracking and billing statistics
    
    ## Perfect for
    - Call center quality assurance
    - Customer service optimization
    - Agent performance monitoring
    - Compliance and reporting
    - Customer satisfaction tracking
    
    Built for API monetization hackathon - Zimbabwe call center market.
    """,
    version="1.0.0",
    contact={
        "name": "CallGist Team",
        "email": "support@callgist.co.zw"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include hackathon API routes
app.include_router(hackathon_router)

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "🎯 CallGist - Zimbabwe Call Center AI",
        "version": "1.0.0",
        "description": "AI-powered call intelligence for Zimbabwe call centers",
        "features": [
            "Instant audio transcription with OpenAI Whisper",
            "GPT-4o analysis for Zimbabwe call center scenarios", 
            "Category classification (billing/technical/bundles/complaints)",
            "Sentiment analysis and priority assessment",
            "Actionable insights and agent performance evaluation",
            "Advanced search and analytics dashboard",
            "Monetizable API endpoints with usage tracking"
        ],
        "endpoints": {
            "upload": "/api/v1/upload",
            "transcript": "/api/v1/call/{id}/transcript", 
            "summary": "/api/v1/call/{id}/summary",
            "search": "/api/v1/calls/search",
            "analytics": "/api/v1/analytics/dashboard",
            "documentation": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global db_manager
    
    if not db_manager:
        raise HTTPException(status_code=503, detail="Database not initialized")
    
    db_healthy = await db_manager.health_check()
    
    if not db_healthy:
        raise HTTPException(status_code=503, detail="Database unhealthy")
    
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0",
        "timestamp": "2025-07-02T20:45:00Z"
    }

@app.get("/status")
async def system_status():
    """Detailed system status for monitoring"""
    global db_manager
    
    return {
        "system": "CallGist Zimbabwe Call Center AI",
        "status": "operational",
        "components": {
            "api": "healthy",
            "database": "connected" if db_manager and await db_manager.health_check() else "disconnected",
            "ai_service": "ready",
            "audio_processor": "ready"
        },
        "capabilities": {
            "audio_formats": [".mp3", ".wav", ".webm", ".m4a", ".opus"],
            "languages": ["en"],
            "ai_models": ["whisper-1", "gpt-4o"],
            "categories": ["billing", "technical", "bundles", "complaints", "general_inquiry"],
            "sentiments": ["positive", "neutral", "negative"]
        },
        "limits": {
            "max_file_size_mb": 25,
            "max_duration_minutes": 30,
            "concurrent_processing": 10
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "hackathon_main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development",
        log_level="info"
    )

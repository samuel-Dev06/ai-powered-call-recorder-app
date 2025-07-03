"""
CallGist - Zimbabwe Call Center Hackathon API Endpoints
Production-ready, monetizable endpoints for call analysis
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta
import os
import uuid
import asyncio
from pathlib import Path

from app.models.hackathon_models import (
    CallRecord, UploadAudioRequest, UploadAudioResponse, 
    CallListResponse, CallSearchRequest, APIUsageStats,
    CallCategory, SentimentType, Priority, ResolutionStatus, CallStatus
)
from app.services.hackathon_database import HackathonDatabaseManager
from app.services.ai_service import AIService
from app.services.audio_processor import AudioProcessor

router = APIRouter(prefix="/api/v1", tags=["CallGist Zimbabwe API"])


# Dependency injection
async def get_services():
    return {
        "db": HackathonDatabaseManager(),
        "ai": AIService(api_key=os.getenv("OPENAI_API_KEY")),
        "audio": AudioProcessor()
    }


@router.post("/upload", response_model=UploadAudioResponse)
async def upload_call_audio(
    audio_file: UploadFile = File(..., description="Audio file (.mp3, .wav, .webm)"),
    services: dict = Depends(get_services)
):
    """
    🎯 MONETIZABLE ENDPOINT: Upload customer call audio for AI analysis
    
    Immediately processes uploaded audio and returns actionable insights for
    Zimbabwe call centers including sentiment, categorization, and action items.
    """
    try:
        # Validate audio file
        allowed_formats = ['.mp3', '.wav', '.webm', '.m4a', '.opus']
        file_ext = Path(audio_file.filename).suffix.lower()
        
        if file_ext not in allowed_formats:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported audio format. Allowed: {', '.join(allowed_formats)}"
            )
        
        # Generate unique call ID
        call_id = f"call_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{call_id}_{timestamp}_{audio_file.filename}"
        
        # Save audio file
        upload_dir = Path("/tmp/callgist_uploads")
        upload_dir.mkdir(exist_ok=True)
        audio_path = upload_dir / safe_filename
        
        with open(audio_path, "wb") as buffer:
            content = await audio_file.read()
            buffer.write(content)
        
        # Create call record in MongoDB
        call_record = CallRecord(
            call_id=call_id,
            audio_file_path=str(audio_path),
            audio_filename=audio_file.filename,
            status=CallStatus.PROCESSING,
            processing_metadata={
                "upload_size_bytes": len(content),
                "upload_timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Insert into database
        await services["db"].create_call_record(call_record)
        
        # Start background processing
        asyncio.create_task(process_call_async(call_id, str(audio_path), services))
        
        return UploadAudioResponse(
            call_id=call_id,
            status="processing",
            message="Audio uploaded successfully. Processing started.",
            processing_url=f"/api/v1/call/{call_id}/status"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/call/{call_id}/transcript")
async def get_call_transcript(
    call_id: str,
    services: dict = Depends(get_services)
):
    """
    🎯 MONETIZABLE ENDPOINT: Get full transcript of processed call
    """
    call_record = await services["db"].get_call_record(call_id)
    if not call_record:
        raise HTTPException(status_code=404, detail="Call not found")
    
    if not call_record.transcript:
        raise HTTPException(status_code=202, detail="Transcript not ready yet")
    
    return {
        "call_id": call_id,
        "transcript": call_record.transcript,
        "audio_duration": call_record.audio_duration,
        "processed_at": call_record.processed_at
    }


@router.get("/call/{call_id}/summary")
async def get_call_summary(
    call_id: str,
    services: dict = Depends(get_services)
):
    """
    🎯 MONETIZABLE ENDPOINT: Get AI-generated summary and insights
    
    Returns comprehensive Zimbabwe call center insights including:
    - 3-bullet summary
    - Sentiment analysis
    - Call categorization (billing/technical/bundles/complaints)
    - Action items for agents
    - Customer requests
    - Priority and resolution status
    """
    call_record = await services["db"].get_call_record(call_id)
    if not call_record:
        raise HTTPException(status_code=404, detail="Call not found")
    
    if call_record.status == CallStatus.PROCESSING:
        raise HTTPException(status_code=202, detail="Processing in progress")
    
    if call_record.status == CallStatus.FAILED:
        raise HTTPException(status_code=500, detail="Processing failed")
    
    return {
        "call_id": call_id,
        "summary": call_record.summary,
        "sentiment": call_record.sentiment,
        "category": call_record.category,
        "action_items": call_record.action_items,
        "customer_requests": call_record.customer_requests,
        "resolution_status": call_record.resolution_status,
        "priority": call_record.priority,
        "tags": call_record.tags,
        "agent_performance": call_record.agent_performance,
        "follow_up_required": call_record.follow_up_required,
        "processed_at": call_record.processed_at
    }


@router.get("/call/{call_id}/status")
async def get_call_status(
    call_id: str,
    services: dict = Depends(get_services)
):
    """
    🎯 ENDPOINT: Check processing status of uploaded call
    """
    call_record = await services["db"].get_call_record(call_id)
    if not call_record:
        raise HTTPException(status_code=404, detail="Call not found")
    
    return {
        "call_id": call_id,
        "status": call_record.status,
        "upload_timestamp": call_record.upload_timestamp,
        "processed_at": call_record.processed_at,
        "progress": "completed" if call_record.status == CallStatus.COMPLETED else "processing"
    }


@router.post("/calls/search", response_model=CallListResponse)
async def search_calls(
    search_request: CallSearchRequest,
    services: dict = Depends(get_services)
):
    """
    🎯 MONETIZABLE ENDPOINT: Search and filter calls for Zimbabwe call centers
    
    Advanced search capabilities:
    - Filter by category (billing/technical/bundles/complaints)
    - Filter by sentiment (positive/neutral/negative)
    - Filter by priority and resolution status
    - Date range filtering
    - Tag-based search
    - Full-text search in transcripts and summaries
    """
    calls, total = await services["db"].search_call_records(search_request)
    
    return CallListResponse(
        calls=calls,
        total=total,
        page=search_request.page,
        per_page=search_request.per_page
    )


@router.get("/calls", response_model=CallListResponse)
async def list_calls(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    category: Optional[CallCategory] = Query(None, description="Filter by call category"),
    sentiment: Optional[SentimentType] = Query(None, description="Filter by sentiment"),
    services: dict = Depends(get_services)
):
    """
    🎯 MONETIZABLE ENDPOINT: List all processed calls with pagination
    """
    search_request = CallSearchRequest(
        page=page,
        per_page=per_page,
        category=category,
        sentiment=sentiment
    )
    
    calls, total = await services["db"].search_call_records(search_request)
    
    return CallListResponse(
        calls=calls,
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/analytics/dashboard")
async def get_analytics_dashboard(
    days: int = Query(30, description="Number of days to analyze"),
    services: dict = Depends(get_services)
):
    """
    🎯 MONETIZABLE ENDPOINT: Call center analytics dashboard
    
    Provides actionable insights for Zimbabwe call center management:
    - Call volume trends
    - Category distribution (billing vs technical vs bundles)
    - Sentiment analysis trends
    - Agent performance metrics
    - Resolution rate statistics
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    analytics = await services["db"].get_dashboard_analytics(start_date, end_date)
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        "metrics": analytics,
        "insights": {
            "top_categories": analytics.get("category_breakdown", {}),
            "sentiment_distribution": analytics.get("sentiment_breakdown", {}),
            "resolution_rate": analytics.get("resolution_rate", 0),
            "average_priority": analytics.get("average_priority", "medium"),
            "follow_up_rate": analytics.get("follow_up_rate", 0)
        }
    }


@router.get("/analytics/usage", response_model=APIUsageStats)
async def get_api_usage_stats(
    days: int = Query(30, description="Number of days to analyze"),
    services: dict = Depends(get_services)
):
    """
    🎯 MONETIZATION ENDPOINT: API usage statistics for billing
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    usage_stats = await services["db"].get_api_usage_stats(start_date, end_date)
    
    return usage_stats


# Background processing function
async def process_call_async(call_id: str, audio_path: str, services: dict):
    """
    Background task to process uploaded call audio
    """
    try:
        # Step 1: Audio processing and transcription
        processed_audio = await services["audio"].process_audio_file(audio_path)
        transcript = await services["ai"].transcribe_audio(processed_audio["enhanced_path"])
        
        # Step 2: AI analysis with Zimbabwe call center prompts
        insights = await services["ai"].generate_summary_from_text(transcript, is_final=True)
        
        # Step 3: Update call record with results
        await services["db"].update_call_record(call_id, {
            "transcript": transcript,
            "audio_duration": processed_audio.get("duration", 0),
            "summary": insights.get("summary", []),
            "sentiment": insights.get("sentiment"),
            "category": insights.get("category"),
            "action_items": insights.get("action_items", []),
            "customer_requests": insights.get("customer_requests", []),
            "resolution_status": insights.get("resolution_status"),
            "priority": insights.get("priority"),
            "tags": insights.get("tags", []),
            "agent_performance": insights.get("agent_performance"),
            "follow_up_required": insights.get("follow_up_required", False),
            "status": CallStatus.COMPLETED,
            "processed_at": datetime.utcnow(),
            "processing_metadata": {
                "transcription_time": processed_audio.get("processing_time", 0),
                "ai_analysis_completed": True
            }
        })
        
    except Exception as e:
        # Mark as failed
        await services["db"].update_call_record(call_id, {
            "status": CallStatus.FAILED,
            "processing_metadata": {
                "error": str(e),
                "failed_at": datetime.utcnow().isoformat()
            }
        })
        raise

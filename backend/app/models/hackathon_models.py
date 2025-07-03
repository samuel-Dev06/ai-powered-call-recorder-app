"""
CallGist - Zimbabwe Call Center Hackathon Models
Unified "calls" collection with all insights, monetizable API structure
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from bson import ObjectId


class CallStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class CallCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    BUNDLES = "bundles"
    COMPLAINTS = "complaints"
    GENERAL_INQUIRY = "general_inquiry"
    OTHER = "other"


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium" 
    LOW = "low"


class ResolutionStatus(str, Enum):
    RESOLVED = "resolved"
    PENDING = "pending"
    ESCALATED = "escalated"


# Unified Call Model - Single "calls" collection for hackathon
class CallRecord(BaseModel):
    """
    Unified call record containing all insights for Zimbabwe call centers.
    Single MongoDB collection: 'calls'
    """
    id: Optional[str] = Field(default=None, alias="_id")
    
    # Basic Call Info
    call_id: str = Field(..., description="Unique call identifier")
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)
    audio_file_path: str = Field(..., description="Path to uploaded audio file")
    audio_filename: str = Field(..., description="Original filename")
    audio_duration: Optional[float] = Field(None, description="Duration in seconds")
    
    # Processing Status
    status: CallStatus = CallStatus.PROCESSING
    processed_at: Optional[datetime] = None
    
    # Transcription
    transcript: Optional[str] = Field(None, description="Full call transcript")
    
    # AI-Generated Zimbabwe Call Center Insights
    summary: Optional[List[str]] = Field(None, description="3-bullet summary of key points")
    sentiment: Optional[SentimentType] = Field(None, description="Overall call sentiment")
    category: Optional[CallCategory] = Field(None, description="Call type classification")
    action_items: Optional[List[str]] = Field(None, description="Required follow-up actions")
    customer_requests: Optional[List[str]] = Field(None, description="What customer asked for")
    resolution_status: Optional[ResolutionStatus] = Field(None, description="Call resolution state")
    priority: Optional[Priority] = Field(None, description="Call priority level")
    tags: Optional[List[str]] = Field(default_factory=list, description="Searchable tags")
    agent_performance: Optional[str] = Field(None, description="Agent performance assessment")
    follow_up_required: Optional[bool] = Field(None, description="Whether callback needed")
    
    # Metadata for Call Center Operations
    user_metadata: Dict[str, Any] = Field(default_factory=dict, description="User upload metadata")
    processing_metadata: Dict[str, Any] = Field(default_factory=dict, description="System processing info")
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "call_id": "call_20250702_001",
                "audio_filename": "customer_call.wav",
                "audio_file_path": "/uploads/call_20250702_001.wav",
                "transcript": "Agent: Good morning, how can I help you today? Customer: Hi, I'm having issues with my data bundle...",
                "summary": [
                    "Customer reported data bundle not working properly",
                    "Agent provided troubleshooting steps and reset account",
                    "Issue resolved, customer satisfied with service"
                ],
                "sentiment": "positive",
                "category": "bundles", 
                "action_items": ["Monitor data bundle activation system", "Follow up with customer in 24h"],
                "customer_requests": ["Fix data bundle", "Extend validity period"],
                "resolution_status": "resolved",
                "priority": "medium",
                "tags": ["data_bundle", "technical_issue", "resolved", "harare"],
                "agent_performance": "Excellent - resolved issue quickly and professionally",
                "follow_up_required": True
            }
        }


# API Request/Response Models for Hackathon
class UploadAudioRequest(BaseModel):
    """Request model for audio upload"""
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class UploadAudioResponse(BaseModel):
    """Response model for audio upload"""
    call_id: str
    status: str
    message: str
    processing_url: str


class CallListResponse(BaseModel):
    """Response model for call listing"""
    calls: List[CallRecord]
    total: int
    page: int
    per_page: int


class CallSearchRequest(BaseModel):
    """Request model for call search/filtering"""
    category: Optional[CallCategory] = None
    sentiment: Optional[SentimentType] = None
    priority: Optional[Priority] = None
    resolution_status: Optional[ResolutionStatus] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    tags: Optional[List[str]] = None
    search_text: Optional[str] = None
    page: int = 1
    per_page: int = 20


# Monetization Models
class APIUsageStats(BaseModel):
    """API usage statistics for monetization"""
    total_calls_processed: int
    calls_by_category: Dict[CallCategory, int]
    calls_by_sentiment: Dict[SentimentType, int]
    average_processing_time: float
    success_rate: float
    date_range: Dict[str, datetime]


class MonetizationMetrics(BaseModel):
    """Metrics for API monetization"""
    api_calls_count: int
    processing_minutes: float
    storage_mb: float
    premium_features_used: List[str]
    billing_period: Dict[str, datetime]

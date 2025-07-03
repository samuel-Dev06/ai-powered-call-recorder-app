from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
from bson import ObjectId


class CallStatus(str, Enum):
    ACTIVE = "active"
    ENDED = "ended"
    PROCESSING = "processing"


class SpeakerType(str, Enum):
    AGENT = "agent"
    CUSTOMER = "customer"
    UNKNOWN = "unknown"


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class DialogTurn(BaseModel):
    timestamp: datetime
    speaker: SpeakerType
    text: str
    confidence: float = 0.0
    sentiment: Optional[SentimentType] = None
    duration: Optional[float] = None  # in seconds


class CallSession(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: CallStatus = CallStatus.ACTIVE
    dialog_turns: List[DialogTurn] = []
    audio_file_path: Optional[str] = None
    metadata: Dict[str, Any] = {}
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class CallSummary(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    call_session_id: str
    summary_text: str
    key_points: List[str] = []
    sentiment_analysis: Dict[str, Any] = {}
    talk_time_stats: Dict[str, float] = {}  # agent_talk_time, customer_talk_time
    created_at: datetime
    is_final: bool = False
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class CallAnalytics(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    call_session_id: str
    total_duration: float
    agent_talk_time: float
    customer_talk_time: float
    silence_time: float
    interruptions_count: int
    overall_sentiment: SentimentType
    sentiment_scores: Dict[str, float]
    word_count: int
    topics: List[str] = []
    created_at: datetime
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# Request/Response models for API
class StartCallRequest(BaseModel):
    session_id: str
    metadata: Optional[Dict[str, Any]] = {}


class StartCallResponse(BaseModel):
    call_id: str
    session_id: str
    status: str
    message: str


class EndCallRequest(BaseModel):
    generate_summary: bool = True


class TranscriptUpdate(BaseModel):
    session_id: str
    timestamp: datetime
    speaker: SpeakerType
    text: str
    confidence: float
    is_final: bool = False


class SummaryUpdate(BaseModel):
    session_id: str
    summary_text: str
    key_points: List[str]
    is_final: bool = False
    sentiment_analysis: Optional[Dict[str, Any]] = None

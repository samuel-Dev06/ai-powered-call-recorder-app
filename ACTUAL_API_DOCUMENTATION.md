# AI Call Summarization API Documentation
## Based on Current Implementation

## Overview
The AI Call Summarization API provides intelligent analysis of customer service calls for Zimbabwe call centers. It uses advanced AI models to transcribe audio, analyze sentiment, categorize calls, and extract actionable insights.

**Base URL:** `http://localhost:8000`
**API Version:** v1
**Prefix:** `/api/v1`

---

## Actual Implemented Endpoints

### 1. Upload Call Audio
**POST** `/api/v1/upload`

Upload an audio file for AI analysis and transcription.

#### Request
- **Content-Type:** `multipart/form-data`
- **Parameters:**
  - `audio_file` (file, required): Audio file (.mp3, .wav, .webm, .m4a, .opus)

#### Response
```json
{
  "call_id": "call_5c20fc3b2de5",
  "status": "processing",
  "message": "Audio uploaded successfully. Processing started.",
  "processing_url": "/api/v1/call/call_5c20fc3b2de5/status"
}
```

#### Implementation Details
- Validates audio file format against allowed formats
- Generates unique call ID using UUID
- Saves file to `/tmp/callgist_uploads/`
- Creates CallRecord in MongoDB with PROCESSING status
- Starts background processing task

---

### 2. Get Call Status
**GET** `/api/v1/call/{call_id}/status`

Check the processing status of an uploaded call.

#### Parameters
- `call_id` (string, required): Unique call identifier

#### Response
```json
{
  "call_id": "call_5c20fc3b2de5",
  "status": "completed",
  "upload_timestamp": "2025-07-03T09:24:16.123Z",
  "processed_at": "2025-07-03T09:25:45.678Z",
  "progress": "completed"
}
```

#### Status Values (from CallStatus enum)
- `processing`: Audio is being transcribed and analyzed
- `completed`: Analysis finished successfully
- `failed`: Processing encountered an error

---

### 3. Get Call Transcript
**GET** `/api/v1/call/{call_id}/transcript`

Retrieve the transcribed text from the audio file.

#### Parameters
- `call_id` (string, required): Unique call identifier

#### Response
```json
{
  "call_id": "call_5c20fc3b2de5",
  "transcript": "Good afternoon, thank you for calling EcoCash support, my name is Fadzai, how can I help you today?...",
  "audio_duration": 45.2,
  "processed_at": "2025-07-03T09:25:45.678Z"
}
```

#### Error Responses
- **404**: Call not found
- **202**: Transcript not ready yet (still processing)

---

### 4. Get Call Summary & Analysis
**GET** `/api/v1/call/{call_id}/summary`

Get comprehensive AI analysis of the call including sentiment, categorization, and actionable insights.

#### Parameters
- `call_id` (string, required): Unique call identifier

#### Response (Based on Actual CallRecord Model)
```json
{
  "call_id": "call_5c20fc3b2de5",
  "summary": [
    "Customer experienced airtime purchase issue with EcoCash",
    "Agent efficiently resolved the issue by crediting airtime",
    "Customer confirmed satisfaction with resolution"
  ],
  "sentiment": "positive",
  "category": "billing",
  "action_items": [
    "Investigate why airtime did not post to mobile operator system",
    "Update system to prevent future occurrences"
  ],
  "customer_requests": [
    "Receive purchased airtime",
    "Resolution of airtime deduction issue"
  ],
  "resolution_status": "resolved",
  "priority": "medium",
  "tags": [
    "airtime_purchase",
    "credit_issue",
    "resolved"
  ],
  "agent_performance": "Efficient - resolved the issue promptly and credited airtime",
  "follow_up_required": false,
  "processed_at": "2025-07-03T09:25:45.678Z"
}
```

#### Error Responses
- **404**: Call not found
- **202**: Processing in progress
- **500**: Processing failed

---

### 5. Search Calls
**POST** `/api/v1/calls/search`

Search and filter calls based on various criteria.

#### Request Body (CallSearchRequest Model)
```json
{
  "category": "billing",
  "sentiment": "positive",
  "priority": "medium",
  "resolution_status": "resolved",
  "date_from": "2025-07-01T00:00:00Z",
  "date_to": "2025-07-03T23:59:59Z",
  "tags": ["airtime", "payment"],
  "search_text": "EcoCash",
  "page": 1,
  "per_page": 20
}
```

#### Response (CallListResponse Model)
```json
{
  "calls": [
    {
      "call_id": "call_5c20fc3b2de5",
      "upload_timestamp": "2025-07-03T09:24:16.123Z",
      "audio_filename": "customer_call.mp3",
      "audio_duration": 45.2,
      "status": "completed",
      "summary": ["Customer experienced airtime purchase issue..."],
      "sentiment": "positive",
      "category": "billing",
      "priority": "medium",
      "resolution_status": "resolved",
      "tags": ["airtime_purchase", "credit_issue", "resolved"],
      "processed_at": "2025-07-03T09:25:45.678Z"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20
}
```

---

### 6. List Calls
**GET** `/api/v1/calls`

Get a list of calls with optional filtering and pagination.

#### Query Parameters
- `page` (integer, optional): Page number (default: 1, min: 1)
- `per_page` (integer, optional): Items per page (default: 20, min: 1, max: 100)
- `category` (CallCategory, optional): Filter by category
- `sentiment` (SentimentType, optional): Filter by sentiment

#### Response
Same as search calls response (CallListResponse model)

---

### 7. Analytics Dashboard
**GET** `/api/v1/analytics/dashboard`

Get comprehensive analytics for call center performance.

#### Query Parameters
- `days` (integer, optional): Number of days to analyze (default: 30)

#### Response
```json
{
  "period": {
    "start_date": "2025-06-03T09:24:16.123Z",
    "end_date": "2025-07-03T09:24:16.123Z",
    "days": 30
  },
  "metrics": {
    "total_calls": 150,
    "category_breakdown": {
      "billing": 60,
      "technical": 40,
      "bundles": 25,
      "complaints": 15,
      "general_inquiry": 10
    },
    "sentiment_breakdown": {
      "positive": 85,
      "neutral": 45,
      "negative": 20
    },
    "resolution_rate": 0.85,
    "average_priority": "medium",
    "follow_up_rate": 0.15
  },
  "insights": {
    "top_categories": {
      "billing": 60,
      "technical": 40
    },
    "sentiment_distribution": {
      "positive": 85,
      "neutral": 45,
      "negative": 20
    },
    "resolution_rate": 0.85,
    "average_priority": "medium",
    "follow_up_rate": 0.15
  }
}
```

---

### 8. API Usage Statistics
**GET** `/api/v1/analytics/usage`

Get API usage statistics and metrics.

#### Query Parameters
- `days` (integer, optional): Number of days to analyze (default: 30)

#### Response (APIUsageStats Model)
```json
{
  "total_calls_processed": 150,
  "calls_by_category": {
    "billing": 60,
    "technical": 40,
    "bundles": 25,
    "complaints": 15,
    "general_inquiry": 10,
    "other": 0
  },
  "calls_by_sentiment": {
    "positive": 85,
    "neutral": 45,
    "negative": 20
  },
  "average_processing_time": 12.5,
  "success_rate": 0.98,
  "date_range": {
    "start": "2025-06-03T09:24:16.123Z",
    "end": "2025-07-03T09:24:16.123Z"
  }
}
```

---

## Data Models (From Actual Implementation)

### CallStatus Enum
- `processing`: Call is being processed
- `completed`: Processing completed successfully
- `failed`: Processing failed

### SentimentType Enum
- `positive`: Positive customer interaction
- `neutral`: Neutral tone
- `negative`: Negative customer experience

### CallCategory Enum
- `billing`: Payment, account, billing issues
- `technical`: Network, connectivity, technical problems
- `bundles`: Data bundles, airtime, packages
- `complaints`: Customer complaints and grievances
- `general_inquiry`: General questions and information
- `other`: Miscellaneous calls

### Priority Enum
- `high`: Urgent issues
- `medium`: Standard priority
- `low`: Low priority

### ResolutionStatus Enum
- `resolved`: Issue completely resolved
- `pending`: Issue requires follow-up
- `escalated`: Issue escalated to higher level

---

## CallRecord Model Fields (Actual Implementation)

### Basic Call Info
- `call_id`: Unique call identifier
- `upload_timestamp`: When call was uploaded
- `audio_file_path`: Path to uploaded audio file
- `audio_filename`: Original filename
- `audio_duration`: Duration in seconds

### Processing Status
- `status`: Current processing status (CallStatus enum)
- `processed_at`: When processing completed

### Transcription
- `transcript`: Full call transcript

### AI-Generated Insights
- `summary`: List of 3 bullet points summarizing key discussion points
- `sentiment`: Overall call sentiment (SentimentType enum)
- `category`: Call type classification (CallCategory enum)
- `action_items`: List of required follow-up actions
- `customer_requests`: List of what customer asked for
- `resolution_status`: Call resolution state (ResolutionStatus enum)
- `priority`: Call priority level (Priority enum)
- `tags`: List of searchable tags
- `agent_performance`: Agent performance assessment string
- `follow_up_required`: Boolean indicating if callback needed

### Metadata
- `user_metadata`: User upload metadata dictionary
- `processing_metadata`: System processing info dictionary

---

## Error Handling

### Common HTTP Status Codes
- **200**: Success
- **202**: Accepted (processing in progress)
- **400**: Bad Request (invalid file format, validation errors)
- **404**: Not Found (call not found)
- **500**: Internal Server Error (processing failed)

### Error Response Format
```json
{
  "detail": "Error message describing the issue"
}
```

---

## File Upload Constraints
- **Allowed formats**: .mp3, .wav, .webm, .m4a, .opus
- **File size**: No explicit limit mentioned in current implementation
- **Storage location**: `/tmp/callgist_uploads/`

---

## Database
- **MongoDB collection**: `calls`
- **Single unified collection** containing all call records and insights
- **Indexes**: Created automatically by database manager

---

## Background Processing
- Audio upload triggers background processing task
- Processing includes:
  1. Audio transcription using OpenAI Whisper
  2. Transcript sanitization (removes sensitive data)
  3. AI analysis using OpenAI GPT-3.5-turbo
  4. Database update with results

---

## AI Processing Details
- **Transcription**: OpenAI Whisper API
- **Analysis**: OpenAI GPT-3.5-turbo
- **Token usage**: ~925 tokens per call average
- **Processing time**: ~30-60 seconds per call
- **Sanitization**: Removes phone numbers, amounts, customer names

This documentation is based on the actual implementation in the codebase and reflects the current working features.

# AI Call Summarization API Documentation

## Overview
The AI Call Summarization API provides intelligent analysis of customer service calls for Zimbabwe call centers. It uses OpenAI's advanced AI models to transcribe audio, analyze sentiment, categorize calls, and extract actionable insights.

**Base URL:** `http://localhost:8000`
**API Version:** v1
**Prefix:** `/api/v1`

---

## Authentication
Currently, no authentication is required for the API endpoints. In production, you would typically add API key authentication.

---

## Core Endpoints

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

#### Example Usage
```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "audio_file=@customer_call.mp3"
```

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
  "progress": 100,
  "message": "Call analysis completed successfully",
  "created_at": "2025-07-03T09:24:16.123Z",
  "completed_at": "2025-07-03T09:25:45.678Z"
}
```

#### Status Values
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
  "transcript": "Good afternoon, thank you for calling EcoCash support, my name is Fadzai, how can I help you today? Hi Fadzai, I just tried to buy airtime using EcoCash, the money was deducted from my wallet but I haven't received my airtime...",
  "word_count": 156,
  "duration_seconds": 45.2,
  "language": "en",
  "confidence": 0.95
}
```

---

### 4. Get Call Summary & Analysis
**GET** `/api/v1/call/{call_id}/summary`

Get comprehensive AI analysis of the call including sentiment, categorization, and actionable insights.

#### Parameters
- `call_id` (string, required): Unique call identifier

#### Response
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
  "priority": "medium",
  "resolution_status": "resolved",
  "action_items": [
    "Investigate why airtime did not post to mobile operator system",
    "Update system to prevent future occurrences"
  ],
  "customer_requests": [
    "Receive purchased airtime",
    "Resolution of airtime deduction issue"
  ],
  "tags": [
    "airtime_purchase",
    "credit_issue",
    "resolved",
    "ecocash"
  ],
  "agent_performance": "Efficient - resolved the issue promptly and credited airtime",
  "follow_up_required": false,
  "call_duration": 45.2,
  "created_at": "2025-07-03T09:24:16.123Z"
}
```

---

### 5. Search Calls
**POST** `/api/v1/calls/search`

Search and filter calls based on various criteria.

#### Request Body
```json
{
  "sentiment": "positive",
  "category": "billing",
  "priority": "high",
  "resolution_status": "resolved",
  "date_from": "2025-07-01T00:00:00Z",
  "date_to": "2025-07-03T23:59:59Z",
  "tags": ["airtime", "payment"],
  "limit": 20,
  "offset": 0
}
```

#### Response
```json
{
  "calls": [
    {
      "call_id": "call_5c20fc3b2de5",
      "summary": ["Customer experienced airtime purchase issue..."],
      "sentiment": "positive",
      "category": "billing",
      "priority": "medium",
      "resolution_status": "resolved",
      "created_at": "2025-07-03T09:24:16.123Z",
      "tags": ["airtime_purchase", "credit_issue", "resolved"]
    }
  ],
  "total_count": 1,
  "limit": 20,
  "offset": 0,
  "has_more": false
}
```

---

### 6. List Recent Calls
**GET** `/api/v1/calls`

Get a list of recent calls with optional filtering.

#### Query Parameters
- `limit` (integer, optional): Number of calls to return (default: 20, max: 100)
- `offset` (integer, optional): Number of calls to skip (default: 0)
- `status` (string, optional): Filter by status (processing, completed, failed)
- `sentiment` (string, optional): Filter by sentiment (positive, neutral, negative)
- `category` (string, optional): Filter by category

#### Response
```json
{
  "calls": [
    {
      "call_id": "call_5c20fc3b2de5",
      "status": "completed",
      "sentiment": "positive",
      "category": "billing",
      "priority": "medium",
      "resolution_status": "resolved",
      "created_at": "2025-07-03T09:24:16.123Z",
      "audio_filename": "customer_call.mp3"
    }
  ],
  "total_count": 1,
  "limit": 20,
  "offset": 0,
  "has_more": false
}
```

---

### 7. Analytics Dashboard
**GET** `/api/v1/analytics/dashboard`

Get comprehensive analytics for call center performance.

#### Response
```json
{
  "total_calls": 150,
  "calls_today": 12,
  "sentiment_distribution": {
    "positive": 85,
    "neutral": 45,
    "negative": 20
  },
  "category_distribution": {
    "billing": 60,
    "technical": 40,
    "bundles": 25,
    "complaints": 15,
    "general_inquiry": 10
  },
  "resolution_stats": {
    "resolved": 120,
    "pending": 20,
    "escalated": 10
  },
  "priority_distribution": {
    "high": 30,
    "medium": 80,
    "low": 40
  },
  "average_call_duration": 65.5,
  "agent_performance_avg": 4.2,
  "follow_up_rate": 0.15,
  "top_tags": [
    {"tag": "payment_issue", "count": 25},
    {"tag": "network_problem", "count": 20},
    {"tag": "data_bundle", "count": 18}
  ]
}
```

---

### 8. API Usage Statistics
**GET** `/api/v1/analytics/usage`

Get API usage statistics and metrics.

#### Response
```json
{
  "total_api_calls": 1250,
  "calls_today": 45,
  "calls_this_week": 280,
  "calls_this_month": 1100,
  "average_processing_time": 12.5,
  "success_rate": 0.98,
  "error_rate": 0.02,
  "most_active_hours": [9, 10, 11, 14, 15],
  "peak_usage_day": "Monday"
}
```

---

## Data Models

### Call Categories
- `billing`: Payment, account, billing issues
- `technical`: Network, connectivity, technical problems
- `bundles`: Data bundles, airtime, packages
- `complaints`: Customer complaints and grievances
- `general_inquiry`: General questions and information
- `other`: Miscellaneous calls

### Sentiment Types
- `positive`: Customer satisfied, positive interaction
- `neutral`: Neutral tone, standard interaction
- `negative`: Customer frustrated, negative experience

### Priority Levels
- `high`: Urgent issues requiring immediate attention
- `medium`: Standard priority issues
- `low`: Low priority, routine inquiries

### Resolution Status
- `resolved`: Issue completely resolved
- `pending`: Issue requires follow-up
- `escalated`: Issue escalated to higher level

---

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Unsupported audio format. Allowed: .mp3, .wav, .webm, .m4a, .opus"
}
```

#### 404 Not Found
```json
{
  "detail": "Call not found: call_invalid_id"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Processing failed: OpenAI API error"
}
```

---

## Rate Limits
- **Upload endpoint**: 10 requests per minute per IP
- **Other endpoints**: 100 requests per minute per IP

---

## Best Practices

1. **File Size**: Keep audio files under 25MB for optimal processing
2. **Format**: Use .mp3 or .wav for best transcription accuracy
3. **Polling**: Poll the status endpoint every 5-10 seconds during processing
4. **Caching**: Cache summary results to avoid repeated API calls
5. **Error Handling**: Implement proper retry logic for failed requests

---

## Integration Examples

### Python Example
```python
import requests
import time

# Upload audio file
with open('customer_call.mp3', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/upload',
        files={'audio_file': f}
    )
    call_data = response.json()
    call_id = call_data['call_id']

# Poll for completion
while True:
    status_response = requests.get(f'http://localhost:8000/api/v1/call/{call_id}/status')
    status_data = status_response.json()
    
    if status_data['status'] == 'completed':
        break
    elif status_data['status'] == 'failed':
        print("Processing failed")
        break
    
    time.sleep(5)

# Get summary
summary_response = requests.get(f'http://localhost:8000/api/v1/call/{call_id}/summary')
summary_data = summary_response.json()
print(f"Sentiment: {summary_data['sentiment']}")
print(f"Category: {summary_data['category']}")
```

### JavaScript Example
```javascript
// Upload audio file
const formData = new FormData();
formData.append('audio_file', audioFile);

const uploadResponse = await fetch('http://localhost:8000/api/v1/upload', {
    method: 'POST',
    body: formData
});

const uploadData = await uploadResponse.json();
const callId = uploadData.call_id;

// Poll for completion
let completed = false;
while (!completed) {
    const statusResponse = await fetch(`http://localhost:8000/api/v1/call/${callId}/status`);
    const statusData = await statusResponse.json();
    
    if (statusData.status === 'completed') {
        completed = true;
    } else if (statusData.status === 'failed') {
        throw new Error('Processing failed');
    }
    
    await new Promise(resolve => setTimeout(resolve, 5000));
}

// Get summary
const summaryResponse = await fetch(`http://localhost:8000/api/v1/call/${callId}/summary`);
const summaryData = await summaryResponse.json();
console.log('Analysis:', summaryData);
```

---

## Support
For technical support or questions about the API, please contact the development team or refer to the interactive Swagger documentation at `http://localhost:8000/docs`.

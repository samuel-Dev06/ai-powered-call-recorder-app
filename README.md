# 🎙️ AI Call Summarization System

A complete, containerized system for real-time call transcription, AI-powered summarization, and sentiment analysis using OpenAI Whisper and GPT-4.

## ✨ Features

### 🔧 Backend (FastAPI)
- **Audio Processing**: Support for OPUS, MP3, WAV, OGG, M4A formats
- **Real-time Transcription**: OpenAI Whisper API integration
- **AI Summarization**: GPT-4 powered analysis and insights
- **Sentiment Analysis**: Emotional tone and satisfaction detection
- **WebSocket Events**: Real-time status updates
- **MongoDB Storage**: Persistent call data and analytics
- **REST API**: Comprehensive endpoints for all operations

### 🖥️ Frontend (Streamlit)
- **Audio Upload Workflow**: Drag-and-drop file analysis
- **Live Call Simulation**: Record and analyze in real-time
- **Interactive Dashboard**: Comprehensive results visualization
- **Real-time Updates**: Live progress tracking
- **Call History**: Browse past analyses
- **Mobile Responsive**: Works on all devices

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 1. Clone and Setup
```bash
git clone <repository-url>
cd ai-call-summarization
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Start the System
```bash
# Windows (PowerShell)
.\run-system.ps1

# Or manually with Docker Compose
docker-compose up -d
```

### 4. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📋 Usage

### Audio Upload Workflow
1. Open the Streamlit frontend at http://localhost:8501
2. Go to "Audio Upload & Analysis" section
3. Upload an audio file (MP3, WAV, OPUS, etc.)
4. Click "Analyze Audio"
5. View comprehensive results in tabs:
   - **Summary**: Key points and action items
   - **Sentiment**: Emotional analysis
   - **Analytics**: Call metrics and topics
   - **Details**: Raw data

### Live Call Simulation
1. Click "Start Call" to begin a session
2. Upload audio during the "call"
3. Click "End Call" to trigger analysis
4. View results immediately

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI      │    │    MongoDB      │
│   Frontend      │◄──►│    Backend      │◄──►│    Database     │
│   (Port 8501)   │    │   (Port 8000)   │    │   (Port 27017)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       
         │                       ▼                       
         │              ┌─────────────────┐              
         │              │   OpenAI APIs   │              
         └──────────────┤  Whisper + GPT-4 │              
                        └─────────────────┘              
```

## 🐳 Docker Services

| Service | Container Name | Port | Description |
|---------|---------------|------|-------------|
| Frontend | ai-call-frontend | 8501 | Streamlit web interface |
| Backend | ai-call-backend | 8000 | FastAPI REST API |
| Database | ai-call-mongodb | 27017 | MongoDB data storage |

## 🔧 Development

### Local Development (without Docker)
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend  
pip install -r requirements.txt
streamlit run app.py
```

### Building Images
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build frontend
docker-compose build backend
```

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
docker-compose logs -f backend
```

## 📊 API Endpoints

### Call Management
- `POST /api/calls/start` - Start new call session
- `POST /api/calls/{id}/audio` - Upload audio to session
- `POST /api/calls/{id}/end` - End call and process
- `GET /api/calls/{id}/summary` - Get analysis results
- `GET /api/calls/history` - Get call history

### System
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /api/analytics/dashboard` - System analytics

## 🔒 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `MONGODB_URL` | MongoDB connection string | `mongodb://ai-call-mongodb:27017` |
| `DATABASE_NAME` | MongoDB database name | `ai_call_summarization` |
| `BACKEND_URL` | Backend URL for frontend | `http://ai-call-backend:8000` |
| `CORS_ORIGINS` | Allowed CORS origins | Frontend URLs |

## 🛠️ Troubleshooting

### System Won't Start
```bash
# Check Docker is running
docker version

# Clean restart
docker-compose down
docker-compose up -d

# Check logs
docker-compose logs
```

### Frontend Can't Connect to Backend
- Verify backend is healthy: `docker-compose ps`
- Check backend logs: `docker-compose logs backend`
- Ensure CORS origins include frontend URL

### Audio Processing Fails
- Verify OpenAI API key is set correctly
- Check backend logs for API errors
- Ensure audio file format is supported

### MongoDB Connection Issues
- Verify MongoDB container is running
- Check if port 27017 is available
- Review database logs: `docker-compose logs mongodb`

## 📈 Performance

### Recommended Specs
- **CPU**: 2+ cores
- **Memory**: 4GB+ RAM
- **Storage**: 2GB+ free space
- **Network**: Stable internet for OpenAI API

### Scaling
- Backend can be horizontally scaled
- MongoDB supports clustering
- Frontend is stateless and scalable

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for Whisper and GPT-4 APIs
- Streamlit for the amazing frontend framework
- FastAPI for the robust backend framework
- MongoDB for reliable data storage

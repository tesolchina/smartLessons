I# AI Video Generator - Integration Guide

## Overview
This guide explains how to integrate the AI Video Generator with your existing backend streaming avatar service for production use.

## Architecture

### Frontend Components
1. **production-video-generator.html** - Main application interface
2. **script-slide-demo.html** - Simplified demo version
3. **vue-avatar-demo.html** - Vue.js implementation

### Backend Components
1. **streaming_avatar_backend.py** - Flask/SocketIO backend service
2. **Avatar figure assets** - 3D models and textures in `avatarFigure/`

## Integration Steps

### 1. Backend Setup

#### Prerequisites
```bash
pip install flask flask-socketio speech-recognition gtts
```

#### WebSocket Configuration
The backend uses Socket.IO with namespace `/api/streaming-avatar`:

```python
socket_namespace = "/api/streaming-avatar"

@socketio.on("user_message", namespace=socket_namespace)
def handle_user_message(data):
    # Process script → Generate TTS → Stream audio chunks
```

#### Key Features
- **Speech-to-Text**: Google Speech Recognition API
- **Text-to-Speech**: Google TTS (gTTS)
- **Audio Streaming**: MP3 chunks via WebSocket
- **Multi-provider Support**: HKBU GenAI, OpenRouter, OpenAI

### 2. Frontend Integration

#### API Configuration
```javascript
// Connect to your backend
const socket = io('your-backend-url/api/streaming-avatar');

// Configure API providers
const apiProviders = {
    hkbu: 'HKBU GenAI',
    openrouter: 'OpenRouter', 
    openai: 'OpenAI'
};
```

#### Real-time Communication
```javascript
// Send script for processing
socket.emit('user_message', {
    text: scriptContent,
    system_prompt: 'You are an educational AI assistant...',
    api_key: userApiKey,
    model: selectedModel,
    provider: selectedProvider
});

// Receive audio chunks
socket.on('audio_chunk', (chunk) => {
    audioChunks.push(chunk);
});

socket.on('audio_complete', () => {
    // Combine chunks and play audio
    const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });
    audioPlayer.src = URL.createObjectURL(audioBlob);
});
```

### 3. Avatar Integration

#### 3D Avatar Assets
Located in `demo/avatarFigure/`:
- `*.fbx` - 3D model files
- `tex/` - Texture files including:
  - Character textures
  - Logo overlays
  - UI elements

#### Avatar States
```javascript
const avatarStates = {
    idle: 'Ready to generate video',
    listening: 'Processing script...',
    thinking: 'Generating response...',
    speaking: 'Playing audio...'
};
```

### 4. Production Deployment

#### Environment Variables
```bash
# API Configuration
HKBU_API_KEY=your_hkbu_key
OPENROUTER_API_KEY=your_openrouter_key
OPENAI_API_KEY=your_openai_key

# Server Configuration
FLASK_ENV=production
SOCKETIO_CORS_ALLOWED_ORIGINS=your-frontend-domain
```

#### Docker Configuration
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

### 5. API Endpoints

#### REST Endpoints
- `GET /api/streaming-avatar/a` - Health check
- `POST /api/chat` - Direct chat completion
- `POST /api/chat_openrouter` - OpenRouter integration

#### WebSocket Events
- `connect` - Client connection
- `disconnect` - Client disconnection  
- `user_audio` - Audio input for STT
- `user_message` - Text message processing
- `stt_result` - Speech recognition result
- `audio_chunk` - TTS audio chunk
- `audio_complete` - Audio generation complete
- `assistant_reply` - Text response

### 6. Error Handling

#### Common Issues
1. **API Key Invalid**: Check provider configuration
2. **Audio Processing Failed**: Verify audio format (WAV)
3. **WebSocket Connection Lost**: Implement reconnection logic
4. **TTS Generation Error**: Handle empty/emoji text

#### Error Responses
```javascript
{
    "error": "API key invalid",
    "code": "AUTH_ERROR",
    "details": "Please check your API configuration"
}
```

### 7. Performance Optimization

#### Audio Streaming
- Chunk size: 4096 bytes
- Format: MP3 for web compatibility
- Compression: Balanced quality/size

#### Caching Strategy
- Cache TTS results for repeated content
- Store user preferences locally
- Implement session management

### 8. Security Considerations

#### API Key Management
- Store keys securely (environment variables)
- Implement key rotation
- Use HTTPS for all communications

#### Input Validation
- Sanitize script content
- Limit message length
- Rate limiting for API calls

### 9. Testing

#### Unit Tests
```bash
# Test API connections
python -m pytest tests/test_api.py

# Test WebSocket functionality  
python -m pytest tests/test_websocket.py
```

#### Integration Tests
```bash
# Test full workflow
npm run test:integration
```

### 10. Monitoring

#### Metrics to Track
- API response times
- Audio generation success rate
- WebSocket connection stability
- User engagement metrics

#### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Usage Examples

### Basic Video Generation
```javascript
const generator = new ProductionVideoGenerator();
await generator.connectToAPI();
await generator.generateVideo({
    script: "Welcome to AI education...",
    slides: ["AI Basics", "Applications", "Future"],
    voice: "en",
    speed: 1.0
});
```

### Advanced Configuration
```javascript
const config = {
    provider: 'openrouter',
    model: 'claude-3-sonnet',
    maxTokens: 150,
    temperature: 0.7,
    systemPrompt: 'You are an expert educator...'
};

await generator.generateVideo(script, config);
```

## Support

For technical support or questions:
- Check the demo files for implementation examples
- Review the backend code for API details
- Test with the provided sample scripts

## Version History

- v1.0: Initial implementation with basic TTS
- v1.1: Added multi-provider support
- v1.2: Integrated 3D avatar assets
- v1.3: Production-ready with error handling

# 🎬 Script-to-Avatar Video Generator

## 📋 Simple Workflow Overview

**Input**: Ready script + bullet points → **Output**: Avatar video with synchronized slide bullets

```
Educational Script + Bullet Points
          ↓
    Text-to-Speech Audio
          ↓
    Avatar Video Generation
          ↓
    Bullet Points Sync & Overlay
          ↓
    Final Composed Video
```

## 🎯 Core Requirements

### Input Format
```javascript
const videoRequest = {
  script: "Welcome to today's lesson on AI in education. First, let's explore how AI personalizes learning...",
  bulletPoints: [
    "AI Personalizes Learning",
    "Improves Student Engagement", 
    "Provides Real-time Feedback",
    "Scales Educational Content"
  ],
  timing: {
    totalDuration: 120, // seconds
    bulletRevealTiming: [15, 45, 75, 105] // when each bullet appears
  },
  avatar: {
    id: "professional_teacher",
    voice: "en-US-female-1",
    background: "classroom"
  }
};
```

### Output Specifications
- **Video**: 1080p MP4, 16:9 aspect ratio
- **Duration**: Auto-calculated from script length
- **Layout**: Avatar (left 60%) + Bullet slides (right 40%)
- **Audio**: High-quality TTS synchronized with avatar lip movements

## 🛠️ Technical Implementation

### 1. Script Processing & Timing
```javascript
// Calculate timing for bullet point reveals
function calculateBulletTiming(script, bulletPoints) {
  const wordsPerMinute = 150; // Average speaking speed
  const words = script.split(' ').length;
  const totalDuration = (words / wordsPerMinute) * 60;
  
  // Distribute bullet points evenly across script duration
  const bulletInterval = totalDuration / bulletPoints.length;
  const bulletTiming = bulletPoints.map((_, index) => 
    Math.round(bulletInterval * (index + 0.5))
  );
  
  return { totalDuration, bulletTiming };
}
```

### 2. Text-to-Speech Generation
```javascript
// Using ElevenLabs for high-quality TTS
async function generateSpeech(script, voiceId) {
  const response = await fetch('https://api.elevenlabs.io/v1/text-to-speech/' + voiceId, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${ELEVENLABS_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      text: script,
      voice_settings: {
        stability: 0.5,
        similarity_boost: 0.75,
        style: 0.3,
        use_speaker_boost: true
      }
    })
  });
  
  return await response.arrayBuffer(); // Audio file
}
```

### 3. Avatar Video Generation
```javascript
// Using HeyGen API for avatar video
async function generateAvatarVideo(audioFile, avatarConfig) {
  const formData = new FormData();
  formData.append('audio', new Blob([audioFile], { type: 'audio/mpeg' }));
  formData.append('avatar_id', avatarConfig.id);
  formData.append('background', avatarConfig.background);
  
  const response = await fetch('https://api.heygen.com/v2/video/generate', {
    method: 'POST',
    headers: {
      'X-API-Key': HEYGEN_API_KEY
    },
    body: formData
  });
  
  const result = await response.json();
  
  // Poll for completion
  return await pollVideoCompletion(result.video_id);
}

async function pollVideoCompletion(videoId) {
  while (true) {
    const status = await fetch(`https://api.heygen.com/v1/video_status/${videoId}`, {
      headers: { 'X-API-Key': HEYGEN_API_KEY }
    });
    
    const data = await status.json();
    
    if (data.status === 'completed') {
      return data.video_url;
    } else if (data.status === 'failed') {
      throw new Error('Video generation failed');
    }
    
    await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds
  }
}
```

### 4. Bullet Points Slide Generation
```javascript
// Generate bullet point slides with timing
function generateBulletSlides(bulletPoints, timing, dimensions) {
  const slides = bulletPoints.map((bullet, index) => ({
    text: bullet,
    startTime: timing.bulletTiming[index],
    endTime: timing.bulletTiming[index + 1] || timing.totalDuration,
    animation: 'fadeIn'
  }));
  
  return slides;
}

// Create slide video using HTML5 Canvas
function createSlideVideo(slides, duration, dimensions) {
  const canvas = document.createElement('canvas');
  canvas.width = dimensions.width;
  canvas.height = dimensions.height;
  const ctx = canvas.getContext('2d');
  
  const stream = canvas.captureStream(30); // 30 fps
  const recorder = new MediaRecorder(stream);
  
  // Animate slides based on timing
  animateSlides(ctx, slides, duration);
  
  return recorder;
}
```

### 5. Video Composition (Server-side with FFmpeg)
```javascript
// Combine avatar video with bullet slides
async function composeVideo(avatarVideoPath, slidesVideoPath, outputPath) {
  return new Promise((resolve, reject) => {
    ffmpeg()
      .input(avatarVideoPath)
      .input(slidesVideoPath)
      .complexFilter([
        // Resize avatar to 60% width
        '[0:v]scale=iw*0.6:ih[avatar]',
        // Resize slides to 40% width  
        '[1:v]scale=iw*0.4:ih[slides]',
        // Combine side by side
        '[avatar][slides]hstack=inputs=2[v]'
      ])
      .outputOptions([
        '-map [v]',
        '-map 0:a', // Use audio from avatar video
        '-c:v libx264',
        '-c:a aac',
        '-preset fast',
        '-crf 23'
      ])
      .output(outputPath)
      .on('end', resolve)
      .on('error', reject)
      .run();
  });
}
```

## 🚀 Complete Workflow Implementation

### Backend API Endpoint
```javascript
app.post('/api/generate-video', async (req, res) => {
  try {
    const { script, bulletPoints, avatar } = req.body;
    
    // Step 1: Calculate timing
    const timing = calculateBulletTiming(script, bulletPoints);
    
    // Step 2: Generate speech
    const audioBuffer = await generateSpeech(script, avatar.voice);
    
    // Step 3: Generate avatar video
    const avatarVideoUrl = await generateAvatarVideo(audioBuffer, avatar);
    
    // Step 4: Download avatar video
    const avatarVideoPath = await downloadVideo(avatarVideoUrl);
    
    // Step 5: Generate bullet slides video
    const slides = generateBulletSlides(bulletPoints, timing);
    const slidesVideoPath = await renderSlidesVideo(slides, timing.totalDuration);
    
    // Step 6: Compose final video
    const finalVideoPath = await composeVideo(avatarVideoPath, slidesVideoPath);
    
    // Step 7: Upload and return URL
    const finalVideoUrl = await uploadToS3(finalVideoPath);
    
    res.json({
      success: true,
      videoUrl: finalVideoUrl,
      duration: timing.totalDuration
    });
    
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### Frontend Implementation
```html
<!DOCTYPE html>
<html>
<head>
    <title>Script to Avatar Video Generator</title>
    <style>
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .video-output { margin-top: 20px; text-align: center; }
        .progress { width: 100%; height: 20px; background: #f0f0f0; border-radius: 10px; overflow: hidden; }
        .progress-bar { height: 100%; background: #007bff; transition: width 0.3s; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 Script to Avatar Video Generator</h1>
        
        <form id="videoForm">
            <div class="form-group">
                <label for="script">Educational Script:</label>
                <textarea id="script" rows="8" placeholder="Enter your educational script here...">Welcome to today's lesson on artificial intelligence in education. AI is revolutionizing how we learn and teach. First, let's explore how AI personalizes learning for each student. Next, we'll see how it improves student engagement through interactive content. Then, we'll discuss how AI provides real-time feedback to help students learn faster. Finally, we'll look at how AI scales educational content to reach more learners worldwide.</textarea>
            </div>
            
            <div class="form-group">
                <label for="bullets">Bullet Points (one per line):</label>
                <textarea id="bullets" rows="4" placeholder="Enter bullet points...">AI Personalizes Learning
Improves Student Engagement
Provides Real-time Feedback
Scales Educational Content</textarea>
            </div>
            
            <div class="form-group">
                <label for="avatar">Avatar Style:</label>
                <select id="avatar">
                    <option value="professional_teacher">Professional Teacher</option>
                    <option value="friendly_instructor">Friendly Instructor</option>
                    <option value="expert_presenter">Expert Presenter</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="voice">Voice Style:</label>
                <select id="voice">
                    <option value="en-US-female-1">English Female (Professional)</option>
                    <option value="en-US-male-1">English Male (Professional)</option>
                    <option value="en-UK-female-1">English Female (British)</option>
                </select>
            </div>
            
            <button type="submit">🎬 Generate Video</button>
        </form>
        
        <div id="progress" class="progress" style="display: none;">
            <div id="progressBar" class="progress-bar" style="width: 0%"></div>
        </div>
        
        <div id="status" style="margin-top: 10px; font-weight: bold;"></div>
        
        <div id="videoOutput" class="video-output" style="display: none;">
            <h3>Generated Video:</h3>
            <video id="resultVideo" controls width="100%" style="max-width: 800px;">
                Your browser does not support the video tag.
            </video>
            <br><br>
            <a id="downloadLink" href="#" download="generated-video.mp4">
                <button>📥 Download Video</button>
            </a>
        </div>
    </div>

    <script>
        document.getElementById('videoForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const script = document.getElementById('script').value;
            const bullets = document.getElementById('bullets').value.split('\n').filter(b => b.trim());
            const avatar = document.getElementById('avatar').value;
            const voice = document.getElementById('voice').value;
            
            // Show progress
            document.getElementById('progress').style.display = 'block';
            document.getElementById('status').textContent = 'Generating video...';
            
            try {
                const response = await fetch('/api/generate-video', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        script,
                        bulletPoints: bullets,
                        avatar: { id: avatar, voice }
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Show video
                    document.getElementById('resultVideo').src = result.videoUrl;
                    document.getElementById('downloadLink').href = result.videoUrl;
                    document.getElementById('videoOutput').style.display = 'block';
                    document.getElementById('status').textContent = 'Video generated successfully!';
                } else {
                    document.getElementById('status').textContent = 'Error: ' + result.error;
                }
                
            } catch (error) {
                document.getElementById('status').textContent = 'Error: ' + error.message;
            } finally {
                document.getElementById('progress').style.display = 'none';
            }
        });
        
        // Simulate progress updates (in real implementation, use WebSocket)
        function updateProgress(percentage) {
            document.getElementById('progressBar').style.width = percentage + '%';
        }
    </script>
</body>
</html>
```

## 🎯 Example Output

### Input:
- **Script**: "Welcome to AI in education. First, AI personalizes learning..."
- **Bullets**: ["AI Personalizes Learning", "Improves Engagement", "Real-time Feedback", "Scales Content"]

### Processing:
1. **Audio Generation**: 2 minutes of high-quality speech
2. **Avatar Video**: Professional teacher avatar speaking for 2 minutes
3. **Bullet Slides**: 4 bullets appearing at 30s, 60s, 90s, 120s
4. **Composition**: Side-by-side layout with smooth transitions

### Final Video:
- **Duration**: 2 minutes
- **Layout**: Avatar (60%) + Bullets (40%)
- **Quality**: 1080p, professional audio
- **File Size**: ~50MB MP4

## 💰 Cost Per Video

### API Costs (per 2-minute video):
- **ElevenLabs TTS**: ~$0.30
- **HeyGen Avatar**: ~$3.00
- **Server Processing**: ~$0.10
- **Storage**: ~$0.05

**Total Cost Per Video**: ~$3.45

## 🚀 Quick Setup

### 1. Environment Variables
```bash
ELEVENLABS_API_KEY=your_elevenlabs_key
HEYGEN_API_KEY=your_heygen_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

### 2. Dependencies
```bash
npm install express multer fluent-ffmpeg aws-sdk
```

### 3. Run
```bash
node server.js
```

This implementation provides exactly what you need: a simple input of script + bullet points that generates a professional avatar video with synchronized bullet point reveals!

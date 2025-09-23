# AI-Powered Script-to-Avatar Demo

Generate professional avatar videos with synchronized speech and bullet points using Azure TTS or browser-based speech synthesis.

## 🚀 Quick Start

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd presentationWorkhop
   npm install
   ```

2. **Setup Azure Speech (recommended for fast, high-quality audio):**
   - Create Azure Speech resource in [Azure Portal](https://portal.azure.com)
   - Copy Key and Region from "Keys and Endpoint" page
   - Create `.env` file:
     ```
     AZURE_SPEECH_KEY=your_key_here
     AZURE_SPEECH_REGION=your_region_here
     ```

3. **Start the server:**
   ```bash
   npm start
   ```

4. **Open the Vue demo:**
   Navigate to: http://localhost:3000/demo/simple-script-avatar-demo-vue.html

## 🎬 Vue Demo Features

### Main Interface
- **Script Selection**: Choose from AI Education, Climate Change, or Space Exploration topics
- **Engine Selector**: Switch between "Browser TTS" (slow but free) and "Azure TTS" (fast, high-quality)
- **Two-Step Process**: Generate audio first, then create synchronized video

### Step-by-Step Usage

1. **Select a Script**: Click one of the three demo script buttons
2. **Choose TTS Engine**: 
   - Browser TTS: Uses built-in speech synthesis (slower, varies by device)
   - Azure TTS: Uses cloud service (faster, consistent quality)
3. **Generate Audio**: Click "Step 1: Generate & Preview Audio"
   - Progress bar shows generation status
   - Audio player appears when ready
   - Test playback before proceeding
4. **Generate Video**: Click "Step 2: Generate Full Video"
   - Creates 1280x720 video with synchronized bullet points
   - Bullet points appear timed to speech
   - Video preview available immediately
5. **Download**: Use download buttons for audio (.webm) and video (.webm) files

### Additional Features
- **Quick Video**: Generate video without audio (faster for testing)
- **Cancel**: Stop generation mid-process
- **Reset**: Clear audio/video and start over
- **Live Logs**: View real-time generation progress in bottom panel

## ⚙️ Azure Speech Setup (Detailed)

### Create Azure Resource
1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → Search "Speech"
3. Select "Speech" by Microsoft
4. Fill out form:
   - **Subscription**: Choose your subscription
   - **Resource group**: Create new or use existing
   - **Region**: Choose closest region (e.g., eastus, eastasia, westeurope)
   - **Name**: Choose unique name
   - **Pricing tier**: F0 (free) for testing, S0 for production
5. Click "Review + Create" → "Create"

### Get Credentials
1. After deployment, go to your Speech resource
2. Left sidebar: "Keys and Endpoint"
3. Copy **Key 1** (32-character string)
4. Note **Region** (exact string like "eastus" or "eastasia")

### Configure Application
1. Create `.env` file in project root:
   ```
   AZURE_SPEECH_KEY=paste_your_key_here
   AZURE_SPEECH_REGION=your_region_here
   ```
2. Restart server: `npm start`

## 🧪 Testing Commands

### Test Azure Integration
```bash
# Test direct Azure connection
node tts-test.js --direct --text "Hello Azure"

# Test via local server proxy
node tts-test.js --local --text "Hello local proxy"

# Custom voice and output
node tts-test.js --direct --voice en-GB-RyanNeural --text "British accent test" --out british.mp3
```

### Available npm Scripts
```bash
npm start                    # Start server
npm run dev                  # Start with nodemon (auto-restart)
npm run test:tts:local       # Quick local proxy test
npm run test:tts:direct      # Quick direct Azure test
```

## 🎙️ Voice Options

### Popular Azure Neural Voices
- `en-US-JennyNeural` (default female, US)
- `en-US-GuyNeural` (male, US)
- `en-GB-SoniaNeural` (female, British)
- `en-GB-RyanNeural` (male, British)
- `en-AU-NatashaNeural` (female, Australian)
- `en-CA-ClaraNeural` (female, Canadian)

### Change Voice
In Vue demo: Edit `fetchAzureTTS` method to change default voice, or add voice selector UI.

For testing: Use `--voice` parameter:
```bash
node tts-test.js --direct --voice en-GB-SoniaNeural --text "British female voice"
```

## 📁 File Structure

```
presentationWorkhop/
├── server.js                          # Express server with Azure TTS proxy
├── package.json                       # Dependencies and scripts
├── .env                               # Azure credentials (create this)
├── .env.example                       # Template for .env
├── tts-test.js                        # CLI testing utility
├── demo/
│   ├── simple-script-avatar-demo-vue.html    # Main Vue demo
│   ├── simple-script-avatar-demo-v2.html     # Working v2 reference
│   └── simple-script-avatar-demo-v3.html     # v3 with improvements
└── components/                        # Additional demo components
```

## 🔧 Troubleshooting

### Common Issues

**"Missing AZURE_SPEECH_KEY or AZURE_SPEECH_REGION"**
- Ensure `.env` file exists in project root
- Check key/region format matches Azure Portal exactly
- Restart server after creating/modifying `.env`

**"Token request failed 401"**
- Key is incorrect or expired
- Region mismatch (check Azure Portal for exact region string)
- Try regenerating key in Azure Portal

**"Azure TTS failed" with HTML error**
- Wrong region specified
- Quota exceeded (check Azure Portal usage)
- Network connectivity issues

**Browser TTS not working**
- Refresh page to load voices
- Try different browser (Chrome/Edge recommended)
- Check browser console for errors

**Video has no audio**
- Test audio generation first (Step 1)
- Ensure audio plays in preview before generating video
- Try "Quick Video" to test video generation without audio

**Large file sizes**
- Videos are high quality (1280x720, 30fps)
- Audio uses compressed formats (.webm, .mp3)
- For smaller files: edit format settings in code

### Performance Tips

- **Azure TTS**: Much faster than browser TTS (500ms vs 15-30s)
- **Browser TTS**: Free but slower, varies by device/browser
- **Video Generation**: Takes ~1-2 seconds per second of final video
- **Quick Video**: Faster option for testing without audio

### Development

**Add new demo scripts:**
Edit `scripts` object in Vue demo with new title, description, text, and bullets.

**Customize avatar appearance:**
Modify CSS classes in `<style>` section for avatar container, colors, animations.

**Add voice selection UI:**
Extend Vue demo with voice dropdown using available Azure neural voices.

## 📄 License

MIT License - feel free to use and modify for your projects.

## 🆘 Support

For issues:
1. Check this README troubleshooting section
2. Test with `tts-test.js` commands
3. Check browser console for errors
4. Verify Azure Portal credentials and quota

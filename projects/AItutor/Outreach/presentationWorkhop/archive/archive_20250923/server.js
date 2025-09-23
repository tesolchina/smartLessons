// Load environment variables (if .env present)
try { require('dotenv').config(); } catch(_) {}
const express = require('express');
const cors = require('cors');
const path = require('path');
const https = require('https');
const fetch = global.fetch || ((...args)=>import('node-fetch').then(m=>m.default(...args)));

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS for all routes
app.use(cors());

// Parse JSON bodies
app.use(express.json());

// Serve static files from the root directory
app.use(express.static(__dirname));

// Serve component files specifically
app.use('/components', express.static(path.join(__dirname, 'components')));

// API route for component loading (if needed for future enhancements)
app.get('/api/component/:name', (req, res) => {
    const componentName = req.params.name;
    const componentPath = path.join(__dirname, 'components', `${componentName}.html`);
    
    res.sendFile(componentPath, (err) => {
        if (err) {
            console.error(`Error serving component ${componentName}:`, err);
            res.status(404).json({ error: 'Component not found' });
        }
    });
});

// Serve the main index.html for all other routes (SPA support)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Azure TTS proxy endpoint
// Requires environment variables: AZURE_SPEECH_KEY, AZURE_SPEECH_REGION
app.post('/api/tts', async (req, res) => {
    try {
        const { text, voice = 'en-US-JennyNeural', format = 'audio-24khz-48kbitrate-mono-mp3' } = req.body || {};
        if (!text || !text.trim()) return res.status(400).json({ error: 'Missing text' });
        const key = process.env.AZURE_SPEECH_KEY;
        const region = process.env.AZURE_SPEECH_REGION;
        if (!key || !region) return res.status(500).json({ error: 'Azure Speech credentials not set' });

        // Acquire token (optional optimization: cache for 9 minutes)
        const tokenResp = await fetch(`https://${region}.api.cognitive.microsoft.com/sts/v1.0/issueToken`, {
            method: 'POST',
            headers: { 'Ocp-Apim-Subscription-Key': key }
        });
        if (!tokenResp.ok) {
            return res.status(500).json({ error: 'Failed to get Azure token' });
        }
        const token = await tokenResp.text();

        // Build SSML
        const ssml = `<?xml version="1.0" encoding="utf-8"?>\n<speak version="1.0" xml:lang="en-US"><voice name="${voice}">${text.replace(/&/g,'&amp;')}</voice></speak>`;

        const ttsResp = await fetch(`https://${region}.tts.speech.microsoft.com/cognitiveservices/v1`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': format,
                'User-Agent': 'WorkshopAvatarDemo'
            },
            body: ssml
        });
        if (!ttsResp.ok) {
            const errText = await ttsResp.text();
            return res.status(500).json({ error: 'Azure TTS failed', details: errText.slice(0,200) });
        }
        const arrayBuffer = await ttsResp.arrayBuffer();
        res.setHeader('Content-Type', 'audio/mpeg');
        res.setHeader('Content-Length', arrayBuffer.byteLength);
        res.send(Buffer.from(arrayBuffer));
    } catch (e) {
        console.error('Azure TTS error:', e);
        res.status(500).json({ error: 'TTS proxy error' });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Server error:', err);
    res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
    console.log(`🚀 Workshop server running on port ${PORT}`);
    console.log(`📖 Access your workshop at: http://localhost:${PORT}`);
    console.log(`🎯 Workshop planning document: http://localhost:${PORT}/workshop-planning-document.md`);
});

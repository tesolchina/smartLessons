# 🤖 Avatar Animation System

A comprehensive, reusable avatar animation component for web applications with speech synthesis, emotion display, and interactive animations.

## 📁 Files Overview

### Fixed Directory Structure
```
avatar-assets/
├── avatar-model.c4d          # 3D model source (Cinema 4D)
├── avatar-model.fbx          # 3D model export (FBX format)
├── tex/                      # Texture assets
│   ├── owl.png              # Main owl avatar image
│   ├── Lingua.png           # Alternative avatar image
│   ├── Meet Lingua.png      # Presentation avatar
│   ├── head-texture-2.png   # Head texture map
│   ├── head-texture-upscaled.png # Enhanced head texture
│   ├── eyes-texture-upscaled.png # Enhanced eye texture
│   ├── texture-map-2.png    # Additional texture map
│   ├── base-texture.png     # Base texture layer
│   └── logo[1-3].png        # Logo variations
├── avatar-animation.js       # Core animation component
├── animated-avatar.html     # Standalone demo
├── integration-example.html # Integration guide
└── README.md               # This documentation
```

## 🚀 Quick Start

### 1. Include the Script
```html
<script src="avatar-assets/avatar-animation.js"></script>
```

### 2. Create Avatar Container
```html
<div id="my-avatar"></div>
```

### 3. Initialize Avatar
```javascript
const avatar = new AvatarAnimation('my-avatar', {
    size: 120,
    avatarType: 'image',
    imagePath: 'avatar-assets/tex/owl.png',
    enableSpeech: true
});
```

## ⚙️ Configuration Options

```javascript
const options = {
    size: 120,                    // Avatar size in pixels
    avatarType: 'image',          // 'image' or 'emoji'
    imagePath: 'path/to/owl.png', // Path to avatar image
    defaultEmoji: '�',           // Fallback emoji
    enableSpeech: true,           // Enable TTS features
    autoAnimations: true          // Enable auto-animations
};
```

## 🎭 Animation Methods

### Basic Animations
```javascript
avatar.playAnimation('bounce');  // Bounce effect
avatar.playAnimation('shake');   // Shake effect
avatar.playAnimation('spin');    // Spin rotation
avatar.playAnimation('glow');    // Glow effect
avatar.playAnimation('pulse');   // Pulse effect
```

### Speech Synthesis
```javascript
// Basic speech
avatar.speak('Hello world!');

// Advanced speech with options
avatar.speak('Custom message', {
    rate: 0.8,    // Speech rate (0.1 to 10)
    pitch: 1.2,   // Voice pitch (0 to 2)
    volume: 0.9   // Volume (0 to 1)
});

// Stop speaking
avatar.stopSpeaking();
```

### Emotion Display
```javascript
avatar.showEmotion('happy');     // 😊
avatar.showEmotion('thinking');  // 🤔
avatar.showEmotion('excited');   // 🤩
avatar.showEmotion('confused');  // 😕
avatar.showEmotion('sleeping');  // 😴
```

### Customization
```javascript
avatar.setSize(160);             // Change size
avatar.setEmoji('👨‍💻');          // Change emoji
avatar.setImage('new/path.png'); // Change image
```

## 🎨 CSS Animations

The component includes these built-in animations:
- **Pulse**: Gentle scaling effect
- **Bounce**: Vertical bouncing motion
- **Shake**: Horizontal shaking
- **Spin**: 360° rotation
- **Glow**: Glowing border effect
- **Speaking**: Subtle movement during speech

## 🔧 Integration Examples

### With Existing Demo
Replace the existing avatar icon in your demo:

```javascript
// Replace emoji with animated avatar
const avatarContainer = document.getElementById('avatarIcon');
const avatar = new AvatarAnimation(avatarContainer.id, {
    size: 80,
    avatarType: 'image',
    imagePath: 'avatar-assets/tex/owl.png'
});

// Connect to TTS events
function onSpeechStart() {
    avatar.startSpeaking();
}

function onSpeechEnd() {
    avatar.stopSpeaking();
}
```

### Responsive Design
```css
/* Mobile responsive */
@media (max-width: 768px) {
    .avatar-animation-wrapper {
        width: 80px !important;
        height: 80px !important;
    }
}
```

## 🎯 Features

### ✅ Core Features
- **Interactive Animations**: Click, hover, and programmatic triggers
- **Speech Synthesis**: Built-in TTS with voice selection
- **Emotion System**: Quick emotion display shortcuts
- **Responsive Design**: Scales to any size
- **Image Support**: Use custom avatar images or emoji fallbacks
- **Event Handling**: Mouse interactions and keyboard shortcuts

### ✅ Technical Features
- **Zero Dependencies**: Pure JavaScript and CSS
- **Lightweight**: < 10KB total size
- **Cross-browser**: Works in all modern browsers
- **Module Support**: CommonJS and global registration
- **Error Handling**: Graceful fallbacks for missing assets

## 🎪 Demo Files

### `animated-avatar.html`
Standalone demo showing all features with interactive controls.

### `integration-example.html`
Complete integration guide with code examples and live demo.

## 🔗 Integration with Main Demo

To integrate with `simple-script-avatar-demo-v2.html`:

1. **Include the script**:
```html
<script src="avatar-assets/avatar-animation.js"></script>
```

2. **Replace avatar icon**:
```javascript
// After audio generation
const avatar = new AvatarAnimation('avatarIcon', {
    size: 60,
    avatarType: 'image',
    imagePath: 'avatar-assets/tex/Lingua.png'
});

// Connect to TTS events
window.currentUtterance.onstart = () => {
    avatar.startSpeaking();
    // ... existing code
};

window.currentUtterance.onend = () => {
    avatar.stopSpeaking();
    // ... existing code
};
```

## 🎨 Customization

### Custom Animations
Add your own CSS animations:

```css
@keyframes myCustomAnimation {
    0% { transform: rotate(0deg) scale(1); }
    50% { transform: rotate(180deg) scale(1.2); }
    100% { transform: rotate(360deg) scale(1); }
}
```

Then use:
```javascript
avatar.avatarWrapper.style.animation = 'myCustomAnimation 2s ease';
```

### Custom Voices
```javascript
// Select specific voice
const voices = speechSynthesis.getVoices();
const preferredVoice = voices.find(v => v.name.includes('Samantha'));

avatar.speak('Hello!', { voice: preferredVoice });
```

## 🚀 Performance Tips

1. **Preload Images**: Load avatar images early
2. **Debounce Animations**: Prevent animation spam
3. **Clean Memory**: Call `avatar.destroy()` when done
4. **Optimize Images**: Use optimized PNG/WebP formats

## 🔧 Browser Compatibility

- **Chrome**: Full support
- **Firefox**: Full support  
- **Safari**: Full support (iOS 14.5+ for TTS)
- **Edge**: Full support
- **Mobile**: Responsive design included

## 📝 License

This avatar animation system is part of the AI Tutor project and follows the same licensing terms.

---

**Created for the HKBU AI Workshop Presentation System** 🎓

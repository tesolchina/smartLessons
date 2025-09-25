/**
 * Animated Avatar Component
 * A reusable avatar animation system for web applications
 */

class AvatarAnimation {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            size: options.size || 120,
            avatarType: options.avatarType || 'emoji', // 'emoji' or 'image'
            imagePath: options.imagePath || 'avatar-assets/tex/owl.png',
            defaultEmoji: options.defaultEmoji || '�',
            enableSpeech: options.enableSpeech !== false,
            autoAnimations: options.autoAnimations !== false,
            ...options
        };
        
        this.isAnimating = false;
        this.isSpeaking = false;
        this.currentAnimation = null;
        
        this.init();
    }
    
    init() {
        this.createAvatarElement();
        this.setupEventListeners();
        
        if (this.options.avatarType === 'image') {
            this.loadAvatarImage();
        }
    }
    
    createAvatarElement() {
        this.container.innerHTML = `
            <div class="avatar-animation-wrapper" style="
                width: ${this.options.size}px;
                height: ${this.options.size}px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.2);
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                cursor: pointer;
                transition: all 0.3s ease;
                overflow: hidden;
            ">
                <div class="avatar-figure" style="
                    font-size: ${this.options.size * 0.6}px;
                    transition: all 0.3s ease;
                ">${this.options.defaultEmoji}</div>
                
                <!-- Speaking indicator -->
                <div class="speaking-rings" style="
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: ${this.options.size + 20}px;
                    height: ${this.options.size + 20}px;
                    border: 2px solid rgba(76, 175, 80, 0.6);
                    border-radius: 50%;
                    opacity: 0;
                    animation: speakingRing 1.5s infinite;
                "></div>
                
                <!-- Animation overlay -->
                <div class="animation-overlay" style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    border-radius: 50%;
                    pointer-events: none;
                "></div>
            </div>
        `;
        
        this.avatarWrapper = this.container.querySelector('.avatar-animation-wrapper');
        this.avatarFigure = this.container.querySelector('.avatar-figure');
        this.speakingRings = this.container.querySelector('.speaking-rings');
        this.animationOverlay = this.container.querySelector('.animation-overlay');
        
        this.addStyles();
    }
    
    addStyles() {
        if (!document.getElementById('avatar-animation-styles')) {
            const styles = document.createElement('style');
            styles.id = 'avatar-animation-styles';
            styles.textContent = `
                @keyframes speakingRing {
                    0% { transform: translate(-50%, -50%) scale(1); opacity: 0.6; }
                    50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.3; }
                    100% { transform: translate(-50%, -50%) scale(1.4); opacity: 0; }
                }
                
                @keyframes avatarPulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                }
                
                @keyframes avatarBounce {
                    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                    40% { transform: translateY(-15px); }
                    60% { transform: translateY(-8px); }
                }
                
                @keyframes avatarShake {
                    0%, 100% { transform: translateX(0); }
                    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
                    20%, 40%, 60%, 80% { transform: translateX(5px); }
                }
                
                @keyframes avatarSpin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                
                @keyframes avatarGlow {
                    0%, 100% { box-shadow: 0 0 20px rgba(255, 255, 255, 0.3); }
                    50% { box-shadow: 0 0 40px rgba(76, 175, 80, 0.8); }
                }
                
                @keyframes speaking {
                    0% { transform: scale(1) rotate(-0.5deg); }
                    50% { transform: scale(1.02) rotate(0.5deg); }
                    100% { transform: scale(1) rotate(-0.5deg); }
                }
                
                .avatar-speaking .avatar-figure {
                    animation: speaking 0.6s infinite;
                }
                
                .avatar-speaking .speaking-rings {
                    opacity: 1 !important;
                }
            `;
            document.head.appendChild(styles);
        }
    }
    
    setupEventListeners() {
        this.avatarWrapper.addEventListener('click', () => {
            if (!this.isAnimating) {
                this.playAnimation('bounce');
            }
        });
        
        this.avatarWrapper.addEventListener('mouseenter', () => {
            if (!this.isAnimating && !this.isSpeaking) {
                this.avatarWrapper.style.transform = 'scale(1.05)';
                this.avatarWrapper.style.boxShadow = '0 10px 30px rgba(255, 255, 255, 0.3)';
            }
        });
        
        this.avatarWrapper.addEventListener('mouseleave', () => {
            if (!this.isAnimating) {
                this.avatarWrapper.style.transform = 'scale(1)';
                this.avatarWrapper.style.boxShadow = 'none';
            }
        });
    }
    
    loadAvatarImage() {
        const img = new Image();
        img.onload = () => {
            this.avatarFigure.innerHTML = `<img src="${this.options.imagePath}" 
                style="width: ${this.options.size * 0.9}px; height: ${this.options.size * 0.9}px; 
                border-radius: 50%; object-fit: cover;" alt="Avatar">`;
        };
        img.onerror = () => {
            console.log('Avatar image failed to load, using emoji fallback');
        };
        img.src = this.options.imagePath;
    }
    
    // Public Methods
    
    speak(text, options = {}) {
        if (!this.options.enableSpeech || !window.speechSynthesis) {
            console.warn('Speech synthesis not available');
            return;
        }
        
        this.startSpeaking();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = options.rate || 0.9;
        utterance.pitch = options.pitch || 1.0;
        utterance.volume = options.volume || 1.0;
        
        // Try to use a good voice
        const voices = speechSynthesis.getVoices();
        const voice = voices.find(v => v.name.includes('Daniel') || v.lang === 'en-GB') || voices[0];
        if (voice) utterance.voice = voice;
        
        utterance.onend = () => this.stopSpeaking();
        utterance.onerror = () => this.stopSpeaking();
        
        speechSynthesis.speak(utterance);
        
        return utterance;
    }
    
    startSpeaking() {
        this.isSpeaking = true;
        this.avatarWrapper.classList.add('avatar-speaking');
    }
    
    stopSpeaking() {
        this.isSpeaking = false;
        this.avatarWrapper.classList.remove('avatar-speaking');
        if (window.speechSynthesis) {
            speechSynthesis.cancel();
        }
    }
    
    playAnimation(type, duration = 2000) {
        if (this.isAnimating) return;
        
        this.isAnimating = true;
        this.currentAnimation = type;
        
        const animations = {
            pulse: () => {
                this.avatarFigure.style.animation = 'avatarPulse 1s infinite';
            },
            bounce: () => {
                this.avatarWrapper.style.animation = 'avatarBounce 1s ease';
            },
            shake: () => {
                this.avatarWrapper.style.animation = 'avatarShake 0.5s infinite';
            },
            spin: () => {
                this.avatarWrapper.style.animation = 'avatarSpin 1s linear';
            },
            glow: () => {
                this.avatarWrapper.style.animation = 'avatarGlow 2s infinite';
            }
        };
        
        if (animations[type]) {
            animations[type]();
            
            setTimeout(() => {
                this.stopAnimation();
            }, duration);
        }
    }
    
    stopAnimation() {
        this.isAnimating = false;
        this.currentAnimation = null;
        this.avatarWrapper.style.animation = '';
        this.avatarFigure.style.animation = '';
    }
    
    setEmoji(emoji) {
        if (!this.avatarFigure.querySelector('img')) {
            this.avatarFigure.textContent = emoji;
        }
    }
    
    setImage(imagePath) {
        this.options.imagePath = imagePath;
        this.options.avatarType = 'image';
        this.loadAvatarImage();
    }
    
    setSize(size) {
        this.options.size = size;
        this.avatarWrapper.style.width = size + 'px';
        this.avatarWrapper.style.height = size + 'px';
        this.avatarFigure.style.fontSize = (size * 0.6) + 'px';
        
        const img = this.avatarFigure.querySelector('img');
        if (img) {
            img.style.width = (size * 0.9) + 'px';
            img.style.height = (size * 0.9) + 'px';
        }
    }
    
    // Emotion shortcuts
    showEmotion(emotion) {
        const emotions = {
            happy: '😊',
            sad: '😢',
            excited: '🤩',
            thinking: '🤔',
            confused: '😕',
            sleeping: '😴',
            angry: '😠',
            surprised: '😮'
        };
        
        if (emotions[emotion]) {
            this.setEmoji(emotions[emotion]);
            this.playAnimation('pulse');
        }
    }
    
    // Integration helpers
    destroy() {
        this.stopSpeaking();
        this.stopAnimation();
        this.container.innerHTML = '';
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AvatarAnimation;
}

// Global registration
window.AvatarAnimation = AvatarAnimation;

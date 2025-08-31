// main.js - Module Coordinator and Initialization

// Bot Configuration - Controls which features are enabled
const BOT_CONFIG = {
    features: {
        promptEditing: true,      // Load prompts.js
        reportGeneration: true,   // Load reports.js
        advancedUI: true,        // Load ui.js (session restore, banners)
        sessionRestore: true     // Enable caching features
    },
    ui: {
        showSystemPrompt: true,   // Show/hide system prompt section
        showWelcomePrompt: true,  // Show/hide welcome section
        enableReports: true       // Show/hide report button
    }
};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing HKBU Chat Assistant...');
    
    // Load user preferences first
    loadPreferencesFromCache();
    
    // Initialize UI warning if advanced UI is enabled
    if (BOT_CONFIG.features.advancedUI) {
        initializeBeforeUnloadWarning();
    }
    
    // Load prompts from files (if prompt editing is enabled)
    if (BOT_CONFIG.features.promptEditing && typeof loadPrompts === 'function') {
        loadPrompts();
    }
    
    // Set up core event listeners
    setupEventListeners();
    
    // Try to restore API key
    const cachedApiKey = loadApiKeyFromCache();
    if (cachedApiKey) {
        document.getElementById('connect-btn').disabled = false;
        showNotification('API key restored from cache', 'info');
    }
    // Restore model selection
        loadModelFromCache();
    
    // Check for previous chat session (if advanced UI is enabled)
    if (BOT_CONFIG.features.sessionRestore && typeof checkForPreviousSession === 'function') {
        checkForPreviousSession();
    }
    
    // Hide UI elements based on configuration
    applyUIConfiguration();
    
    console.log('✅ Chat Assistant initialized successfully');
});

function applyUIConfiguration() {
    // Hide system prompt section if disabled
    if (!BOT_CONFIG.ui.showSystemPrompt) {
        const systemSection = document.querySelector('.prompt-section:has(#system-content)');
        if (systemSection) {
            systemSection.style.display = 'none';
        }
    }
    
    // Hide welcome prompt section if disabled
    if (!BOT_CONFIG.ui.showWelcomePrompt) {
        const welcomeSection = document.querySelector('.prompt-section:has(#welcome-content)');
        if (welcomeSection) {
            welcomeSection.style.display = 'none';
        }
    }
    
    // Hide report button if disabled
    if (!BOT_CONFIG.ui.enableReports) {
        const reportButton = document.getElementById('done-btn');
        if (reportButton) {
            reportButton.style.display = 'none';
        }
    }
}

// Module loader function (for future dynamic loading)
function loadModule(moduleName) {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = `/bots/js/${moduleName}.js`;
        script.onload = () => {
            console.log(`✅ Module ${moduleName} loaded`);
            resolve();
        };
        script.onerror = () => {
            console.error(`❌ Failed to load module ${moduleName}`);
            reject(new Error(`Failed to load ${moduleName}`));
        };
        document.head.appendChild(script);
    });
}

// Configuration helpers for different bot types
function createSimpleBot() {
    return {
        features: {
            promptEditing: false,
            reportGeneration: false,
            advancedUI: false,
            sessionRestore: true
        },
        ui: {
            showSystemPrompt: false,
            showWelcomePrompt: false,
            enableReports: false
        }
    };
}

function createTutorBot() {
    return {
        features: {
            promptEditing: true,
            reportGeneration: true,
            advancedUI: true,
            sessionRestore: true
        },
        ui: {
            showSystemPrompt: true,
            showWelcomePrompt: true,
            enableReports: true
        }
    };
}

function createQuickChatBot() {
    return {
        features: {
            promptEditing: false,
            reportGeneration: false,
            advancedUI: false,
            sessionRestore: false
        },
        ui: {
            showSystemPrompt: false,
            showWelcomePrompt: false,
            enableReports: false
        }
    };
}

// Debug helpers
function getBotStatus() {
    return {
        config: BOT_CONFIG,
        connected: isConnected,
        chatHistory: chatHistory.length,
        modules: {
            core: typeof sendMessage !== 'undefined',
            prompts: typeof loadPrompts !== 'undefined',
            reports: typeof generateReport !== 'undefined',
            ui: typeof checkForPreviousSession !== 'undefined'
        }
    };
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('🚨 Application Error:', e.error);
    showNotification('An error occurred. Please refresh the page.', 'error');
});

// Export configuration for console access
window.BOT_CONFIG = BOT_CONFIG;
window.getBotStatus = getBotStatus;

console.log('📋 Bot Configuration:', BOT_CONFIG);
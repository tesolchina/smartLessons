// core.js - Core Functionality Module

// Global variables
let chatHistory = [];
let isConnected = false;
let apiKey = '';
let welcomePrompt = '';
let systemPrompt = '';
let defaultWelcome = '';
let defaultSystem = '';

// Core system prompt (non-editable, always prepended)
const CORE_SYSTEM_PROMPT = `You are a helpful AI assistant. Follow these formatting guidelines:
• Be concise and clear in your responses
• Use bullet points to organize information when appropriate
• Keep paragraphs short and focused
• Only provide longer explanations when specifically requested
• Structure your responses for easy scanning
• Use headings and lists to improve readability

`;

// Cache variables
const STORAGE_KEYS = {
    API_KEY: 'hkbu_chat_api_key',
    CHAT_HISTORY: 'hkbu_chat_current_session',
    PREFERENCES: 'hkbu_chat_preferences'
};

let userPreferences = {
    rememberApiKey: true,
    saveConversations: true,
    autoRestore: true
};

// ============================================
// EVENT LISTENERS
// ============================================
function setupEventListeners() {
    const messageInput = document.getElementById('message-input');
    if (messageInput) {
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 100) + 'px';
        });
    }

    // Auto-enable connect button when API key is entered
    const apiKeyInput = document.getElementById('api-key');
    if (apiKeyInput) {
        apiKeyInput.addEventListener('input', function() {
            const connectBtn = document.getElementById('connect-btn');
            if (connectBtn) {
                connectBtn.disabled = !this.value.trim();
            }
        });
    }

    // Save model selection when changed
    const modelSelect = document.getElementById('model-select');
    if (modelSelect) {
        modelSelect.addEventListener('change', function() {
            saveModelToCache();
            showNotification(`Model changed to ${this.options[this.selectedIndex].text}`, 'info');
        });
    }
}

// ============================================
// TOGGLE FUNCTIONS
// ============================================
function togglePrompt(type) {
    const contentDiv = document.getElementById(`${type}-content`);
    const toggleIcon = contentDiv?.parentElement?.querySelector('.toggle-icon');
    
    if (!contentDiv || !toggleIcon) return;
    
    if (contentDiv.classList.contains('expanded')) {
        contentDiv.classList.remove('expanded');
        toggleIcon.textContent = '▼';
    } else {
        contentDiv.classList.add('expanded');
        toggleIcon.textContent = '▲';
        
        // Load prompt when expanding system prompt section
        if (type === 'system' && (!systemPrompt || systemPrompt === '')) {
            loadSystemPrompt();
        }
        
        // Load prompt when expanding welcome prompt section
        if (type === 'welcome' && (!welcomePrompt || welcomePrompt === '')) {
            loadWelcomePrompt();
        }
    }
}

function toggleSection(sectionType) {
    const contentDiv = document.getElementById(`${sectionType}-content`);
    const toggleIcon = document.getElementById(`${sectionType}-toggle`);
    
    if (!contentDiv || !toggleIcon) return;
    
    if (contentDiv.classList.contains('expanded')) {
        contentDiv.classList.remove('expanded');
        toggleIcon.textContent = '▼';
    } else {
        contentDiv.classList.add('expanded');
        toggleIcon.textContent = '▲';
    }
}

// ============================================
// PROMPT MANAGEMENT
// ============================================
function updateSystemPromptDisplay() {
    const systemDisplay = document.getElementById('system-display');
    if (systemDisplay) {
        const currentPrompt = systemPrompt || defaultSystem || 'Loading system prompt...';
        systemDisplay.textContent = currentPrompt;
        
        if (currentPrompt.length > 200) {
            systemDisplay.title = `${currentPrompt.length} characters`;
        }
    }
}

function updateWelcomePromptDisplay() {
    const welcomeDisplay = document.getElementById('welcome-display');
    if (welcomeDisplay) {
        const currentPrompt = welcomePrompt || defaultWelcome || 'Loading welcome message...';
        welcomeDisplay.textContent = currentPrompt;
        
        if (currentPrompt.length > 200) {
            welcomeDisplay.title = `${currentPrompt.length} characters`;
        }
    }
}

async function loadSystemPrompt() {
    try {
        const response = await fetch('/aitutor/prompts/system.txt');
        if (response.ok) {
            const content = await response.text();
            defaultSystem = content.trim();
            systemPrompt = defaultSystem;
            updateSystemPromptDisplay();
            console.log('✅ System prompt loaded');
        } else {
            throw new Error('Failed to fetch system prompt');
        }
    } catch (error) {
        console.error('Error loading system prompt:', error);
        defaultSystem = 'You are a helpful AI assistant.';
        systemPrompt = defaultSystem;
        updateSystemPromptDisplay();
    }
}

async function loadWelcomePrompt() {
    try {
        const response = await fetch('/aitutor/prompts/welcome.txt');
        if (response.ok) {
            const content = await response.text();
            defaultWelcome = content.trim();
            welcomePrompt = defaultWelcome;
            updateWelcomePromptDisplay();
            console.log('✅ Welcome prompt loaded');
        } else {
            defaultWelcome = 'Welcome! How can I help you today?';
            welcomePrompt = defaultWelcome;
            updateWelcomePromptDisplay();
        }
    } catch (error) {
        console.error('Error loading welcome prompt:', error);
        defaultWelcome = 'Welcome! How can I help you today?';
        welcomePrompt = defaultWelcome;
        updateWelcomePromptDisplay();
    }
}

function loadPrompts() {
    loadSystemPrompt();
    loadWelcomePrompt();
}

function handleRoleTagClick(role) {
    const rolePrompts = {
        'Math Tutor': 'You are a patient and encouraging math tutor. Help students understand mathematical concepts step by step. Use clear explanations and examples.',
        'Writing Coach': 'You are a writing coach helping students improve their writing skills. Provide constructive feedback, suggest improvements, and help with grammar and style.',
        'Research Assistant': 'You are a research assistant helping students with academic research. Help them find sources, organize information, and develop arguments.',
        'Language Partner': 'You are a friendly language learning partner. Help students practice conversation, correct mistakes gently, and explain grammar and vocabulary.'
    };

    if (rolePrompts[role]) {
        handleSystemPromptEdit(rolePrompts[role]);
    }
}

async function handleSystemPromptEdit(initialPrompt = null) {
    const currentPrompt = initialPrompt || systemPrompt || defaultSystem;
    
    const modal = document.createElement('div');
    modal.className = 'prompt-edit-modal';
    modal.innerHTML = `
        <div class="prompt-edit-content">
            <div class="prompt-edit-header">
                <h3>Edit System Prompt</h3>
                <button class="close-btn" onclick="this.closest('.prompt-edit-modal').remove()">×</button>
            </div>
            <textarea class="prompt-edit-textarea">${currentPrompt}</textarea>
            <div class="prompt-edit-buttons">
                <button class="btn btn-secondary" onclick="this.closest('.prompt-edit-modal').remove()">Cancel</button>
                <button class="btn btn-primary" onclick="saveSystemPrompt(this)">Save Changes</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

async function handleWelcomePromptEdit(initialPrompt = null) {
    const currentPrompt = initialPrompt || welcomePrompt || defaultWelcome;
    
    const modal = document.createElement('div');
    modal.className = 'prompt-edit-modal';
    modal.innerHTML = `
        <div class="prompt-edit-content">
            <div class="prompt-edit-header">
                <h3>Edit Welcome Message</h3>
                <button class="close-btn" onclick="this.closest('.prompt-edit-modal').remove()">×</button>
            </div>
            <textarea class="prompt-edit-textarea">${currentPrompt}</textarea>
            <div class="prompt-edit-buttons">
                <button class="btn btn-secondary" onclick="this.closest('.prompt-edit-modal').remove()">Cancel</button>
                <button class="btn btn-primary" onclick="saveWelcomePrompt(this)">Save Changes</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

async function saveSystemPrompt(button) {
    const modal = button.closest('.prompt-edit-modal');
    const newPrompt = modal.querySelector('.prompt-edit-textarea').value;
    
    if (newPrompt && newPrompt !== systemPrompt) {
        systemPrompt = newPrompt;
        updateSystemPromptDisplay();
        modal.remove();
        startNewSession();
        showNotification('System prompt updated!', 'success');
    } else {
        modal.remove();
    }
}

async function saveWelcomePrompt(button) {
    const modal = button.closest('.prompt-edit-modal');
    const newPrompt = modal.querySelector('.prompt-edit-textarea').value;
    
    if (newPrompt && newPrompt !== welcomePrompt) {
        welcomePrompt = newPrompt;
        updateWelcomePromptDisplay();
        modal.remove();
        showNotification('Welcome message updated!', 'success');
    } else {
        modal.remove();
    }
}

function resetPrompt(type) {
    if (type === 'system') {
        systemPrompt = defaultSystem;
        updateSystemPromptDisplay();
        showNotification('System prompt reset to default', 'info');
    } else if (type === 'welcome') {
        welcomePrompt = defaultWelcome;
        updateWelcomePromptDisplay();
        showNotification('Welcome message reset to default', 'info');
    }
}

// ============================================
// API FUNCTIONS
// ============================================
async function testConnection() {
    const key = document.getElementById('api-key')?.value?.trim();
    const statusDiv = document.getElementById('connection-status');
    
    if (!key) {
        showNotification('Please enter an API key first', 'error');
        return;
    }

    if (statusDiv) {
        statusDiv.style.display = 'block';
        statusDiv.className = 'connection-status status-loading';
        statusDiv.innerHTML = '🔄 Testing connection to HKBU GenAI...';
    }
    
    try {
        const response = await fetch('https://smartlessons-production.up.railway.app/api/test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                apiKey: key,
                provider: 'hkbu',
                model: getSelectedModel()
            })
        });

        const data = await response.json();

        if (response.ok && !data.error) {
            if (statusDiv) {
                statusDiv.className = 'connection-status status-success';
                statusDiv.innerHTML = '✅ Connection successful! API key is valid.';
            }
            const connectBtn = document.getElementById('connect-btn');
            if (connectBtn) connectBtn.disabled = false;
            showNotification('API key is valid!', 'success');
        } else {
            throw new Error(data.error || 'Connection failed');
        }
    } catch (error) {
        if (statusDiv) {
            statusDiv.className = 'connection-status status-error';
            statusDiv.innerHTML = '❌ Connection failed: ' + error.message;
        }
        showNotification(`Connection test failed: ${error.message}`, 'error');
    }
}

async function connectAPI() {
    const key = document.getElementById('api-key')?.value?.trim();
    
    if (!key) {
        showNotification('Please enter an API key', 'error');
        return;
    }

    apiKey = key;
    isConnected = true;
    
    saveApiKeyToCache();
    
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    
    if (messageInput) {
        messageInput.disabled = false;
        messageInput.placeholder = 'Type your message here... (Enter to send)';
    }
    if (sendBtn) sendBtn.disabled = false;
    
    showWelcomeMessage();
    showNotification('API connected successfully!', 'success');
}

function clearAPI() {
    apiKey = '';
    isConnected = false;
    
    const apiKeyInput = document.getElementById('api-key');
    const statusDiv = document.getElementById('connection-status');
    const connectBtn = document.getElementById('connect-btn');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const doneBtn = document.getElementById('done-btn');
    
    if (apiKeyInput) apiKeyInput.value = '';
    if (statusDiv) statusDiv.style.display = 'none';
    if (connectBtn) connectBtn.disabled = true;
    if (messageInput) {
        messageInput.disabled = true;
        messageInput.placeholder = 'Connect your API key first to start chatting...';
    }
    if (sendBtn) sendBtn.disabled = true;
    if (doneBtn) doneBtn.disabled = true;
    
    clearCache(STORAGE_KEYS.API_KEY);
    chatHistory = [];
    clearCache(STORAGE_KEYS.CHAT_HISTORY);
    
    const messagesContainer = document.getElementById('chat-messages');
    if (messagesContainer) {
        messagesContainer.innerHTML = `
            <div class="message assistant">
                <div class="message-content">
                    🔑 Please configure your API key first to start chatting!<br><br>
                    Follow the instructions in the sidebar to get your HKBU GenAI API key and test the connection.
                </div>
            </div>
        `;
    }
    
    showNotification('API disconnected and cache cleared.', 'info');
}

// ============================================
// CHAT FUNCTIONS
// ============================================
async function sendMessage() {
    if (!isConnected) {
        showNotification('Please connect your API key first', 'error');
        return;
    }

    const input = document.getElementById('message-input');
    const message = input?.value?.trim();
    
    if (!message) return;

    addMessage('user', message);
    chatHistory.push({ role: 'user', content: message, timestamp: new Date() });
    saveChatHistoryToCache();
    
    if (input) {
        input.value = '';
        input.style.height = 'auto';
    }
    
    showTyping();
    
    try {
        const response = await fetch('https://smartlessons-production.up.railway.app/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                apiKey: apiKey,
                provider: 'hkbu',
                model: getSelectedModel(),
                systemPrompt: getCombinedSystemPrompt()
            })
        });

        const data = await response.json();
        hideTyping();

        if (response.ok && !data.error) {
            addMessage('assistant', data.response);
            chatHistory.push({ role: 'assistant', content: data.response, timestamp: new Date() });
            saveChatHistoryToCache();
            const doneBtn = document.getElementById('done-btn');
            if (doneBtn) doneBtn.disabled = false;
        } else {
            addMessage('error', `Error: ${data.error || 'Unknown error'}`);
        }
        
    } catch (error) {
        hideTyping();
        addMessage('error', `Network error: ${error.message}`);
    }
}

function addMessage(type, content) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const formattedContent = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
    
    messageDiv.innerHTML = `<div class="message-content">${formattedContent}</div>`;
    messagesContainer.appendChild(messageDiv);
    
    setTimeout(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 100);
}

function showTyping() {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'message assistant';
    typingDiv.innerHTML = '<div class="message-content">🤖 Thinking...</div>';
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideTyping() {
    const typingDiv = document.getElementById('typing-indicator');
    if (typingDiv) typingDiv.remove();
}

function showWelcomeMessage() {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const welcomeMsg = welcomePrompt || defaultWelcome || 'Welcome! How can I help you today?';
    messagesContainer.innerHTML = `
        <div class="message assistant">
            <div class="message-content">${welcomeMsg}</div>
        </div>
    `;
}

// ============================================
// SESSION MANAGEMENT
// ============================================
function startNewSession() {
    const confirmNew = confirm('Start a new session? This will clear the current conversation.');
    
    if (confirmNew) {
        chatHistory = [];
        clearCache(STORAGE_KEYS.CHAT_HISTORY);
        
        showWelcomeMessage();
        
        const messageInput = document.getElementById('message-input');
        const doneBtn = document.getElementById('done-btn');
        
        if (messageInput) messageInput.value = '';
        if (doneBtn) doneBtn.disabled = true;
        
        showNotification('Started new session', 'success');
    }
}

async function generateReport() {
    if (chatHistory.length === 0) {
        showNotification('No conversation to generate report from', 'error');
        return;
    }

    try {
        const reportContent = `# Chat Session Report

**Date:** ${new Date().toLocaleDateString()}
**Time:** ${new Date().toLocaleTimeString()}
**Messages:** ${chatHistory.length}

## Conversation:

${chatHistory.map((msg, index) => {
    const role = msg.role === 'user' ? '**You:**' : '**Assistant:**';
    return `${index + 1}. ${role} ${msg.content}`;
}).join('\n\n')}

---
*Generated by HKBU Learning Assistant*
`;

        // Create downloadable file
        const blob = new Blob([reportContent], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat-report-${new Date().toISOString().split('T')[0]}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        showNotification('Chat report downloaded!', 'success');
    } catch (error) {
        console.error('Error generating report:', error);
        showNotification('Failed to generate report', 'error');
    }
}

// ============================================
// CACHE FUNCTIONS
// ============================================
function saveToCache(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (error) {
        console.error('Failed to save to cache:', error);
        return false;
    }
}

function loadFromCache(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.error('Failed to load from cache:', error);
        return null;
    }
}

function clearCache(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (error) {
        console.error('Failed to clear cache:', error);
        return false;
    }
}

function encodeApiKey(key) {
    return btoa(key);
}

function decodeApiKey(encodedKey) {
    try {
        return atob(encodedKey);
    } catch (error) {
        return null;
    }
}

function saveApiKeyToCache() {
    if (userPreferences.rememberApiKey && apiKey) {
        const encodedKey = encodeApiKey(apiKey);
        saveToCache(STORAGE_KEYS.API_KEY, encodedKey);
    }
}

function loadApiKeyFromCache() {
    if (userPreferences.rememberApiKey) {
        const encodedKey = loadFromCache(STORAGE_KEYS.API_KEY);
        if (encodedKey) {
            const decodedKey = decodeApiKey(encodedKey);
            if (decodedKey) {
                const apiKeyInput = document.getElementById('api-key');
                if (apiKeyInput) apiKeyInput.value = decodedKey;
                return decodedKey;
            }
        }
    }
    return null;
}

function saveChatHistoryToCache() {
    if (userPreferences.saveConversations && chatHistory.length > 0) {
        const sessionData = {
            messages: chatHistory,
            startTime: chatHistory[0]?.timestamp || new Date(),
            lastActivity: new Date(),
            messageCount: chatHistory.length,
            customPrompts: {
                welcome: welcomePrompt,
                system: systemPrompt
            }
        };
        saveToCache(STORAGE_KEYS.CHAT_HISTORY, sessionData);
    }
}

function loadChatHistoryFromCache() {
    if (userPreferences.saveConversations) {
        return loadFromCache(STORAGE_KEYS.CHAT_HISTORY);
    }
    return null;
}

function savePreferencesToCache() {
    saveToCache(STORAGE_KEYS.PREFERENCES, userPreferences);
}

function loadPreferencesFromCache() {
    const savedPrefs = loadFromCache(STORAGE_KEYS.PREFERENCES);
    if (savedPrefs) {
        userPreferences = { ...userPreferences, ...savedPrefs };
    }
}

function saveModelToCache() {
    const selectedModel = getSelectedModel();
    saveToCache('hkbu_selected_model', selectedModel);
}

function loadModelFromCache() {
    const savedModel = loadFromCache('hkbu_selected_model');
    if (savedModel) {
        const modelSelect = document.getElementById('model-select');
        if (modelSelect) modelSelect.value = savedModel;
    }
}

// ============================================
// UTILITY FUNCTIONS
// ============================================
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'notification ' + type;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 4000);
}

function getSelectedModel() {
    const modelSelect = document.getElementById('model-select');
    return modelSelect ? modelSelect.value : 'gpt-4.1-mini';
}

function getCombinedSystemPrompt() {
    const userSystemPrompt = systemPrompt || '';
    return CORE_SYSTEM_PROMPT + userSystemPrompt;
}

// ============================================
// INITIALIZATION
// ============================================
function initializeSections() {
    console.log('🔧 Initializing sections...');
    
    const apiContent = document.getElementById('api-content');
    const systemContent = document.getElementById('system-content');
    const welcomeContent = document.getElementById('welcome-content');
    const apiToggle = document.getElementById('api-toggle');
    const systemToggle = document.querySelector('.prompt-header .toggle-icon');
    
    // Start sections collapsed
    if (apiContent) {
        apiContent.classList.remove('expanded');
        console.log('✅ API section collapsed');
    } else {
        console.log('❌ API content element not found');
    }
    
    if (systemContent) {
        systemContent.classList.remove('expanded');
        console.log('✅ System section collapsed');
    } else {
        console.log('❌ System content element not found');
    }
    
    if (welcomeContent) {
        welcomeContent.classList.remove('expanded');
        console.log('✅ Welcome section collapsed');
    } else {
        console.log('❌ Welcome content element not found');
    }
    
    // Set toggle icons
    if (apiToggle) {
        apiToggle.textContent = '▼';
        console.log('✅ API toggle icon set');
    } else {
        console.log('❌ API toggle element not found');
    }
    
    if (systemToggle) {
        systemToggle.textContent = '▼';
        console.log('✅ System toggle icon set');
    } else {
        console.log('❌ System toggle element not found');
    }
}

// ============================================
// GLOBAL EXPORTS
// ============================================
window.togglePrompt = togglePrompt;
window.toggleSection = toggleSection;
window.handleRoleTagClick = handleRoleTagClick;
window.handleSystemPromptEdit = handleSystemPromptEdit;
window.handleWelcomePromptEdit = handleWelcomePromptEdit;
window.saveSystemPrompt = saveSystemPrompt;
window.saveWelcomePrompt = saveWelcomePrompt;
window.updateWelcomePromptDisplay = updateWelcomePromptDisplay;
window.resetPrompt = resetPrompt;
window.testConnection = testConnection;
window.connectAPI = connectAPI;
window.clearAPI = clearAPI;
window.sendMessage = sendMessage;
window.startNewSession = startNewSession;
window.showWelcomeMessage = showWelcomeMessage;
window.generateReport = generateReport;

// ============================================
// DOM READY INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing AI Tutor...');
    
    try {
        setupEventListeners();
        loadPreferencesFromCache();
        loadModelFromCache();
        loadApiKeyFromCache();
        initializeSections();
        loadPrompts();
        
        console.log('✅ AI Tutor initialized successfully');
    } catch (error) {
        console.error('❌ Error initializing AI Tutor:', error);
    }
});
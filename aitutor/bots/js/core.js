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

// Event listeners setup
function setupEventListeners() {
    const messageInput = document.getElementById('message-input');
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

    // Auto-enable connect button when API key is entered
    document.getElementById('api-key').addEventListener('input', function() {
        const connectBtn = document.getElementById('connect-btn');
        if (this.value.trim()) {
            connectBtn.disabled = false;
        } else {
            connectBtn.disabled = true;
        }
    });
    // Save model selection when changed
        const modelSelect = document.getElementById('model-select');
        if (modelSelect) {
            modelSelect.addEventListener('change', function() {
                saveModelToCache();
                showNotification(`Model changed to ${this.options[this.selectedIndex].text}`, 'info');
            });
        }
}

// Add after setupEventListeners function
function togglePrompt(type) {
    const contentDiv = document.getElementById(`${type}-content`);
    const toggleIcon = contentDiv.parentElement.querySelector('.toggle-icon');
    
    if (contentDiv.classList.contains('expanded')) {
        contentDiv.classList.remove('expanded');
        toggleIcon.textContent = '▼';
    } else {
        contentDiv.classList.add('expanded');
        toggleIcon.textContent = '▲';
        
        // Scroll prompt into view if needed
        const promptDisplay = contentDiv.querySelector('.prompt-display');
        if (promptDisplay && promptDisplay.scrollHeight > promptDisplay.clientHeight) {
            promptDisplay.scrollTop = 0;
        }
    }
}

// Make function available globally
window.togglePrompt = togglePrompt;
 

// Add after the existing togglePrompt function
function toggleSection(sectionType) {
    const contentDiv = document.getElementById(`${sectionType}-content`);
    const toggleIcon = document.getElementById(`${sectionType}-toggle`);
    
    if (contentDiv.classList.contains('expanded')) {
        contentDiv.classList.remove('expanded');
        toggleIcon.textContent = '▼';
    } else {
        contentDiv.classList.add('expanded');
        toggleIcon.textContent = '▲';
    }
}

// Make function available globally
window.toggleSection = toggleSection;

// System prompt display function
function updateSystemPromptDisplay() {
    const systemDisplay = document.getElementById('system-display');
    if (systemDisplay) {
        const currentPrompt = systemPrompt || defaultSystem || 'Loading system prompt...';
        systemDisplay.textContent = currentPrompt;
        
        // Show character count for long prompts
        if (currentPrompt.length > 200) {
            systemDisplay.title = `${currentPrompt.length} characters`;
        }
    }
}

// Load and display system prompt from file
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

// Load prompts function (called by main.js)
function loadPrompts() {
    loadSystemPrompt();
}


// Role tag click handler
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

// Make functions available globally
window.updateSystemPromptDisplay = updateSystemPromptDisplay;
window.loadSystemPrompt = loadSystemPrompt;
window.loadPrompts = loadPrompts;
window.handleRoleTagClick = handleRoleTagClick;





// API Functions
async function testConnection() {
    const key = document.getElementById('api-key').value.trim();
    const statusDiv = document.getElementById('connection-status');
    
    if (!key) {
        showNotification('Please enter an API key first', 'error');
        return;
    }

    statusDiv.style.display = 'block';
    statusDiv.className = 'connection-status status-loading';
    statusDiv.innerHTML = '🔄 Testing connection to HKBU GenAI...';
    
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
            statusDiv.className = 'connection-status status-success';
            statusDiv.innerHTML = '✅ Connection successful! API key is valid.';
            document.getElementById('connect-btn').disabled = false;
            showNotification('API key is valid!', 'success');
        } else {
            throw new Error(data.error || 'Connection failed');
        }
    } catch (error) {
        statusDiv.className = 'connection-status status-error';
        statusDiv.innerHTML = '❌ Connection failed: ' + error.message;
        showNotification(`Connection test failed: ${error.message}`, 'error');
    }
}

async function connectAPI() {
    const key = document.getElementById('api-key').value.trim();
    
    if (!key) {
        showNotification('Please enter an API key', 'error');
        return;
    }

    apiKey = key;
    isConnected = true;
    
    // Save API key to cache
    saveApiKeyToCache();
    
    document.getElementById('message-input').disabled = false;
    document.getElementById('message-input').placeholder = 'Type your message here... (Enter to send)';
    document.getElementById('send-btn').disabled = false;
    
    // Show welcome message with loaded content (if prompts module is loaded)
    if (typeof showWelcomeMessage === 'function') {
        showWelcomeMessage();
    }
    showNotification('API connected successfully!', 'success');
}

function clearAPI() {
    apiKey = '';
    isConnected = false;
    document.getElementById('api-key').value = '';
    document.getElementById('connection-status').style.display = 'none';
    document.getElementById('connect-btn').disabled = true;
    document.getElementById('message-input').disabled = true;
    document.getElementById('message-input').placeholder = 'Connect your API key first to start chatting...';
    document.getElementById('send-btn').disabled = true;
    document.getElementById('done-btn').disabled = true;
    
    // Clear API key from cache
    clearCache(STORAGE_KEYS.API_KEY);
    
    // Reset chat
    chatHistory = [];
    clearCache(STORAGE_KEYS.CHAT_HISTORY);
    
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.innerHTML = `
        <div class="message assistant">
            <div class="message-content">
                🔑 Please configure your API key first to start chatting!<br><br>
                Follow the instructions in the sidebar to get your HKBU GenAI API key and test the connection.
            </div>
        </div>
    `;
    
    showNotification('API disconnected and cache cleared.', 'info');
}

// Chat Functions
async function sendMessage() {
    if (!isConnected) {
        showNotification('Please connect your API key first', 'error');
        return;
    }

    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message) return;

    // Add user message
    addMessage('user', message);
    chatHistory.push({ role: 'user', content: message, timestamp: new Date() });
    saveChatHistoryToCache();
    
    input.value = '';
    input.style.height = 'auto';
    
    // Show typing indicator
    showTyping();
    
    try {
        const response = await fetch('https://smartlessons-production.up.railway.app/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                apiKey: apiKey,
                provider: 'hkbu',
                model: 'gpt-4.1',
                systemPrompt: getCombinedSystemPrompt()
            })
        });

        const data = await response.json();
        hideTyping();

        if (response.ok && !data.error) {
            addMessage('assistant', data.response);
            chatHistory.push({ role: 'assistant', content: data.response, timestamp: new Date() });
            saveChatHistoryToCache();
            document.getElementById('done-btn').disabled = false;
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
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    // Convert markdown-style formatting to HTML
    const formattedContent = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>')             // Italic
        .replace(/\n/g, '<br>');                          // Line breaks
    
    messageDiv.innerHTML = `
        <div class="message-content">${formattedContent}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    
    // Force scroll to bottom
    setTimeout(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 100);
}

function showTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'message assistant';
    typingDiv.innerHTML = '<div class="message-content">🤖 Thinking...</div>';
    
    document.getElementById('chat-messages').appendChild(typingDiv);
    document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
}

function hideTyping() {
    const typingDiv = document.getElementById('typing-indicator');
    if (typingDiv) {
        typingDiv.remove();
    }
}

// Session Management
function startNewSession() {
    // Show confirmation dialog
    const confirmNew = confirm('Start a new session? This will clear the current conversation.');
    
    if (confirmNew) {
        // Clear chat history
        chatHistory = [];
        
        // Clear chat messages display
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = `
            <div class="message assistant">
                <div class="message-content">
                    🔄 Starting new session...<br><br>
                    How can I help you today?
                </div>
            </div>
        `;
        
        // Reset any session-specific variables
        document.getElementById('message-input').value = '';
        document.getElementById('done-btn').disabled = true;
        
        // Clear cached chat history
        clearCache(STORAGE_KEYS.CHAT_HISTORY);
        
        // Show notification
        showNotification('Started new session', 'success');
    }
}

// System Prompt Management
async function updateSystemPrompt(newPrompt) {
    try {
        const response = await fetch('/api/system-prompt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',  // Important for session handling
            body: JSON.stringify({
                systemPrompt: newPrompt
            })
        });
        
        if (response.ok) {
            systemPrompt = newPrompt;  // Update local variable
            saveChatHistoryToCache();  // Save to cache with new prompt
            startNewSession();         // Start fresh session
            return true;
        } else {
            throw new Error('Failed to update system prompt');
        }
    } catch (error) {
        console.error('Error updating system prompt:', error);
        showNotification('Failed to update system prompt', 'error');
        return false;
    }
}

// Add after the updateSystemPrompt function but before the Cache utility functions
async function handleSystemPromptEdit(initialPrompt = null) {
    const currentPrompt = initialPrompt || systemPrompt || defaultSystem;
    
    // Create modal for editing
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

// Add this helper function right after handleSystemPromptEdit
async function saveSystemPrompt(button) {
    const modal = button.closest('.prompt-edit-modal');
    const newPrompt = modal.querySelector('.prompt-edit-textarea').value;
    
    if (newPrompt && newPrompt !== systemPrompt) {
        const success = await updateSystemPrompt(newPrompt);
        if (success) {
            modal.remove();
            startNewSession();
        }
    } else {
        modal.remove();
    }
}




// Make function available globally
window.startNewSession = startNewSession;
window.updateSystemPrompt = updateSystemPrompt;
window.handleSystemPromptEdit = handleSystemPromptEdit;
window.saveSystemPrompt = saveSystemPrompt;

// Cache utility functions
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
    // Simple encoding (not encryption, just obfuscation)
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
                document.getElementById('api-key').value = decodedKey;
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

// Notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'notification ' + type;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 4000);
}

// Helper function to get selected model
function getSelectedModel() {
    const modelSelect = document.getElementById('model-select');
    return modelSelect ? modelSelect.value : 'gpt-4.1-mini';
}

// Helper function to combine core and user system prompts
function getCombinedSystemPrompt() {
    const userSystemPrompt = systemPrompt || '';
    return CORE_SYSTEM_PROMPT + userSystemPrompt;
}

// Save model selection to cache
function saveModelToCache() {
    const selectedModel = getSelectedModel();
    saveToCache('hkbu_selected_model', selectedModel);
}

// Load model selection from cache
function loadModelFromCache() {
    const savedModel = loadFromCache('hkbu_selected_model');
    if (savedModel) {
        const modelSelect = document.getElementById('model-select');
        if (modelSelect) {
            modelSelect.value = savedModel;
        }
    }
}


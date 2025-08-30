// video.js
// Avoid redeclaring variables that might be in core.js
let systemPrompt = '';
let welcomePrompt = '';

// Load prompts when page loads
window.onload = async function() {
    try {
        // Load system prompt
        const sysResponse = await fetch('/aitutor/prompts/videoS.txt');
        systemPrompt = await sysResponse.text();

        // Load welcome prompt
        const welcomeResponse = await fetch('/aitutor/prompts/videoW.txt');
        welcomePrompt = await welcomeResponse.text();
    } catch (error) {
        console.error('Error loading prompts:', error);
        systemPrompt = 'You are a helpful assistant for EEGC students preparing their 2-minute pre-course video.';
        welcomePrompt = 'Hello! I\'m here to help you prepare your video presentation.';
    }
};

// Function to start the chat session
function connectAPI() {
    // Store API key locally to avoid global conflict
    const localApiKey = document.getElementById('api-key').value;
    if (!localApiKey) {
        alert('Please enter your API key');
        return;
    }

    document.querySelector('.api-section').style.display = 'none';
    document.getElementById('chat-container').style.display = 'block';
    addMessage(welcomePrompt, 'assistant');
    
    // Store API key in a way that avoids global conflict
    window.videoHelperApiKey = localApiKey;
}

// Function to add a message to the chat
function addMessage(text, sender) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Function to send a message to the API
function sendMessage() {
    const input = document.getElementById('user-input'); // Changed from 'message-input' to match videoHelper.html
    const message = input.value.trim();
    const model = document.getElementById('model-select').value;
    
    if (!message) return;

    addMessage(message, 'user');
    input.value = '';

    fetch('/aitutor/api/chat', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            apiKey: window.videoHelperApiKey, // Use the stored local key
            provider: 'hkbu',
            model: model,
            systemPrompt: systemPrompt
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        addMessage(data.response, 'assistant');
    })
    .catch(error => {
        addMessage('Error: ' + error.message, 'assistant');
        console.error('Error:', error);
    });
}

// Handle Enter key in textarea
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
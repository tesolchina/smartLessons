// video.js
// Use highly unique variable names to avoid any conflicts with core.js or other scripts
let videoHelperSysPrompt = '';
let videoHelperWelcomeMsg = '';

// Load prompts when page loads
window.onload = async function() {
    try {
        // Load system prompt
        const sysResponse = await fetch('/aitutor/prompts/videoS.txt');
        videoHelperSysPrompt = await sysResponse.text();

        // Load welcome prompt
        const welcomeResponse = await fetch('/aitutor/prompts/videoW.txt');
        videoHelperWelcomeMsg = await welcomeResponse.text();
    } catch (error) {
        console.error('Error loading prompts:', error);
        videoHelperSysPrompt = 'You are a helpful assistant for EEGC students preparing their 2-minute pre-course video.';
        videoHelperWelcomeMsg = 'Hello! I\'m here to help you prepare your video presentation.';
    }
};

// Function to start the chat session
function connectAPI() {
    // Store API key locally to avoid global conflict
    const videoHelperKey = document.getElementById('api-key').value;
    if (!videoHelperKey) {
        alert('Please enter your API key');
        return;
    }

    document.querySelector('.api-section').style.display = 'none';
    document.getElementById('chat-container').style.display = 'block';
    addMessage(videoHelperWelcomeMsg, 'assistant');
    
    // Store API key in a way that avoids global conflict
    window.videoHelperUniqueKey = videoHelperKey;
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
    const input = document.getElementById('user-input');
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
            apiKey: window.videoHelperUniqueKey, // Use the stored local key
            provider: 'hkbu',
            model: model,
            systemPrompt: videoHelperSysPrompt
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
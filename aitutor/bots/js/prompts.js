// prompts.js - Prompt Management Module

async function loadPrompts() {
    try {
        // Load welcome prompt from backend API
        const welcomeResponse = await fetch('https://smartlessons-production.up.railway.app/prompts/welcome.txt');
        if (welcomeResponse.ok) {
            const welcomeData = await welcomeResponse.json();
            defaultWelcome = welcomeData.content;
            welcomePrompt = defaultWelcome;
            console.log('✅ Welcome prompt loaded from file');
        } else {
            throw new Error('Failed to load welcome.txt');
        }

        // Load system prompt from backend API
        const systemResponse = await fetch('https://smartlessons-production.up.railway.app/prompts/system.txt');
        if (systemResponse.ok) {
            const systemData = await systemResponse.json();
            defaultSystem = systemData.content;
            systemPrompt = defaultSystem;
            console.log('✅ System prompt loaded from file');
        } else {
            throw new Error('Failed to load system.txt');
        }

        // Update displays
        updatePromptDisplay('welcome');
        updatePromptDisplay('system');
        
        showNotification('Prompts loaded from files successfully!', 'success');
        
    } catch (error) {
        console.error('❌ Error loading prompts from files:', error);
        
        // Fallback to hardcoded defaults
        defaultWelcome = `Welcome to the HKBU Learning Assistant! 🎓

I'm here to help you explore various topics and enhance your learning experience. You can customize my behavior by editing the system prompt below.

🔧 **How to customize:**
- Click 'Edit System Prompt' to modify my personality and expertise
- Try different roles: tutor, writing coach, research assistant, etc.
- Experiment with different teaching styles

💡 **Tips:**
- Ask me to explain concepts step-by-step
- Request examples and practice problems
- Get help with assignments and projects

When you're done with our conversation, click 'Done' to generate a comprehensive learning report!

Let's start learning together!`;

        defaultSystem = `You are a knowledgeable and friendly educational assistant for HKBU students. Your role is to:

1. **Teaching Style**: Explain concepts clearly with examples, encourage critical thinking, and adapt to different learning styles.

2. **Subject Expertise**: Help with various academic subjects including language learning, sciences, humanities, and general study skills.

3. **Interaction Approach**: 
   - Ask clarifying questions to understand student needs
   - Provide step-by-step explanations
   - Encourage students to think through problems
   - Offer constructive feedback and encouragement

4. **Learning Support**: 
   - Break down complex topics into manageable parts
   - Suggest additional resources when helpful
   - Help students develop study strategies
   - Foster independent learning skills

5. **Communication**: Be encouraging, patient, and supportive. Use clear language appropriate for university-level students.

Remember: Guide students toward understanding rather than simply providing answers.`;

        welcomePrompt = defaultWelcome;
        systemPrompt = defaultSystem;
        
        updatePromptDisplay('welcome');
        updatePromptDisplay('system');
        
        showNotification('Using default prompts (files not accessible)', 'info');
    }
}

function togglePrompt(section) {
    const content = document.getElementById(section + '-content');
    const header = content.previousElementSibling;
    const icon = header.querySelector('.toggle-icon');
    
    content.classList.toggle('hidden');
    header.classList.toggle('collapsed');
}

function updatePromptDisplay(type) {
    const display = document.getElementById(type + '-display');
    const prompt = type === 'welcome' ? welcomePrompt : systemPrompt;
    display.textContent = prompt;
}

function editPrompt(type) {
    const display = document.getElementById(type + '-display');
    const currentText = type === 'welcome' ? welcomePrompt : systemPrompt;
    
    const textarea = document.createElement('textarea');
    textarea.className = 'prompt-editor';
    textarea.value = currentText;
    
    display.parentNode.replaceChild(textarea, display);
    
    // Replace buttons
    const buttonsContainer = textarea.nextElementSibling;
    buttonsContainer.innerHTML = `
        <button class="btn btn-success" onclick="savePrompt('${type}')">Save</button>
        <button class="btn btn-secondary" onclick="cancelEdit('${type}')">Cancel</button>
    `;
    
    textarea.focus();
}

function savePrompt(type) {
    const textarea = document.querySelector('.prompt-editor');
    const newText = textarea.value;
    
    if (type === 'welcome') {
        welcomePrompt = newText;
    } else {
        systemPrompt = newText;
    }
    
    cancelEdit(type);
    showNotification(`${type === 'welcome' ? 'Welcome' : 'System'} prompt updated! (Resets on page refresh)`, 'success');
    saveChatHistoryToCache();
    
    // Update welcome message if connected and editing welcome
    if (type === 'welcome' && isConnected) {
        showWelcomeMessage();
    }
}

function cancelEdit(type) {
    const textarea = document.querySelector('.prompt-editor');
    const display = document.createElement('div');
    display.className = 'prompt-display';
    display.id = type + '-display';
    
    textarea.parentNode.replaceChild(display, textarea);
    
    // Restore buttons
    const buttonsContainer = display.nextElementSibling;
    if (type === 'welcome') {
        buttonsContainer.innerHTML = `
            <button class="btn btn-primary" onclick="editPrompt('welcome')">Edit Welcome</button>
            <button class="btn btn-secondary" onclick="resetPrompt('welcome')">Reset</button>
        `;
    } else {
        buttonsContainer.innerHTML = `
            <button class="btn btn-primary" onclick="editPrompt('system')">Edit System</button>
            <button class="btn btn-secondary" onclick="resetPrompt('system')">Reset</button>
            <div style="margin-top: 10px;">
                <small style="color: #666;">💡 Try roles like: Math Tutor, Writing Coach, Research Assistant, Language Partner</small>
            </div>
        `;
    }
    
    updatePromptDisplay(type);
}

function resetPrompt(type) {
    if (type === 'welcome') {
        welcomePrompt = defaultWelcome;
    } else {
        systemPrompt = defaultSystem;
    }
    updatePromptDisplay(type);
    showNotification(`${type === 'welcome' ? 'Welcome' : 'System'} prompt reset to default`, 'info');
    
    // Update welcome message if connected and resetting welcome
    if (type === 'welcome' && isConnected) {
        showWelcomeMessage();
    }
}

function showWelcomeMessage() {
    if (!isConnected) return; // Only show when connected
    
    const messagesContainer = document.getElementById('chat-messages');
    const formattedWelcome = welcomePrompt
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
    
    messagesContainer.innerHTML = `
        <div class="message assistant">
            <div class="message-content">${formattedWelcome}</div>
        </div>
    `;
    
    setTimeout(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }, 100);
}
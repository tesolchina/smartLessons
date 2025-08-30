// prompts.js - Prompt Management Module

let currentEditingPrompt = null;
let defaultPrompts = {
    welcome: "Welcome to HKBU Chat Assistant! I'm here to help you learn and explore. How can I assist you today?",
    system: "You are a helpful AI learning assistant at HKBU, designed to support students in their academic journey."
};

// Load prompts from files
async function loadPrompts() {
    try {
        const welcomeResponse = await fetch('prompts/welcome.txt');
        const systemResponse = await fetch('prompts/system.txt');
        
        if (welcomeResponse.ok && systemResponse.ok) {
            defaultPrompts.welcome = await welcomeResponse.text();
            defaultPrompts.system = await systemResponse.text();
        }
    } catch (error) {
        console.log('Using default prompts:', error);
    }

    // Initialize displays
    document.getElementById('welcome-display').textContent = defaultPrompts.welcome;
    document.getElementById('system-display').textContent = defaultPrompts.system;
}

// Toggle prompt sections
function togglePrompt(type) {
    const content = document.getElementById(`${type}-content`);
    const header = content.previousElementSibling;
    const icon = header.querySelector('.toggle-icon');
    
    if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        icon.textContent = '▼';
    } else {
        content.classList.add('hidden');
        icon.textContent = '▶';
    }
}

// Edit prompt in modal
function editPrompt(type) {
    currentEditingPrompt = type;
    const modal = document.getElementById('prompt-edit-modal');
    const textarea = document.getElementById('prompt-edit-textarea');
    const title = document.getElementById('prompt-edit-title');
    
    // Set the title based on type
    title.textContent = `Edit ${type.charAt(0).toUpperCase() + type.slice(1)} Prompt`;
    
    // Get current content
    const currentContent = document.getElementById(`${type}-display`).textContent;
    textarea.value = currentContent;
    
    // Show modal
    modal.style.display = 'flex';
    textarea.focus();
}

// Close prompt edit modal
function closePromptEdit() {
    const modal = document.getElementById('prompt-edit-modal');
    modal.style.display = 'none';
    currentEditingPrompt = null;
}

// Save prompt changes
function savePromptEdit() {
    if (!currentEditingPrompt) return;
    
    const textarea = document.getElementById('prompt-edit-textarea');
    const newContent = textarea.value.trim();
    
    if (newContent) {
        // Update the display
        document.getElementById(`${currentEditingPrompt}-display`).textContent = newContent;
        
        // Update the default prompts object
        defaultPrompts[currentEditingPrompt] = newContent;
        
        // Show success notification
        showNotification('Prompt updated successfully!', 'success');
    }
    
    // Close modal
    closePromptEdit();
}

// Reset prompt to default
function resetPrompt(type) {
    const confirmReset = confirm('Are you sure you want to reset this prompt to its default value?');
    
    if (confirmReset) {
        document.getElementById(`${type}-display`).textContent = defaultPrompts[type];
        showNotification('Prompt reset to default', 'info');
    }
}

// Initialize prompts when the page loads
document.addEventListener('DOMContentLoaded', () => {
    loadPrompts();
    
    // Add event listener for clicking outside the modal
    const modal = document.getElementById('prompt-edit-modal');
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closePromptEdit();
        }
    });
    
    // Add event listener for Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && currentEditingPrompt) {
            closePromptEdit();
        }
    });
});

// Export necessary functions and variables
window.editPrompt = editPrompt;
window.closePromptEdit = closePromptEdit;
window.savePromptEdit = savePromptEdit;
window.resetPrompt = resetPrompt;
window.togglePrompt = togglePrompt;
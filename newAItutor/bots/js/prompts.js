// prompts.js - Minimal conflict-free version

console.log('📄 prompts.js loading (minimal version)...');

// This file is now just a compatibility layer
// All real functionality is in core.js

// Simple state for this module only
let promptsModuleState = {
    initialized: false
};

// Only provide fallback functions if core.js versions don't exist
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        // Check if core.js has already defined these functions
        if (typeof window.handleWelcomePromptEdit !== 'function') {
            window.handleWelcomePromptEdit = function() {
                console.log('⚠️ handleWelcomePromptEdit called but not implemented');
                alert('Welcome prompt editing not available');
            };
        }
        
        if (typeof window.handleSystemPromptEdit !== 'function') {
            window.handleSystemPromptEdit = function() {
                console.log('⚠️ handleSystemPromptEdit called but not implemented');
                alert('System prompt editing not available');
            };
        }
        
        if (typeof window.togglePrompt !== 'function') {
            window.togglePrompt = function(type) {
                console.log('⚠️ togglePrompt called for', type);
            };
        }
        
        if (typeof window.resetPrompt !== 'function') {
            window.resetPrompt = function(type) {
                console.log('⚠️ resetPrompt called for', type);
            };
        }
        
        promptsModuleState.initialized = true;
        console.log('✅ prompts.js minimal initialization complete');
    }, 100);
});

console.log('✅ prompts.js loaded (minimal version)');
// ui.js - UI Enhancement Module (Session restore, modals, etc.)

function checkForPreviousSession() {
    const sessionData = loadChatHistoryFromCache();
    if (sessionData && sessionData.messages.length > 0) {
        const timeDiff = new Date() - new Date(sessionData.lastActivity);
        const hoursSinceLastActivity = timeDiff / (1000 * 60 * 60);
        
        if (hoursSinceLastActivity < 2 && userPreferences.autoRestore) {
            // Auto-restore recent sessions
            restoreSession(sessionData);
            showNotification(`Previous session restored (${sessionData.messageCount} messages)`, 'success');
        } else if (hoursSinceLastActivity < 24) {
            // Prompt user for older sessions
            showSessionRestorePrompt(sessionData);
        } else {
            // Clear very old sessions
            clearCache(STORAGE_KEYS.CHAT_HISTORY);
        }
    }
}

function showSessionRestorePrompt(sessionData) {
    const timeDiff = new Date() - new Date(sessionData.lastActivity);
    const hours = Math.floor(timeDiff / (1000 * 60 * 60));
    const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
    
    const timeAgo = hours > 0 ? `${hours}h ${minutes}m ago` : `${minutes}m ago`;
    
    // Create restore banner
    const banner = document.createElement('div');
    banner.id = 'session-restore-banner';
    banner.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        text-align: center;
        z-index: 3000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;
    
    banner.innerHTML = `
        <div style="max-width: 800px; margin: 0 auto;">
            <strong>📚 Previous learning session found</strong><br>
            ${sessionData.messageCount} messages • ${timeAgo}
            <div style="margin-top: 10px;">
                <button onclick="restoreSession(${JSON.stringify(sessionData).replace(/"/g, '&quot;')}); closeBanner()" 
                        style="background: white; color: #667eea; border: none; padding: 8px 16px; margin: 0 5px; border-radius: 5px; cursor: pointer;">
                    Continue Session
                </button>
                <button onclick="startFreshSession(); closeBanner()" 
                        style="background: rgba(255,255,255,0.2); color: white; border: 1px solid white; padding: 8px 16px; margin: 0 5px; border-radius: 5px; cursor: pointer;">
                    Start Fresh
                </button>
                <button onclick="closeBanner()" 
                        style="background: none; color: white; border: none; padding: 8px 16px; margin: 0 5px; cursor: pointer; text-decoration: underline;">
                    Decide Later
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(banner);
}

function restoreSession(sessionData) {
    try {
        // Restore chat history
        chatHistory = sessionData.messages.map(msg => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
        }));
        
        // Restore custom prompts if they exist (if prompts module is loaded)
        if (sessionData.customPrompts && typeof updatePromptDisplay === 'function') {
            if (sessionData.customPrompts.welcome) {
                welcomePrompt = sessionData.customPrompts.welcome;
                updatePromptDisplay('welcome');
            }
            if (sessionData.customPrompts.system) {
                systemPrompt = sessionData.customPrompts.system;
                updatePromptDisplay('system');
            }
        }
        
        // Restore chat display
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.innerHTML = '';
        
        chatHistory.forEach(msg => {
            addMessage(msg.role, msg.content);
        });
        
        // Enable done button if there are messages
        if (chatHistory.length > 0) {
            document.getElementById('done-btn').disabled = false;
        }
        
    } catch (error) {
        console.error('Failed to restore session:', error);
        showNotification('Failed to restore previous session', 'error');
        startFreshSession();
    }
}

function startFreshSession() {
    // Clear current session
    chatHistory = [];
    clearCache(STORAGE_KEYS.CHAT_HISTORY);
    
    // Reset chat display
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.innerHTML = `
        <div class="message assistant">
            <div class="message-content">
                🔑 Please configure your API key first to start chatting!<br><br>
                Follow the instructions in the sidebar to get your HKBU GenAI API key and test the connection.
            </div>
        </div>
    `;
    
    // Disable done button
    document.getElementById('done-btn').disabled = true;
    
    showNotification('Started fresh session', 'info');
}

function closeBanner() {
    const banner = document.getElementById('session-restore-banner');
    if (banner) {
        banner.remove();
    }
}

// Initialize before unload warning
function initializeBeforeUnloadWarning() {
    window.addEventListener('beforeunload', function(e) {
        if (chatHistory.length > 0 && userPreferences.saveConversations) {
            e.preventDefault();
            e.returnValue = 'You have an active chat session. Are you sure you want to leave?';
            return 'You have an active chat session. Are you sure you want to leave?';
        }
    });
}

// Sidebar Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.container');
    const toggleBtn = document.getElementById('sidebar-toggle');
    const toggleIcon = toggleBtn.querySelector('.toggle-icon');

    // Initialize sidebar state
    function initializeSidebar() {
        if (localStorage.getItem('sidebarCollapsed') === 'true') {
            container.classList.add('sidebar-collapsed');
        }
    }

    // Toggle sidebar
    function toggleSidebar() {
        container.classList.toggle('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', 
            container.classList.contains('sidebar-collapsed'));
    }

    // Add click event listener to toggle button
    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleSidebar);
    }

    // Initialize sidebar on page load
    initializeSidebar();

    // Handle window resize
    let windowWidth = window.innerWidth;
    window.addEventListener('resize', function() {
        const newWidth = window.innerWidth;
        
        // Auto-collapse sidebar on small screens
        if (newWidth < 768 && windowWidth >= 768) {
            container.classList.add('sidebar-collapsed');
        }
        // Auto-expand sidebar on large screens
        else if (newWidth >= 768 && windowWidth < 768) {
            container.classList.remove('sidebar-collapsed');
        }
        
        windowWidth = newWidth;
    });

    // Double-click header to toggle sidebar
    const sidebarHeader = document.querySelector('.sidebar-header');
    if (sidebarHeader) {
        sidebarHeader.addEventListener('dblclick', toggleSidebar);
    }
});

// Export functions if needed
window.toggleSidebar = function() {
    const container = document.querySelector('.container');
    container.classList.toggle('sidebar-collapsed');
    localStorage.setItem('sidebarCollapsed', 
        container.classList.contains('sidebar-collapsed'));
};
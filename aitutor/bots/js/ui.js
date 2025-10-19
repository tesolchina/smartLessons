// ui.js - UI Enhancement Module

// Global variables for UI state
let sidebarCollapsed = false;

// Check for previous session and offer restoration
function checkForPreviousSession() {
    // Only check if core functions are available
    if (typeof loadFromCache !== 'function' || typeof STORAGE_KEYS === 'undefined') {
        console.log('⚠️ Core cache functions not available, skipping session restore');
        return;
    }

    const sessionData = loadFromCache(STORAGE_KEYS.CHAT_HISTORY);
    if (sessionData && sessionData.messages && sessionData.messages.length > 0) {
        const timeDiff = new Date() - new Date(sessionData.lastActivity);
        const hoursSinceLastActivity = timeDiff / (1000 * 60 * 60);
        
        if (hoursSinceLastActivity < 2 && userPreferences.autoRestore) {
            // Auto-restore recent sessions
            restoreSession(sessionData);
            if (typeof showNotification === 'function') {
                showNotification(`Previous session restored (${sessionData.messageCount} messages)`, 'success');
            }
        } else if (hoursSinceLastActivity < 24) {
            // Prompt user for older sessions
            showSessionRestorePrompt(sessionData);
        } else {
            // Clear very old sessions
            if (typeof clearCache === 'function') {
                clearCache(STORAGE_KEYS.CHAT_HISTORY);
            }
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
                <button onclick="restoreSessionFromUI()" 
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
    
    // Store session data for restoration
    window.pendingSessionData = sessionData;
}

function restoreSessionFromUI() {
    if (window.pendingSessionData) {
        restoreSession(window.pendingSessionData);
        closeBanner();
        window.pendingSessionData = null;
    }
}

function restoreSession(sessionData) {
    try {
        // Check if core functions are available
        if (typeof chatHistory === 'undefined' || typeof addMessage !== 'function') {
            console.error('Core chat functions not available');
            return;
        }

        // Restore chat history
        chatHistory.length = 0; // Clear existing history
        sessionData.messages.forEach(msg => {
            chatHistory.push({
                ...msg,
                timestamp: new Date(msg.timestamp)
            });
        });
        
        // Restore custom prompts if they exist
        if (sessionData.customPrompts) {
            if (sessionData.customPrompts.welcome && typeof welcomePrompt !== 'undefined') {
                welcomePrompt = sessionData.customPrompts.welcome;
                if (typeof updateWelcomePromptDisplay === 'function') {
                    updateWelcomePromptDisplay();
                }
            }
            if (sessionData.customPrompts.system && typeof systemPrompt !== 'undefined') {
                systemPrompt = sessionData.customPrompts.system;
                if (typeof updateSystemPromptDisplay === 'function') {
                    updateSystemPromptDisplay();
                }
            }
        }
        
        // Restore chat display
        const messagesContainer = document.getElementById('chat-messages');
        if (messagesContainer) {
            messagesContainer.innerHTML = '';
            
            chatHistory.forEach(msg => {
                addMessage(msg.role, msg.content);
            });
        }
        
        // Enable done button if there are messages
        const doneBtn = document.getElementById('done-btn');
        if (doneBtn && chatHistory.length > 0) {
            doneBtn.disabled = false;
        }
        
        console.log('✅ Session restored successfully');
        
    } catch (error) {
        console.error('Failed to restore session:', error);
        if (typeof showNotification === 'function') {
            showNotification('Failed to restore previous session', 'error');
        }
        startFreshSession();
    }
}

function startFreshSession() {
    try {
        // Clear current session
        if (typeof chatHistory !== 'undefined') {
            chatHistory.length = 0;
        }
        
        if (typeof clearCache === 'function' && typeof STORAGE_KEYS !== 'undefined') {
            clearCache(STORAGE_KEYS.CHAT_HISTORY);
        }
        
        // Reset chat display
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
        
        // Disable done button
        const doneBtn = document.getElementById('done-btn');
        if (doneBtn) {
            doneBtn.disabled = true;
        }
        
        if (typeof showNotification === 'function') {
            showNotification('Started fresh session', 'info');
        }
        
    } catch (error) {
        console.error('Error starting fresh session:', error);
    }
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
        if (typeof chatHistory !== 'undefined' && chatHistory.length > 0 && 
            typeof userPreferences !== 'undefined' && userPreferences.saveConversations) {
            e.preventDefault();
            e.returnValue = 'You have an active chat session. Are you sure you want to leave?';
            return 'You have an active chat session. Are you sure you want to leave?';
        }
    });
}

// Sidebar Toggle Functionality
function initializeSidebarToggle() {
    const container = document.querySelector('.container');
    const toggleBtn = document.getElementById('sidebar-toggle');
    
    if (!container) {
        console.log('⚠️ Container element not found, skipping sidebar toggle');
        return;
    }

    // Initialize sidebar state
    function initializeSidebar() {
        const collapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (collapsed) {
            container.classList.add('sidebar-collapsed');
            sidebarCollapsed = true;
        }
    }

    // Toggle sidebar
    function toggleSidebar() {
        container.classList.toggle('sidebar-collapsed');
        sidebarCollapsed = container.classList.contains('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', sidebarCollapsed.toString());
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
            sidebarCollapsed = true;
            localStorage.setItem('sidebarCollapsed', 'true');
        }
        // Auto-expand sidebar on large screens
        else if (newWidth >= 768 && windowWidth < 768) {
            container.classList.remove('sidebar-collapsed');
            sidebarCollapsed = false;
            localStorage.setItem('sidebarCollapsed', 'false');
        }
        
        windowWidth = newWidth;
    });

    // Double-click header to toggle sidebar
    const sidebarHeader = document.querySelector('.sidebar-header');
    if (sidebarHeader) {
        sidebarHeader.addEventListener('dblclick', toggleSidebar);
    }
    
    // Export toggle function
    window.toggleSidebar = toggleSidebar;
}

// UI Enhancement functions
function addUIEnhancements() {
    // Add smooth transitions to interactive elements
    const style = document.createElement('style');
    style.textContent = `
        .btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            transition: all 0.2s ease;
        }
        
        .prompt-header:hover,
        .api-header:hover {
            background-color: rgba(0,0,0,0.05);
            transition: background-color 0.2s ease;
        }
        
        .notification {
            animation: slideInFromRight 0.3s ease-out;
        }
        
        @keyframes slideInFromRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
}

// Initialize all UI components
function initializeUI() {
    console.log('🎨 Initializing UI enhancements...');
    
    try {
        initializeSidebarToggle();
        initializeBeforeUnloadWarning();
        addUIEnhancements();
        
        // Check for previous session after a delay
        setTimeout(checkForPreviousSession, 500);
        
        console.log('✅ UI enhancements initialized');
    } catch (error) {
        console.error('Error initializing UI:', error);
    }
}

// Export functions to global scope
window.checkForPreviousSession = checkForPreviousSession;
window.restoreSession = restoreSession;
window.restoreSessionFromUI = restoreSessionFromUI;
window.startFreshSession = startFreshSession;
window.closeBanner = closeBanner;
window.initializeUI = initializeUI;

// Initialize UI when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎨 ui.js initializing...');
    
    // Delay initialization to ensure other scripts load first
    setTimeout(initializeUI, 200);
    
    console.log('✅ ui.js loaded');
});

console.log('✅ ui.js loaded');
// Main Application Controller
class App {
    constructor() {
        this.initialized = false;
        this.currentContent = null;
        this.startTime = Date.now();
    }

    async init() {
        if (this.initialized) return;
        
        try {
            console.log('🚀 Initializing Course Container App...');
            
            // Initialize core managers
            await this.initializeManagers();
            
            // Setup global event listeners
            this.setupEventListeners();
            
            // Initialize course data
            this.initializeCourseData();
            
            // Initialize theme
            this.initializeTheme();
            
            this.initialized = true;
            console.log('✅ App initialization complete');
            
            // Show welcome notification
            if (window.notificationManager) {
                window.notificationManager.show('Course container loaded successfully!', 'success');
            }
            
        } catch (error) {
            console.error('❌ App initialization failed:', error);
            if (window.notificationManager) {
                window.notificationManager.show('Failed to initialize course container', 'error');
            }
        }
    }

    async initializeManagers() {
        console.log('📦 Initializing managers...');
        
        // Check if classes are available
        const requiredClasses = [
            'StateManager', 'TimerManager', 'ProgressManager', 
            'NotificationManager', 'ReportGenerator', 'ContentLoader'
        ];
        
        const missingClasses = requiredClasses.filter(className => typeof window[className] === 'undefined');
        
        if (missingClasses.length > 0) {
            console.error('❌ Missing required classes:', missingClasses);
            throw new Error(`Missing required classes: ${missingClasses.join(', ')}`);
        }
        
        // Initialize managers in dependency order
        try {
            window.notificationManager = new NotificationManager();
            window.stateManager = new StateManager();
            window.timerManager = new TimerManager();
            window.progressManager = new ProgressManager();
            window.reportGenerator = new ReportGenerator();
            window.contentLoader = new ContentLoader();
            
            console.log('✅ All managers initialized successfully');
        } catch (error) {
            console.error('❌ Failed to initialize managers:', error);
            throw error;
        }
    }

    setupEventListeners() {
        console.log('🔗 Setting up event listeners...');
        // Your existing HTML uses inline onclick handlers, so we don't need to set up additional listeners
        console.log('✅ Event listeners setup complete (using inline handlers)');
    }

    initializeCourseData() {
        // Set current date
        const lastUpdatedElement = document.getElementById('lastUpdated');
        if (lastUpdatedElement) {
            lastUpdatedElement.textContent = new Date().toLocaleDateString();
        }
        
        // Initialize section progress indicators
        this.updateSectionIndicators();
    }

    initializeTheme() {
        // Check for saved theme preference or default to 'light'
        const theme = localStorage.getItem('theme') || 'light';
        this.setTheme(theme);
    }

    setTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
        localStorage.setItem('theme', theme);
    }

    toggleDarkMode() {
        const isDark = document.documentElement.classList.contains('dark');
        this.setTheme(isDark ? 'light' : 'dark');
        if (window.notificationManager) {
            window.notificationManager.show(`Switched to ${isDark ? 'light' : 'dark'} mode`, 'info');
        }
    }

    updateSectionIndicators() {
        const sections = ['lecture', 'practice', 'reflect'];
        sections.forEach(section => {
            const progress = window.stateManager ? window.stateManager.getSectionProgress(section) : 0;
            this.updateSectionProgress(section, progress);
        });
    }

    updateSectionProgress(section, progress) {
        const sectionButton = document.querySelector(`[data-section="${section}"]`);
        if (sectionButton) {
            const progressBar = sectionButton.querySelector('.section-progress');
            const statusSpan = sectionButton.querySelector('.completion-status');
            
            if (progressBar) {
                progressBar.style.width = progress + '%';
            }
            
            if (statusSpan) {
                if (progress >= 100) {
                    statusSpan.textContent = '✅ Completed';
                    statusSpan.className = 'completion-status text-green-600 dark:text-green-400';
                } else if (progress > 0) {
                    statusSpan.textContent = `⏳ In Progress (${progress}%)`;
                    statusSpan.className = 'completion-status text-yellow-600 dark:text-yellow-400';
                } else {
                    statusSpan.textContent = '⭕ Not Started';
                    statusSpan.className = 'completion-status text-gray-500 dark:text-gray-400';
                }
            }
        }
        
        this.updateOverallProgress();
    }

    updateOverallProgress() {
        const sections = document.querySelectorAll('.section-progress');
        let totalProgress = 0;
        
        sections.forEach(bar => {
            const width = parseFloat(bar.style.width) || 0;
            totalProgress += width;
        });
        
        const overallProgress = sections.length > 0 ? totalProgress / sections.length : 0;
        const overallBar = document.getElementById('overallProgressBar');
        const overallText = document.getElementById('overallProgressText');
        
        if (overallBar) {
            overallBar.style.width = overallProgress + '%';
        }
        
        if (overallText) {
            overallText.textContent = Math.round(overallProgress) + '%';
        }
    }

    async loadContent(url) {
        if (window.contentLoader) {
            await window.contentLoader.loadContent(url);
        }
    }

    saveProgress() {
        try {
            if (window.stateManager) {
                window.stateManager.saveState();
                if (window.notificationManager) {
                    window.notificationManager.show('Progress saved successfully!', 'success');
                }
            }
        } catch (error) {
            console.error('Save failed:', error);
            if (window.notificationManager) {
                window.notificationManager.show('Failed to save progress', 'error');
            }
        }
    }

    generateReport() {
        try {
            if (window.stateManager && window.reportGenerator) {
                const reportData = window.stateManager.getFullState();
                window.reportGenerator.generateDetailedReport(reportData);
            }
        } catch (error) {
            console.error('Report generation failed:', error);
            if (window.notificationManager) {
                window.notificationManager.show('Failed to generate report', 'error');
            }
        }
    }

    goBack() {
        if (window.history.length > 1) {
            window.history.back();
        } else {
            if (window.notificationManager) {
                window.notificationManager.show('No previous page to return to', 'info');
            }
        }
    }
}

// Global functions for content integration
window.generateReportFromContent = function(lectureData) {
    console.log('📊 Report received from interactive content:', lectureData);
    
    if (window.reportGenerator) {
        window.reportGenerator.showInteractiveReport(lectureData);
    } else {
        console.warn('ReportGenerator not available');
    }
};

window.updateSectionProgress = function(section, progress) {
    console.log(`📈 Section ${section} progress updated to ${progress}%`);
    
    if (window.stateManager) {
        window.stateManager.updateSection(section, { progress: progress });
    }
    
    if (window.app) {
        window.app.updateSectionProgress(section, progress);
    }
};

// Global content loading function
window.loadContent = function(url) {
    if (window.app) {
        window.app.loadContent(url);
    }
};

// Legacy function support - these match your existing onclick handlers
window.toggleDarkMode = function() {
    if (window.app) {
        window.app.toggleDarkMode();
    }
};

window.goBack = function() {
    if (window.app) {
        window.app.goBack();
    }
};

window.saveProgress = function() {
    if (window.app) {
        window.app.saveProgress();
    }
};

// This function will be called by your existing "Generate Report" button
window.generateReport = function(lectureData = null) {
    if (lectureData) {
        // Called from interactive content
        window.generateReportFromContent(lectureData);
    } else {
        // Called from main UI
        if (window.app) {
            window.app.generateReport();
        }
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
    window.app.init();
});

// Handle messages from iframe content
window.addEventListener('message', (event) => {
    if (event.data.type === 'generateReport') {
        window.generateReport(event.data.data);
    }
});
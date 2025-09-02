// Course Container Application - Combined JavaScript
// All classes in one file to avoid loading conflicts

// Notification Manager
class NotificationManager {
    constructor() {
        this.container = this.createContainer();
        this.notifications = [];
    }

    createContainer() {
        let container = document.getElementById('notificationContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'notificationContainer';
            container.className = 'fixed top-4 right-4 z-50 space-y-2';
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'info', duration = 5000) {
        const notification = this.createNotification(message, type);
        this.container.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto remove
        setTimeout(() => this.remove(notification), duration);
        
        return notification;
    }

    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification bg-white dark:bg-gray-800 border-l-4 p-4 rounded-lg shadow-lg transform translate-x-full transition-all duration-300 ${this.getTypeClasses(type)}`;
        
        notification.innerHTML = `
            <div class="flex items-center">
                <div class="mr-3">
                    ${this.getIcon(type)}
                </div>
                <div class="flex-1">
                    <p class="text-sm font-medium text-gray-900 dark:text-white">${message}</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"/>
                    </svg>
                </button>
            </div>
        `;
        
        return notification;
    }

    getTypeClasses(type) {
        const classes = {
            success: 'border-green-500',
            error: 'border-red-500',
            warning: 'border-yellow-500',
            info: 'border-blue-500'
        };
        return classes[type] || classes.info;
    }

    getIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        return icons[type] || icons.info;
    }

    remove(notification) {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }
}

// Timer Manager
class TimerManager {
    constructor() {
        this.timers = new Map();
        this.startTime = Date.now();
    }

    startTimer(sectionId) {
        if (!this.timers.has(sectionId)) {
            this.timers.set(sectionId, {
                startTime: Date.now(),
                totalTime: 0,
                isRunning: true
            });
        } else {
            const timer = this.timers.get(sectionId);
            if (!timer.isRunning) {
                timer.startTime = Date.now();
                timer.isRunning = true;
            }
        }
        console.log(`⏱️ Timer started for section: ${sectionId}`);
    }

    stopTimer(sectionId) {
        const timer = this.timers.get(sectionId);
        if (timer && timer.isRunning) {
            timer.totalTime += Date.now() - timer.startTime;
            timer.isRunning = false;
            console.log(`⏹️ Timer stopped for section: ${sectionId}`);
        }
    }

    getTimeSpent(sectionId) {
        const timer = this.timers.get(sectionId);
        if (!timer) return 0;
        
        let totalTime = timer.totalTime;
        if (timer.isRunning) {
            totalTime += Date.now() - timer.startTime;
        }
        return totalTime;
    }

    getTotalTimeSpent() {
        return Date.now() - this.startTime;
    }
}

// Progress Manager
class ProgressManager {
    constructor() {
        this.progressData = new Map();
    }

    markSectionProgress(sectionId, progress) {
        this.progressData.set(sectionId, Math.max(0, Math.min(100, progress)));
        
        // Update state manager
        if (window.stateManager) {
            window.stateManager.updateSection(sectionId, {
                progress: progress,
                completed: progress >= 100,
                timeSpent: window.timerManager ? window.timerManager.getTimeSpent(sectionId) : 0
            });
        }
        
        // Update UI
        if (window.app) {
            window.app.updateSectionProgress(sectionId, progress);
        }
        
        console.log(`📈 Progress updated for ${sectionId}: ${progress}%`);
    }

    getSectionProgress(sectionId) {
        return this.progressData.get(sectionId) || 0;
    }

    getOverallProgress() {
        if (this.progressData.size === 0) return 0;
        
        const total = Array.from(this.progressData.values()).reduce((sum, progress) => sum + progress, 0);
        return total / this.progressData.size;
    }
}

// State Management System
class StateManager {
    constructor() {
        this.state = {
            user: {
                id: null,
                name: 'Student',
                startTime: Date.now(),
                lastActivity: Date.now()
            },
            course: {
                id: 'course-001',
                name: 'Interactive Learning Course',
                sections: {
                    lecture: {
                        progress: 0,
                        timeSpent: 0,
                        completed: false,
                        lastAccessed: null,
                        data: {}
                    },
                    practice: {
                        progress: 0,
                        timeSpent: 0,
                        completed: false,
                        lastAccessed: null,
                        data: {}
                    },
                    reflect: {
                        progress: 0,
                        timeSpent: 0,
                        completed: false,
                        lastAccessed: null,
                        data: {}
                    }
                }
            },
            settings: {
                theme: 'light',
                autoSave: true,
                notifications: true
            },
            interactions: [],
            reports: []
        };
        
        this.loadState();
        this.setupAutoSave();
    }

    loadState() {
        try {
            const savedState = localStorage.getItem('courseState');
            if (savedState) {
                const parsed = JSON.parse(savedState);
                this.state = { ...this.state, ...parsed };
                console.log('✅ State loaded from localStorage');
            }
        } catch (error) {
            console.warn('⚠️ Failed to load state:', error);
        }
    }

    saveState() {
        try {
            this.state.user.lastActivity = Date.now();
            localStorage.setItem('courseState', JSON.stringify(this.state));
            console.log('✅ State saved to localStorage');
            return true;
        } catch (error) {
            console.error('❌ Failed to save state:', error);
            return false;
        }
    }

    setupAutoSave() {
        if (this.state.settings.autoSave) {
            setInterval(() => {
                this.saveState();
            }, 30000); // Auto-save every 30 seconds
        }
    }

    updateSection(sectionId, updates) {
        if (this.state.course.sections[sectionId]) {
            this.state.course.sections[sectionId] = {
                ...this.state.course.sections[sectionId],
                ...updates,
                lastAccessed: Date.now()
            };
            
            if (this.state.settings.autoSave) {
                this.saveState();
            }
            
            console.log(`📊 Section ${sectionId} updated:`, updates);
            return true;
        }
        return false;
    }

    getSectionProgress(sectionId) {
        return this.state.course.sections[sectionId]?.progress || 0;
    }

    getSectionData(sectionId) {
        return this.state.course.sections[sectionId] || null;
    }

    addInteraction(interaction) {
        this.state.interactions.push({
            ...interaction,
            timestamp: Date.now(),
            id: `interaction-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
        });
    }

    getOverallProgress() {
        const sections = Object.values(this.state.course.sections);
        const totalProgress = sections.reduce((sum, section) => sum + section.progress, 0);
        return sections.length > 0 ? totalProgress / sections.length : 0;
    }

    getTimeSpent() {
        return Date.now() - this.state.user.startTime;
    }

    getFullState() {
        return {
            ...this.state,
            computed: {
                overallProgress: this.getOverallProgress(),
                totalTimeSpent: this.getTimeSpent(),
                sectionsCompleted: Object.values(this.state.course.sections).filter(s => s.completed).length,
                lastActivity: new Date(this.state.user.lastActivity).toLocaleString()
            }
        };
    }

    resetState() {
        localStorage.removeItem('courseState');
        location.reload();
    }

    exportState() {
        return JSON.stringify(this.state, null, 2);
    }

    importState(stateJson) {
        try {
            const newState = JSON.parse(stateJson);
            this.state = newState;
            this.saveState();
            return true;
        } catch (error) {
            console.error('Failed to import state:', error);
            return false;
        }
    }
}

// Enhanced Content Loader Module
class ContentLoader {
    constructor() {
        this.cache = new Map();
        this.loadingQueue = new Set();
    }

    async loadContent(url) {
        if (this.loadingQueue.has(url)) {
            return; // Already loading
        }

        this.loadingQueue.add(url);
        this.toggleLoading(true);
        
        const section = this.getSectionFromUrl(url);
        
        try {
            let content;
            
            // Check cache first
            if (this.cache.has(url)) {
                content = this.cache.get(url);
                console.log(`📄 Loaded ${section} from cache`);
            } else {
                // Try to fetch the actual file
                console.log(`🌐 Fetching ${url}...`);
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                content = await response.text();
                this.cache.set(url, content);
                console.log(`✅ Fetched and cached ${section} content`);
            }
            
            // Clear the content area
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = '';
            
            // Create a temporary container to parse the HTML
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = content;
            
            // Extract and move body content (skip head)
            const bodyContent = tempDiv.querySelector('body');
            if (bodyContent) {
                // Move all body content to content area
                while (bodyContent.firstChild) {
                    contentArea.appendChild(bodyContent.firstChild);
                }
            } else {
                // If no body tag, just use all content
                while (tempDiv.firstChild) {
                    contentArea.appendChild(tempDiv.firstChild);
                }
            }
            
        // Execute any inline scripts
        this.executeScripts(contentArea);

        // Override any report functions in the loaded content
        setTimeout(() => {
            overrideContentReportFunctions();
            console.log('🔧 Report functions overridden after content load');
        }, 1000);

        // Set up data collection for interactive content
        setTimeout(() => {
            setupInteractiveDataCollection(section);
            console.log('📊 Data collection setup for:', section);
        }, 1500);
            // Update state
            if (window.stateManager) {
                window.stateManager.updateSection(section, {
                    lastAccessed: new Date().toISOString()
                });
            }
            
            // Start timer
            if (window.timerManager) {
                window.timerManager.startTimer(section);
            }
            
            // Show success notification
            if (window.notificationManager) {
                window.notificationManager.show(`Loaded ${section} content successfully!`, 'success');
            }
            
            console.log(`🎉 Successfully loaded ${section} content`);
            
        } catch (error) {
            console.error('❌ Error loading content:', error);
            
            // Provide fallback content
            const fallbackContent = this.createFallbackContent(section);
            document.getElementById('contentArea').innerHTML = fallbackContent;
            
            if (window.notificationManager) {
                window.notificationManager.show(`Loaded demo content for ${section}`, 'warning');
            }
        } finally {
            this.loadingQueue.delete(url);
            this.toggleLoading(false);
        }
    }

    executeScripts(container) {
        // Find all script tags in the loaded content
        const scripts = container.querySelectorAll('script');
        
        scripts.forEach(oldScript => {
            // Create a new script element
            const newScript = document.createElement('script');
            
            // Copy attributes
            Array.from(oldScript.attributes).forEach(attr => {
                newScript.setAttribute(attr.name, attr.value);
            });
            
            // Copy script content
            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
            
            // Replace old script with new one to trigger execution
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
        
        console.log(`⚡ Executed ${scripts.length} scripts for loaded content`);
    }

    getSectionFromUrl(url) {
        const filename = url.split('/').pop().split('.')[0];
        if (filename.toLowerCase().includes('lecture')) return 'lecture';
        if (filename.toLowerCase().includes('practice')) return 'practice';
        if (filename.toLowerCase().includes('reflect')) return 'reflect';
        return 'lecture';
    }

    createFallbackContent(section) {
        const contents = {
            lecture: `
                <div class="space-y-6">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-white">📚 Interactive Lecture</h2>
                    <div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-700">
                        <h3 class="text-lg font-semibold mb-4 text-blue-900 dark:text-blue-100">Demo Content</h3>
                        <p class="mb-4 text-blue-800 dark:text-blue-200">This is placeholder content for the interactive lecture section. In your actual implementation, this would contain:</p>
                        <ul class="list-disc list-inside space-y-2 text-blue-700 dark:text-blue-300">
                            <li>Video lectures with interactive elements</li>
                            <li>Embedded quizzes and knowledge checks</li>
                            <li>Downloadable resources and materials</li>
                            <li>Progress tracking and bookmarking</li>
                        </ul>
                        <button onclick="window.updateSectionProgress('lecture', 100)" 
                                class="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                            Complete Section
                        </button>
                    </div>
                </div>
            `,
            practice: `
                <div class="space-y-6">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-white">💬 Practice & Discussion</h2>
                    <div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg border border-green-200 dark:border-green-700">
                        <h3 class="text-lg font-semibold mb-4 text-green-900 dark:text-green-100">Demo Content</h3>
                        <p class="mb-4 text-green-800 dark:text-green-200">This is placeholder content for the practice and discussion section. Features would include:</p>
                        <ul class="list-disc list-inside space-y-2 text-green-700 dark:text-green-300">
                            <li>Interactive exercises and simulations</li>
                            <li>Discussion forums and peer collaboration</li>
                            <li>Case studies and real-world applications</li>
                            <li>Peer review and feedback systems</li>
                        </ul>
                        <button onclick="window.updateSectionProgress('practice', 100)" 
                                class="mt-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors">
                            Complete Section
                        </button>
                    </div>
                </div>
            `,
            reflect: `
                <div class="space-y-6">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-white">🎯 Reflect & Assess</h2>
                    <div class="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-lg border border-purple-200 dark:border-purple-700">
                        <h3 class="text-lg font-semibold mb-4 text-purple-900 dark:text-purple-100">Demo Content</h3>
                        <p class="mb-4 text-purple-800 dark:text-purple-200">This is placeholder content for the reflection and assessment section. Components include:</p>
                        <ul class="list-disc list-inside space-y-2 text-purple-700 dark:text-purple-300">
                            <li>Self-reflection exercises and journaling</li>
                            <li>Formative and summative assessments</li>
                            <li>Portfolio creation and showcasing</li>
                            <li>Goal setting and progress evaluation</li>
                        </ul>
                        <button onclick="window.updateSectionProgress('reflect', 100)" 
                                class="mt-4 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
                            Complete Section
                        </button>
                    </div>
                </div>
            `
        };
        
        return contents[section] || contents.lecture;
    }

    toggleLoading(show) {
        const loader = document.getElementById('loadingIndicator');
        if (loader) {
            loader.style.transform = show ? 'scaleX(1)' : 'scaleX(0)';
        }
    }

    clearCache() {
        this.cache.clear();
        console.log('🗑️ Content cache cleared');
    }

    preloadContent(urls) {
        console.log('🚀 Preloading content...');
        urls.forEach(async (url) => {
            try {
                const response = await fetch(url);
                if (response.ok) {
                    const content = await response.text();
                    this.cache.set(url, content);
                    console.log(`✅ Preloaded: ${url}`);
                }
            } catch (error) {
                console.warn(`⚠️ Failed to preload ${url}:`, error);
            }
        });
    }
}

// Report Generator
class ReportGenerator {
    constructor() {
        this.reports = [];
    }

    generateDetailedReport(data) {
        console.log('📊 Generating detailed report...');
        
        const report = this.createReportData(data);
        this.showReportModal(report, 'detailed');
    }

    showInteractiveReport(lectureData) {
        console.log('📋 Showing interactive content report...');
        
        const report = this.createInteractiveReportData(lectureData);
        this.showReportModal(report, 'interactive');
    }

    createReportData(stateData) {
        const sections = stateData.course?.sections || {};
        const overallProgress = stateData.computed?.overallProgress || 0;
        const totalTime = stateData.computed?.totalTimeSpent || 0;
        
        return {
            metadata: {
                generated: new Date().toISOString(),
                reportType: 'Course Progress Report'
            },
            summary: {
                overallProgress: Math.round(overallProgress),
                totalTimeSpent: this.formatDuration(totalTime),
                sectionsCompleted: Object.values(sections).filter(s => s.completed).length,
                totalSections: Object.keys(sections).length
            },
            sections: Object.entries(sections).map(([id, data]) => ({
                id,
                name: this.getSectionName(id),
                progress: data.progress || 0,
                timeSpent: this.formatDuration(data.timeSpent || 0),
                completed: data.completed || false
            })),
            interactions: stateData.interactions || []
        };
    }

    createInteractiveReportData(lectureData) {
        const duration = lectureData.timeSpent || (Date.now() - lectureData.startTime);
        
        return {
            metadata: {
                generated: new Date().toISOString(),
                contentType: 'Interactive Lecture'
            },
            performance: {
                score: lectureData.score,
                choiceSelected: lectureData.choiceSelected,
                timeSpent: this.formatDuration(duration),
                completed: lectureData.completed || false
            },
            sectionProgress: lectureData.sectionProgress || {},
            interactions: lectureData.interactions || []
        };
    }

    showReportModal(reportData, template = 'detailed') {
        let modal = document.getElementById('reportModal');
        if (!modal) {
            modal = this.createReportModal();
        }

        const content = document.getElementById('reportModalContent');
        content.innerHTML = this.generateReportHTML(reportData, template);
        
        modal.style.display = 'flex';
        
        this.setupModalEventListeners(modal, reportData);
    }

    createReportModal() {
    const modal = document.createElement('div');
    modal.id = 'reportModal';
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4';
    modal.style.display = 'none';
    
    modal.innerHTML = `
        <div class="bg-white dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
            <div class="flex justify-between items-center p-6 border-b dark:border-gray-600 bg-gray-50 dark:bg-gray-700">
                <h3 class="text-xl font-bold text-gray-900 dark:text-white flex items-center">
                    <span class="mr-2">📊</span>
                    Learning Report
                </h3>
                <button id="closeReportModal" 
                        class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 p-2 rounded-lg transition-colors"
                        title="Close Report">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
            <div id="reportModalContent" class="flex-1 overflow-auto p-6">
                <!-- Report content will be inserted here -->
            </div>
            <div class="border-t dark:border-gray-600 p-4 bg-gray-50 dark:bg-gray-700">
                <div class="flex justify-between items-center">
                    <button id="closeReportModalBottom" 
                            class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition-colors">
                        Close
                    </button>
                    <button id="downloadReportBtn" 
                            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-4-4m4 4l4-4m-6 8h8a2 2 0 002-2V7a2 2 0 00-2-2H9a2 2 0 00-2 2v11a2 2 0 002 2z"></path>
                        </svg>
                        Download Report
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add bottom close button handler
    const bottomCloseBtn = modal.querySelector('#closeReportModalBottom');
    if (bottomCloseBtn) {
        bottomCloseBtn.onclick = (e) => {
            e.preventDefault();
            modal.style.display = 'none';
        };
    }
    
    return modal;
}

    generateReportHTML(data, template) {
        if (template === 'interactive') {
            return `
                <div class="space-y-4">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded text-center">
                            <div class="text-2xl font-bold text-blue-600">${data.performance.score || 'N/A'}%</div>
                            <div class="text-sm text-blue-800 dark:text-blue-300">Score</div>
                        </div>
                        <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded text-center">
                            <div class="text-2xl font-bold text-green-600">${data.performance.timeSpent}</div>
                            <div class="text-sm text-green-800 dark:text-green-300">Time</div>
                        </div>
                        <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded text-center">
                            <div class="text-2xl font-bold text-purple-600">${data.performance.completed ? '✅' : '⏳'}</div>
                            <div class="text-sm text-purple-800 dark:text-purple-300">Status</div>
                        </div>
                        <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded text-center">
                            <div class="text-2xl font-bold text-orange-600">${data.interactions.length}</div>
                            <div class="text-sm text-orange-800 dark:text-orange-300">Interactions</div>
                        </div>
                    </div>
                    <div class="mt-4">
                        <h4 class="font-semibold mb-2">Choice Selected: ${data.performance.choiceSelected || 'None'}</h4>
                        <h4 class="font-semibold mb-2">Section Progress:</h4>
                        ${Object.entries(data.sectionProgress).map(([section, progress]) => `
                            <div class="flex justify-between items-center mb-2">
                                <span>${this.getSectionName(section)}</span>
                                <span>${progress}%</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        } else {
            return `
                <div class="space-y-4">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded text-center">
                            <div class="text-2xl font-bold text-blue-600">${data.summary.overallProgress}%</div>
                            <div class="text-sm text-blue-800 dark:text-blue-300">Progress</div>
                        </div>
                        <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded text-center">
                            <div class="text-2xl font-bold text-green-600">${data.summary.totalTimeSpent}</div>
                            <div class="text-sm text-green-800 dark:text-green-300">Time</div>
                        </div>
                        <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded text-center">
                            <div class="text-2xl font-bold text-purple-600">${data.summary.sectionsCompleted}</div>
                            <div class="text-sm text-purple-800 dark:text-purple-300">Completed</div>
                        </div>
                        <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded text-center">
                            <div class="text-2xl font-bold text-orange-600">${data.interactions.length}</div>
                            <div class="text-sm text-orange-800 dark:text-orange-300">Interactions</div>
                        </div>
                    </div>
                    <div class="mt-4">
                        <h4 class="font-semibold mb-2">Section Details:</h4>
                        ${data.sections.map(section => `
                            <div class="flex justify-between items-center mb-2 p-2 bg-gray-50 dark:bg-gray-700 rounded">
                                <span>${section.name}</span>
                                <span>${section.progress}% (${section.timeSpent})</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
    }

 setupModalEventListeners(modal, reportData) {
    // Multiple ways to close the modal
    const closeButtons = modal.querySelectorAll('#closeReportModal, #closeReportModalBottom');
    closeButtons.forEach(btn => {
        if (btn) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                modal.style.display = 'none';
                console.log('✅ Report modal closed');
            });
        }
    });

    // Download functionality
    const downloadBtn = modal.querySelector('#downloadReportBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `report-${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            URL.revokeObjectURL(url);
        });
    }

    // Click outside to close
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Escape key to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            modal.style.display = 'none';
        }
    });
}

    formatDuration(milliseconds) {
        const minutes = Math.floor(milliseconds / 60000);
        const seconds = Math.floor((milliseconds % 60000) / 1000);
        return minutes > 0 ? `${minutes}m ${seconds}s` : `${seconds}s`;
    }

    getSectionName(sectionId) {
        const names = {
            '1': 'Opening Assessment',
            '2': 'Content Review', 
            '3': 'Completion',
            'lecture': 'Interactive Lecture',
            'practice': 'Practice & Discussion',
            'reflect': 'Reflect & Assess'
        };
        return names[sectionId] || sectionId;
    }
}

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
            this.initializeManagers();
            
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

    initializeManagers() {
        console.log('📦 Initializing managers...');
        
        // Initialize managers directly since they're all in this file
        window.notificationManager = new NotificationManager();
        window.stateManager = new StateManager();
        window.timerManager = new TimerManager();
        window.progressManager = new ProgressManager();
        window.reportGenerator = new ReportGenerator();
        window.contentLoader = new ContentLoader();
        
        console.log('✅ All managers initialized successfully');
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

// Global functions
window.updateSectionProgress = function(section, progress) {
    console.log(`📈 Section ${section} progress updated to ${progress}%`);
    
    if (window.stateManager) {
        window.stateManager.updateSection(section, { progress: progress });
    }
    
    if (window.app) {
        window.app.updateSectionProgress(section, progress);
    }
};

window.loadContent = function(url) {
    if (window.app) {
        window.app.loadContent(url);
    }
};

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

window.generateReport = function(lectureData = null) {
    if (lectureData) {
        // Called from interactive content
        if (window.reportGenerator) {
            window.reportGenerator.showInteractiveReport(lectureData);
        }
    } else {
        // Called from main UI
        if (window.app) {
            window.app.generateReport();
        }
    }
};

window.resetContentArea = function() {
    const contentArea = document.getElementById('contentArea');
    
    // Check if we have the content area and the stored HTML
    if (contentArea && originalContentAreaHTML) {
        contentArea.innerHTML = originalContentAreaHTML;

        // Apply a fade-in animation for a smooth transition
        contentArea.classList.remove('fade-in');
        // This is a small trick to force the browser to re-apply the animation
        void contentArea.offsetWidth; 
        contentArea.classList.add('fade-in');
        
        console.log('🔄 View reset to initial state.');
        
        // Let the user know the view was reset
        if (window.notificationManager) {
            window.notificationManager.show('View has been reset', 'info');
        }
    } else {
        console.error('❌ Could not reset the view. Original content not found.');
    }
};

// A global variable to hold the initial welcome screen content.
let originalContentAreaHTML = '';

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Capture the initial state of the content area once the DOM is loaded.
    originalContentAreaHTML = document.getElementById('contentArea').innerHTML;
    window.app = new App();
    window.app.init();
});

// Handle messages from iframe content
window.addEventListener('message', (event) => {
    if (event.data.type === 'generateReport') {
        window.generateReport(event.data.data);
    }
});
// Global function to generate report (called by HTML button)
function generateReport() {
    console.log('🔍 Generate Report button clicked from HTML');
    
    if (window.app && window.app.generateReport) {
        window.app.generateReport();
    } else if (window.reportGenerator) {
        window.reportGenerator.generateReport();
    } else {
        // Create a simple report if no app exists
        console.log('📊 Creating simple report...');
        const modal = createSimpleReportModal();
        modal.style.display = 'flex';
    }
}

// Global function to save progress (called by HTML button)
function saveProgress() {
    console.log('💾 Save Progress button clicked from HTML');
    
    if (window.app && window.app.saveProgress) {
        window.app.saveProgress();
    } else {
        // Simple save functionality
        try {
            const progressData = {
                timestamp: new Date().toISOString(),
                message: 'Progress saved successfully!'
            };
            localStorage.setItem('courseProgress', JSON.stringify(progressData));
            
            // Show notification
            if (window.notificationManager) {
                window.notificationManager.show('Progress saved!', 'success');
            } else {
                alert('Progress saved successfully!');
            }
        } catch (error) {
            console.error('❌ Error saving progress:', error);
            alert('Error saving progress');
        }
    }
}
// Function to collect user data from interactions and localStorage
function collectUserData() {
    console.log('📊 Collecting user data...');
    
    // Get data from localStorage
    const savedData = localStorage.getItem('courseInteractionData');
    const interactionData = savedData ? JSON.parse(savedData) : {};
    
    // Get current form data
    const currentInputs = document.querySelectorAll('input, textarea, select, [contenteditable="true"]');
    const currentData = [];
    
    currentInputs.forEach((input, index) => {
        const value = input.value || input.textContent;
        if (value && value.trim()) {
            currentData.push({
                type: input.tagName.toLowerCase(),
                id: input.id || `element-${index}`,
                content: value,
                timestamp: new Date().toISOString()
            });
        }
    });
    
    // Calculate statistics
    const lectureData = interactionData.lecture || [];
    const practiceData = interactionData.practice || [];
    const discussionData = interactionData.discussion || [];
    
    const totalInteractions = lectureData.length + practiceData.length + discussionData.length + currentData.length;
    const lectureAnswers = lectureData.filter(item => item.type === 'multiple_choice').length;
    const practiceInputs = practiceData.length;
    const discussionInputs = discussionData.length;
    
    // Calculate simple progress based on interactions
    const lectureProgress = lectureAnswers > 0 ? Math.min(100, lectureAnswers * 25) : 0;
    const practiceProgress = practiceInputs > 0 ? Math.min(100, practiceInputs * 20) : 0;
    const discussionProgress = discussionInputs > 0 ? Math.min(100, discussionInputs * 20) : 0;
    const overallProgress = Math.round((lectureProgress + practiceProgress + discussionProgress) / 3);
    
    return {
        timestamp: new Date().toISOString(),
        sections: {
            lecture: lectureData,
            practice: practiceData,
            discussion: discussionData,
            current: currentData
        },
        summary: {
            totalInteractions: totalInteractions,
            lectureAnswers: lectureAnswers,
            practiceInputs: practiceInputs,
            discussionInputs: discussionInputs,
            overallProgress: overallProgress,
            lectureProgress: lectureProgress,
            practiceProgress: practiceProgress,
            discussionProgress: discussionProgress
        }
    };
}

// Function to populate dynamic report content
function populateReportContent(userData) {
    console.log('📋 Populating report with real data:', userData);
    
    // Update statistics in header
    const statsContainer = document.getElementById('reportStats');
    if (statsContainer) {
        statsContainer.innerHTML = `
            <div class="text-center">
                <div class="text-2xl font-bold text-blue-600">${userData.summary.overallProgress}%</div>
                <div class="text-sm text-gray-600">Progress</div>
            </div>
            <div class="text-center">
                <div class="text-2xl font-bold text-green-600">${Math.round((Date.now() - (JSON.parse(localStorage.getItem('courseStartTime') || Date.now()))) / 60000)}m</div>
                <div class="text-sm text-gray-600">Time Spent</div>
            </div>
            <div class="text-center">
                <div class="text-2xl font-bold text-purple-600">${[userData.summary.lectureProgress, userData.summary.practiceProgress, userData.summary.discussionProgress].filter(p => p > 0).length}/3</div>
                <div class="text-sm text-gray-600">Sections Done</div>
            </div>
            <div class="text-center">
                <div class="text-2xl font-bold text-orange-600">${userData.summary.totalInteractions}</div>
                <div class="text-sm text-gray-600">Interactions</div>
            </div>
        `;
    }
    
    // Update section details
    const updateSectionCard = (sectionName, progress, interactions, status) => {
        const sectionCard = document.querySelector(`[data-section="${sectionName}"]`);
        if (sectionCard) {
            const progressBar = sectionCard.querySelector('.bg-blue-500, .bg-green-500, .bg-purple-500');
            const statusText = sectionCard.querySelector('.font-bold');
            const progressText = sectionCard.querySelector('.text-blue-600, .text-green-600, .text-purple-600');
            
            if (progressBar) progressBar.style.width = progress + '%';
            if (progressText) progressText.textContent = progress + '%';
            if (statusText) statusText.textContent = status;
        }
    };
    
    // Update each section
    updateSectionCard('lecture', 
        userData.summary.lectureProgress, 
        userData.summary.lectureAnswers,
        userData.summary.lectureProgress >= 100 ? '✅ Completed' : 
        userData.summary.lectureProgress > 0 ? '⏳ In Progress' : '⭕ Ready to start'
    );
    
    updateSectionCard('practice', 
        userData.summary.practiceProgress, 
        userData.summary.practiceInputs,
        userData.summary.practiceProgress >= 100 ? '✅ Completed' : 
        userData.summary.practiceProgress > 0 ? '⏳ In Progress' : '⭕ Ready to start'
    );
    
    updateSectionCard('discussion', 
        userData.summary.discussionProgress, 
        userData.summary.discussionInputs,
        userData.summary.discussionProgress >= 100 ? '✅ Completed' : 
        userData.summary.discussionProgress > 0 ? '⏳ In Progress' : '⭕ Ready to start'
    );
    
    // Update markdown content
    updateMarkdownContent(userData);
}

// Function to update markdown content with real data
function updateMarkdownContent(userData) {
    const markdownContent = document.getElementById('markdownContent');
    if (markdownContent) {
        const lectureAnswers = userData.sections.lecture.filter(item => item.type === 'multiple_choice');
        const practiceTexts = userData.sections.practice;
        const discussionTexts = userData.sections.discussion;
        
        let interactionsSection = '## Learning Interactions\n\n';
        
        if (lectureAnswers.length > 0) {
            interactionsSection += '### 📚 Interactive Lecture Responses\n';
            lectureAnswers.forEach((answer, index) => {
                interactionsSection += `${index + 1}. **${answer.question}**\n   - Answer: ${answer.answer}\n   - Time: ${new Date(answer.timestamp).toLocaleString()}\n\n`;
            });
        }
        
        if (practiceTexts.length > 0) {
            interactionsSection += '### 🏋️ Practice Section Inputs\n';
            practiceTexts.forEach((input, index) => {
                interactionsSection += `${index + 1}. **Input ${input.inputId}**\n   - Content: ${input.content.substring(0, 100)}${input.content.length > 100 ? '...' : ''}\n   - Time: ${new Date(input.timestamp).toLocaleString()}\n\n`;
            });
        }
        
        if (discussionTexts.length > 0) {
            interactionsSection += '### 💬 Discussion Section Inputs\n';
            discussionTexts.forEach((input, index) => {
                interactionsSection += `${index + 1}. **Input ${input.inputId}**\n   - Content: ${input.content.substring(0, 100)}${input.content.length > 100 ? '...' : ''}\n   - Time: ${new Date(input.timestamp).toLocaleString()}\n\n`;
            });
        }
        
        if (userData.summary.totalInteractions === 0) {
            interactionsSection += 'No interactions recorded yet. Complete some activities to see detailed results here.\n\n';
        }
        
        markdownContent.textContent = `# Learning Report: Community Advocacy & Civic Engagement

## Course Information
- **Course Code:** CIVICS 2025
- **Student:** Student
- **Status:** ${userData.summary.overallProgress >= 100 ? 'Completed' : userData.summary.overallProgress > 0 ? 'In Progress' : 'Getting Started'}
- **Generated:** ${new Date(userData.timestamp).toLocaleString()}

## Summary Statistics
- **Overall Progress:** ${userData.summary.overallProgress}%
- **Total Time Spent:** ${Math.round((Date.now() - (JSON.parse(localStorage.getItem('courseStartTime') || Date.now()))) / 60000)} minutes
- **Sections Completed:** ${[userData.summary.lectureProgress, userData.summary.practiceProgress, userData.summary.discussionProgress].filter(p => p >= 100).length}/3
- **Total Interactions:** ${userData.summary.totalInteractions}

## Section Details

### 📚 Interactive Lecture
- **Progress:** ${userData.summary.lectureProgress}%
- **Status:** ${userData.summary.lectureProgress >= 100 ? 'Completed ✅' : userData.summary.lectureProgress > 0 ? 'In Progress ⏳' : 'Ready to start ⭕'}
- **Multiple Choice Answers:** ${userData.summary.lectureAnswers}
- **Interactions:** ${userData.sections.lecture.length}

### 💬 Practice & Discussion
- **Progress:** ${userData.summary.practiceProgress}%
- **Status:** ${userData.summary.practiceProgress >= 100 ? 'Completed ✅' : userData.summary.practiceProgress > 0 ? 'In Progress ⏳' : 'Ready to start ⭕'}
- **Text Inputs:** ${userData.summary.practiceInputs}
- **Interactions:** ${userData.sections.practice.length}

### 🎯 Reflect & Assess
- **Progress:** ${userData.summary.discussionProgress}%
- **Status:** ${userData.summary.discussionProgress >= 100 ? 'Completed ✅' : userData.summary.discussionProgress > 0 ? 'In Progress ⏳' : 'Ready to start ⭕'}
- **Text Inputs:** ${userData.summary.discussionInputs}
- **Interactions:** ${userData.sections.discussion.length}

${interactionsSection}

## Performance Analysis
**Completion Rate:** ${userData.summary.overallProgress}%
**Status:** ${userData.summary.overallProgress >= 100 ? 'Course completed! 🎉' : userData.summary.overallProgress > 50 ? 'Making great progress! 📈' : userData.summary.overallProgress > 0 ? 'Just getting started. 🚀' : 'Ready to begin your learning journey! 🌟'}

---
*Report generated by Course Container System v1.0*`;
    }
}
// Enhanced report modal with PDF and Markdown features
function createSimpleReportModal() {
    // Remove existing modal if it exists
    const existingModal = document.getElementById('simpleReportModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.id = 'simpleReportModal';
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4';
    modal.style.display = 'none';
    
    modal.innerHTML = `
        <div class="bg-white dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
            <div class="flex justify-between items-center p-6 border-b dark:border-gray-600 bg-gray-50 dark:bg-gray-700">
                <h3 class="text-xl font-bold text-gray-900 dark:text-white">📊 Learning Progress Report</h3>
                <button onclick="closeSimpleReport()" 
                        class="text-gray-500 hover:text-gray-700 p-2 rounded-lg transition-colors">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
            
            <!-- Tab Navigation -->
            <div class="border-b dark:border-gray-600 bg-gray-50 dark:bg-gray-700">
                <nav class="flex space-x-8 px-6">
                    <button class="tab-btn active py-4 px-2 border-b-2 border-blue-500 text-blue-600 font-medium text-sm" data-tab="visual" onclick="switchTab('visual')">
                        📊 Visual Report
                    </button>
                    <button class="tab-btn py-4 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-700 font-medium text-sm" data-tab="markdown" onclick="switchTab('markdown')">
                        📝 Markdown
                    </button>
                </nav>
            </div>
            
            <!-- Tab Content -->
            <div class="flex-1 overflow-auto">
                <!-- Visual Tab -->
                <div id="visualTabContent" class="tab-content p-6">
                    <div class="space-y-6">
                        <!-- Header -->
                       <!-- Header -->
                <div class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 p-6 rounded-lg">
                    <div class="text-center">
                        <div class="text-4xl mb-4">🎓</div>
                        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                            Community Advocacy & Civic Engagement
                        </h2>
                        <p class="text-gray-600 dark:text-gray-400 mb-4">Course Code: CIVICS 2025</p>
                        <div class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-green-100 text-green-800">
                            <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                            Active Course
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6" id="reportStats">
                        <!-- Dynamic stats will be populated here -->
                    </div>
                </div>  

                        <!-- Section Details -->
                        <div class="grid gap-4">
                            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg border border-blue-200">
                                <div class="flex items-center justify-between mb-3">
                                    <h4 class="text-lg font-semibold text-gray-900 dark:text-white">⭕ 📚 Interactive Lecture</h4>
                                    <span class="text-blue-600 font-bold">0%</span>
                                </div>
                                <div class="mb-3">
                                    <div class="bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                                        <div class="bg-blue-500 h-2 rounded-full" style="width: 0%"></div>
                                    </div>
                                </div>
                                <div class="grid grid-cols-2 gap-4 text-sm">
                                    <div><span class="text-gray-600">Time:</span> <span class="font-medium ml-1">0m</span></div>
                                    <div><span class="text-gray-600">Status:</span> <span class="font-medium ml-1">Ready to start</span></div>
                                </div>
                            </div>

                            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg border border-green-200">
                                <div class="flex items-center justify-between mb-3">
                                    <h4 class="text-lg font-semibold text-gray-900 dark:text-white">⭕ 💬 Practice & Discussion</h4>
                                    <span class="text-green-600 font-bold">0%</span>
                                </div>
                                <div class="mb-3">
                                    <div class="bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                                        <div class="bg-green-500 h-2 rounded-full" style="width: 0%"></div>
                                    </div>
                                </div>
                                <div class="grid grid-cols-2 gap-4 text-sm">
                                    <div><span class="text-gray-600">Time:</span> <span class="font-medium ml-1">0m</span></div>
                                    <div><span class="text-gray-600">Status:</span> <span class="font-medium ml-1">Ready to start</span></div>
                                </div>
                            </div>

                            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg border border-purple-200">
                                <div class="flex items-center justify-between mb-3">
                                    <h4 class="text-lg font-semibold text-gray-900 dark:text-white">⭕ 🎯 Reflect & Assess</h4>
                                    <span class="text-purple-600 font-bold">0%</span>
                                </div>
                                <div class="mb-3">
                                    <div class="bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                                        <div class="bg-purple-500 h-2 rounded-full" style="width: 0%"></div>
                                    </div>
                                </div>
                                <div class="grid grid-cols-2 gap-4 text-sm">
                                    <div><span class="text-gray-600">Time:</span> <span class="font-medium ml-1">0m</span></div>
                                    <div><span class="text-gray-600">Status:</span> <span class="font-medium ml-1">Ready to start</span></div>
                                </div>
                            </div>
                        </div>

                        <!-- Generated Info -->
                        <div class="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg text-center">
                            <p class="text-sm text-gray-600 dark:text-gray-400">
                                Report generated on ${new Date().toLocaleString()}
                            </p>
                            <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">
                                Complete sections to see detailed progress analytics
                            </p>
                        </div>
                    </div>
                </div>
                
                <!-- Markdown Tab -->
                <div id="markdownTabContent" class="tab-content p-6 hidden">
                    <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-4">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Markdown Report</span>
                            <button id="copyMarkdownBtn" onclick="copyMarkdownReport()" class="text-blue-600 hover:text-blue-800 text-sm flex items-center gap-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                                </svg>
                                Copy
                            </button>
                        </div>
                        <pre id="markdownContent" class="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap font-mono max-h-96 overflow-auto"># Learning Report: Community Advocacy & Civic Engagement

## Course Information
- **Course Code:** CIVICS 2025
- **Student:** Student
- **Status:** Getting Started
- **Generated:** ${new Date().toLocaleString()}

## Summary Statistics
- **Overall Progress:** 0%
- **Total Time Spent:** 0 minutes
- **Sections Completed:** 0/3
- **Total Interactions:** 0

## Section Details

### 📚 Interactive Lecture
- **Progress:** 0%
- **Status:** Ready to start ⭕
- **Time Spent:** 0 minutes
- **Interactions:** 0

### 💬 Practice & Discussion
- **Progress:** 0%
- **Status:** Ready to start ⭕
- **Time Spent:** 0 minutes
- **Interactions:** 0

### 🎯 Reflect & Assess
- **Progress:** 0%
- **Status:** Ready to start ⭕
- **Time Spent:** 0 minutes
- **Interactions:** 0

## Learning Timeline
- **${new Date().toLocaleString()}:** Report generated

## Performance Analysis
**Completion Rate:** 0%
**Status:** Just getting started. 🚀

---
*Report generated by Course Container System v1.0*</pre>
                    </div>
                </div>
            </div>
            
            <!-- Footer with action buttons -->
            <div class="border-t dark:border-gray-600 p-4 bg-gray-50 dark:bg-gray-700">
                <div class="flex justify-between items-center">
                    <button onclick="closeSimpleReport()" 
                            class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition-colors">
                        Close
                    </button>
                    <div class="flex gap-2">
                        <button onclick="downloadMarkdownReport()" 
                                class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors flex items-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-4-4m4 4l4-4m-6 8h8a2 2 0 002-2V7a2 2 0 00-2-2H9a2 2 0 00-2 2v11a2 2 0 002 2z"></path>
                            </svg>
                            Download MD
                        </button>
                        <button onclick="downloadPDFReport()" 
                                class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors flex items-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                            </svg>
                            Download PDF
                        </button>
                        <button onclick="downloadJSONReport()" 
                                class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-4-4m4 4l4-4m-6 8h8a2 2 0 002-2V7a2 2 0 00-2-2H9a2 2 0 00-2 2v11a2 2 0 002 2z"></path>
                            </svg>
                            Download JSON
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close when clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeSimpleReport();
        }
    });
    
    // Close with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            closeSimpleReport();
        }
    });
    
    return modal;
}

// Function to close simple report
function closeSimpleReport() {
    const modal = document.getElementById('simpleReportModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

 // Tab switching function
function switchTab(tabName) {
    // Update button states
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.classList.remove('active', 'border-blue-500', 'text-blue-600');
        btn.classList.add('border-transparent', 'text-gray-500');
    });
    
    const activeBtn = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active', 'border-blue-500', 'text-blue-600');
        activeBtn.classList.remove('border-transparent', 'text-gray-500');
    }
    
    // Update content visibility
    const visualTab = document.getElementById('visualTabContent');
    const markdownTab = document.getElementById('markdownTabContent');
    
    if (tabName === 'visual') {
        visualTab.classList.remove('hidden');
        markdownTab.classList.add('hidden');
    } else {
        visualTab.classList.add('hidden');
        markdownTab.classList.remove('hidden');
    }
}

// Copy markdown to clipboard
function copyMarkdownReport() {
    const markdownContent = document.getElementById('markdownContent');
    const copyBtn = document.getElementById('copyMarkdownBtn');
    
    if (markdownContent && copyBtn) {
        navigator.clipboard.writeText(markdownContent.textContent).then(() => {
            copyBtn.innerHTML = `
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                Copied!
            `;
            setTimeout(() => {
                copyBtn.innerHTML = `
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                    </svg>
                    Copy
                `;
            }, 2000);
        }).catch(err => {
            alert('Failed to copy to clipboard');
            console.error('Copy failed:', err);
        });
    }
}

// Download markdown file
function downloadMarkdownReport() {
    const markdownContent = document.getElementById('markdownContent');
    if (markdownContent) {
        const timestamp = new Date().toISOString().split('T')[0];
        const filename = `learning-report-${timestamp}.md`;
        
        const blob = new Blob([markdownContent.textContent], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        URL.revokeObjectURL(url);
        
        // Show notification
        if (window.notificationManager) {
            window.notificationManager.show(`Downloaded ${filename}`, 'success');
        } else {
            alert(`Downloaded ${filename}`);
        }
    }
}

// Download PDF (using print dialog)
function downloadPDFReport() {
    const timestamp = new Date().toISOString().split('T')[0];
    const printWindow = window.open('', '_blank');
    
    // Get the visual report content
    const visualContent = document.getElementById('visualTabContent');
    const reportHTML = visualContent ? visualContent.innerHTML : '<p>No content available</p>';
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Learning Report - Community Advocacy Course</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    line-height: 1.6; 
                    color: #333; 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 20px; 
                }
                .space-y-6 > * + * { margin-top: 1.5rem; }
                .grid { display: grid; }
                .grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
                .grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
                .gap-4 { gap: 1rem; }
                .p-6 { padding: 1.5rem; }
                .p-4 { padding: 1rem; }
                .rounded-lg { border-radius: 0.5rem; }
                .text-center { text-align: center; }
                .font-bold { font-weight: bold; }
                .text-2xl { font-size: 1.5rem; }
                .text-lg { font-size: 1.125rem; }
                .text-sm { font-size: 0.875rem; }
                .mb-4 { margin-bottom: 1rem; }
                .mb-3 { margin-bottom: 0.75rem; }
                .mb-2 { margin-bottom: 0.5rem; }
                .mt-6 { margin-top: 1.5rem; }
                .border { border: 1px solid #e5e7eb; }
                .bg-gradient-to-r { background: linear-gradient(90deg, #f0f9ff 0%, #faf5ff 100%); }
                .bg-gray-50 { background-color: #f9fafb; }
                .bg-white { background-color: white; }
                .text-blue-600 { color: #2563eb; }
                .text-green-600 { color: #16a34a; }
                .text-purple-600 { color: #9333ea; }
                .text-orange-600 { color: #ea580c; }
                .text-gray-600 { color: #4b5563; }
                .text-gray-900 { color: #111827; }
                .bg-blue-500 { background-color: #3b82f6; }
                .bg-green-500 { background-color: #22c55e; }
                .bg-purple-500 { background-color: #a855f7; }
                .bg-gray-200 { background-color: #e5e7eb; }
                .h-2 { height: 0.5rem; }
                .rounded-full { border-radius: 9999px; }
                .border-blue-200 { border-color: #bfdbfe; }
                .border-green-200 { border-color: #bbf7d0; }
                .border-purple-200 { border-color: #e9d5ff; }
                @media print {
                    body { print-color-adjust: exact; }
                    .no-print { display: none; }
                }
            </style>
        </head>
        <body>
            <h1 style="text-align: center; margin-bottom: 2rem;">Learning Progress Report</h1>
            <p style="text-align: center; margin-bottom: 2rem;"><strong>Generated:</strong> ${new Date().toLocaleString()}</p>
            ${reportHTML}
            <div style="margin-top: 2rem; text-align: center; font-size: 0.875rem; color: #666;">
                Report generated by Course Container System
            </div>
        </body>
        </html>
    `);
    
    printWindow.document.close();
    
    setTimeout(() => {
        printWindow.print();
    }, 500);
    
    // Show notification
    if (window.notificationManager) {
        window.notificationManager.show('PDF generation started - use browser print dialog', 'info');
    } else {
        alert('PDF generation started - use your browser\'s print dialog to save as PDF');
    }
}

// Download JSON report
function downloadJSONReport() {
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `learning-report-${timestamp}.json`;
    
    const reportData = {
        courseInfo: {
            name: 'Community Advocacy & Civic Engagement',
            code: 'CIVICS 2025',
            generatedAt: new Date().toISOString()
        },
        progress: {
            overall: 0,
            sections: {
                lecture: { progress: 0, completed: false },
                practice: { progress: 0, completed: false },
                reflect: { progress: 0, completed: false }
            }
        },
        statistics: {
            timeSpent: 0,
            interactions: 0,
            sectionsCompleted: 0
        },
        metadata: {
            version: '1.0',
            platform: 'Course Container System'
        }
    };
    
    const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.style.display = 'none';
    
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    URL.revokeObjectURL(url);
    
    // Show notification
    if (window.notificationManager) {
        window.notificationManager.show(`Downloaded ${filename}`, 'success');
    } else {
        alert(`Downloaded ${filename}`);
    }
}

// Function to override any content's generateReport function
function overrideContentReportFunctions() {
    console.log('🔧 Overriding content report functions...');
    
    // Store original if it exists
    if (typeof window.generateReport === 'function' && !window.originalGenerateReport) {
        window.originalGenerateReport = window.generateReport;
    }
    
// Our enhanced generateReport function
const enhancedGenerateReport = function() {
    console.log('🚀 Enhanced generateReport called');
    try {
        // Collect user data first
        const userData = collectUserData();
        console.log('📊 User data collected:', userData);
        
        // Remove any existing modal first
        const existingModal = document.getElementById('simpleReportModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        const modal = createSimpleReportModal();
        modal.style.display = 'flex';
        
        // Populate with real data after a short delay
        setTimeout(() => {
            populateReportContent(userData);
            console.log('✅ Report populated with real data');
        }, 100);
        
        console.log('✅ Enhanced modal created and shown');
    } catch (error) {
        console.error('❌ Error with enhanced report:', error);
        // Fallback to original if our enhanced version fails
        if (window.originalGenerateReport && typeof window.originalGenerateReport === 'function') {
            console.log('🔄 Falling back to original generateReport');
            window.originalGenerateReport();
        } else {
            alert('Report function temporarily unavailable');
        }
    }
};
    
    // Override both global and window versions
    window.generateReport = enhancedGenerateReport;
    if (typeof generateReport !== 'undefined') {
        generateReport = enhancedGenerateReport;
    }
    
    // Also find and override any report buttons in the DOM
    const reportButtons = document.querySelectorAll('button[onclick*="generateReport"], #reportBtn, .report-btn');
    reportButtons.forEach(btn => {
        console.log('🔗 Found report button:', btn);
        // Remove existing onclick
        btn.removeAttribute('onclick');
        // Add our enhanced function
        btn.onclick = enhancedGenerateReport;
    });
    
    console.log('✅ Report functions overridden with enhanced version');
}

// Function to set up data collection for interactive content
function setupInteractiveDataCollection(section) {
    console.log('🔧 Setting up data collection for:', section);
    
    // Ensure report button exists
    ensureReportButtonExists();
    
    if (section === 'lecture') {
        setupLectureDataCollection();
    } else if (section === 'practice') {
        setupPracticeDataCollection();
    } else if (section === 'discussion') {
        setupDiscussionDataCollection();
    }
}

// Set up data collection for interactive lecture
function setupLectureDataCollection() {
    console.log('📚 Setting up lecture data collection...');
    
    // Monitor all choice buttons
    const choiceButtons = document.querySelectorAll('button[data-choice], .choice-btn, button[onclick*="choice"]');
    choiceButtons.forEach((btn, index) => {
        btn.addEventListener('click', function() {
            const questionText = this.closest('.question')?.querySelector('h3, .question-text')?.textContent || `Question ${index + 1}`;
            const choiceText = this.textContent || this.getAttribute('data-choice') || `Choice ${index + 1}`;
            
            console.log('📝 MC Answer recorded:', { questionText, choiceText });
            
            // Save to our data store
            if (!window.interactionData) window.interactionData = {};
            if (!window.interactionData.lecture) window.interactionData.lecture = [];
            
            window.interactionData.lecture.push({
                type: 'multiple_choice',
                question: questionText,
                answer: choiceText,
                timestamp: new Date().toISOString(),
                section: 'lecture'
            });
            
            // Save to localStorage
            localStorage.setItem('courseInteractionData', JSON.stringify(window.interactionData));
            console.log('💾 Lecture data saved to localStorage');
        });
    });
    
    // Monitor performance/progress
    const progressElements = document.querySelectorAll('.progress, [data-progress], .score');
    progressElements.forEach(el => {
        const observer = new MutationObserver(() => {
            const progressText = el.textContent;
            if (progressText && progressText.includes('%') || progressText.includes('score')) {
                console.log('📊 Performance recorded:', progressText);
                
                if (!window.interactionData) window.interactionData = {};
                if (!window.interactionData.lecture) window.interactionData.lecture = [];
                
                window.interactionData.lecture.push({
                    type: 'performance',
                    data: progressText,
                    timestamp: new Date().toISOString(),
                    section: 'lecture'
                });
                
                localStorage.setItem('courseInteractionData', JSON.stringify(window.interactionData));
            }
        });
        
        observer.observe(el, { childList: true, subtree: true, characterData: true });
    });
    
    console.log('✅ Lecture data collection active');
}

// Set up data collection for practice section
function setupPracticeDataCollection() {
    console.log('🏋️ Setting up practice data collection...');
    
    // Monitor text inputs and textareas
    const textInputs = document.querySelectorAll('input[type="text"], textarea, [contenteditable="true"]');
    textInputs.forEach((input, index) => {
        input.addEventListener('input', debounce(function() {
            const value = this.value || this.textContent;
            if (value && value.trim().length > 2) {
                console.log('✍️ Practice text recorded:', value.substring(0, 50) + '...');
                
                if (!window.interactionData) window.interactionData = {};
                if (!window.interactionData.practice) window.interactionData.practice = [];
                
                // Update or add the entry
                const existingIndex = window.interactionData.practice.findIndex(item => 
                    item.inputId === (this.id || `input-${index}`)
                );
                
                const entry = {
                    type: 'text_input',
                    inputId: this.id || `input-${index}`,
                    content: value,
                    timestamp: new Date().toISOString(),
                    section: 'practice'
                };
                
                if (existingIndex !== -1) {
                    window.interactionData.practice[existingIndex] = entry;
                } else {
                    window.interactionData.practice.push(entry);
                }
                
                localStorage.setItem('courseInteractionData', JSON.stringify(window.interactionData));
            }
        }, 1000));
    });
    
    console.log('✅ Practice data collection active');
}

// Set up data collection for discussion section
function setupDiscussionDataCollection() {
    console.log('💬 Setting up discussion data collection...');
    
    // Monitor text inputs and textareas
    const textInputs = document.querySelectorAll('input[type="text"], textarea, [contenteditable="true"]');
    textInputs.forEach((input, index) => {
        input.addEventListener('input', debounce(function() {
            const value = this.value || this.textContent;
            if (value && value.trim().length > 2) {
                console.log('💬 Discussion text recorded:', value.substring(0, 50) + '...');
                
                if (!window.interactionData) window.interactionData = {};
                if (!window.interactionData.discussion) window.interactionData.discussion = [];
                
                // Update or add the entry
                const existingIndex = window.interactionData.discussion.findIndex(item => 
                    item.inputId === (this.id || `input-${index}`)
                );
                
                const entry = {
                    type: 'text_input',
                    inputId: this.id || `input-${index}`,
                    content: value,
                    timestamp: new Date().toISOString(),
                    section: 'discussion'
                };
                
                if (existingIndex !== -1) {
                    window.interactionData.discussion[existingIndex] = entry;
                } else {
                    window.interactionData.discussion.push(entry);
                }
                
                localStorage.setItem('courseInteractionData', JSON.stringify(window.interactionData));
            }
        }, 1000));
    });
    
    console.log('✅ Discussion data collection active');
}

// Function to ensure Generate Report button exists in all sections
function ensureReportButtonExists() {
    console.log('🔧 Ensuring Generate Report button exists...');
    
    // Check if button already exists
    let reportBtn = document.querySelector('#reportBtn, .report-btn, button[onclick*="generateReport"]');
    
    if (!reportBtn) {
        console.log('➕ Creating Generate Report button...');
        
        // Create the button
        reportBtn = document.createElement('button');
        reportBtn.id = 'reportBtn';
        reportBtn.className = 'bg-primary hover:bg-primary-dark text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors';
        reportBtn.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Generate Report
        `;
        reportBtn.onclick = generateReport;
        
        // Find a good place to insert it
        const contentArea = document.getElementById('contentArea');
        if (contentArea) {
            // Try to find a container or just append to content area
            const container = contentArea.querySelector('.container, .content, .main') || contentArea;
            
            // Create a button container
            const buttonContainer = document.createElement('div');
            buttonContainer.className = 'mt-6 flex justify-center';
            buttonContainer.appendChild(reportBtn);
            
            container.appendChild(buttonContainer);
            console.log('✅ Generate Report button added to page');
        }
    } else {
        // Button exists, make sure it uses our enhanced function
        reportBtn.onclick = generateReport;
        console.log('✅ Generate Report button found and enhanced');
    }
}

// Debounce function to avoid too many saves
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Override immediately
overrideContentReportFunctions();

// Override after content loads
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(overrideContentReportFunctions, 500);
});

// Override after any new content is loaded
setTimeout(overrideContentReportFunctions, 2000);
setTimeout(overrideContentReportFunctions, 5000);
console.log('📦 Course App loaded successfully');
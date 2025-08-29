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
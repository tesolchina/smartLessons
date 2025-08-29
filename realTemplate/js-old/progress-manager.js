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
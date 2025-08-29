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
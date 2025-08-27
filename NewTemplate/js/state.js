// js/state.js

// Holds shared data and functions accessible by all other scripts for the interactive module.

// Shared state for the application
let completionData = {
    slides: [false, false, false, false, false],
    tasks: [false, false, false, false, false, false], // 6 tasks (2 per section)
    interactions: [false, false, false]
};

// Global variable for the report data, accessible by report.js
window.currentReport = null;

// Central progress update function
function updateProgress() {
    // Check reflection task completion
    completionData.tasks[0] = !!document.getElementById('task1-response')?.value.trim();
    completionData.tasks[1] = !!document.getElementById('task1-interest')?.value.trim();
    completionData.tasks[2] = !!document.getElementById('task2-question')?.value.trim();
    completionData.tasks[3] = !!document.getElementById('task2-significance')?.value.trim();
    completionData.tasks[4] = !!document.getElementById('task3-impact')?.value.trim();
    completionData.tasks[5] = !!document.getElementById('task3-challenges')?.value.trim();
    
    // Calculate overall progress
    const allItems = [
        ...completionData.slides, 
        ...completionData.tasks, 
        ...completionData.interactions
    ];
    const completedItems = allItems.filter(item => item).length;
    const totalItems = allItems.length;
    
    const progress = totalItems > 0 ? Math.round((completedItems / totalItems) * 100) : 0;
    
    // Update UI elements if they exist
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');

    if (progressBar) progressBar.style.width = `${progress}%`;
    if (progressText) progressText.textContent = `${progress}% Complete`;
}
// Slide 02 - Learning Objectives
console.log('🎯 Slide 02 JavaScript module loaded - Learning Objectives');

// Add any interactive functionality for slide 02 here
function initializeSlide02() {
    console.log('🎯 Initializing Learning Objectives slide');
    
    // Add hover effects to objectives
    const objectives = document.querySelectorAll('.slide02-content .flex');
    objectives.forEach((objective, index) => {
        objective.addEventListener('mouseenter', () => {
            objective.style.transform = 'translateX(10px)';
            objective.style.transition = 'transform 0.3s ease';
        });
        
        objective.addEventListener('mouseleave', () => {
            objective.style.transform = 'translateX(0)';
        });
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeSlide02);
} else {
    initializeSlide02();
}
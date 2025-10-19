// Slide 03 - Traditional vs Flipped Classroom
console.log('🔄 Slide 03 JavaScript module loaded - Traditional vs Flipped');

// Add any interactive functionality for slide 03 here
function initializeSlide03() {
    console.log('🔄 Initializing Traditional vs Flipped slide');
    
    // Add comparison animation
    const cards = document.querySelectorAll('.slide03-content .grid > div');
    
    cards.forEach((card, index) => {
        // Stagger the animation
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.6s ease-out';
            
            // Animate in
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        }, index * 200);
        
        // Add hover effect
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px) scale(1.02)';
            card.style.boxShadow = '0 10px 25px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
            card.style.boxShadow = '';
        });
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeSlide03);
} else {
    initializeSlide03();
}
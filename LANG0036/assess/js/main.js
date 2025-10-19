import assessments from '../assessments/index.js';
import summaryData from './summary-data.js';
import { createAssessmentItem } from '../components/assessment-item.js';
import { createSummarySection } from '../components/summary-section.js';

// Load header
fetch('./components/header.html')
    .then(response => response.text())
    .then(data => {
        document.getElementById('header-container').innerHTML = data;
    });

// Load assessment grid
document.addEventListener('DOMContentLoaded', function() {
    // Create assessment grid
    const assessmentGridContainer = document.getElementById('assessment-grid-container');
    let assessmentGridHTML = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">';
    
    assessments.forEach(assessment => {
        assessmentGridHTML += createAssessmentItem(assessment);
    });
    
    assessmentGridHTML += '</div>';
    assessmentGridContainer.innerHTML = assessmentGridHTML;
    
    // Create summary section
    const summaryContainer = document.getElementById('summary-section-container');
    summaryContainer.innerHTML = createSummarySection(summaryData);
    
    // Initialize animations with a slight delay for iframe loading
    setTimeout(() => {
        const circles = document.querySelectorAll('.assessment-circle');
        circles.forEach((circle, index) => {
            setTimeout(() => {
                circle.style.opacity = '1';
                circle.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }, 300);
    
    // Send height to parent if in iframe
    function sendHeight() {
        if (window.self !== window.top) {
            const height = document.body.scrollHeight;
            window.parent.postMessage({ height: height }, '*');
        }
    }
    
    // Send height after content loads and on resize
    window.addEventListener('load', sendHeight);
    window.addEventListener('resize', sendHeight);
});

// Dark mode functionality
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.classList.add('dark');
}
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    if (event.matches) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
});

// Toggle details functionality - needs to be global for the onclick attribute
window.toggleDetails = function(assessmentId) {
    const detailsPanel = document.getElementById(assessmentId);
    const isOpen = detailsPanel.classList.contains('open');
    
    // Close all other panels
    document.querySelectorAll('.details-panel').forEach(panel => {
        panel.classList.remove('open');
    });
    
    // Toggle current panel
    if (!isOpen) {
        detailsPanel.classList.add('open');
    }
    
    // Update iframe height after panel toggle
    setTimeout(() => {
        if (window.self !== window.top) {
            const height = document.body.scrollHeight;
            window.parent.postMessage({ height: height }, '*');
        }
    }, 300);
};

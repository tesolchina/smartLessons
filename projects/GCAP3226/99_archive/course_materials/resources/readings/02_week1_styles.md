# GCAP 3226 CSS File

**Downloaded:** 2025-09-06 18:11:11

---

```css
/* ============================================
   Course Container Template - Professional Styles
   ============================================ */

/* Core Transitions and Animations */
.section-transition {
    transition: all 0.3s ease-in-out;
}

.section-collapsed {
    opacity: 0.6;
    transform: scale(0.98);
}

.section-expanded {
    opacity: 1;
    transform: scale(1);
}

/* Progress Bar Styling */
.progress-bar {
    background: linear-gradient(90deg, #5D5CDE 0%, #7B7AE8 100%);
    height: 4px;
    border-radius: 2px;
    transition: width 0.5s ease;
}

/* Enhanced progress bars for sections */
.section-progress {
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Notification System */
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
    opacity: 0;
    transform: translateX(100%);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 8px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(10px);
}

.notification.show {
    opacity: 1;
    transform: translateX(0);
}

/* ============================================
   LAYOUT & SPACING OPTIMIZATIONS
   ============================================ */

/* Professional content width optimization */
.max-w-4xl {
    max-width: 1400px !important;
    width: 92% !important;
}

.mx-auto {
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Container padding optimization */
.container {
    padding-left: 1rem;
    padding-right: 1rem;
}

/* ============================================
   RESPONSIVE DESIGN
   ============================================ */

/* Large Desktop (1400px+) */
@media (min-width: 1400px) {
    .max-w-4xl {
        max-width: 1600px !important;
        width: 90% !important;
    }
    
    .container {
        padding-left: 2rem;
        padding-right: 2rem;
    }
}

/* Standard Desktop (1024px - 1399px) */
@media (min-width: 1024px) and (max-width: 1399px) {
    .max-w-4xl {
        width: 94% !important;
    }
}

/* Tablet (768px - 1023px) */
@media (min-width: 768px) and (max-width: 1023px) {
    .max-w-4xl {
        width: 96% !important;
    }
    
    /* Adjust grid layouts for tablet */
    .grid.md\\:grid-cols-3 {
        grid-template-columns: 1fr !important;
        gap: 1rem;
    }
    
    .grid.md\\:grid-cols-2 {
        grid-template-columns: 1fr !important;
        gap: 1.5rem;
    }
    
    /* Stack header elements on tablet */
    .flex.items-center.justify-between {
        flex-direction: column;
        gap: 1rem;
        align-items: stretch;
    }
}

/* Mobile (up to 767px) */
@media (max-width: 767px) {
    .max-w-4xl {
        width: 98% !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    
    .container {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }
    
    /* Mobile-specific adjustments */
    .grid.md\\:grid-cols-3,
    .grid.md\\:grid-cols-2,
    .grid.md\\:grid-cols-4 {
        grid-template-columns: 1fr !important;
        gap: 1rem;
    }
    
    /* Stack header elements on mobile */
    .flex.items-center.justify-between {
        flex-direction: column;
        gap: 1rem;
        align-items: stretch;
        text-align: center;
    }
    
    /* Adjust button sizes for mobile */
    .flex.gap-3 {
        flex-direction: column;
        gap: 0.75rem;
    }
    
    /* Better mobile typography */
    .text-3xl {
        font-size: 1.875rem !important; /* Reduce from 3xl to 2xl on mobile */
    }
    
    .text-2xl {
        font-size: 1.5rem !important; /* Reduce from 2xl to xl on mobile */
    }
}

/* Small Mobile (up to 480px) */
@media (max-width: 480px) {
    .max-w-4xl {
        width: 99% !important;
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
    }
    
    /* Reduce padding for very small screens */
    .p-6 {
        padding: 1rem !important;
    }
    
    .p-8 {
        padding: 1.5rem !important;
    }
}

/* ============================================
   ENHANCED UI COMPONENTS
   ============================================ */

/* Loading animation */
@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.5;
    }
}

.loading {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Loading indicator enhancement */
#loadingIndicator {
    background: linear-gradient(90deg, #5D5CDE, #7B7AE8, #5D5CDE);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
    0% {
        background-position: -200% 0;
    }
    100% {
        background-position: 200% 0;
    }
}

/* Button hover enhancements */
.section-btn {
    position: relative;
    overflow: hidden;
}

.section-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transition: left 0.5s;
}

.section-btn:hover::before {
    left: 100%;
}

/* Card shadow enhancements */
.bg-white.dark\\:bg-gray-800 {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    transition: box-shadow 0.3s ease;
}

.bg-white.dark\\:bg-gray-800:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* ============================================
   DARK MODE ENHANCEMENTS
   ============================================ */

/* Dark mode improvements */
@media (prefers-color-scheme: dark) {
    .bg-white {
        background-color: rgb(31 41 55) !important;
    }
    
    .notification {
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
}

/* Dark mode card enhancements */
.dark .bg-white {
    background-color: rgb(31 41 55) !important;
    border: 1px solid rgb(55 65 81);
}

.dark .section-btn {
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* ============================================
   ACCESSIBILITY ENHANCEMENTS
   ============================================ */

/* Focus indicators */
button:focus,
.section-btn:focus {
    outline: 2px solid #5D5CDE;
    outline-offset: 2px;
}

/* Reduced motion for accessibility */
@media (prefers-reduced-motion: reduce) {
    .section-transition,
    .notification,
    .progress-bar,
    .section-progress {
        transition: none !important;
    }
    
    .loading {
        animation: none !important;
    }
    
    #loadingIndicator {
        animation: none !important;
    }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    .bg-primary {
        background-color: #000000 !important;
    }
    
    .text-primary {
        color: #000000 !important;
    }
    
    .border-primary {
        border-color: #000000 !important;
    }
}

/* ============================================
   PRINT STYLES
   ============================================ */

@media print {
    .notification,
    #loadingIndicator,
    button {
        display: none !important;
    }
    
    .max-w-4xl {
        max-width: none !important;
        width: 100% !important;
    }
    
    .bg-gradient-to-r {
        background: #5D5CDE !important;
        color: white !important;
    }
}

/* ============================================
   UTILITY OVERRIDES
   ============================================ */

/* Ensure proper spacing in all contexts */
.space-y-4 > * + * {
    margin-top: 1rem !important;
}

.space-y-6 > * + * {
    margin-top: 1.5rem !important;
}

.space-y-8 > * + * {
    margin-top: 2rem !important;
}

/* Consistent border radius */
.rounded-lg {
    border-radius: 0.75rem !important;
}

.rounded-xl {
    border-radius: 1rem !important;
}

/* Performance optimizations */
* {
    box-sizing: border-box;
}

img {
    max-width: 100%;
    height: auto;
}

/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* ============================================
   COMPONENT-SPECIFIC ENHANCEMENTS
   ============================================ */

/* Progress tracker enhancements */
#progressTracker {
    border: 1px solid rgba(93, 92, 222, 0.2);
    background: linear-gradient(135deg, rgba(93, 92, 222, 0.02), rgba(123, 122, 232, 0.02));
}

/* Content area minimum height adjustment */
#contentArea {
    min-height: 60vh;
    transition: all 0.3s ease;
}

/* Section icon hover effects */
#sectionIcons .text-center {
    transition: transform 0.2s ease;
}

#sectionIcons .text-center:hover {
    transform: translateY(-2px);
}

/* Add this to your existing css/styles.css */

/* Report Modal Styles */
.max-h-90vh {
    max-height: 90vh;
}

.report-tab {
    transition: all 0.2s ease;
}

.report-tab:hover {
    background-color: rgba(93, 92, 222, 0.05);
}

.report-content {
    transition: opacity 0.3s ease;
}

/* Modal backdrop */
#reportModal {
    backdrop-filter: blur(5px);
}

/* Scrollbar styling for markdown textarea */
#markdownText::-webkit-scrollbar {
    width: 8px;
}

#markdownText::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

#markdownText::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}

#markdownText::-webkit-scrollbar-thumb:hover {
    background: #555;
}

/* Dark mode scrollbar */
.dark #markdownText::-webkit-scrollbar-track {
    background: #374151;
}

.dark #markdownText::-webkit-scrollbar-thumb {
    background: #6b7280;
}
```

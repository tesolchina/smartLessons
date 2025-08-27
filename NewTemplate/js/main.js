// js/main.js

// This is the main orchestrator for the interactive-activities.html page.
// It loads all HTML modules and then initializes the interactive components.

document.addEventListener('DOMContentLoaded', () => {
    const modules = [
        'overview',
        'learning-content',
        'interactive-activities',
        'reflection-tasks',
        'learning-report',
        'ai-assistant',
        'moodle-discussion'
    ];

    // Function to load an HTML module into its container
    const loadModule = async (moduleName) => {
        try {
            // 
            // THIS IS THE FIX: 
            // Removed the "modules/" prefix. The script will now look for files like "overview.html"
            // in the same directory as interactive-activities.html, which is correct.
            //
            const response = await fetch(`${moduleName}.html`);
            
            if (!response.ok) throw new Error(`Failed to load ${moduleName}.html`);
            const content = await response.text();
            
            const container = document.getElementById(`${moduleName}-container`);
            if (container) {
                container.innerHTML = content;
            }
        } catch (error) {
            console.error(error);
            const container = document.getElementById(`${moduleName}-container`);
            if(container) {
                container.innerHTML = `<div class="text-center p-8 bg-red-50 dark:bg-red-900/20 rounded-lg"><p class="text-red-600 dark:text-red-300">Error: Could not load content for this section.</p></div>`;
            }
        }
    };

    // Function to run after all modules are loaded and in the DOM
    const initializeApp = () => {
        // Initialize the starting state of all interactive components
        showSlide(1);
        showGame(1);
        showChatMessage(0);
        updateProgress(); // Set initial progress to 0%

        // Add event listeners for reflection tasks to update progress on input
        document.querySelectorAll('#reflection-tasks textarea').forEach(textarea => {
            textarea.addEventListener('input', updateProgress);
        });
    };

    // Main execution flow: Load all modules, then initialize the app
    const loadAllModules = async () => {
        await Promise.all(modules.map(loadModule));
        initializeApp();
    };

    loadAllModules();
});

// General utility function for the main page layout
function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (!section) return;

    const isCurrentlyHidden = section.style.display === 'none' || section.classList.contains('hidden');
    
    // Toggle visibility
    if (isCurrentlyHidden) {
        section.classList.remove('hidden');
        section.style.display = ''; // Reset display property
    } else {
        section.classList.add('hidden');
    }
    
    // Update button appearance for visual feedback
    const button = document.querySelector(`button[onclick="toggleSection('${sectionId}')"]`);
    if (button) {
        if (isCurrentlyHidden) {
            // Section is now visible
            button.style.opacity = '1';
            button.style.transform = 'scale(1)';
            button.style.filter = 'grayscale(0)';
            // Scroll to the section for better user experience
            setTimeout(() => {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);
        } else {
            // Section is now hidden
            button.style.opacity = '0.6';
            button.style.transform = 'scale(0.95)';
            button.style.filter = 'grayscale(0.5)';
        }
    }
}
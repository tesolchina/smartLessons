// Workshop Navigation and Component Loading
class WorkshopManager {
    constructor() {
        this.currentComponent = 'overview';
        this.components = ['overview', 'ai-video', 'streaming-avatars', 'implementation', 'resources'];
        this.init();
    }

    init() {
        // Set up event listeners for toggle buttons
        const buttons = document.querySelectorAll('.toggle-btn');
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                const componentId = e.target.getAttribute('data-component');
                this.showComponent(componentId);
            });
        });

        // Load initial component
        this.loadComponent('overview');
    }

    showComponent(componentId) {
        // Hide all components
        const components = document.querySelectorAll('.component');
        components.forEach(component => {
            component.classList.remove('active');
        });

        // Remove active class from all buttons
        const buttons = document.querySelectorAll('.toggle-btn');
        buttons.forEach(button => {
            button.classList.remove('active');
        });

        // Show selected component
        const selectedComponent = document.getElementById(componentId);
        if (selectedComponent) {
            selectedComponent.classList.add('active');
        }

        // Add active class to clicked button
        const clickedButton = document.querySelector(`[data-component="${componentId}"]`);
        if (clickedButton) {
            clickedButton.classList.add('active');
        }

        // Load component content if not already loaded
        this.loadComponent(componentId);
    }

    loadComponent(componentId) {
        const component = document.getElementById(componentId);

        // Check if component already has content loaded
        if (component && component.dataset.loaded !== 'true') {
            this.fetchComponentContent(componentId);
        }
    }

    async fetchComponentContent(componentId) {
        const component = document.getElementById(componentId);

        try {
            // Use fetch API with proper error handling
            const response = await fetch(`components/${componentId}.html`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const htmlContent = await response.text();
            
            // Parse the HTML content
            const parser = new DOMParser();
            const doc = parser.parseFromString(htmlContent, 'text/html');
            const bodyContent = doc.body.innerHTML;

            // Insert the content with animation
            component.style.opacity = '0';
            component.innerHTML = bodyContent;
            component.dataset.loaded = 'true';
            
            // Fade in the content
            setTimeout(() => {
                component.style.opacity = '1';
            }, 100);
            
        } catch (error) {
            console.error(`Error loading component ${componentId}:`, error);
            component.innerHTML = this.getErrorContent(componentId);
        }
    }

    getErrorContent(componentId) {
        return `
            <div class="error-content">
                <h2>Content Loading</h2>
                <p>The ${componentId} module is being prepared for your workshop experience.</p>
                <div class="loading-placeholder">
                    <div class="placeholder-line"></div>
                    <div class="placeholder-line"></div>
                    <div class="placeholder-line short"></div>
                </div>
                <p><em>This content will be dynamically loaded based on your workshop planning document.</em></p>
            </div>
        `;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WorkshopManager();
});

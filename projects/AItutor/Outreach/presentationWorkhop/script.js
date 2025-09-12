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

    fetchComponentContent(componentId) {
        const component = document.getElementById(componentId);

        // Use XMLHttpRequest to avoid CORS issues with local files
        const xhr = new XMLHttpRequest();
        xhr.open('GET', `components/${componentId}.html`, true);

        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300) {
                // Parse the HTML content
                const parser = new DOMParser();
                const doc = parser.parseFromString(xhr.responseText, 'text/html');
                const bodyContent = doc.body.innerHTML;

                // Insert the content
                component.innerHTML = bodyContent;
                component.dataset.loaded = 'true';
            } else {
                console.error(`Error loading ${componentId}: ${xhr.status}`);
                component.innerHTML = '<p>Error loading content. Please check the component file.</p>';
            }
        };

        xhr.onerror = () => {
            console.error(`Network error loading ${componentId}`);
            component.innerHTML = '<p>Error loading content. Please check your internet connection.</p>';
        };

        xhr.send();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WorkshopManager();
});

// Workshop Navigation and Component Loading
class WorkshopManager {
    constructor() {
        this.currentComponent = 'overview';
        this.components = ['overview', 'video-generation', 'avatar-interaction', 'vibe-coding', 'future-roadmap'];
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
            const bodyContent = doc.body ? doc.body.innerHTML : htmlContent;

            // Inject component-specific styles (from head) once per component
            const head = doc.head;
            if (head) {
                const styleNodes = head.querySelectorAll('style, link[rel="stylesheet"]');
                styleNodes.forEach((node, idx) => {
                    const marker = `comp-style-${componentId}-${idx}`;
                    if (!document.head.querySelector(`[data-style-marker="${marker}"]`)) {
                        const clone = node.cloneNode(true);
                        clone.setAttribute('data-style-marker', marker);
                        document.head.appendChild(clone);
                    }
                });
            }

            // Insert the content with animation
            component.style.opacity = '0';
            component.innerHTML = bodyContent;
            component.dataset.loaded = 'true';
            
            // Execute scripts after content is loaded
            this.executeScripts(component);
            
            // Fade in the content
            setTimeout(() => {
                component.style.opacity = '1';
            }, 100);
            
        } catch (error) {
            console.error(`Error loading component ${componentId}:`, error);
            component.innerHTML = this.getErrorContent(componentId);
        }
    }

    executeScripts(container) {
        // Find all script tags in the loaded content
        const scripts = container.querySelectorAll('script');
        scripts.forEach(oldScript => {
            // Create a new script element
            const newScript = document.createElement('script');
            
            // Copy all attributes
            Array.from(oldScript.attributes).forEach(attr => {
                newScript.setAttribute(attr.name, attr.value);
            });
            
            // Copy the script content
            newScript.textContent = oldScript.textContent;
            
            // Replace the old script with the new one to trigger execution
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
        
        console.log('Scripts executed for component:', container.id);
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

// Global function for demo toggles in slides
function toggleDemo(demoId) {
    const demoArea = document.getElementById(demoId);
    const toggleBtn = document.querySelector(`[onclick="toggleDemo('${demoId}')"]`);
    
    if (demoArea) {
        if (demoArea.style.display === 'none' || demoArea.style.display === '') {
            demoArea.style.display = 'block';
            if (toggleBtn) {
                toggleBtn.textContent = toggleBtn.textContent.replace('Show', 'Hide');
            }
        } else {
            demoArea.style.display = 'none';
            if (toggleBtn) {
                toggleBtn.textContent = toggleBtn.textContent.replace('Hide', 'Show');
            }
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WorkshopManager();
});

/**
 * Module Loader for Presentation Slides
 * Manages loading and switching between slide modules
 */

class SlideModuleLoader {
    constructor() {
        this.currentSlide = 1;
        this.totalSlides = 15;
        this.modules = new Map();
        this.loadedModules = new Set();
        this.init();
    }
    
    init() {
        console.log('SlideModuleLoader initialized');
        this.preloadCriticalModules();
    }
    
    /**
     * Load a specific slide module
     * @param {number} slideNumber - The slide number to load (1-15)
     * @returns {Promise} - Promise that resolves when module is loaded
     */
    async loadSlideModule(slideNumber) {
        const slideKey = this.getSlideKey(slideNumber);
        
        // Return cached module if already loaded
        if (this.modules.has(slideKey)) {
            return this.modules.get(slideKey);
        }
        
        try {
            // Load slide content
            const moduleContent = await this.fetchSlideContent(slideNumber);
            
            // Store in cache
            this.modules.set(slideKey, moduleContent);
            this.loadedModules.add(slideNumber);
            
            console.log(`Slide ${slideNumber} module loaded successfully`);
            return moduleContent;
            
        } catch (error) {
            console.error(`Failed to load slide ${slideNumber} module:`, error);
            return this.getFallbackContent(slideNumber);
        }
    }
    
    /**
     * Fetch slide content from the modules directory
     * @param {number} slideNumber - The slide number to fetch
     * @returns {Promise<Object>} - Promise that resolves to slide content object
     */
    async fetchSlideContent(slideNumber) {
        const slideKey = this.getSlideKey(slideNumber);
        const basePath = `modules/${slideKey}`;
        
        try {
            // Fetch HTML content
            const htmlResponse = await fetch(`${basePath}/${slideKey}.html`);
            const htmlContent = htmlResponse.ok ? await htmlResponse.text() : null;
            
            // Try to load JavaScript module
            let jsModule = null;
            try {
                // Dynamic import for JavaScript module
                jsModule = await import(`../${basePath}/${slideKey}.js`);
            } catch (jsError) {
                console.log(`No JS module found for ${slideKey}, using default behavior`);
            }
            
            return {
                slideNumber,
                html: htmlContent || this.getDefaultHTML(slideNumber),
                jsModule: jsModule,
                cssPath: `${basePath}/${slideKey}.css`,
                loaded: true
            };
            
        } catch (error) {
            console.error(`Error fetching slide ${slideNumber} content:`, error);
            throw error;
        }
    }
    
    /**
     * Switch to a specific slide module
     * @param {number} slideNumber - The slide number to switch to
     * @param {HTMLElement} targetContainer - The container to render the slide in
     */
    async switchToSlide(slideNumber, targetContainer) {
        try {
            // Load the slide module
            const moduleContent = await this.loadSlideModule(slideNumber);
            
            // Cleanup previous slide if needed
            this.cleanupCurrentSlide();
            
            // Render the new slide
            this.renderSlideContent(moduleContent, targetContainer);
            
            // Initialize slide-specific functionality
            this.initializeSlideModule(moduleContent);
            
            // Update current slide tracker
            this.currentSlide = slideNumber;
            
            console.log(`Switched to slide ${slideNumber}`);
            
        } catch (error) {
            console.error(`Failed to switch to slide ${slideNumber}:`, error);
            this.renderFallbackContent(slideNumber, targetContainer);
        }
    }
    
    /**
     * Render slide content in the target container
     * @param {Object} moduleContent - The slide module content
     * @param {HTMLElement} targetContainer - The container to render in
     */
    renderSlideContent(moduleContent, targetContainer) {
        if (!targetContainer) {
            console.error('Target container not found');
            return;
        }
        
        // Clear previous content
        targetContainer.innerHTML = '';
        
        // Insert HTML content
        if (moduleContent.html) {
            targetContainer.innerHTML = moduleContent.html;
        }
        
        // Load CSS if exists
        this.loadSlideCSS(moduleContent.cssPath);
        
        // Add fade-in animation
        targetContainer.style.opacity = '0';
        setTimeout(() => {
            targetContainer.style.opacity = '1';
        }, 50);
    }
    
    /**
     * Initialize slide-specific JavaScript module
     * @param {Object} moduleContent - The slide module content
     */
    initializeSlideModule(moduleContent) {
        if (moduleContent.jsModule && moduleContent.jsModule.default) {
            const slideModule = moduleContent.jsModule.default;
            if (typeof slideModule.init === 'function') {
                slideModule.init();
            }
        }
    }
    
    /**
     * Cleanup current slide before switching
     */
    cleanupCurrentSlide() {
        const currentModule = this.modules.get(this.getSlideKey(this.currentSlide));
        if (currentModule && currentModule.jsModule && currentModule.jsModule.default) {
            const slideModule = currentModule.jsModule.default;
            if (typeof slideModule.cleanup === 'function') {
                slideModule.cleanup();
            }
        }
    }
    
    /**
     * Load slide-specific CSS
     * @param {string} cssPath - Path to the CSS file
     */
    loadSlideCSS(cssPath) {
        const existingLink = document.querySelector(`link[href="${cssPath}"]`);
        if (!existingLink) {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = cssPath;
            link.onerror = () => console.log(`CSS not found: ${cssPath}`);
            document.head.appendChild(link);
        }
    }
    
    /**
     * Preload critical slide modules (slide 1 and next few slides)
     */
    async preloadCriticalModules() {
        const criticalSlides = [1, 2, 3];
        for (const slideNum of criticalSlides) {
            try {
                await this.loadSlideModule(slideNum);
            } catch (error) {
                console.log(`Failed to preload slide ${slideNum}:`, error);
            }
        }
    }
    
    /**
     * Get slide key with zero-padding
     * @param {number} slideNumber - The slide number
     * @returns {string} - Formatted slide key (e.g., "slide01")
     */
    getSlideKey(slideNumber) {
        return `slide${slideNumber.toString().padStart(2, '0')}`;
    }
    
    /**
     * Get default HTML content for a slide
     * @param {number} slideNumber - The slide number
     * @returns {string} - Default HTML content
     */
    getDefaultHTML(slideNumber) {
        const slideData = this.getSlideData(slideNumber);
        return `
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow border border-gray-200 dark:border-gray-700">
                <div class="text-center">
                    <div class="text-4xl mb-4">${slideData.icon}</div>
                    <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-3">${slideData.title}</h2>
                    <p class="text-gray-600 dark:text-gray-400 mb-4">${slideData.description}</p>
                    <div class="text-sm text-${slideData.color}-600 dark:text-${slideData.color}-400 mb-4 font-medium">
                        Slide ${slideNumber} of ${this.totalSlides}
                    </div>
                    <div class="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                        <p class="text-sm text-gray-600 dark:text-gray-400">
                            Content for this slide is loading...
                        </p>
                    </div>
                </div>
            </div>
        `;
    }
    
    /**
     * Get fallback content when module loading fails
     * @param {number} slideNumber - The slide number
     * @returns {Object} - Fallback content object
     */
    getFallbackContent(slideNumber) {
        return {
            slideNumber,
            html: this.getDefaultHTML(slideNumber),
            jsModule: null,
            cssPath: null,
            loaded: false
        };
    }
    
    /**
     * Render fallback content in case of errors
     * @param {number} slideNumber - The slide number
     * @param {HTMLElement} targetContainer - The container to render in
     */
    renderFallbackContent(slideNumber, targetContainer) {
        const fallbackContent = this.getFallbackContent(slideNumber);
        this.renderSlideContent(fallbackContent, targetContainer);
    }
    
    /**
     * Get slide metadata
     * @param {number} slideNumber - The slide number
     * @returns {Object} - Slide metadata
     */
    getSlideData(slideNumber) {
        const slideDataMap = {
            1: { title: "QR Code Access", icon: "📱", description: "Scan to join the presentation", color: "blue" },
            2: { title: "What is Flipped Learning?", icon: "🔄", description: "Understanding the core concepts", color: "green" },
            3: { title: "Benefits Overview", icon: "📈", description: "Why flip your classroom?", color: "purple" },
            4: { title: "Implementation Planning", icon: "📋", description: "Step-by-step implementation guide", color: "orange" },
            5: { title: "Content Creation", icon: "🎬", description: "Creating engaging video content", color: "red" },
            6: { title: "Technology Tools", icon: "💻", description: "Essential tools and platforms", color: "teal" },
            7: { title: "AI in Education", icon: "🤖", description: "Leveraging AI for better learning", color: "indigo" },
            8: { title: "Video Generation", icon: "🎥", description: "AI-powered content creation", color: "pink" },
            9: { title: "Interactive Elements", icon: "🎯", description: "Engaging student interactions", color: "yellow" },
            10: { title: "Assessment Strategies", icon: "📊", description: "Evaluating flipped learning", color: "cyan" },
            11: { title: "Student Feedback", icon: "💬", description: "Gathering and using feedback", color: "lime" },
            12: { title: "Continuous Improvement", icon: "🔧", description: "Refining your approach", color: "amber" },
            13: { title: "Community Building", icon: "👥", description: "Creating learning communities", color: "emerald" },
            14: { title: "Future Trends", icon: "🚀", description: "What's next in flipped learning", color: "violet" },
            15: { title: "Workshop Conclusion", icon: "✅", description: "Key takeaways and next steps", color: "rose" }
        };
        
        return slideDataMap[slideNumber] || { 
            title: `Slide ${slideNumber}`, 
            icon: "📄", 
            description: "Content loading...", 
            color: "gray" 
        };
    }
    
    /**
     * Get information about loaded modules
     * @returns {Object} - Module loading statistics
     */
    getModuleStats() {
        return {
            totalSlides: this.totalSlides,
            loadedModules: Array.from(this.loadedModules),
            loadedCount: this.loadedModules.size,
            currentSlide: this.currentSlide
        };
    }
}

// Global instance
window.slideModuleLoader = new SlideModuleLoader();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SlideModuleLoader;
}
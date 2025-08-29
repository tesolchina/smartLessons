// Enhanced Content Loader Module
class ContentLoader {
    constructor() {
        this.cache = new Map();
        this.loadingQueue = new Set();
    }

    async loadContent(url) {
        if (this.loadingQueue.has(url)) {
            return; // Already loading
        }

        this.loadingQueue.add(url);
        this.toggleLoading(true);
        
        const section = this.getSectionFromUrl(url);
        
        try {
            let content;
            
            // Check cache first
            if (this.cache.has(url)) {
                content = this.cache.get(url);
                console.log(`📄 Loaded ${section} from cache`);
            } else {
                // Try to fetch the actual file
                console.log(`🌐 Fetching ${url}...`);
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                content = await response.text();
                this.cache.set(url, content);
                console.log(`✅ Fetched and cached ${section} content`);
            }
            
            // Clear the content area
            const contentArea = document.getElementById('contentArea');
            contentArea.innerHTML = '';
            
            // Create a temporary container to parse the HTML
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = content;
            
            // Extract and move body content (skip head)
            const bodyContent = tempDiv.querySelector('body');
            if (bodyContent) {
                // Move all body content to content area
                while (bodyContent.firstChild) {
                    contentArea.appendChild(bodyContent.firstChild);
                }
            } else {
                // If no body tag, just use all content
                while (tempDiv.firstChild) {
                    contentArea.appendChild(tempDiv.firstChild);
                }
            }
            
            // Execute any inline scripts
            this.executeScripts(contentArea);
            
            // Update state
            if (window.stateManager) {
                window.stateManager.updateSection(section, {
                    lastAccessed: new Date().toISOString()
                });
            }
            
            // Start timer
            if (window.timerManager) {
                window.timerManager.startTimer(section);
            }
            
            // Show success notification
            if (window.notificationManager) {
                window.notificationManager.show(`Loaded ${section} content successfully!`, 'success');
            }
            
            console.log(`🎉 Successfully loaded ${section} content`);
            
        } catch (error) {
            console.error('❌ Error loading content:', error);
            
            // Provide fallback content
            const fallbackContent = this.createFallbackContent(section);
            document.getElementById('contentArea').innerHTML = fallbackContent;
            
            if (window.notificationManager) {
                window.notificationManager.show(`Loaded demo content for ${section}`, 'warning');
            }
        } finally {
            this.loadingQueue.delete(url);
            this.toggleLoading(false);
        }
    }

    executeScripts(container) {
        // Find all script tags in the loaded content
        const scripts = container.querySelectorAll('script');
        
        scripts.forEach(oldScript => {
            // Create a new script element
            const newScript = document.createElement('script');
            
            // Copy attributes
            Array.from(oldScript.attributes).forEach(attr => {
                newScript.setAttribute(attr.name, attr.value);
            });
            
            // Copy script content
            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
            
            // Replace old script with new one to trigger execution
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
        
        console.log(`⚡ Executed ${scripts.length} scripts for loaded content`);
    }

    getSectionFromUrl(url) {
        const filename = url.split('/').pop().split('.')[0];
        if (filename.toLowerCase().includes('lecture')) return 'lecture';
        if (filename.toLowerCase().includes('practice')) return 'practice';
        if (filename.toLowerCase().includes('reflect')) return 'reflect';
        return 'lecture';
    }

    createFallbackContent(section) {
        const contents = {
            lecture: `
                <div class="space-y-6">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-white">📚 Interactive Lecture</h2>
                    <div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg border border-blue-200 dark:border-blue-700">
                        <h3 class="text-lg font-semibold mb-4 text-blue-900 dark:text-blue-100">Demo Content</h3>
                        <p class="mb-4 text-blue-800 dark:text-blue-200">This is placeholder content for the interactive lecture section. In your actual implementation, this would contain:</p>
                        <ul class="list-disc list-inside space-y-2 text-blue-700 dark:text-blue-300">
                            <li>Video lectures with interactive elements</li>
                            <li>Embedded quizzes and knowledge checks</li>
                            <li>Downloadable resources and materials</li>
                            <li>Progress tracking and bookmarking</li>
                        </ul>
                        <button onclick="window.updateSectionProgress('lecture', 100)" 
                                class="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                            Complete Section
                        </button>
                    </div>
                </div>
            `,
            practice: `
                <div class="space-y-6">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-white">💬 Practice & Discussion</h2>
                    <div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg border border-green-200 dark:border-green-700">
                        <h3 class="text-lg font-semibold mb-4 text-green-900 dark:text-green-100">Demo Content</h3>
                        <p class="mb-4 text-green-800 dark:text-green-200">This is placeholder content for the practice and discussion section. Features would include:</p>
                        <ul class="list-disc list-inside space-y-2 text-green-700 dark:text-green-300">
                            <li>Interactive exercises and simulations</li>
                            <li>Discussion forums and peer collaboration</li>
                            <li>Case studies and real-world applications</li>
                            <li>Peer review and feedback systems</li>
                        </ul>
                        <button onclick="window.updateSectionProgress('practice', 100)" 
                                class="mt-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors">
                            Complete Section
                        </button>
                    </div>
                </div>
            `,
            reflect: `
                <div class="space-y-6">
                    <h2 class="text-2xl font-bold text-gray-900 dark:text-white">🎯 Reflect & Assess</h2>
                    <div class="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-lg border border-purple-200 dark:border-purple-700">
                        <h3 class="text-lg font-semibold mb-4 text-purple-900 dark:text-purple-100">Demo Content</h3>
                        <p class="mb-4 text-purple-800 dark:text-purple-200">This is placeholder content for the reflection and assessment section. Components include:</p>
                        <ul class="list-disc list-inside space-y-2 text-purple-700 dark:text-purple-300">
                            <li>Self-reflection exercises and journaling</li>
                            <li>Formative and summative assessments</li>
                            <li>Portfolio creation and showcasing</li>
                            <li>Goal setting and progress evaluation</li>
                        </ul>
                        <button onclick="window.updateSectionProgress('reflect', 100)" 
                                class="mt-4 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
                            Complete Section
                        </button>
                    </div>
                </div>
            `
        };
        
        return contents[section] || contents.lecture;
    }

    toggleLoading(show) {
        const loader = document.getElementById('loadingIndicator');
        if (loader) {
            loader.style.transform = show ? 'scaleX(1)' : 'scaleX(0)';
        }
    }

    clearCache() {
        this.cache.clear();
        console.log('🗑️ Content cache cleared');
    }

    preloadContent(urls) {
        console.log('🚀 Preloading content...');
        urls.forEach(async (url) => {
            try {
                const response = await fetch(url);
                if (response.ok) {
                    const content = await response.text();
                    this.cache.set(url, content);
                    console.log(`✅ Preloaded: ${url}`);
                }
            } catch (error) {
                console.warn(`⚠️ Failed to preload ${url}:`, error);
            }
        });
    }
}
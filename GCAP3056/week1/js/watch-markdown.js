// Watch-markdown functionality for GCAP3056 interactive content
// This script enables dynamic loading of markdown content into interactive HTML structures

class MarkdownContentLoader {
    constructor() {
        this.contentCache = new Map();
        this.watchInterval = 5000; // Check for changes every 5 seconds
        this.isWatching = false;
    }

    // Enhanced markdown parser for interactive elements
    parseMarkdown(text) {
        let html = text;
        
        // Headers with special handling for sections
        html = html.replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold text-primary mb-4">$1</h1>');
        html = html.replace(/^## (.*$)/gim, '<h2 class="text-xl font-semibold text-gray-800 mb-3">$1</h2>');
        html = html.replace(/^### (.*$)/gim, '<h3 class="text-lg font-medium text-gray-700 mb-2">$1</h3>');
        
        // Bold and italic text
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Links
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="text-primary hover:underline">$1</a>');
        
        // Lists
        html = html.replace(/^\* (.*$)/gim, '<li class="mb-1">$1</li>');
        html = html.replace(/^- (.*$)/gim, '<li class="mb-1">$1</li>');
        
        // Wrap consecutive list items in ul tags
        html = html.replace(/(<li.*?<\/li>\s*)+/gs, function(match) {
            return '<ul class="list-disc list-inside mb-4 space-y-1">' + match + '</ul>';
        });
        
        // Parse interactive elements
        html = this.parseInteractiveElements(html);
        
        // Paragraphs
        html = html.replace(/\n\n+/g, '</p><p class="mb-4">');
        html = '<p class="mb-4">' + html + '</p>';
        
        // Clean up structure
        html = html.replace(/<p class="mb-4"><\/p>/g, '');
        html = html.replace(/<p class="mb-4">(<h[1-6])/g, '$1');
        html = html.replace(/(<\/h[1-6]>)<\/p>/g, '$1');
        html = html.replace(/<p class="mb-4">(<ul>)/g, '$1');
        html = html.replace(/(<\/ul>)<\/p>/g, '$1');
        html = html.replace(/<p class="mb-4">(<div)/g, '$1');
        html = html.replace(/(<\/div>)<\/p>/g, '$1');
        
        return html;
    }

    // Parse interactive markdown elements into HTML
    parseInteractiveElements(html) {
        // Multiple Choice Questions
        html = html.replace(/### MC Question (\d+)\nquestion: (.*?)\noptions:\n((?:- .*?\|.*?\n)*)/gims, (match, num, question, options) => {
            const optionLines = options.trim().split('\n');
            const optionsHtml = optionLines.map((line, index) => {
                const [text, isCorrect] = line.replace(/^- /, '').split(' | ');
                const letter = String.fromCharCode(65 + index);
                return `<button class="mc-option w-full text-left p-3 rounded border hover:bg-gray-50 mb-2" data-correct="${isCorrect}" data-question="${num}">
                    ${letter}. ${text}
                </button>`;
            }).join('');
            
            return `<div class="mc-question mb-6" data-question="${num}">
                <h4 class="font-medium mb-3">${question}</h4>
                <div class="mc-options">${optionsHtml}</div>
                <div class="mc-feedback hidden mt-3 p-3 rounded"></div>
            </div>`;
        });

        // True/False Questions
        html = html.replace(/### TF Question (\d+)\nquestion: (.*?)\noptions:\n((?:- .*?\|.*?\n)*)/gims, (match, num, question, options) => {
            const optionLines = options.trim().split('\n');
            const optionsHtml = optionLines.map((line) => {
                const [text, isCorrect] = line.replace(/^- /, '').split(' | ');
                return `<button class="tf-option px-6 py-2 rounded border hover:bg-gray-50 mr-3" data-correct="${isCorrect}" data-question="${num}">
                    ${text}
                </button>`;
            }).join('');
            
            return `<div class="tf-question mb-6" data-question="${num}">
                <h4 class="font-medium mb-3">${question}</h4>
                <div class="tf-options">${optionsHtml}</div>
                <div class="tf-feedback hidden mt-3 p-3 rounded"></div>
            </div>`;
        });

        // Fill in the Blank
        html = html.replace(/### Fill in the Blank\nquestion: (.*?)\nvalid_answers: (.*?)\n/gims, (match, question, answers) => {
            return `<div class="fill-blank mb-6">
                <h4 class="font-medium mb-3">${question}</h4>
                <input type="text" class="fill-input w-full p-2 border rounded" data-answers="${answers}" placeholder="Type your answer here...">
                <button class="check-fill bg-primary text-white px-4 py-2 rounded mt-2">Check Answer</button>
                <div class="fill-feedback hidden mt-3 p-3 rounded"></div>
            </div>`;
        });

        // Text Areas
        html = html.replace(/question: (.*?)\ntype: textarea\nplaceholder: (.*?)\nmin_length: (\d+)/gims, (match, question, placeholder, minLength) => {
            return `<div class="textarea-question mb-6">
                <h4 class="font-medium mb-3">${question}</h4>
                <textarea class="response-textarea w-full p-3 border rounded h-32" placeholder="${placeholder}" data-min-length="${minLength}"></textarea>
                <button class="submit-response bg-primary text-white px-4 py-2 rounded mt-2">Submit Response</button>
                <div class="textarea-feedback hidden mt-3 p-3 rounded"></div>
            </div>`;
        });

        // Checkbox Questions
        html = html.replace(/### Checkbox Question\nquestion: (.*?)\noptions:\n((?:- .*?\|.*?\n)*)/gims, (match, question, options) => {
            const optionLines = options.trim().split('\n');
            const optionsHtml = optionLines.map((line, index) => {
                const [text, isCorrect] = line.replace(/^- /, '').split(' | ');
                return `<label class="flex items-center mb-2">
                    <input type="checkbox" class="mr-2" data-correct="${isCorrect}">
                    <span>${text}</span>
                </label>`;
            }).join('');
            
            return `<div class="checkbox-question mb-6">
                <h4 class="font-medium mb-3">${question}</h4>
                <div class="checkbox-options">${optionsHtml}</div>
                <button class="check-checkboxes bg-primary text-white px-4 py-2 rounded mt-2">Check Answers</button>
                <div class="checkbox-feedback hidden mt-3 p-3 rounded"></div>
            </div>`;
        });

        // Video embeds
        html = html.replace(/video_url: (.*?)$/gim, (match, url) => {
            return `<div class="video-container mb-6">
                <iframe src="${url}" width="100%" height="315" frameborder="0" allowfullscreen class="rounded"></iframe>
            </div>`;
        });

        // Toggle sections
        html = html.replace(/toggle_title: (.*?)\ncontent: (.*?)$/gims, (match, title, content) => {
            return `<div class="toggle-section mb-6">
                <button class="toggle-btn w-full text-left p-3 border rounded hover:bg-gray-50 font-medium">
                    ${title} <span class="float-right">▼</span>
                </button>
                <div class="toggle-content hidden mt-2 p-3 border-l-4 border-primary bg-gray-50 rounded">
                    ${content}
                </div>
            </div>`;
        });

        return html;
    }

    // Load markdown content from file
    async loadMarkdownContent(filename, containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with ID '${containerId}' not found`);
            return;
        }

        try {
            container.innerHTML = '<div class="loading">Loading content...</div>';
            
            const response = await fetch(`../content/${filename}`);
            if (!response.ok) {
                throw new Error(`Failed to load ${filename}: ${response.status}`);
            }
            
            const markdownText = await response.text();
            const htmlContent = this.parseMarkdown(markdownText);
            
            container.innerHTML = htmlContent;
            this.contentCache.set(filename, markdownText);
            
            // Initialize interactive elements
            this.initializeInteractiveElements(container);
            
            console.log(`Loaded content from ${filename}`);
        } catch (error) {
            console.error(`Error loading ${filename}:`, error);
            container.innerHTML = `<div class="error text-red-600 p-4 border border-red-300 rounded">
                Error loading content from ${filename}. Please check if the file exists.
            </div>`;
        }
    }

    // Initialize interactive elements after content is loaded
    initializeInteractiveElements(container) {
        // Multiple Choice Questions
        container.querySelectorAll('.mc-option').forEach(button => {
            button.addEventListener('click', this.handleMCQuestion.bind(this));
        });

        // True/False Questions
        container.querySelectorAll('.tf-option').forEach(button => {
            button.addEventListener('click', this.handleTFQuestion.bind(this));
        });

        // Fill in the Blank
        container.querySelectorAll('.check-fill').forEach(button => {
            button.addEventListener('click', this.handleFillBlank.bind(this));
        });

        // Text Areas
        container.querySelectorAll('.submit-response').forEach(button => {
            button.addEventListener('click', this.handleTextArea.bind(this));
        });

        // Checkbox Questions
        container.querySelectorAll('.check-checkboxes').forEach(button => {
            button.addEventListener('click', this.handleCheckboxes.bind(this));
        });

        // Toggle Sections
        container.querySelectorAll('.toggle-btn').forEach(button => {
            button.addEventListener('click', this.handleToggle.bind(this));
        });
    }

    // Event handlers for interactive elements
    handleMCQuestion(event) {
        const button = event.target;
        const questionDiv = button.closest('.mc-question');
        const isCorrect = button.dataset.correct === 'true';
        const feedback = questionDiv.querySelector('.mc-feedback');
        
        // Remove previous selections
        questionDiv.querySelectorAll('.mc-option').forEach(opt => {
            opt.classList.remove('bg-green-100', 'bg-red-100', 'border-green-500', 'border-red-500');
        });
        
        // Show feedback
        if (isCorrect) {
            button.classList.add('bg-green-100', 'border-green-500');
            feedback.innerHTML = '✅ Correct! Great job!';
            feedback.className = 'mc-feedback mt-3 p-3 rounded bg-green-100 text-green-800';
        } else {
            button.classList.add('bg-red-100', 'border-red-500');
            feedback.innerHTML = '❌ Not quite right. Try again!';
            feedback.className = 'mc-feedback mt-3 p-3 rounded bg-red-100 text-red-800';
        }
        
        feedback.classList.remove('hidden');
    }

    handleTFQuestion(event) {
        const button = event.target;
        const questionDiv = button.closest('.tf-question');
        const isCorrect = button.dataset.correct === 'true';
        const feedback = questionDiv.querySelector('.tf-feedback');
        
        // Remove previous selections
        questionDiv.querySelectorAll('.tf-option').forEach(opt => {
            opt.classList.remove('bg-green-100', 'bg-red-100');
        });
        
        // Show feedback
        if (isCorrect) {
            button.classList.add('bg-green-100');
            feedback.innerHTML = '✅ Correct!';
            feedback.className = 'tf-feedback mt-3 p-3 rounded bg-green-100 text-green-800';
        } else {
            button.classList.add('bg-red-100');
            feedback.innerHTML = '❌ Try again!';
            feedback.className = 'tf-feedback mt-3 p-3 rounded bg-red-100 text-red-800';
        }
        
        feedback.classList.remove('hidden');
    }

    handleFillBlank(event) {
        const button = event.target;
        const questionDiv = button.closest('.fill-blank');
        const input = questionDiv.querySelector('.fill-input');
        const validAnswers = input.dataset.answers.split(',');
        const userAnswer = input.value.toLowerCase().trim();
        const feedback = questionDiv.querySelector('.fill-feedback');
        
        const isCorrect = validAnswers.some(answer => 
            userAnswer.includes(answer.toLowerCase().trim())
        );
        
        if (isCorrect) {
            feedback.innerHTML = '✅ Correct! Well done!';
            feedback.className = 'fill-feedback mt-3 p-3 rounded bg-green-100 text-green-800';
            input.classList.add('border-green-500');
        } else {
            feedback.innerHTML = '❌ Not quite. Think about the key concept we discussed.';
            feedback.className = 'fill-feedback mt-3 p-3 rounded bg-red-100 text-red-800';
            input.classList.add('border-red-500');
        }
        
        feedback.classList.remove('hidden');
    }

    handleTextArea(event) {
        const button = event.target;
        const questionDiv = button.closest('.textarea-question');
        const textarea = questionDiv.querySelector('.response-textarea');
        const minLength = parseInt(textarea.dataset.minLength);
        const feedback = questionDiv.querySelector('.textarea-feedback');
        
        if (textarea.value.length >= minLength) {
            feedback.innerHTML = '✅ Thank you for your thoughtful response!';
            feedback.className = 'textarea-feedback mt-3 p-3 rounded bg-green-100 text-green-800';
            // Store response in localStorage
            localStorage.setItem(`response_${Date.now()}`, textarea.value);
        } else {
            feedback.innerHTML = `❌ Please provide a more detailed response (at least ${minLength} characters).`;
            feedback.className = 'textarea-feedback mt-3 p-3 rounded bg-red-100 text-red-800';
        }
        
        feedback.classList.remove('hidden');
    }

    handleCheckboxes(event) {
        const button = event.target;
        const questionDiv = button.closest('.checkbox-question');
        const checkboxes = questionDiv.querySelectorAll('input[type="checkbox"]');
        const feedback = questionDiv.querySelector('.checkbox-feedback');
        
        let allCorrect = true;
        checkboxes.forEach(checkbox => {
            const shouldBeChecked = checkbox.dataset.correct === 'true';
            const isChecked = checkbox.checked;
            if (shouldBeChecked !== isChecked) {
                allCorrect = false;
            }
        });
        
        if (allCorrect) {
            feedback.innerHTML = '✅ Perfect! You got all the answers right!';
            feedback.className = 'checkbox-feedback mt-3 p-3 rounded bg-green-100 text-green-800';
        } else {
            feedback.innerHTML = '❌ Some selections need adjustment. Review and try again!';
            feedback.className = 'checkbox-feedback mt-3 p-3 rounded bg-red-100 text-red-800';
        }
        
        feedback.classList.remove('hidden');
    }

    handleToggle(event) {
        const button = event.target;
        const content = button.nextElementSibling;
        const arrow = button.querySelector('span');
        
        if (content.classList.contains('hidden')) {
            content.classList.remove('hidden');
            arrow.textContent = '▲';
        } else {
            content.classList.add('hidden');
            arrow.textContent = '▼';
        }
    }

    // Watch for file changes (for development)
    startWatching(filenames, containerIds) {
        if (this.isWatching) return;
        
        this.isWatching = true;
        setInterval(async () => {
            for (let i = 0; i < filenames.length; i++) {
                const filename = filenames[i];
                const containerId = containerIds[i];
                
                try {
                    const response = await fetch(`../content/${filename}`);
                    if (response.ok) {
                        const markdownText = await response.text();
                        const cachedContent = this.contentCache.get(filename);
                        
                        if (cachedContent !== markdownText) {
                            console.log(`Content changed: ${filename}`);
                            this.loadMarkdownContent(filename, containerId);
                        }
                    }
                } catch (error) {
                    // Silently ignore errors during watching
                }
            }
        }, this.watchInterval);
    }
}

// Global instance
window.markdownLoader = new MarkdownContentLoader();

// Helper function for easy use
window.loadContent = (filename, containerId) => {
    window.markdownLoader.loadMarkdownContent(filename, containerId);
};

// Helper function to start watching multiple files
window.startContentWatch = (filenames, containerIds) => {
    window.markdownLoader.startWatching(filenames, containerIds);
};

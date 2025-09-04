// Watch-markdown functionality for GCAP3056 interactive content (Student Version)
// This script enables dynamic loading of markdown content with answers hidden from students

class MarkdownContentLoader {
    constructor(hideAnswers = true) {
        this.contentCache = new Map();
        this.watchInterval = 5000; // Check for changes every 5 seconds
        this.isWatching = false;
        this.hideAnswers = hideAnswers; // Hide correct answers from students
    }

    // Enhanced markdown parser for interactive elements (student version)
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

    // Parse interactive markdown elements into HTML (student version - answers hidden)
    parseInteractiveElements(html) {
        // Header section parsing
        html = html.replace(/## Header\s*\n([\s\S]*?)(?=\n##|\n###|$)/gim, (match, content) => {
            let title = '';
            let subtitle = '';
            
            const titleMatch = content.match(/title:\s*(.+)/);
            const subtitleMatch = content.match(/subtitle:\s*(.+)/);
            
            if (titleMatch) title = titleMatch[1].trim();
            if (subtitleMatch) subtitle = subtitleMatch[1].trim();
            
            return `<div class="header-section mb-8 p-6 bg-gradient-to-r from-primary to-primary-light text-white rounded-xl">
                <h1 class="text-3xl font-bold mb-3">${title}</h1>
                <p class="text-lg opacity-90">${subtitle}</p>
            </div>`;
        });

        // Section content parsing - handle multiple content patterns
        html = html.replace(/## Section (\d+):\s*(.+?)\n\ncontent:\s*(.+?)(?=\n###|\n## |\n$)/gims, (match, num, title, content) => {
            return `<div class="content-section mb-8 p-6 bg-gray-50 dark:bg-gray-800 rounded-xl border">
                <h2 class="text-xl font-semibold text-primary mb-4">${num}. ${title}</h2>
                <div class="text-gray-700 dark:text-gray-300 mb-4 prose prose-sm max-w-none">${content}</div>
            </div>`;
        });

        // Also handle content2 and other content patterns
        html = html.replace(/content2:\s*(.+?)(?=\n###|\n## |\n$)/gims, (match, content) => {
            return `<div class="content-section mb-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg border border-blue-200 dark:border-blue-700">
                <div class="text-blue-800 dark:text-blue-200 prose prose-sm max-w-none">${content}</div>
            </div>`;
        });

        // Multiple Choice Questions - Hide correct answers and format properly
        html = html.replace(/### MC Question (\d+)\s*\n\nquestion:\s*(.+?)\noptions:\s*\n\n((?:- .+?\n)*)/gims, (match, num, question, options) => {
            const optionLines = options.trim().split('\n').filter(line => line.trim().startsWith('-'));
            const optionsHtml = optionLines.map((line, index) => {
                // Remove the answer indicator (| true/false) from display
                const text = line.replace(/^- /, '').replace(/\s*\|\s*(true|false)\s*$/, '').trim();
                const letter = String.fromCharCode(65 + index);
                return `<button class="mc-option w-full text-left p-3 rounded border border-gray-300 hover:border-primary hover:bg-blue-50 mb-2 transition-all" data-question="${num}" data-option="${index}">
                    <span class="font-medium text-primary">${letter}.</span> ${text}
                </button>`;
            }).join('');
            
            return `<div class="mc-question mb-6 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700" data-question="${num}">
                <h3 class="text-lg font-medium text-gray-800 dark:text-gray-200 mb-4">${question}</h3>
                <div class="mc-options space-y-2">${optionsHtml}</div>
                <div class="mc-feedback hidden mt-4 p-3 rounded-lg"></div>
            </div>`;
        });

        // True/False Questions - Hide correct answers and format properly  
        html = html.replace(/### TF Question (\d+)\s*\n\nquestion:\s*(.+?)\noptions:\s*\n\n((?:- .+?\n)*)/gims, (match, num, question, options) => {
            const optionLines = options.trim().split('\n').filter(line => line.trim().startsWith('-'));
            const optionsHtml = optionLines.map((line, index) => {
                // Remove the answer indicator from display
                const text = line.replace(/^- /, '').replace(/\s*\|\s*(true|false)\s*$/, '').trim();
                return `<button class="tf-option px-6 py-3 rounded-lg border border-gray-300 hover:border-primary hover:bg-blue-50 mr-3 transition-all font-medium" data-question="${num}" data-option="${index}">
                    ${text}
                </button>`;
            }).join('');
            
            return `<div class="tf-question mb-6 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700" data-question="${num}">
                <h3 class="text-lg font-medium text-gray-800 dark:text-gray-200 mb-4">${question}</h3>
                <div class="tf-options flex gap-3">${optionsHtml}</div>
                <div class="tf-feedback hidden mt-4 p-3 rounded-lg"></div>
            </div>`;
        });

        // Test Questions - Handle dynamically added questions with options
        html = html.replace(/### TEST QUESTION - LIVE UPDATE\s*\n\nquestion:\s*(.+?)\noptions:\s*\n\n((?:- .+?\n)*)/gims, (match, question, options) => {
            const optionLines = options.trim().split('\n').filter(line => line.trim().startsWith('-'));
            const optionsHtml = optionLines.map((line, index) => {
                // Remove the answer indicator from display
                const text = line.replace(/^- /, '').replace(/\s*\|\s*(true|false)\s*$/, '').trim();
                return `<button class="test-option w-full text-left p-3 rounded border border-yellow-300 hover:border-yellow-500 hover:bg-yellow-100 mb-2 transition-all" data-option="${index}">
                    ${text}
                </button>`;
            }).join('');
            
            return `<div class="test-question mb-6 p-4 bg-yellow-50 dark:bg-yellow-900 rounded-lg border border-yellow-200 dark:border-yellow-700">
                <h3 class="text-lg font-medium text-yellow-800 dark:text-yellow-200 mb-4">🧪 Live Update Test</h3>
                <p class="text-yellow-700 dark:text-yellow-300 mb-4">${question}</p>
                <div class="test-options space-y-2">${optionsHtml}</div>
                <div class="mt-3 text-sm text-yellow-600 dark:text-yellow-400">This question was dynamically loaded from the markdown file!</div>
            </div>`;
        });

        // Fill in the Blank
        html = html.replace(/### Fill in the Blank\s*\nquestion:\s*(.+?)\nvalid_answers:\s*(.+?)\n/gims, (match, question, answers) => {
            return `<div class="fill-blank mb-6 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                <h3 class="text-lg font-medium text-gray-800 dark:text-gray-200 mb-4">${question}</h3>
                <input type="text" class="fill-input w-full p-3 border border-gray-300 rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20" placeholder="Type your answer here...">
                <button class="check-fill bg-primary hover:bg-primary-dark text-white px-6 py-2 rounded-lg mt-3 transition-colors">Submit Answer</button>
                <div class="fill-feedback hidden mt-4 p-3 rounded-lg"></div>
            </div>`;
        });

        // Text Areas
        html = html.replace(/question:\s*(.+?)\ntype:\s*textarea\nplaceholder:\s*(.+?)\nmin_length:\s*(\d+)/gims, (match, question, placeholder, minLength) => {
            return `<div class="textarea-question mb-6 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                <h3 class="text-lg font-medium text-gray-800 dark:text-gray-200 mb-4">${question}</h3>
                <textarea class="response-textarea w-full p-3 border border-gray-300 rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 h-32 resize-y" placeholder="${placeholder}" data-min-length="${minLength}"></textarea>
                <button class="submit-response bg-primary hover:bg-primary-dark text-white px-6 py-2 rounded-lg mt-3 transition-colors">Submit Response</button>
                <div class="textarea-feedback hidden mt-4 p-3 rounded-lg"></div>
            </div>`;
        });

        // Checkbox Questions - Hide correct answers
        html = html.replace(/### Checkbox Question\s*\nquestion:\s*(.+?)\noptions:\s*\n((?:- .+?\n)*)/gims, (match, question, options) => {
            const optionLines = options.trim().split('\n');
            const optionsHtml = optionLines.map((line, index) => {
                // Remove the answer indicator from display
                const text = line.replace(/^- /, '').replace(/\s*\|\s*(true|false)\s*$/, '').trim();
                return `<label class="flex items-center p-3 rounded-lg border border-gray-200 hover:bg-gray-50 cursor-pointer transition-colors mb-2">
                    <input type="checkbox" class="mr-3 w-4 h-4 text-primary border-gray-300 rounded focus:ring-primary">
                    <span class="text-gray-700 dark:text-gray-300">${text}</span>
                </label>`;
            }).join('');
            
            return `<div class="checkbox-question mb-6 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                <h3 class="text-lg font-medium text-gray-800 dark:text-gray-200 mb-4">${question}</h3>
                <div class="checkbox-options space-y-2">${optionsHtml}</div>
                <button class="check-checkboxes bg-primary hover:bg-primary-dark text-white px-6 py-2 rounded-lg mt-4 transition-colors">Submit Answers</button>
                <div class="checkbox-feedback hidden mt-4 p-3 rounded-lg"></div>
            </div>`;
        });

        // Key Points and bullet lists
        html = html.replace(/### Key Points\s*\n\n((?:- .+?\n)*)/gims, (match, points) => {
            const pointLines = points.trim().split('\n').filter(line => line.trim().startsWith('-'));
            const pointsHtml = pointLines.map(line => {
                const text = line.replace(/^- /, '').trim();
                return `<li class="text-gray-700 dark:text-gray-300 mb-2">${text}</li>`;
            }).join('');
            
            return `<div class="key-points mb-6 p-4 bg-green-50 dark:bg-green-900 rounded-lg border border-green-200 dark:border-green-700">
                <h3 class="text-lg font-medium text-green-800 dark:text-green-200 mb-4">📝 Key Points</h3>
                <ul class="list-disc list-inside space-y-1">${pointsHtml}</ul>
            </div>`;
        });

        // Critical Points sections
        html = html.replace(/### Critical Points\s*\n\n((?:- .+?\n)*)/gims, (match, points) => {
            const pointLines = points.trim().split('\n').filter(line => line.trim().startsWith('-'));
            const pointsHtml = pointLines.map(line => {
                const text = line.replace(/^- /, '').trim();
                return `<li class="text-red-700 dark:text-red-300 mb-2">${text}</li>`;
            }).join('');
            
            return `<div class="critical-points mb-6 p-4 bg-red-50 dark:bg-red-900 rounded-lg border border-red-200 dark:border-red-700">
                <h3 class="text-lg font-medium text-red-800 dark:text-red-200 mb-4">⚠️ Critical Points</h3>
                <ul class="list-disc list-inside space-y-1">${pointsHtml}</ul>
            </div>`;
        });

        // Note sections
        html = html.replace(/### Note\s*\n\ncontent:\s*(.+?)(?=\n###|\n## |\n$)/gims, (match, content) => {
            return `<div class="note-section mb-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg border border-blue-200 dark:border-blue-700">
                <h3 class="text-lg font-medium text-blue-800 dark:text-blue-200 mb-3">📌 Note</h3>
                <div class="text-blue-700 dark:text-blue-300 prose prose-sm max-w-none">${content}</div>
            </div>`;
        });

        // Video sections with titles
        html = html.replace(/## Section (\d+):\s*Video Review\s*\n\ntitle:\s*(.+?)\nvideo_url:\s*(.+?)\ncontent:\s*(.+?)(?=\n###|\n## |\n$)/gims, (match, num, title, url, content) => {
            return `<div class="video-section mb-8 p-6 bg-purple-50 dark:bg-purple-900 rounded-xl border border-purple-200 dark:border-purple-700">
                <h2 class="text-xl font-semibold text-purple-800 dark:text-purple-200 mb-4">${num}. ${title}</h2>
                <div class="video-container mb-4">
                    <iframe src="${url}" width="100%" height="315" frameborder="0" allowfullscreen class="rounded-lg shadow-sm"></iframe>
                </div>
                <div class="text-purple-700 dark:text-purple-300 prose prose-sm max-w-none">${content}</div>
            </div>`;
        });

        // Toggle sections
        html = html.replace(/toggle_title:\s*(.+?)\ncontent:\s*(.+?)$/gims, (match, title, content) => {
            return `<div class="toggle-section mb-6 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                <button class="toggle-btn w-full text-left p-4 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 font-medium transition-colors flex items-center justify-between">
                    <span>${title}</span>
                    <span class="toggle-arrow text-primary">▼</span>
                </button>
                <div class="toggle-content hidden p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
                    <div class="prose prose-sm max-w-none text-gray-700 dark:text-gray-300">${content}</div>
                </div>
            </div>`;
        });

        // Clean up any remaining raw markdown formatting
        html = html.replace(/feedback_correct:\s*(.+?)(?=\n|$)/g, '');
        html = html.replace(/feedback_incorrect:\s*(.+?)(?=\n|$)/g, '');
        html = html.replace(/\s*\|\s*(true|false)\s*(?=\n|$)/g, '');

        return html;
    }

    // Load markdown content from file
    async loadMarkdownContent(filename, containerId) {
        console.log(`Loading ${filename} into container ${containerId}`);
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with ID '${containerId}' not found`);
            return;
        }

        try {
            container.innerHTML = '<div class="loading text-center py-8">Loading content...</div>';
            
            // Add cache-busting parameter to ensure fresh content
            const cacheBuster = new Date().getTime();
            const response = await fetch(`content/${filename}?v=${cacheBuster}`);
            if (!response.ok) {
                throw new Error(`Failed to load ${filename}: ${response.status}`);
            }
            
            const markdownText = await response.text();
            console.log('Raw markdown loaded:', markdownText.substring(0, 200) + '...');
            
            const htmlContent = this.parseMarkdown(markdownText);
            console.log('Parsed HTML:', htmlContent.substring(0, 300) + '...');
            
            container.innerHTML = htmlContent;
            this.contentCache.set(filename, markdownText);
            
            // Initialize interactive elements after content is loaded
            setTimeout(() => {
                this.initializeInteractiveElements(container);
            }, 100);
            
            console.log(`Successfully loaded content from ${filename}`);
        } catch (error) {
            console.error(`Error loading ${filename}:`, error);
            container.innerHTML = `<div class="error text-red-600 p-4 border border-red-300 rounded">
                <strong>Error loading content:</strong><br>
                ${error.message}<br>
                <small>Check browser console for details</small>
            </div>`;
        }
    }

    // Initialize interactive elements after content is loaded (student version)
    initializeInteractiveElements(container) {
        console.log('Initializing interactive elements in container:', container.id);
        
        // Multiple Choice Questions (no correct answer checking for students)
        container.querySelectorAll('.mc-option').forEach(button => {
            console.log('Found MC option button:', button);
            button.addEventListener('click', this.handleMCQuestionStudent.bind(this));
        });

        // True/False Questions (no correct answer checking for students)
        container.querySelectorAll('.tf-option').forEach(button => {
            console.log('Found TF option button:', button);
            button.addEventListener('click', this.handleTFQuestionStudent.bind(this));
        });

        // Fill in the Blank (no answer validation for students)
        container.querySelectorAll('.check-fill').forEach(button => {
            button.addEventListener('click', this.handleFillBlankStudent.bind(this));
        });

        // Text Areas
        container.querySelectorAll('.submit-response').forEach(button => {
            button.addEventListener('click', this.handleTextArea.bind(this));
        });

        // Checkbox Questions (no answer checking for students)
        container.querySelectorAll('.check-checkboxes').forEach(button => {
            button.addEventListener('click', this.handleCheckboxesStudent.bind(this));
        });

        // Toggle Sections
        container.querySelectorAll('.toggle-btn').forEach(button => {
            button.addEventListener('click', this.handleToggle.bind(this));
        });

        // Test Question Options (for live update testing)
        container.querySelectorAll('.test-option').forEach(button => {
            console.log('Found test option button:', button);
            button.addEventListener('click', this.handleTestOption.bind(this));
        });
        
        console.log('Interactive elements initialized successfully');
    }

    // Student version event handlers (improved feedback and formatting)
    handleMCQuestionStudent(event) {
        const button = event.target;
        const questionDiv = button.closest('.mc-question');
        const feedback = questionDiv.querySelector('.mc-feedback');
        
        // Remove previous selections and reset styling
        questionDiv.querySelectorAll('.mc-option').forEach(opt => {
            opt.classList.remove('border-primary', 'bg-blue-50', 'border-green-500', 'bg-green-50');
            opt.classList.add('border-gray-300');
        });
        
        // Highlight current selection with primary color
        button.classList.remove('border-gray-300');
        button.classList.add('border-primary', 'bg-blue-50');
        
        // Show improved feedback
        feedback.innerHTML = `<span class="text-blue-800">✓ Answer recorded! Your selection: ${button.textContent.trim()}</span>`;
        feedback.className = 'mc-feedback mt-4 p-3 rounded-lg bg-blue-50 border border-blue-200';
        feedback.classList.remove('hidden');
        
        // Store answer
        this.storeStudentAnswer('mc', questionDiv.dataset.question, button.textContent.trim());
    }

    handleTFQuestionStudent(event) {
        const button = event.target;
        const questionDiv = button.closest('.tf-question');
        const feedback = questionDiv.querySelector('.tf-feedback');
        
        // Remove previous selections and reset styling
        questionDiv.querySelectorAll('.tf-option').forEach(opt => {
            opt.classList.remove('border-primary', 'bg-blue-50', 'border-green-500', 'bg-green-50');
            opt.classList.add('border-gray-300');
        });
        
        // Highlight current selection
        button.classList.remove('border-gray-300');
        button.classList.add('border-primary', 'bg-blue-50');
        
        // Show improved feedback
        feedback.innerHTML = `<span class="text-blue-800">✓ Answer recorded! Your selection: ${button.textContent.trim()}</span>`;
        feedback.className = 'tf-feedback mt-4 p-3 rounded-lg bg-blue-50 border border-blue-200';
        feedback.classList.remove('hidden');
        
        // Store answer
        this.storeStudentAnswer('tf', questionDiv.dataset.question, button.textContent.trim());
    }

    handleTestOption(event) {
        const button = event.target;
        const questionDiv = button.closest('.test-question');
        
        // Remove previous selections
        questionDiv.querySelectorAll('.test-option').forEach(opt => {
            opt.classList.remove('border-yellow-500', 'bg-yellow-100');
            opt.classList.add('border-yellow-300');
        });
        
        // Highlight current selection
        button.classList.remove('border-yellow-300');
        button.classList.add('border-yellow-500', 'bg-yellow-100');
        
        // Show special feedback for test questions
        const existingFeedback = questionDiv.querySelector('.test-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }
        
        const feedback = document.createElement('div');
        feedback.className = 'test-feedback mt-4 p-3 rounded-lg bg-yellow-100 border border-yellow-300';
        feedback.innerHTML = `<span class="text-yellow-800">🎉 Test successful! Your selection: "${button.textContent.trim()}" - The live markdown loading is working perfectly!</span>`;
        questionDiv.appendChild(feedback);
        
        // Store answer
        this.storeStudentAnswer('test', 'live-update', button.textContent.trim());
    }

    handleFillBlankStudent(event) {
        const button = event.target;
        const questionDiv = button.closest('.fill-blank');
        const input = questionDiv.querySelector('.fill-input');
        const feedback = questionDiv.querySelector('.fill-feedback');
        const userAnswer = input.value.trim();
        
        if (userAnswer.length > 0) {
            // Show success feedback
            feedback.innerHTML = `<span class="text-green-800">✓ Answer submitted: "${userAnswer}"</span>`;
            feedback.className = 'fill-feedback mt-4 p-3 rounded-lg bg-green-50 border border-green-200';
            
            // Style input as completed
            input.classList.remove('border-gray-300', 'focus:border-primary');
            input.classList.add('border-green-500', 'bg-green-50');
            input.disabled = true;
            
            // Update button
            button.disabled = true;
            button.textContent = 'Submitted';
            button.classList.remove('bg-primary', 'hover:bg-primary-dark');
            button.classList.add('bg-gray-400');
            
            // Store answer
            this.storeStudentAnswer('fill', 'fill-blank', userAnswer);
        } else {
            // Show error feedback
            feedback.innerHTML = '<span class="text-red-800">⚠ Please enter an answer before submitting.</span>';
            feedback.className = 'fill-feedback mt-4 p-3 rounded-lg bg-red-50 border border-red-200';
            
            // Highlight input as requiring attention
            input.classList.remove('border-gray-300');
            input.classList.add('border-red-500');
            input.focus();
        }
        
        feedback.classList.remove('hidden');
    }

    handleTextArea(event) {
        const button = event.target;
        const questionDiv = button.closest('.textarea-question');
        const textarea = questionDiv.querySelector('.response-textarea');
        const minLength = parseInt(textarea.dataset.minLength) || 0;
        const feedback = questionDiv.querySelector('.textarea-feedback');
        const userResponse = textarea.value.trim();
        
        if (userResponse.length >= minLength) {
            // Show success feedback
            feedback.innerHTML = `<span class="text-green-800">✓ Response submitted (${userResponse.length} characters)</span>`;
            feedback.className = 'textarea-feedback mt-4 p-3 rounded-lg bg-green-50 border border-green-200';
            
            // Style textarea as completed
            textarea.classList.remove('border-gray-300', 'focus:border-primary');
            textarea.classList.add('border-green-500', 'bg-green-50');
            textarea.disabled = true;
            
            // Update button
            button.disabled = true;
            button.textContent = 'Submitted';
            button.classList.remove('bg-primary', 'hover:bg-primary-dark');
            button.classList.add('bg-gray-400');
            
            // Store response
            this.storeStudentAnswer('textarea', Date.now(), userResponse);
        } else {
            // Show error feedback
            feedback.innerHTML = `<span class="text-red-800">⚠ Please write at least ${minLength} characters. Current: ${userResponse.length}</span>`;
            feedback.className = 'textarea-feedback mt-4 p-3 rounded-lg bg-red-50 border border-red-200';
            
            // Highlight textarea as requiring attention
            textarea.classList.remove('border-gray-300');
            textarea.classList.add('border-red-500');
            textarea.focus();
        }
        
        feedback.classList.remove('hidden');
    }

    handleCheckboxesStudent(event) {
        const button = event.target;
        const questionDiv = button.closest('.checkbox-question');
        const checkboxes = questionDiv.querySelectorAll('input[type="checkbox"]');
        const feedback = questionDiv.querySelector('.checkbox-feedback');
        
        const selectedAnswers = [];
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                selectedAnswers.push(checkbox.parentElement.textContent.trim());
            }
        });
        
        if (selectedAnswers.length > 0) {
            // Show success feedback
            feedback.innerHTML = `<span class="text-green-800">✓ Answers submitted: ${selectedAnswers.join(', ')}</span>`;
            feedback.className = 'checkbox-feedback mt-4 p-3 rounded-lg bg-green-50 border border-green-200';
            
            // Disable checkboxes and style as completed
            checkboxes.forEach(checkbox => {
                checkbox.disabled = true;
                if (checkbox.checked) {
                    checkbox.parentElement.classList.add('bg-green-50', 'border-green-200');
                } else {
                    checkbox.parentElement.classList.add('opacity-50');
                }
            });
            
            // Update button
            button.disabled = true;
            button.textContent = 'Submitted';
            button.classList.remove('bg-primary', 'hover:bg-primary-dark');
            button.classList.add('bg-gray-400');
            
            // Store answers
            this.storeStudentAnswer('checkbox', questionDiv.dataset.question || 'checkbox', selectedAnswers.join(', '));
        } else {
            // Show error feedback
            feedback.innerHTML = '<span class="text-red-800">⚠ Please select at least one option.</span>';
            feedback.className = 'checkbox-feedback mt-4 p-3 rounded-lg bg-red-50 border border-red-200';
        }
        
        feedback.classList.remove('hidden');
    }

    handleToggle(event) {
        const button = event.target.closest('.toggle-btn');
        const toggleSection = button.closest('.toggle-section');
        const content = toggleSection.querySelector('.toggle-content');
        const arrow = button.querySelector('.toggle-arrow');
        
        if (content.classList.contains('hidden')) {
            content.classList.remove('hidden');
            arrow.textContent = '▲';
            button.classList.add('bg-primary', 'text-white');
            button.classList.remove('bg-gray-50', 'hover:bg-gray-100');
        } else {
            content.classList.add('hidden');
            arrow.textContent = '▼';
            button.classList.remove('bg-primary', 'text-white');
            button.classList.add('bg-gray-50', 'hover:bg-gray-100');
        }
    }

    // Store student answers (for instructor review)
    storeStudentAnswer(type, questionId, answer) {
        const timestamp = new Date().toISOString();
        const studentData = {
            type: type,
            questionId: questionId,
            answer: answer,
            timestamp: timestamp
        };
        
        // Store in localStorage for now (could be sent to server)
        const existingData = JSON.parse(localStorage.getItem('studentAnswers') || '[]');
        existingData.push(studentData);
        localStorage.setItem('studentAnswers', JSON.stringify(existingData));
        
        console.log('Student answer stored:', studentData);
    }

    // Alternative method name for compatibility
    storeUserAnswer(questionId, answer) {
        this.storeStudentAnswer('general', questionId, answer);
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
                    const response = await fetch(`content/${filename}`);
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

// Global instance (student version with answers hidden)
window.markdownLoader = new MarkdownContentLoader(true);

// Helper function for easy use
window.loadMarkdownContent = (filename, containerId) => {
    window.markdownLoader.loadMarkdownContent(filename, containerId);
};

// Helper function to start watching multiple files
window.startContentWatch = (filenames, containerIds) => {
    window.markdownLoader.startWatching(filenames, containerIds);
};

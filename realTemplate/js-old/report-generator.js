// Advanced Report Generator
class ReportGenerator {
    constructor() {
        this.reports = [];
        this.templates = this.initializeTemplates();
    }

    initializeTemplates() {
        return {
            summary: 'summary-template',
            detailed: 'detailed-template',
            interactive: 'interactive-template'
        };
    }

    generateDetailedReport(data) {
        console.log('📊 Generating detailed report...');
        
        const report = this.createReportData(data);
        this.showReportModal(report, 'detailed');
        
        // Store report
        this.reports.push({
            id: `report-${Date.now()}`,
            type: 'detailed',
            data: report,
            generated: new Date().toISOString()
        });
    }

    showInteractiveReport(lectureData) {
        console.log('📋 Showing interactive content report...');
        
        const report = this.createInteractiveReportData(lectureData);
        this.showReportModal(report, 'interactive');
    }

    createReportData(stateData) {
        const sections = stateData.course?.sections || {};
        const overallProgress = stateData.computed?.overallProgress || 0;
        const totalTime = stateData.computed?.totalTimeSpent || 0;
        
        return {
            metadata: {
                generated: new Date().toISOString(),
                studentId: stateData.user?.id || 'anonymous',
                courseId: stateData.course?.id || 'unknown',
                reportType: 'Course Progress Report'
            },
            summary: {
                overallProgress: Math.round(overallProgress),
                totalTimeSpent: this.formatDuration(totalTime),
                sectionsCompleted: Object.values(sections).filter(s => s.completed).length,
                totalSections: Object.keys(sections).length,
                lastActivity: stateData.computed?.lastActivity || 'Unknown'
            },
            sections: Object.entries(sections).map(([id, data]) => ({
                id,
                name: this.getSectionName(id),
                progress: data.progress || 0,
                timeSpent: this.formatDuration(data.timeSpent || 0),
                completed: data.completed || false,
                lastAccessed: data.lastAccessed ? new Date(data.lastAccessed).toLocaleString() : 'Never'
            })),
            interactions: stateData.interactions || [],
            recommendations: this.generateRecommendations(sections, overallProgress)
        };
    }

    createInteractiveReportData(lectureData) {
        const duration = lectureData.timeSpent || (Date.now() - lectureData.startTime);
        
        return {
            metadata: {
                generated: new Date().toISOString(),
                contentType: 'Interactive Lecture',
                subject: lectureData.metadata?.subject || 'Learning Content'
            },
            performance: {
                score: lectureData.score,
                choiceSelected: lectureData.choiceSelected,
                timeSpent: this.formatDuration(duration),
                completed: lectureData.completed || false,
                engagementLevel: lectureData.finalMetrics?.engagementLevel || 'Unknown'
            },
            sectionProgress: lectureData.sectionProgress || {},
            interactions: lectureData.interactions || [],
            insights: this.generateLectureInsights(lectureData)
        };
    }

    showReportModal(reportData, template = 'detailed') {
        let modal = document.getElementById('reportModal');
        if (!modal) {
            modal = this.createReportModal();
        }

        const content = document.getElementById('reportModalContent');
        content.innerHTML = this.generateReportHTML(reportData, template);
        
        modal.style.display = 'flex';
        
        // Add event listeners for modal
        this.setupModalEventListeners(modal, reportData);
    }

    createReportModal() {
        const modal = document.createElement('div');
        modal.id = 'reportModal';
        modal.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4';
        modal.style.display = 'none';
        
        modal.innerHTML = `
            <div class="bg-white dark:bg-gray-800 rounded-lg max-w-6xl w-full max-h-[95vh] overflow-hidden flex flex-col">
                <div class="flex justify-between items-center p-6 border-b dark:border-gray-600">
                    <h3 class="text-xl font-bold text-gray-900 dark:text-white">📊 Learning Analytics Report</h3>
                    <button id="closeReportModal" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <div id="reportModalContent" class="flex-1 overflow-auto p-6">
                    <!-- Report content will be inserted here -->
                </div>
                <div class="border-t dark:border-gray-600 p-6 bg-gray-50 dark:bg-gray-700">
                    <div class="flex justify-between items-center">
                        <div class="text-sm text-gray-600 dark:text-gray-400">
                            <span id="reportTimestamp"></span>
                        </div>
                        <div class="space-x-2">
                            <button id="downloadReportBtn" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors">
                                📥 Download
                            </button>
                            <button id="printReportBtn" class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded transition-colors">
                                🖨️ Print
                            </button>
                            <button id="shareReportBtn" class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded transition-colors">
                                📤 Share
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        return modal;
    }

    generateReportHTML(data, template) {
        switch (template) {
            case 'interactive':
                return this.generateInteractiveReportHTML(data);
            case 'detailed':
                return this.generateDetailedReportHTML(data);
            default:
                return this.generateSummaryReportHTML(data);
        }
    }

    generateInteractiveReportHTML(data) {
        return `
            <div class="space-y-6">
                <!-- Performance Overview -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg text-center">
                        <div class="text-3xl font-bold text-blue-600 dark:text-blue-400">${data.performance.score !== null ? data.performance.score + '%' : 'N/A'}</div>
                        <div class="text-sm text-blue-800 dark:text-blue-300">Quiz Score</div>
                    </div>
                    <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg text-center">
                        <div class="text-3xl font-bold text-green-600 dark:text-green-400">${data.performance.timeSpent}</div>
                        <div class="text-sm text-green-800 dark:text-green-300">Time Spent</div>
                    </div>
                    <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg text-center">
                        <div class="text-3xl font-bold text-purple-600 dark:text-purple-400">${data.performance.completed ? '✅' : '⏳'}</div>
                        <div class="text-sm text-purple-800 dark:text-purple-300">Status</div>
                    </div>
                    <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg text-center">
                        <div class="text-3xl font-bold text-orange-600 dark:text-orange-400">${data.interactions.length}</div>
                        <div class="text-sm text-orange-800 dark:text-orange-300">Interactions</div>
                    </div>
                </div>

                <!-- Section Progress -->
                <div class="bg-white dark:bg-gray-700 rounded-lg p-6">
                    <h4 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">📈 Section Progress</h4>
                    <div class="space-y-4">
                        ${Object.entries(data.sectionProgress).map(([section, progress]) => `
                            <div class="flex items-center justify-between">
                                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">${this.getSectionName(section)}</span>
                                <div class="flex items-center space-x-3">
                                    <div class="w-32 bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                                        <div class="bg-blue-600 dark:bg-blue-400 h-2 rounded-full transition-all duration-300" style="width: ${progress}%"></div>
                                    </div>
                                    <span class="text-sm text-gray-600 dark:text-gray-400 w-12">${progress}%</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- Performance Analysis -->
                <div class="grid md:grid-cols-2 gap-6">
                    <div class="bg-white dark:bg-gray-700 rounded-lg p-6">
                        <h4 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">🎯 Performance Details</h4>
                        <div class="space-y-3">
                            <div class="flex justify-between">
                                <span class="text-gray-600 dark:text-gray-400">Choice Selected:</span>
                                <span class="font-medium text-gray-900 dark:text-white">${data.performance.choiceSelected || 'None'}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600 dark:text-gray-400">Engagement Level:</span>
                                <span class="font-medium text-gray-900 dark:text-white">${data.performance.engagementLevel}</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600 dark:text-gray-400">Completion Status:</span>
                                <span class="font-medium text-gray-900 dark:text-white">${data.performance.completed ? 'Completed' : 'In Progress'}</span>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white dark:bg-gray-700 rounded-lg p-6">
                        <h4 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">💡 Insights</h4>
                        <div class="space-y-2 text-sm">
                            ${data.insights.map(insight => `
                                <div class="flex items-start space-x-2">
                                    <span class="text-blue-500 mt-1">•</span>
                                    <span class="text-gray-700 dark:text-gray-300">${insight}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <!-- Activity Timeline -->
                <div class="bg-white dark:bg-gray-700 rounded-lg p-6">
                    <h4 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">📝 Activity Timeline</h4>
                    <div class="space-y-2 max-h-60 overflow-y-auto">
                        ${data.interactions.map(interaction => {
                            const time = new Date(interaction.timestamp).toLocaleTimeString();
                            const description = this.getInteractionDescription(interaction);
                            return `
                                <div class="flex justify-between items-center py-2 border-b dark:border-gray-600 last:border-b-0">
                                    <span class="text-sm text-gray-700 dark:text-gray-300">${description}</span>
                                    <span class="text-xs text-gray-500 dark:text-gray-400">${time}</span>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    generateDetailedReportHTML(data) {
        return `
            <div class="space-y-6">
                <!-- Summary Cards -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg text-center">
                        <div class="text-3xl font-bold text-blue-600 dark:text-blue-400">${data.summary.overallProgress}%</div>
                        <div class="text-sm text-blue-800 dark:text-blue-300">Overall Progress</div>
                    </div>
                    <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg text-center">
                        <div class="text-3xl font-bold text-green-600 dark:text-green-400">${data.summary.totalTimeSpent}</div>
                        <div class="text-sm text-green-800 dark:text-green-300">Time Spent</div>
                    </div>
                    <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg text-center">
                        <div class="text-3xl font-bold text-purple-600 dark:text-purple-400">${data.summary.sectionsCompleted}/${data.summary.totalSections}</div>
                        <div class="text-sm text-purple-800 dark:text-purple-300">Sections</div>
                    </div>
                    <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg text-center">
                        <div class="text-3xl font-bold text-orange-600 dark:text-orange-400">${data.interactions.length}</div>
                        <div class="text-sm text-orange-800 dark:text-orange-300">Interactions</div>
                    </div>
                </div>

                <!-- Section Details -->
                <div class="bg-white dark:bg-gray-700 rounded-lg p-6">
                    <h4 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">📚 Section Breakdown</h4>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm">
                            <thead>
                                <tr class="border-b dark:border-gray-600">
                                    <th class="text-left py-2 text-gray-900 dark:text-white">Section</th>
                                    <th class="text-left py-2 text-gray-900 dark:text-white">Progress</th>
                                    <th class="text-left py-2 text-gray-900 dark:text-white">Time Spent</th>
                                    <th class="text-left py-2 text-gray-900 dark:text-white">Status</th>
                                    <th class="text-left py-2 text-gray-900 dark:text-white">Last Accessed</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.sections.map(section => `
                                    <tr class="border-b dark:border-gray-600">
                                        <td class="py-2 text-gray-700 dark:text-gray-300">${section.name}</td>
                                        <td class="py-2">
                                            <div class="flex items-center space-x-2">
                                                <div class="w-20 bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                                                    <div class="bg-blue-600 dark:bg-blue-400 h-2 rounded-full" style="width: ${section.progress}%"></div>
                                                </div>
                                                <span class="text-gray-600 dark:text-gray-400">${section.progress}%</span>
                                            </div>
                                        </td>
                                        <td class="py-2 text-gray-700 dark:text-gray-300">${section.timeSpent}</td>
                                        <td class="py-2">
                                            <span class="px-2 py-1 rounded-full text-xs ${section.completed ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'}">
                                                ${section.completed ? 'Completed' : 'In Progress'}
                                            </span>
                                        </td>
                                        <td class="py-2 text-gray-700 dark:text-gray-300">${section.lastAccessed}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Recommendations -->
                <div class="bg-white dark:bg-gray-700 rounded-lg p-6">
                    <h4 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">💡 Recommendations</h4>
                    <div class="space-y-2">
                        ${data.recommendations.map(rec => `
                            <div class="flex items-start space-x-2">
                                <span class="text-blue-500 mt-1">•</span>
                                <span class="text-gray-700 dark:text-gray-300">${rec}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    setupModalEventListeners(modal, reportData) {
        const closeBtn = modal.querySelector('#closeReportModal');
        const downloadBtn = modal.querySelector('#downloadReportBtn');
        const printBtn = modal.querySelector('#printReportBtn');
        const shareBtn = modal.querySelector('#shareReportBtn');
        const timestamp = modal.querySelector('#reportTimestamp');

        if (timestamp) {
            timestamp.textContent = `Generated on ${new Date().toLocaleString()}`;
        }

        if (closeBtn) {
            closeBtn.onclick = () => modal.style.display = 'none';
        }

        if (downloadBtn) {
            downloadBtn.onclick = () => this.downloadReport(reportData);
        }

        if (printBtn) {
            printBtn.onclick = () => this.printReport(modal);
        }

        if (shareBtn) {
            shareBtn.onclick = () => this.shareReport(reportData);
        }

        // Close on backdrop click
        modal.onclick = (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        };
    }

    downloadReport(data) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `learning-report-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        if (window.notificationManager) {
            window.notificationManager.show('Report downloaded successfully!', 'success');
        }
    }

    printReport(modal) {
        const content = modal.querySelector('#reportModalContent').innerHTML;
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
                <head>
                    <title>Learning Analytics Report</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
                        .grid { display: grid; gap: 1rem; }
                        .grid-cols-1 { grid-template-columns: 1fr; }
                        .grid-cols-2 { grid-template-columns: 1fr 1fr; }
                        .grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
                        .space-y-6 > * + * { margin-top: 1.5rem; }
                        .space-y-4 > * + * { margin-top: 1rem; }
                        .space-y-3 > * + * { margin-top: 0.75rem; }
                        .space-y-2 > * + * { margin-top: 0.5rem; }
                        .bg-blue-50, .bg-green-50, .bg-purple-50, .bg-orange-50, .bg-white { 
                            background-color: #f8f9fa; border: 1px solid #dee2e6; 
                        }
                        .p-4, .p-6 { padding: 1rem; }
                        .rounded-lg { border-radius: 0.5rem; }
                        .text-center { text-align: center; }
                        .font-bold { font-weight: bold; }
                        .font-semibold { font-weight: 600; }
                        .text-3xl { font-size: 2rem; }
                        .text-lg { font-size: 1.125rem; }
                        .text-sm { font-size: 0.875rem; }
                        .text-xs { font-size: 0.75rem; }
                        .flex { display: flex; }
                        .justify-between { justify-content: space-between; }
                        .items-center { align-items: center; }
                        .overflow-x-auto { overflow-x: auto; }
                        table { width: 100%; border-collapse: collapse; }
                        th, td { padding: 0.5rem; text-align: left; border-bottom: 1px solid #dee2e6; }
                        @media print { 
                            body { margin: 0; } 
                            .no-print { display: none; }
                        }
                    </style>
                </head>
                <body>
                    <h1>📊 Learning Analytics Report</h1>
                    ${content}
                    <div style="margin-top: 2rem; text-align: center; color: #666; font-size: 0.875rem;">
                        <p>Generated on ${new Date().toLocaleString()}</p>
                        <p>Course Container System</p>
                    </div>
                </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }

    shareReport(data) {
        if (navigator.share) {
            navigator.share({
                title: 'Learning Progress Report',
                text: `Learning progress: ${data.summary?.overallProgress || data.performance?.score || 'N/A'}% complete`,
                url: window.location.href
            });
        } else {
            // Fallback: copy to clipboard
            const summary = `Learning Progress Report\nProgress: ${data.summary?.overallProgress || data.performance?.score || 'N/A'}%\nGenerated: ${new Date().toLocaleString()}`;
            navigator.clipboard.writeText(summary).then(() => {
                if (window.notificationManager) {
                    window.notificationManager.show('Report summary copied to clipboard!', 'success');
                }
            });
        }
    }

    formatDuration(milliseconds) {
        const hours = Math.floor(milliseconds / 3600000);
        const minutes = Math.floor((milliseconds % 3600000) / 60000);
        const seconds = Math.floor((milliseconds % 60000) / 1000);
        
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else if (minutes > 0) {
            return `${minutes}m ${seconds}s`;
        } else {
            return `${seconds}s`;
        }
    }

    getSectionName(sectionId) {
        const names = {
            '1': 'Opening Assessment',
            '2': 'Content Review',
            '3': 'Completion',
            'lecture': 'Interactive Lecture',
            'practice': 'Practice & Discussion',
            'reflect': 'Reflect & Assess'
        };
        return names[sectionId] || sectionId;
    }

    getInteractionDescription(interaction) {
        switch (interaction.type) {
            case 'multiple_choice':
                return `Selected choice ${interaction.choice} (${interaction.correct ? 'Correct' : 'Incorrect'})`;
            case 'task_skipped':
                return 'Skipped assessment task';
            case 'lesson_completed':
                return 'Completed the lesson';
            case 'section_start':
                return `Started section ${interaction.section}`;
            default:
                return interaction.type || 'Unknown interaction';
        }
    }

    generateRecommendations(sections, overallProgress) {
        const recommendations = [];
        
        if (overallProgress < 25) {
            recommendations.push('Consider starting with the Interactive Lecture to build foundational knowledge');
        }
        
        if (overallProgress >= 25 && overallProgress < 75) {
            recommendations.push('Continue with the Practice & Discussion section to apply your learning');
        }
        
        if (overallProgress >= 75 && overallProgress < 100) {
            recommendations.push('Complete the Reflect & Assess section to consolidate your understanding');
        }
        
        const incompleteSections = Object.entries(sections).filter(([_, data]) => !data.completed);
        if (incompleteSections.length > 0) {
            recommendations.push(`Focus on completing: ${incompleteSections.map(([id, _]) => this.getSectionName(id)).join(', ')}`);
        }
        
        if (recommendations.length === 0) {
            recommendations.push('Excellent work! Consider reviewing completed sections or exploring advanced topics');
        }
        
        return recommendations;
    }

    generateLectureInsights(lectureData) {
        const insights = [];
        
        if (lectureData.score !== null) {
            if (lectureData.score >= 80) {
                insights.push('Excellent performance on the assessment - you have a strong grasp of the concepts');
            } else if (lectureData.score >= 60) {
                insights.push('Good performance with room for improvement - consider reviewing the explanation');
            } else {
                insights.push('Consider reviewing the content and retaking the assessment to improve understanding');
            }
        }
        
        const timeSpent = lectureData.timeSpent || (Date.now() - lectureData.startTime);
        const minutes = Math.floor(timeSpent / 60000);
        
        if (minutes < 5) {
            insights.push('Quick completion - ensure you had enough time to absorb the material');
        } else if (minutes > 20) {
            insights.push('Thorough engagement with the content - great dedication to learning');
        }
        
        if (lectureData.interactions.length > 0) {
            insights.push(`Active engagement with ${lectureData.interactions.length} interactions recorded`);
        }
        
        if (lectureData.completed) {
            insights.push('Successfully completed all sections of the interactive lecture');
        }
        
        return insights.length > 0 ? insights : ['Continue engaging with the learning materials for best results'];
    }
}
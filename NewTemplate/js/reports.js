// js/report.js

// Logic for generating and downloading the learning report.

function generateReport() {
    const report = {
        timestamp: new Date().toLocaleString(),
        slideCompletion: completionData.slides.filter(s => s).length,
        taskCompletion: completionData.tasks.filter(t => t).length / 2, // Each task has 2 parts
        interactionCompletion: completionData.interactions.filter(i => i).length,
        responses: {
            task1: { position: document.getElementById('task1-response').value, interest: document.getElementById('task1-interest').value },
            task2: { question: document.getElementById('task2-question').value, significance: document.getElementById('task2-significance').value },
            task3: { impact: document.getElementById('task3-impact').value, challenges: document.getElementById('task3-challenges').value }
        }
    };
    
    const reportHTML = `
        <div class="space-y-6">
            <div class="grid md:grid-cols-3 gap-4">
                <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg text-center"><div class="text-2xl font-bold text-blue-600 dark:text-blue-400">${report.slideCompletion}/5</div><div class="text-sm text-gray-600 dark:text-gray-400">Learning Slides</div></div>
                <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg text-center"><div class="text-2xl font-bold text-green-600 dark:text-green-400">${report.taskCompletion}/3</div><div class="text-sm text-gray-600 dark:text-gray-400">Reflection Tasks</div></div>
                <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg text-center"><div class="text-2xl font-bold text-purple-600 dark:text-purple-400">${report.interactionCompletion}/3</div><div class="text-sm text-gray-600 dark:text-gray-400">Interactive Activities</div></div>
            </div>
            <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <h4 class="font-bold text-gray-900 dark:text-white mb-3">📝 Your Responses Summary</h4>
                <div class="space-y-3 text-sm">
                    <div><strong>Knowledge Position:</strong> ${report.responses.task1.position ? 'Completed' : 'Not completed'}</div>
                    <div><strong>Research Interest:</strong> ${report.responses.task1.interest ? 'Completed' : 'Not completed'}</div>
                    <div><strong>Research Question:</strong> ${report.responses.task2.question ? 'Completed' : 'Not completed'}</div>
                    <div><strong>Research Impact:</strong> ${report.responses.task3.impact ? 'Completed' : 'Not completed'}</div>
                </div>
            </div>
            <div class="text-center"><p class="text-sm text-gray-600 dark:text-gray-400">Generated on: ${report.timestamp}</p></div>
        </div>
    `;
    
    document.getElementById('learningReport').innerHTML = reportHTML;
    window.currentReport = report; // Store for download
}

function downloadReport() {
    if (!window.currentReport) {
        alert('Please generate a report first!');
        return;
    }
    
    const report = window.currentReport;
    const markdown = `# Learning Report: Understanding Research & Ph.D. Studies
**Course:** UCLC 1008 University English I  
**Module:** Research Foundations  
**Generated:** ${report.timestamp}

## Completion Summary
- **Learning Slides:** ${report.slideCompletion}/5 completed
- **Reflection Tasks:** ${report.taskCompletion}/3 completed  
- **Interactive Activities:** ${report.interactionCompletion}/3 completed

## Reflection Responses
### Task 1: Personal Knowledge Reflection
**Current position in knowledge journey:**
${report.responses.task1.position || 'Not completed'}

**Area of interest for exploration:**
${report.responses.task1.interest || 'Not completed'}

### Task 2: Research Question Development
**Research question:**
${report.responses.task2.question || 'Not completed'}

**Significance and knowledge gap:**
${report.responses.task2.significance || 'Not completed'}

### Task 3: Research Impact Vision
**Real-world contributions:**
${report.responses.task3.impact || 'Not completed'}

**Anticipated challenges and solutions:**
${report.responses.task3.challenges || 'Not completed'}

## Next Steps
1. Review any incomplete sections.
2. Discuss your research interests with classmates on Moodle.
3. Consult with an AI assistant for further guidance.
4. Meet with your instructor for personalized feedback.
---
*This report was generated from the UCLC 1008 interactive learning module.*`;

    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'research-learning-report.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
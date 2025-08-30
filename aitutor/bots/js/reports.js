// reports.js - Report Generation Module

function updateReportTimestamp() {
    const timestamp = new Date().toLocaleString();
    document.getElementById('report-timestamp').textContent = timestamp;
}

function generateReport() {
    if (chatHistory.length === 0) {
        showNotification('No conversation to report on', 'error');
        return;
    }

    const report = createReport();
    document.getElementById('report-content').innerHTML = report;
    updateReportTimestamp();
    document.getElementById('report-modal').style.display = 'flex';
}

function createReport() {
    const now = new Date();
    const duration = chatHistory.length > 0 ? 
        Math.round((chatHistory[chatHistory.length - 1].timestamp - chatHistory[0].timestamp) / 1000 / 60) : 0;
    
    const userMessages = chatHistory.filter(msg => msg.role === 'user');
    const assistantMessages = chatHistory.filter(msg => msg.role === 'assistant');
    
    let report = `
        <h2>📊 HKBU Learning Session Report</h2>
        <p><strong>Generated:</strong> ${now.toLocaleString()}</p>
        <p><strong>Duration:</strong> ${duration} minutes</p>
        <p><strong>Total Messages:</strong> ${chatHistory.length}</p>
        <p><strong>Your Messages:</strong> ${userMessages.length}</p>
        <p><strong>Assistant Responses:</strong> ${assistantMessages.length}</p>
        
        <h3>💡 Session Summary</h3>
        <p>${generateSummary()}</p>
        
        <h3>📈 Your Contribution Analysis</h3>
        <p>${analyzeContribution()}</p>
        
        <h3>📝 Complete Conversation</h3>
        <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; max-height: 400px; overflow-y: auto;">
    `;
    
    chatHistory.forEach(msg => {
        report += `
            <div style="margin-bottom: 15px; padding: 10px; background: ${msg.role === 'user' ? '#e3f2fd' : '#f1f8e9'}; border-radius: 6px;">
                <strong>${msg.role === 'user' ? '👤 You' : '🤖 Assistant'}:</strong><br>
                ${msg.content.replace(/\n/g, '<br>')}
                <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
                    ${msg.timestamp.toLocaleTimeString()}
                </div>
            </div>
        `;
    });
    
    report += '</div>';
    
    report += `
        <hr style="margin: 20px 0;">
        <div style="text-align: center; font-size: 0.9rem; color: #666;">
            <strong>Created by:</strong> Dr. Simon Wang, Innovation Officer<br>
            Language Centre, Hong Kong Baptist University<br>
            <a href="mailto:simonwang@hkbu.edu.hk">simonwang@hkbu.edu.hk</a>
        </div>
    `;
    
    return report;
}

function generateSummary() {
    const topics = extractTopics();
    const questionsAsked = chatHistory.filter(msg => 
        msg.role === 'user' && msg.content.includes('?')
    ).length;
    
    return `This learning session covered ${topics.length > 0 ? topics.join(', ') : 'various topics'}. 
            You asked ${questionsAsked} questions and engaged in ${Math.floor(chatHistory.length / 2)} conversation exchanges. 
            The session demonstrated active learning through inquiry and discussion.`;
}

function analyzeContribution() {
    const userMessages = chatHistory.filter(msg => msg.role === 'user');
    if (userMessages.length === 0) return 'No user messages to analyze.';
    
    const avgLength = userMessages.reduce((sum, msg) => sum + msg.content.length, 0) / userMessages.length;
    const questionsRatio = userMessages.filter(msg => msg.content.includes('?')).length / userMessages.length;
    
    let analysis = '';
    
    if (avgLength > 100) {
        analysis += 'You provided detailed and thoughtful messages. ';
    } else if (avgLength > 50) {
        analysis += 'You engaged with good depth in your responses. ';
    } else {
        analysis += 'You kept your messages concise and focused. ';
    }
    
    if (questionsRatio > 0.5) {
        analysis += 'You showed excellent curiosity by asking many questions. ';
    } else if (questionsRatio > 0.2) {
        analysis += 'You balanced questions with statements effectively. ';
    }
    
    analysis += 'Your engagement shows a positive learning attitude and willingness to explore topics deeply.';
    
    return analysis;
}

function extractTopics() {
    const commonWords = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must'];
    const allWords = chatHistory
        .filter(msg => msg.role === 'user')
        .map(msg => msg.content.toLowerCase())
        .join(' ')
        .replace(/[^\w\s]/g, '')
        .split(' ')
        .filter(word => word.length > 3 && !commonWords.includes(word));
    
    const wordCount = {};
    allWords.forEach(word => {
        wordCount[word] = (wordCount[word] || 0) + 1;
    });
    
    return Object.entries(wordCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([word]) => word);
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    doc.setFontSize(16);
    doc.text('HKBU Learning Session Report', 20, 20);
    
    doc.setFontSize(12);
    let yPos = 40;
    
    const reportText = document.getElementById('report-content').innerText;
    const lines = doc.splitTextToSize(reportText, 170);
    
    lines.forEach(line => {
        if (yPos > 280) {
            doc.addPage();
            yPos = 20;
        }
        doc.text(line, 20, yPos);
        yPos += 6;
    });
    
    doc.save(`HKBU_Learning_Report_${new Date().toISOString().split('T')[0]}.pdf`);
}

function downloadMarkdown() {
    const report = createMarkdownReport();
    const blob = new Blob([report], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `HKBU_Learning_Report_${new Date().toISOString().split('T')[0]}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function createMarkdownReport() {
    const now = new Date();
    const duration = chatHistory.length > 0 ? 
        Math.round((chatHistory[chatHistory.length - 1].timestamp - chatHistory[0].timestamp) / 1000 / 60) : 0;
    
    let markdown = `# 📊 HKBU Learning Session Report

**Generated:** ${now.toLocaleString()}
**Duration:** ${duration} minutes
**Total Messages:** ${chatHistory.length}

## 💡 Session Summary

${generateSummary()}

## 📈 Your Contribution Analysis

${analyzeContribution()}

## 📝 Complete Conversation

`;
    
    chatHistory.forEach(msg => {
        const role = msg.role === 'user' ? '👤 **You**' : '🤖 **Assistant**';
        markdown += `### ${role} (${msg.timestamp.toLocaleTimeString()})\n\n${msg.content}\n\n`;
    });
    
    markdown += `---
*Created by: Dr. Simon Wang, Innovation Officer*  
*Language Centre, Hong Kong Baptist University*  
*simonwang@hkbu.edu.hk*`;
    
    return markdown;
}

function copyReport() {
    const reportText = document.getElementById('report-content').innerText;
    navigator.clipboard.writeText(reportText).then(() => {
        showNotification('Report copied to clipboard!', 'success');
    });
}

function closeReport() {
    document.getElementById('report-modal').style.display = 'none';
}
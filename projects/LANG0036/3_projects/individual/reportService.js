// Report generation matching original interactive.html downloadReport formatting

export function generateLearningReportMarkdown(report) {
  if (!report) {
    const ts = new Date().toLocaleString();
    return `# Learning Report: Understanding Research & Ph.D. Studies

**Course:** UCLC 1008 University English I  
**Module:** Research Foundations  
**Generated:** ${ts}
`;
  }

  const timestamp = report.timestamp;

  const task1Position = report?.responses?.task1?.position || 'Not completed';
  const task1Interest = report?.responses?.task1?.interest || 'Not completed';
  const task2Question = report?.responses?.task2?.question || 'Not completed';
  const task2Significance = report?.responses?.task2?.significance || 'Not completed';
  const task3Impact = report?.responses?.task3?.impact || 'Not completed';
  const task3Challenges = report?.responses?.task3?.challenges || 'Not completed';

  // Extract AI feedback, removing HTML tags and converting <br> to newlines
  const cleanHtml = (html) => {
    if (!html) return '';
    return html.replace(/<br>/g, '\n').replace(/<[^>]*>/g, '');
  };

  const aiFeedback = {
    task1: {
      position: cleanHtml(report?.aiFeedback?.task1?.position) || 'No AI feedback received yet',
      interest: cleanHtml(report?.aiFeedback?.task1?.interest) || 'No AI feedback received yet'
    },
    task2: {
      question: cleanHtml(report?.aiFeedback?.task2?.question) || 'No AI feedback received yet',
      significance: cleanHtml(report?.aiFeedback?.task2?.significance) || 'No AI feedback received yet'
    },
    task3: {
      impact: cleanHtml(report?.aiFeedback?.task3?.impact) || 'No AI feedback received yet',
      challenges: cleanHtml(report?.aiFeedback?.task3?.challenges) || 'No AI feedback received yet'
    }
  };

  const md = `# Learning Report: Understanding Research & Ph.D. Studies

**Course:** UCLC 1008 University English I  
**Module:** Research Foundations  
**Generated:** ${timestamp}

## Completion Summary

- **Learning Slides:** ${report.slideCompletion}/5 completed
- **Reflection Tasks:** ${report.taskCompletion}/3 completed  
- **Interactive Activities:** ${report.interactionCompletion}/3 completed

## Reflection Responses

### Task 1: Personal Knowledge Reflection

**Current position in knowledge journey:**
${task1Position}

**AI Feedback on Current Position:**
${aiFeedback.task1.position}

**Area of interest for exploration:**
${task1Interest}

**AI Feedback on Area of Interest:**
${aiFeedback.task1.interest}

### Task 2: Research Question Development

**Research question:**
${task2Question}

**AI Feedback on Research Question:**
${aiFeedback.task2.question}

**Significance and knowledge gap:**
${task2Significance}

**AI Feedback on Significance:**
${aiFeedback.task2.significance}

### Task 3: Research Impact Vision

**Real-world contributions:**
${task3Impact}

**AI Feedback on Real-world Applications:**
${aiFeedback.task3.impact}

**Anticipated challenges and solutions:**
${task3Challenges}

**AI Feedback on Challenges and Solutions:**
${aiFeedback.task3.challenges}

## Next Steps

1. Review any incomplete sections
2. Discuss your research interests with classmates on Moodle
3. Consult with AI assistant for further guidance
4. Meet with instructor during office hours for personalized feedback

---
*This report was generated from the UCLC 1008 interactive learning module on research fundamentals.*
`;

  return md;
}


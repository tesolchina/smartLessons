// js/ai-assistant.js

// Logic for the "AI Learning Assistant" demo chat.

let currentChatMessage = 0;
const chatMessages = [
    { type: 'student', message: 'Hi! I just completed a learning module about research and Ph.D. studies. Can you help me think through my research interests?', analysis: { title: 'Effective Opening', content: 'Student provides context and clearly states what they want help with. This sets up a productive conversation.' } },
    { type: 'ai', message: 'I\'d be happy to help! Could you share what aspects of research most intrigued you from the module? Also, feel free to paste any reflection responses you completed.', analysis: { title: 'Good AI Response', content: 'AI shows willingness to help and asks for specific information to provide better guidance.' } },
    { type: 'student', message: 'I found Matt Might\'s illustration really compelling. I\'m interested in environmental sustainability, particularly how social media can influence environmental behaviors. Here\'s my research question: "How do social media campaigns affect young adults\' environmental behaviors?"', analysis: { title: 'Specific Sharing', content: 'Student shares specific interests and a concrete research question, giving AI something substantive to work with.' } },
    { type: 'ai', message: 'That\'s a fascinating research question! It sits at the intersection of environmental psychology, digital media studies, and behavioral science. To refine it, what specific environmental behaviors are you most interested in? And what aspect of social media campaigns - their messaging, frequency, or visual elements?', analysis: { title: 'Constructive Guidance', content: 'AI recognizes the value of the question while suggesting specific ways to make it more focused and researchable.' } },
    { type: 'student', message: 'I\'m particularly interested in recycling and energy conservation behaviors. For social media, I think the visual storytelling aspect might be most influential - like before/after images or infographics.', analysis: { title: 'Building Specificity', content: 'Student responds to AI\'s questions with more specific details, showing engagement and refinement of thinking.' } },
    { type: 'ai', message: 'Excellent refinement! Now you\'re looking at: "How do visual storytelling elements in social media campaigns influence recycling and energy conservation behaviors among young adults?" This is much more focused. Some follow-up considerations: What age range defines "young adults"? How would you measure behavior change?', analysis: { title: 'Methodological Thinking', content: 'AI helps the student think about practical research design elements and connects to the broader research process.' } }
];

function showChatMessage(index) {
    const container = document.getElementById('aiChatDemo');
    if (!container) return;
    
    container.innerHTML = ''; // Clear existing messages
    
    // Show all messages up to the current index
    for (let i = 0; i <= index; i++) {
        const msg = chatMessages[i];
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${msg.type === 'student' ? 'flex justify-end' : 'flex justify-start'}`;
        messageDiv.innerHTML = `<div class="${msg.type === 'student' ? 'bg-primary text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-100'} rounded-lg p-3 max-w-xs"><p class="text-sm">${msg.message}</p></div>`;
        container.appendChild(messageDiv);
    }
    
    document.getElementById('chatProgress').textContent = `${index + 1} / ${chatMessages.length}`;
    updateChatAnalysis(index);
    container.scrollTop = container.scrollHeight;
}

function updateChatAnalysis(index) {
    const analysisContainer = document.getElementById('chatAnalysis');
    if (!analysisContainer) return;
    const { title, content } = chatMessages[index].analysis;
    analysisContainer.innerHTML = `<div class="annotation-highlight"><h4 class="font-medium text-primary">${title}</h4><p class="text-sm">${content}</p></div>`;
}

function nextChatMessage() { if (currentChatMessage < chatMessages.length - 1) { currentChatMessage++; showChatMessage(currentChatMessage); } }
function prevChatMessage() { if (currentChatMessage > 0) { currentChatMessage--; showChatMessage(currentChatMessage); } }
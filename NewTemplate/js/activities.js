// js/activities.js

// Contains all logic for the "Interactive Knowledge Explorer" games.

let currentGame = 1;
const totalGames = 3;

function showGame(gameNumber) {
    document.querySelectorAll('.game-slide').forEach(slide => slide.classList.add('hidden'));
    document.querySelectorAll('.activity-notes').forEach(notes => notes.classList.add('hidden'));
    
    const currentGameElement = document.querySelector(`[data-game="${gameNumber}"]`);
    const currentNotesElement = document.querySelector(`[data-notes="${gameNumber}"]`);
    
    if (currentGameElement) currentGameElement.classList.remove('hidden');
    if (currentNotesElement) currentNotesElement.classList.remove('hidden');
    
    const gameCounter = document.getElementById('gameCounter');
    if(gameCounter) gameCounter.textContent = `${gameNumber} / ${totalGames}`;
    
    // Initialize specific game content if needed
    if (gameNumber === 1) {
        updateKnowledgeCircle();
    }
    
    // Mark interaction as completed for progress tracking
    if (!completionData.interactions[gameNumber - 1]) {
        completionData.interactions[gameNumber - 1] = true;
        updateProgress();
    }
}

function nextGame() { if (currentGame < totalGames) { currentGame++; showGame(currentGame); } }
function prevGame() { if (currentGame > 1) { currentGame--; showGame(currentGame); } }

// --- Activity 1: Knowledge Circle ---
function updateKnowledgeCircle() {
    const levelEl = document.getElementById('educationLevel');
    if (!levelEl) return; // Guard clause
    const level = levelEl.value;
    const container = document.getElementById('knowledgeVisualization');
    const configs = {
        elementary: { size: 30, color: '#FFB800', label: 'Basic Knowledge' },
        highschool: { size: 50, color: '#FF8C00', label: 'Expanded Knowledge' },
        bachelor: { size: 70, color: '#5D5CDE', label: 'Specialized Knowledge' },
        master: { size: 85, color: '#7B7AE8', label: 'Deep Specialty' },
        phd: { size: 95, color: '#4A49C2', label: 'Expert + New Knowledge' }
    };
    const config = configs[level];
    container.innerHTML = `<svg viewBox="0 0 320 320" class="w-full h-full"><circle cx="160" cy="160" r="150" fill="#E5E7EB" stroke="#9CA3AF" stroke-width="2"/><text x="160" y="50" text-anchor="middle" fill="#6B7280" font-size="12" font-weight="bold">All Human Knowledge</text><circle cx="160" cy="160" r="${config.size}" fill="${config.color}" opacity="0.7" class="interactive-circle" onclick="highlightKnowledge()"/><text x="160" y="160" text-anchor="middle" dominant-baseline="middle" fill="white" font-size="10" font-weight="bold">${config.label}</text>${level === 'phd' ? `<circle cx="${160 + config.size - 10}" cy="160" r="15" fill="#9F9EED" opacity="0.9"/><text x="${160 + config.size - 10}" y="160" text-anchor="middle" dominant-baseline="middle" fill="white" font-size="8" font-weight="bold">Your Dent</text>` : ''}</svg>`;
}

function highlightKnowledge() {
    document.querySelectorAll('.interactive-circle').forEach(circle => {
        circle.style.filter = 'brightness(1.2)';
        setTimeout(() => { circle.style.filter = 'brightness(1)'; }, 200);
    });
}

// --- Activity 2: Research Journey Simulator ---
let researchStep = 0;
const researchSteps = ['Choose Your Field', 'Find Knowledge Gap', 'Focus Your Question', 'Push the Boundary', 'Make Your Contribution!'];
const researchFeedback = ['Click "Choose Field" to start your research journey!', 'Great! You\'ve chosen your field. Now find a gap in current knowledge.', 'Excellent! You\'ve identified a gap. Time to focus on a specific research question.', 'Perfect! Now comes the hard part - years of pushing at the boundary.', 'Congratulations! You\'ve made your dent in human knowledge. Keep pushing!'];

function advanceResearch(step) {
    if (step !== researchStep + 1) return;
    researchStep = step;
    
    document.getElementById('researchProgress').textContent = `Step ${step}: ${researchSteps[step - 1]}`;
    document.getElementById('researchFeedback').textContent = researchFeedback[step];
    
    const currentButton = document.querySelector(`[data-step="${step}"]`);
    currentButton.classList.remove('bg-gray-400', 'bg-blue-500', 'hover:bg-blue-600');
    currentButton.classList.add('bg-green-500', 'hover:bg-green-600');
    
    if (step < 4) {
        const nextButton = document.querySelector(`[data-step="${step + 1}"]`);
        nextButton.disabled = false;
        nextButton.classList.remove('bg-gray-400');
        nextButton.classList.add('bg-blue-500', 'hover:bg-blue-600');
    }
}

// --- Activity 3: Citation Network ---
function showCitationNetwork() {
    const container = document.getElementById('citationNetwork');
    container.innerHTML = `
        <div class="bg-white dark:bg-gray-800 rounded-lg p-6">
            <svg viewBox="0 0 600 400" class="w-full h-auto">
                <circle cx="100" cy="100" r="15" fill="#FFB800" opacity="0.8"/><text x="100" y="85" text-anchor="middle" fill="#374151" font-size="10">Smith 2010</text>
                <circle cx="200" cy="150" r="15" fill="#FF8C00" opacity="0.8"/><text x="200" y="135" text-anchor="middle" fill="#374151" font-size="10">Jones 2015</text>
                <circle cx="300" cy="120" r="15" fill="#5D5CDE" opacity="0.8"/><text x="300" y="105" text-anchor="middle" fill="#374151" font-size="10">Lee 2018</text>
                <circle cx="400" cy="180" r="15" fill="#7B7AE8" opacity="0.8"/><text x="400" y="165" text-anchor="middle" fill="#374151" font-size="10">Taylor 2020</text>
                <circle cx="500" cy="140" r="20" fill="#4A49C2" opacity="0.9"/><text x="500" y="125" text-anchor="middle" fill="#374151" font-size="10" font-weight="bold">Your Work 2024</text>
                <line x1="115" y1="100" x2="185" y2="150" stroke="#9CA3AF" stroke-width="2"/><line x1="215" y1="150" x2="285" y2="120" stroke="#9CA3AF" stroke-width="2"/><line x1="315" y1="120" x2="385" y2="180" stroke="#9CA3AF" stroke-width="2"/><line x1="415" y1="180" x2="480" y2="140" stroke="#9CA3AF" stroke-width="2"/><line x1="115" y1="100" x2="285" y2="120" stroke="#9CA3AF" stroke-width="1" stroke-dasharray="5,5"/><line x1="215" y1="150" x2="480" y2="140" stroke="#9CA3AF" stroke-width="1" stroke-dasharray="5,5"/>
                <text x="50" y="350" fill="#374151" font-size="12" font-weight="bold">Citation Network:</text><line x1="50" y1="365" x2="80" y2="365" stroke="#9CA3AF" stroke-width="2"/><text x="90" y="370" fill="#6B7280" font-size="10">Direct Citation</text><line x1="200" y1="365" x2="230" y2="365" stroke="#9CA3AF" stroke-width="1" stroke-dasharray="5,5"/><text x="240" y="370" fill="#6B7280" font-size="10">Indirect Influence</text>
            </svg>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-4 text-center">Each research contribution builds upon previous work and enables future discoveries.</p>
        </div>
    `;
}
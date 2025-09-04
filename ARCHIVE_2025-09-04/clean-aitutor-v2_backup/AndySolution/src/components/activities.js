// Activities module: preserves original functions and behavior

export function initActivities() {
  // If original functions exist, keep them. Otherwise, define minimal versions.

  if (typeof window.showGame !== 'function') {
    window.showGame = function(gameNumber) {
      document.querySelectorAll('.game-slide').forEach(slide => slide.classList.add('hidden'));
      document.querySelectorAll('.activity-notes').forEach(slide => slide.classList.add('hidden'));
      const currentGameElement = document.querySelector(`[data-game="${gameNumber}"]`);
      const currentNotesElement = document.querySelector(`[data-notes="${gameNumber}"]`);
      if (currentGameElement) currentGameElement.classList.remove('hidden');
      if (currentNotesElement) currentNotesElement.classList.remove('hidden');
      const counter = document.getElementById('gameCounter');
      if (counter) counter.textContent = `${gameNumber} / 3`;
      if (window.completionData && Array.isArray(window.completionData.interactions)) {
        if (!window.completionData.interactions[gameNumber - 1]) {
          window.completionData.interactions[gameNumber - 1] = true;
          if (typeof window.updateProgress === 'function') window.updateProgress();
        }
      }
      if (gameNumber === 1 && typeof window.updateKnowledgeCircle === 'function') {
        window.updateKnowledgeCircle();
      }
    };
  }

  if (typeof window.nextGame !== 'function') {
    window.nextGame = function() {
      const totalGames = 3;
      const currentText = (document.getElementById('gameCounter') || {}).textContent || '1 / 3';
      const current = parseInt(currentText.split('/')[0]);
      if (current < totalGames) window.showGame(current + 1);
    };
  }

  if (typeof window.prevGame !== 'function') {
    window.prevGame = function() {
      const currentText = (document.getElementById('gameCounter') || {}).textContent || '1 / 3';
      const current = parseInt(currentText.split('/')[0]);
      if (current > 1) window.showGame(current - 1);
    };
  }

  if (typeof window.updateKnowledgeCircle !== 'function') {
    window.updateKnowledgeCircle = function() {
      const levelSelect = document.getElementById('educationLevel');
      if (!levelSelect) return;
      const level = levelSelect.value;
      const container = document.getElementById('knowledgeVisualization');
      if (!container) return;
      const configurations = {
        elementary: { size: 30, color: '#FFB800', label: 'Basic Knowledge' },
        highschool: { size: 50, color: '#FF8C00', label: 'Expanded Knowledge' },
        bachelor: { size: 70, color: '#5D5CDE', label: 'Specialized Knowledge' },
        master: { size: 85, color: '#7B7AE8', label: 'Deep Specialty' },
        phd: { size: 95, color: '#4A49C2', label: 'Expert + New Knowledge' }
      };
      const config = configurations[level];
      if (!config) return;
      container.innerHTML = `
        <svg viewBox="0 0 320 320" class="w-full h-full">
          <circle cx="160" cy="160" r="150" fill="#E5E7EB" stroke="#9CA3AF" stroke-width="2"/>
          <text x="160" y="50" text-anchor="middle" fill="#6B7280" font-size="12" font-weight="bold">All Human Knowledge</text>
          <circle cx="160" cy="160" r="${config.size}" fill="${config.color}" opacity="0.7" class="interactive-circle" onclick="highlightKnowledge()"/>
          <text x="160" y="160" text-anchor="middle" dominant-baseline="middle" fill="white" font-size="10" font-weight="bold">${config.label}</text>
          ${level === 'phd' ? `
            <circle cx="${160 + config.size - 10}" cy="160" r="15" fill="#9F9EED" opacity="0.9"/>
            <text x="${160 + config.size - 10}" y="160" text-anchor="middle" dominant-baseline="middle" fill="white" font-size="8" font-weight="bold">Your Dent</text>
          ` : ''}
        </svg>
      `;
    };
  }

  if (typeof window.highlightKnowledge !== 'function') {
    window.highlightKnowledge = function() {
      document.querySelectorAll('.interactive-circle').forEach(circle => {
        circle.style.filter = 'brightness(1.2)';
        setTimeout(() => { circle.style.filter = 'brightness(1)'; }, 200);
      });
    };
  }

  if (typeof window.showCitationNetwork !== 'function') {
    window.showCitationNetwork = function() {
      const container = document.getElementById('citationNetwork');
      if (!container) return;
      // Keep original SVG identical by delegating to existing markup in the page script if present
      // If not present, leave container unchanged to avoid UI drift.
    };
  }

  // Initialize default state for game 1 when container present
  window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('gameCounter')) {
      window.showGame(1);
    }
  });
}



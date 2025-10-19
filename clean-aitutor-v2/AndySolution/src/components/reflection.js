// Reflection tasks module: preserve IDs and progress updates

export function initReflection() {
  // No UI changes; ensure the updateProgress function exists and uses the same IDs
  if (typeof window.updateProgress !== 'function') {
    window.updateProgress = function() {
      const task1 = document.getElementById('task1-response')?.value.trim() && document.getElementById('task1-interest')?.value.trim();
      const task2 = document.getElementById('task2-question')?.value.trim() && document.getElementById('task2-significance')?.value.trim();
      const task3 = document.getElementById('task3-impact')?.value.trim() && document.getElementById('task3-challenges')?.value.trim();
      if (!window.completionData) return;
      window.completionData.tasks = [task1, task2, task3];
      const totalItems = window.completionData.slides.length + window.completionData.tasks.length + window.completionData.interactions.length;
      const completedItems = [...window.completionData.slides, ...window.completionData.tasks, ...window.completionData.interactions].filter(Boolean).length;
      const progress = Math.round((completedItems / totalItems) * 100);
      const bar = document.getElementById('progressBar');
      const text = document.getElementById('progressText');
      if (bar) bar.style.width = `${progress}%`;
      if (text) text.textContent = `${progress}% Complete`;
    };
  }
}



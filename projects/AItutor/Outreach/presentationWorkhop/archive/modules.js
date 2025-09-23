// modules.js: Handles dynamic iFrame loading in the canvas area based on Google Slides navigation

// --- CONFIG ---
// Map slide numbers to iFrame URLs or HTML modules
const slideModules = {
    1: { type: 'text', content: 'Welcome! Select a slide in Google Slides to load a module here.' },
    2: { type: 'iframe', url: 'https://www.example.com/' },
    3: { type: 'iframe', url: 'https://www.wikipedia.org/' },
    4: { type: 'iframe', url: 'https://www.youtube.com/embed/dQw4w9WgXcQ' },
    // Add more mappings as needed
};

// --- LOGIC ---
const canvas = document.getElementById('canvas-area');
const slideNumSpan = document.getElementById('slide-num');

// Simulate slide change (for demo: use arrow keys)
let currentSlide = 1;
function loadModuleForSlide(slide) {
    slideNumSpan.textContent = slide;
    const mod = slideModules[slide];
    if (!mod) {
        canvas.innerHTML = '<em>No module mapped for this slide.</em>';
        return;
    }
    if (mod.type === 'iframe') {
        canvas.innerHTML = `<iframe src="${mod.url}" style="width:100%;height:300px;border:none;border-radius:8px;"></iframe>`;
    } else if (mod.type === 'text') {
        canvas.textContent = mod.content;
    }
}

// For demo: left/right arrow keys to change slide
window.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') {
        currentSlide = Math.min(currentSlide + 1, 10);
        loadModuleForSlide(currentSlide);
    } else if (e.key === 'ArrowLeft') {
        currentSlide = Math.max(currentSlide - 1, 1);
        loadModuleForSlide(currentSlide);
    }
});

// Initial load
loadModuleForSlide(currentSlide);

// ---
// In production, you would sync the slide number with the Google Slides API or listen for postMessage events from the iframe if possible.
// For now, this demo uses arrow keys to simulate slide navigation.

// js/slides.js

// Contains all logic related to the "Learning Content" slides.

let currentSlide = 1;
const totalSlides = 5;

function showSlide(slideNumber) {
    document.querySelectorAll('.slide').forEach(slide => {
        slide.classList.add('hidden');
    });
    
    const currentSlideElement = document.querySelector(`[data-slide="${slideNumber}"]`);
    if (currentSlideElement) {
        currentSlideElement.classList.remove('hidden');
    }
    
    const slideCounter = document.getElementById('slideCounter');
    if(slideCounter) slideCounter.textContent = `${slideNumber} / ${totalSlides}`;
    
    // Mark slide as visited for progress tracking
    if (!completionData.slides[slideNumber - 1]) {
        completionData.slides[slideNumber - 1] = true;
        updateProgress();
    }
}

function nextSlide() {
    if (currentSlide < totalSlides) {
        currentSlide++;
        showSlide(currentSlide);
    }
}

function prevSlide() {
    if (currentSlide > 1) {
        currentSlide--;
        showSlide(currentSlide);
    }
}

function checkAnswer(questionNumber, correctAnswer) {
    const selected = document.querySelector(`input[name="q${questionNumber}"]:checked`);
    const feedback = document.getElementById(`feedback${questionNumber}`);
    
    if (!selected) {
        feedback.className = 'mt-2 text-sm text-orange-600 dark:text-orange-400';
        feedback.textContent = '⚠️ Please select an answer first.';
        feedback.classList.remove('hidden');
        return;
    }
    
    const isCorrect = selected.value === correctAnswer;
    
    const feedbackMessages = {
        1: { correct: "✅ Excellent! Research is indeed about discovering new knowledge and expanding human understanding.", incorrect: "❌ Not quite. The primary goal of academic research is to discover new knowledge and expand human understanding." },
        2: { correct: "✅ Perfect! A Ph.D. represents making a small but meaningful contribution to the boundary of human knowledge.", incorrect: "❌ Incorrect. According to Matt Might, a Ph.D. is about making a small dent in the boundary of human knowledge." },
        3: { correct: "✅ Correct! Research begins by identifying what we don't yet know - the gaps in current understanding.", incorrect: "❌ Not quite. The research process starts by identifying gaps in current knowledge at the boundary of what we know." },
        4: { correct: "✅ Exactly! Literature reviews help you understand what has already been discovered in your field.", incorrect: "❌ Incorrect. Literature reviews are conducted to survey and understand existing knowledge in your research area." },
        5: { correct: "✅ Perfect! Matt Might's key message is that every contribution matters and we should keep pushing the boundaries.", incorrect: "❌ Not quite. The key message is that every small contribution to knowledge matters and you should keep pushing." }
    };
    
    feedback.className = isCorrect ? 'mt-2 text-sm text-green-600 dark:text-green-400' : 'mt-2 text-sm text-red-600 dark:text-red-400';
    feedback.textContent = isCorrect ? feedbackMessages[questionNumber].correct : feedbackMessages[questionNumber].incorrect;
    feedback.classList.remove('hidden');
    
    document.querySelectorAll(`input[name="q${questionNumber}"]`).forEach(input => {
        input.disabled = true;
    });
}
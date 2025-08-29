// Slides component: preserves original global API while encapsulating logic

export function initSlides() {
  const totalSlides = 5;
  let currentSlide = 1;

  function showSlideInternal(slideNumber) {
    document.querySelectorAll('.slide').forEach(slide => {
      slide.classList.add('hidden');
    });
    const currentSlideElement = document.querySelector(`[data-slide="${slideNumber}"]`);
    if (currentSlideElement) {
      currentSlideElement.classList.remove('hidden');
    }
    const counter = document.getElementById('slideCounter');
    if (counter) counter.textContent = `${slideNumber} / ${totalSlides}`;
    if (window.completionData && Array.isArray(window.completionData.slides)) {
      if (!window.completionData.slides[slideNumber - 1]) {
        window.completionData.slides[slideNumber - 1] = true;
        if (typeof window.updateProgress === 'function') {
          window.updateProgress();
        }
      }
    }
  }

  // Expose identical global API expected by the page
  window.showSlide = function(slideNumber) {
    currentSlide = Math.max(1, Math.min(slideNumber, totalSlides));
    showSlideInternal(currentSlide);
  };

  window.nextSlide = function() {
    if (currentSlide < totalSlides) {
      currentSlide++;
      showSlideInternal(currentSlide);
    }
  };

  window.prevSlide = function() {
    if (currentSlide > 1) {
      currentSlide--;
      showSlideInternal(currentSlide);
    }
  };

  // Initialize to slide 1 if container exists
  if (document.getElementById('slidesContainer')) {
    showSlideInternal(currentSlide);
  }
}


// Progress tracker bootstrap preserving original data shape

export function initProgressState() {
  if (!window.completionData) {
    window.completionData = {
      slides: [false, false, false, false, false],
      tasks: [false, false, false],
      interactions: [false, false, false]
    };
  }
}



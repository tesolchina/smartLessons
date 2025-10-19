export function createAssessmentItem(assessment) {
    const dashOffset = 251.2 - (assessment.percentage * 251.2 / 100);
    
    // Generate category tags
    const categoryTags = assessment.categories ? assessment.categories.map(category => 
        `<span class="category-tag tag-${category.toLowerCase()}">${category}</span>`
    ).join('') : '';
    
    return `
    <div class="assessment-item bg-white rounded-lg shadow-md p-6 mb-4">
        <div class="assessment-circle cursor-pointer" onclick="toggleDetails('${assessment.id}')">
            <div class="w-24 h-24 mx-auto mb-4 relative">
                <svg class="w-24 h-24 progress-circle">
                    <circle cx="48" cy="48" r="40" stroke="#e5e7eb" stroke-width="6" fill="none"/>
                    <circle cx="48" cy="48" r="40" stroke="#3B82F6" stroke-width="6" fill="none" 
                        stroke-dasharray="251.2" stroke-dashoffset="${dashOffset}" stroke-linecap="round"/>
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                    <span class="text-xl font-bold text-gray-900">${assessment.percentage}%</span>
                </div>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 text-center mb-2">${assessment.title}</h3>
            <p class="text-sm text-gray-600 text-center">${assessment.timeframe}</p>
        </div>
        <div id="${assessment.id}" class="details-panel mt-4">
            <div class="border-t border-gray-200 pt-4">
                <div class="mb-3">
                    ${categoryTags}
                </div>
                <h4 class="font-medium text-gray-900 mb-2">Task Details:</h4>
                <ul class="text-sm text-gray-600 space-y-1">
                    ${assessment.details.map(detail => `<li>• ${detail}</li>`).join('')}
                </ul>
                <p class="text-sm font-medium text-red-600 mt-2">Due: ${assessment.dueDate}</p>
                <div class="edit-links mt-3 pt-3 border-t border-gray-100">
                    ${assessment.links.map((link, index) => 
                        `<a href="${link.url}" class="text-blue-600 text-sm hover:underline ${index > 0 ? 'ml-4' : ''}">${link.text}</a>`
                    ).join('')}
                </div>
            </div>
        </div>
    </div>
    `;
}
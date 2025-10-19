export function createSummarySection(summaryData) {
    return `
    <div class="summary-section p-6 mt-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">Assessment Summary</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="total-breakdown bg-white p-5 rounded-lg shadow-sm">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Assessment Breakdown</h3>
                <div class="space-y-3">
                    ${summaryData.breakdowns.map(item => `
                        <div class="mb-2">
                            <div class="flex justify-between items-center mb-1">
                                <span class="text-gray-700">${item.category}</span>
                                <span class="font-medium text-gray-900">${item.percentage}%</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2.5">
                                <div class="bg-blue-600 h-2.5 rounded-full" style="width: ${item.percentage}%"></div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            <div class="key-dates bg-white p-5 rounded-lg shadow-sm">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Key Dates</h3>
                <div class="space-y-3">
                    ${summaryData.keyDates.map(item => `
                        <div class="key-date-item">
                            <span class="font-medium text-gray-900">${item.week}:</span>
                            <span class="text-gray-700 ml-2">${item.event}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    </div>
    `;
}
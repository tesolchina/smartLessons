#!/usr/bin/env python3

with open('flipped926.html', 'r') as f:
    content = f.read()

# Add header to demo section
demo_header = '''                            <!-- Demo Section Header -->
                            <div class="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                                <div class="flex items-center justify-between">
                                    <h4 class="font-semibold text-blue-800 dark:text-blue-200">📱 Demo Content</h4>
                                    <span id="demo-slide-indicator" class="text-sm text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-800 px-2 py-1 rounded">Slide 1</span>
                                </div>
                                <p class="text-xs text-blue-600 dark:text-blue-300 mt-1">Interactive demonstrations and QR codes for this slide</p>
                            </div>
                            <div id="demo-content" class="demo-content">'''

content = content.replace(
    '                            <div id="demo-content" class="demo-content">',
    demo_header
)

# Add header to resources section  
resources_header = '''                        <div id="resourcesSection" class="canvas-section-content" style="display: none;">
                            <!-- Resources Section Header -->
                            <div class="mb-4 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                                <div class="flex items-center justify-between">
                                    <h4 class="font-semibold text-green-800 dark:text-green-200">📚 Learning Resources</h4>
                                    <span id="resources-slide-indicator" class="text-sm text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-800 px-2 py-1 rounded">Slide 1</span>
                                </div>
                                <p class="text-xs text-green-600 dark:text-green-300 mt-1">Additional materials and references for this slide</p>
                            </div>
                            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Additional Resources</h2>'''

content = content.replace(
    '                        <div id="resourcesSection" class="canvas-section-content" style="display: none;">\n                            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Additional Resources</h2>',
    resources_header
)

with open('flipped926.html', 'w') as f:
    f.write(content)

print("Added section headers successfully")
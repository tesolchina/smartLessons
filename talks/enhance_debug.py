#!/usr/bin/env python3

with open('flipped926.html', 'r') as f:
    content = f.read()

# Add more detailed debug logging for updateDemoContent
content = content.replace(
    'console.log("updateDemoContent called for slide:", slideNum);',
    'console.log("📱 updateDemoContent called for slide:", slideNum);'
)

with open('flipped926.html', 'w') as f:
    f.write(content)

print('Enhanced debug logging')
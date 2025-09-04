#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Configuration
const MARKDOWN_DIR = '../gcap3056_notes';
const HTML_FILE = './intro.html';

// Files to watch
const WATCH_FILES = [
    'project_rubric.md',
    'portfolio_rubric.md', 
    'journal_rubric.md'
];

console.log('🔍 Watching markdown files for changes...');
console.log(`Markdown directory: ${MARKDOWN_DIR}`);
console.log(`Files being watched: ${WATCH_FILES.join(', ')}`);

// Watch each markdown file
WATCH_FILES.forEach(filename => {
    const filePath = path.join(__dirname, MARKDOWN_DIR, filename);
    
    if (fs.existsSync(filePath)) {
        console.log(`✅ Watching: ${filename}`);
        
        fs.watchFile(filePath, { interval: 1000 }, (curr, prev) => {
            if (curr.mtime !== prev.mtime) {
                console.log(`📝 ${filename} has been modified`);
                console.log(`🔄 The web page will automatically reload the content when refreshed`);
                console.log(`💡 Tip: If you have the page open in a browser, just refresh to see changes`);
            }
        });
    } else {
        console.log(`⚠️  File not found: ${filePath}`);
    }
});

console.log('\n📄 Assessment Guide Integration Status:');
console.log('✅ Dynamic markdown loading implemented');
console.log('✅ Content automatically loaded from .md files');
console.log('✅ Changes to .md files will be reflected on page refresh');
console.log('\n💡 To see changes:');
console.log('1. Edit any of the markdown files');
console.log('2. Refresh the browser page');
console.log('3. The updated content will appear automatically');

console.log('\n🚀 Press Ctrl+C to stop watching');

// Keep the script running
process.on('SIGINT', () => {
    console.log('\n👋 Stopped watching files');
    process.exit();
});

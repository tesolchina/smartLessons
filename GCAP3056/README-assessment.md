# Dynamic Assessment Guide Integration

## Overview
The assessment guide now dynamically loads content from markdown files, allowing for easy updates without editing HTML directly.

## How to Use

### Development Setup
1. **Start the web server** from the project root:
   ```bash
   cd /Users/simonwang/gcap3056_project
   python3 -m http.server 8000
   ```

2. **Open the page** at: `http://localhost:8000/GCAP3056/intro.html`

3. **Edit markdown files** in `gcap3056_notes/` directory

4. **Refresh the browser** to see changes automatically

### File Paths
- Main page: `/GCAP3056/intro.html`
- Markdown files: `/gcap3056_notes/*.md`
- Both accessible from web server root at project directory

### 1. Markdown Files
Content is stored in separate markdown files in the `../gcap3056_notes/` directory:
- `project_rubric.md` - Research Paper assessment details
- `portfolio_rubric.md` - Community Engagement Portfolio details  
- `journal_rubric.md` - Reflective Learning Journal details

### 2. Dynamic Loading
When the page loads, JavaScript automatically:
- Fetches the markdown files
- Converts them to HTML using a built-in parser
- Displays them in the appropriate assessment tabs

### 3. Auto-Update Process
To update the assessment content:

1. **Edit the markdown files** in `gcap3056_notes/`
2. **Refresh the browser page** - content updates automatically
3. **No HTML editing required**

## File Structure
```
GCAP3056/
├── intro.html              # Main course page
├── watch-markdown.js       # File watcher script (optional)
└── README-assessment.md    # This file

../gcap3056_notes/
├── project_rubric.md       # Research Paper content
├── portfolio_rubric.md     # Portfolio content
├── journal_rubric.md       # Journal content
└── timeline.md            # Project timeline
```

## Benefits

✅ **Easy Updates**: Edit markdown files instead of HTML  
✅ **Automatic Loading**: Content appears instantly on page refresh  
✅ **Version Control**: Track changes to assessment criteria easily  
✅ **Consistent Formatting**: Markdown ensures uniform appearance  
✅ **Separation of Concerns**: Content separate from presentation  

## Optional: File Watching

For development convenience, you can run the file watcher:

```bash
cd GCAP3056
node watch-markdown.js
```

This will monitor the markdown files and notify you when changes are detected.

## Markdown Support

The built-in parser supports:
- Headers (# ## ###)
- Bold text (**text**)
- Lists (- or *)
- Tables (| column | column |)
- Links ([text](url))

## Troubleshooting

**Content not loading?**
- Check browser console for errors
- Verify markdown files exist in `../gcap3056_notes/`
- Ensure file names match exactly

**Formatting issues?**
- Check markdown syntax
- Tables need proper `|` delimiters
- Lists need proper indentation

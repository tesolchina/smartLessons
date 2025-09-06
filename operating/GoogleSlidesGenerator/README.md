# Google Slides Generator System
**Automated Markdown to Google Slides Converter**

## 📁 System Overview

This automation system converts markdown files (especially lecture notes and presentations) into Google Slides presentations and uploads them directly to Google Drive. It's designed to work with educational content like the GCAP 3226 course materials.

## 🛠️ How It Works

### **Input:** 
- Markdown files with slide structures (using `---` or `##` as slide delimiters)
- Configuration files specifying slide themes, layouts, and Google Drive destinations
- Optional image files for slide content

### **Processing:**
1. **Parse Markdown:** Extract slide content, titles, bullet points, and formatting
2. **Create Slides:** Generate Google Slides presentation using Google Slides API
3. **Apply Styling:** Use professional templates and consistent formatting
4. **Upload to Drive:** Save directly to specified Google Drive folder
5. **Share Access:** Set appropriate permissions for course team access

### **Output:**
- Native Google Slides presentations (not PowerPoint files)
- Direct Google Drive integration with sharing capabilities
- Automatic slide formatting and professional styling

## 📋 System Components

### **Core Scripts:**
- `markdown_to_slides.py` - Main conversion engine
- `slides_api.py` - Google Slides API wrapper
- `config_manager.py` - Configuration and settings handler
- `template_manager.py` - Slide templates and styling
- `batch_converter.py` - Process multiple files at once

### **Configuration Files:**
- `templates.json` - Slide design templates and themes
- `drive_config.json` - Google Drive folder mappings
- `auth_config.json` - API authentication settings

### **Utilities:**
- `setup_auth.py` - Initial Google API authentication
- `test_conversion.py` - Test individual file conversions
- `batch_process.py` - Bulk process course materials

## 🎯 Key Features

### **Intelligent Parsing:**
- **Auto-detect slide breaks:** `---`, `## Slide N:`, or custom delimiters
- **Extract hierarchical content:** Titles, subtitles, bullet points, code blocks
- **Handle formatting:** Bold, italic, code, links, images
- **Preserve structure:** Nested lists, numbered items, emphasis

### **Professional Templates:**
- **Educational theme:** Clean, readable fonts and layouts
- **HKBU branding:** University colors and styling options
- **Flexible layouts:** Title slides, content slides, image slides, comparison slides
- **Consistent styling:** Automatic font sizing, spacing, and alignment

### **Google Integration:**
- **Direct API upload:** No intermediate PowerPoint files
- **Drive organization:** Automatic folder structure creation
- **Permission management:** Share with course team automatically
- **Version control:** Track changes and updates

### **Batch Processing:**
- **Course-wide conversion:** Process entire course material folders
- **Smart updates:** Only regenerate slides when source files change
- **Progress tracking:** Monitor conversion status and errors
- **Parallel processing:** Handle multiple presentations simultaneously

## 🚀 Usage Examples

### **Single File Conversion:**
```bash
python markdown_to_slides.py --input "Week2_Lecture_Slides.md" --template "educational" --drive-folder "GCAP3226/Lectures"
```

### **Batch Course Processing:**
```bash
python batch_converter.py --course-folder "/projects/GCAP3226/course_materials" --drive-base "GCAP3226"
```

### **Custom Template:**
```bash
python markdown_to_slides.py --input "presentation.md" --template-file "custom_template.json" --title "GCAP 3226 Week 2"
```

## 🔧 Setup Requirements

### **Google API Setup:**
1. Enable Google Slides API and Google Drive API
2. Create service account credentials
3. Share target Google Drive folders with service account email
4. Configure authentication in `auth_config.json`

### **Python Dependencies:**
- `google-api-python-client` - Google APIs integration
- `google-auth` - Authentication handling
- `markdown` - Markdown parsing
- `beautifulsoup4` - HTML/text processing
- `Pillow` - Image processing for slides
- `requests` - HTTP requests for remote images

### **Configuration:**
- Set up Google Drive folder structure
- Configure slide templates and themes
- Define course-specific settings and branding

## 📊 Supported Markdown Features

### **Slide Structure:**
```markdown
# Presentation Title

---

## Slide 1: Introduction
- Bullet point 1
- Bullet point 2

### Subsection
More detailed content

---

## Slide 2: Main Content
**Bold text** and *italic text*

1. Numbered list item
2. Another numbered item

`code snippets` and [links](https://example.com)
```

### **Advanced Features:**
- **Images:** `![alt text](image.png)` - Auto-resize and position
- **Code blocks:** ``` fenced code with syntax highlighting
- **Tables:** Markdown tables converted to slide tables
- **Math:** LaTeX math expressions (when supported)
- **Speaker notes:** Comments converted to slide notes

## 🎓 Educational Integration

### **Course Material Workflow:**
1. **Create markdown lecture notes** with slide-friendly structure
2. **Run conversion script** to generate Google Slides
3. **Auto-upload to course folder** in Google Drive
4. **Share with students** via automatic permissions
5. **Update slides** by re-running script on modified markdown

### **Template Customization:**
- **GCAP 3226 branding:** Course-specific colors and logos
- **Consistent styling:** Professional academic presentation format  
- **Content-aware layouts:** Different templates for different slide types
- **Responsive design:** Readable on projectors and mobile devices

## 📈 Benefits for Course Management

### **Efficiency:**
- **Time savings:** Generate slides in seconds, not hours
- **Consistency:** All presentations follow same professional format
- **Version control:** Track changes through markdown version control
- **Collaboration:** Multiple instructors can edit markdown simultaneously

### **Flexibility:**
- **Easy updates:** Modify markdown and regenerate slides instantly  
- **Multiple formats:** Same content can generate different slide styles
- **Reusability:** Templates work across different courses and topics
- **Integration:** Works with existing Google Drive course infrastructure

### **Quality:**
- **Professional appearance:** No more inconsistent manual formatting
- **Error reduction:** Automated processing reduces formatting mistakes
- **Accessibility:** Consistent styling improves readability
- **Standards compliance:** Follows educational presentation best practices

---

*This system transforms the tedious process of creating course presentations into an automated, efficient, and professional workflow that scales across entire academic programs.*

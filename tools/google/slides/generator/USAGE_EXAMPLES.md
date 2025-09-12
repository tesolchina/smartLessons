# GoogleSlidesGenerator - Practical Usage Examples
==================================================

## Quick Start with Week 2 Lecture Slides

### 1. Single File Conversion
```bash
cd /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleSlidesGenerator

# Convert Week 2 lecture slides
python3 markdown_to_slides.py ../Week2_Lecture_Slides.md \
    --template educational \
    --drive-folder "GCAP3226/Weekly Materials/Week 2" \
    --output-name "Week 2 - AI-Assisted Programming Lecture"
```

### 2. Test the System
```bash
# Quick test with Week 2
python3 test_system.py --week2-only

# Full test suite
python3 test_system.py
```

### 3. Batch Process Course Materials
```bash
# Process all markdown files in the course folder
python3 batch_converter.py \
    --course-folder "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating" \
    --drive-base "GCAP3226" \
    --template educational \
    --report batch_report.md
```

## Real Course Integration Examples

### Example 1: GCAP 3226 Weekly Materials
```bash
# Process Week 2 materials specifically
python3 batch_converter.py \
    --course-folder "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/course_materials/week2" \
    --drive-base "GCAP3226/Weekly Materials" \
    --template educational

# Result: All Week 2 markdown files → Google Slides in GCAP3226/Weekly Materials/Week 2/
```

### Example 2: Team Presentation Materials
```bash
# Convert team project templates to presentations
python3 markdown_to_slides.py "team_project_template.md" \
    --template gcap3226 \
    --drive-folder "GCAP3226/Team Resources" \
    --output-name "Team Project Template - Presentation"
```

### Example 3: Data Analysis Workshop
```bash
# Convert Week 2 data analysis guide
python3 markdown_to_slides.py "Week2_Student_Guide_Complete.md" \
    --template data_visualization \
    --drive-folder "GCAP3226/Weekly Materials/Week 2" \
    --output-name "Week 2 - Data Analysis Workshop"
```

## File Organization Examples

### Before Conversion
```
/operating/
├── Week2_Lecture_Slides.md
├── Week2_Student_Guide_Complete.md
├── course_materials/
│   ├── week2/
│   │   ├── lecture_notes.md
│   │   ├── workshop_guide.md
│   │   └── assignment_brief.md
│   └── week3/
│       └── materials.md
```

### After Batch Conversion
```
Google Drive: GCAP3226/
├── Weekly Materials/
│   ├── Week 2/
│   │   ├── Week 2 - AI-Assisted Programming Lecture.slides
│   │   ├── Week 2 - Data Analysis Workshop.slides
│   │   ├── Lecture Notes - Slides.slides
│   │   ├── Workshop Guide - Slides.slides
│   │   └── Assignment Brief - Slides.slides
│   └── Week 3/
│       └── Materials - Slides.slides
```

## Template Selection Guide

### Educational Template
- **Best for**: General lectures, course introductions
- **Features**: HKBU branding, clean layout, educational color scheme
- **Example**: Week 2 lecture slides
```bash
--template educational
```

### GCAP 3226 Template  
- **Best for**: Course-specific materials, team presentations
- **Features**: Course branding, consistent styling
- **Example**: Course overview, project templates
```bash
--template gcap3226
```

### Data Visualization Template
- **Best for**: Data analysis workshops, statistical presentations
- **Features**: Chart-friendly layouts, data-focused design
- **Example**: Week 2 data analysis materials
```bash
--template data_visualization
```

### Minimalist Template
- **Best for**: Simple presentations, quick overviews
- **Features**: Clean, distraction-free design
- **Example**: Quick team updates, announcements
```bash
--template minimalist
```

## Advanced Usage Patterns

### 1. Course-wide Batch Processing
```bash
# Process entire course with detailed reporting
python3 batch_converter.py \
    --course-folder "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating" \
    --drive-base "GCAP3226" \
    --template educational \
    --pattern "**/*_Slides.md" \
    --report "course_conversion_report.md"
```

### 2. Team-specific Processing
```bash
# Process materials for Team 1
python3 batch_converter.py \
    --course-folder "team_materials/team1" \
    --drive-base "GCAP3226/Teams/Team1" \
    --template gcap3226
```

### 3. Weekly Material Updates
```bash
# Update Week 2 materials
python3 batch_converter.py \
    --course-folder "week2_updates" \
    --drive-base "GCAP3226/Weekly Materials/Week 2" \
    --template educational \
    --pattern "*updated*.md"
```

## Integration with Existing GCAP 3226 System

### 1. Team Folder Integration
The system automatically integrates with your existing team structure:
- Team presentations → GCAP3226/Teams/[TeamName]/Presentations/
- Shared materials → GCAP3226/Shared Resources/Presentations/

### 2. Course Timeline Integration
Materials are organized by course timeline:
- Week 1-4: Foundation materials
- Week 5-8: Advanced topics  
- Week 9-12: Project presentations
- Week 13-15: Final presentations

### 3. Google Drive Sharing
All presentations inherit sharing settings from parent folders:
- Team folders: Restricted to team members + instructors
- Shared resources: All students + instructors
- Weekly materials: All course participants

## Troubleshooting Common Issues

### Authentication Problems
```bash
# Reset authentication
rm config/token.json
python3 setup_auth.py
```

### Template Issues
```bash
# Verify templates
python3 -c "import json; print(json.load(open('config/templates.json')).keys())"
```

### Drive Folder Issues  
```bash
# Test drive access
python3 test_system.py --auth-only
```

### Large File Processing
For large markdown files (>100 slides):
```bash
# Use chunked processing
python3 markdown_to_slides.py large_file.md --chunk-size 50
```

## Integration Commands

### Daily Workflow
```bash
# 1. Update lecture materials
python3 markdown_to_slides.py "today_lecture.md" --template educational

# 2. Process team submissions
python3 batch_converter.py --course-folder "submissions" --drive-base "GCAP3226/Submissions"

# 3. Generate weekly summary
python3 batch_converter.py --course-folder "week_summary" --template minimalist --report weekly_report.md
```

### Pre-class Setup
```bash
# Convert all materials for upcoming class
python3 batch_converter.py \
    --course-folder "next_class_materials" \
    --drive-base "GCAP3226/Weekly Materials/Week 3" \
    --template educational
```

This system seamlessly integrates with your existing GCAP 3226 course infrastructure, automatically organizing presentations in your established Google Drive structure while maintaining the professional educational standards your course requires.

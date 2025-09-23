# GCAP3226 Moodle Management System - Usage Guide

## 🚀 Quick Start

### Daily Workflow
1. **Generate a new post:** Use the template generator for consistent formatting
2. **Add forum link:** Register the new post in the links database  
3. **Update index:** Keep the master index current with new content

### Common Commands
```bash
# Generate a new assignment post
python automation_scripts/generate_post.py --category assignments --template reflective_essay --week 4

# Add the forum link to database
python automation_scripts/update_links.py --add --topic "Reflective Essay 1" --url "https://moodle..." --category assignment

# List all active assignments
python automation_scripts/update_links.py --list --filter-category assignment --filter-status active
```

---

## 📋 Template System

### Available Template Categories
- **📢 announcements/**: Course updates, deadline reminders, welcome messages
- **📝 assignments/**: Individual and group assignment instructions
- **🎯 projects/**: Multi-week project guidelines and timelines  
- **💬 discussions/**: Discussion starters and topic exploration
- **🤔 reflections/**: Personal reflection exercises and prompts

### Template Creation Guidelines

#### 1. HTML Structure
All templates follow a consistent structure:
```html
<div style="width: 100%; max-width: 1200px; margin: 0 auto; font-family: Arial, sans-serif;">
  <!-- Header with course branding -->
  <div style="background-color: #4a90e2; color: #ffffff; padding: 30px;">
    <h1>{TITLE}</h1>
  </div>
  
  <!-- Content sections with distinct styling -->
  <div style="background-color: #e8f5e8; padding: 25px;">
    <!-- Content goes here -->
  </div>
</div>
```

#### 2. Parameter Placeholders
Use `{PARAMETER_NAME}` format for dynamic content:
- `{COURSE_CODE}` → GCAP 3226
- `{DUE_DATE}` → Friday, Week 5
- `{AI_TUTOR_URL}` → https://smartlessons.hkbu.tech/...
- `{WHATSAPP_GROUP_URL}` → https://chat.whatsapp.com/...

#### 3. Color Scheme
Maintain consistent branding:
- **Primary Blue:** `#4a90e2` (headers)
- **Success Green:** `#28a745` (positive actions)
- **Warning Yellow:** `#ffc107` (important notices)
- **Info Blue:** `#17a2b8` (instructions)
- **Danger Red:** `#dc3545` (deadlines, rules)

### Creating New Templates

#### Step 1: Design the Template
1. Copy an existing template from the same category
2. Modify content sections as needed
3. Add appropriate parameter placeholders
4. Test with sample data

#### Step 2: Save with Standard Naming
```
templates/{category}/{template_name}_template.html
```

#### Step 3: Create Sample Configuration
```bash
python automation_scripts/generate_post.py --category {category} --template {template_name} --create-sample-config
```

#### Step 4: Test Generation
```bash
python automation_scripts/generate_post.py --category {category} --template {template_name} --config sample_config.json
```

---

## 🔗 Link Management System

### Database Structure
Forum links are stored in CSV format with these fields:
- **Course Title**: Always "GCAP3226"
- **Forum Type**: discussion, assignment, project, announcement
- **Week**: Week number or range (e.g., "4", "3-11")
- **Topic**: Descriptive title
- **Description**: Detailed explanation
- **Moodle URL**: Full forum URL
- **Creation Date**: Auto-generated timestamp
- **Status**: active, planned, archived, draft
- **Category**: assignment, discussion, project, announcement, reflection
- **Tags**: Semicolon-separated keywords

### Adding New Links

#### Method 1: Command Line
```bash
python automation_scripts/update_links.py --add \
  --topic "Week 5 Discussion: Ethics in Data Analysis" \
  --url "https://moodle.hkbu.edu.hk/mod/forum/view.php?id=12345" \
  --category discussion \
  --description "Explore ethical considerations in data collection and analysis" \
  --week 5 \
  --status active \
  --tags "ethics;data_analysis;discussion"
```

#### Method 2: Direct CSV Edit
Edit `links_database/forum_links.csv` directly for bulk additions.

### Searching and Filtering
```bash
# Search by keyword
python automation_scripts/update_links.py --search "reflection"

# Filter by category
python automation_scripts/update_links.py --list --filter-category assignment

# Filter by status
python automation_scripts/update_links.py --list --filter-status planned

# Multiple filters
python automation_scripts/update_links.py --list --filter-category project --filter-week "3-11"
```

### Exporting Links
```bash
# Export as HTML webpage
python automation_scripts/update_links.py --export --format html --open

# Export as JSON for backup
python automation_scripts/update_links.py --export --format json

# Export as Markdown for documentation
python automation_scripts/update_links.py --export --format markdown
```

---

## 📊 Content Organization

### Weekly Structure
Content is organized by academic weeks:
```
forum_posts/
├── week01/    # Course introduction
├── week02/    # Data sources exploration  
├── week03/    # Topic selection
├── week04/    # Reflective essays
├── week05/    # Group formation
...
├── week11/    # Final presentations
```

### Naming Conventions

#### Templates
```
{category}/{descriptive_name}_template.html
```
Examples:
- `assignments/reflective_essay_template.html`
- `projects/timeline_template.html`
- `announcements/weekly_update_template.html`

#### Generated Posts
```
week{XX}/{template_name}_week{XX}.html
```
Examples:
- `week04/reflective_essay_week04.html`
- `week05/group_formation_week05.html`

#### Configuration Files
```
configs/{category}_{template}_{purpose}.json
```
Examples:
- `configs/assignments_reflective_essay_week4.json`
- `configs/projects_timeline_full_semester.json`

---

## ⚙️ Automation Scripts

### generate_post.py

#### Purpose
Generate Moodle forum posts from HTML templates with parameter substitution.

#### Key Features
- Template validation and placeholder detection
- Automatic parameter substitution
- Week-based organization
- Sample configuration generation

#### Usage Examples
```bash
# Basic generation
python generate_post.py --category assignments --template reflective_essay --week 4

# With custom configuration
python generate_post.py --category projects --template timeline --config custom_config.json

# List available templates
python generate_post.py --list-templates

# Create sample configuration
python generate_post.py --category assignments --template individual --create-sample-config

# Validate template
python generate_post.py --category discussions --template topic_exploration --validate
```

### update_links.py

#### Purpose
Manage the forum links database with CRUD operations and reporting.

#### Key Features
- Add/update/delete forum links
- Search and filtering capabilities
- Export in multiple formats
- Link validation
- Category management

#### Usage Examples
```bash
# Add new link
python update_links.py --add --topic "New Discussion" --url "https://..." --category discussion

# List all links
python update_links.py --list

# Search functionality
python update_links.py --search "essay"

# Export and view
python update_links.py --export --format html --open

# Validate all links
python update_links.py --validate-links
```

---

## 🎨 Styling Guidelines

### Visual Hierarchy
1. **Headers**: Large, bold, with background colors
2. **Sections**: Distinct background colors and borders
3. **Instructions**: Numbered steps with clear formatting
4. **Important Info**: Highlighted boxes with warning colors

### Responsive Design
- Maximum width: 1200px
- Font size: 18px base with relative scaling
- Mobile-friendly spacing and layout

### Accessibility
- High contrast color combinations
- Descriptive alt text for images
- Semantic HTML structure
- Clear navigation patterns

---

## 📈 Quality Assurance

### Template Validation Checklist
- [ ] All placeholders follow `{PARAMETER_NAME}` format
- [ ] HTML tags are properly closed
- [ ] Colors match brand guidelines
- [ ] Responsive design elements included
- [ ] Accessibility standards met
- [ ] Links are functional

### Content Review Process
1. **Generate** post using template
2. **Review** content for accuracy and completeness
3. **Test** all links and functionality
4. **Validate** HTML structure
5. **Add** to links database
6. **Update** master index

### Maintenance Schedule
- **Weekly**: Update current week content
- **Bi-weekly**: Validate all external links
- **Monthly**: Review and update templates
- **Semester**: Archive old content, prepare new structure

---

## 🔧 Troubleshooting

### Common Issues

#### Template Generation Fails
```bash
# Check template exists
ls templates/{category}/{template}_template.html

# Validate template
python generate_post.py --category {category} --template {template} --validate

# Check placeholders
grep -o '{[A-Z_]*}' templates/{category}/{template}_template.html
```

#### Links Database Corruption
```bash
# Backup current database
cp links_database/forum_links.csv links_database/forum_links_backup.csv

# Validate CSV format
python -c "import csv; csv.DictReader(open('links_database/forum_links.csv'))"

# Regenerate from backup if needed
```

#### Missing Parameters
1. Check the sample configuration file
2. Verify all placeholders in template
3. Add missing parameters to config
4. Regenerate post

### Error Messages

#### "Template not found"
- Verify template filename and location
- Check category spelling
- Ensure `_template.html` suffix

#### "Parameter not substituted"
- Add missing parameter to configuration
- Check placeholder format `{PARAMETER_NAME}`
- Verify parameter case sensitivity

#### "Link already exists"
- Check existing links database
- Update existing link instead of adding new
- Verify URL uniqueness

---

## 📚 Advanced Usage

### Batch Operations
```bash
# Generate multiple weeks
for week in {4..8}; do
  python generate_post.py --category assignments --template weekly_exercise --week $week
done

# Export multiple formats
for format in html json markdown; do
  python update_links.py --export --format $format
done
```

### Custom Configurations
Create reusable configuration files for complex templates:

```json
{
  "COURSE_CODE": "GCAP 3226",
  "ASSIGNMENT_TITLE": "Policy Analysis Report",
  "WORD_COUNT": "2000-2500",
  "DUE_DATE": "Friday, Week 10",
  "RUBRIC_CRITERIA": [
    "Research Quality",
    "Analysis Depth", 
    "Writing Clarity",
    "Formatting"
  ],
  "AI_SUPPORT": true,
  "GROUP_WORK": false
}
```

### Integration with Other Tools
- **GitHub**: Version control for template changes
- **Moodle API**: Automated post publishing (future enhancement)
- **Analytics**: Track engagement with generated content
- **Calendar**: Sync due dates and schedules

---

## 🎯 Best Practices

### Content Creation
1. **Start with existing templates** - Don't reinvent the wheel
2. **Use consistent branding** - Maintain professional appearance
3. **Include clear instructions** - Students should understand expectations
4. **Provide support resources** - Link to AI tutors, office hours, etc.
5. **Test before publishing** - Verify all links and functionality

### Database Management
1. **Regular backups** - Export database weekly
2. **Consistent categorization** - Use predefined categories
3. **Descriptive titles** - Make content easily searchable
4. **Update status** - Keep link status current
5. **Tag appropriately** - Use relevant, searchable tags

### System Maintenance
1. **Monitor disk space** - Generated files can accumulate
2. **Update dependencies** - Keep Python packages current
3. **Review templates** - Update content based on feedback
4. **Archive old content** - Move completed semester materials
5. **Document changes** - Track modifications and improvements

---

**📞 Support & Questions**

For technical issues or questions about the Moodle management system:
- Check this documentation first
- Review error messages and troubleshooting section
- Contact system administrator
- Submit enhancement requests via GitHub issues

**🔄 System Status**: ✅ Operational  
**📊 Last Updated**: December 23, 2024
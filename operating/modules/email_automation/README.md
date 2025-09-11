# Email Automation Module

## Purpose
Automate email processing, drafting, and communication workflows across projects.

## Features
- **Email Extraction**: Extract emails from local Outlook by keywords
- **Draft Management**: Organize and template email drafts
- **Cross-Platform Sending**: AppleScript (macOS) and PowerShell (Windows) integration
- **Template System**: Reusable email templates for common tasks

## Usage

### Extract Project Emails
```bash
# Extract emails related to specific project
python3 modules/email_automation/email_retrieval_script.py

# Customize keywords in the script for different projects
```

### Email Drafts
- **Location**: `modules/email_automation/email_drafts/`
- **Templates**: Store reusable email templates
- **Project Drafts**: Organize by project or category

### Integration Examples
```bash
# From screening test project
cd projects/screening_test/
python3 ../../modules/email_automation/email_retrieval_script.py

# Results saved to project's documentation folder
```

## Files
- `email_retrieval_script.py` - Extract emails from Outlook
- `email_drafts/` - Draft storage and templates
- `README.md` - This documentation

## Configuration
- **Keywords**: Customize in email_retrieval_script.py
- **Output Format**: Markdown summaries
- **Email Client**: Microsoft Outlook (macOS)

## Future Enhancements
- [ ] Gmail API integration
- [ ] Automated draft generation with AI
- [ ] Email scheduling functionality
- [ ] Template-based sending
- [ ] Multi-platform client support

## Templates Available
- Plain email draft template
- Website update tracking
- Project communication templates

---
*Module: Email Automation | Updated: September 6, 2025*

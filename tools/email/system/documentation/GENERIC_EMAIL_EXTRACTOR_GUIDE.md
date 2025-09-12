# Generic Email Extractor Usage Guide

## Overview
The Generic Email Extractor is a flexible tool that can extract emails based on various criteria and save them to any project folder. It's perfect for collecting emails related to specific projects, courses, or topics.

## Features
✅ **Flexible Search** - Search by keywords, sender, date, mailboxes  
✅ **Multi-Project Support** - Save to any project folder  
✅ **Structured Output** - Organized markdown files with metadata  
✅ **Summary Reports** - Automatic extraction summaries  
✅ **Extraction Logging** - Track all extractions in JSON log  
✅ **Safe Filenames** - Automatic sanitization of subject lines

## Quick Examples

### Extract LANG2077 Service Learning Emails
```bash
# Search for service learning emails and save to LANG2077 project
python3 operating/email_automation/generic_email_extractor.py \
    --keywords "service learning" "departmental meeting" "LANG2077" \
    --project-path "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG2077" \
    --filename-prefix "service_learning" \
    --max-results 5
```

### Extract Emails from Specific Sender
```bash
# Get all emails from a specific person
python3 operating/email_automation/generic_email_extractor.py \
    --sender "hermine_chan@hkbu.edu.hk" \
    --project-path "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/admin" \
    --filename-prefix "hermine_emails"
```

### Extract Screening Test Communications
```bash
# Find screening test related emails
python3 operating/email_automation/generic_email_extractor.py \
    --keywords "screening test" "test-taker" "ui testing" \
    --project-path "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/screening_test/emails" \
    --filename-prefix "screening_communications"
```

### Extract Goal-Setting Chatbot Research Emails
```bash
# Technical team communications
python3 operating/email_automation/generic_email_extractor.py \
    --keywords "chatbot" "chat history" "junxin" "data request" \
    --project-path "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/goal-setting-chatbot-paper/communications" \
    --filename-prefix "technical_emails"
```

## Command Line Options

### Required
- `--project-path`: Path where emails will be saved

### Search Filters
- `--keywords`: List of keywords to search for in subject/content  
- `--sender`: Filter by sender email or name
- `--mailboxes`: Mailboxes to search (default: INBOX Exchange)

### Output Options
- `--filename-prefix`: Prefix for saved files (default: extracted_emails)
- `--max-results`: Maximum emails to extract (default: 10)

## Output Structure

### Individual Email Files
Each email is saved as: `{prefix}_{timestamp}_{number}_{subject}.md`

Example: `service_learning_20250906_143022_01_Departmental_Meeting_New_Service.md`

### Summary File
Overall summary: `{prefix}_{timestamp}_SUMMARY.md`

Contains:
- Extraction metadata
- List of all found emails
- Files created

### Extraction Log
Global log: `operating/email_automation/extraction_log.json`

Tracks all extractions for reference.

## Integration Examples

### Use with Existing Projects

```bash
# For ongoing projects, extract new emails periodically
python3 operating/email_automation/generic_email_extractor.py \
    --keywords "project update" \
    --project-path "/path/to/project/communications" \
    --max-results 20
```

### Batch Extract Multiple Topics
```bash
# Extract multiple email types to different projects
./extract_all_projects.sh  # Custom script calling generic_email_extractor.py
```

## Advanced Usage

### Search Multiple Mailboxes
```bash
python3 operating/email_automation/generic_email_extractor.py \
    --keywords "research" \
    --mailboxes "INBOX" "Archive" "Sent" \
    --project-path "/path/to/project"
```

### Large Scale Extraction
```bash
# Extract many emails (increase max-results)
python3 operating/email_automation/generic_email_extractor.py \
    --keywords "course" "student" \
    --max-results 50 \
    --project-path "/path/to/teaching/emails"
```

## Tips for Effective Use

1. **Use Specific Keywords**: Better results with specific terms
2. **Start Small**: Use low max-results first to test
3. **Check Summaries**: Review summary files before processing
4. **Organize by Project**: Use clear project paths and prefixes
5. **Regular Extraction**: Run periodically for ongoing projects

## Error Handling

- If no emails found, clear message is displayed
- AppleScript errors are captured and reported
- File creation errors are handled gracefully
- All operations are logged for debugging

This generic extractor replaces project-specific extractors and provides a unified interface for all email extraction needs!

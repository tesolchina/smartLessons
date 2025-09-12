# Generic Email Sender - Usage Guide

## Overview
A flexible email automation system for Mac Mail.app with two main components:

1. **`generic_email_sender.py`** - Core email sending functionality
2. **`send_draft_email.py`** - Parser for markdown email drafts

## Quick Start

### Send Sophie's Sick Leave Response
```bash
# Navigate to project directory
cd /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant

# Send the draft (will prompt for Sophie's email)
python3 operating/email_automation/send_draft_email.py operating/email_automation/email_drafts/draft_sophie_sick_leave_response.md

# Or specify recipient directly
python3 operating/email_automation/send_draft_email.py operating/email_automation/email_drafts/draft_sophie_sick_leave_response.md --to sophie@example.com
```

## Core Email Sender Usage

### Command Line Interface
```bash
# Basic email
python3 operating/email_automation/generic_email_sender.py \
    --to recipient@example.com \
    --subject "Test Subject" \
    --body "Test message content"

# Email with CC and BCC
python3 operating/email_automation/generic_email_sender.py \
    --to recipient1@example.com recipient2@example.com \
    --cc cc@example.com \
    --bcc bcc@example.com \
    --subject "Meeting Reminder" \
    --body "Don't forget about tomorrow's meeting"

# Auto-send without manual review
python3 operating/email_automation/generic_email_sender.py \
    --to recipient@example.com \
    --subject "Automated Message" \
    --body "This will send automatically" \
    --auto-send

# Read body from file
python3 operating/email_automation/generic_email_sender.py \
    --to recipient@example.com \
    --subject "File Content" \
    --body-file path/to/content.txt
```

### Python API Usage
```python
from generic_email_sender import EmailSender

sender = EmailSender()

# Simple email
sender.send_email(
    to_addresses=["recipient@example.com"],
    subject="Test Subject",
    body="Test message"
)

# Complex email
sender.send_email(
    to_addresses=["recipient1@example.com", "recipient2@example.com"],
    subject="Important Update",
    body="This is the message content",
    cc_addresses=["cc@example.com"],
    bcc_addresses=["bcc@example.com"],
    auto_send=False  # Opens for review
)
```

## Draft Email Format

Email drafts should follow this markdown format:

```markdown
# Email Draft - Title

**To**: Recipient Name/Description
**Subject**: Email Subject Line
**Date**: Creation Date
**Status**: DRAFT

---

## Email Content

Your email content here...

---

## Notes
Additional notes for reference
```

## Features

### Email Logging
- All emails are logged to `sent_emails_log.json`
- Includes timestamp, recipients, subject, and body preview
- Tracks whether email was auto-sent or manually reviewed

### Security
- Emails open for manual review by default
- Use `--auto-send` flag only when confident
- AppleScript integration requires Mail.app permissions

### Error Handling
- Timeout protection (60 seconds)
- Proper error reporting
- Graceful handling of Mail.app issues

## Common Use Cases

### Daily Assistant Tasks
1. **Student Communications**: Sick leave responses, grade notifications
2. **Administrative Emails**: Meeting reminders, policy updates  
3. **Bulk Communications**: Class announcements, newsletter distribution
4. **Template Responses**: FAQ replies, standard procedures

### Integration Examples
```bash
# Send weekly bulletin
python3 operating/email_automation/generic_email_sender.py \
    --to class-list@university.edu \
    --subject "Weekly Bulletin - $(date +%Y-%m-%d)" \
    --body-file bulletins/weekly_$(date +%Y%m%d).txt

# Emergency notification
python3 operating/email_automation/generic_email_sender.py \
    --to all-students@university.edu \
    --subject "URGENT: Class Cancellation" \
    --body "Due to weather conditions, today's classes are cancelled." \
    --auto-send
```

## Troubleshooting

### Common Issues
1. **Permission Denied**: Ensure Mail.app has Automation permissions
2. **Timeout Errors**: Close other applications, restart Mail.app
3. **Script Hangs**: Check Mail.app isn't showing modal dialogs

### Debug Commands
```bash
# Test Mail.app connectivity
osascript -e 'tell application "Mail" to get name of account 1'

# List available accounts
python3 -c "
import subprocess
result = subprocess.run(['osascript', '-e', 'tell application \"Mail\" to get name of every account'], capture_output=True, text=True)
print('Accounts:', result.stdout)
"
```

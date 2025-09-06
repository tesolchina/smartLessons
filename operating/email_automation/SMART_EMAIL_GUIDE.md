# Smart Email Handler Usage Guide

## Overview
The Smart Email Handler provides automated workflows for replying to emails and archiving them automatically, eliminating manual confirmation steps.

## Key Features
✅ **Find and Reply** - Find emails by subject, reply, and archive original  
✅ **Quick Reply** - Reply to latest email and archive  
✅ **Auto-Send** - No manual confirmation required  
✅ **Auto-Archive** - Original emails archived after reply  
✅ **Action Logging** - Track all email actions

## Usage Examples

### 1. Reply to Specific Email by Subject
```bash
# Find email with "Screening Test" in subject, reply, and archive
python3 operating/email_automation/smart_email_handler.py \
    --action reply \
    --subject-search "Screening Test" \
    --reply-subject "Re: Screening Test - Completed" \
    --reply-body "Thank you for your message. The screening test has been completed successfully."
```

### 2. Quick Reply to Latest Email
```bash
# Reply to most recent email in inbox and archive it
python3 operating/email_automation/smart_email_handler.py \
    --action quick-reply \
    --reply-subject "Quick Response" \
    --reply-body "Thank you for your email. I will review and get back to you soon."
```

### 3. Quick Reply with Sender Filter
```bash
# Reply only to emails from specific sender
python3 operating/email_automation/smart_email_handler.py \
    --action quick-reply \
    --reply-subject "Response to Sophie" \
    --reply-body "Thank you Sophie. Please refer to the course document for details." \
    --sender-filter "sophie"
```

### 4. Archive Email Only
```bash
# Just archive an email without replying
python3 operating/email_automation/smart_email_handler.py \
    --action archive \
    --subject-search "Old Meeting Notes"
```

## Common Workflows

### Sophie Sick Leave Response
```bash
python3 operating/email_automation/smart_email_handler.py \
    --action reply \
    --subject-search "sick leave" \
    --reply-subject "Re: Sick Leave - UE1 Section 37" \
    --reply-body "Thank you for letting me know, Sophie. Please rest well and recover soon. 

Please refer to our course document: https://docs.google.com/document/d/1efLZhPk1i5Hdlg2rQ2vfoR-ccFUMkJkYSj7rPSVSXNU/edit

Don't forget the pre-course writing test is due September 12th.

Best regards"
```

### Technical Team Data Request Follow-up
```bash
python3 operating/email_automation/smart_email_handler.py \
    --action reply \
    --subject-search "chat history" \
    --reply-subject "Re: Chat History Data - Follow Up" \
    --reply-body "Thank you for your response. Please let me know if you need any additional information about our research requirements."
```

## Action Logging
All actions are logged to: `operating/email_automation/email_actions_log.md`

## Error Handling
- If email not found, operation stops with error message
- If Mail.app is not accessible, clear error reporting
- All actions are logged for debugging

## Integration with Existing System
Works seamlessly with your existing:
- `generic_email_sender.py` - For standalone sending
- `send_draft_email.py` - For markdown draft processing  
- `quick_send.py` - For menu-driven sending

The Smart Email Handler adds **reply-and-archive workflow** to your email automation toolkit!

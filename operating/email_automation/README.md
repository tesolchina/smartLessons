# Email Automation System

A comprehensive, organized email workflow system for Mac Mail.app automation.

## 📁 Directory Structure

```
email_automation/
├── email_workflow.py          # 🎯 MAIN UNIFIED WORKFLOW TOOL
├── core_tools/                # 🔧 General-purpose email tools
├── specialized_scripts/       # 🎯 Task-specific scripts (archived)
├── documentation/             # 📚 Guides and documentation  
├── contacts/                  # 👥 Contact management
├── logs/                     # 📊 Activity logs
└── archive/                  # 🗄️ Deprecated scripts
```

## 🚀 Quick Start

### Primary Tool: Email Workflow System

```bash
python3 email_workflow.py
```

This is your main interface for all email operations:

- **Locate emails** by subject, sender, or content
- **Reply** with proper email threading
- **Forward emails** to contacts
- **Archive emails** automatically  
- **Manage contacts** database
- **Track activity** with logging

### Core Features

1. **📧 Email Location & Search**
   - Find emails by subject line
   - Search by sender name/email
   - Full-text content search
   - Multi-mailbox support

2. **🔄 Email Actions**
   - Reply with threading
   - Reply-all functionality
   - Forward with custom messages
   - Archive to proper folders

3. **👥 Contact Management**
   - Organized contact database
   - Categories: colleagues, students, recent
   - Smart contact search
   - Auto-population from emails

4. **📊 Activity Tracking**
   - All actions logged
   - Success/failure tracking
   - Email history preservation

## 🔧 Core Tools (For Advanced Users)

### Generic Email Tools

- `generic_email_sender.py` - Send emails with full configuration
- `email_reply_system.py` - Handle replies with proper threading  
- `email_address_extractor.py` - Extract and manage email addresses
- `generic_email_extractor.py` - Advanced email search and extraction
- `smart_email_handler.py` - Automated email operations

### Email Workflow Tools

- `send_draft_email.py` - Send pre-written drafts
- `quick_send.py` - Quick send menu system
- `forward_and_archive.py` - Forward and file emails
- `mail_app_retrieval.py` - Comprehensive email retrieval

### Diagnostic Tools

- `debug_inbox.py` - Troubleshoot mailbox issues
- `mailbox_discovery.py` - Explore account structure
- `account_mailbox_check.py` - Verify account access

## 🎯 Use Cases

### Daily Email Management
```bash
python3 email_workflow.py
# Follow menu to locate, reply, forward, or archive emails
```

### Contact Database
The system automatically maintains a contact database in `contacts/email_contacts.json`:

```json
{
  "colleagues": [
    {"name": "Nancy", "email": "nancymak@hkbu.edu.hk", "department": "Language Centre"},
    {"name": "Joshua", "email": "joshuachan@hkbu.edu.hk", "department": "Language Centre"}
  ],
  "students": [],
  "recent": []
}
```

### Typical Workflow
1. **Locate** an email: "Departmental Meeting"
2. **Reply** with your response  
3. **Add contacts** from the email
4. **Archive** the processed email
5. **Track** all actions in logs

## 📚 Documentation

- `README.md` - This file
- `EMAIL_SENDER_GUIDE.md` - Detailed sending instructions
- `SMART_EMAIL_GUIDE.md` - Advanced automation features
- `GENERIC_EMAIL_EXTRACTOR_GUIDE.md` - Email extraction documentation
- `mail_app_setup_guide.md` - Mac Mail.app configuration
- `progressonEmail.md` - Development history
- `email_actions_log.md` - Action tracking examples

## 🗄️ Specialized Scripts (Archived)

These scripts are kept for reference but are specialized for particular tasks:

- `lang2077_specific_extractor.py` - LANG2077 course email extraction
- `screening_test_email_extractor.py` - Screening test email processing
- `auto_send_service_learning.py` - Automated service learning replies
- `service_learning_email_search.py` - Service learning email finder
- `send_sophie_email.py` - Sophie-specific email automation

## 🔒 Security & Privacy

- All email processing happens locally
- No cloud services or external APIs
- Uses Mac Mail.app's native AppleScript interface
- Contact database stored locally in JSON format
- Activity logs contain no email content, only metadata

## 🛠️ Requirements

- macOS with Mail.app configured
- Python 3.6+
- AppleScript support (built into macOS)
- Email accounts configured in Mail.app

## 📊 Activity Logging

All email operations are logged to `logs/` directory:
- `sent_emails_log.json` - Sent email tracking
- `focused_extraction_log.txt` - Email extraction history

## 🎯 Migration from Old System

If upgrading from the previous messy folder structure:

1. **Use `email_workflow.py`** for all new email operations
2. **Check `specialized_scripts/`** if you need old functionality  
3. **Import contacts** from previous email interactions
4. **Review `documentation/`** for guides and setup

## 💡 Tips for Effective Use

1. **Start with the main workflow tool** - covers 90% of email needs
2. **Build your contact database** - makes future emails faster  
3. **Use descriptive search terms** - improves email location accuracy
4. **Archive processed emails** - keeps inbox clean
5. **Check logs periodically** - verify operations completed successfully

## 🚨 Troubleshooting

**Email not found?**
- Check spelling in search terms
- Try searching by sender instead of subject
- Use `debug_inbox.py` to verify mailbox access

**Script permissions?**
- Enable AppleScript access for Terminal in System Preferences
- Grant Mail.app automation permissions
- Check Mail.app is running and responsive

**Contact database issues?**
- Delete `contacts/email_contacts.json` to reset
- Check JSON syntax if manually edited
- Restart the workflow tool

---

## 📞 Support

This system was designed for clean, efficient email workflow management. For issues:

1. Check the troubleshooting section above
2. Review documentation in `documentation/` folder  
3. Use diagnostic tools in `core_tools/` for debugging
4. Check activity logs in `logs/` for operation history

**Last Updated**: September 6, 2025
**Version**: 2.0 - Reorganized and Unified System

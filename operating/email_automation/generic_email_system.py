#!/usr/bin/env python3
"""
Generic Email Draft and Send System
1. Creates markdown draft for review
2. Converts to rich text and sends via Mail.app after confirmation
3. Ensures clickable links and removes markdown formatting
"""

import subprocess
import os
import re
from datetime import datetime
from pathlib import Path

class EmailDraftSystem:
    def __init__(self, project_folder=None):
        """Initialize email system with project folder for drafts"""
        self.project_folder = project_folder or os.getcwd()
        self.draft_folder = os.path.join(self.project_folder, "email_drafts")
        os.makedirs(self.draft_folder, exist_ok=True)
        
    def create_draft(self, recipient, subject, content, draft_name=None):
        """Create markdown email draft for review"""
        if not draft_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            draft_name = f"draft_{timestamp}"
            
        draft_file = os.path.join(self.draft_folder, f"{draft_name}.md")
        
        # Create markdown draft with metadata
        draft_content = f"""# Email Draft - {draft_name}

## Email Metadata
- **To:** {recipient}
- **Subject:** {subject}
- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Status:** DRAFT (Not sent)

---

## Email Content

{content}

---

## Instructions
1. Review the email content above
2. Edit if needed
3. Run: `python3 generic_email_system.py --send "{draft_name}"`
4. Or use the send_draft() method in code

## Notes
- Links will be made clickable automatically
- Markdown formatting will be converted to rich text
- No # symbols will appear in final email
"""
        
        with open(draft_file, 'w', encoding='utf-8') as f:
            f.write(draft_content)
            
        print(f"📝 Email draft created: {draft_file}")
        print(f"📋 Review and edit the draft, then run:")
        print(f"   python3 generic_email_system.py --send \"{draft_name}\"")
        
        return draft_file
    
    def send_draft(self, draft_name):
        """Send email from approved markdown draft"""
        draft_file = os.path.join(self.draft_folder, f"{draft_name}.md")
        
        if not os.path.exists(draft_file):
            print(f"❌ Draft file not found: {draft_file}")
            return False
            
        # Parse draft file
        metadata, content = self._parse_draft_file(draft_file)
        
        if not metadata:
            print("❌ Could not parse draft metadata")
            return False
            
        # Convert markdown to rich text for email
        email_content = self._convert_to_email_format(content)
        
        # Send via Mail.app
        success = self._send_via_mail_app(
            metadata['recipient'], 
            metadata['subject'], 
            email_content
        )
        
        if success:
            # Update draft status
            self._mark_draft_as_sent(draft_file)
            self._log_email_send(metadata['recipient'], metadata['subject'], draft_name)
            
        return success
    
    def _parse_draft_file(self, draft_file):
        """Parse metadata and content from draft file"""
        try:
            with open(draft_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract metadata
            metadata = {}
            lines = content.split('\n')
            
            for line in lines:
                if line.startswith('- **To:**'):
                    metadata['recipient'] = line.split('**To:**')[1].strip()
                elif line.startswith('- **Subject:**'):
                    metadata['subject'] = line.split('**Subject:**')[1].strip()
                    
            # Extract email content between "## Email Content" and "---"
            content_start = content.find('## Email Content\n') + len('## Email Content\n')
            content_end = content.find('\n---\n', content_start)
            
            if content_start > 0 and content_end > 0:
                email_content = content[content_start:content_end].strip()
                return metadata, email_content
            else:
                return None, None
                
        except Exception as e:
            print(f"❌ Error parsing draft: {e}")
            return None, None
    
    def _convert_to_email_format(self, markdown_content):
        """Convert markdown to email-friendly rich text"""
        # Remove markdown headers (# ## ###)
        content = re.sub(r'^#+\s*', '', markdown_content, flags=re.MULTILINE)
        
        # Convert markdown bold (**text**) to plain text (keep emphasis)
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
        
        # Convert markdown links [text](url) to just text with URL
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1\n\2', content)
        
        # Remove any remaining markdown formatting
        content = content.replace('*', '')
        content = content.replace('_', '')
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)
        content = content.strip()
        
        return content
    
    def _send_via_mail_app(self, recipient, subject, content):
        """Send email using macOS Mail.app"""
        # Escape quotes for AppleScript
        subject_escaped = subject.replace('"', '\\"')
        content_escaped = content.replace('"', '\\"').replace('\n', '\\n')
        recipient_escaped = recipient.replace('"', '\\"')
        
        applescript = f'''
        tell application "Mail"
            activate
            set newMessage to make new outgoing message with properties {{subject:"{subject_escaped}", content:"{content_escaped}"}}
            tell newMessage
                make new to recipient with properties {{address:"{recipient_escaped}"}}
            end tell
            send newMessage
        end tell
        '''
        
        try:
            print("📧 Sending email via Mail.app...")
            print(f"   To: {recipient}")
            print(f"   Subject: {subject}")
            
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, check=True)
            
            print("✅ Email sent successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error sending email: {e}")
            print(f"   Error output: {e.stderr}")
            return False
    
    def _mark_draft_as_sent(self, draft_file):
        """Update draft file to mark as sent"""
        try:
            with open(draft_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Update status line
            content = content.replace(
                '- **Status:** DRAFT (Not sent)',
                f'- **Status:** SENT ({datetime.now().strftime("%Y-%m-%d %H:%M:%S")})'
            )
            
            with open(draft_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"📝 Draft marked as sent: {draft_file}")
            
        except Exception as e:
            print(f"⚠️  Could not update draft status: {e}")
    
    def _log_email_send(self, recipient, subject, draft_name):
        """Log email send details"""
        log_file = os.path.join(self.project_folder, "email_log.md")
        
        log_entry = f"""
## Email Sent - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**To:** {recipient}
**Subject:** {subject}
**Draft:** {draft_name}
**Method:** Mail.app via AppleScript
**Status:** Sent successfully

---
"""
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            print(f"📝 Email logged to: {log_file}")
        except Exception as e:
            print(f"⚠️  Could not write to log: {e}")

def main():
    """Main function for command line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generic Email Draft and Send System')
    parser.add_argument('--draft', help='Create email draft')
    parser.add_argument('--send', help='Send email from draft name')
    parser.add_argument('--recipient', help='Email recipient')
    parser.add_argument('--subject', help='Email subject')
    parser.add_argument('--content', help='Email content')
    parser.add_argument('--project', help='Project folder path', 
                       default='/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/RefLetter')
    
    args = parser.parse_args()
    
    email_system = EmailDraftSystem(args.project)
    
    if args.send:
        print(f"📧 Sending draft: {args.send}")
        success = email_system.send_draft(args.send)
        if not success:
            exit(1)
    elif args.draft:
        if not all([args.recipient, args.subject, args.content]):
            print("❌ --recipient, --subject, and --content required for draft creation")
            exit(1)
        email_system.create_draft(args.recipient, args.subject, args.content, args.draft)
    else:
        print("Use --draft to create draft or --send to send existing draft")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Email notification script to inform Yanbo about the reference letter Google Doc
Uses macOS Mail.app via osascript for rich text email
"""

import subprocess
import os
from datetime import datetime

def send_mail_via_applescript():
    """Send email using macOS Mail.app with AppleScript"""
    
    # Email details
    recipient = "22258221@life.hkbu.edu.hk"
    subject = "Reference Letter Google Doc - Please Add Your Input"
    
    # Rich text email content
    email_body = """Hi Yanbo,

I hope this email finds you well. I've created a Google Doc for your reference letter for the UST Science Leadership & Entrepreneurship program application.

📄 **Google Doc Access:**
You should have received an email invitation to edit the document. Please click on the link to access it directly, or use this URL:
https://docs.google.com/document/d/1lSa8N__d4JSJVbsUOPPlF2oApTc5EvSOOCEz4glUQtQ/edit

📝 **What I need from you:**
1. **Add specific examples** of leadership roles and collaborative projects you've been involved in
2. **Include program details** - research the UST Science Leadership & Entrepreneurship program and add key information about:
   - Program objectives and focus areas
   - Why this program aligns with your career goals
   - Specific skills or experiences they value
3. **Provide concrete examples** of your organizational skills and work success potential
4. **Fill in collaboration sections** with details about group projects, team leadership, or collaborative research

🎯 **Focus Areas:**
Since you mentioned you already have academic references covered, this letter will emphasize:
- Leadership abilities and experience
- Organizational and management skills
- Collaborative work and team dynamics
- Potential for success in professional environments

⏰ **Timeline:**
Please complete your input within the next few days so I have adequate time to review, refine, and finalize the letter before your application deadline.

If you have any questions or need clarification on what information to include, please don't hesitate to reach out.

Best regards,
Professor Wang"""

    # AppleScript to send email via Mail.app
    applescript = f'''
    tell application "Mail"
        activate
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{email_body}"}}
        tell newMessage
            make new to recipient with properties {{address:"{recipient}"}}
        end tell
        send newMessage
    end tell
    '''
    
    try:
        print("📧 Preparing to send email via Mail.app...")
        print(f"   Recipient: {recipient}")
        print(f"   Subject: {subject}")
        
        # Execute AppleScript
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, check=True)
        
        print("✅ Email sent successfully!")
        print(f"   Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Log the email send
        log_email_send(recipient, subject)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error sending email: {e}")
        print(f"   Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def log_email_send(recipient, subject):
    """Log email send details"""
    log_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/RefLetter/email_log.md"
    
    log_entry = f"""
## Email Sent - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**To:** {recipient}
**Subject:** {subject}
**Method:** Mail.app via AppleScript
**Document:** Reference Letter Google Doc
**Status:** Sent successfully

---
"""
    
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        print(f"📝 Email send logged to: {log_file}")
    except Exception as e:
        print(f"⚠️  Could not write to log file: {e}")

def main():
    """Main execution function"""
    print("🚀 Starting reference letter email notification...")
    print("=" * 50)
    
    success = send_mail_via_applescript()
    
    if success:
        print("\n✅ Email notification process completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Yanbo will receive the email with Google Doc access")
        print("   2. Student will add program details and examples")
        print("   3. Review and finalize reference letter content")
    else:
        print("\n❌ Email sending failed. Please check Mail.app settings and try again.")

if __name__ == "__main__":
    main()

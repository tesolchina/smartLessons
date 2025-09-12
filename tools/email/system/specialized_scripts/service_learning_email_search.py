#!/usr/bin/env python3
"""
Service Learning Email Search
Search for emails about Service Learning Course in Mail.app
"""

import subprocess
import os
import json
from datetime import datetime


def search_service_learning_emails():
    """Search for Service Learning related emails."""
    
    print("🔍 Searching for Service Learning emails...")
    
    applescript = '''
    tell application "Mail"
        set foundEmails to {}
        
        try
            -- Search inbox for Service Learning related emails
            set inboxFolder to inbox
            set serviceEmails to (every message in inboxFolder whose (subject contains "Service Learning" or subject contains "Departmental Meeting" or content contains "Service Learning" or content contains "Nancy" or content contains "Joshua"))
            
            repeat with msg in serviceEmails
                set emailSubject to subject of msg
                set emailSender to sender of msg
                set emailDate to date received of msg
                set emailContent to content of msg
                
                set emailData to "SUBJECT: " & emailSubject & " | FROM: " & emailSender & " | DATE: " & emailDate & " | CONTENT: " & emailContent
                set end of foundEmails to emailData
            end repeat
            
        end try
        
        return foundEmails
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout.strip():
            emails = result.stdout.strip().split('\n')
            print(f"📧 Found {len(emails)} emails")
            
            for i, email in enumerate(emails, 1):
                print(f"\n--- Email {i} ---")
                print(email[:500] + "..." if len(email) > 500 else email)
                
            return emails
        else:
            print("❌ No Service Learning emails found or error occurred")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def draft_reply_email(emails):
    """Draft a reply email to Nancy and Joshua about the Google Slides."""
    
    print("\n✏️ Drafting reply email...")
    
    # Email details
    google_slides_link = "https://docs.google.com/presentation/d/1_6aRzEFlUnvTPSSG5vtgFTKhxo5NpajnynDekjiiNgs/edit?usp=sharing"
    
    draft = f"""Subject: Re: Departmental Meeting - New Service Learning Course - Google Slides Ready

Dear Nancy and Joshua,

I hope this email finds you well.

Following our discussion about the new Service Learning course and the upcoming departmental meeting, I've prepared a collaborative Google Slides presentation for our joint sharing session.

🔗 **Google Slides Link:** {google_slides_link}

**Presentation Structure:**
1. Title slide with all three presenters (Dr. Joshua Chan, Dr. Nancy Guo, Dr. Simon Wang)
2. Dr. Joshua Chan's section - Service Learning methodology and community engagement
3. Dr. Nancy Guo's section - Language learning in service contexts
4. Dr. Simon Wang's section - LANG 2077: Language Skills for Human-AI Partnership
5. Discussion and Q&A slide

**Key Features:**
• Anyone with the link can edit (perfect for collaboration)
• Colorful, professional design with HKBU branding
• Structured content with placeholders for each presenter
• Ready for our departmental presentation

Please feel free to:
- Add your specific content to your respective sections
- Modify the design or layout as needed  
- Share additional feedback or suggestions

The presentation is set up so we can work on it collaboratively before the departmental meeting. I've included placeholder content that you can replace with your own materials.

Looking forward to our collaborative presentation and the positive impact our Service Learning initiatives will have on student learning.

Best regards,
Simon

---
Dr. Simon H. Wang
HKBU Language Centre
Hong Kong Baptist University
Email: simonwang@hkbu.edu.hk
"""
    
    return draft


def save_draft_email(draft):
    """Save the draft email to a file."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"service_learning_reply_draft_{timestamp}.txt"
    filepath = f"/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/email_automation/email_drafts/{filename}"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w') as f:
        f.write(draft)
    
    print(f"💾 Draft saved to: {filepath}")
    return filepath


def create_mail_draft(draft):
    """Create a draft email in Mail.app."""
    
    print("📧 Creating draft in Mail.app...")
    
    # Extract subject from draft
    lines = draft.split('\n')
    subject = lines[0].replace('Subject: ', '')
    content = '\n'.join(lines[2:])  # Skip subject and empty line
    
    # Escape quotes in content
    escaped_content = content.replace('"', '\\"')
    
    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}"}}
        set content of newMessage to "{escaped_content}"
        
        -- Add recipients (you'll need to add them manually)
        make new to recipient at end of to recipients of newMessage with properties {{name:"Nancy Guo", address:"nancyguo@hkbu.edu.hk"}}
        make new to recipient at end of to recipients of newMessage with properties {{name:"Joshua Chan", address:"joshuachan@hkbu.edu.hk"}}
        
        -- Show the draft
        set visible of newMessage to true
        activate
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("✅ Draft created in Mail.app")
            print("📝 Please review and send the email manually")
            return True
        else:
            print(f"❌ Error creating draft: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main function."""
    
    print("📧 Service Learning Email Reply System")
    print("=" * 40)
    
    # Search for emails
    emails = search_service_learning_emails()
    
    # Draft reply
    draft = draft_reply_email(emails)
    
    print("\n📄 Draft Email:")
    print("=" * 50)
    print(draft)
    
    # Save draft
    filepath = save_draft_email(draft)
    
    # Offer to create in Mail.app
    create_draft = input("\n❓ Create draft in Mail.app? (y/n): ").lower().strip()
    
    if create_draft == 'y':
        create_mail_draft(draft)
    else:
        print("💾 Draft saved to file only")
        print(f"📁 Location: {filepath}")


if __name__ == "__main__":
    main()

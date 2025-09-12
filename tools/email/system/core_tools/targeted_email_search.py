#!/usr/bin/env python3
"""
Targeted Screening Test Email Extractor
Quick search for specific emails and save to dedicated folder
"""

import subprocess
from datetime import datetime
from pathlib import Path
import re

def targeted_email_search():
    """
    Targeted search for specific screening test emails
    """
    applescript = '''
    tell application "Mail"
        set foundEmails to {}
        
        try
            -- Search recent emails in inbox and sent
            set inboxFolder to inbox
            set sentFolder to sent mailbox
            
            -- Search for Hermine's screening test email
            set hermineEmails to (every message in inboxFolder whose sender contains "hermine_chan@hkbu.edu.hk" and subject contains "Screening Test")
            
            repeat with msg in hermineEmails
                set emailData to "FOUND_EMAIL||SUBJECT:" & (subject of msg) & "||FROM:" & (sender of msg) & "||DATE:" & (date received of msg) & "||CONTENT:" & (content of msg) & "||END_EMAIL"
                set end of foundEmails to emailData
            end repeat
            
            -- Search for hermitriver emails
            set riverEmails to (every message in inboxFolder whose (sender contains "hermitriver" or content contains "hermitriver@hotmail.com" or content contains "River"))
            
            repeat with msg in riverEmails
                set emailData to "FOUND_EMAIL||SUBJECT:" & (subject of msg) & "||FROM:" & (sender of msg) & "||DATE:" & (date received of msg) & "||CONTENT:" & (content of msg) & "||END_EMAIL"
                set end of foundEmails to emailData
            end repeat
            
            -- Search sent emails to hermitriver
            set sentRiverEmails to (every message in sentFolder whose content contains "hermitriver@hotmail.com")
            
            repeat with msg in sentRiverEmails
                set emailData to "FOUND_EMAIL||SUBJECT:" & (subject of msg) & "||TO:hermitriver@hotmail.com||DATE:" & (date sent of msg) & "||CONTENT:" & (content of msg) & "||END_EMAIL"
                set end of foundEmails to emailData
            end repeat
            
        end try
        
        return foundEmails
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=60)
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_targeted_emails(email_data, output_dir):
    """
    Parse and save the targeted email results
    """
    if not email_data:
        return 0
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    emails = email_data.split('FOUND_EMAIL')
    email_count = 0
    
    for i, email in enumerate(emails):
        if '||SUBJECT:' in email and '||END_EMAIL' in email:
            try:
                # Parse email components
                parts = email.split('||')
                email_info = {}
                
                for part in parts:
                    if part.startswith('SUBJECT:'):
                        email_info['subject'] = part[8:]
                    elif part.startswith('FROM:'):
                        email_info['from'] = part[5:]
                    elif part.startswith('TO:'):
                        email_info['to'] = part[3:]
                    elif part.startswith('DATE:'):
                        email_info['date'] = part[5:]
                    elif part.startswith('CONTENT:'):
                        # Extract content (remove END_EMAIL)
                        content = part[8:].replace('END_EMAIL', '')
                        email_info['content'] = content
                
                if email_info.get('subject'):
                    # Create filename
                    safe_subject = re.sub(r'[^\w\s-]', '', email_info['subject'])[:40]
                    safe_subject = re.sub(r'[-\s]+', '-', safe_subject)
                    filename = f"email_{email_count+1:03d}_{safe_subject}.md"
                    
                    # Save email
                    file_path = output_path / filename
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {email_info.get('subject', 'No Subject')}\n\n")
                        f.write(f"**From**: {email_info.get('from', 'Unknown')}\n")
                        f.write(f"**To**: {email_info.get('to', 'Unknown')}\n")  
                        f.write(f"**Date**: {email_info.get('date', 'Unknown')}\n")
                        f.write(f"**Extracted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        f.write("## Email Content\n\n")
                        f.write("```\n")
                        f.write(email_info.get('content', 'No content'))
                        f.write("\n```\n")
                    
                    email_count += 1
                    print(f"📧 Saved: {email_info.get('subject', 'No Subject')}")
                
            except Exception as e:
                print(f"Error processing email: {e}")
                continue
    
    return email_count

def main():
    print("🎯 Targeted screening test email extraction...")
    
    # Search for specific emails
    email_data = targeted_email_search()
    
    # Output directory
    output_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/screening_test/emails"
    
    # Save emails
    if email_data:
        email_count = save_targeted_emails(email_data, output_dir)
    else:
        email_count = 0
        print("❌ No email data found")
    
    print(f"\n✅ Extraction complete! Found {email_count} emails")
    print(f"📁 Saved to: {output_dir}")

if __name__ == "__main__":
    main()

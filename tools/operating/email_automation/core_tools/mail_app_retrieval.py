#!/usr/bin/env python3
"""
Mail App Email Retrieval Script
Extract emails from Mac Mail app (including Exchange folders) using AppleScript
"""

import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

def get_mail_app_emails_via_applescript():
    """
    Use AppleScript to extract emails from Mac Mail app, focusing on Exchange folders
    """
    applescript = '''
    tell application "Mail"
        set searchResults to {}
        
        -- Get all accounts
        set accountList to every account
        
        repeat with currentAccount in accountList
            try
                -- Get all mailboxes in this account (including Exchange folders)
                set mailboxList to every mailbox of currentAccount
                
                repeat with currentMailbox in mailboxList
                    try
                        -- Search for screening test related emails
                        set messageList to (every message in currentMailbox whose (subject contains "screening test" or subject contains "Screening Test" or subject contains "SCREENING TEST" or subject contains "River" or subject contains "simon001" or subject contains "simon101" or subject contains "test-taker-test" or subject contains "UI testing"))
                        
                        repeat with currentMessage in messageList
                            set messageInfo to "SUBJECT: " & (subject of currentMessage) & return & "FROM: " & (sender of currentMessage) & return & "DATE: " & (date received of currentMessage) & return & "ACCOUNT: " & (name of currentAccount) & return & "MAILBOX: " & (name of currentMailbox) & return & "CONTENT: " & (content of currentMessage) & return & "---EMAIL-SEPARATOR---" & return
                            set end of searchResults to messageInfo
                        end repeat
                    end try
                end repeat
            end try
        end repeat
        
        return searchResults
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=120)
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception as e:
        print(f"Error running AppleScript: {e}")
        return None

def parse_email_results(email_data):
    """
    Parse the email results into structured format
    """
    if not email_data:
        return []
    
    emails = []
    email_blocks = email_data.split('---EMAIL-SEPARATOR---')
    
    for block in email_blocks:
        if block.strip():
            email_info = {}
            lines = block.strip().split('\n')
            current_content = []
            in_content = False
            
            for line in lines:
                if line.startswith('SUBJECT: '):
                    email_info['subject'] = line[9:]
                elif line.startswith('FROM: '):
                    email_info['from'] = line[6:]
                elif line.startswith('DATE: '):
                    email_info['date'] = line[6:]
                elif line.startswith('ACCOUNT: '):
                    email_info['account'] = line[9:]
                elif line.startswith('MAILBOX: '):
                    email_info['mailbox'] = line[9:]
                elif line.startswith('CONTENT: '):
                    in_content = True
                    current_content.append(line[9:])
                elif in_content:
                    current_content.append(line)
            
            if current_content:
                email_info['content'] = '\n'.join(current_content)
            
            if email_info:
                emails.append(email_info)
    
    return emails

def save_email_summary_markdown(emails, output_file):
    """
    Save extracted emails to markdown file
    """
    output_path = Path(output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Screening Test Emails - Mail App Extraction\n\n")
        f.write(f"**Extracted on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Source**: Mac Mail app (including Exchange folders)\n\n")
        
        if emails:
            f.write(f"## Found {len(emails)} Relevant Emails\n\n")
            
            for i, email in enumerate(emails, 1):
                f.write(f"### Email {i}\n")
                f.write(f"**Subject**: {email.get('subject', 'N/A')}\n")
                f.write(f"**From**: {email.get('from', 'N/A')}\n")
                f.write(f"**Date**: {email.get('date', 'N/A')}\n")
                f.write(f"**Account**: {email.get('account', 'N/A')}\n")
                f.write(f"**Mailbox**: {email.get('mailbox', 'N/A')}\n\n")
                
                if email.get('content'):
                    content = email['content'][:500] + "..." if len(email['content']) > 500 else email['content']
                    f.write(f"**Content Preview**:\n```\n{content}\n```\n\n")
                
                f.write("---\n\n")
        else:
            f.write("## No Relevant Emails Found\n\n")
            f.write("*The search did not find any emails matching the screening test keywords.*\n\n")
        
        f.write("## Search Keywords Used\n")
        f.write("- screening test, Screening Test, SCREENING TEST\n")
        f.write("- River\n")
        f.write("- simon001, simon101\n")
        f.write("- test-taker-test\n")
        f.write("- UI testing\n\n")
        
        f.write("## Next Steps\n")
        f.write("- [ ] Review found emails for testing instructions\n")
        f.write("- [ ] Extract account credentials and platform details\n")
        f.write("- [ ] Update testing documentation\n")
        f.write("- [ ] Proceed with UI testing\n")

def main():
    """
    Main email extraction function for Mac Mail app
    """
    print("🔍 Extracting screening test emails from Mac Mail app...")
    print("📧 Searching all accounts including Exchange folders...")
    
    # Extract emails
    email_data = get_mail_app_emails_via_applescript()
    
    # Parse results
    emails = parse_email_results(email_data)
    
    # Save summary
    output_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/screening_test/ui_testing/mail_app_email_summary.md"
    save_email_summary_markdown(emails, output_file)
    
    print(f"✅ Email summary saved to: {output_file}")
    print(f"📊 Found {len(emails)} relevant emails")
    
    if emails:
        print("\n📧 Email subjects found:")
        for email in emails:
            print(f"  - {email.get('subject', 'No subject')}")
    
    print("💡 Check the summary file for detailed email content")

if __name__ == "__main__":
    main()

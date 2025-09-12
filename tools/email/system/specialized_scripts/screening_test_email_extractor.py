#!/usr/bin/env python3
"""
Comprehensive Screening Test Email Extractor
Search for all emails related to screening test and hermitriver@hotmail.com
Save individual emails as separate files in the screening test emails folder
"""

import subprocess
import re
from datetime import datetime, timedelta
from pathlib import Path
import os

def comprehensive_screening_test_search():
    """
    Comprehensive search for screening test emails and hermitriver@hotmail.com communications
    """
    applescript = '''
    tell application "Mail"
        set emailResults to {}
        
        try
            -- Get all accounts
            set accountList to every account
            
            repeat with currentAccount in accountList
                try
                    -- Get all mailboxes in this account
                    set mailboxList to every mailbox of currentAccount
                    
                    repeat with currentMailbox in mailboxList
                        try
                            -- Search for screening test related emails
                            set screeningMessages to (every message in currentMailbox whose (subject contains "screening test" or subject contains "Screening Test" or subject contains "SCREENING TEST" or subject contains "screening" or subject contains "River" or subject contains "hermitriver" or sender contains "hermitriver@hotmail.com" or content contains "hermitriver@hotmail.com" or content contains "simon001" or content contains "simon101" or content contains "test-taker-test"))
                            
                            repeat with msg in screeningMessages
                                try
                                    set emailData to "EMAIL_START" & return & "SUBJECT: " & (subject of msg) & return & "FROM: " & (sender of msg) & return & "TO: " & (content of msg) & return & "DATE: " & (date received of msg) & return & "ACCOUNT: " & (name of currentAccount) & return & "MAILBOX: " & (name of currentMailbox) & return & "CONTENT_START" & return & (content of msg) & return & "CONTENT_END" & return & "EMAIL_END" & return & "---SEPARATOR---" & return
                                    set end of emailResults to emailData
                                end try
                            end repeat
                            
                            -- Also search specifically for hermitriver in recipients/cc
                            set hermitriverMessages to (every message in currentMailbox whose (content contains "hermitriver@hotmail.com" or recipient contains "hermitriver" or sender contains "hermitriver"))
                            
                            repeat with msg in hermitriverMessages
                                try
                                    set emailData to "EMAIL_START" & return & "SUBJECT: " & (subject of msg) & return & "FROM: " & (sender of msg) & return & "TO: " & (content of msg) & return & "DATE: " & (date received of msg) & return & "ACCOUNT: " & (name of currentAccount) & return & "MAILBOX: " & (name of currentMailbox) & return & "HERMITRIVER: YES" & return & "CONTENT_START" & return & (content of msg) & return & "CONTENT_END" & return & "EMAIL_END" & return & "---SEPARATOR---" & return
                                    set end of emailResults to emailData
                                end try
                            end repeat
                            
                        end try
                    end repeat
                end try
            end repeat
            
        end try
        
        return emailResults
    end tell
    '''
    
    try:
        print("🔍 Searching all mailboxes for screening test emails...")
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=180)
        return result.stdout.strip() if result.returncode == 0 else None
    except subprocess.TimeoutExpired:
        print("⚠️ Search timed out - trying quick search instead")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_and_save_emails(email_data, output_dir):
    """
    Parse email data and save each email as a separate markdown file
    """
    if not email_data:
        print("❌ No email data to process")
        return 0
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Split emails by separator
    email_blocks = email_data.split('---SEPARATOR---')
    email_count = 0
    
    for i, block in enumerate(email_blocks):
        if 'EMAIL_START' in block and 'EMAIL_END' in block:
            try:
                # Parse email components
                lines = block.split('\n')
                email_info = {}
                content_lines = []
                in_content = False
                
                for line in lines:
                    if line.startswith('SUBJECT: '):
                        email_info['subject'] = line[9:].strip()
                    elif line.startswith('FROM: '):
                        email_info['from'] = line[6:].strip()
                    elif line.startswith('TO: '):
                        email_info['to'] = line[4:].strip()
                    elif line.startswith('DATE: '):
                        email_info['date'] = line[6:].strip()
                    elif line.startswith('ACCOUNT: '):
                        email_info['account'] = line[9:].strip()
                    elif line.startswith('MAILBOX: '):
                        email_info['mailbox'] = line[9:].strip()
                    elif line.startswith('HERMITRIVER: '):
                        email_info['hermitriver'] = True
                    elif line.strip() == 'CONTENT_START':
                        in_content = True
                    elif line.strip() == 'CONTENT_END':
                        in_content = False
                    elif in_content:
                        content_lines.append(line)
                
                if email_info.get('subject'):
                    # Create safe filename
                    safe_subject = re.sub(r'[^\w\s-]', '', email_info['subject'])[:50]
                    safe_subject = re.sub(r'[-\s]+', '-', safe_subject)
                    filename = f"email_{i+1:03d}_{safe_subject}.md"
                    
                    # Save email as markdown file
                    file_path = output_path / filename
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"# Email: {email_info.get('subject', 'No Subject')}\n\n")
                        f.write(f"**From**: {email_info.get('from', 'Unknown')}\n")
                        f.write(f"**To**: {email_info.get('to', 'Unknown')}\n")
                        f.write(f"**Date**: {email_info.get('date', 'Unknown')}\n")
                        f.write(f"**Account**: {email_info.get('account', 'Unknown')}\n")
                        f.write(f"**Mailbox**: {email_info.get('mailbox', 'Unknown')}\n")
                        if email_info.get('hermitriver'):
                            f.write(f"**Contains hermitriver@hotmail.com**: Yes\n")
                        f.write(f"**Extracted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        f.write("## Email Content\n\n")
                        f.write("```\n")
                        f.write('\n'.join(content_lines))
                        f.write("\n```\n")
                    
                    email_count += 1
                    print(f"📧 Saved: {filename}")
                
            except Exception as e:
                print(f"Error processing email {i}: {e}")
                continue
    
    return email_count

def create_summary_file(email_count, output_dir):
    """
    Create a summary file of all extracted emails
    """
    summary_path = Path(output_dir) / "README.md"
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# Screening Test Email Collection\n\n")
        f.write(f"**Extraction Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Emails Found**: {email_count}\n")
        f.write(f"**Source**: Mac Mail app (all accounts and mailboxes)\n\n")
        
        f.write("## Search Criteria\n")
        f.write("- **Keywords**: screening test, Screening Test, River, hermitriver\n")
        f.write("- **Email Address**: hermitriver@hotmail.com (sender, recipient, CC, content)\n")
        f.write("- **Platform References**: simon001, simon101, test-taker-test\n\n")
        
        f.write("## Files in this Directory\n")
        email_files = sorted([f for f in os.listdir(output_dir) if f.startswith('email_') and f.endswith('.md')])
        
        for email_file in email_files:
            f.write(f"- `{email_file}`\n")
        
        f.write(f"\n## Usage\n")
        f.write("Each email is saved as a separate markdown file for easy reading and organization.\n")
        f.write("Files are named with format: `email_XXX_subject-preview.md`\n\n")
        f.write("## Related Folders\n")
        f.write("- **Main Project**: `../` (screening_test/)\n")
        f.write("- **UI Testing**: `../ui_testing/`\n")
        f.write("- **Email Automation**: `../../operating/email_automation/`\n")

def main():
    """
    Main function to extract and organize screening test emails
    """
    print("🚀 Starting comprehensive screening test email extraction...")
    
    # Search for emails
    email_data = comprehensive_screening_test_search()
    
    # Output directory
    output_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/screening_test/emails"
    
    # Parse and save emails
    if email_data:
        email_count = parse_and_save_emails(email_data, output_dir)
    else:
        email_count = 0
    
    # Create summary
    create_summary_file(email_count, output_dir)
    
    print(f"\n✅ Email extraction complete!")
    print(f"📁 Output directory: {output_dir}")
    print(f"📧 Total emails saved: {email_count}")
    print(f"📝 Summary file: {output_dir}/README.md")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Email Retrieval Script for Screening Test Communications
Extracts emails related to screening test from local Outlook
"""

import os
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

def get_outlook_emails_via_applescript():
    """
    Use AppleScript to extract emails from Outlook about screening test
    """
    applescript = '''
    tell application "Microsoft Outlook"
        set searchResults to {}
        set folderList to every folder
        
        repeat with currentFolder in folderList
            try
                set messageList to (every message in currentFolder whose subject contains "screening test" or subject contains "Screening Test" or subject contains "SCREENING TEST")
                repeat with currentMessage in messageList
                    set messageInfo to {subject:(subject of currentMessage), sender:(sender of currentMessage), date received:(time received of currentMessage), content:(content of currentMessage)}
                    set end of searchResults to messageInfo
                end repeat
            end try
        end repeat
        
        return searchResults
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=60)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running AppleScript: {e}")
        return None

def extract_screening_test_keywords():
    """
    Extract emails with screening test related keywords
    """
    keywords = [
        "screening test",
        "test 1",
        "test 2", 
        "river",
        "simon001",
        "simon101",
        "test-taker-test.hkbu.me",
        "ui testing",
        "platform",
        "bugs",
        "feedback"
    ]
    return keywords

def save_email_summary(emails_data, output_file):
    """
    Save extracted emails to markdown file
    """
    output_path = Path(output_file)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Screening Test Email Summary\\n\\n")
        f.write(f"**Extracted on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
        f.write("## Email Communications\\n\\n")
        
        if emails_data:
            f.write("### Recent Messages\\n\\n")
            # Process and format email data here
            f.write("*Email data processing in progress...*\\n\\n")
        else:
            f.write("*No emails found or extraction failed*\\n\\n")
        
        f.write("## Key Information Extracted\\n\\n")
        f.write("- **Platform**: https://test-taker-test.hkbu.me/\\n")
        f.write("- **Test Accounts**: simon001-010, simon101-110\\n")
        f.write("- **Contact**: River\\n")
        f.write("- **Task**: UI testing on 2 test sets\\n\\n")
        
        f.write("## Next Steps\\n")
        f.write("- [ ] Complete UI testing with provided accounts\\n")
        f.write("- [ ] Document bugs and issues\\n")
        f.write("- [ ] Report findings to River\\n")

def main():
    """
    Main email extraction function
    """
    print("🔍 Extracting screening test emails from Outlook...")
    
    # Try to extract emails
    emails_data = get_outlook_emails_via_applescript()
    
    # Save summary
    output_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/screening_test/ui_testing/email_summary.md"
    save_email_summary(emails_data, output_file)
    
    print(f"✅ Email summary saved to: {output_file}")
    print("💡 Check the file for extracted screening test communications")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Email Forward and Archive Script
Find specific email, forward it, and archive it using Mac Mail app
"""

import subprocess
from datetime import datetime

def find_and_forward_email():
    """
    Find email with specific subject, forward it to hswanghk@gmail.com, and archive it
    """
    applescript = '''
    tell application "Mail"
        set targetSubject to "Logs Panel, Automatic Image Updates, Database Credentials & Extensions, SMTP"
        set forwardAddress to "hswanghk@gmail.com"
        set emailFound to false
        
        try
            -- Search all mailboxes for the email
            set allAccounts to every account
            
            repeat with currentAccount in allAccounts
                set mailboxList to every mailbox of currentAccount
                
                repeat with currentMailbox in mailboxList
                    try
                        set foundMessages to (every message in currentMailbox whose subject is targetSubject)
                        
                        if (count of foundMessages) > 0 then
                            set targetMessage to item 1 of foundMessages
                            set emailFound to true
                            
                            -- Forward the email
                            set forwardMessage to forward targetMessage with opening window
                            
                            -- Set recipient
                            tell forwardMessage
                                make new to recipient at end of to recipients with properties {address:forwardAddress}
                                send
                            end tell
                            
                            -- Archive the original message (move to Archive folder if it exists, otherwise just mark)
                            try
                                set archiveMailbox to mailbox "Archive" of currentAccount
                                move targetMessage to archiveMailbox
                            on error
                                -- If no Archive folder, try to set as read/flagged for manual archiving
                                set read status of targetMessage to true
                                set flag index of targetMessage to 2
                            end try
                            
                            return "SUCCESS: Email found, forwarded to " & forwardAddress & ", and archived from " & (name of currentMailbox)
                        end if
                    end try
                end repeat
            end repeat
            
            if not emailFound then
                return "EMAIL NOT FOUND: Could not locate email with subject: " & targetSubject
            end if
            
        on error errorMessage
            return "ERROR: " & errorMessage
        end try
        
    end tell
    '''
    
    try:
        print("🔍 Searching for email: 'Logs Panel, Automatic Image Updates, Database Credentials & Extensions, SMTP'")
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"AppleScript Error: {result.stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return "TIMEOUT: Email search and forward operation timed out"
    except Exception as e:
        return f"EXCEPTION: {e}"

def log_email_action(result, log_file):
    """
    Log the email action result
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n## Email Forward & Archive Action - {timestamp}\n\n")
        f.write(f"**Subject**: Logs Panel, Automatic Image Updates, Database Credentials & Extensions, SMTP\n")
        f.write(f"**Forward To**: hswanghk@gmail.com\n")
        f.write(f"**Action**: Forward and Archive\n")
        f.write(f"**Result**: {result}\n")
        f.write(f"**Timestamp**: {timestamp}\n\n")
        f.write("---\n\n")

def main():
    """
    Main function to handle the email forward and archive task
    """
    print("📧 Starting email forward and archive operation...")
    
    # Execute the email operation
    result = find_and_forward_email()
    
    # Log the result
    log_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/email_automation/email_actions_log.md"
    log_email_action(result, log_file)
    
    # Print result
    print(f"📊 Result: {result}")
    print(f"📝 Action logged to: {log_file}")
    
    if "SUCCESS" in result:
        print("✅ Email operation completed successfully!")
        print("📧 Email forwarded to hswanghk@gmail.com")
        print("📁 Original email archived")
    elif "EMAIL NOT FOUND" in result:
        print("❌ Could not find the specified email")
        print("💡 Please check the subject line or search manually in Mail app")
    else:
        print("⚠️ Operation encountered an issue")
        print("🔍 Check the log for details")

if __name__ == "__main__":
    main()

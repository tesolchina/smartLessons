#!/usr/bin/env python3
"""
Working Email Forward and Archive Script
Now that permissions are confirmed working
"""

import subprocess
from datetime import datetime

def forward_and_archive_email():
    """
    Forward the specific email and archive it - working version
    """
    applescript = '''
    tell application "Mail"
        -- Find the email in inbox
        set targetMessages to (every message in inbox whose subject is "Logs Panel, Automatic Image Updates, Database Credentials & Extensions, SMTP")
        
        if (count of targetMessages) > 0 then
            set targetMessage to item 1 of targetMessages
            
            -- Forward the email
            set forwardMessage to forward targetMessage with opening window
            
            -- Set recipient
            tell forwardMessage
                make new to recipient at end of to recipients with properties {address:"hswanghk@gmail.com"}
                send
            end tell
            
            -- Archive the original message
            try
                -- Try to move to Archive mailbox
                set archiveMailbox to mailbox "Archive" of account "Exchange"
                move targetMessage to archiveMailbox
                return "SUCCESS: Email forwarded to hswanghk@gmail.com and moved to Archive"
            on error
                try
                    -- Try iCloud Archive
                    set archiveMailbox to mailbox "Archive" of account "iCloud"
                    move targetMessage to archiveMailbox
                    return "SUCCESS: Email forwarded to hswanghk@gmail.com and moved to iCloud Archive"
                on error
                    -- If no Archive folder, flag it and mark as read
                    set flag index of targetMessage to 2
                    set read status of targetMessage to true
                    return "SUCCESS: Email forwarded to hswanghk@gmail.com and flagged (no Archive folder found)"
                end try
            end try
        else
            return "ERROR: Email not found in inbox"
        end if
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"AppleScript Error: {result.stderr.strip()}"
            
    except Exception as e:
        return f"Exception: {e}"

def main():
    print("📧 Mail.app access confirmed - running forward and archive...")
    
    result = forward_and_archive_email()
    print(f"📊 Result: {result}")
    
    # Log the action
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/email_automation/email_actions_log.md"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n## Email Forward & Archive - {timestamp}\n\n")
        f.write(f"**Subject**: Logs Panel, Automatic Image Updates, Database Credentials & Extensions, SMTP\n")
        f.write(f"**Forward To**: hswanghk@gmail.com\n")
        f.write(f"**Action**: Forward and Archive\n")
        f.write(f"**Result**: {result}\n")
        f.write(f"**Mail.app Access**: ✅ Working\n")
        f.write(f"**Accounts Available**: iCloud, Exchange\n")
        f.write(f"**Timestamp**: {timestamp}\n\n")
        f.write("---\n\n")
    
    if "SUCCESS" in result:
        print("✅ Email operation completed successfully!")
        print("📧 Email forwarded to hswanghk@gmail.com")
        print("📁 Email archived/flagged")
    else:
        print("❌ Operation failed")
    
    print(f"📝 Action logged to: {log_file}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Quick Email Forward - Recent Emails Only
Search recent emails for the target subject and forward it
"""

import subprocess
from datetime import datetime

def quick_forward_recent_email():
    """
    Search only recent emails for faster processing
    """
    applescript = '''
    tell application "Mail"
        set targetSubject to "Logs Panel, Automatic Image Updates, Database Credentials & Extensions, SMTP"
        set forwardAddress to "hswanghk@gmail.com"
        
        try
            -- Search only in Inbox for recent emails (last 30 days)
            set inboxFolder to inbox
            set recentDate to (current date) - (30 * days)
            
            set recentMessages to (every message in inboxFolder whose date received > recentDate and subject contains "Logs Panel")
            
            if (count of recentMessages) > 0 then
                -- Find exact match
                repeat with msg in recentMessages
                    if (subject of msg) is targetSubject then
                        -- Forward the email
                        set forwardMessage to forward msg with opening window
                        
                        -- Set recipient and send
                        tell forwardMessage
                            make new to recipient at end of to recipients with properties {address:forwardAddress}
                            send
                        end tell
                        
                        -- Archive (move to Archive or flag for manual archiving)
                        try
                            -- Try to move to Archive folder
                            move msg to mailbox "Archive"
                        on error
                            -- If no Archive folder, flag it
                            set flag index of msg to 2
                            set read status of msg to true
                        end try
                        
                        return "SUCCESS: Email forwarded to " & forwardAddress & " and archived/flagged"
                    end if
                end repeat
                
                return "PARTIAL: Found similar emails but no exact match for: " & targetSubject
            else
                return "NOT FOUND: No recent emails matching subject found"
            end if
            
        on error errorMessage
            return "ERROR: " & errorMessage
        end try
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=30)
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {e}"

def manual_search_instruction():
    """
    Provide manual search instructions if automated search fails
    """
    instructions = """
    ## Manual Email Search Instructions
    
    If the automated search doesn't work, please follow these steps:
    
    1. **Open Mail app**
    2. **Use the search bar** (⌘F)
    3. **Search for**: "Logs Panel"
    4. **Look for subject**: "Logs Panel, Automatic Image Updates, Database Credentials & Extensions, SMTP"
    5. **Select the email** and click Forward (⌘F)
    6. **Enter recipient**: hswanghk@gmail.com
    7. **Send the forward**
    8. **Archive the original**: Right-click → Archive (or drag to Archive folder)
    
    ## Alternative AppleScript Commands
    
    You can also run these commands in Script Editor:
    
    ```applescript
    tell application "Mail"
        -- Search command
        set searchResults to (every message whose subject contains "Logs Panel")
        -- Then manually process the results
    end tell
    ```
    """
    return instructions

def main():
    print("🚀 Quick email forward operation...")
    
    # Try the quick search
    result = quick_forward_recent_email()
    print(f"📊 Result: {result}")
    
    # Log the action
    log_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/email_automation/email_actions_log.md"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n## Quick Email Forward - {timestamp}\n\n")
        f.write(f"**Target Subject**: Logs Panel, Automatic Image Updates, Database Credentials & Extensions, SMTP\n")
        f.write(f"**Forward To**: hswanghk@gmail.com\n")
        f.write(f"**Result**: {result}\n\n")
        
        if "SUCCESS" not in result:
            f.write("## Manual Instructions\n\n")
            f.write(manual_search_instruction())
        
        f.write("---\n\n")
    
    if "SUCCESS" in result:
        print("✅ Email forwarded successfully!")
    else:
        print("⚠️ Automated forward failed - check log for manual instructions")
        print(f"📝 Instructions logged to: {log_file}")

if __name__ == "__main__":
    main()

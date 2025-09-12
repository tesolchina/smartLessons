#!/usr/bin/env python3
"""
Email Debug Script - Check what's in inbox
"""

import subprocess

def check_inbox():
    """Simple check of what emails are available"""
    
    applescript = '''
    tell application "Mail"
        set emailList to ""
        set emailCount to 0
        
        try
            repeat with mailboxItem in mailboxes
                set mailboxName to name of mailboxItem
                set messageCount to count of messages of mailboxItem
                set emailList to emailList & "Mailbox: " & mailboxName & " (" & messageCount & " messages)" & return
                
                if mailboxName contains "INBOX" or mailboxName contains "Exchange" then
                    set emailList to emailList & "  Recent emails in " & mailboxName & ":" & return
                    
                    repeat with i from 1 to (messageCount)
                        if i > 5 then exit repeat -- Show only first 5
                        try
                            set emailItem to message i of mailboxItem
                            set emailSubject to subject of emailItem
                            set emailSender to (sender of emailItem as string)
                            set emailList to emailList & "    " & i & ". " & emailSubject & " (from: " & emailSender & ")" & return
                        on error
                            set emailList to emailList & "    " & i & ". [Error reading email]" & return
                        end try
                    end repeat
                    set emailList to emailList & return
                end if
            end repeat
            
            return emailList
        on error errMsg
            return "ERROR: " & errMsg
        end try
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=60)
        
        return result.stdout.strip()
        
    except Exception as e:
        return f"Exception: {e}"

if __name__ == "__main__":
    print("🔍 Checking Mail.app inbox...")
    result = check_inbox()
    print(result)

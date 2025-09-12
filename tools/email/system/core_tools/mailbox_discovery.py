#!/usr/bin/env python3
"""
Mail.app Mailbox Discovery - Find all available mailboxes and accounts
"""

import subprocess

def discover_mailboxes():
    """Discover all mailboxes in Mail.app"""
    
    applescript = '''
    tell application "Mail"
        set mailboxInfo to ""
        set accountInfo to ""
        
        try
            -- Get account information
            set accountInfo to "=== ACCOUNTS ===" & return
            repeat with acct in accounts
                set accountInfo to accountInfo & "Account: " & (name of acct) & return
                set accountInfo to accountInfo & "  Type: " & (class of acct as string) & return
                try
                    set accountInfo to accountInfo & "  Email: " & (email addresses of acct as string) & return
                end try
                set accountInfo to accountInfo & return
            end repeat
            set accountInfo to accountInfo & return
            
            -- Get mailbox information
            set mailboxInfo to "=== ALL MAILBOXES ===" & return
            repeat with mailboxItem in mailboxes
                set mailboxName to name of mailboxItem
                set messageCount to count of messages of mailboxItem
                set mailboxInfo to mailboxInfo & "Mailbox: " & mailboxName & " (" & messageCount & " messages)" & return
                
                try
                    set accountName to name of account of mailboxItem
                    set mailboxInfo to mailboxInfo & "  Account: " & accountName & return
                end try
                
                -- Show sample emails for mailboxes with messages
                if messageCount > 0 and messageCount <= 20 then
                    set mailboxInfo to mailboxInfo & "  Sample emails:" & return
                    repeat with i from 1 to (messageCount)
                        if i > 3 then exit repeat
                        try
                            set emailItem to message i of mailboxItem
                            set emailSubject to subject of emailItem
                            set emailDate to date received of emailItem
                            set mailboxInfo to mailboxInfo & "    " & i & ". " & emailSubject & " (" & emailDate & ")" & return
                        on error
                            set mailboxInfo to mailboxInfo & "    " & i & ". [Could not read email]" & return
                        end try
                    end repeat
                else if messageCount > 20 then
                    set mailboxInfo to mailboxInfo & "  [Too many messages to sample]" & return
                end if
                set mailboxInfo to mailboxInfo & return
            end repeat
            
            return accountInfo & mailboxInfo
        on error errMsg
            return "ERROR: " & errMsg & return & "Make sure Mail.app is running and has permission to be controlled by AppleScript."
        end try
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=90)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"AppleScript Error: {result.stderr}\n\nMake sure:\n1. Mail.app is running\n2. System Preferences > Security & Privacy > Privacy > Automation allows Terminal to control Mail"
        
    except Exception as e:
        return f"Exception: {e}"

if __name__ == "__main__":
    print("🔍 Discovering Mail.app mailboxes and accounts...")
    print("This will help us understand your mail setup.\n")
    result = discover_mailboxes()
    print(result)

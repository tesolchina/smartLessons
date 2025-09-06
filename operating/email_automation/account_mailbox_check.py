#!/usr/bin/env python3
"""
Account-specific mailbox access for Mail.app
"""

import subprocess

def check_account_mailboxes():
    """Check mailboxes for each account specifically"""
    
    applescript = '''
    tell application "Mail"
        set allInfo to ""
        
        try
            repeat with acct in accounts
                set accountName to name of acct
                set allInfo to allInfo & "=== ACCOUNT: " & accountName & " ===" & return
                
                try
                    -- Get mailboxes for this account
                    repeat with mbox in mailboxes of acct
                        set mboxName to name of mbox
                        set msgCount to count of messages of mbox
                        set allInfo to allInfo & "Mailbox: " & mboxName & " (" & msgCount & " messages)" & return
                        
                        -- Sample recent emails
                        if msgCount > 0 then
                            set allInfo to allInfo & "  Recent emails:" & return
                            repeat with i from 1 to msgCount
                                if i > 3 then exit repeat
                                try
                                    set msg to message i of mbox
                                    set msgSubject to subject of msg
                                    set msgSender to sender of msg as string
                                    set msgDate to date received of msg as string
                                    set allInfo to allInfo & "    " & i & ". " & msgSubject & return
                                    set allInfo to allInfo & "       From: " & msgSender & return
                                    set allInfo to allInfo & "       Date: " & msgDate & return
                                on error
                                    set allInfo to allInfo & "    " & i & ". [Error reading message]" & return
                                end try
                            end repeat
                        end if
                        set allInfo to allInfo & return
                    end repeat
                on error accErr
                    set allInfo to allInfo & "Error accessing mailboxes for " & accountName & ": " & accErr & return
                end try
                set allInfo to allInfo & return
            end repeat
            
            -- Also try top-level mailboxes (Smart Mailboxes, etc.)
            set allInfo to allInfo & "=== TOP-LEVEL MAILBOXES ===" & return
            repeat with mbox in mailboxes
                try
                    set mboxName to name of mbox
                    set msgCount to count of messages of mbox
                    set allInfo to allInfo & "Mailbox: " & mboxName & " (" & msgCount & " messages)" & return
                    
                    if msgCount > 0 and msgCount <= 10 then
                        repeat with i from 1 to msgCount
                            if i > 2 then exit repeat
                            try
                                set msg to message i of mbox
                                set msgSubject to subject of msg
                                set allInfo to allInfo & "    " & i & ". " & msgSubject & return
                            end try
                        end repeat
                    end if
                on error mboxErr
                    set allInfo to allInfo & "Error with mailbox: " & mboxErr & return
                end try
            end repeat
            
            return allInfo
        on error mainErr
            return "Main Error: " & mainErr
        end try
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=120)
        
        return result.stdout.strip()
        
    except Exception as e:
        return f"Python Exception: {e}"

if __name__ == "__main__":
    print("🔍 Checking account-specific mailboxes...")
    result = check_account_mailboxes()
    print(result)

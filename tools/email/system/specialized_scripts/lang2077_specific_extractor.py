#!/usr/bin/env python3
"""
LANG2077 Specific Email Extractor
Extract the service learning departmental meeting email from Joshua Chan
"""

import subprocess
import os
from datetime import datetime

def extract_joshua_email():
    """Extract the specific email from Joshua Chan about service learning"""
    
    applescript = '''
    tell application "Mail"
        set foundEmail to ""
        
        try
            -- Look specifically in Exchange account
            repeat with acct in accounts
                if name of acct is "Exchange" then
                    repeat with mbox in mailboxes of acct
                        if name of mbox is "Inbox" then
                            repeat with emailItem in messages of mbox
                                set emailSubject to subject of emailItem
                                set emailSender to sender of emailItem as string
                                set emailContent to content of emailItem
                                set emailDate to date received of emailItem as string
                                set senderAddress to (address of sender of emailItem)
                                
                                -- Look for the specific email
                                if (emailSubject contains "Departmental Meeting" and emailSubject contains "Service Learning") or 
                                   (senderAddress contains "joshuachan@hkbu.edu.hk") then
                                    
                                    set foundEmail to "=== SERVICE LEARNING EMAIL FOUND ===" & return
                                    set foundEmail to foundEmail & "Subject: " & emailSubject & return
                                    set foundEmail to foundEmail & "From: " & emailSender & return
                                    set foundEmail to foundEmail & "Address: " & senderAddress & return
                                    set foundEmail to foundEmail & "Date: " & emailDate & return
                                    set foundEmail to foundEmail & "Content:" & return & emailContent & return
                                    set foundEmail to foundEmail & "===================" & return
                                    exit repeat
                                end if
                            end repeat
                            exit repeat
                        end if
                    end repeat
                    exit repeat
                end if
            end repeat
            
            if foundEmail is not "" then
                return foundEmail
            else
                return "NO_JOSHUA_EMAIL_FOUND"
            end if
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

def save_to_lang2077(email_content):
    """Save the email to LANG2077 project folder"""
    
    project_path = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG2077"
    os.makedirs(project_path, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"departmental_meeting_service_learning_{timestamp}.md"
    filepath = os.path.join(project_path, filename)
    
    formatted_content = f"""# Departmental Meeting - New Service Learning Course

**Extracted on:** {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}
**Project:** LANG2077
**Source:** Exchange Account Inbox

---

{email_content}

---

## Next Steps
- [ ] Review course requirements and implementation plan
- [ ] Set up Canva design materials for course promotion
- [ ] Plan service learning components and partnerships
- [ ] Schedule follow-up meetings with Joshua and team
- [ ] Develop course structure and timeline

## Related Files
- `notesUpdate.md` - Initial request notes
- This email extraction - `{filename}`

## Canva Design TODO
As requested in notesUpdate.md, we need to set up Canva designs via CLI for this new service learning course.
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(formatted_content)
    
    return filepath

if __name__ == "__main__":
    print("🔍 Looking for Joshua Chan's service learning email...")
    
    email_content = extract_joshua_email()
    
    if "NO_JOSHUA_EMAIL_FOUND" in email_content:
        print("❌ Specific email not found")
        print("Let me search more broadly...")
        
        # Broader search
        broader_search = '''
        tell application "Mail"
            set allEmails to ""
            try
                repeat with acct in accounts
                    if name of acct is "Exchange" then
                        repeat with mbox in mailboxes of acct
                            if name of mbox is "Inbox" then
                                repeat with emailItem in messages of mbox
                                    set emailSubject to subject of emailItem
                                    set emailSender to sender of emailItem as string
                                    
                                    if emailSubject contains "Service" or emailSubject contains "Departmental" or 
                                       emailSender contains "joshua" or emailSender contains "chan" then
                                        set allEmails to allEmails & "Found: " & emailSubject & " from " & emailSender & return
                                    end if
                                end repeat
                                exit repeat
                            end if
                        end repeat
                        exit repeat
                    end if
                end repeat
                return allEmails
            end try
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', broader_search], 
                                  capture_output=True, text=True, timeout=60)
            print("📧 Related emails found:")
            print(result.stdout.strip())
        except:
            print("❌ Broader search failed")
        
        return
    
    if "ERROR:" in email_content:
        print(f"❌ Error: {email_content}")
        return
    
    print("✅ Email found! Saving to LANG2077 project...")
    saved_path = save_to_lang2077(email_content)
    print(f"📁 Email saved to: {saved_path}")
    print("📂 Ready for Canva design setup!")

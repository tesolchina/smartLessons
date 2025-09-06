#!/usr/bin/env python3
"""
LANG2077 Email Extractor
Find and extract the departmental meeting email about new service learning course
Created: September 6, 2025
"""

import subprocess
import os
from datetime import datetime

def find_service_learning_email():
    """Find email about service learning course in inbox"""
    
    applescript = '''
    tell application "Mail"
        set foundEmails to {}
        set emailDetails to ""
        
        try
            repeat with mailboxItem in mailboxes
                if name of mailboxItem contains "INBOX" or name of mailboxItem contains "Exchange" then
                    repeat with emailItem in messages of mailboxItem
                        set emailSubject to subject of emailItem
                        set emailContent to content of emailItem
                        set emailSender to (sender of emailItem as string)
                        set emailDate to (date received of emailItem as string)
                        
                        -- Search for service learning or departmental meeting keywords
                        if (emailSubject contains "Service Learning" or emailSubject contains "service learning" or 
                            emailSubject contains "Departmental Meeting" or emailSubject contains "departmental meeting" or
                            emailSubject contains "LANG2077" or emailContent contains "service learning" or 
                            emailContent contains "Service Learning") then
                            
                            set emailDetails to emailDetails & "=== EMAIL FOUND ===" & return
                            set emailDetails to emailDetails & "Subject: " & emailSubject & return
                            set emailDetails to emailDetails & "From: " & emailSender & return  
                            set emailDetails to emailDetails & "Date: " & emailDate & return
                            set emailDetails to emailDetails & "Content: " & return & emailContent & return
                            set emailDetails to emailDetails & "===================" & return & return
                        end if
                    end repeat
                end if
            end repeat
            
            if emailDetails is not "" then
                return emailDetails
            else
                return "NO_SERVICE_LEARNING_EMAIL_FOUND"
            end if
        on error errMsg
            return "ERROR: " & errMsg
        end try
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr}"
            
    except Exception as e:
        return f"Exception: {e}"

def save_email_to_project(email_content, project_path):
    """Save extracted email to LANG2077 project folder"""
    
    # Create project directory if it doesn't exist
    os.makedirs(project_path, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"departmental_meeting_service_learning_{timestamp}.md"
    filepath = os.path.join(project_path, filename)
    
    # Format email content for markdown
    formatted_content = f"""# Departmental Meeting - Service Learning Course Email

**Extracted on:** {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}
**Project:** LANG2077
**Source:** Mac Mail Inbox

---

{email_content}

---

## Next Steps
- [ ] Review course requirements  
- [ ] Set up Canva design materials
- [ ] Plan service learning components
- [ ] Schedule follow-up meetings

## Related Files
- `notesUpdate.md` - Initial request notes
- This email extraction - `{filename}`
"""
    
    # Save to file
    with open(filepath, 'w') as f:
        f.write(formatted_content)
    
    return filepath

def main():
    project_path = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG2077"
    
    print("🔍 Searching for Service Learning email in inbox...")
    
    email_content = find_service_learning_email()
    
    if "NO_SERVICE_LEARNING_EMAIL_FOUND" in email_content:
        print("❌ No service learning emails found in inbox")
        print("🔍 Try checking these manually:")
        print("   - Subject containing 'Service Learning'")
        print("   - Subject containing 'Departmental Meeting'") 
        print("   - Content mentioning 'service learning'")
        return
    
    if "ERROR:" in email_content or "Exception:" in email_content:
        print(f"❌ Error extracting email: {email_content}")
        return
    
    # Save email to project folder
    print("✅ Service learning email found!")
    saved_path = save_email_to_project(email_content, project_path)
    print(f"📁 Email saved to: {saved_path}")
    print(f"📂 Project folder: {project_path}")

if __name__ == "__main__":
    main()

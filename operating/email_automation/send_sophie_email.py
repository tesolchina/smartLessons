#!/usr/bin/env python3
"""
Send email to Sophie regarding sick leave response
Created: September 6, 2025
"""

import subprocess
import os

def send_sophie_sick_leave_email():
    """Send the drafted email to Sophie using Mac Mail.app"""
    
    # Read the email content from the draft
    draft_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/email_automation/email_drafts/draft_sophie_sick_leave_response.md"
    
    # Email content (extracted from the draft)
    email_subject = "Re: UE1 section 37 request for sick leave for today's lesson"
    email_body = """Dear Sophie,

Thank you for letting me know about your absence from today's lesson. I hope you have a speedy recovery and feel better soon.

Please make sure to refer to the course notes and materials available here: https://docs.google.com/document/d/1efLZhPk1i5Hdlg2rQ2vfoR-ccFUMkJkYSj7rPSVSXNU/edit?tab=t.0#heading=h.emudfpxxf0y2

Important reminder: Please pay special attention to the pre-course writing test which is DUE September 12th. This is a crucial requirement for the course.

I also want to caution you that this section currently has only 10 students enrolled and may be subject to cancellation if enrollment doesn't increase.

Please catch up on any missed materials when you're feeling better, and don't hesitate to reach out if you have any questions about today's content or the upcoming assignments.

Get well soon!

Best regards,
Dr. Simon Wang"""

    # AppleScript to compose and send email
    applescript = f'''
    tell application "Mail"
        activate
        
        -- Create new email
        set newMessage to make new outgoing message with properties {{subject:"{email_subject}", content:"{email_body}"}}
        
        -- Note: You'll need to add Sophie's email address manually or we can prompt for it
        display dialog "Please enter Sophie's email address:" default answer "" with title "Send Email to Sophie"
        set sophieEmail to text returned of result
        
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:sophieEmail}}
        end tell
        
        -- Open the email for final review before sending
        open newMessage
        
        display dialog "Email composed and ready. Please review and click Send manually." with title "Email Ready"
        
    end tell
    '''
    
    try:
        # Execute the AppleScript
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Email composed successfully!")
            print("📧 The email to Sophie is now ready in Mail.app")
            print("🔍 Please review and send it manually")
            return True
        else:
            print("❌ Error composing email:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Script timed out - Mail.app may need attention")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("📧 Sending Sophie's sick leave response email...")
    send_sophie_sick_leave_email()

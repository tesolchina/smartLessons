#!/usr/bin/env python3
"""
Script to send emails using macOS Mail.app via AppleScript
"""

import subprocess
import pandas as pd
import time

def send_email_via_mail_app(recipient, subject, body, dept_name):
    """Send email using macOS Mail.app via AppleScript"""
    
    # Escape quotes and backslashes for AppleScript
    def escape_for_applescript(text):
        return text.replace('\\', '\\\\').replace('"', '\\"').replace('\r', '\\r').replace('\n', '\\n')
    
    escaped_recipient = escape_for_applescript(recipient)
    escaped_subject = escape_for_applescript(subject)
    escaped_body = escape_for_applescript(body)
    
    applescript = f'''
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {{subject:"{escaped_subject}", visible:true}}
    tell newMessage
        make new to recipient at end of to recipients with properties {{address:"{escaped_recipient}"}}
        set content to "{escaped_body}"
    end tell
end tell
'''
    
    try:
        print(f"Creating email for: {dept_name}")
        print(f"Recipient: {recipient}")
        
        # Execute the AppleScript
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, check=True)
        
        print(f"✅ Email created successfully in Mail.app!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating email: {e}")
        print(f"Error output: {e.stderr}")
        return False

def send_test_email():
    """Send a test email to Civil Service Bureau"""
    # Read the CSV to get department info
    df = pd.read_csv('hk_gov_emails_20250911_163227.csv')
    
    # Test with Civil Service Bureau
    test_dept = "Civil Service Bureau"
    dept_row = df[df['department'] == test_dept].iloc[0]
    
    recipient = dept_row['email']
    dept_name = dept_row['department']
    
    subject = "Request for Information under Code on Access to Information - Staff Directory for AO and EO Grades"
    
    body = f"""Dear Access to Information Officer,

I hope this email finds you well. I am writing to make a formal request for information under the Code on Access to Information.

REQUEST DETAILS:
I would like to request access to the list of staff members in Administrative Officer (AO) and Executive Officer (EO) grades currently serving in {dept_name}, as contained in the government telephone directory https://tel.directory.gov.hk/index_ENG.html or equivalent internal staff directory.

SPECIFIC INFORMATION REQUESTED:
- Names of staff members holding AO grades (AO, SAO, PAO, etc.)
- Names of staff members holding EO grades (EO, SEO, CEO, etc.)
- Their respective job titles and positions
- The divisions or sections they are assigned to within your department/bureau

PURPOSE AND RESEARCH CONTEXT:
My intention in requesting this information is to conduct academic research on how staff from the Administrative Officer and Executive Officer grades are distributed and serve across different government departments and bureaus. Given your bureau's central role in civil service management and policy formulation, this information would be particularly valuable for understanding the deployment of senior administrative grades across government.

This research aims to analyze deployment patterns, career progression paths, and organizational structures of these key civil service grades within the Hong Kong government system. The findings will contribute to academic understanding of public administration and civil service management in Hong Kong.

LEGAL BASIS:
This request is made under the Code on Access to Information, which provides for public access to government information unless there are specific exemptions that apply. I believe the requested information relates to the general administration and organization of government departments and should be available for public access.

FORMAT PREFERENCE:
I would be grateful if the information could be provided in electronic format (Excel spreadsheet, PDF, or similar) for easier reference and analysis.

I understand that you will acknowledge receipt of this request within 10 days and provide a substantive response within 21 days, as per the Code on Access to Information guidelines. If you require any clarification regarding this request or if there are any processing fees involved, please do not hesitate to contact me.

Thank you for your attention to this matter. I look forward to your response.

Yours sincerely,

Dr Simon Wang
Lecturer in English
The Language Centre
Hong Kong Baptist University

Date: 11 September 2025"""

    return send_email_via_mail_app(recipient, subject, body, dept_name)

if __name__ == "__main__":
    success = send_test_email()
    if success:
        print("\\n📧 Test email has been created in Mail.app!")
        print("Please review the email and send when ready.")
        print("\\nTo send all 77 emails, let me know and I'll create a batch script.")
    else:
        print("\\n❌ Failed to create test email. Please check Mail.app permissions.")

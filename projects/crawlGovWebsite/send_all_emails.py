#!/usr/bin/env python3
"""
Script to send all department emails using macOS Mail.app via AppleScript
"""

import subprocess
import pandas as pd
import time

def escape_for_applescript(text):
    """Escape text for AppleScript"""
    return text.replace('\\', '\\\\').replace('"', '\\"').replace('\r', '\\r').replace('\n', '\\n')

def get_department_context(dept_name):
    """Get department-specific context"""
    contexts = {
        "Civil Service Bureau": "Given your bureau's central role in civil service management and policy formulation, this information would be particularly valuable for understanding the deployment of senior administrative grades across government.",
        
        "Financial Services and the Treasury Bureau": "As a key policy bureau overseeing financial services and treasury functions, your department likely employs significant numbers of AO and EO grade officers in policy development and financial management roles.",
        
        "Education Bureau": "Given the scope of educational policy and administration under your bureau, understanding the deployment of administrative and executive officers would provide insights into educational governance structures.",
        
        "Security Bureau": "As the bureau responsible for security policy coordination, the distribution of AO and EO grades within your organization would reflect the administrative structure of security governance.",
        
        "Home Affairs Department": "Given your department's extensive district-based operations and community liaison functions, the deployment of AO and EO grades across different district offices would be of particular research interest.",
        
        "Hong Kong Police Force": "As one of the largest government departments with extensive operational and administrative functions, your organization likely has a substantial number of AO and EO grade officers in various roles.",
        
        "Department of Health": "Given the complexity of health policy and service delivery, understanding how administrative and executive officers are deployed across different health functions would provide valuable insights.",
        
        "Immigration Department": "As a major operational department handling immigration and related services, the distribution of AO and EO grades would reflect the administrative structure of immigration services.",
        
        "Inland Revenue Department": "Given your department's role in tax administration and revenue collection, understanding the deployment of administrative and executive officers would provide insights into tax administration structures."
    }
    
    if dept_name in contexts:
        return contexts[dept_name]
    elif "Bureau" in dept_name:
        return "As a policy bureau, your organization likely employs AO and EO grade officers in various policy development and coordination roles, making this information valuable for understanding administrative structures in policy formulation."
    elif "Department" in dept_name:
        return "As an operational department, understanding how AO and EO grade officers are deployed across different functions would provide valuable insights into the administrative structure of government service delivery."
    elif "Office" in dept_name:
        return "Given your office's specialized functions, the deployment of administrative and executive officers would reflect the organizational structure needed to fulfill your mandate."
    else:
        return "Understanding how AO and EO grade officers are deployed within your organization would contribute to research on administrative structures across government."

def send_email_via_mail_app(recipient, subject, body, dept_name):
    """Send email using macOS Mail.app via AppleScript"""
    
    escaped_recipient = escape_for_applescript(recipient)
    escaped_subject = escape_for_applescript(subject)
    escaped_body = escape_for_applescript(body)
    
    applescript = f'''
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {{subject:"{escaped_subject}", visible:false}}
    tell newMessage
        make new to recipient at end of to recipients with properties {{address:"{escaped_recipient}"}}
        set content to "{escaped_body}"
    end tell
end tell
'''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating email for {dept_name}: {e}")
        return False

def send_all_emails():
    """Send emails to all departments"""
    # Read the CSV to get department info
    df = pd.read_csv('hk_gov_emails_20250911_163227.csv')
    
    # Get unique departments
    unique_depts = df['department'].unique()
    
    print(f"Preparing to create {len(unique_depts)} emails in Mail.app...")
    print("This will create draft emails that you can review and send.")
    
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    successful = 0
    failed = 0
    
    for i, dept in enumerate(sorted(unique_depts), 1):
        # Get the first email for this department
        dept_row = df[df['department'] == dept].iloc[0]
        recipient = dept_row['email']
        
        subject = "Request for Information under Code on Access to Information - Staff Directory for AO and EO Grades"
        
        # Get department-specific context
        dept_context = get_department_context(dept)
        
        body = f"""Dear Access to Information Officer,

I hope this email finds you well. I am writing to make a formal request for information under the Code on Access to Information.

REQUEST DETAILS:
I would like to request access to the list of staff members in Administrative Officer (AO) and Executive Officer (EO) grades currently serving in {dept}, as contained in the government telephone directory https://tel.directory.gov.hk/index_ENG.html or equivalent internal staff directory.

SPECIFIC INFORMATION REQUESTED:
- Names of staff members holding AO grades (AO, SAO, PAO, etc.)
- Names of staff members holding EO grades (EO, SEO, CEO, etc.)
- Their respective job titles and positions
- The divisions or sections they are assigned to within your department/bureau

PURPOSE AND RESEARCH CONTEXT:
My intention in requesting this information is to conduct academic research on how staff from the Administrative Officer and Executive Officer grades are distributed and serve across different government departments and bureaus. {dept_context}

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

        print(f"[{i}/{len(unique_depts)}] Creating email for: {dept}")
        
        if send_email_via_mail_app(recipient, subject, body, dept):
            successful += 1
            print(f"✅ Email created successfully")
        else:
            failed += 1
            print(f"❌ Failed to create email")
        
        # Small delay to avoid overwhelming the system
        time.sleep(0.5)
    
    print(f"\\n📊 Summary:")
    print(f"✅ Successfully created: {successful} emails")
    print(f"❌ Failed: {failed} emails")
    print(f"\\n📧 All emails are now in your Mail.app drafts!")
    print("You can review and send them at your convenience.")

if __name__ == "__main__":
    send_all_emails()

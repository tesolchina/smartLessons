#!/usr/bin/env python3
"""
Script to open mail app with pre-filled email content
"""

import subprocess
import urllib.parse
import pandas as pd

def send_test_email():
    # Read the CSV to get department info
    df = pd.read_csv('hk_gov_emails_20250911_163227.csv')
    
    # Let's start with Civil Service Bureau as a test
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

    # URL encode the parameters
    encoded_recipient = urllib.parse.quote(recipient)
    encoded_subject = urllib.parse.quote(subject)
    encoded_body = urllib.parse.quote(body)
    
    # Create mailto URL
    mailto_url = f"mailto:{encoded_recipient}?subject={encoded_subject}&body={encoded_body}"
    
    print(f"Opening mail app for: {dept_name}")
    print(f"Recipient: {recipient}")
    print(f"Subject: {subject}")
    
    try:
        # Open the mail app with pre-filled content
        subprocess.run(['open', mailto_url], check=True)
        print("✅ Mail app opened successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error opening mail app: {e}")
        return False

if __name__ == "__main__":
    send_test_email()

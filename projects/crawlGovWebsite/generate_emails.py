#!/usr/bin/env python3
"""
Generate customized email drafts for each Hong Kong government department
"""

import pandas as pd
import os
from datetime import datetime

def create_customized_emails():
    # Read the CSV file
    df = pd.read_csv('hk_gov_emails_20250911_163227.csv')
    
    # Create emails folder
    emails_folder = 'department_emails'
    if not os.path.exists(emails_folder):
        os.makedirs(emails_folder)
    
    # Get unique departments
    unique_depts = df['department'].unique()
    
    # Department-specific customizations
    def get_department_context(dept_name):
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
        
        # Default context for departments not specifically mentioned
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
    
    # Generate email for each unique department
    for dept in sorted(unique_depts):
        # Get the first email for this department
        dept_email = df[df['department'] == dept]['email'].iloc[0]
        
        # Create safe filename
        safe_filename = dept.replace('/', '_').replace(',', '').replace('  ', ' ').strip()
        safe_filename = ''.join(c for c in safe_filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_filename}.txt"
        
        # Get department-specific context
        dept_context = get_department_context(dept)
        
        # Create the email content
        email_content = f"""Subject: Request for Information under Code on Access to Information - Staff Directory for AO and EO Grades

To: {dept_email}

Dear Access to Information Officer,

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

Date: {datetime.now().strftime('%d %B %Y')}

---
Department: {dept}
Email: {dept_email}
Generated: {datetime.now().strftime('%d %B %Y at %H:%M')}
"""
        
        # Write to file
        filepath = os.path.join(emails_folder, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(email_content)
        
        print(f"Created: {filename}")
    
    print(f"\nCompleted! Generated {len(unique_depts)} customized emails in '{emails_folder}' folder.")
    
    # Create a summary file
    summary_content = f"""HONG KONG GOVERNMENT DEPARTMENTS - EMAIL REQUEST SUMMARY

Generated: {datetime.now().strftime('%d %B %Y at %H:%M')}
Total Departments: {len(unique_depts)}

This folder contains customized email requests for AO and EO grade staff information 
under the Code on Access to Information, addressed to each Hong Kong government 
department and bureau.

Each email includes:
- Department-specific context and justification
- Formal request structure
- Legal basis under Code on Access to Information
- Academic research purpose
- Professional signature

Files are named by department name for easy identification.

Dr Simon Wang
Lecturer in English
The Language Centre
Hong Kong Baptist University
"""
    
    with open(os.path.join(emails_folder, '_README.txt'), 'w', encoding='utf-8') as f:
        f.write(summary_content)

if __name__ == "__main__":
    create_customized_emails()

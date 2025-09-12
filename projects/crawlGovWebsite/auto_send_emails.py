#!/usr/bin/env python3
"""
Script to automatically send all department emails via Mail.app with status reporting
"""

import subprocess
import pandas as pd
import time
import json
from datetime import datetime

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

def send_email_auto(recipient, subject, body, dept_name):
    """Send email automatically via Mail.app using AppleScript"""
    
    escaped_recipient = escape_for_applescript(recipient)
    escaped_subject = escape_for_applescript(subject)
    escaped_body = escape_for_applescript(body)
    
    # AppleScript to create and send email automatically
    applescript = f'''
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {{subject:"{escaped_subject}", visible:false}}
    tell newMessage
        make new to recipient at end of to recipients with properties {{address:"{escaped_recipient}"}}
        set content to "{escaped_body}"
        send
    end tell
end tell
'''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, check=True, timeout=30)
        return {"status": "SUCCESS", "error": None}
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "error": "Email send timeout after 30 seconds"}
    except subprocess.CalledProcessError as e:
        return {"status": "FAILED", "error": f"AppleScript error: {e.stderr}"}
    except Exception as e:
        return {"status": "ERROR", "error": f"Unexpected error: {str(e)}"}

def send_all_emails_auto():
    """Automatically send emails to all departments with status reporting"""
    
    # Read the CSV to get department info
    df = pd.read_csv('hk_gov_emails_20250911_163227.csv')
    
    # Get unique departments
    unique_depts = df['department'].unique()
    
    # Initialize status tracking
    status_report = {
        "execution_start": datetime.now().isoformat(),
        "total_departments": len(unique_depts),
        "results": [],
        "summary": {
            "successful": 0,
            "failed": 0,
            "timeout": 0,
            "error": 0
        }
    }
    
    print(f"🚀 AUTOMATIC EMAIL SENDING STARTED")
    print(f"📊 Total departments: {len(unique_depts)}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    for i, dept in enumerate(sorted(unique_depts), 1):
        dept_start_time = datetime.now()
        
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

        print(f"[{i:2}/{len(unique_depts)}] Sending to: {dept[:50]}{'...' if len(dept) > 50 else ''}")
        print(f"        Email: {recipient}")
        
        # Send the email
        result = send_email_auto(recipient, subject, body, dept)
        
        dept_end_time = datetime.now()
        duration = (dept_end_time - dept_start_time).total_seconds()
        
        # Record the result
        dept_result = {
            "department": dept,
            "email": recipient,
            "timestamp": dept_start_time.isoformat(),
            "duration_seconds": duration,
            "status": result["status"],
            "error": result["error"]
        }
        
        status_report["results"].append(dept_result)
        
        # Update summary
        if result["status"] == "SUCCESS":
            status_report["summary"]["successful"] += 1
            print(f"        ✅ SUCCESS (in {duration:.1f}s)")
        elif result["status"] == "TIMEOUT":
            status_report["summary"]["timeout"] += 1
            print(f"        ⏰ TIMEOUT (after {duration:.1f}s)")
        elif result["status"] == "FAILED":
            status_report["summary"]["failed"] += 1
            print(f"        ❌ FAILED: {result['error']}")
        else:
            status_report["summary"]["error"] += 1
            print(f"        🔴 ERROR: {result['error']}")
        
        # Small delay between emails to avoid overwhelming Mail.app
        time.sleep(2)
    
    # Finalize status report
    status_report["execution_end"] = datetime.now().isoformat()
    status_report["total_duration_minutes"] = (
        datetime.fromisoformat(status_report["execution_end"]) - 
        datetime.fromisoformat(status_report["execution_start"])
    ).total_seconds() / 60
    
    # Save status report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON report
    json_filename = f"email_status_report_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(status_report, f, indent=2, ensure_ascii=False)
    
    # Human-readable report
    txt_filename = f"email_status_report_{timestamp}.txt"
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write("HONG KONG GOVERNMENT EMAIL SENDING STATUS REPORT\\n")
        f.write("=" * 50 + "\\n\\n")
        f.write(f"Execution Started: {status_report['execution_start']}\\n")
        f.write(f"Execution Ended: {status_report['execution_end']}\\n")
        f.write(f"Total Duration: {status_report['total_duration_minutes']:.1f} minutes\\n")
        f.write(f"Total Departments: {status_report['total_departments']}\\n\\n")
        
        f.write("SUMMARY:\\n")
        f.write(f"✅ Successful: {status_report['summary']['successful']}\\n")
        f.write(f"❌ Failed: {status_report['summary']['failed']}\\n")
        f.write(f"⏰ Timeout: {status_report['summary']['timeout']}\\n")
        f.write(f"🔴 Error: {status_report['summary']['error']}\\n\\n")
        
        f.write("DETAILED RESULTS:\\n")
        f.write("-" * 50 + "\\n")
        
        for result in status_report["results"]:
            f.write(f"Department: {result['department']}\\n")
            f.write(f"Email: {result['email']}\\n")
            f.write(f"Status: {result['status']}\\n")
            f.write(f"Duration: {result['duration_seconds']:.1f}s\\n")
            if result['error']:
                f.write(f"Error: {result['error']}\\n")
            f.write("-" * 30 + "\\n")
    
    # Print final summary
    print("\\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    print(f"⏰ Total Duration: {status_report['total_duration_minutes']:.1f} minutes")
    print(f"📧 Total Emails: {status_report['total_departments']}")
    print(f"✅ Successful: {status_report['summary']['successful']}")
    print(f"❌ Failed: {status_report['summary']['failed']}")
    print(f"⏰ Timeout: {status_report['summary']['timeout']}")
    print(f"🔴 Error: {status_report['summary']['error']}")
    print("\\n📄 Status reports saved:")
    print(f"   - {json_filename} (JSON format)")
    print(f"   - {txt_filename} (Human-readable)")
    
    success_rate = (status_report['summary']['successful'] / status_report['total_departments']) * 100
    print(f"\\n🎯 Success Rate: {success_rate:.1f}%")

if __name__ == "__main__":
    print("⚠️  WARNING: This will automatically send emails to all 77 HK government departments!")
    print("📧 Emails will be sent immediately without further confirmation.")
    print("📄 Status report will be generated automatically.")
    print("\\nPress Ctrl+C within 5 seconds to cancel...")
    
    try:
        time.sleep(5)
        send_all_emails_auto()
    except KeyboardInterrupt:
        print("\\n❌ Operation cancelled by user.")
        exit(1)

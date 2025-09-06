#!/usr/bin/env python3
"""
Generic Email Extractor
Flexible email extraction tool for any project or search criteria
Created: September 6, 2025
"""

import subprocess
import os
import argparse
import json
from datetime import datetime
from typing import List, Optional, Dict

class GenericEmailExtractor:
    """Generic email extractor with flexible search and save options"""
    
    def __init__(self):
        self.extraction_log = "operating/email_automation/extraction_log.json"
    
    def search_emails(self, 
                     keywords: Optional[List[str]] = None,
                     sender_filter: Optional[str] = None,
                     date_filter: Optional[str] = None,
                     mailboxes: Optional[List[str]] = None,
                     max_results: int = 10) -> List[Dict]:
        """
        Search emails with flexible criteria
        
        Args:
            keywords: List of keywords to search for in subject/content
            sender_filter: Filter by sender email/name
            date_filter: Date filter (format: YYYY-MM-DD or 'today', 'yesterday', 'week')
            mailboxes: List of mailboxes to search (default: INBOX, Exchange)
            max_results: Maximum number of emails to return
            
        Returns:
            List of email dictionaries
        """
        
        # Default search settings
        if keywords is None:
            keywords = []
        if mailboxes is None:
            mailboxes = ["INBOX", "Exchange"]
        
        # Build keyword search condition
        keyword_conditions = []
        for keyword in keywords:
            keyword_conditions.append(f'(emailSubject contains "{keyword}" or emailContent contains "{keyword}")')
        
        keyword_search = " or ".join(keyword_conditions) if keyword_conditions else "true"
        
        # Build sender filter condition
        sender_condition = f'(emailSender contains "{sender_filter}")' if sender_filter else "true"
        
        # Build mailbox search
        mailbox_condition = " or ".join([f'name of mailboxItem contains "{mb}"' for mb in mailboxes])
        
        applescript = f'''
        tell application "Mail"
            set foundEmails to {{}}
            set emailCount to 0
            set maxResults to {max_results}
            
            try
                repeat with mailboxItem in mailboxes
                    if ({mailbox_condition}) then
                        repeat with emailItem in messages of mailboxItem
                            if emailCount >= maxResults then exit repeat
                            
                            set emailSubject to subject of emailItem
                            set emailContent to content of emailItem
                            set emailSender to (sender of emailItem as string)
                            set emailDate to (date received of emailItem as string)
                            set senderAddress to ""
                            
                            try
                                set senderAddress to (address of sender of emailItem)
                            end try
                            
                            -- Apply search filters
                            if ({keyword_search}) and ({sender_condition}) then
                                set emailInfo to "=== EMAIL " & (emailCount + 1) & " ===" & return
                                set emailInfo to emailInfo & "Subject: " & emailSubject & return
                                set emailInfo to emailInfo & "From: " & emailSender & return
                                set emailInfo to emailInfo & "Address: " & senderAddress & return
                                set emailInfo to emailInfo & "Date: " & emailDate & return
                                set emailInfo to emailInfo & "Mailbox: " & name of mailboxItem & return
                                set emailInfo to emailInfo & "Content: " & return & emailContent & return
                                set emailInfo to emailInfo & "===================" & return & return
                                
                                set end of foundEmails to emailInfo
                                set emailCount to emailCount + 1
                            end if
                        end repeat
                    end if
                    if emailCount >= maxResults then exit repeat
                end repeat
                
                if emailCount > 0 then
                    set resultText to "FOUND_" & emailCount & "_EMAILS" & return
                    repeat with emailInfo in foundEmails
                        set resultText to resultText & emailInfo
                    end repeat
                    return resultText
                else
                    return "NO_EMAILS_FOUND"
                end if
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=90)
            
            if result.returncode == 0:
                return self._parse_email_results(result.stdout.strip())
            else:
                return [{"error": f"AppleScript error: {result.stderr}"}]
                
        except Exception as e:
            return [{"error": f"Exception: {e}"}]
    
    def _parse_email_results(self, raw_output: str) -> List[Dict]:
        """Parse the raw AppleScript output into structured email data"""
        
        if "NO_EMAILS_FOUND" in raw_output:
            return []
        
        if "ERROR:" in raw_output:
            return [{"error": raw_output}]
        
        emails = []
        email_blocks = raw_output.split("=== EMAIL")
        
        for block in email_blocks[1:]:  # Skip first empty block
            if "===" not in block:
                continue
                
            lines = block.split('\n')
            email_data = {
                "number": lines[0].strip().split()[0],
                "subject": "",
                "from": "",
                "address": "",
                "date": "",
                "mailbox": "",
                "content": "",
                "raw": block
            }
            
            content_started = False
            content_lines = []
            
            for line in lines[1:]:
                if line.startswith("Subject: "):
                    email_data["subject"] = line[9:]
                elif line.startswith("From: "):
                    email_data["from"] = line[6:]
                elif line.startswith("Address: "):
                    email_data["address"] = line[9:]
                elif line.startswith("Date: "):
                    email_data["date"] = line[6:]
                elif line.startswith("Mailbox: "):
                    email_data["mailbox"] = line[9:]
                elif line.startswith("Content: "):
                    content_started = True
                elif content_started and not line.startswith("==="):
                    content_lines.append(line)
                elif line.startswith("==="):
                    break
            
            email_data["content"] = '\n'.join(content_lines)
            emails.append(email_data)
        
        return emails
    
    def save_emails_to_project(self, 
                              emails: List[Dict], 
                              project_path: str,
                              filename_prefix: str = "extracted_emails") -> List[str]:
        """
        Save extracted emails to project folder
        
        Args:
            emails: List of email dictionaries
            project_path: Path to save emails
            filename_prefix: Prefix for saved files
            
        Returns:
            List of saved file paths
        """
        
        # Create project directory
        os.makedirs(project_path, exist_ok=True)
        saved_files = []
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save individual emails
        for i, email in enumerate(emails, 1):
            if "error" in email:
                continue
                
            # Create safe filename
            subject_safe = "".join(c for c in email.get("subject", "")[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{filename_prefix}_{timestamp}_{i:02d}_{subject_safe}.md"
            filepath = os.path.join(project_path, filename)
            
            # Format email content
            content = f"""# Email Extract {i}

**Extracted on:** {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}
**Source:** {email.get('mailbox', 'Unknown')}

## Email Details
- **Subject:** {email.get('subject', 'No Subject')}
- **From:** {email.get('from', 'Unknown Sender')}
- **Address:** {email.get('address', 'No Address')}
- **Date:** {email.get('date', 'No Date')}
- **Mailbox:** {email.get('mailbox', 'Unknown')}

---

## Email Content

{email.get('content', 'No Content')}

---

## Extraction Info
- **Extraction Time:** {datetime.now().isoformat()}
- **Email Number:** {email.get('number', i)}
- **File:** {filename}
"""
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            saved_files.append(filepath)
        
        # Save summary file
        summary_filename = f"{filename_prefix}_{timestamp}_SUMMARY.md"
        summary_filepath = os.path.join(project_path, summary_filename)
        
        summary_content = f"""# Email Extraction Summary

**Extraction Date:** {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}
**Total Emails Found:** {len(emails)}
**Project Folder:** {project_path}

## Extracted Emails

"""
        
        for i, email in enumerate(emails, 1):
            if "error" not in email:
                summary_content += f"""### Email {i}
- **Subject:** {email.get('subject', 'No Subject')}
- **From:** {email.get('from', 'Unknown')}
- **Date:** {email.get('date', 'Unknown')}
- **Mailbox:** {email.get('mailbox', 'Unknown')}

"""
        
        summary_content += f"""
## Files Created
"""
        
        for filepath in saved_files:
            summary_content += f"- `{os.path.basename(filepath)}`\n"
        
        with open(summary_filepath, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        saved_files.append(summary_filepath)
        
        # Log extraction
        self._log_extraction(emails, project_path, saved_files)
        
        return saved_files
    
    def _log_extraction(self, emails: List[Dict], project_path: str, saved_files: List[str]):
        """Log extraction for tracking"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "project_path": project_path,
            "emails_found": len(emails),
            "files_created": len(saved_files),
            "saved_files": [os.path.basename(f) for f in saved_files]
        }
        
        # Load or create log
        if os.path.exists(self.extraction_log):
            with open(self.extraction_log, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {"extractions": []}
        
        log_data["extractions"].append(log_entry)
        
        # Save log
        os.makedirs(os.path.dirname(self.extraction_log), exist_ok=True)
        with open(self.extraction_log, 'w') as f:
            json.dump(log_data, f, indent=2)

def main():
    """Command line interface for email extraction"""
    
    parser = argparse.ArgumentParser(description="Generic Email Extractor")
    parser.add_argument("--keywords", nargs='+', help="Keywords to search for")
    parser.add_argument("--sender", help="Filter by sender email/name")
    parser.add_argument("--project-path", required=True, help="Path to save extracted emails")
    parser.add_argument("--filename-prefix", default="extracted_emails", help="Prefix for saved files")
    parser.add_argument("--max-results", type=int, default=10, help="Maximum emails to extract")
    parser.add_argument("--mailboxes", nargs='+', default=["INBOX", "Exchange"], help="Mailboxes to search")
    
    args = parser.parse_args()
    
    extractor = GenericEmailExtractor()
    
    print("🔍 Generic Email Extraction")
    print("=" * 40)
    print(f"📂 Project path: {args.project_path}")
    print(f"🔍 Keywords: {args.keywords or 'None'}")
    print(f"👤 Sender filter: {args.sender or 'None'}")
    print(f"📧 Max results: {args.max_results}")
    print(f"📬 Mailboxes: {args.mailboxes}")
    print("\n🔍 Searching emails...")
    
    # Search emails
    emails = extractor.search_emails(
        keywords=args.keywords,
        sender_filter=args.sender,
        mailboxes=args.mailboxes,
        max_results=args.max_results
    )
    
    if not emails:
        print("❌ No emails found matching criteria")
        return
    
    if len(emails) == 1 and "error" in emails[0]:
        print(f"❌ Error during search: {emails[0]['error']}")
        return
    
    print(f"✅ Found {len(emails)} email(s)")
    
    # Save emails
    saved_files = extractor.save_emails_to_project(
        emails=emails,
        project_path=args.project_path,
        filename_prefix=args.filename_prefix
    )
    
    print(f"\n📁 Saved {len(saved_files)} file(s):")
    for filepath in saved_files:
        print(f"   - {os.path.basename(filepath)}")
    
    print(f"\n✅ Email extraction complete!")
    print(f"📂 Files saved to: {args.project_path}")

if __name__ == "__main__":
    main()

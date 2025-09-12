#!/usr/bin/env python3
"""
Focused Inbox Email Extractor
Simple, reliable extraction from main inbox mailboxes
Created: September 6, 2025
"""

import subprocess
import os
import argparse
from datetime import datetime
from typing import List, Optional

class FocusedInboxExtractor:
    """Simple email extractor focused on inbox mailboxes"""
    
    def __init__(self):
        self.extraction_log = "operating/email_automation/focused_extraction_log.txt"
    
    def extract_from_inbox(self, 
                          keywords: Optional[List[str]] = None,
                          sender_filter: Optional[str] = None,
                          max_results: int = 5) -> str:
        """
        Extract emails from inbox mailboxes (Exchange/iCloud Inbox)
        
        Args:
            keywords: Keywords to search for (optional)
            sender_filter: Sender name/email filter (optional) 
            max_results: Maximum emails to return
            
        Returns:
            Raw email content string
        """
        
        # Build search conditions
        keyword_condition = "true"
        if keywords:
            keyword_parts = []
            for keyword in keywords:
                keyword_parts.append(f'(emailSubject contains "{keyword}" or emailContent contains "{keyword}")')
            keyword_condition = " or ".join(keyword_parts)
        
        sender_condition = "true"
        if sender_filter:
            sender_condition = f'(emailSender contains "{sender_filter}" or senderAddress contains "{sender_filter}")'
        
        applescript = f'''
        tell application "Mail"
            set foundEmails to ""
            set emailCount to 0
            set maxResults to {max_results}
            
            try
                -- Search in Exchange account Inbox first
                repeat with acct in accounts
                    if name of acct is "Exchange" then
                        repeat with mbox in mailboxes of acct
                            if name of mbox is "Inbox" then
                                repeat with emailItem in messages of mbox
                                    if emailCount >= maxResults then exit repeat
                                    
                                    set emailSubject to subject of emailItem
                                    set emailContent to content of emailItem
                                    set emailSender to sender of emailItem as string
                                    set emailDate to date received of emailItem as string
                                    
                                    -- Safely get sender address
                                    set senderAddress to ""
                                    try
                                        set senderAddress to (address of sender of emailItem)
                                    end try
                                    
                                    -- Apply filters
                                    if ({keyword_condition}) and ({sender_condition}) then
                                        set emailInfo to "=== EMAIL " & (emailCount + 1) & " ===" & return
                                        set emailInfo to emailInfo & "Subject: " & emailSubject & return
                                        set emailInfo to emailInfo & "From: " & emailSender & return
                                        set emailInfo to emailInfo & "Address: " & senderAddress & return
                                        set emailInfo to emailInfo & "Date: " & emailDate & return
                                        set emailInfo to emailInfo & "Mailbox: Exchange Inbox" & return
                                        set emailInfo to emailInfo & "Content:" & return & emailContent & return
                                        set emailInfo to emailInfo & "===================" & return & return
                                        
                                        set foundEmails to foundEmails & emailInfo
                                        set emailCount to emailCount + 1
                                    end if
                                end repeat
                                exit repeat
                            end if
                        end repeat
                        exit repeat
                    end if
                end repeat
                
                -- Also check iCloud Inbox if needed
                if emailCount < maxResults then
                    repeat with acct in accounts
                        if name of acct is "iCloud" then
                            repeat with mbox in mailboxes of acct
                                if name of mbox is "Inbox" then
                                    repeat with emailItem in messages of mbox
                                        if emailCount >= maxResults then exit repeat
                                        
                                        set emailSubject to subject of emailItem
                                        set emailContent to content of emailItem
                                        set emailSender to sender of emailItem as string
                                        set emailDate to date received of emailItem as string
                                        
                                        -- Safely get sender address
                                        set senderAddress to ""
                                        try
                                            set senderAddress to (address of sender of emailItem)
                                        end try
                                        
                                        -- Apply filters
                                        if ({keyword_condition}) and ({sender_condition}) then
                                            set emailInfo to "=== EMAIL " & (emailCount + 1) & " ===" & return
                                            set emailInfo to emailInfo & "Subject: " & emailSubject & return
                                            set emailInfo to emailInfo & "From: " & emailSender & return
                                            set emailInfo to emailInfo & "Address: " & senderAddress & return
                                            set emailInfo to emailInfo & "Date: " & emailDate & return
                                            set emailInfo to emailInfo & "Mailbox: iCloud Inbox" & return
                                            set emailInfo to emailInfo & "Content:" & return & emailContent & return
                                            set emailInfo to emailInfo & "===================" & return & return
                                            
                                            set foundEmails to foundEmails & emailInfo
                                            set emailCount to emailCount + 1
                                        end if
                                    end repeat
                                    exit repeat
                                end if
                            end repeat
                            exit repeat
                        end if
                    end repeat
                end if
                
                if emailCount > 0 then
                    return "FOUND_" & emailCount & "_EMAILS" & return & foundEmails
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
                return result.stdout.strip()
            else:
                return f"AppleScript Error: {result.stderr}"
                
        except Exception as e:
            return f"Python Exception: {e}"
    
    def save_emails(self, email_content: str, project_path: str, filename_prefix: str = "inbox_emails") -> List[str]:
        """Save extracted emails to project folder"""
        
        if "NO_EMAILS_FOUND" in email_content or "ERROR:" in email_content:
            return []
        
        # Create project directory
        os.makedirs(project_path, exist_ok=True)
        saved_files = []
        
        # Parse emails
        if "FOUND_" in email_content:
            lines = email_content.split('\n')
            count_line = lines[0]
            email_count = int(count_line.split('_')[1])
            
            # Split into individual emails
            email_blocks = email_content.split("=== EMAIL")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for i, block in enumerate(email_blocks[1:], 1):  # Skip first empty block
                if "===" not in block:
                    continue
                
                # Parse email data
                lines = block.split('\n')
                email_data = {}
                content_started = False
                content_lines = []
                
                for line in lines:
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
                    elif line.startswith("Content:"):
                        content_started = True
                    elif content_started and not line.startswith("==="):
                        content_lines.append(line)
                    elif line.startswith("==="):
                        break
                
                email_data["content"] = '\n'.join(content_lines)
                
                # Create safe filename
                subject_safe = "".join(c for c in email_data.get("subject", "")[:40] if c.isalnum() or c in (' ', '-', '_')).strip()
                filename = f"{filename_prefix}_{timestamp}_{i:02d}_{subject_safe}.md"
                filepath = os.path.join(project_path, filename)
                
                # Format and save
                formatted_content = f"""# Inbox Email Extract {i}

**Extracted:** {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}
**Source:** {email_data.get('mailbox', 'Inbox')}

## Email Details
- **Subject:** {email_data.get('subject', 'No Subject')}
- **From:** {email_data.get('from', 'Unknown Sender')}
- **Email Address:** {email_data.get('address', 'No Address')}
- **Date:** {email_data.get('date', 'No Date')}

---

## Email Content

{email_data.get('content', 'No Content')}

---

*Extracted using Focused Inbox Extractor*
"""
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                
                saved_files.append(filepath)
        
        # Create summary
        if saved_files:
            summary_filename = f"{filename_prefix}_{timestamp}_SUMMARY.md"
            summary_filepath = os.path.join(project_path, summary_filename)
            
            summary_content = f"""# Inbox Email Extraction Summary

**Date:** {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}
**Emails Found:** {len(saved_files)}
**Project:** {project_path}

## Extracted Files
"""
            
            for filepath in saved_files:
                summary_content += f"- `{os.path.basename(filepath)}`\n"
            
            with open(summary_filepath, 'w') as f:
                f.write(summary_content)
            
            saved_files.append(summary_filepath)
        
        # Log extraction
        self._log_extraction(len(saved_files), project_path)
        
        return saved_files
    
    def _log_extraction(self, file_count: int, project_path: str):
        """Simple logging"""
        log_entry = f"{datetime.now().isoformat()} - Extracted {file_count} emails to {project_path}\n"
        
        os.makedirs(os.path.dirname(self.extraction_log), exist_ok=True)
        with open(self.extraction_log, 'a') as f:
            f.write(log_entry)

def main():
    """Command line interface"""
    
    parser = argparse.ArgumentParser(description="Focused Inbox Email Extractor")
    parser.add_argument("--keywords", nargs='+', help="Keywords to search for")
    parser.add_argument("--sender", help="Filter by sender")
    parser.add_argument("--project-path", required=True, help="Where to save emails")
    parser.add_argument("--filename-prefix", default="inbox_emails", help="File prefix")
    parser.add_argument("--max-results", type=int, default=5, help="Max emails to extract")
    
    args = parser.parse_args()
    
    extractor = FocusedInboxExtractor()
    
    print("📧 Focused Inbox Email Extractor")
    print("=" * 40)
    print(f"📂 Project: {args.project_path}")
    print(f"🔍 Keywords: {args.keywords or 'All emails'}")
    print(f"👤 Sender: {args.sender or 'Any sender'}")
    print(f"📧 Max results: {args.max_results}")
    print("\n🔍 Searching inbox...")
    
    # Extract emails
    email_content = extractor.extract_from_inbox(
        keywords=args.keywords,
        sender_filter=args.sender,
        max_results=args.max_results
    )
    
    if "NO_EMAILS_FOUND" in email_content:
        print("❌ No emails found matching criteria")
        return
    
    if "ERROR:" in email_content:
        print(f"❌ Error: {email_content}")
        return
    
    # Save emails
    saved_files = extractor.save_emails(
        email_content=email_content,
        project_path=args.project_path,
        filename_prefix=args.filename_prefix
    )
    
    if saved_files:
        print(f"✅ Successfully extracted and saved {len(saved_files)-1} emails")
        print(f"📁 Files saved to: {args.project_path}")
        print(f"📋 Summary: {os.path.basename(saved_files[-1])}")
    else:
        print("❌ No emails were saved")

if __name__ == "__main__":
    main()

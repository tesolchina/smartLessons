#!/usr/bin/env python3
"""
Smart Email Handler - Reply and Archive Workflow
Handles inbox emails with reply, auto-send, and archive functionality
Created: September 6, 2025
"""

import subprocess
import sys
import argparse
import json
import os
from typing import List, Optional, Dict
from datetime import datetime
from generic_email_sender import EmailSender

class SmartEmailHandler:
    """Enhanced email handler with reply and archive functionality"""
    
    def __init__(self):
        self.sender = EmailSender()
        self.actions_log = "operating/email_automation/email_actions_log.md"
    
    def find_email_by_subject(self, subject_search: str, mailbox: str = "INBOX") -> Optional[Dict]:
        """
        Find email in inbox by subject search
        
        Args:
            subject_search: Text to search for in subject line
            mailbox: Mailbox to search (default: INBOX)
            
        Returns:
            Dict with email details or None if not found
        """
        applescript = f'''
        tell application "Mail"
            set foundEmail to null
            set emailDetails to {{}}
            
            try
                repeat with mailboxItem in mailboxes
                    if name of mailboxItem contains "{mailbox}" then
                        repeat with emailItem in messages of mailboxItem
                            set emailSubject to subject of emailItem
                            if emailSubject contains "{subject_search}" then
                                set foundEmail to emailItem
                                set emailDetails to {{subject:emailSubject, sender:(sender of emailItem as string), date_received:(date received of emailItem as string), message_id:(message id of emailItem)}}
                                exit repeat
                            end if
                        end repeat
                        if foundEmail is not null then exit repeat
                    end if
                end repeat
                
                if foundEmail is not null then
                    return emailDetails as string
                else
                    return "EMAIL_NOT_FOUND"
                end if
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and "EMAIL_NOT_FOUND" not in result.stdout:
                # Parse the returned email details
                return {"found": True, "details": result.stdout.strip()}
            else:
                print(f"❌ Email with subject '{subject_search}' not found in {mailbox}")
                return None
                
        except Exception as e:
            print(f"❌ Error searching for email: {e}")
            return None
    
    def reply_and_archive(self, 
                         subject_search: str,
                         reply_subject: str,
                         reply_body: str,
                         mailbox: str = "INBOX",
                         cc_addresses: Optional[List[str]] = None) -> bool:
        """
        Find email, reply to it, and archive the original
        
        Args:
            subject_search: Text to search for in original email subject
            reply_subject: Subject for the reply email
            reply_body: Body content for the reply
            mailbox: Mailbox to search (default: INBOX)
            cc_addresses: Optional CC recipients
            
        Returns:
            bool: True if successful, False otherwise
        """
        
        # First, find the email
        email_info = self.find_email_by_subject(subject_search, mailbox)
        if not email_info:
            return False
        
        # Extract sender for reply - fix escape sequences
        reply_subject_escaped = reply_subject.replace('"', '\\"')
        reply_body_escaped = reply_body.replace('"', '\\"').replace('\\', '\\\\')
        
        applescript_reply_archive = f'''
        tell application "Mail"
            set foundEmail to null
            set originalSender to ""
            
            -- Find the email again for reply
            repeat with mailboxItem in mailboxes
                if name of mailboxItem contains "{mailbox}" then
                    repeat with emailItem in messages of mailboxItem
                        set emailSubject to subject of emailItem
                        if emailSubject contains "{subject_search}" then
                            set foundEmail to emailItem
                            set originalSender to (sender of emailItem as string)
                            exit repeat
                        end if
                    end repeat
                    if foundEmail is not null then exit repeat
                end if
            end repeat
            
            if foundEmail is not null then
                -- Extract sender email address
                set senderEmail to (address of sender of foundEmail)
                
                -- Create new reply message
                set newMessage to make new outgoing message with properties {{subject:"{reply_subject_escaped}"}}
                
                tell newMessage
                    make new to recipient at end of to recipients with properties {{address:senderEmail}}
        '''
        
        # Add CC recipients if provided
        if cc_addresses:
            for cc_addr in cc_addresses:
                applescript_reply_archive += f'''
                    make new cc recipient at end of cc recipients with properties {{address:"{cc_addr}"}}
                '''
        
        # Add body and send/archive
        applescript_reply_archive += f'''
                    set content to "{reply_body_escaped}"
                end tell
                
                -- Send the reply automatically
                send newMessage
                
                -- Archive the original email
                set mailbox of foundEmail to mailbox "Archive"
                
                return "SUCCESS: Reply sent to " & senderEmail & " and original archived"
            else
                return "ERROR: Email not found for reply"
            end if
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript_reply_archive], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and "SUCCESS:" in result.stdout:
                print("✅ Reply sent and original email archived!")
                print(f"📧 Subject: {reply_subject}")
                print(f"📝 Original search: {subject_search}")
                
                # Log the action
                self._log_action("reply_and_archive", {
                    "original_subject_search": subject_search,
                    "reply_subject": reply_subject,
                    "mailbox": mailbox,
                    "status": "success"
                })
                return True
            else:
                print("❌ Error in reply and archive process:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def quick_reply_to_latest(self, 
                             reply_subject: str,
                             reply_body: str,
                             sender_filter: Optional[str] = None) -> bool:
        """
        Reply to the most recent email in inbox and archive it
        
        Args:
            reply_subject: Subject for the reply
            reply_body: Body content for the reply  
            sender_filter: Optional filter for sender email/name
            
        Returns:
            bool: True if successful, False otherwise
        """
        
        # Fix escape sequences for quick reply
        reply_subject_escaped = reply_subject.replace('"', '\\"')
        reply_body_escaped = reply_body.replace('"', '\\"').replace('\\', '\\\\')
        
        applescript = f'''
        tell application "Mail"
            set latestEmail to null
            set senderEmail to ""
            
            -- Get the most recent email from inbox
            repeat with mailboxItem in mailboxes
                if name of mailboxItem contains "INBOX" then
                    if (count of messages of mailboxItem) > 0 then
                        set latestEmail to message 1 of mailboxItem
                        set senderEmail to (address of sender of latestEmail)
                        
        '''
        
        # Add sender filter if provided
        if sender_filter:
            applescript += f'''
                        -- Check sender filter
                        if senderEmail does not contain "{sender_filter}" and (name of sender of latestEmail) does not contain "{sender_filter}" then
                            set latestEmail to null
                        end if
            '''
        
        applescript += f'''
                        exit repeat
                    end if
                end if
            end repeat
            
            if latestEmail is not null then
                -- Create reply
                set newMessage to make new outgoing message with properties {{subject:"{reply_subject_escaped}"}}
                
                tell newMessage
                    make new to recipient at end of to recipients with properties {{address:senderEmail}}
                    set content to "{reply_body_escaped}"
                end tell
                
                -- Send reply
                send newMessage
                
                -- Archive original
                set mailbox of latestEmail to mailbox "Archive"
                
                return "SUCCESS: Reply sent to " & senderEmail & " and archived"
            else
                return "ERROR: No suitable email found"
            end if
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and "SUCCESS:" in result.stdout:
                print("✅ Quick reply sent and email archived!")
                print(f"📧 Reply subject: {reply_subject}")
                self._log_action("quick_reply", {
                    "reply_subject": reply_subject,
                    "sender_filter": sender_filter,
                    "status": "success"
                })
                return True
            else:
                print("❌ Quick reply failed:", result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error in quick reply: {e}")
            return False
    
    def archive_email_by_subject(self, subject_search: str, mailbox: str = "INBOX") -> bool:
        """
        Archive an email by subject search
        
        Args:
            subject_search: Text to search for in subject
            mailbox: Mailbox to search
            
        Returns:
            bool: True if archived successfully
        """
        
        applescript = f'''
        tell application "Mail"
            repeat with mailboxItem in mailboxes
                if name of mailboxItem contains "{mailbox}" then
                    repeat with emailItem in messages of mailboxItem
                        if (subject of emailItem) contains "{subject_search}" then
                            set mailbox of emailItem to mailbox "Archive"
                            return "SUCCESS: Archived email with subject containing '{subject_search}'"
                        end if
                    end repeat
                end if
            end repeat
            return "ERROR: Email not found"
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=30)
            
            if "SUCCESS:" in result.stdout:
                print(f"✅ Email archived: {subject_search}")
                self._log_action("archive", {"subject_search": subject_search, "status": "success"})
                return True
            else:
                print(f"❌ Archive failed: {subject_search}")
                return False
                
        except Exception as e:
            print(f"❌ Archive error: {e}")
            return False
    
    def _log_action(self, action_type: str, details: Dict):
        """Log email actions for tracking"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action_type,
            "details": details
        }
        
        # Append to log file
        os.makedirs(os.path.dirname(self.actions_log), exist_ok=True)
        with open(self.actions_log, 'a') as f:
            f.write(f"\n## {action_type.upper()} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"- **Action**: {action_type}\n")
            for key, value in details.items():
                f.write(f"- **{key.title()}**: {value}\n")
            f.write("\n---\n")

def main():
    """Command line interface for smart email handling"""
    
    parser = argparse.ArgumentParser(description="Smart Email Handler - Reply and Archive")
    parser.add_argument("--action", choices=["reply", "quick-reply", "archive"], 
                       required=True, help="Action to perform")
    
    # Reply specific args
    parser.add_argument("--subject-search", help="Text to search for in original email subject")
    parser.add_argument("--reply-subject", help="Subject for reply email")
    parser.add_argument("--reply-body", help="Body content for reply")
    parser.add_argument("--sender-filter", help="Filter emails by sender (for quick-reply)")
    
    # General args
    parser.add_argument("--mailbox", default="INBOX", help="Mailbox to search")
    parser.add_argument("--cc", nargs='*', help="CC recipients for reply")
    
    args = parser.parse_args()
    
    handler = SmartEmailHandler()
    
    if args.action == "reply":
        if not all([args.subject_search, args.reply_subject, args.reply_body]):
            print("❌ Reply action requires: --subject-search, --reply-subject, --reply-body")
            sys.exit(1)
        
        success = handler.reply_and_archive(
            subject_search=args.subject_search,
            reply_subject=args.reply_subject,
            reply_body=args.reply_body,
            mailbox=args.mailbox,
            cc_addresses=args.cc
        )
        
    elif args.action == "quick-reply":
        if not all([args.reply_subject, args.reply_body]):
            print("❌ Quick reply requires: --reply-subject, --reply-body")
            sys.exit(1)
        
        success = handler.quick_reply_to_latest(
            reply_subject=args.reply_subject,
            reply_body=args.reply_body,
            sender_filter=args.sender_filter
        )
        
    elif args.action == "archive":
        if not args.subject_search:
            print("❌ Archive action requires: --subject-search")
            sys.exit(1)
        
        success = handler.archive_email_by_subject(
            subject_search=args.subject_search,
            mailbox=args.mailbox
        )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

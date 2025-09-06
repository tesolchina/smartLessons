#!/usr/bin/env python3
"""
Generic Email Sender Script
Sends emails via Mac Mail.app with flexible configuration
Created: September 6, 2025
"""

import subprocess
import sys
import argparse
import json
import os
from typing import List, Optional

class EmailSender:
    """Generic email sender using Mac Mail.app via AppleScript"""
    
    def __init__(self):
        self.sent_emails_log = "operating/email_automation/sent_emails_log.json"
    
    def send_email(self, 
                   to_addresses: List[str],
                   subject: str,
                   body: str,
                   cc_addresses: Optional[List[str]] = None,
                   bcc_addresses: Optional[List[str]] = None,
                   auto_send: bool = False) -> bool:
        """
        Send an email using Mac Mail.app
        
        Args:
            to_addresses: List of recipient email addresses
            subject: Email subject line
            body: Email body content
            cc_addresses: Optional list of CC recipients
            bcc_addresses: Optional list of BCC recipients
            auto_send: If True, send automatically; if False, open for review
        
        Returns:
            bool: True if successful, False otherwise
        """
        
        # Escape quotes and backslashes for AppleScript
        subject_escaped = subject.replace('"', '\\"').replace('\\', '\\\\')
        body_escaped = body.replace('"', '\\"').replace('\\', '\\\\')
        
        # Build recipient lists
        to_list = ', '.join([f'"{addr}"' for addr in to_addresses])
        cc_list = ', '.join([f'"{addr}"' for addr in (cc_addresses or [])])
        bcc_list = ', '.join([f'"{addr}"' for addr in (bcc_addresses or [])])
        
        # Build AppleScript
        applescript = f'''
        tell application "Mail"
            activate
            
            -- Create new email
            set newMessage to make new outgoing message with properties {{subject:"{subject_escaped}", content:"{body_escaped}"}}
            
            -- Add TO recipients
            tell newMessage
        '''
        
        # Add TO recipients
        for addr in to_addresses:
            applescript += f'''
                make new to recipient at end of to recipients with properties {{address:"{addr}"}}
            '''
        
        # Add CC recipients if any
        if cc_addresses:
            for addr in cc_addresses:
                applescript += f'''
                    make new cc recipient at end of cc recipients with properties {{address:"{addr}"}}
                '''
        
        # Add BCC recipients if any
        if bcc_addresses:
            for addr in bcc_addresses:
                applescript += f'''
                    make new bcc recipient at end of bcc recipients with properties {{address:"{addr}"}}
                '''
        
        applescript += '''
            end tell
            
        '''
        
        if auto_send:
            applescript += '''
            -- Send automatically
            send newMessage
            display dialog "Email sent successfully!" with title "Email Sent"
            '''
        else:
            applescript += '''
            -- Open for review by activating the compose window
            activate
            set visible of newMessage to true
            display dialog "Email composed and ready for review. Please check and send manually." with title "Email Ready for Review"
            '''
        
        applescript += '''
        end tell
        '''
        
        try:
            # Execute the AppleScript
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                success_msg = "✅ Email sent successfully!" if auto_send else "✅ Email composed and ready for review!"
                print(success_msg)
                print(f"📧 TO: {', '.join(to_addresses)}")
                print(f"📝 Subject: {subject}")
                
                # Log the email
                self._log_email(to_addresses, subject, body, cc_addresses, bcc_addresses, auto_send)
                return True
            else:
                print("❌ Error with email:")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Script timed out - Mail.app may need attention")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def _log_email(self, to_addresses, subject, body, cc_addresses, bcc_addresses, auto_send):
        """Log sent email to JSON file for tracking"""
        import datetime
        
        email_record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "to": to_addresses,
            "cc": cc_addresses or [],
            "bcc": bcc_addresses or [],
            "subject": subject,
            "body_preview": body[:100] + "..." if len(body) > 100 else body,
            "auto_sent": auto_send
        }
        
        # Load existing log or create new
        log_file = self.sent_emails_log
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {"emails": []}
        
        log_data["emails"].append(email_record)
        
        # Save updated log
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

def main():
    """Command line interface for sending emails"""
    parser = argparse.ArgumentParser(description="Send emails via Mac Mail.app")
    parser.add_argument("--to", required=True, nargs='+', help="Recipient email addresses")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body content")
    parser.add_argument("--cc", nargs='*', help="CC email addresses")
    parser.add_argument("--bcc", nargs='*', help="BCC email addresses")
    parser.add_argument("--auto-send", action="store_true", help="Send automatically without review")
    parser.add_argument("--body-file", help="Read email body from file")
    
    args = parser.parse_args()
    
    # Read body from file if specified
    email_body = args.body
    if args.body_file:
        with open(args.body_file, 'r') as f:
            email_body = f.read()
    
    # Create sender and send email
    sender = EmailSender()
    success = sender.send_email(
        to_addresses=args.to,
        subject=args.subject,
        body=email_body,
        cc_addresses=args.cc,
        bcc_addresses=args.bcc,
        auto_send=args.auto_send
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

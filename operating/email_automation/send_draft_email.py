#!/usr/bin/env python3
"""
Email Draft Parser and Sender
Parses email drafts and sends them using the generic email sender
Created: September 6, 2025
"""

import re
import os
from typing import Optional
from generic_email_sender import EmailSender
from email_address_extractor import EmailAddressExtractor

class EmailDraftParser:
    """Parse email drafts in markdown format and extract email components"""
    
    def parse_draft(self, draft_file_path: str) -> dict:
        """
        Parse an email draft file and extract email components
        
        Args:
            draft_file_path: Path to the markdown draft file
            
        Returns:
            dict: Parsed email components
        """
        with open(draft_file_path, 'r') as f:
            content = f.read()
        
        # Extract metadata
        to_match = re.search(r'\*\*To\*\*:\s*(.+)', content)
        subject_match = re.search(r'\*\*Subject\*\*:\s*(.+)', content)
        
        # Extract email body (content between ## Email Content and ---)
        body_match = re.search(r'## Email Content\n\n(.+?)\n\n---', content, re.DOTALL)
        
        parsed = {
            'to': to_match.group(1).strip() if to_match else None,
            'subject': subject_match.group(1).strip() if subject_match else None,
            'body': body_match.group(1).strip() if body_match else None,
            'original_draft': content
        }
        
        return parsed
    
    def send_draft(self, draft_file_path: str, recipient_email: Optional[str] = None, auto_send: bool = False) -> bool:
        """
        Parse a draft file and send the email
        
        Args:
            draft_file_path: Path to the draft file
            recipient_email: Override recipient email (if None, will prompt)
            auto_send: Whether to send automatically or open for review
            
        Returns:
            bool: True if successful
        """
        try:
            parsed = self.parse_draft(draft_file_path)
            
            if not parsed['subject'] or not parsed['body']:
                print("❌ Could not parse subject or body from draft file")
                return False
            
            # Get recipient email
            if not recipient_email:
                # Try to extract email automatically for specific cases
                if "sophie" in draft_file_path.lower() and "sick" in draft_file_path.lower():
                    print("🔍 Attempting to find Sophie's email automatically...")
                    extractor = EmailAddressExtractor()
                    
                    # Search for Sophie's sick leave email
                    search_terms = [
                        "UE1 section 37 request for sick leave",
                        "sick leave for today's lesson",
                        "UE1 section 37"
                    ]
                    
                    for term in search_terms:
                        result = extractor.search_and_extract_sender(term)
                        if result:
                            print(f"✅ Found Sophie's email: {result['email']}")
                            recipient_email = result['email']
                            break
                    
                    if not recipient_email:
                        print("❌ Could not find Sophie's email automatically")
                
                # If still no email, prompt user
                if not recipient_email:
                    recipient_email = input(f"Enter recipient email address (parsed: {parsed['to']}): ").strip()
                    if not recipient_email:
                        print("❌ No recipient email provided")
                        return False
            
            # Send email
            sender = EmailSender()
            return sender.send_email(
                to_addresses=[recipient_email],
                subject=parsed['subject'],
                body=parsed['body'],
                auto_send=auto_send
            )
            
        except Exception as e:
            print(f"❌ Error processing draft: {e}")
            return False

def main():
    """Command line interface for sending draft emails"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Send email drafts via Mac Mail.app")
    parser.add_argument("draft_file", help="Path to email draft file")
    parser.add_argument("--to", help="Recipient email address (overrides draft)")
    parser.add_argument("--auto-send", action="store_true", help="Send automatically without review")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.draft_file):
        print(f"❌ Draft file not found: {args.draft_file}")
        return 1
    
    parser = EmailDraftParser()
    success = parser.send_draft(args.draft_file, args.to, args.auto_send)
    
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())

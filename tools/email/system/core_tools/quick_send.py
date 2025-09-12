#!/usr/bin/env python3
"""
Quick Email Sender
Convenient wrapper for common email sending scenarios
Created: September 6, 2025
"""

import os
import sys
from send_draft_email import EmailDraftParser
from generic_email_sender import EmailSender

def send_sophie_sick_leave():
    """Send Sophie's sick leave response"""
    print("📧 Sending Sophie's sick leave response...")
    
    # You can update this with Sophie's actual email when known
    sophie_email = input("Enter Sophie's email address: ").strip()
    
    if not sophie_email:
        print("❌ No email address provided")
        return False
    
    draft_file = "operating/email_automation/email_drafts/draft_sophie_sick_leave_response.md"
    
    parser = EmailDraftParser()
    return parser.send_draft(draft_file, sophie_email, auto_send=False)

def quick_send_menu():
    """Interactive menu for quick email sending"""
    print("\n📧 Quick Email Sender")
    print("=" * 30)
    print("1. Send Sophie's sick leave response")
    print("2. Send custom email")
    print("3. Send from draft file")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        return send_sophie_sick_leave()
    elif choice == "2":
        return send_custom_email()
    elif choice == "3":
        return send_from_draft()
    elif choice == "4":
        print("👋 Goodbye!")
        return True
    else:
        print("❌ Invalid choice")
        return False

def send_custom_email():
    """Send a custom email with interactive input"""
    print("\n📝 Custom Email")
    print("-" * 20)
    
    to_email = input("To (email address): ").strip()
    if not to_email:
        print("❌ Email address required")
        return False
    
    subject = input("Subject: ").strip()
    if not subject:
        print("❌ Subject required")
        return False
    
    print("Body (type your message, press Enter twice when done):")
    body_lines = []
    while True:
        line = input()
        if line == "" and body_lines and body_lines[-1] == "":
            break
        body_lines.append(line)
    
    body = "\n".join(body_lines[:-1])  # Remove the last empty line
    
    if not body.strip():
        print("❌ Email body required")
        return False
    
    # Send the email
    sender = EmailSender()
    return sender.send_email([to_email], subject, body, auto_send=False)

def send_from_draft():
    """Send email from a draft file"""
    print("\n📄 Send from Draft File")
    print("-" * 25)
    
    # List available drafts
    drafts_dir = "operating/email_automation/email_drafts/"
    if os.path.exists(drafts_dir):
        print("Available drafts:")
        drafts = [f for f in os.listdir(drafts_dir) if f.endswith('.md')]
        for i, draft in enumerate(drafts, 1):
            print(f"  {i}. {draft}")
        
        if not drafts:
            print("No draft files found")
            return False
        
        try:
            selection = int(input(f"\nSelect draft (1-{len(drafts)}): ").strip())
            if 1 <= selection <= len(drafts):
                draft_file = os.path.join(drafts_dir, drafts[selection-1])
            else:
                print("❌ Invalid selection")
                return False
        except ValueError:
            print("❌ Please enter a number")
            return False
    else:
        draft_file = input("Enter path to draft file: ").strip()
        if not os.path.exists(draft_file):
            print(f"❌ File not found: {draft_file}")
            return False
    
    # Get recipient email
    recipient = input("Recipient email (or press Enter to be prompted later): ").strip()
    recipient = recipient if recipient else None
    
    # Send the draft
    parser = EmailDraftParser()
    return parser.send_draft(draft_file, recipient, auto_send=False)

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line mode
        command = sys.argv[1].lower()
        
        if command == "sophie":
            success = send_sophie_sick_leave()
        elif command == "custom":
            success = send_custom_email()
        elif command == "draft":
            success = send_from_draft()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: sophie, custom, draft")
            success = False
    else:
        # Interactive menu mode
        success = quick_send_menu()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

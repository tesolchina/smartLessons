#!/usr/bin/env python3
"""
Unified Email Workflow System
A comprehensive tool for managing email operations in Mac Mail.app
- Locate emails by subject, sender, or content
- Reply with proper threading
- Forward emails
- Archive emails
- Contact management integration
Created: September 6, 2025
"""

import subprocess
import sys
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# Add core_tools to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'core_tools'))
from generic_email_sender import EmailSender
from email_address_extractor import EmailAddressExtractor
from email_reply_system import EmailReplySystem

class EmailWorkflow:
    """Unified email workflow management"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.contacts_file = self.base_path / "contacts" / "email_contacts.json"
        self.sender = EmailSender()
        self.extractor = EmailAddressExtractor()
        self.reply_system = EmailReplySystem()
        self.ensure_contacts_file()
    
    def ensure_contacts_file(self):
        """Create contacts file if it doesn't exist"""
        self.contacts_file.parent.mkdir(exist_ok=True)
        if not self.contacts_file.exists():
            default_contacts = {
                "colleagues": [
                    {"name": "Nancy", "email": "nancymak@hkbu.edu.hk", "department": "Language Centre"},
                    {"name": "Joshua", "email": "joshuachan@hkbu.edu.hk", "department": "Language Centre"}
                ],
                "students": [],
                "recent": []
            }
            with open(self.contacts_file, 'w') as f:
                json.dump(default_contacts, f, indent=2)
    
    def locate_email(self, search_term: str, search_type: str = "subject") -> Dict:
        """
        Locate an email by different search criteria
        
        Args:
            search_term: Term to search for
            search_type: Type of search - "subject", "sender", "content"
            
        Returns:
            Dict with email details
        """
        print(f"🔍 Searching for emails by {search_type}: '{search_term}'")
        
        if search_type == "subject":
            applescript = f'''
            tell application "Mail"
                set foundEmails to {{}}
                repeat with acct in accounts
                    repeat with mbox in mailboxes of acct
                        set messages_list to (every message in mbox whose subject contains "{search_term}")
                        if (count of messages_list) > 0 then
                            repeat with msg in messages_list
                                set email_info to "Subject: " & (subject of msg) & "\\n"
                                set email_info to email_info & "From: " & (sender of msg) & "\\n"
                                set email_info to email_info & "Date: " & (date received of msg) & "\\n"
                                set email_info to email_info & "Account: " & (name of acct) & "\\n"
                                set email_info to email_info & "Mailbox: " & (name of mbox) & "\\n---\\n"
                                set end of foundEmails to email_info
                            end repeat
                        end if
                    end repeat
                end repeat
                return (foundEmails as string)
            end tell
            '''
        elif search_type == "sender":
            applescript = f'''
            tell application "Mail"
                set foundEmails to {{}}
                repeat with acct in accounts
                    repeat with mbox in mailboxes of acct
                        set messages_list to (every message in mbox whose sender contains "{search_term}")
                        if (count of messages_list) > 0 then
                            repeat with msg in messages_list
                                set email_info to "Subject: " & (subject of msg) & "\\n"
                                set email_info to email_info & "From: " & (sender of msg) & "\\n"
                                set email_info to email_info & "Date: " & (date received of msg) & "\\n---\\n"
                                set end of foundEmails to email_info
                            end repeat
                        end if
                    end repeat
                end repeat
                return (foundEmails as string)
            end tell
            '''
        else:  # content search
            applescript = f'''
            tell application "Mail"
                set foundEmails to {{}}
                repeat with acct in accounts
                    repeat with mbox in mailboxes of acct
                        set messages_list to (every message in mbox whose content contains "{search_term}")
                        if (count of messages_list) > 0 then
                            repeat with msg in messages_list
                                set email_info to "Subject: " & (subject of msg) & "\\n"
                                set email_info to email_info & "From: " & (sender of msg) & "\\n"
                                set email_info to email_info & "Date: " & (date received of msg) & "\\n---\\n"
                                set end of foundEmails to email_info
                            end repeat
                        end if
                    end repeat
                end repeat
                return (foundEmails as string)
            end tell
            '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                 capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return {"status": "found", "results": result.stdout.strip()}
            else:
                return {"status": "not_found", "results": "No emails found"}
        except Exception as e:
            return {"status": "error", "results": str(e)}
    
    def reply_to_email(self, search_term: str, reply_content: str, 
                      reply_all: bool = False, auto_send: bool = False) -> bool:
        """
        Reply to an email with proper threading
        
        Args:
            search_term: Subject or identifier to find original email
            reply_content: Content for the reply
            reply_all: Whether to reply to all recipients
            auto_send: Whether to send automatically or draft
            
        Returns:
            bool: Success status
        """
        print(f"📧 Creating reply for: '{search_term}'")
        
        # Get original message
        original = self.reply_system.get_original_message(search_term)
        if not original:
            print("❌ Could not find original message")
            return False
        
        # Create reply
        success = self.reply_system.create_reply_email(
            original_sender=original.get('sender_email'),
            original_subject=original.get('subject'),
            reply_content=reply_content,
            reply_all=reply_all,
            auto_send=auto_send
        )
        
        if success:
            print("✅ Reply created successfully")
        else:
            print("❌ Failed to create reply")
        
        return success
    
    def forward_email(self, search_term: str, forward_to: str, 
                     forward_message: str = "", auto_send: bool = False) -> bool:
        """
        Forward an email to specified recipient
        
        Args:
            search_term: Subject or identifier to find email
            forward_to: Email address to forward to
            forward_message: Additional message to include
            auto_send: Whether to send automatically
            
        Returns:
            bool: Success status
        """
        print(f"📤 Forwarding email about '{search_term}' to {forward_to}")
        
        applescript = f'''
        tell application "Mail"
            set targetMessage to missing value
            repeat with acct in accounts
                repeat with mbox in mailboxes of acct
                    set foundMessages to (every message in mbox whose subject contains "{search_term}")
                    if (count of foundMessages) > 0 then
                        set targetMessage to item 1 of foundMessages
                        exit repeat
                    end if
                end repeat
                if targetMessage is not missing value then exit repeat
            end repeat
            
            if targetMessage is not missing value then
                set forwardMessage to forward targetMessage
                set to recipient of forwardMessage to "{forward_to}"
                set content of forwardMessage to "{forward_message}" & return & return & (content of forwardMessage)
                {"send" if auto_send else "activate"}
                return "success"
            else
                return "not_found"
            end if
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                 capture_output=True, text=True)
            return result.returncode == 0 and "success" in result.stdout
        except Exception as e:
            print(f"❌ Error forwarding email: {e}")
            return False
    
    def archive_email(self, search_term: str) -> bool:
        """Archive an email by moving it to Archive folder"""
        print(f"🗃️ Archiving email: '{search_term}'")
        
        applescript = f'''
        tell application "Mail"
            set targetMessage to missing value
            repeat with acct in accounts
                repeat with mbox in mailboxes of acct
                    set foundMessages to (every message in mbox whose subject contains "{search_term}")
                    if (count of foundMessages) > 0 then
                        set targetMessage to item 1 of foundMessages
                        
                        -- Try to find Archive mailbox
                        repeat with archiveMbox in mailboxes of acct
                            if name of archiveMbox contains "Archive" then
                                move targetMessage to archiveMbox
                                return "archived"
                            end if
                        end repeat
                        
                        -- If no Archive folder, just delete
                        delete targetMessage
                        return "deleted"
                    end if
                end repeat
            end repeat
            return "not_found"
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                 capture_output=True, text=True)
            if "archived" in result.stdout:
                print("✅ Email archived")
                return True
            elif "deleted" in result.stdout:
                print("✅ Email deleted (no archive folder)")
                return True
            else:
                print("❌ Email not found")
                return False
        except Exception as e:
            print(f"❌ Error archiving email: {e}")
            return False
    
    def add_contact(self, name: str, email: str, category: str = "recent") -> bool:
        """Add a contact to the contacts database"""
        try:
            with open(self.contacts_file, 'r') as f:
                contacts = json.load(f)
            
            contact = {"name": name, "email": email, "added": datetime.now().isoformat()}
            
            if category not in contacts:
                contacts[category] = []
            
            # Check if contact already exists
            existing = [c for c in contacts[category] if c['email'].lower() == email.lower()]
            if not existing:
                contacts[category].append(contact)
                
                with open(self.contacts_file, 'w') as f:
                    json.dump(contacts, f, indent=2)
                
                print(f"✅ Added {name} ({email}) to {category}")
                return True
            else:
                print(f"ℹ️ Contact {email} already exists")
                return True
        except Exception as e:
            print(f"❌ Error adding contact: {e}")
            return False
    
    def search_contacts(self, search_term: str) -> List[Dict]:
        """Search contacts by name or email"""
        try:
            with open(self.contacts_file, 'r') as f:
                contacts = json.load(f)
            
            results = []
            for category, contact_list in contacts.items():
                for contact in contact_list:
                    if (search_term.lower() in contact['name'].lower() or 
                        search_term.lower() in contact['email'].lower()):
                        contact['category'] = category
                        results.append(contact)
            
            return results
        except Exception as e:
            print(f"❌ Error searching contacts: {e}")
            return []
    
    def show_menu(self):
        """Display the main workflow menu"""
        print("\n" + "="*60)
        print("📧 EMAIL WORKFLOW SYSTEM")
        print("="*60)
        print("1. Locate email by subject")
        print("2. Locate email by sender")
        print("3. Locate email by content")
        print("4. Reply to email")
        print("5. Reply all to email")
        print("6. Forward email")
        print("7. Archive email")
        print("8. Add contact")
        print("9. Search contacts")
        print("10. View contacts")
        print("0. Exit")
        print("="*60)
    
    def view_contacts(self):
        """Display all contacts organized by category"""
        try:
            with open(self.contacts_file, 'r') as f:
                contacts = json.load(f)
            
            print("\n📇 CONTACTS DATABASE")
            print("="*40)
            for category, contact_list in contacts.items():
                if contact_list:
                    print(f"\n📁 {category.upper()}:")
                    for i, contact in enumerate(contact_list, 1):
                        print(f"  {i}. {contact['name']} <{contact['email']}>")
        except Exception as e:
            print(f"❌ Error viewing contacts: {e}")

def main():
    """Main workflow interface"""
    workflow = EmailWorkflow()
    
    while True:
        workflow.show_menu()
        choice = input("\nSelect option (0-10): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            search_term = input("Enter subject to search: ").strip()
            if search_term:
                result = workflow.locate_email(search_term, "subject")
                print(f"\n{result['results']}")
        elif choice == "2":
            search_term = input("Enter sender name/email: ").strip()
            if search_term:
                result = workflow.locate_email(search_term, "sender")
                print(f"\n{result['results']}")
        elif choice == "3":
            search_term = input("Enter content to search: ").strip()
            if search_term:
                result = workflow.locate_email(search_term, "content")
                print(f"\n{result['results']}")
        elif choice == "4":
            search_term = input("Enter subject of email to reply to: ").strip()
            reply_content = input("Enter your reply: ").strip()
            if search_term and reply_content:
                workflow.reply_to_email(search_term, reply_content, reply_all=False)
        elif choice == "5":
            search_term = input("Enter subject of email to reply all: ").strip()
            reply_content = input("Enter your reply: ").strip()
            if search_term and reply_content:
                workflow.reply_to_email(search_term, reply_content, reply_all=True)
        elif choice == "6":
            search_term = input("Enter subject of email to forward: ").strip()
            forward_to = input("Forward to (email): ").strip()
            message = input("Additional message (optional): ").strip()
            if search_term and forward_to:
                workflow.forward_email(search_term, forward_to, message)
        elif choice == "7":
            search_term = input("Enter subject of email to archive: ").strip()
            if search_term:
                workflow.archive_email(search_term)
        elif choice == "8":
            name = input("Contact name: ").strip()
            email = input("Contact email: ").strip()
            category = input("Category (colleagues/students/recent): ").strip() or "recent"
            if name and email:
                workflow.add_contact(name, email, category)
        elif choice == "9":
            search_term = input("Search contacts: ").strip()
            if search_term:
                results = workflow.search_contacts(search_term)
                if results:
                    print(f"\n🔍 Found {len(results)} contact(s):")
                    for contact in results:
                        print(f"  {contact['name']} <{contact['email']}> ({contact['category']})")
                else:
                    print("No contacts found")
        elif choice == "10":
            workflow.view_contacts()
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()

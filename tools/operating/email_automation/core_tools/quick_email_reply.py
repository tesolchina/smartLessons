#!/usr/bin/env python3
"""
Quick Email Reply - Simplified Interface
For common reply-and-archive workflows
Created: September 6, 2025
"""

import sys
import os
from smart_email_handler import SmartEmailHandler

def main():
    """Interactive interface for quick email replies"""
    
    handler = SmartEmailHandler()
    
    print("\n📧 Quick Email Reply & Archive")
    print("=" * 40)
    print("1. Reply to specific email by subject")
    print("2. Quick reply to latest email")
    print("3. Archive email only")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        # Reply to specific email
        subject_search = input("Enter text to search for in subject: ").strip()
        if not subject_search:
            print("❌ Subject search required")
            return
        
        reply_subject = input("Enter reply subject: ").strip()
        if not reply_subject:
            print("❌ Reply subject required")
            return
            
        print("\nEnter reply body (press Enter twice to finish):")
        reply_lines = []
        while True:
            line = input()
            if line == "" and len(reply_lines) > 0:
                break
            reply_lines.append(line)
        
        reply_body = "\n".join(reply_lines)
        
        print(f"\n📧 Searching for email with subject containing: '{subject_search}'")
        print(f"📝 Reply subject: {reply_subject}")
        print(f"✉️ Sending reply and archiving original...")
        
        success = handler.reply_and_archive(
            subject_search=subject_search,
            reply_subject=reply_subject,
            reply_body=reply_body
        )
        
        if success:
            print("✅ Email replied and archived successfully!")
        else:
            print("❌ Failed to reply and archive email")
    
    elif choice == "2":
        # Quick reply to latest
        reply_subject = input("Enter reply subject: ").strip()
        if not reply_subject:
            print("❌ Reply subject required")
            return
        
        print("\nEnter reply body (press Enter twice to finish):")
        reply_lines = []
        while True:
            line = input()
            if line == "" and len(reply_lines) > 0:
                break
            reply_lines.append(line)
        
        reply_body = "\n".join(reply_lines)
        
        sender_filter = input("Filter by sender (optional, press Enter to skip): ").strip()
        sender_filter = sender_filter if sender_filter else None
        
        print(f"\n📧 Replying to latest email in inbox")
        print(f"📝 Reply subject: {reply_subject}")
        if sender_filter:
            print(f"🔍 Sender filter: {sender_filter}")
        print(f"✉️ Sending reply and archiving original...")
        
        success = handler.quick_reply_to_latest(
            reply_subject=reply_subject,
            reply_body=reply_body,
            sender_filter=sender_filter
        )
        
        if success:
            print("✅ Quick reply sent and archived successfully!")
        else:
            print("❌ Failed to send quick reply")
    
    elif choice == "3":
        # Archive only
        subject_search = input("Enter text to search for in subject to archive: ").strip()
        if not subject_search:
            print("❌ Subject search required")
            return
        
        print(f"\n📧 Searching for email with subject containing: '{subject_search}'")
        print(f"📁 Archiving email...")
        
        success = handler.archive_email_by_subject(subject_search)
        
        if success:
            print("✅ Email archived successfully!")
        else:
            print("❌ Failed to archive email")
    
    elif choice == "4":
        print("👋 Goodbye!")
        return
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()

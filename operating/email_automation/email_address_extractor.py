#!/usr/bin/env python3
"""
Email Address Extractor
Retrieve sender's email address from Mail.app by searching for specific emails
Created: September 6, 2025
"""

import subprocess
import json
import re
from typing import Optional, Dict, List

class EmailAddressExtractor:
    """Extract email addresses from Mail.app messages"""
    
    def search_and_extract_sender(self, search_term: str) -> Optional[Dict[str, str]]:
        """
        Search for an email in Mail.app and extract sender information
        
        Args:
            search_term: Subject line or content to search for
            
        Returns:
            Dict with sender name and email, or None if not found
        """
        
        applescript = f'''
        tell application "Mail"
            set searchResults to {{}}
            
            -- Search in all mailboxes
            repeat with eachAccount in accounts
                repeat with eachMailbox in mailboxes of eachAccount
                    try
                        set foundMessages to (messages of eachMailbox whose subject contains "{search_term}")
                        if (count of foundMessages) > 0 then
                            -- Get the first matching message
                            set firstMessage to item 1 of foundMessages
                            set senderName to sender of firstMessage
                            set senderEmail to ""
                            
                            -- Extract email from sender string (format: "Name <email@domain.com>")
                            if senderName contains "<" and senderName contains ">" then
                                set senderEmail to text ((offset of "<" in senderName) + 1) thru ((offset of ">" in senderName) - 1) of senderName
                                set senderName to text 1 thru ((offset of "<" in senderName) - 2) of senderName
                            else
                                set senderEmail to senderName
                                set senderName to senderName
                            end if
                            
                            return "SENDER_INFO:" & senderName & "|" & senderEmail & "|" & subject of firstMessage
                        end if
                    end try
                end repeat
            end repeat
            
            return "NO_MATCH_FOUND"
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                
                if output.startswith("SENDER_INFO:"):
                    # Parse the result
                    info_part = output.replace("SENDER_INFO:", "")
                    parts = info_part.split("|")
                    
                    if len(parts) >= 3:
                        return {
                            "name": parts[0].strip(),
                            "email": parts[1].strip(),
                            "subject": parts[2].strip()
                        }
                elif output == "NO_MATCH_FOUND":
                    print(f"❌ No email found with search term: '{search_term}'")
                    return None
                    
            else:
                print(f"❌ Error searching emails: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⏰ Search timed out - Mail.app may be busy")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def get_recent_senders(self, mailbox_name: str = "INBOX", limit: int = 10) -> List[Dict[str, str]]:
        """
        Get recent email senders from a specific mailbox
        
        Args:
            mailbox_name: Name of mailbox to search
            limit: Maximum number of senders to return
            
        Returns:
            List of dictionaries with sender information
        """
        
        applescript = f'''
        tell application "Mail"
            set recentSenders to {{}}
            
            try
                -- Get messages from inbox (recent first)
                set recentMessages to messages 1 thru {limit} of mailbox "INBOX" of account 1
                
                repeat with eachMessage in recentMessages
                    set senderName to sender of eachMessage
                    set messageSubject to subject of eachMessage
                    set senderEmail to ""
                    
                    -- Extract email from sender string
                    if senderName contains "<" and senderName contains ">" then
                        set senderEmail to text ((offset of "<" in senderName) + 1) thru ((offset of ">" in senderName) - 1) of senderName
                        set senderName to text 1 thru ((offset of "<" in senderName) - 2) of senderName
                    else
                        set senderEmail to senderName
                    end if
                    
                    set end of recentSenders to "SENDER:" & senderName & "|" & senderEmail & "|" & messageSubject
                end repeat
                
                return my list_to_string(recentSenders, "\\n")
            on error errMsg
                return "ERROR:" & errMsg
            end try
        end tell
        
        on list_to_string(lst, delim)
            set AppleScript's text item delimiters to delim
            set str to lst as string
            set AppleScript's text item delimiters to ""
            return str
        end list_to_string
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                output = result.stdout.strip()
                senders = []
                
                for line in output.split('\n'):
                    if line.startswith("SENDER:"):
                        info_part = line.replace("SENDER:", "")
                        parts = info_part.split("|")
                        
                        if len(parts) >= 3:
                            senders.append({
                                "name": parts[0].strip(),
                                "email": parts[1].strip(),
                                "subject": parts[2].strip()
                            })
                
                return senders
            else:
                print(f"❌ Error getting recent senders: {result.stderr}")
                return []
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return []

def find_sophie_email():
    """Specific function to find Sophie's email from her sick leave message"""
    extractor = EmailAddressExtractor()
    
    # Search terms for Sophie's sick leave email
    search_terms = [
        "UE1 section 37 request for sick leave",
        "sick leave for today's lesson",
        "UE1 section 37"
    ]
    
    print("🔍 Searching for Sophie's email...")
    
    for term in search_terms:
        print(f"   Searching for: '{term}'")
        result = extractor.search_and_extract_sender(term)
        
        if result:
            print(f"✅ Found email from: {result['name']} <{result['email']}>")
            print(f"   Subject: {result['subject']}")
            return result['email']
    
    print("❌ Could not find Sophie's email automatically")
    print("💡 Trying to get recent senders...")
    
    # Fallback: show recent senders
    recent_senders = extractor.get_recent_senders(limit=20)
    if recent_senders:
        print("\n📧 Recent email senders:")
        for i, sender in enumerate(recent_senders, 1):
            print(f"   {i:2d}. {sender['name']} <{sender['email']}>")
            print(f"       Subject: {sender['subject'][:60]}...")
        
        # Ask user to select
        try:
            choice = input(f"\nSelect Sophie's email (1-{len(recent_senders)}) or press Enter to skip: ")
            if choice.strip():
                idx = int(choice) - 1
                if 0 <= idx < len(recent_senders):
                    selected = recent_senders[idx]
                    print(f"✅ Selected: {selected['email']}")
                    return selected['email']
        except ValueError:
            pass
    
    return None

def main():
    """Command line interface"""
    import sys
    
    if len(sys.argv) > 1:
        search_term = " ".join(sys.argv[1:])
        extractor = EmailAddressExtractor()
        result = extractor.search_and_extract_sender(search_term)
        
        if result:
            print(f"Name: {result['name']}")
            print(f"Email: {result['email']}")
            print(f"Subject: {result['subject']}")
        else:
            print("No matching email found")
    else:
        # Interactive mode - find Sophie specifically
        sophie_email = find_sophie_email()
        if sophie_email:
            print(f"\n📧 Sophie's email: {sophie_email}")
        else:
            print("\n❌ Could not determine Sophie's email address")

if __name__ == "__main__":
    main()

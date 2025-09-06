#!/usr/bin/env python3
"""
Email Reply System
Creates proper replies with original message content included
Created: September 6, 2025
"""

import subprocess
import re
from typing import Optional, Dict
from email_address_extractor import EmailAddressExtractor

class EmailReplySystem:
    """Handle email replies with original message threading"""
    
    def get_original_message(self, search_term: str) -> Optional[Dict[str, str]]:
        """
        Retrieve the full original message for replying
        
        Args:
            search_term: Subject or content to search for
            
        Returns:
            Dict with message details including full content
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
                            set originalMessage to item 1 of foundMessages
                            
                            set senderName to sender of originalMessage
                            set messageSubject to subject of originalMessage
                            set messageContent to content of originalMessage
                            set messageDate to (date received of originalMessage) as string
                            
                            -- Extract email from sender string
                            set senderEmail to ""
                            if senderName contains "<" and senderName contains ">" then
                                set senderEmail to text ((offset of "<" in senderName) + 1) thru ((offset of ">" in senderName) - 1) of senderName
                                set senderName to text 1 thru ((offset of "<" in senderName) - 2) of senderName
                            else
                                set senderEmail to senderName
                            end if
                            
                            -- Return formatted message info
                            return "ORIGINAL_MESSAGE:" & senderName & "|" & senderEmail & "|" & messageSubject & "|" & messageDate & "|" & messageContent
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
                
                if output.startswith("ORIGINAL_MESSAGE:"):
                    # Parse the result
                    info_part = output.replace("ORIGINAL_MESSAGE:", "")
                    parts = info_part.split("|", 4)  # Split into max 5 parts
                    
                    if len(parts) >= 5:
                        return {
                            "sender_name": parts[0].strip(),
                            "sender_email": parts[1].strip(),
                            "subject": parts[2].strip(),
                            "date": parts[3].strip(),
                            "content": parts[4].strip()
                        }
                elif output == "NO_MATCH_FOUND":
                    print(f"❌ No email found with search term: '{search_term}'")
                    return None
                    
            else:
                print(f"❌ Error retrieving original message: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⏰ Search timed out - Mail.app may be busy")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def create_reply_email(self, 
                          original_message: Dict[str, str],
                          reply_content: str,
                          auto_send: bool = False) -> bool:
        """
        Create a proper reply email with original message included
        
        Args:
            original_message: Original message details from get_original_message
            reply_content: Your reply content
            auto_send: Whether to send automatically
            
        Returns:
            bool: True if successful
        """
        
        # Format the reply subject (add "Re: " if not already there)
        reply_subject = original_message["subject"]
        if not reply_subject.lower().startswith("re:"):
            reply_subject = f"Re: {reply_subject}"
        
        # Create the full reply body with original message
        reply_body = f'''{reply_content}

---

On {original_message["date"]}, {original_message["sender_name"]} <{original_message["sender_email"]}> wrote:

{original_message["content"]}'''
        
        # Escape content for AppleScript
        subject_escaped = reply_subject.replace('"', '\\"').replace('\\', '\\\\')
        body_escaped = reply_body.replace('"', '\\"').replace('\\', '\\\\')
        sender_email = original_message["sender_email"]
        
        applescript = f'''
        tell application "Mail"
            activate
            
            -- Create new reply message
            set replyMessage to make new outgoing message with properties {{subject:"{subject_escaped}", content:"{body_escaped}"}}
            
            -- Add recipient (reply to original sender)
            tell replyMessage
                make new to recipient at end of to recipients with properties {{address:"{sender_email}"}}
            end tell
            
        '''
        
        if auto_send:
            applescript += '''
            -- Send automatically
            send replyMessage
            display dialog "Reply sent successfully!" with title "Reply Sent"
            '''
        else:
            applescript += '''
            -- Open for review
            activate
            set visible of replyMessage to true
            display dialog "Reply composed and ready for review. Please check and send manually." with title "Reply Ready"
            '''
        
        applescript += '''
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', applescript], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                success_msg = "✅ Reply sent!" if auto_send else "✅ Reply composed and ready!"
                print(success_msg)
                print(f"📧 TO: {sender_email}")
                print(f"📝 Subject: {reply_subject}")
                return True
            else:
                print("❌ Error creating reply:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False

def reply_to_sophie_sick_leave():
    """Specific function to reply to Sophie's sick leave email"""
    print("🔍 Finding Sophie's original sick leave email...")
    
    reply_system = EmailReplySystem()
    
    # Search for Sophie's original message
    search_terms = [
        "UE1 section 37 request for sick leave",
        "sick leave for today's lesson"
    ]
    
    original_message = None
    for term in search_terms:
        original_message = reply_system.get_original_message(term)
        if original_message:
            break
    
    if not original_message:
        print("❌ Could not find Sophie's original email")
        return False
    
    print(f"✅ Found original email from: {original_message['sender_name']} <{original_message['sender_email']}>")
    
    # Read the reply content from our draft
    draft_file = "operating/email_automation/email_drafts/draft_sophie_sick_leave_response.md"
    
    try:
        with open(draft_file, 'r') as f:
            draft_content = f.read()
        
        # Extract just the email body from the draft (between ## Email Content and ---)
        body_match = re.search(r'## Email Content\n\n(.+?)\n\n---', draft_content, re.DOTALL)
        if body_match:
            reply_content = body_match.group(1).strip()
        else:
            print("❌ Could not extract email content from draft")
            return False
        
        print("📝 Creating reply with original message included...")
        return reply_system.create_reply_email(original_message, reply_content, auto_send=False)
        
    except Exception as e:
        print(f"❌ Error reading draft: {e}")
        return False

def main():
    """Command line interface"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "sophie":
            reply_to_sophie_sick_leave()
        else:
            search_term = " ".join(sys.argv[1:])
            reply_system = EmailReplySystem()
            original = reply_system.get_original_message(search_term)
            if original:
                print(f"Found: {original['sender_name']} <{original['sender_email']}>")
                print(f"Subject: {original['subject']}")
                print(f"Date: {original['date']}")
                print(f"Content preview: {original['content'][:200]}...")
    else:
        # Default: Reply to Sophie
        reply_to_sophie_sick_leave()

if __name__ == "__main__":
    main()

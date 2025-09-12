#!/usr/bin/env python3
"""
Simple Mail App Email Search
Quick search for screening test emails in Mac Mail app
"""

import subprocess
from datetime import datetime

def quick_mail_search():
    """
    Quick search for recent emails containing key terms
    """
    applescript = '''
    tell application "Mail"
        set recentEmails to {}
        
        try
            -- Search in inbox and sent items for recent emails
            set inboxFolder to inbox
            set sentFolder to sent mailbox
            
            -- Search inbox
            set inboxMessages to (every message in inboxFolder whose date received > (current date) - (7 * days) and (subject contains "River" or subject contains "screening" or subject contains "test" or subject contains "simon" or sender contains "River"))
            
            repeat with msg in inboxMessages
                set emailInfo to "INBOX: " & (subject of msg) & " | FROM: " & (sender of msg) & " | DATE: " & (date received of msg)
                set end of recentEmails to emailInfo
            end repeat
            
            -- Search sent items  
            set sentMessages to (every message in sentFolder whose date sent > (current date) - (7 * days) and (subject contains "River" or subject contains "screening" or subject contains "test" or subject contains "simon"))
            
            repeat with msg in sentMessages
                set emailInfo to "SENT: " & (subject of msg) & " | TO: " & (content of msg) & " | DATE: " & (date sent of msg)
                set end of recentEmails to emailInfo
            end repeat
            
        end try
        
        return recentEmails
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                              capture_output=True, text=True, timeout=30)
        return result.stdout.strip() if result.returncode == 0 else "No results or error occurred"
    except Exception as e:
        return f"Error: {e}"

def main():
    print("🔍 Quick search in Mac Mail app for screening test emails...")
    result = quick_mail_search()
    print(f"📧 Results:\n{result}")
    
    # Save results
    output_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/screening_test/ui_testing/quick_mail_search.md"
    with open(output_file, 'w') as f:
        f.write(f"# Quick Mail Search Results\n\n**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n**Results**:\n```\n{result}\n```\n")
    
    print(f"✅ Results saved to: {output_file}")

if __name__ == "__main__":
    main()

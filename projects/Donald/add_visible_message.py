#!/usr/bin/env python3
"""
Script to add a comment/suggestion to Donald's Google Doc that will definitely be visible.
"""
import sys
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime

# Add the tools path
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant')

# Document ID from the Google Docs URL
DOCUMENT_ID = '1nPsKZbUZUtzyZcR73DZ2mQL8zC6TvA28orVh7g7-LJA'

# Scopes for editing documents and adding comments
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file'
]

def authenticate():
    """Authenticate with Google API"""
    creds = None
    token_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/google/docs/api/token.pickle'
    credentials_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/google/docs/api/credentials.json'
    
    # Load existing token
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists(credentials_path):
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            else:
                print(f"❌ Credentials file not found at {credentials_path}")
                return None
        
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def add_comment_to_document():
    """Add a comment to the document that will be highly visible"""
    try:
        # Authenticate
        creds = authenticate()
        if not creds:
            print("❌ Authentication failed")
            return False
        
        # Build the services
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        
        # First, let's try adding a very visible heading at the beginning
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create a highly visible message with formatting
        message_text = f"""🚨 COPILOT MESSAGE - {timestamp} 🚨

DONALD - IF YOU CAN SEE THIS, THE API IS WORKING!

Your deadline is September 17th (4 days away).
Check your workspace files for completed analysis and charts.

"""

        # Insert at the very beginning with formatting
        requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': message_text
                }
            },
            {
                'updateTextStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': 1 + len(message_text)
                    },
                    'textStyle': {
                        'bold': True,
                        'fontSize': {
                            'magnitude': 14,
                            'unit': 'PT'
                        },
                        'foregroundColor': {
                            'color': {
                                'rgbColor': {
                                    'red': 1.0,
                                    'green': 0.0,
                                    'blue': 0.0
                                }
                            }
                        }
                    },
                    'fields': 'bold,fontSize,foregroundColor'
                }
            }
        ]
        
        print(f"✍️  Adding highly visible message at the beginning...")
        result = docs_service.documents().batchUpdate(
            documentId=DOCUMENT_ID,
            body={'requests': requests}
        ).execute()
        
        print("✅ Formatted message added!")
        
        # Also try adding a comment to the document
        try:
            comment_content = "🤖 GitHub Copilot here! I can see and edit your document. Check the beginning of your doc for my message with next steps for your coursework!"
            
            # Add comment to the title area
            comment_request = {
                'content': comment_content,
                'anchor': {
                    'start': 1,
                    'end': 10
                }
            }
            
            comment_result = drive_service.comments().create(
                fileId=DOCUMENT_ID,
                body=comment_request
            ).execute()
            
            print(f"💬 Comment added! Comment ID: {comment_result.get('id')}")
            
        except Exception as comment_error:
            print(f"⚠️  Could not add comment: {comment_error}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_document_permissions():
    """Check what permissions we have on the document"""
    try:
        creds = authenticate()
        if not creds:
            return False
            
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Get file metadata
        file_info = drive_service.files().get(
            fileId=DOCUMENT_ID,
            fields='name,permissions,owners,shared,writersCanShare'
        ).execute()
        
        print("📋 Document permissions:")
        print(f"Name: {file_info.get('name')}")
        print(f"Shared: {file_info.get('shared')}")
        print(f"Writers can share: {file_info.get('writersCanShare')}")
        
        if 'owners' in file_info:
            print("👑 Owners:")
            for owner in file_info['owners']:
                print(f"  - {owner.get('displayName', 'Unknown')} ({owner.get('emailAddress', 'No email')})")
        
        if 'permissions' in file_info:
            print("🔐 Permissions:")
            for perm in file_info['permissions']:
                print(f"  - {perm.get('type', 'Unknown type')}: {perm.get('role', 'Unknown role')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking permissions: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Step 1: Checking document permissions...")
    check_document_permissions()
    
    print("\n" + "="*60)
    print("✍️  Step 2: Adding highly visible message...")
    add_comment_to_document()
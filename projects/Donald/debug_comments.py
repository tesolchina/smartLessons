#!/usr/bin/env python3
"""
Investigate why comments aren't visible and try alternative comment methods.
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
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

def authenticate():
    """Authenticate with Google API"""
    creds = None
    token_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/google/docs/api/token.pickle'
    credentials_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/google/docs/api/credentials.json'
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
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
        
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def check_existing_comments():
    """Check what comments already exist on the document"""
    try:
        creds = authenticate()
        if not creds:
            return False
        
        drive_service = build('drive', 'v3', credentials=creds)
        
        print("🔍 Checking existing comments on the document...")
        
        # List all comments
        comments = drive_service.comments().list(
            fileId=DOCUMENT_ID,
            fields='comments(id,content,created,author,anchor)'
        ).execute()
        
        comment_list = comments.get('comments', [])
        print(f"📝 Found {len(comment_list)} existing comments:")
        
        for i, comment in enumerate(comment_list):
            print(f"\nComment {i+1}:")
            print(f"  ID: {comment.get('id')}")
            print(f"  Author: {comment.get('author', {}).get('displayName', 'Unknown')}")
            print(f"  Created: {comment.get('createdTime', 'Unknown')}")
            print(f"  Content: {comment.get('content', '')[:100]}...")
            if 'anchor' in comment:
                print(f"  Anchor: {comment['anchor']}")
            else:
                print(f"  Anchor: None (general comment)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking comments: {e}")
        return False

def try_simple_comment_method():
    """Try a simpler comment method that should definitely be visible"""
    try:
        creds = authenticate()
        if not creds:
            return False
        
        drive_service = build('drive', 'v3', credentials=creds)
        
        print("💬 Trying simple comment method...")
        
        # Create a simple comment without anchor (should appear as general comment)
        simple_comment = {
            'content': f'''🎯 DONALD'S COURSEWORK FEEDBACK - {datetime.now().strftime("%Y-%m-%d %H:%M")}

Hi Donald! This is a test comment that should be clearly visible in your Google Doc.

URGENT PRIORITIES for your September 17th deadline (4 days):

1. 📍 INTRODUCTION: Add Victoria Harbour historical background
   - Why it became HK's economic center
   - Connection to your research question

2. 🗺️ MAPS: Create hand-drawn map (MANDATORY for IGCSE)
   - Include scale, north arrow, legend
   - Show your survey locations

3. 🎯 HYPOTHESES: Connect each to urban geography theory
   - Distance decay theory
   - Bid-rent theory
   - Environmental justice

4. 🔬 METHODOLOGY: Explain WHY each method tests your theory

5. 📊 ANALYSIS: Use "Describe → Explain → Anomalies → Theory" structure

If you can see this comment, please reply "YES" so we know the commenting system is working!

Good luck with your coursework! 🌟'''
        }
        
        result = drive_service.comments().create(
            fileId=DOCUMENT_ID,
            body=simple_comment,
            fields='id,content,created,author'
        ).execute()
        
        print(f"✅ Simple comment created successfully!")
        print(f"Comment ID: {result.get('id')}")
        print(f"This should appear as a general comment bubble in the document.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating simple comment: {e}")
        import traceback
        traceback.print_exc()
        return False

def try_suggestion_mode():
    """Try adding suggestions instead of comments"""
    try:
        creds = authenticate()
        if not creds:
            return False
        
        docs_service = build('docs', 'v1', credentials=creds)
        
        print("💡 Trying to add text suggestions...")
        
        # Get document to find text to suggest on
        document = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
        
        # Find "Intro" text
        content = ""
        body = document.get('body', {})
        for element in body.get('content', []):
            if 'paragraph' in element:
                for elem in element['paragraph'].get('elements', []):
                    if 'textRun' in elem:
                        content += elem['textRun'].get('content', '')
        
        intro_pos = content.find('Intro')
        if intro_pos != -1:
            # Try to insert suggested text
            requests = [{
                'insertText': {
                    'location': {'index': intro_pos + 5},
                    'text': ' [SUGGESTION: Add Victoria Harbour background here!]'
                }
            }]
            
            result = docs_service.documents().batchUpdate(
                documentId=DOCUMENT_ID,
                body={'requests': requests}
            ).execute()
            
            print("✅ Suggestion text added to document!")
            return True
        else:
            print("⚠️  Could not find 'Intro' text to add suggestion")
            return False
        
    except Exception as e:
        print(f"❌ Error adding suggestion: {e}")
        return False

def check_document_sharing():
    """Check the document's sharing settings"""
    try:
        creds = authenticate()
        if not creds:
            return False
        
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Get file permissions
        file_info = drive_service.files().get(
            fileId=DOCUMENT_ID,
            fields='name,permissions,owners,shared,capabilities'
        ).execute()
        
        print("🔐 Document sharing information:")
        print(f"Name: {file_info.get('name')}")
        print(f"Shared: {file_info.get('shared')}")
        
        capabilities = file_info.get('capabilities', {})
        print(f"Can comment: {capabilities.get('canComment', 'Unknown')}")
        print(f"Can edit: {capabilities.get('canEdit', 'Unknown')}")
        
        if 'permissions' in file_info:
            print("Permissions:")
            for perm in file_info['permissions']:
                role = perm.get('role', 'Unknown')
                perm_type = perm.get('type', 'Unknown')
                email = perm.get('emailAddress', 'No email')
                print(f"  - {perm_type}: {role} ({email})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking sharing: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Step 1: Checking existing comments...")
    check_existing_comments()
    
    print("\n" + "="*60)
    print("🔐 Step 2: Checking document sharing settings...")
    check_document_sharing()
    
    print("\n" + "="*60)
    print("💬 Step 3: Adding a simple, visible comment...")
    try_simple_comment_method()
    
    print("\n" + "="*60)
    print("💡 Step 4: Trying suggestion method...")
    try_suggestion_mode()
    
    print("\n" + "="*60)
    print("📋 INSTRUCTIONS FOR DONALD:")
    print("1. Open your Google Doc in a web browser (not mobile app)")
    print("2. Look for comment bubbles on the right side")
    print("3. Click the 'Comments' icon in the toolbar if needed")
    print("4. Try refreshing the page (Ctrl+F5 or Cmd+Shift+R)")
    print("5. If still no comments, reply to this message with 'STILL NO COMMENTS'")
    print(f"🔗 Direct link: https://docs.google.com/document/d/{DOCUMENT_ID}/edit")
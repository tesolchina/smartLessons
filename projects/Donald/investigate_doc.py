#!/usr/bin/env python3
"""
Script to investigate Donald's Google Doc structure and try different editing approaches.
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

# Scopes for editing documents
SCOPES = ['https://www.googleapis.com/auth/documents']

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

def investigate_document_structure():
    """Investigate the document structure in detail"""
    try:
        # Authenticate
        creds = authenticate()
        if not creds:
            print("❌ Authentication failed")
            return False
        
        # Build the service
        service = build('docs', 'v1', credentials=creds)
        
        # Get the document with full details
        print(f"🔍 Investigating document structure: {DOCUMENT_ID}")
        document = service.documents().get(documentId=DOCUMENT_ID).execute()
        
        print("📋 Document metadata:")
        print(f"Title: {document.get('title', 'N/A')}")
        print(f"Document ID: {document.get('documentId', 'N/A')}")
        print(f"Revision ID: {document.get('revisionId', 'N/A')}")
        
        # Check if document has tabs/suggestions
        if 'tabs' in document:
            print(f"📑 Document has {len(document['tabs'])} tabs:")
            for i, tab in enumerate(document['tabs']):
                print(f"  Tab {i}: {tab}")
        else:
            print("📄 Document has no tabs (single document)")
        
        # Check suggestions
        if 'suggestedChanges' in document:
            print(f"💭 Document has {len(document['suggestedChanges'])} suggested changes")
        
        # Analyze the body structure
        body = document.get('body', {})
        content = body.get('content', [])
        
        print(f"\n📊 Document body analysis:")
        print(f"Total content elements: {len(content)}")
        
        for i, element in enumerate(content):
            print(f"\nElement {i}:")
            print(f"  Start index: {element.get('startIndex', 'N/A')}")
            print(f"  End index: {element.get('endIndex', 'N/A')}")
            
            if 'paragraph' in element:
                para = element['paragraph']
                elements = para.get('elements', [])
                text_content = ""
                for elem in elements:
                    if 'textRun' in elem:
                        text_content += elem['textRun'].get('content', '')
                print(f"  Type: Paragraph")
                print(f"  Text preview: {repr(text_content[:100])}")
                
            elif 'table' in element:
                print(f"  Type: Table")
                
            elif 'sectionBreak' in element:
                print(f"  Type: Section Break")
                
            else:
                print(f"  Type: {list(element.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error investigating document: {e}")
        import traceback
        traceback.print_exc()
        return False

def try_different_insert_location():
    """Try inserting at different locations with more specific targeting"""
    try:
        # Authenticate
        creds = authenticate()
        if not creds:
            print("❌ Authentication failed")
            return False
        
        # Build the service
        service = build('docs', 'v1', credentials=creds)
        
        # Get the document
        document = service.documents().get(documentId=DOCUMENT_ID).execute()
        
        # Try inserting at index 1 (very beginning after first character)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"""
🚨 URGENT MESSAGE FROM COPILOT - {timestamp} 🚨

Donald, this message should appear at the beginning of your document!

If you can see this, the API is working correctly.

"""

        # Insert at the very beginning (index 1, after the first character)
        requests = [{
            'insertText': {
                'location': {'index': 1},
                'text': message
            }
        }]
        
        print(f"✍️  Inserting test message at index 1...")
        result = service.documents().batchUpdate(
            documentId=DOCUMENT_ID,
            body={'requests': requests}
        ).execute()
        
        print("✅ Test message inserted!")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting test message: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Step 1: Investigating document structure...")
    investigate_document_structure()
    
    print("\n" + "="*60)
    print("✍️  Step 2: Trying to insert a test message at the beginning...")
    try_different_insert_location()
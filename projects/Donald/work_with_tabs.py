#!/usr/bin/env python3
"""
Script to work with specific tabs in Donald's Google Doc.
"""
import sys
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Add the tools path
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant')

# Document ID from the Google Docs URL
DOCUMENT_ID = '1nPsKZbUZUtzyZcR73DZ2mQL8zC6TvA28orVh7g7-LJA'
TAB_ID = 't.f08gqwqiiq2s'  # The specific tab ID from the URL

SCOPES = ['https://www.googleapis.com/auth/documents']

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

def explore_tabs():
    """Explore document tabs and try to add content to the specific tab"""
    try:
        creds = authenticate()
        if not creds:
            return False
        
        service = build('docs', 'v1', credentials=creds)
        
        # Get document with tabs information
        document = service.documents().get(documentId=DOCUMENT_ID).execute()
        
        print("🔍 Looking for tabs in the document...")
        
        # Check if the document has tabs
        if 'tabs' in document:
            print(f"📑 Found {len(document['tabs'])} tabs:")
            for i, tab in enumerate(document['tabs']):
                tab_id = tab.get('tabId', 'No ID')
                tab_properties = tab.get('tabProperties', {})
                title = tab_properties.get('title', 'Untitled')
                print(f"  Tab {i}: ID='{tab_id}', Title='{title}'")
                
                if tab_id == TAB_ID:
                    print(f"  🎯 Found target tab: {title}")
                    return add_content_to_tab(service, tab_id)
        else:
            print("📄 This document doesn't use tabs - it's a single document")
            print("✅ Your message should be visible in the main document!")
            print("🔗 Try this link: https://docs.google.com/document/d/1nPsKZbUZUtzyZcR73DZ2mQL8zC6TvA28orVh7g7-LJA/edit")
        
        return True
        
    except Exception as e:
        print(f"❌ Error exploring tabs: {e}")
        return False

def add_content_to_tab(service, tab_id):
    """Add content to a specific tab"""
    try:
        message = f"""
📝 Message from GitHub Copilot in "Notes from Dad and co-pilot" tab!

Hello Donald! 👋

If you can see this message, I've successfully accessed your specific tab.

🎯 Quick reminder: Your first draft is due September 17th (4 days away!)

Check the main document for detailed guidance and next steps.

Best regards,
GitHub Copilot
"""
        
        # Try to add content to the specific tab
        # Note: Google Docs API might handle tabs differently
        requests = [{
            'insertText': {
                'location': {'index': 1, 'tabId': tab_id},
                'text': message
            }
        }]
        
        print(f"✍️  Adding content to tab {tab_id}...")
        result = service.documents().batchUpdate(
            documentId=DOCUMENT_ID,
            body={'requests': requests}
        ).execute()
        
        print("✅ Content added to specific tab!")
        return True
        
    except Exception as e:
        print(f"❌ Error adding content to tab: {e}")
        print("This might be because the tab structure is different than expected")
        return False

if __name__ == "__main__":
    explore_tabs()
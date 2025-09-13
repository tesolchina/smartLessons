#!/usr/bin/env python3
"""
Script to edit Donald's Google Doc - specifically the "Notes from Dad and co-pilot" tab/section.
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

def extract_text_from_element(element):
    """Extract text from a document element"""
    text = ""
    if 'paragraph' in element:
        paragraph = element['paragraph']
        for elem in paragraph.get('elements', []):
            if 'textRun' in elem:
                text += elem['textRun'].get('content', '')
    elif 'table' in element:
        table = element['table']
        for row in table.get('tableRows', []):
            for cell in row.get('tableCells', []):
                for content in cell.get('content', []):
                    text += extract_text_from_element(content)
    return text

def find_notes_section_index(document):
    """Find the index where to insert content in the Notes from Dad and co-pilot section"""
    body = document.get('body', {})
    content = body.get('content', [])
    
    # Look for "Notes from Dad and co-pilot" text or similar
    for i, element in enumerate(content):
        text = extract_text_from_element(element)
        if 'Notes from Dad' in text or 'co-pilot' in text or 'copilot' in text:
            print(f"🎯 Found notes section at element {i}: {text.strip()}")
            # Return the end of this element to insert after it
            return element.get('endIndex', 1)
    
    # If section not found, insert at the end
    print("⚠️  'Notes from Dad and co-pilot' section not found, will insert at end")
    return len(extract_text_from_document(document)) - 1

def extract_text_from_document(document):
    """Extract all text content from document"""
    content = ""
    body = document.get('body', {})
    for element in body.get('content', []):
        content += extract_text_from_element(element)
    return content

def add_message_to_notes_section():
    """Add a message to the Notes from Dad and co-pilot section"""
    try:
        # Authenticate
        creds = authenticate()
        if not creds:
            print("❌ Authentication failed")
            return False
        
        # Build the service
        service = build('docs', 'v1', credentials=creds)
        
        # Get the document first to understand its structure
        print(f"📖 Reading document structure: {DOCUMENT_ID}")
        document = service.documents().get(documentId=DOCUMENT_ID).execute()
        
        # Show current content for debugging
        current_content = extract_text_from_document(document)
        print("📋 Current document content:")
        print("=" * 60)
        print(current_content)
        print("=" * 60)
        
        # Create the message to add
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"""

📝 Message from GitHub Copilot - {timestamp}

Hello Donald! 👋

I've successfully accessed your Google Doc through the API tools! Here's what I can help you with:

🎯 **Your Immediate Priorities (Deadline: Sept 17, 2025 - 4 days!):**
1. Complete your data analysis (we have excellent visualizations ready)
2. Write the analysis sections connecting your data to theory
3. Finalize your conclusion and evaluation

📊 **What We've Already Prepared for You:**
- Data cleaning and visualization (check your workspace files)
- Correlation analysis between distance from CBD and various factors
- Professional charts with trendlines ready for your report
- NOTE_FOR_DONALD.md with detailed guidance

🔧 **Available Tools & Support:**
- Google Docs API access for collaborative editing
- Jupyter notebooks with your urban geography analysis
- Clean data files in both wide and long formats
- Pre-generated figures for your report

💡 **Next Steps Recommendation:**
1. Review the analysis in your Jupyter notebooks
2. Copy the professional charts to your report
3. Write connecting text following the "Describe → Explain → Anomalies → Link to theory" structure
4. Use the prepared notes to speed up your writing

Ready to help you ace this geography coursework! 🌟

Best regards,
GitHub Copilot & Dad's Assistant Team

"""

        # Find where to insert (at the end for now, since we need to locate or create the notes section)
        insert_index = len(current_content)
        
        # Prepare the request to insert text
        requests = [{
            'insertText': {
                'location': {'index': insert_index},
                'text': message
            }
        }]
        
        # Execute the update
        print(f"✍️  Adding message to document...")
        result = service.documents().batchUpdate(
            documentId=DOCUMENT_ID,
            body={'requests': requests}
        ).execute()
        
        print("✅ Successfully added message to Donald's Google Doc!")
        print(f"📝 Added {len(message)} characters")
        print(f"🔗 Direct link: https://docs.google.com/document/d/{DOCUMENT_ID}/edit")
        
        return True
        
    except Exception as e:
        print(f"❌ Error editing document: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = add_message_to_notes_section()
    if success:
        print("\n🎉 Mission accomplished! Check Donald's Google Doc for the new message.")
    else:
        print("\n😞 Something went wrong. Check the error messages above.")
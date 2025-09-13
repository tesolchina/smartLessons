#!/usr/bin/env python3
"""
Script to read Donald's Google Doc using the available API tools.
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

# Scopes for reading documents
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

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

def read_document():
    """Read the Google Document content"""
    try:
        # Authenticate
        creds = authenticate()
        if not creds:
            print("❌ Authentication failed")
            return None
        
        # Build the service
        service = build('docs', 'v1', credentials=creds)
        
        # Get the document
        print(f"📖 Attempting to read document: {DOCUMENT_ID}")
        document = service.documents().get(documentId=DOCUMENT_ID).execute()
        
        # Extract text content
        content = ""
        body = document.get('body', {})
        for element in body.get('content', []):
            content += extract_text_from_element(element)
        
        print(f"✅ Successfully read document!")
        print(f"📊 Content length: {len(content)} characters")
        print("=" * 60)
        print(content)
        
        # Save to file
        output_file = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/Donald/donald_doc_content.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Content saved to: {output_file}")
        
        return content
        
    except Exception as e:
        print(f"❌ Error reading document: {e}")
        return None

if __name__ == "__main__":
    read_document()
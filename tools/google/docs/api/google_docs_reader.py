#!/usr/bin/env python3
"""
Generic Google Docs Reader
A reusable tool to read any Google Doc by its ID.

Usage:
    python google_docs_reader.py --doc-id YOUR_DOCUMENT_ID
    python google_docs_reader.py --url "https://docs.google.com/document/d/YOUR_ID/edit"
"""
import sys
import os
import pickle
import argparse
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google API configuration
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(SCRIPT_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, 'credentials.json')

class GoogleDocsReader:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google API"""
        creds = None
        
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.exists(CREDENTIALS_PATH):
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    raise FileNotFoundError(f"Credentials file not found at {CREDENTIALS_PATH}")
            
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('docs', 'v1', credentials=creds)
    
    def extract_doc_id_from_url(self, url):
        """Extract document ID from Google Docs URL"""
        pattern = r'/document/d/([a-zA-Z0-9-_]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            raise ValueError(f"Could not extract document ID from URL: {url}")
    
    def extract_text_from_element(self, element):
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
                        text += self.extract_text_from_element(content)
        return text
    
    def read_document(self, doc_id, output_file=None):
        """Read a Google Document and return its content"""
        try:
            print(f"📖 Reading document: {doc_id}")
            document = self.service.documents().get(documentId=doc_id).execute()
            
            # Extract metadata
            title = document.get('title', 'Untitled')
            revision_id = document.get('revisionId', 'Unknown')
            
            print(f"📄 Title: {title}")
            print(f"🔄 Revision: {revision_id}")
            
            # Extract text content
            content = ""
            body = document.get('body', {})
            for element in body.get('content', []):
                content += self.extract_text_from_element(element)
            
            print(f"📊 Content length: {len(content)} characters")
            
            # Save to file if specified
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"Title: {title}\\n")
                    f.write(f"Revision: {revision_id}\\n")
                    f.write(f"Content Length: {len(content)} characters\\n")
                    f.write("=" * 50 + "\\n\\n")
                    f.write(content)
                print(f"💾 Content saved to: {output_file}")
            
            return {
                'title': title,
                'revision_id': revision_id,
                'content': content,
                'length': len(content)
            }
            
        except Exception as e:
            print(f"❌ Error reading document: {e}")
            return None
    
    def get_document_info(self, doc_id):
        """Get basic information about a document without reading full content"""
        try:
            document = self.service.documents().get(documentId=doc_id).execute()
            
            title = document.get('title', 'Untitled')
            revision_id = document.get('revisionId', 'Unknown')
            
            # Count elements
            body = document.get('body', {})
            elements = body.get('content', [])
            
            return {
                'title': title,
                'revision_id': revision_id,
                'element_count': len(elements),
                'document_id': doc_id
            }
            
        except Exception as e:
            print(f"❌ Error getting document info: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='Read Google Docs content')
    parser.add_argument('--doc-id', help='Google Docs document ID')
    parser.add_argument('--url', help='Google Docs URL')
    parser.add_argument('--output', help='Output file path (optional)')
    parser.add_argument('--info-only', action='store_true', help='Get document info only')
    
    args = parser.parse_args()
    
    if not args.doc_id and not args.url:
        print("❌ Please provide either --doc-id or --url")
        sys.exit(1)
    
    reader = GoogleDocsReader()
    
    # Extract document ID
    if args.url:
        doc_id = reader.extract_doc_id_from_url(args.url)
    else:
        doc_id = args.doc_id
    
    print(f"🔍 Using document ID: {doc_id}")
    
    if args.info_only:
        info = reader.get_document_info(doc_id)
        if info:
            print("📋 Document Information:")
            for key, value in info.items():
                print(f"  {key}: {value}")
    else:
        result = reader.read_document(doc_id, args.output)
        if result:
            print("\\n" + "="*50)
            print("📄 DOCUMENT CONTENT:")
            print("="*50)
            print(result['content'])

if __name__ == "__main__":
    main()
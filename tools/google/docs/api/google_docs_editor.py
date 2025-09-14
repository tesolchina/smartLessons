#!/usr/bin/env python3
"""
Generic Google Docs Editor
A reusable tool to edit any Google Doc by adding text, comments, and formatting.

Usage:
    python google_docs_editor.py --doc-id YOUR_DOCUMENT_ID --add-text "Your text here"
    python google_docs_editor.py --url "https://docs.google.com/document/d/YOUR_ID/edit" --insert-at-position 100 --text "Insert this"
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
from datetime import datetime

# Google API configuration
SCOPES = ['https://www.googleapis.com/auth/documents']
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(SCRIPT_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, 'credentials.json')

class GoogleDocsEditor:
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
    
    def get_document_content(self, doc_id):
        """Get the current document content"""
        try:
            document = self.service.documents().get(documentId=doc_id).execute()
            
            content = ""
            body = document.get('body', {})
            for element in body.get('content', []):
                if 'paragraph' in element:
                    paragraph = element['paragraph']
                    for elem in paragraph.get('elements', []):
                        if 'textRun' in elem:
                            content += elem['textRun'].get('content', '')
            
            return content, document
        except Exception as e:
            print(f"❌ Error getting document content: {e}")
            return None, None
    
    def insert_text(self, doc_id, text, position=1):
        """Insert text at a specific position in the document"""
        try:
            requests = [{
                'insertText': {
                    'location': {'index': position},
                    'text': text
                }
            }]
            
            result = self.service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Inserted {len(text)} characters at position {position}")
            return True
            
        except Exception as e:
            print(f"❌ Error inserting text: {e}")
            return False
    
    def append_text(self, doc_id, text):
        """Append text to the end of the document"""
        try:
            content, _ = self.get_document_content(doc_id)
            if content is None:
                return False
            
            # Insert at the end
            position = len(content)
            return self.insert_text(doc_id, text, position)
            
        except Exception as e:
            print(f"❌ Error appending text: {e}")
            return False
    
    def prepend_text(self, doc_id, text):
        """Add text to the beginning of the document"""
        return self.insert_text(doc_id, text, 1)
    
    def replace_text(self, doc_id, old_text, new_text):
        """Replace specific text in the document"""
        try:
            content, document = self.get_document_content(doc_id)
            if content is None:
                return False
            
            # Find the text to replace
            start_pos = content.find(old_text)
            if start_pos == -1:
                print(f"⚠️  Text '{old_text}' not found in document")
                return False
            
            end_pos = start_pos + len(old_text)
            
            requests = [
                {
                    'deleteContentRange': {
                        'range': {
                            'startIndex': start_pos,
                            'endIndex': end_pos
                        }
                    }
                },
                {
                    'insertText': {
                        'location': {'index': start_pos},
                        'text': new_text
                    }
                }
            ]
            
            result = self.service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Replaced '{old_text}' with '{new_text}'")
            return True
            
        except Exception as e:
            print(f"❌ Error replacing text: {e}")
            return False
    
    def add_formatted_text(self, doc_id, text, position=1, bold=False, italic=False, font_size=None, color=None):
        """Add text with formatting"""
        try:
            # First insert the text
            requests = [{
                'insertText': {
                    'location': {'index': position},
                    'text': text
                }
            }]
            
            # Then apply formatting
            if bold or italic or font_size or color:
                text_style = {}
                fields = []
                
                if bold:
                    text_style['bold'] = True
                    fields.append('bold')
                
                if italic:
                    text_style['italic'] = True
                    fields.append('italic')
                
                if font_size:
                    text_style['fontSize'] = {
                        'magnitude': font_size,
                        'unit': 'PT'
                    }
                    fields.append('fontSize')
                
                if color:
                    # Color should be in format {'red': 1.0, 'green': 0.0, 'blue': 0.0}
                    text_style['foregroundColor'] = {
                        'color': {
                            'rgbColor': color
                        }
                    }
                    fields.append('foregroundColor')
                
                formatting_request = {
                    'updateTextStyle': {
                        'range': {
                            'startIndex': position,
                            'endIndex': position + len(text)
                        },
                        'textStyle': text_style,
                        'fields': ','.join(fields)
                    }
                }
                requests.append(formatting_request)
            
            result = self.service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Added formatted text: {len(text)} characters")
            return True
            
        except Exception as e:
            print(f"❌ Error adding formatted text: {e}")
            return False
    
    def find_text_position(self, doc_id, search_text):
        """Find the position of specific text in the document"""
        try:
            content, _ = self.get_document_content(doc_id)
            if content is None:
                return None
            
            position = content.find(search_text)
            if position != -1:
                print(f"🔍 Found '{search_text}' at position {position}")
                return position
            else:
                print(f"⚠️  Text '{search_text}' not found")
                return None
                
        except Exception as e:
            print(f"❌ Error finding text: {e}")
            return None
    
    def add_timestamp_header(self, doc_id, message="Document updated"):
        """Add a timestamp header to the document"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_text = f"\\n🕒 {message} - {timestamp}\\n{'='*50}\\n\\n"
        return self.prepend_text(doc_id, header_text)

def main():
    parser = argparse.ArgumentParser(description='Edit Google Docs content')
    parser.add_argument('--doc-id', help='Google Docs document ID')
    parser.add_argument('--url', help='Google Docs URL')
    
    # Text operations
    parser.add_argument('--add-text', help='Text to add to document')
    parser.add_argument('--append-text', help='Text to append to end of document')
    parser.add_argument('--prepend-text', help='Text to add to beginning of document')
    parser.add_argument('--insert-at-position', type=int, help='Position to insert text')
    parser.add_argument('--replace-old', help='Old text to replace')
    parser.add_argument('--replace-new', help='New text to replace with')
    parser.add_argument('--find-text', help='Text to find in document')
    
    # Formatting options
    parser.add_argument('--bold', action='store_true', help='Make text bold')
    parser.add_argument('--italic', action='store_true', help='Make text italic')
    parser.add_argument('--font-size', type=int, help='Font size in points')
    parser.add_argument('--color-red', type=float, default=0.0, help='Red color component (0-1)')
    parser.add_argument('--color-green', type=float, default=0.0, help='Green color component (0-1)')
    parser.add_argument('--color-blue', type=float, default=0.0, help='Blue color component (0-1)')
    
    # Utility operations
    parser.add_argument('--add-timestamp', action='store_true', help='Add timestamp header')
    parser.add_argument('--timestamp-message', default='Document updated', help='Message for timestamp')
    
    args = parser.parse_args()
    
    if not args.doc_id and not args.url:
        print("❌ Please provide either --doc-id or --url")
        sys.exit(1)
    
    editor = GoogleDocsEditor()
    
    # Extract document ID
    if args.url:
        doc_id = editor.extract_doc_id_from_url(args.url)
    else:
        doc_id = args.doc_id
    
    print(f"📝 Editing document: {doc_id}")
    
    # Handle different operations
    if args.find_text:
        editor.find_text_position(doc_id, args.find_text)
    
    elif args.replace_old and args.replace_new:
        editor.replace_text(doc_id, args.replace_old, args.replace_new)
    
    elif args.add_timestamp:
        editor.add_timestamp_header(doc_id, args.timestamp_message)
    
    elif args.add_text:
        if args.insert_at_position is not None:
            # Check for formatting options
            color = None
            if args.color_red or args.color_green or args.color_blue:
                color = {
                    'red': args.color_red,
                    'green': args.color_green,
                    'blue': args.color_blue
                }
            
            editor.add_formatted_text(
                doc_id, args.add_text, args.insert_at_position,
                bold=args.bold, italic=args.italic, 
                font_size=args.font_size, color=color
            )
        else:
            editor.insert_text(doc_id, args.add_text)
    
    elif args.append_text:
        editor.append_text(doc_id, args.append_text)
    
    elif args.prepend_text:
        editor.prepend_text(doc_id, args.prepend_text)
    
    else:
        print("❌ Please specify an operation (--add-text, --append-text, etc.)")
        sys.exit(1)

if __name__ == "__main__":
    main()
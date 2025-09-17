#!/usr/bin/env python3
"""
GCAP 3056 Google Docs Manager
Tool to read and write to project team Google Docs

Usage:
    python gcap3056_google_docs_manager.py --read-all
    python gcap3056_google_docs_manager.py --read-project "energy_poverty"
    python gcap3056_google_docs_manager.py --write-project "energy_poverty" --text "Your update here"
    python gcap3056_google_docs_manager.py --sync-all
"""
import sys
import os
import pickle
import argparse
import re
import json
from pathlib import Path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google API configuration
SCOPES = ['https://www.googleapis.com/auth/documents']
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_TOOLS_DIR = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/google/docs/api"
TOKEN_PATH = os.path.join(GOOGLE_TOOLS_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(GOOGLE_TOOLS_DIR, 'credentials.json')

# Project documents configuration
PROJECT_DOCS = {
    "energy_poverty": {
        "url": "https://docs.google.com/document/d/1IPVnQEKA3cKMCaYWtc4R8-PcFq7n79MYrMq8QLzAHhk/edit?tab=t.0",
        "doc_id": "1IPVnQEKA3cKMCaYWtc4R8-PcFq7n79MYrMq8QLzAHhk",
        "local_dir": "Projects and teams/energy_poverty"
    },
    "hko_chatbot": {
        "url": "https://docs.google.com/document/d/1E6NLBbnTE1WNS8aU0xwvZOls6CVLe_0i5LHyjOQ76iw/edit?tab=t.0",
        "doc_id": "1E6NLBbnTE1WNS8aU0xwvZOls6CVLe_0i5LHyjOQ76iw",
        "local_dir": "Projects and teams/hko_chatbot"
    },
    "chronic_disease_co_care": {
        "url": "https://docs.google.com/document/d/1i0efENpeAYYNchaCSvKwN2HEL2YXGVXYUr4-Lf4X7RA/edit?tab=t.0",
        "doc_id": "1i0efENpeAYYNchaCSvKwN2HEL2YXGVXYUr4-Lf4X7RA",
        "local_dir": "Projects and teams/chronic_disease_co_care"
    },
    "anti_scamming_education": {
        "url": "https://docs.google.com/document/d/1MQ3Gk1kyNvaw7e-Tc72y41UKMrztIZ21Cj-1STsWZNA/edit?tab=t.8lpba9bjqpel#heading=h.s640o2lk1eg6",
        "doc_id": "1MQ3Gk1kyNvaw7e-Tc72y41UKMrztIZ21Cj-1STsWZNA",
        "local_dir": "Projects and teams/anti_scamming_education"
    },
    "emergency_alert_system": {
        "url": "https://docs.google.com/document/d/19ND3APGCVjd-UC1ie0kurt9YXlJw-smf1EfuF6szMJ0/edit?tab=t.0",
        "doc_id": "19ND3APGCVjd-UC1ie0kurt9YXlJw-smf1EfuF6szMJ0",
        "local_dir": "Projects and teams/emergency_alert_system"
    }
}

class GCAP3056GoogleDocsManager:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google API using existing credentials"""
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
                    print(f"❌ Credentials file not found at {CREDENTIALS_PATH}")
                    print("Please set up Google API credentials first.")
                    return False
            
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('docs', 'v1', credentials=creds)
        print("✅ Authenticated with Google Docs API")
        return True
    
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
    
    def read_document(self, project_name):
        """Read a specific project document"""
        if project_name not in PROJECT_DOCS:
            print(f"❌ Project '{project_name}' not found")
            return None
        
        doc_info = PROJECT_DOCS[project_name]
        doc_id = doc_info['doc_id']
        
        try:
            print(f"📖 Reading {project_name} document...")
            document = self.service.documents().get(documentId=doc_id).execute()
            
            # Extract metadata
            title = document.get('title', 'Untitled')
            revision_id = document.get('revisionId', 'Unknown')
            
            # Extract text content
            content = ""
            body = document.get('body', {})
            for element in body.get('content', []):
                content += self.extract_text_from_element(element)
            
            result = {
                'project_name': project_name,
                'title': title,
                'revision_id': revision_id,
                'content': content,
                'length': len(content),
                'doc_id': doc_id,
                'url': doc_info['url']
            }
            
            print(f"✅ Read {project_name}: {len(content)} characters")
            return result
            
        except Exception as e:
            print(f"❌ Error reading {project_name}: {e}")
            return None
    
    def read_all_documents(self):
        """Read all project documents"""
        all_docs = {}
        for project_name in PROJECT_DOCS.keys():
            doc_data = self.read_document(project_name)
            if doc_data:
                all_docs[project_name] = doc_data
        
        return all_docs
    
    def save_document_locally(self, doc_data, save_content=True, save_metadata=True):
        """Save document content and metadata locally"""
        project_name = doc_data['project_name']
        local_dir = Path(PROJECT_DOCS[project_name]['local_dir'])
        
        # Ensure directory exists
        local_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if save_content:
            # Save content as markdown
            content_file = local_dir / f"google_doc_content_{timestamp}.md"
            with open(content_file, 'w', encoding='utf-8') as f:
                f.write(f"# {doc_data['title']}\n\n")
                f.write(f"**Document ID:** {doc_data['doc_id']}\n")
                f.write(f"**URL:** {doc_data['url']}\n")
                f.write(f"**Last Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Revision:** {doc_data['revision_id']}\n")
                f.write(f"**Length:** {doc_data['length']} characters\n\n")
                f.write("---\n\n")
                f.write(doc_data['content'])
            
            print(f"💾 Content saved: {content_file}")
        
        if save_metadata:
            # Save metadata as JSON
            metadata_file = local_dir / f"google_doc_metadata_{timestamp}.json"
            metadata = {
                'project_name': doc_data['project_name'],
                'title': doc_data['title'],
                'doc_id': doc_data['doc_id'],
                'url': doc_data['url'],
                'revision_id': doc_data['revision_id'],
                'length': doc_data['length'],
                'last_sync': datetime.now().isoformat(),
                'content_file': str(content_file.name) if save_content else None
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"📋 Metadata saved: {metadata_file}")
    
    def append_text_to_document(self, project_name, text):
        """Append text to the end of a project document"""
        if project_name not in PROJECT_DOCS:
            print(f"❌ Project '{project_name}' not found")
            return False
        
        doc_id = PROJECT_DOCS[project_name]['doc_id']
        
        try:
            # Get current content to find end position
            document = self.service.documents().get(documentId=doc_id).execute()
            content = ""
            body = document.get('body', {})
            for element in body.get('content', []):
                content += self.extract_text_from_element(element)
            
            # Append text at the end
            position = len(content)
            requests = [{
                'insertText': {
                    'location': {'index': position},
                    'text': f"\n\n{text}"
                }
            }]
            
            result = self.service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Appended {len(text)} characters to {project_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error appending to {project_name}: {e}")
            return False
    
    def add_timestamp_update(self, project_name, message="Document updated via API"):
        """Add a timestamp update to a project document"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_text = f"\n\n---\n🕒 {message} - {timestamp}\n---"
        return self.append_text_to_document(project_name, update_text)
    
    def sync_all_projects(self):
        """Read all documents and save them locally"""
        print("🔄 Syncing all project documents...")
        all_docs = self.read_all_documents()
        
        sync_summary = []
        for project_name, doc_data in all_docs.items():
            self.save_document_locally(doc_data)
            sync_summary.append({
                'project': project_name,
                'title': doc_data['title'],
                'length': doc_data['length'],
                'synced_at': datetime.now().isoformat()
            })
        
        # Save sync summary
        summary_file = Path("google_docs_sync_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(sync_summary, f, indent=2)
        
        print(f"📊 Sync complete! Summary saved to {summary_file}")
        return sync_summary
    
    def list_projects(self):
        """List all available projects"""
        print("📁 Available projects:")
        for i, (project_name, info) in enumerate(PROJECT_DOCS.items(), 1):
            print(f"  {i}. {project_name}")
            print(f"     URL: {info['url']}")
            print(f"     Doc ID: {info['doc_id']}")
            print()

def main():
    parser = argparse.ArgumentParser(description='GCAP 3056 Google Docs Manager')
    
    # Read operations
    parser.add_argument('--read-all', action='store_true', help='Read all project documents')
    parser.add_argument('--read-project', help='Read specific project document')
    parser.add_argument('--list-projects', action='store_true', help='List all available projects')
    
    # Write operations
    parser.add_argument('--write-project', help='Project to write to')
    parser.add_argument('--text', help='Text to append to document')
    parser.add_argument('--add-timestamp', action='store_true', help='Add timestamp update')
    parser.add_argument('--timestamp-message', default='Document updated via API', help='Message for timestamp')
    
    # Sync operations
    parser.add_argument('--sync-all', action='store_true', help='Sync all documents locally')
    parser.add_argument('--save-content', action='store_true', default=True, help='Save document content')
    parser.add_argument('--save-metadata', action='store_true', default=True, help='Save document metadata')
    
    args = parser.parse_args()
    
    if not any([args.read_all, args.read_project, args.list_projects, args.write_project, 
                args.sync_all, args.add_timestamp]):
        print("❌ Please specify an operation")
        parser.print_help()
        sys.exit(1)
    
    manager = GCAP3056GoogleDocsManager()
    
    if args.list_projects:
        manager.list_projects()
    
    elif args.read_all:
        docs = manager.read_all_documents()
        for project_name, doc_data in docs.items():
            print(f"\n{'='*50}")
            print(f"📄 {project_name.upper()}")
            print(f"Title: {doc_data['title']}")
            print(f"Length: {doc_data['length']} characters")
            print(f"{'='*50}")
            print(doc_data['content'][:500] + "..." if len(doc_data['content']) > 500 else doc_data['content'])
    
    elif args.read_project:
        doc_data = manager.read_document(args.read_project)
        if doc_data:
            print(f"\n{'='*50}")
            print(f"📄 {doc_data['title']}")
            print(f"{'='*50}")
            print(doc_data['content'])
    
    elif args.write_project and args.text:
        manager.append_text_to_document(args.write_project, args.text)
    
    elif args.add_timestamp:
        if args.write_project:
            manager.add_timestamp_update(args.write_project, args.timestamp_message)
        else:
            print("❌ Please specify --write-project with --add-timestamp")
    
    elif args.sync_all:
        manager.sync_all_projects()
    
    else:
        print("❌ Invalid operation combination")
        parser.print_help()

if __name__ == "__main__":
    main()

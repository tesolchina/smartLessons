#!/usr/bin/env python3
"""
Generic Google Docs Comment Manager
A reusable tool to add, list, and manage comments on any Google Doc.

Usage:
    python google_docs_comments.py --doc-id YOUR_DOCUMENT_ID --add-comment "Your comment"
    python google_docs_comments.py --url "https://docs.google.com/document/d/YOUR_ID/edit" --list-comments
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
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(SCRIPT_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, 'credentials.json')

class GoogleDocsCommentManager:
    def __init__(self):
        self.docs_service = None
        self.drive_service = None
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
        
        self.docs_service = build('docs', 'v1', credentials=creds)
        self.drive_service = build('drive', 'v3', credentials=creds)
    
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
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            
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
    
    def list_comments(self, doc_id):
        """List all comments in the document"""
        try:
            print(f"💬 Listing comments for document: {doc_id}")
            
            # Get comments using Drive API
            comments_result = self.drive_service.comments().list(
                fileId=doc_id,
                fields='comments(id,content,createdTime,author,resolved,anchor)'
            ).execute()
            
            comments = comments_result.get('comments', [])
            
            if not comments:
                print("📝 No comments found in this document")
                return []
            
            print(f"📋 Found {len(comments)} comments:")
            print("="*60)
            
            for i, comment in enumerate(comments, 1):
                print(f"\\nComment {i}:")
                print(f"  ID: {comment.get('id', 'Unknown')}")
                print(f"  Author: {comment.get('author', {}).get('displayName', 'Unknown')}")
                print(f"  Created: {comment.get('createdTime', 'Unknown')}")
                print(f"  Resolved: {comment.get('resolved', False)}")
                
                if 'anchor' in comment:
                    print(f"  Anchored: Yes")
                    anchor = comment['anchor']
                    if 'r' in anchor:
                        print(f"  Anchor range: {anchor['r']}")
                else:
                    print(f"  Anchored: No (general comment)")
                
                content = comment.get('content', '')
                print(f"  Content: {content[:100]}{'...' if len(content) > 100 else ''}")
                print("-" * 40)
            
            return comments
            
        except Exception as e:
            print(f"❌ Error listing comments: {e}")
            return []
    
    def add_general_comment(self, doc_id, comment_text):
        """Add a general comment to the document (not anchored to specific text)"""
        try:
            comment_body = {
                'content': comment_text
            }
            
            result = self.drive_service.comments().create(
                fileId=doc_id,
                body=comment_body,
                fields='id,content,createdTime'
            ).execute()
            
            print(f"✅ General comment added successfully!")
            print(f"Comment ID: {result.get('id', 'Unknown')}")
            return result.get('id')
            
        except Exception as e:
            print(f"❌ Error adding general comment: {e}")
            return None
    
    def add_anchored_comment(self, doc_id, comment_text, search_text=None, position_start=None, position_end=None):
        """Add a comment anchored to specific text or position"""
        try:
            if search_text:
                # Find the text to anchor to
                content, _ = self.get_document_content(doc_id)
                if content is None:
                    return None
                
                start_pos = content.find(search_text)
                if start_pos == -1:
                    print(f"⚠️  Text '{search_text}' not found. Adding as general comment.")
                    return self.add_general_comment(doc_id, comment_text)
                
                end_pos = start_pos + len(search_text)
            
            elif position_start is not None and position_end is not None:
                start_pos = position_start
                end_pos = position_end
            
            else:
                print("⚠️  No anchor specified. Adding as general comment.")
                return self.add_general_comment(doc_id, comment_text)
            
            comment_body = {
                'content': comment_text,
                'anchor': {
                    'r': f"kix.{start_pos}:{end_pos}"
                }
            }
            
            result = self.drive_service.comments().create(
                fileId=doc_id,
                body=comment_body,
                fields='id,content,createdTime'
            ).execute()
            
            print(f"✅ Anchored comment added successfully!")
            print(f"Comment ID: {result.get('id', 'Unknown')}")
            print(f"Anchored to positions: {start_pos}-{end_pos}")
            
            return result.get('id')
            
        except Exception as e:
            print(f"❌ Error adding anchored comment: {e}")
            print("🔄 Trying to add as general comment instead...")
            return self.add_general_comment(doc_id, comment_text)
    
    def resolve_comment(self, doc_id, comment_id):
        """Mark a comment as resolved"""
        try:
            result = self.drive_service.comments().update(
                fileId=doc_id,
                commentId=comment_id,
                body={'resolved': True}
            ).execute()
            
            print(f"✅ Comment {comment_id} marked as resolved")
            return True
            
        except Exception as e:
            print(f"❌ Error resolving comment: {e}")
            return False
    
    def delete_comment(self, doc_id, comment_id):
        """Delete a comment"""
        try:
            self.drive_service.comments().delete(
                fileId=doc_id,
                commentId=comment_id
            ).execute()
            
            print(f"✅ Comment {comment_id} deleted")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting comment: {e}")
            return False
    
    def add_feedback_comments(self, doc_id, feedback_sections):
        """Add multiple feedback comments based on common sections"""
        results = []
        
        common_sections = {
            'Introduction': 'Add more background context and connect to theoretical frameworks',
            'Methodology': 'Explain the rationale behind each method and link to research objectives',
            'Analysis': 'Use the describe→explain→anomalies→theory structure for thorough analysis',
            'Conclusion': 'Summarize key findings and connect back to original research questions',
            'References': 'Ensure all sources are properly cited in the required format'
        }
        
        for section, default_feedback in common_sections.items():
            feedback = feedback_sections.get(section, default_feedback)
            comment_id = self.add_anchored_comment(
                doc_id, 
                f"📝 {section.upper()} FEEDBACK:\\n\\n{feedback}",
                search_text=section
            )
            if comment_id:
                results.append({'section': section, 'comment_id': comment_id})
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Manage Google Docs comments')
    parser.add_argument('--doc-id', help='Google Docs document ID')
    parser.add_argument('--url', help='Google Docs URL')
    
    # Comment operations
    parser.add_argument('--list-comments', action='store_true', help='List all comments')
    parser.add_argument('--add-comment', help='Add a general comment')
    parser.add_argument('--add-anchored-comment', help='Add a comment anchored to specific text')
    parser.add_argument('--anchor-text', help='Text to anchor comment to')
    parser.add_argument('--anchor-start', type=int, help='Start position for anchor')
    parser.add_argument('--anchor-end', type=int, help='End position for anchor')
    parser.add_argument('--resolve-comment', help='Comment ID to resolve')
    parser.add_argument('--delete-comment', help='Comment ID to delete')
    parser.add_argument('--add-feedback', action='store_true', help='Add standard feedback comments')
    
    args = parser.parse_args()
    
    if not args.doc_id and not args.url:
        print("❌ Please provide either --doc-id or --url")
        sys.exit(1)
    
    manager = GoogleDocsCommentManager()
    
    # Extract document ID
    if args.url:
        doc_id = manager.extract_doc_id_from_url(args.url)
    else:
        doc_id = args.doc_id
    
    print(f"💬 Managing comments for document: {doc_id}")
    
    # Handle different operations
    if args.list_comments:
        manager.list_comments(doc_id)
    
    elif args.add_comment:
        manager.add_general_comment(doc_id, args.add_comment)
    
    elif args.add_anchored_comment:
        manager.add_anchored_comment(
            doc_id, args.add_anchored_comment,
            search_text=args.anchor_text,
            position_start=args.anchor_start,
            position_end=args.anchor_end
        )
    
    elif args.resolve_comment:
        manager.resolve_comment(doc_id, args.resolve_comment)
    
    elif args.delete_comment:
        manager.delete_comment(doc_id, args.delete_comment)
    
    elif args.add_feedback:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        feedback_sections = {
            'Introduction': f'Add more background context and theoretical framework connections. Updated {timestamp}',
            'Methodology': f'Explain rationale for each method and link to research objectives. Updated {timestamp}',
            'Analysis': f'Structure analysis using describe→explain→anomalies→theory format. Updated {timestamp}',
            'Conclusion': f'Strengthen conclusions with specific data evidence. Updated {timestamp}'
        }
        results = manager.add_feedback_comments(doc_id, feedback_sections)
        print(f"✅ Added {len(results)} feedback comments")
    
    else:
        print("❌ Please specify an operation (--list-comments, --add-comment, etc.)")
        sys.exit(1)

if __name__ == "__main__":
    main()
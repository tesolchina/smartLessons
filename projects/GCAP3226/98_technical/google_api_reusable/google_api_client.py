"""
Universal Google API Client

A reusable class for accessing Google APIs across different projects.
Supports Drive, Sheets, Docs, Gmail, Calendar, and more.

Usage:
    from google_api_client import GoogleAPIClient
    
    client = GoogleAPIClient()
    drive_service = client.get_drive_service()
    sheets_service = client.get_sheets_service()
"""

import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleAPIClient:
    """Universal Google API client for multiple services"""
    
    # Available scopes for different Google services
    SCOPES = {
        'drive': 'https://www.googleapis.com/auth/drive',
        'drive_readonly': 'https://www.googleapis.com/auth/drive.readonly',
        'sheets': 'https://www.googleapis.com/auth/spreadsheets',
        'docs': 'https://www.googleapis.com/auth/documents',
        'slides': 'https://www.googleapis.com/auth/presentations',
        'gmail_readonly': 'https://www.googleapis.com/auth/gmail.readonly',
        'gmail_send': 'https://www.googleapis.com/auth/gmail.send',
        'calendar': 'https://www.googleapis.com/auth/calendar',
        'calendar_readonly': 'https://www.googleapis.com/auth/calendar.readonly'
    }
    
    def __init__(self, 
                 credentials_file: str = 'credentials_template.json',
                 token_file: str = 'token.json',
                 scopes: Optional[List[str]] = None):
        """
        Initialize Google API client
        
        Args:
            credentials_file: Path to OAuth credentials JSON file
            token_file: Path to store authentication tokens
            scopes: List of OAuth scopes (default: drive + sheets)
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        
        # Default scopes for most common use cases
        if scopes is None:
            scopes = [
                self.SCOPES['drive'],
                self.SCOPES['sheets'],
                self.SCOPES['docs'],
                self.SCOPES['slides']
            ]
        
        self.scopes = scopes
        self.credentials = None
        self._services = {}
        
        # Authenticate on initialization
        self._authenticate()
    
    def _authenticate(self) -> bool:
        """Authenticate with Google APIs"""
        try:
            # Load existing token
            if os.path.exists(self.token_file):
                self.credentials = Credentials.from_authorized_user_file(
                    self.token_file, self.scopes
                )
            
            # Refresh or get new credentials
            if not self.credentials or not self.credentials.valid:
                if (self.credentials and self.credentials.expired and 
                    self.credentials.refresh_token):
                    try:
                        self.credentials.refresh(Request())
                        print("🔄 Refreshed authentication token")
                    except Exception as e:
                        print(f"⚠️  Could not refresh token: {e}")
                        self.credentials = None
                
                if not self.credentials:
                    # Load client configuration
                    if not os.path.exists(self.credentials_file):
                        print(f"❌ Credentials file not found: {self.credentials_file}")
                        return False
                    
                    print("🔐 Starting OAuth authentication...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.scopes
                    )
                    self.credentials = flow.run_local_server(port=0)
                    print("✅ Authentication successful")
                
                # Save credentials for next run
                with open(self.token_file, 'w') as token:
                    token.write(self.credentials.to_json())
                    print(f"💾 Saved authentication to {self.token_file}")
            
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def _get_service(self, service_name: str, version: str):
        """Get or create a Google API service"""
        service_key = f"{service_name}_{version}"
        
        if service_key not in self._services:
            if not self.credentials:
                raise Exception("Not authenticated. Please run authenticate() first.")
            
            try:
                self._services[service_key] = build(
                    service_name, version, credentials=self.credentials
                )
                print(f"🔧 Connected to {service_name.title()} API")
            except Exception as e:
                print(f"❌ Failed to connect to {service_name}: {e}")
                raise
        
        return self._services[service_key]
    
    def get_drive_service(self):
        """Get Google Drive service"""
        return self._get_service('drive', 'v3')
    
    def get_sheets_service(self):
        """Get Google Sheets service"""
        return self._get_service('sheets', 'v4')
    
    def get_docs_service(self):
        """Get Google Docs service"""
        return self._get_service('docs', 'v1')
    
    def get_slides_service(self):
        """Get Google Slides service"""
        return self._get_service('slides', 'v1')
    
    def get_gmail_service(self):
        """Get Gmail service"""
        return self._get_service('gmail', 'v1')
    
    def get_calendar_service(self):
        """Get Google Calendar service"""
        return self._get_service('calendar', 'v3')
    
    # Convenience methods for common operations
    
    def create_folder(self, name: str, parent_id: Optional[str] = None) -> Dict:
        """Create a folder in Google Drive"""
        drive = self.get_drive_service()
        
        folder_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            folder_metadata['parents'] = [parent_id]
        
        try:
            folder = drive.files().create(
                body=folder_metadata,
                fields='id,name,webViewLink'
            ).execute()
            
            print(f"📁 Created folder: {folder['name']}")
            return folder
            
        except HttpError as e:
            print(f"❌ Error creating folder: {e}")
            raise
    
    def create_document(self, title: str, parent_id: Optional[str] = None) -> Dict:
        """Create a Google Document"""
        drive = self.get_drive_service()
        
        doc_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document'
        }
        
        if parent_id:
            doc_metadata['parents'] = [parent_id]
        
        try:
            doc = drive.files().create(
                body=doc_metadata,
                fields='id,name,webViewLink'
            ).execute()
            
            print(f"📄 Created document: {doc['name']}")
            return doc
            
        except HttpError as e:
            print(f"❌ Error creating document: {e}")
            raise
    
    def create_spreadsheet(self, title: str, parent_id: Optional[str] = None) -> Dict:
        """Create a Google Spreadsheet"""
        drive = self.get_drive_service()
        
        sheet_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        
        if parent_id:
            sheet_metadata['parents'] = [parent_id]
        
        try:
            sheet = drive.files().create(
                body=sheet_metadata,
                fields='id,name,webViewLink'
            ).execute()
            
            print(f"📊 Created spreadsheet: {sheet['name']}")
            return sheet
            
        except HttpError as e:
            print(f"❌ Error creating spreadsheet: {e}")
            raise
    
    def list_files(self, query: str = None, max_results: int = 10) -> List[Dict]:
        """List files in Google Drive"""
        drive = self.get_drive_service()
        
        try:
            results = drive.files().list(
                q=query,
                pageSize=max_results,
                fields="files(id, name, mimeType, modifiedTime, webViewLink)"
            ).execute()
            
            return results.get('files', [])
            
        except HttpError as e:
            print(f"❌ Error listing files: {e}")
            return []
    
    def set_file_permissions(self, file_id: str, email: str, role: str = 'writer') -> bool:
        """Set permissions for a file or folder"""
        drive = self.get_drive_service()
        
        try:
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }
            
            drive.permissions().create(
                fileId=file_id,
                body=permission,
                sendNotificationEmail=True
            ).execute()
            
            print(f"✅ Granted {role} access to {email}")
            return True
            
        except HttpError as e:
            print(f"❌ Error setting permissions: {e}")
            return False
    
    def read_sheet_data(self, spreadsheet_id: str, range_name: str) -> List[List]:
        """Read data from a Google Sheet"""
        sheets = self.get_sheets_service()
        
        try:
            result = sheets.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            return result.get('values', [])
            
        except HttpError as e:
            print(f"❌ Error reading sheet: {e}")
            return []
    
    def write_sheet_data(self, spreadsheet_id: str, range_name: str, data: List[List]) -> bool:
        """Write data to a Google Sheet"""
        sheets = self.get_sheets_service()
        
        try:
            body = {'values': data}
            
            sheets.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"✅ Updated sheet range: {range_name}")
            return True
            
        except HttpError as e:
            print(f"❌ Error writing to sheet: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test the API connection"""
        try:
            drive = self.get_drive_service()
            
            # Test basic API call
            results = drive.files().list(pageSize=1).execute()
            
            print("✅ Google API connection successful")
            return True
            
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Google API Client")
    print("=" * 40)
    
    try:
        # Initialize client
        client = GoogleAPIClient()
        
        # Test connection
        if client.test_connection():
            print("🎉 Google API Client is ready to use!")
            
            # Example: List recent files
            files = client.list_files(max_results=5)
            print(f"\n📋 Recent files ({len(files)} found):")
            for file in files:
                print(f"  📄 {file['name']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure credentials_template.json exists")
        print("2. Check your internet connection")
        print("3. Verify your OAuth credentials are correct")
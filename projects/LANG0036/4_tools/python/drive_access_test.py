"""
Google Drive API Access Test using OAuth Client Key

This script tests Google Drive API access using the OAuth client credentials
for accessing and managing files and folders.

Usage:
    python drive_access_test.py
"""

import os
import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# OAuth 2.0 scopes for Google Drive
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.readonly'
]

# Your client configuration
CLIENT_CONFIG = {
    "installed": {
        "client_id": "584822767688-sljrj83d92o8l3efd7urg3il9unlca1b.apps.googleusercontent.com",
        "project_id": "gcap3226-project",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "YOUR_CLIENT_SECRET_HERE",
        "redirect_uris": ["http://localhost"]
    }
}

def get_credentials():
    """Get valid user credentials from storage or run OAuth flow"""
    creds = None
    token_file = 'credentials/token.json'
    
    # Create credentials directory if it doesn't exist
    os.makedirs('credentials', exist_ok=True)
    
    # Load existing token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("✅ Refreshed existing credentials")
            except Exception as e:
                print(f"❌ Error refreshing credentials: {e}")
                creds = None
        
        if not creds:
            print("🔐 Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
            creds = flow.run_local_server(port=0)
            print("✅ OAuth flow completed")
        
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
            print(f"💾 Credentials saved to {token_file}")
    
    return creds

def test_drive_connection(service):
    """Test basic Drive API connection"""
    try:
        # Test basic API call
        results = service.files().list(pageSize=10).execute()
        items = results.get('files', [])
        
        print(f"✅ Connected to Google Drive")
        print(f"📁 Found {len(items)} files in your Drive")
        
        if items:
            print("\n📋 Recent files:")
            for item in items[:5]:
                print(f"   • {item['name']} ({item.get('mimeType', 'unknown type')})")
        
        return True
        
    except HttpError as error:
        print(f"❌ Drive API error: {error}")
        return False

def list_folders(service, max_results=20):
    """List folders in Google Drive"""
    try:
        query = "mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(
            q=query,
            pageSize=max_results,
            fields="files(id, name, parents, createdTime)"
        ).execute()
        
        folders = results.get('files', [])
        
        print(f"\n📁 Your Google Drive Folders ({len(folders)} found):")
        print("-" * 60)
        
        for folder in folders:
            print(f"📂 {folder['name']}")
            print(f"   ID: {folder['id']}")
            print(f"   Created: {folder.get('createdTime', 'Unknown')}")
            print()
        
        return folders
        
    except HttpError as error:
        print(f"❌ Error listing folders: {error}")
        return []

def search_gcap_files(service):
    """Search for GCAP3226 related files"""
    try:
        query = "name contains 'GCAP' or name contains 'gcap' or name contains '3226'"
        results = service.files().list(
            q=query,
            pageSize=20,
            fields="files(id, name, mimeType, parents, modifiedTime, webViewLink)"
        ).execute()
        
        files = results.get('files', [])
        
        print(f"\n🔍 GCAP3226 Related Files ({len(files)} found):")
        print("-" * 60)
        
        for file in files:
            print(f"📄 {file['name']}")
            print(f"   Type: {file.get('mimeType', 'Unknown')}")
            print(f"   ID: {file['id']}")
            print(f"   Link: {file.get('webViewLink', 'No link')}")
            print(f"   Modified: {file.get('modifiedTime', 'Unknown')}")
            print()
        
        return files
        
    except HttpError as error:
        print(f"❌ Error searching files: {error}")
        return []

def create_test_folder(service, folder_name="GCAP3226_Test_Folder"):
    """Create a test folder to verify write permissions"""
    try:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        folder = service.files().create(
            body=folder_metadata,
            fields='id,name,webViewLink'
        ).execute()
        
        print(f"✅ Created test folder: {folder['name']}")
        print(f"   ID: {folder['id']}")
        print(f"   Link: {folder['webViewLink']}")
        
        return folder
        
    except HttpError as error:
        print(f"❌ Error creating folder: {error}")
        return None

def get_drive_info(service):
    """Get information about the user's Drive"""
    try:
        about = service.about().get(fields="user,storageQuota").execute()
        user = about.get('user', {})
        storage = about.get('storageQuota', {})
        
        print(f"\n👤 Drive Account Info:")
        print(f"   User: {user.get('displayName', 'Unknown')}")
        print(f"   Email: {user.get('emailAddress', 'Unknown')}")
        
        if storage:
            used = int(storage.get('usage', 0))
            limit = int(storage.get('limit', 0))
            
            used_gb = used / (1024**3)
            limit_gb = limit / (1024**3)
            
            print(f"   Storage: {used_gb:.1f} GB / {limit_gb:.1f} GB used")
        
        return about
        
    except HttpError as error:
        print(f"❌ Error getting drive info: {error}")
        return None

def main():
    """Main function to test Google Drive API access"""
    print("🚀 Google Drive API Access Test")
    print("=" * 50)
    
    try:
        # Get credentials
        print("🔑 Getting credentials...")
        creds = get_credentials()
        
        # Build the service
        service = build('drive', 'v3', credentials=creds)
        print("🔧 Built Drive service")
        
        # Test connection
        print("\n🧪 Testing connection...")
        if not test_drive_connection(service):
            print("❌ Connection test failed")
            return
        
        # Get drive info
        get_drive_info(service)
        
        # List folders
        folders = list_folders(service)
        
        # Search for GCAP files
        gcap_files = search_gcap_files(service)
        
        # Create test folder (optional)
        print("\n🔧 Testing folder creation...")
        test_folder = create_test_folder(service)
        
        print("\n" + "=" * 50)
        print("📊 SUMMARY")
        print("=" * 50)
        print(f"✅ API Connection: Working")
        print(f"📁 Folders found: {len(folders)}")
        print(f"📄 GCAP files found: {len(gcap_files)}")
        print(f"🔧 Folder creation: {'Success' if test_folder else 'Failed'}")
        
        print("\n🎉 Google Drive API is working correctly!")
        print("\nNext steps:")
        print("1. You can now create team folders automatically")
        print("2. Use the team_setup.py script for bulk operations")
        print("3. Check the created test folder in your Drive")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you have the correct client_secret")
        print("2. Check your internet connection")
        print("3. Verify the client_id is correct")

if __name__ == "__main__":
    main()
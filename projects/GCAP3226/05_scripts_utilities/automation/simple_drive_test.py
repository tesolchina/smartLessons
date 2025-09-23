"""
Simplified Google Drive Access using OAuth Credentials File

This version loads credentials from a JSON file for easier management.
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# OAuth 2.0 scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]

def load_client_credentials():
    """Load client credentials from JSON file"""
    creds_file = 'credentials/client_credentials.json'
    
    if not os.path.exists(creds_file):
        print(f"❌ Credentials file not found: {creds_file}")
        print("Please create the file with your OAuth client credentials")
        return None
    
    try:
        with open(creds_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return None

def authenticate():
    """Authenticate and return Google Drive service"""
    print("🔑 Authenticating with Google Drive...")
    
    creds = None
    token_file = 'credentials/token.json'
    
    # Load existing token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        print("📂 Found existing token file")
    
    # If credentials are not valid, refresh or get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("🔄 Refreshed expired token")
            except Exception as e:
                print(f"⚠️  Could not refresh token: {e}")
                creds = None
        
        if not creds:
            # Load client config
            client_config = load_client_credentials()
            if not client_config:
                return None
            
            # Check if client_secret is set
            if client_config['installed']['client_secret'] == 'REPLACE_WITH_YOUR_CLIENT_SECRET':
                print("❌ Please replace 'REPLACE_WITH_YOUR_CLIENT_SECRET' with your actual client secret")
                print("   Get it from Google Cloud Console > Credentials > OAuth 2.0 Client IDs")
                return None
            
            print("🌐 Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
            print("✅ OAuth flow completed successfully")
        
        # Save credentials for next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
            print(f"💾 Saved credentials to {token_file}")
    
    # Build and return service
    service = build('drive', 'v3', credentials=creds)
    print("🔧 Google Drive service ready")
    return service

def list_recent_files(service, count=10):
    """List recent files in Google Drive"""
    try:
        results = service.files().list(
            pageSize=count,
            fields="files(id, name, mimeType, modifiedTime, webViewLink)",
            orderBy="modifiedTime desc"
        ).execute()
        
        files = results.get('files', [])
        
        print(f"\n📋 Your {count} Most Recent Files:")
        print("-" * 60)
        
        for i, file in enumerate(files, 1):
            print(f"{i:2d}. {file['name']}")
            print(f"     Type: {file.get('mimeType', 'Unknown')}")
            print(f"     ID: {file['id']}")
            print(f"     Link: {file.get('webViewLink', 'No link')}")
            print()
        
        return files
        
    except HttpError as error:
        print(f"❌ Error listing files: {error}")
        return []

def search_course_content(service):
    """Search for course-related content"""
    search_terms = ['GCAP', 'gcap', '3226', 'team', 'group', 'project']
    
    for term in search_terms:
        try:
            query = f"name contains '{term}'"
            results = service.files().list(
                q=query,
                pageSize=5,
                fields="files(id, name, mimeType, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                print(f"\n🔍 Files containing '{term}' ({len(files)} found):")
                for file in files:
                    print(f"   📄 {file['name']} ({file.get('mimeType', 'unknown')})")
                    print(f"      Link: {file.get('webViewLink', 'No link')}")
        
        except HttpError as error:
            print(f"❌ Error searching for '{term}': {error}")

def create_course_folder(service):
    """Create a folder for GCAP3226 course"""
    try:
        folder_name = "GCAP3226_Course_Materials"
        
        # Check if folder already exists
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(q=query).execute()
        existing = results.get('files', [])
        
        if existing:
            folder = existing[0]
            print(f"📁 Course folder already exists: {folder['name']}")
            print(f"   ID: {folder['id']}")
            return folder
        
        # Create new folder
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        folder = service.files().create(
            body=folder_metadata,
            fields='id,name,webViewLink'
        ).execute()
        
        print(f"✅ Created course folder: {folder['name']}")
        print(f"   ID: {folder['id']}")
        print(f"   Link: {folder['webViewLink']}")
        
        return folder
        
    except HttpError as error:
        print(f"❌ Error creating course folder: {error}")
        return None

def main():
    """Main function"""
    print("🚀 GCAP3226 Google Drive Access")
    print("=" * 50)
    
    # Authenticate
    service = authenticate()
    if not service:
        print("❌ Authentication failed")
        return
    
    try:
        # Test basic access
        print("\n🧪 Testing Drive access...")
        
        # List recent files
        recent_files = list_recent_files(service, 5)
        
        # Search for course content
        search_course_content(service)
        
        # Create course folder
        print("\n📁 Setting up course folder...")
        course_folder = create_course_folder(service)
        
        print("\n" + "=" * 50)
        print("📊 SUMMARY")
        print("=" * 50)
        print(f"✅ Authentication: Success")
        print(f"📄 Recent files: {len(recent_files)} found")
        print(f"📁 Course folder: {'Created/Found' if course_folder else 'Failed'}")
        
        print("\n🎉 Google Drive API is working!")
        print("\nYou can now:")
        print("• Access your Google Drive files programmatically")
        print("• Create folders for team projects")
        print("• Manage file permissions for students")
        print("• Automate course material organization")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main()
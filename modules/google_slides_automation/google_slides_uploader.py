#!/usr/bin/env python3
"""
Google Slides Automation for HKBU LANG 2077
Upload PowerPoint presentations to Google Slides and set sharing permissions.
"""

import os
import json
import pickle
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import shutil


class GoogleSlidesUploader:
    """Upload and manage presentations in Google Slides."""
    
    def __init__(self):
        """Initialize with Google API credentials."""
        # Google Slides API scopes
        self.SCOPES = [
            'https://www.googleapis.com/auth/presentations',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        
        self.creds = None
        self.slides_service = None
        self.drive_service = None
        
        # File paths
        self.credentials_file = 'credentials.json'
        self.token_file = 'token.pickle'
        
    def setup_credentials(self):
        """Set up Google API credentials."""
        print("🔐 Setting up Google API credentials...")
        
        # Check if token file exists
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"⚠️ Token refresh failed: {e}")
                    self.creds = None
            
            if not self.creds:
                if not os.path.exists(self.credentials_file):
                    print("❌ credentials.json file not found!")
                    print("\n📋 Setup Instructions:")
                    print("1. Go to: https://console.cloud.google.com/")
                    print("2. Create a new project or select existing")
                    print("3. Enable Google Slides API and Google Drive API")
                    print("4. Create credentials (OAuth 2.0 Client ID)")
                    print("5. Download as 'credentials.json' and place in this folder")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)
        
        # Build the services
        self.slides_service = build('slides', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        
        print("✅ Google API credentials configured")
        return True
    
    def upload_powerpoint_to_slides(self, pptx_path, title=None):
        """Upload PowerPoint file to Google Slides."""
        
        if not self.drive_service:
            print("❌ Google API not configured")
            return None
        
        if not os.path.exists(pptx_path):
            print(f"❌ PowerPoint file not found: {pptx_path}")
            return None
        
        print(f"📤 Uploading {os.path.basename(pptx_path)} to Google Slides...")
        
        # Set title
        if not title:
            title = os.path.splitext(os.path.basename(pptx_path))[0]
        
        # File metadata
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.presentation'
        }
        
        # Upload file
        media = MediaFileUpload(
            pptx_path,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            resumable=True
        )
        
        try:
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink,alternateLink'
            ).execute()
            
            presentation_id = file.get('id')
            presentation_url = file.get('webViewLink')
            
            print(f"✅ Upload successful!")
            print(f"   📊 Presentation ID: {presentation_id}")
            print(f"   🔗 View URL: {presentation_url}")
            
            return {
                'id': presentation_id,
                'name': title,
                'url': presentation_url,
                'file': file
            }
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    def set_sharing_permissions(self, file_id, permission_type='anyone', role='writer'):
        """Set sharing permissions for the presentation."""
        
        if not self.drive_service:
            print("❌ Google API not configured")
            return False
        
        print(f"🔒 Setting sharing permissions to '{permission_type} can {role}'...")
        
        permission = {
            'type': permission_type,
            'role': role
        }
        
        try:
            self.drive_service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
            
            print("✅ Sharing permissions set successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to set permissions: {e}")
            return False
    
    def get_shareable_link(self, file_id):
        """Get the shareable link for the presentation."""
        
        try:
            file = self.drive_service.files().get(
                fileId=file_id,
                fields='webViewLink,alternateLink'
            ).execute()
            
            return file.get('webViewLink')
            
        except Exception as e:
            print(f"❌ Failed to get shareable link: {e}")
            return None
    
    def list_presentations(self):
        """List all presentations in Google Drive."""
        
        if not self.drive_service:
            print("❌ Google API not configured")
            return []
        
        try:
            results = self.drive_service.files().list(
                q="mimeType='application/vnd.google-apps.presentation'",
                fields="nextPageToken, files(id, name, createdTime, webViewLink)"
            ).execute()
            
            presentations = results.get('files', [])
            return presentations
            
        except Exception as e:
            print(f"❌ Failed to list presentations: {e}")
            return []


def upload_lang2077_slides():
    """Upload LANG 2077 slides to Google Slides."""
    
    print("🎓 HKBU LANG 2077 - Google Slides Upload")
    print("=" * 50)
    
    # Initialize uploader
    uploader = GoogleSlidesUploader()
    
    # Setup credentials
    if not uploader.setup_credentials():
        return None
    
    # Find PowerPoint files
    slides_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/generated_slides"
    
    if not os.path.exists(slides_dir):
        print(f"❌ Slides directory not found: {slides_dir}")
        return None
    
    # Get PowerPoint files
    pptx_files = [f for f in os.listdir(slides_dir) if f.endswith('.pptx')]
    
    if not pptx_files:
        print("❌ No PowerPoint files found")
        return None
    
    print(f"📁 Found {len(pptx_files)} PowerPoint files:")
    for i, file in enumerate(pptx_files, 1):
        print(f"   {i}. {file}")
    
    # Let user choose file or upload the latest
    latest_file = max(pptx_files, key=lambda f: os.path.getmtime(os.path.join(slides_dir, f)))
    print(f"\n🎯 Using latest file: {latest_file}")
    
    pptx_path = os.path.join(slides_dir, latest_file)
    
    # Upload to Google Slides
    result = uploader.upload_powerpoint_to_slides(
        pptx_path, 
        title=f"LANG 2077: Language Skills for human-AI partnership - {datetime.now().strftime('%Y-%m-%d')}"
    )
    
    if not result:
        return None
    
    # Set sharing permissions
    if uploader.set_sharing_permissions(result['id'], 'anyone', 'writer'):
        # Get shareable link
        shareable_link = uploader.get_shareable_link(result['id'])
        
        print(f"\n🎉 Success! LANG 2077 slides uploaded to Google Slides")
        print(f"📊 Title: {result['name']}")
        print(f"🔗 Shareable Link: {shareable_link}")
        print(f"✏️  Permission: Anyone with link can edit")
        
        # Save result to file
        result_data = {
            'timestamp': datetime.now().isoformat(),
            'presentation_id': result['id'],
            'title': result['name'],
            'url': shareable_link,
            'permissions': 'anyone_can_edit',
            'original_file': latest_file
        }
        
        result_file = 'upload_result.json'
        with open(result_file, 'w') as f:
            json.dump(result_data, f, indent=2)
        
        print(f"💾 Upload details saved to: {result_file}")
        
        return result_data
    
    return result


def interactive_slides_manager():
    """Interactive Google Slides management interface."""
    
    print("🎓 HKBU Google Slides Manager")
    print("=" * 40)
    
    uploader = GoogleSlidesUploader()
    
    # Setup credentials
    if not uploader.setup_credentials():
        return
    
    while True:
        print("\n📋 Available Actions:")
        print("1. Upload LANG 2077 PowerPoint to Google Slides")
        print("2. List existing presentations")
        print("3. Set sharing permissions for presentation")
        print("4. Get shareable link")
        print("5. Exit")
        
        choice = input("\nSelect action (1-5): ").strip()
        
        if choice == "1":
            result = upload_lang2077_slides()
            if result:
                print(f"\n✅ Upload completed successfully!")
        
        elif choice == "2":
            presentations = uploader.list_presentations()
            if presentations:
                print(f"\n📊 Found {len(presentations)} presentations:")
                for i, pres in enumerate(presentations, 1):
                    print(f"   {i}. {pres['name']}")
                    print(f"      ID: {pres['id']}")
                    print(f"      URL: {pres.get('webViewLink', 'N/A')}")
                    print()
            else:
                print("\n❌ No presentations found")
        
        elif choice == "3":
            file_id = input("Enter presentation ID: ").strip()
            if file_id:
                uploader.set_sharing_permissions(file_id, 'anyone', 'writer')
        
        elif choice == "4":
            file_id = input("Enter presentation ID: ").strip()
            if file_id:
                link = uploader.get_shareable_link(file_id)
                if link:
                    print(f"🔗 Shareable link: {link}")
        
        elif choice == "5":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    upload_lang2077_slides()

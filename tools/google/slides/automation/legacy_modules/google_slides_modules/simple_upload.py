#!/usr/bin/env python3
"""
Simple Google Slides Upload
Upload PowerPoint to Google Slides with proper credential handling.
"""

import os
import json
import sys


def check_credentials():
    """Check and validate credentials.json format."""
    
    creds_path = 'credentials.json'
    
    if not os.path.exists(creds_path):
        print("❌ credentials.json not found")
        print("Please run: python3 setup_credentials.py")
        return False
    
    try:
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        
        print(f"📋 Credentials file found: {creds_path}")
        print(f"📊 File size: {os.path.getsize(creds_path)} bytes")
        
        # Check for different credential types
        if 'installed' in creds:
            client_info = creds['installed']
            print("✅ OAuth Desktop Application credentials detected")
            print(f"   Client ID: {client_info.get('client_id', 'Not found')[:50]}...")
            return True
            
        elif 'web' in creds:
            print("⚠️  Web application credentials detected")
            print("   You need Desktop Application credentials for CLI use")
            return False
            
        elif 'type' in creds and creds['type'] == 'service_account':
            print("⚠️  Service account credentials detected")
            print("   You need OAuth Desktop Application credentials")
            return False
            
        else:
            print("❌ Unknown credentials format")
            print("Available keys:", list(creds.keys()))
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in credentials file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading credentials: {e}")
        return False


def fix_credentials_setup():
    """Guide user to fix credentials setup."""
    
    print("\n🔧 How to fix credentials:")
    print("=" * 30)
    print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Select your project (or create one)")
    print("3. Go to APIs & Services > Credentials")
    print("4. Click '+ CREATE CREDENTIALS' > OAuth 2.0 Client IDs")
    print("5. Application type: Desktop application")
    print("6. Name: 'LANG2077 Slides Uploader'")
    print("7. Click CREATE")
    print("8. Download the JSON file")
    print("9. Save as 'credentials.json' in this folder")
    print("\n📁 Current folder:", os.getcwd())


def simple_upload():
    """Simple upload using google-api-python-client."""
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from datetime import datetime
        
        print("📦 Google API libraries loaded")
        
    except ImportError as e:
        print(f"❌ Missing library: {e}")
        print("Run: pip3 install google-api-python-client google-auth-oauthlib")
        return None
    
    # OAuth scopes
    SCOPES = [
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/presentations'
    ]
    
    try:
        # Authenticate
        print("🔐 Starting authentication...")
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        print("✅ Authentication successful")
        
        # Build services
        drive_service = build('drive', 'v3', credentials=creds)
        slides_service = build('slides', 'v1', credentials=creds)
        
        # Find PowerPoint file
        slides_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/generated_slides"
        
        if not os.path.exists(slides_dir):
            print(f"❌ Slides directory not found: {slides_dir}")
            return None
            
        pptx_files = [f for f in os.listdir(slides_dir) if f.endswith('.pptx')]
        
        if not pptx_files:
            print("❌ No PowerPoint files found")
            return None
        
        # Get latest file
        latest_file = max(pptx_files, key=lambda f: os.path.getmtime(os.path.join(slides_dir, f)))
        file_path = os.path.join(slides_dir, latest_file)
        
        print(f"📤 Uploading: {latest_file}")
        print(f"📁 From: {file_path}")
        
        # Upload and convert to Google Slides
        file_metadata = {
            'name': f'LANG 2077: Language Skills for human-AI partnership - {datetime.now().strftime("%Y-%m-%d")}',
            'mimeType': 'application/vnd.google-apps.presentation'  # Convert to Google Slides
        }
        
        media = MediaFileUpload(
            file_path,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            resumable=True
        )
        
        # Upload
        print("⏳ Uploading to Google Drive...")
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()
        
        file_id = file.get('id')
        file_name = file.get('name')
        
        print(f"✅ Upload successful!")
        print(f"📄 File: {file_name}")
        print(f"🆔 ID: {file_id}")
        
        # Set sharing permissions - anyone with link can edit
        print("🔓 Setting sharing permissions...")
        permission = {
            'type': 'anyone',
            'role': 'writer'  # Can edit
        }
        
        drive_service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        
        # Get shareable link
        link = file.get('webViewLink')
        
        print("🎉 Success! Your LANG 2077 slides are ready!")
        print("=" * 50)
        print(f"🔗 Link: {link}")
        print("✏️  Permission: Anyone with link can edit")
        print("📱 The link has been copied below for easy sharing:")
        print(f"{link}")
        
        # Try to copy to clipboard on macOS
        try:
            import subprocess
            subprocess.run(['pbcopy'], input=link, text=True, check=True)
            print("📋 Link copied to clipboard!")
        except:
            pass
            
        return link
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function."""
    
    print("🎓 LANG 2077 - Simple Google Slides Upload")
    print("=" * 45)
    
    # Check credentials
    if not check_credentials():
        fix_credentials_setup()
        return
    
    print("\n🚀 Credentials validated! Starting upload...")
    
    # Upload
    result = simple_upload()
    
    if result:
        print("\n✨ All done! Your slides are live on Google Slides.")
    else:
        print("\n❌ Upload failed. Please check the error messages above.")


if __name__ == "__main__":
    main()

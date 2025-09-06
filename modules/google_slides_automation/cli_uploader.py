#!/usr/bin/env python3
"""
Google Drive CLI Uploader
Upload files to Google Drive using command-line tools.
"""

import os
import subprocess
import sys
from datetime import datetime


class GoogleDriveCLI:
    """Google Drive CLI uploader using rclone or gdrive."""
    
    def __init__(self):
        self.upload_method = None
        self.check_available_tools()
    
    def check_available_tools(self):
        """Check which CLI tools are available."""
        
        print("🔍 Checking available Google Drive CLI tools...")
        
        # Check for rclone
        try:
            result = subprocess.run(['rclone', 'version'], 
                                  capture_output=True, text=True, check=False)
            if result.returncode == 0:
                print("✅ rclone found")
                self.upload_method = 'rclone'
                return
        except FileNotFoundError:
            pass
        
        # Check for gdrive
        try:
            result = subprocess.run(['gdrive', 'version'], 
                                  capture_output=True, text=True, check=False)
            if result.returncode == 0:
                print("✅ gdrive found")
                self.upload_method = 'gdrive'
                return
        except FileNotFoundError:
            pass
        
        print("❌ No Google Drive CLI tools found")
        self.upload_method = None
    
    def install_rclone(self):
        """Install rclone using homebrew."""
        
        print("📦 Installing rclone...")
        
        try:
            # Check if homebrew is available
            subprocess.run(['brew', '--version'], 
                          capture_output=True, check=True)
            
            # Install rclone
            result = subprocess.run(['brew', 'install', 'rclone'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ rclone installed successfully")
                self.upload_method = 'rclone'
                return True
            else:
                print(f"❌ Installation failed: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("❌ Homebrew not found. Please install rclone manually:")
            print("   Visit: https://rclone.org/downloads/")
            return False
        except subprocess.CalledProcessError:
            print("❌ Homebrew installation failed")
            return False
    
    def setup_rclone(self):
        """Set up rclone Google Drive connection."""
        
        if self.upload_method != 'rclone':
            if not self.install_rclone():
                return False
        
        print("\n🔧 Setting up rclone Google Drive connection...")
        print("This will open a browser window for authentication.")
        
        try:
            # Run rclone config
            subprocess.run(['rclone', 'config', 'create', 'gdrive', 'drive'], 
                          check=False)
            
            print("✅ rclone configured")
            return True
            
        except Exception as e:
            print(f"❌ rclone setup failed: {e}")
            return False
    
    def upload_file_rclone(self, file_path, remote_name=None):
        """Upload file using rclone."""
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        if not remote_name:
            remote_name = os.path.basename(file_path)
        
        print(f"📤 Uploading {os.path.basename(file_path)} to Google Drive...")
        
        try:
            # Upload file
            cmd = ['rclone', 'copy', file_path, f'gdrive:HKBU_LANG2077/']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Upload successful!")
                
                # Try to get shareable link
                link_cmd = ['rclone', 'link', f'gdrive:HKBU_LANG2077/{os.path.basename(file_path)}']
                link_result = subprocess.run(link_cmd, capture_output=True, text=True)
                
                if link_result.returncode == 0:
                    link = link_result.stdout.strip()
                    print(f"🔗 Shareable link: {link}")
                    return link
                else:
                    print("⚠️ Upload successful, but couldn't get shareable link")
                    return "Upload successful"
            else:
                print(f"❌ Upload failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return None
    
    def upload_to_slides(self, file_path):
        """Upload PowerPoint and convert to Google Slides."""
        
        if self.upload_method == 'rclone':
            return self.upload_file_rclone(file_path)
        else:
            print("❌ No upload method available")
            return None


def direct_api_upload():
    """Direct Google Drive API upload without OAuth flow complexity."""
    
    print("🚀 Direct Google Drive API Upload")
    print("=" * 35)
    
    # Create a simpler API client
    try:
        import json
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        # Simplified OAuth flow
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        
        if not os.path.exists('credentials.json'):
            print("❌ credentials.json not found")
            print("Run: python3 setup_credentials.py")
            return None
        
        # Get credentials
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
        # Build drive service
        service = build('drive', 'v3', credentials=creds)
        
        # Find PowerPoint file
        slides_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/generated_slides"
        pptx_files = [f for f in os.listdir(slides_dir) if f.endswith('.pptx')]
        
        if not pptx_files:
            print("❌ No PowerPoint files found")
            return None
        
        latest_file = max(pptx_files, key=lambda f: os.path.getmtime(os.path.join(slides_dir, f)))
        file_path = os.path.join(slides_dir, latest_file)
        
        print(f"📤 Uploading: {latest_file}")
        
        # Upload file
        file_metadata = {
            'name': f'LANG 2077: Language Skills for human-AI partnership - {datetime.now().strftime("%Y-%m-%d")}',
            'mimeType': 'application/vnd.google-apps.presentation'
        }
        
        media = MediaFileUpload(
            file_path,
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            resumable=True
        )
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()
        
        file_id = file.get('id')
        
        # Set sharing permissions
        permission = {
            'type': 'anyone',
            'role': 'writer'
        }
        
        service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        
        link = file.get('webViewLink')
        print(f"✅ Upload successful!")
        print(f"🔗 Shareable link: {link}")
        print(f"✏️  Permission: Anyone with link can edit")
        
        return link
        
    except Exception as e:
        print(f"❌ API upload failed: {e}")
        return None


def main():
    """Main CLI upload interface."""
    
    print("🎓 LANG 2077 - Google Drive CLI Upload")
    print("=" * 40)
    
    print("\nChoose upload method:")
    print("1. 🔧 rclone (recommended for CLI)")
    print("2. 🌐 Google Drive API (direct)")
    print("3. 📋 Show manual instructions")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        uploader = GoogleDriveCLI()
        if uploader.upload_method != 'rclone':
            if input("\nInstall rclone? (y/n): ").lower() == 'y':
                uploader.install_rclone()
            else:
                print("❌ rclone required for this method")
                return
        
        # Setup rclone if needed
        if input("\nConfigure rclone Google Drive? (y/n): ").lower() == 'y':
            uploader.setup_rclone()
        
        # Find and upload file
        slides_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/generated_slides"
        pptx_files = [f for f in os.listdir(slides_dir) if f.endswith('.pptx')]
        
        if pptx_files:
            latest_file = max(pptx_files, key=lambda f: os.path.getmtime(os.path.join(slides_dir, f)))
            file_path = os.path.join(slides_dir, latest_file)
            
            link = uploader.upload_to_slides(file_path)
            if link:
                print(f"\n🎉 Success! Your LANG 2077 slides are uploaded!")
        else:
            print("❌ No PowerPoint files found")
    
    elif choice == "2":
        link = direct_api_upload()
        if link:
            print(f"\n🎉 Success! Google Slides created and shared!")
    
    elif choice == "3":
        print("\n📋 Manual CLI Upload Instructions:")
        print("=" * 35)
        print("1. Install rclone: brew install rclone")
        print("2. Configure: rclone config")
        print("3. Upload: rclone copy file.pptx gdrive:")
        print("4. Share: rclone link gdrive:file.pptx")
    
    elif choice == "4":
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()

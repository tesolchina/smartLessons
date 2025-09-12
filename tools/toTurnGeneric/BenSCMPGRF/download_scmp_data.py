#!/usr/bin/env python3
"""
Google Drive Data Loader for Ben SCMP GRF Project
Downloads files from shared Google Drive folder to local corpus directory
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional

# Add the GoogleDocsAPI path for imports
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

class SCMPDataLoader:
    """Downloads SCMP corpus data from Google Drive to local directory"""
    
    def __init__(self, target_dir: str = None):
        self.target_dir = Path(target_dir) if target_dir else Path("GRF_SCMP_letters/corpus/downloaded_data")
        self.drive_service = None
        self.setup_services()
        
        # Create target directory
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
    def setup_services(self):
        """Initialize Google Drive API service"""
        try:
            from googleapiclient.discovery import build
            from auth_setup import authenticate_google_apis
            
            creds = authenticate_google_apis()
            if not creds:
                raise Exception("Authentication failed")
            
            self.drive_service = build('drive', 'v3', credentials=creds)
            print("✅ Google Drive API service initialized")
            
        except ImportError:
            print("⚠️  Google API libraries not installed.")
            print("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
            return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
            
    def extract_folder_id(self, drive_url: str) -> str:
        """Extract folder ID from Google Drive URL"""
        # https://drive.google.com/drive/u/0/folders/1Qt6Ak8sHMd7ZpX5T-p_4-pBH0r98L3rs
        if "folders/" in drive_url:
            return drive_url.split("folders/")[1].split("?")[0]
        elif "id=" in drive_url:
            return drive_url.split("id=")[1].split("&")[0]
        else:
            print(f"❌ Could not extract folder ID from: {drive_url}")
            return None
    
    def list_folder_contents(self, folder_id: str) -> List[Dict]:
        """List all files in the Google Drive folder"""
        if not self.drive_service:
            print("❌ Google Drive service not available")
            return []
            
        try:
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.drive_service.files().list(
                q=query,
                fields="files(id, name, mimeType, size, modifiedTime)",
                pageSize=100
            ).execute()
            
            files = results.get('files', [])
            print(f"📁 Found {len(files)} items in folder")
            
            for file in files:
                size = int(file.get('size', 0)) if file.get('size') else 'N/A'
                size_str = f"{size:,} bytes" if isinstance(size, int) else size
                print(f"  📄 {file['name']} ({file['mimeType']}) - {size_str}")
                
            return files
            
        except Exception as e:
            print(f"❌ Error listing folder contents: {e}")
            return []
    
    def download_file(self, file_id: str, filename: str, mime_type: str) -> bool:
        """Download a single file from Google Drive"""
        if not self.drive_service:
            return False
            
        try:
            target_path = self.target_dir / filename
            
            # Handle Google Docs/Sheets/Slides by exporting
            if mime_type.startswith('application/vnd.google-apps'):
                if 'document' in mime_type:
                    # Export Google Doc as .docx
                    export_mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                    target_path = target_path.with_suffix('.docx')
                    request = self.drive_service.files().export_media(fileId=file_id, mimeType=export_mime)
                elif 'spreadsheet' in mime_type:
                    # Export Google Sheet as .xlsx
                    export_mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    target_path = target_path.with_suffix('.xlsx')
                    request = self.drive_service.files().export_media(fileId=file_id, mimeType=export_mime)
                elif 'presentation' in mime_type:
                    # Export Google Slides as .pptx
                    export_mime = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
                    target_path = target_path.with_suffix('.pptx')
                    request = self.drive_service.files().export_media(fileId=file_id, mimeType=export_mime)
                else:
                    print(f"⚠️  Unsupported Google Apps format: {mime_type}")
                    return False
            else:
                # Direct download for regular files
                request = self.drive_service.files().get_media(fileId=file_id)
            
            # Download the file
            with open(target_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    if status:
                        progress = int(status.progress() * 100)
                        print(f"  📥 Downloading {filename}... {progress}%", end='\\r')
            
            print(f"  ✅ Downloaded: {target_path.name}")
            return True
            
        except Exception as e:
            print(f"  ❌ Error downloading {filename}: {e}")
            return False
    
    def download_folder(self, drive_url: str) -> bool:
        """Download all files from the Google Drive folder"""
        print(f"🚀 Starting download from: {drive_url}")
        
        folder_id = self.extract_folder_id(drive_url)
        if not folder_id:
            return False
            
        files = self.list_folder_contents(folder_id)
        if not files:
            print("📭 No files found to download")
            return False
            
        # Import MediaIoBaseDownload for file downloads
        try:
            from googleapiclient.http import MediaIoBaseDownload
            globals()['MediaIoBaseDownload'] = MediaIoBaseDownload
        except ImportError:
            print("❌ MediaIoBaseDownload not available")
            return False
            
        successful_downloads = 0
        total_files = len(files)
        
        print(f"\\n📥 Downloading {total_files} files to: {self.target_dir}")
        
        for file in files:
            success = self.download_file(file['id'], file['name'], file['mimeType'])
            if success:
                successful_downloads += 1
        
        print(f"\\n✅ Download complete: {successful_downloads}/{total_files} files")
        return successful_downloads > 0
    
    def create_download_manifest(self, files: List[Dict]):
        """Create a manifest of downloaded files"""
        manifest = {
            "download_date": str(Path().resolve()),
            "total_files": len(files),
            "files": files
        }
        
        manifest_path = self.target_dir / "download_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Download manifest created: {manifest_path}")

def main():
    """Main execution function"""
    # Google Drive folder URL from Ben's RA Pui Ying
    drive_url = "https://drive.google.com/drive/u/0/folders/1Qt6Ak8sHMd7ZpX5T-p_4-pBH0r98L3rs"
    
    # Initialize loader
    loader = SCMPDataLoader()
    
    # Download all files
    success = loader.download_folder(drive_url)
    
    if success:
        print("\\n🎉 All files downloaded successfully!")
        print(f"📂 Files saved to: {loader.target_dir}")
    else:
        print("\\n❌ Download failed or incomplete")

if __name__ == "__main__":
    main()

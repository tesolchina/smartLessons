#!/usr/bin/env python3
"""
Upload simulationBus56.html to smartLesson GCAP3226 folder
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from google_api_client import GoogleAPIClient

def upload_simulation_file():
    """Upload the simulation HTML file to Google Drive"""
    
    # Initialize Google API client
    client = GoogleAPIClient()
    drive_service = client.get_drive_service()
    
    # File to upload
    local_file_path = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/01_course_content/week04_simulation/resources/simulationBus56.html"
    
    # smartLesson GCAP3226 folder ID (need to find this)
    # Let's search for the smartLesson folder first
    
    print("🔍 Searching for smartLesson GCAP3226 folder...")
    
    try:
        # Search for folders with "smartLesson" or "GCAP3226" in the name
        query = "name contains 'smartLesson' or name contains 'GCAP3226'"
        results = drive_service.files().list(
            q=query,
            fields="files(id, name, parents, mimeType)"
        ).execute()
        
        folders = results.get('files', [])
        
        print(f"Found {len(folders)} potential folders:")
        for folder in folders:
            if folder['mimeType'] == 'application/vnd.google-apps.folder':
                print(f"📁 {folder['name']} (ID: {folder['id']})")
        
        # Look for specific smartLesson GCAP3226 folder
        target_folder_id = None
        for folder in folders:
            if 'smartLesson' in folder['name'] and 'GCAP3226' in folder['name']:
                target_folder_id = folder['id']
                break
        
        if not target_folder_id:
            # Use the main smartLessons folder if specific GCAP3226 folder not found
            for folder in folders:
                if folder['name'] == 'smartLessons' and folder['mimeType'] == 'application/vnd.google-apps.folder':
                    target_folder_id = folder['id']
                    print(f"✅ Using smartLessons folder: {folder['name']} (ID: {folder['id']})")
                    break
        
        if not target_folder_id:
            # Try to find by exact name
            query = "name = 'smartLesson_GCAP3226' or name = 'smartLessons_GCAP3226' or name contains 'smartLesson GCAP3226'"
            results = drive_service.files().list(
                q=query,
                fields="files(id, name, parents, mimeType)"
            ).execute()
            
            folders = results.get('files', [])
            for folder in folders:
                if folder['mimeType'] == 'application/vnd.google-apps.folder':
                    target_folder_id = folder['id']
                    print(f"✅ Found target folder: {folder['name']} (ID: {folder['id']})")
                    break
        
        if not target_folder_id:
            print("❌ Could not find smartLesson GCAP3226 folder. Available folders:")
            for folder in folders:
                if folder['mimeType'] == 'application/vnd.google-apps.folder':
                    print(f"   📁 {folder['name']}")
            return None
        
        # Upload the file
        print(f"📤 Uploading simulationBus56.html to folder...")
        
        file_metadata = {
            'name': 'simulationBus56.html',
            'parents': [target_folder_id]
        }
        
        # Read the file content
        with open(local_file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Create the file in Google Drive
        from googleapiclient.http import MediaInMemoryUpload
        
        media = MediaInMemoryUpload(
            file_content.encode('utf-8'),
            mimetype='text/html'
        )
        
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        print(f"✅ File uploaded successfully!")
        print(f"📄 File Name: {uploaded_file['name']}")
        print(f"🆔 File ID: {uploaded_file['id']}")
        print(f"🔗 URL: {uploaded_file['webViewLink']}")
        
        return uploaded_file['webViewLink']
        
    except Exception as e:
        print(f"❌ Error uploading file: {str(e)}")
        return None

def main():
    """Main execution function"""
    try:
        url = upload_simulation_file()
        if url:
            print(f"\n🎉 Success! Your file is available at: {url}")
        else:
            print("\n❌ Upload failed")
        return 0 if url else 1
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
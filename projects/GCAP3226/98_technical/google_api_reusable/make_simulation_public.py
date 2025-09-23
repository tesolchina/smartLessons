#!/usr/bin/env python3
"""
Make the uploaded simulation file publicly accessible
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from google_api_client import GoogleAPIClient

def make_file_public():
    """Make the uploaded file publicly accessible"""
    
    # Initialize Google API client
    client = GoogleAPIClient()
    drive_service = client.get_drive_service()
    
    # File ID from previous upload
    file_id = "1XC-JuVBi7WZCt-z7KW5P6MjuTzLPPLi9"
    
    try:
        print("🔧 Making file publicly accessible...")
        
        # Set the file to be publicly readable
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        
        drive_service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        
        # Get the file details with the public link
        file_details = drive_service.files().get(
            fileId=file_id,
            fields='id, name, webViewLink, webContentLink'
        ).execute()
        
        print("✅ File is now publicly accessible!")
        print(f"📄 File Name: {file_details['name']}")
        print(f"🆔 File ID: {file_details['id']}")
        print(f"👁️ View Link: {file_details['webViewLink']}")
        
        # For HTML files, we can also provide a direct content link
        if 'webContentLink' in file_details:
            print(f"📥 Direct Download: {file_details['webContentLink']}")
        
        # Create a direct viewable link for HTML content
        direct_view_url = f"https://drive.google.com/uc?id={file_id}&export=download"
        print(f"🌐 Direct HTML View: {direct_view_url}")
        
        return {
            'view_link': file_details['webViewLink'],
            'direct_view': direct_view_url,
            'file_id': file_id
        }
        
    except Exception as e:
        print(f"❌ Error making file public: {str(e)}")
        return None

def main():
    """Main execution function"""
    try:
        result = make_file_public()
        if result:
            print(f"\n🎉 Your simulation is now publicly accessible!")
            print(f"📋 View in Drive: {result['view_link']}")
            print(f"🌐 Direct HTML View: {result['direct_view']}")
        return 0 if result else 1
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
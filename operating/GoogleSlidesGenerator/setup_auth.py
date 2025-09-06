#!/usr/bin/env python3
"""
Google Slides Generator - Setup Authentication
=============================================

Sets up Google API authentication for the Slides Generator system.
This script helps you configure the necessary credentials and permissions.

Usage:
    python setup_auth.py
"""

import os
import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def setup_authentication():
    """Guide user through authentication setup."""
    print("🔐 Google Slides Generator - Authentication Setup")
    print("=" * 50)
    
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    print("\n📋 Step 1: Service Account Setup")
    print("You need to create a Google Cloud Project and Service Account.")
    print("Follow these steps:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select existing project")
    print("3. Enable Google Slides API and Google Drive API")
    print("4. Create a Service Account")
    print("5. Download the Service Account key as JSON")
    print("6. Save the JSON file as 'service_account_key.json' in the config/ folder")
    
    key_file = config_dir / "service_account_key.json"
    
    while not key_file.exists():
        input("\nPress Enter after you've saved the service_account_key.json file...")
        if not key_file.exists():
            print("❌ File not found. Please save the service account key file in config/")
    
    print("✅ Service account key file found!")
    
    # Test authentication
    print("\n🧪 Step 2: Testing Authentication")
    try:
        scopes = [
            'https://www.googleapis.com/auth/presentations',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials = Credentials.from_service_account_file(
            str(key_file), scopes=scopes
        )
        
        # Test Slides API
        slides_service = build('slides', 'v1', credentials=credentials)
        print("✅ Google Slides API connection successful")
        
        # Test Drive API
        drive_service = build('drive', 'v3', credentials=credentials)
        print("✅ Google Drive API connection successful")
        
        # Get service account email
        with open(key_file, 'r') as f:
            key_data = json.load(f)
            service_email = key_data.get('client_email')
            
        print(f"\n📧 Service Account Email: {service_email}")
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False
        
    print("\n📁 Step 3: Google Drive Folder Setup")
    print("To upload presentations to specific folders:")
    print(f"1. Share your Google Drive folders with: {service_email}")
    print("2. Give the service account 'Editor' permissions")
    print("3. Use folder paths in the conversion commands")
    
    print("\n🎉 Setup Complete!")
    print("You can now use the Google Slides Generator:")
    print("python markdown_to_slides.py --input your_file.md --template educational")
    
    return True


def create_sample_config():
    """Create sample configuration files."""
    config_dir = Path("config")
    
    # Create auth config template
    auth_config = {
        "service_account_file": "service_account_key.json",
        "scopes": [
            "https://www.googleapis.com/auth/presentations",
            "https://www.googleapis.com/auth/drive"
        ],
        "api_settings": {
            "slides_api_version": "v1",
            "drive_api_version": "v3"
        }
    }
    
    auth_file = config_dir / "auth_config.json"
    with open(auth_file, 'w') as f:
        json.dump(auth_config, f, indent=2)
        
    print(f"✅ Created {auth_file}")


def main():
    """Main setup function."""
    print("🚀 Starting Google Slides Generator setup...")
    
    try:
        # Create sample config
        create_sample_config()
        
        # Setup authentication
        if setup_authentication():
            print("\n🎊 Setup completed successfully!")
            print("You're ready to convert markdown to Google Slides!")
        else:
            print("\n⚠️ Setup incomplete. Please resolve authentication issues.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
Google Cloud Setup Helper
Guide user through Google Cloud Console setup for Slides API access.
"""

import webbrowser
import os


def setup_google_cloud_project():
    """Guide user through Google Cloud Console setup."""
    
    print("🔧 Google Cloud Console Setup Guide")
    print("=" * 45)
    
    print("\n📋 Steps to complete:")
    print("1. Create/select Google Cloud project")
    print("2. Enable required APIs") 
    print("3. Create OAuth 2.0 credentials")
    print("4. Download credentials.json")
    
    input("\nPress Enter to open Google Cloud Console...")
    
    # Open Google Cloud Console
    print("🌐 Opening Google Cloud Console...")
    webbrowser.open("https://console.cloud.google.com/")
    
    print("\n" + "="*50)
    print("🎯 STEP 1: Create or Select Project")
    print("="*50)
    print("• Click on project selector (top left)")
    print("• Create new project: 'HKBU LANG2077 Slides'")
    print("• Or select existing project")
    
    input("\nPress Enter when project is ready...")
    
    print("\n" + "="*50)
    print("🔧 STEP 2: Enable APIs")
    print("="*50)
    print("• Go to 'APIs & Services' > 'Library'")
    print("• Search and Enable:")
    print("  - Google Slides API")
    print("  - Google Drive API")
    
    # Open APIs library
    print("\n🌐 Opening APIs Library...")
    webbrowser.open("https://console.cloud.google.com/apis/library")
    
    input("\nPress Enter when APIs are enabled...")
    
    print("\n" + "="*50)
    print("🔐 STEP 3: Create OAuth Credentials")
    print("="*50)
    print("• Go to 'APIs & Services' > 'Credentials'")
    print("• Click 'Create Credentials' > 'OAuth 2.0 Client ID'")
    print("• If first time, configure OAuth consent screen:")
    print("  - User Type: External")
    print("  - App name: 'HKBU LANG2077 Slides'")
    print("  - User support email: your email")
    print("  - Developer email: your email")
    print("• Create OAuth Client:")
    print("  - Application type: Desktop application")
    print("  - Name: 'HKBU Slides Uploader'")
    
    # Open credentials page
    print("\n🌐 Opening Credentials page...")
    webbrowser.open("https://console.cloud.google.com/apis/credentials")
    
    input("\nPress Enter when OAuth client is created...")
    
    print("\n" + "="*50)
    print("📥 STEP 4: Download Credentials")
    print("="*50)
    print("• Find your OAuth 2.0 Client ID")
    print("• Click download button (⬇️)")
    print("• Save as 'credentials.json'")
    print("• Move to this folder:")
    print(f"  {os.getcwd()}")
    
    input("\nPress Enter when credentials.json is saved...")
    
    # Check if file exists
    if os.path.exists('credentials.json'):
        print("✅ credentials.json found!")
        print("🎉 Setup complete! Ready to upload slides.")
        return True
    else:
        print("❌ credentials.json not found")
        print("Please make sure the file is in this directory:")
        print(f"   {os.getcwd()}")
        return False


def test_credentials():
    """Test if credentials are properly configured."""
    
    print("\n🧪 Testing Credentials...")
    
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found")
        return False
    
    try:
        import json
        with open('credentials.json', 'r') as f:
            creds_data = json.load(f)
        
        if 'installed' in creds_data:
            client_id = creds_data['installed'].get('client_id', '')
            print(f"✅ Client ID: {client_id[:20]}...")
            print("✅ Credentials file format: OK")
            return True
        else:
            print("❌ Invalid credentials format")
            return False
            
    except Exception as e:
        print(f"❌ Error reading credentials: {e}")
        return False


def main():
    """Main setup function."""
    
    print("🎓 HKBU Google Slides API Setup")
    print("=" * 35)
    
    if os.path.exists('credentials.json'):
        print("✅ credentials.json already exists")
        if test_credentials():
            print("\n🚀 Ready to upload! Run:")
            print("   python3 google_slides_uploader.py")
        return
    
    print("⚙️ Setting up Google Slides API access...")
    
    # Guide through setup
    if setup_google_cloud_project():
        if test_credentials():
            print("\n🎉 Setup successful!")
            print("\n🚀 Next steps:")
            print("   python3 google_slides_uploader.py")
            print("\n📚 Or read the full guide:")
            print("   cat SETUP_GUIDE.md")
        else:
            print("\n⚠️ Setup incomplete. Please check credentials.json")
    else:
        print("\n⚠️ Setup incomplete. Please follow the guide.")


if __name__ == "__main__":
    main()

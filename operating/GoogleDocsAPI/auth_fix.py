"""
Simplified Authentication Setup for GCAP 3226
This version handles OAuth consent screen issues better
"""

import os
import pickle
from pathlib import Path
import json

def setup_oauth_consent_screen():
    """Guide user through OAuth consent screen setup"""
    print("🔧 OAUTH CONSENT SCREEN SETUP REQUIRED")
    print("=" * 45)
    print()
    print("❌ Error: 'CourseDriveManage has not completed Google verification process'")
    print()
    print("✅ SOLUTION: Configure OAuth consent screen properly")
    print()
    print("📋 FOLLOW THESE STEPS:")
    print()
    print("1. 🌐 Open: https://console.cloud.google.com/apis/credentials/consent")
    print("2. 📝 Configure OAuth consent screen:")
    print("   - User Type: External")
    print("   - App name: CourseDriveManage")
    print("   - User support email: simonwanghkteacher@gmail.com")
    print("   - Developer email: simonwanghkteacher@gmail.com")
    print()
    print("3. 👤 ADD TEST USER (CRITICAL!):")
    print("   - Go to 'Test users' section")
    print("   - Add: simonwanghkteacher@gmail.com")
    print("   - Save changes")
    print()
    print("4. 🔧 Add required scopes:")
    print("   - https://www.googleapis.com/auth/drive")
    print("   - https://www.googleapis.com/auth/documents")
    print("   - https://www.googleapis.com/auth/spreadsheets")
    print()
    print("5. 💾 Save and set status to 'Testing'")
    print()
    print("After completing these steps, run this script again!")
    print()
    
    response = input("Have you completed the OAuth setup? (y/n): ")
    return response.lower() == 'y'

def check_credentials_file():
    """Check if credentials.json exists and is valid"""
    creds_file = Path(__file__).parent / 'credentials.json'
    
    if not creds_file.exists():
        print("❌ credentials.json not found!")
        print(f"Expected location: {creds_file}")
        return False
    
    try:
        with open(creds_file, 'r') as f:
            creds_data = json.load(f)
        
        # Check if it's the right type of credentials
        if 'installed' in creds_data:
            print("✅ Desktop application credentials found")
            return True
        else:
            print("❌ Wrong credential type. Need 'Desktop application' credentials")
            return False
            
    except Exception as e:
        print(f"❌ Error reading credentials file: {e}")
        return False

def test_simple_auth():
    """Test authentication with better error handling"""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        
        print("✅ Google API libraries imported successfully")
        
        # Check credentials file
        if not check_credentials_file():
            return False
        
        # Test authentication flow
        SCOPES = [
            'https://www.googleapis.com/auth/drive.metadata.readonly',  # Less sensitive scope for testing
        ]
        
        creds_file = Path(__file__).parent / 'credentials.json'
        
        print("🔐 Starting authentication flow...")
        print("⚠️  If you see 'access_denied' error, complete OAuth consent setup first!")
        
        flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
        
        # Try authentication
        try:
            creds = flow.run_local_server(port=0, open_browser=True)
            print("✅ Authentication successful!")
            
            # Test API access
            service = build('drive', 'v3', credentials=creds)
            results = service.files().list(pageSize=1).execute()
            
            print("✅ Google Drive API access confirmed")
            return True
            
        except Exception as auth_error:
            print(f"❌ Authentication failed: {auth_error}")
            
            if "access_denied" in str(auth_error):
                print()
                print("🔧 This is likely an OAuth consent screen issue.")
                print("Please complete the OAuth setup steps above.")
                return False
            else:
                print(f"🔧 Unexpected error: {auth_error}")
                return False
        
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Run: pip install google-auth google-auth-oauthlib google-api-python-client")
        return False

def main():
    """Main authentication test"""
    print("🔐 GCAP 3226 Authentication Setup")
    print("=" * 35)
    print()
    
    # Check if OAuth setup is complete
    if not setup_oauth_consent_screen():
        print("⏸️  Please complete OAuth consent screen setup first.")
        return
    
    # Test authentication
    print("🧪 Testing authentication...")
    success = test_simple_auth()
    
    if success:
        print()
        print("🎉 AUTHENTICATION SETUP COMPLETE!")
        print("✅ Ready to create team folders and documents")
        print("✅ Run: python team_manager.py")
    else:
        print()
        print("❌ Authentication setup incomplete")
        print("📋 Please review the OAuth consent screen setup steps")

if __name__ == "__main__":
    main()

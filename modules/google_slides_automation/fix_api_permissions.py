#!/usr/bin/env python3
"""
Fix Google API Permissions
Troubleshoot and fix Google Drive API access issues.
"""

import webbrowser
import time
import os


def check_api_status():
    """Check current API status and fix permissions."""
    
    print("🔍 Diagnosing Google API Issues")
    print("=" * 35)
    
    project_id = "452791587294"
    
    # Check if we can authenticate first
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        import pickle
        
        print("✅ Google API libraries available")
        
        # Load credentials
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', [
                    'https://www.googleapis.com/auth/drive.file',
                    'https://www.googleapis.com/auth/presentations'
                ])
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        print("✅ Authentication successful")
        
        # Test Google Slides API (this worked)
        try:
            slides_service = build('slides', 'v1', credentials=creds)
            print("✅ Google Slides API - Working")
        except Exception as e:
            print(f"❌ Google Slides API - Error: {e}")
        
        # Test Google Drive API (this failed)
        try:
            drive_service = build('drive', 'v3', credentials=creds)
            # Try a simple operation
            about = drive_service.about().get(fields='user').execute()
            print("✅ Google Drive API - Working")
            return True
        except Exception as e:
            print(f"❌ Google Drive API - Error: {e}")
            print("🔧 Need to fix Drive API permissions")
            return False
            
    except ImportError as e:
        print(f"❌ Missing library: {e}")
        return False


def fix_drive_api():
    """Fix Google Drive API permissions."""
    
    print("\n🛠️  Fixing Google Drive API Access")
    print("=" * 35)
    
    project_id = "452791587294"
    
    # Direct links to enable APIs
    apis = [
        {
            'name': 'Google Drive API',
            'enable_url': f'https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project={project_id}',
            'library_url': f'https://console.developers.google.com/apis/library/drive.googleapis.com?project={project_id}'
        }
    ]
    
    for api in apis:
        print(f"\n🔧 Fixing {api['name']}...")
        print("Method 1: Direct enable")
        print(f"Opening: {api['enable_url']}")
        webbrowser.open(api['enable_url'])
        
        print("\n📋 Steps:")
        print("1. If you see 'ENABLE' button → Click it")
        print("2. If it says 'MANAGE' → API is already enabled")
        print("3. If you get an error → Try Method 2")
        
        response = input("Did the API enable successfully? (y/n/try-method-2): ").lower()
        
        if response == 'try-method-2':
            print(f"\nMethod 2: Via API Library")
            print(f"Opening: {api['library_url']}")
            webbrowser.open(api['library_url'])
            
            print("\n📋 Steps:")
            print("1. Search for 'Google Drive API'")
            print("2. Click on it")
            print("3. Click 'ENABLE'")
            
            input("Press Enter when done...")
        
        elif response != 'y':
            print("⚠️  API might not be properly enabled")
    
    print("\n⏳ Waiting for API propagation (60 seconds)...")
    for i in range(60, 0, -1):
        print(f"\r   Waiting... {i:2d} seconds remaining", end="", flush=True)
        time.sleep(1)
    print()


def test_fixed_apis():
    """Test if the API fix worked."""
    
    print("\n🧪 Testing Fixed APIs")
    print("=" * 22)
    
    if check_api_status():
        print("✅ All APIs working! Attempting to set sharing permissions...")
        
        # Try to set sharing on the existing presentation
        try:
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            import pickle
            
            # Load credentials
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
            
            drive_service = build('drive', 'v3', credentials=creds)
            
            presentation_id = "1_6aRzEFlUnvTPSSG5vtgFTKhxo5NpajnynDekjiiNgs"
            
            # Set sharing permissions
            permission = {
                'type': 'anyone',
                'role': 'writer'
            }
            
            drive_service.permissions().create(
                fileId=presentation_id,
                body=permission
            ).execute()
            
            print("✅ Sharing permissions set successfully!")
            print("🔓 Anyone with the link can now edit the presentation")
            
            presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
            print(f"🔗 Your presentation: {presentation_url}")
            
            # Copy to clipboard
            try:
                import subprocess
                subprocess.run(['pbcopy'], input=presentation_url, text=True, check=True)
                print("📋 Link copied to clipboard!")
            except:
                pass
            
            return True
            
        except Exception as e:
            print(f"❌ Still failed: {e}")
            return False
    else:
        print("❌ APIs still not working properly")
        return False


def manual_sharing_guide():
    """Provide manual sharing instructions."""
    
    presentation_id = "1_6aRzEFlUnvTPSSG5vtgFTKhxo5NpajnynDekjiiNgs"
    presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    
    print("\n📋 Manual Sharing Instructions")
    print("=" * 35)
    print(f"🔗 Presentation: {presentation_url}")
    print("\nSteps to enable sharing:")
    print("1. Open the presentation link above")
    print("2. Click the 'Share' button (top right corner)")
    print("3. Under 'General access', click 'Restricted'")
    print("4. Select 'Anyone with the link'")
    print("5. Change role from 'Viewer' to 'Editor'")
    print("6. Click 'Done'")
    print("7. Click 'Copy link' to share with others")
    
    print("\n✨ Your presentation structure:")
    print("   1. Title - Service Learning Sharing Session")
    print("   2. Dr. Joshua Chan - Service Learning Methods")
    print("   3. Dr. Nancy Guo - Language Learning & Impact")  
    print("   4. Dr. Simon Wang - LANG 2077 Integration")
    print("   5. Thank You & Discussion")
    print("   🎨 Each slide has colorful backgrounds!")


def main():
    """Main function to fix API permissions."""
    
    print("🔧 Google API Permission Fixer")
    print("=" * 30)
    
    # Step 1: Check current status
    if check_api_status():
        print("🎉 APIs are working! No fix needed.")
        if test_fixed_apis():
            print("✅ All done!")
        else:
            manual_sharing_guide()
    else:
        # Step 2: Fix the APIs
        fix_drive_api()
        
        # Step 3: Test again
        if test_fixed_apis():
            print("🎉 Fixed! APIs now working.")
        else:
            print("❌ Manual intervention needed")
            manual_sharing_guide()


if __name__ == "__main__":
    main()

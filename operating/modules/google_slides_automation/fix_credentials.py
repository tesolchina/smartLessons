#!/usr/bin/env python3
"""
Fix Google Credentials
Create correct Desktop Application credentials automatically.
"""

import webbrowser
import time
import os


def open_credentials_setup():
    """Open Google Cloud Console to create desktop credentials."""
    
    print("🔧 Creating Desktop Application Credentials")
    print("=" * 45)
    
    # Check if we have the project from before
    if os.path.exists('credentials.json'):
        print("📋 Found existing credentials (wrong type)")
        backup_name = f'credentials_backup_{int(time.time())}.json'
        os.rename('credentials.json', backup_name)
        print(f"💾 Backed up as: {backup_name}")
    
    print("\n🌐 Opening Google Cloud Console...")
    
    # Direct link to create OAuth credentials
    console_url = "https://console.cloud.google.com/apis/credentials"
    
    print(f"Opening: {console_url}")
    webbrowser.open(console_url)
    
    print("\n📋 Follow these steps:")
    print("=" * 25)
    print("1. ✅ Select your existing project (should already be done)")
    print("2. 🔵 Click '+ CREATE CREDENTIALS'")
    print("3. 📱 Select 'OAuth 2.0 Client IDs'")
    print("4. 🖥️  Application type: 'Desktop application'")  # This is key!
    print("5. ✏️  Name: 'LANG2077 Slides Uploader'")
    print("6. 🎯 Click 'CREATE'")
    print("7. 💾 Click 'DOWNLOAD JSON'")
    print("8. 📁 Save as 'credentials.json' in this folder:")
    print(f"   {os.getcwd()}")
    
    print("\n⚠️  IMPORTANT: Choose 'Desktop application', not 'Web application'!")
    
    # Wait for user
    input("\n⏳ Press Enter when you've downloaded the new credentials.json...")
    
    # Verify the new credentials
    if os.path.exists('credentials.json'):
        import json
        try:
            with open('credentials.json', 'r') as f:
                creds = json.load(f)
            
            if 'installed' in creds:
                print("✅ Perfect! Desktop application credentials detected.")
                print("🚀 Ready to upload to Google Slides!")
                return True
            else:
                print("❌ Still wrong credential type. Please try again.")
                print("   Make sure to select 'Desktop application'")
                return False
                
        except Exception as e:
            print(f"❌ Error reading credentials: {e}")
            return False
    else:
        print("❌ credentials.json not found. Please download it.")
        return False


def main():
    """Main function to fix credentials."""
    
    print("🛠️  Google Credentials Fixer")
    print("=" * 30)
    
    if open_credentials_setup():
        print("\n✨ Credentials fixed! Now running the upload...")
        
        # Run the simple upload
        os.system('python3 simple_upload.py')
    else:
        print("\n❌ Credentials setup incomplete.")
        print("Please run this script again when ready.")


if __name__ == "__main__":
    main()

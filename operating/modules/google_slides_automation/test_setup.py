#!/usr/bin/env python3
"""
Google Slides Upload Test
Test connection to PowerPoint files and prepare for Google Slides upload.
"""

import os
import sys
from datetime import datetime


def check_powerpoint_files():
    """Check available PowerPoint files for upload."""
    
    print("🔍 Checking PowerPoint Files for Google Slides Upload")
    print("=" * 60)
    
    # Path to generated slides
    slides_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/generated_slides"
    
    if not os.path.exists(slides_dir):
        print(f"❌ Slides directory not found: {slides_dir}")
        return []
    
    # Find PowerPoint files
    pptx_files = []
    for file in os.listdir(slides_dir):
        if file.endswith('.pptx'):
            file_path = os.path.join(slides_dir, file)
            file_size = os.path.getsize(file_path)
            modified_time = os.path.getmtime(file_path)
            modified_date = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
            
            pptx_files.append({
                'name': file,
                'path': file_path,
                'size': file_size,
                'modified': modified_date,
                'modified_timestamp': modified_time
            })
    
    if not pptx_files:
        print("❌ No PowerPoint files found")
        return []
    
    # Sort by modification time (newest first)
    pptx_files.sort(key=lambda x: x['modified_timestamp'], reverse=True)
    
    print(f"✅ Found {len(pptx_files)} PowerPoint files:")
    print()
    
    for i, file in enumerate(pptx_files, 1):
        size_mb = file['size'] / (1024 * 1024)
        print(f"   {i}. {file['name']}")
        print(f"      📅 Modified: {file['modified']}")
        print(f"      📏 Size: {size_mb:.1f} MB")
        print(f"      📁 Path: {file['path']}")
        print()
    
    # Recommend latest file
    latest_file = pptx_files[0]
    print(f"🎯 Recommended for upload: {latest_file['name']}")
    print(f"   (Most recently modified)")
    
    return pptx_files


def check_google_api_setup():
    """Check Google API setup requirements."""
    
    print("\n🔐 Google API Setup Check")
    print("=" * 30)
    
    # Check if credentials.json exists
    creds_file = "credentials.json"
    if os.path.exists(creds_file):
        print("✅ credentials.json found")
    else:
        print("❌ credentials.json not found")
        print("   📋 Setup required:")
        print("   1. Go to: https://console.cloud.google.com/")
        print("   2. Enable Google Slides API and Google Drive API")
        print("   3. Create OAuth 2.0 credentials")
        print("   4. Download as 'credentials.json'")
        return False
    
    # Check if token.pickle exists (saved authentication)
    token_file = "token.pickle"
    if os.path.exists(token_file):
        print("✅ Authentication token found")
        print("   (Previous login saved)")
    else:
        print("⚠️  No authentication token")
        print("   (Will prompt for login on first run)")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    required_packages = [
        'google-api-python-client',
        'google-auth-httplib2', 
        'google-auth-oauthlib'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Install with: pip install {package}")
    
    return True


def simulate_upload_process():
    """Simulate the upload process without actually uploading."""
    
    files = check_powerpoint_files()
    if not files:
        return
    
    print("\n🎬 Upload Process Simulation")
    print("=" * 35)
    
    latest_file = files[0]
    
    print(f"📤 Would upload: {latest_file['name']}")
    print(f"📊 File size: {latest_file['size'] / (1024 * 1024):.1f} MB")
    print(f"🎯 Target: Google Slides")
    print(f"🔒 Permissions: Anyone with link can edit")
    print(f"🏷️  Title: LANG 2077: Language Skills for human-AI partnership")
    
    print("\n✅ Process would:")
    print("   1. Authenticate with Google API")
    print("   2. Upload PowerPoint to Google Drive")  
    print("   3. Convert to Google Slides format")
    print("   4. Set sharing permissions")
    print("   5. Return shareable link")
    
    print(f"\n🔗 Expected result: Shareable Google Slides link")
    print(f"   Students can edit, comment, and collaborate")


def main():
    """Main test function."""
    
    print("🎓 HKBU LANG 2077 - Google Slides Upload Test")
    print("=" * 50)
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 Working directory: {script_dir}")
    
    # Check files
    files = check_powerpoint_files()
    
    # Check API setup
    api_ready = check_google_api_setup()
    
    # Simulate process
    if files:
        simulate_upload_process()
    
    # Next steps
    print("\n📋 Next Steps:")
    if not api_ready:
        print("   1. Set up Google Cloud Console project")
        print("   2. Enable Google Slides and Drive APIs")  
        print("   3. Create OAuth credentials")
        print("   4. Download credentials.json")
        print("   5. Install dependencies: pip install -r requirements.txt")
    else:
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run: python3 google_slides_uploader.py")
        print("   3. Authenticate with Google account")
        print("   4. Get shareable link for collaboration")
    
    if files:
        print(f"\n✅ Ready to upload: {len(files)} PowerPoint files available")
    else:
        print(f"\n❌ No files to upload - create slides first")
        print(f"   Run: cd ../canva_automation && python3 create_lang2077_from_content.py")


if __name__ == "__main__":
    main()

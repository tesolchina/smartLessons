#!/usr/bin/env python3
"""
Quick Google Slides Upload Guide
Manual upload process for immediate sharing without API setup.
"""

import os
import webbrowser
import shutil
from datetime import datetime


def find_latest_presentation():
    """Find the latest PowerPoint presentation."""
    
    slides_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/generated_slides"
    
    if not os.path.exists(slides_dir):
        return None
    
    pptx_files = [f for f in os.listdir(slides_dir) if f.endswith('.pptx')]
    if not pptx_files:
        return None
    
    # Find most recent file
    latest_file = max(pptx_files, key=lambda f: os.path.getmtime(os.path.join(slides_dir, f)))
    return os.path.join(slides_dir, latest_file)


def copy_to_desktop(file_path):
    """Copy the presentation to desktop for easy access."""
    
    if not file_path or not os.path.exists(file_path):
        return None
    
    desktop_path = os.path.expanduser("~/Desktop")
    filename = os.path.basename(file_path)
    
    # Create a simplified name
    timestamp = datetime.now().strftime("%Y%m%d")
    simple_name = f"LANG2077_Slides_{timestamp}.pptx"
    
    desktop_file = os.path.join(desktop_path, simple_name)
    
    try:
        shutil.copy2(file_path, desktop_file)
        print(f"✅ Copied to desktop: {simple_name}")
        return desktop_file
    except Exception as e:
        print(f"❌ Copy failed: {e}")
        return None


def manual_upload_guide():
    """Guide user through manual upload process."""
    
    print("🎓 LANG 2077 - Quick Google Slides Upload")
    print("=" * 45)
    
    # Find presentation file
    latest_file = find_latest_presentation()
    
    if not latest_file:
        print("❌ No PowerPoint files found")
        print("   Create slides first:")
        print("   cd ../canva_automation")
        print("   python3 create_lang2077_from_content.py")
        return
    
    print(f"📊 Found presentation: {os.path.basename(latest_file)}")
    
    # Copy to desktop for easy access
    desktop_file = copy_to_desktop(latest_file)
    
    print("\n🚀 Manual Upload Process:")
    print("=" * 30)
    
    print("1. 📁 Open Google Drive")
    input("   Press Enter to open Google Drive...")
    
    webbrowser.open("https://drive.google.com/")
    
    print("\n2. 📤 Upload PowerPoint File")
    print("   • Click 'New' button")
    print("   • Select 'File upload'")
    if desktop_file:
        print(f"   • Choose: {os.path.basename(desktop_file)} (from Desktop)")
    else:
        print(f"   • Choose: {os.path.basename(latest_file)}")
    print("   • Wait for upload to complete")
    
    input("\nPress Enter when file is uploaded...")
    
    print("\n3. 🔄 Convert to Google Slides")
    print("   • Right-click the uploaded .pptx file")
    print("   • Select 'Open with' > 'Google Slides'")
    print("   • Google Slides will convert the file")
    
    input("\nPress Enter when converted to Google Slides...")
    
    print("\n4. 🔒 Set Sharing Permissions")
    print("   • Click 'Share' button (top right)")
    print("   • Change 'Restricted' to 'Anyone with the link'")
    print("   • Set permission to 'Editor' (can edit)")
    print("   • Click 'Copy link'")
    
    input("\nPress Enter when sharing is configured...")
    
    print("\n5. ✅ Share the Link")
    print("   • Paste the link in email/message")
    print("   • Students can now edit the slides")
    print("   • Real-time collaboration enabled")
    
    print(f"\n🎉 Success! Your LANG 2077 slides are now shareable!")
    print(f"📋 Title suggestion: 'LANG 2077: Language Skills for human-AI partnership'")
    print(f"👥 Permissions: Anyone with link can edit")
    
    # Cleanup desktop copy
    if desktop_file and os.path.exists(desktop_file):
        cleanup = input(f"\nRemove desktop copy? (y/n): ").lower().strip()
        if cleanup == 'y':
            os.remove(desktop_file)
            print(f"🗑️  Removed: {os.path.basename(desktop_file)}")


def quick_start():
    """Quick start option - just open necessary pages."""
    
    print("🚀 Quick Start - Open Google Drive")
    print("=" * 35)
    
    latest_file = find_latest_presentation()
    
    if latest_file:
        print(f"📊 Ready to upload: {os.path.basename(latest_file)}")
        copy_to_desktop(latest_file)
    else:
        print("❌ No presentations found")
        return
    
    print("\n🌐 Opening Google Drive...")
    webbrowser.open("https://drive.google.com/")
    
    print("\n📋 Quick Steps:")
    print("1. Click 'New' > 'File upload'")
    print("2. Choose the .pptx file from Desktop")
    print("3. Right-click uploaded file > 'Open with' > 'Google Slides'")
    print("4. Click 'Share' > 'Anyone with link' > 'Editor'")
    print("5. Copy and share the link!")


def main():
    """Main menu."""
    
    print("🎓 HKBU LANG 2077 - Google Slides Upload")
    print("=" * 45)
    
    print("\nChoose upload method:")
    print("1. 📖 Guided manual upload (step-by-step)")
    print("2. 🚀 Quick start (just open Google Drive)")
    print("3. 🔧 Set up Google API (for automation)")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        manual_upload_guide()
    elif choice == "2":
        quick_start()
    elif choice == "3":
        print("\n🔧 For API setup, run:")
        print("   python3 setup_credentials.py")
        print("\n📚 Or read the guide:")
        print("   cat SETUP_GUIDE.md")
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()

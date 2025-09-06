#!/usr/bin/env python3
"""
Enable Google APIs
Enable required APIs for the Google Slides upload project.
"""

import webbrowser
import time
import os


def enable_apis():
    """Enable Google Drive and Slides APIs."""
    
    print("🔧 Enabling Google APIs")
    print("=" * 25)
    
    # Project ID from the error
    project_id = "452791587294"
    
    apis_to_enable = [
        {
            'name': 'Google Drive API',
            'url': f'https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project={project_id}'
        },
        {
            'name': 'Google Slides API', 
            'url': f'https://console.developers.google.com/apis/api/slides.googleapis.com/overview?project={project_id}'
        }
    ]
    
    for i, api in enumerate(apis_to_enable, 1):
        print(f"\n{i}. 🔓 Enabling {api['name']}...")
        print(f"   Opening: {api['url']}")
        
        webbrowser.open(api['url'])
        
        print(f"\n   📋 Steps for {api['name']}:")
        print("   - Click the 'ENABLE' button")
        print("   - Wait for confirmation")
        
        input(f"   ⏳ Press Enter when {api['name']} is enabled...")
        
        time.sleep(1)  # Brief pause between APIs
    
    print("\n✅ All APIs should now be enabled!")
    print("⏳ Waiting 30 seconds for changes to propagate...")
    
    # Countdown
    for i in range(30, 0, -1):
        print(f"\r   Waiting... {i:2d} seconds remaining", end="", flush=True)
        time.sleep(1)
    
    print("\n\n🚀 Ready to try upload again!")


def main():
    """Main function."""
    
    print("⚡ Google APIs Enabler")
    print("=" * 25)
    
    enable_apis()
    
    print("\n🎯 Now attempting upload...")
    os.system('python3 simple_upload.py')


if __name__ == "__main__":
    main()

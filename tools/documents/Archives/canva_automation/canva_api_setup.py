#!/usr/bin/env python3
"""
Canva Connect API Setup Assistant
Guides user through API credential setup
Created: September 6, 2025
"""

import os
import json
import webbrowser
from datetime import datetime

def setup_canva_connect_api():
    """Interactive setup for Canva Connect API"""
    
    print("🔧 Canva Connect API Setup Assistant")
    print("=" * 45)
    print()
    
    print("This will guide you through setting up Canva Connect API for true CLI access.")
    print("No browser automation needed - direct API calls!")
    print()
    
    # Step 1: Account Setup
    print("📋 Step 1: Canva Developer Account")
    print("-" * 35)
    print("1. You need a Canva developer account")
    print("2. It's free and separate from your regular Canva account")
    print()
    
    response = input("Do you have a Canva developer account? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("🌐 Opening Canva Developer Portal...")
        webbrowser.open("https://developers.canva.com/")
        print()
        print("📝 Please:")
        print("   1. Sign up for a developer account")
        print("   2. Verify your email")
        print("   3. Come back here when ready")
        input("Press Enter when you have a developer account...")
    
    # Step 2: Create Connect API App
    print("\n📋 Step 2: Create Connect API App")
    print("-" * 35)
    print("1. Go to the Canva Developers Console")
    print("2. Click 'Create an app'")
    print("3. Choose 'Connect API' (not Apps SDK)")
    print("4. Fill in your app details:")
    print("   - App name: 'HKBU Language Centre CLI'")
    print("   - Description: 'CLI tool for creating presentations'")
    print("   - App type: 'Internal use'")
    print()
    
    response = input("Open Canva Developers Console? (Y/n): ").strip().lower()
    if response not in ['n', 'no']:
        webbrowser.open("https://developers.canva.com/console")
    
    print("\n📋 Step 3: Configure API Scopes")
    print("-" * 30)
    print("In your app settings, enable these scopes:")
    print("   ✅ design:content:read")
    print("   ✅ design:content:write") 
    print("   ✅ asset:read")
    print("   ✅ asset:write")
    print("   ✅ folder:read")
    print("   ✅ folder:write")
    print()
    
    # Step 4: Get Access Token
    print("📋 Step 4: Get Access Token")
    print("-" * 25)
    print("1. In your app dashboard, go to 'Authentication'")
    print("2. Generate a new access token")
    print("3. Copy the token (it starts with 'canva_...')")
    print("4. IMPORTANT: Save it securely - you can't see it again!")
    print()
    
    access_token = input("Paste your access token here: ").strip()
    
    if not access_token:
        print("❌ No access token provided. Setup incomplete.")
        return False
    
    if not access_token.startswith('canva_'):
        print("⚠️  Access token should start with 'canva_'")
        confirm = input("Continue anyway? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            return False
    
    # Step 5: Save Configuration
    print("\n📋 Step 5: Save Configuration")
    print("-" * 27)
    
    env_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/.env"
    
    # Read existing .env file or create new
    env_content = {}
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_content[key] = value
    
    # Add API configuration
    env_content['CANVA_ACCESS_TOKEN'] = access_token
    env_content['CANVA_EMAIL'] = 'simonwang@hkbu.edu.hk'
    env_content['DEFAULT_EXPORT_FORMAT'] = 'pdf'
    
    # Write updated .env file
    with open(env_file, 'w') as f:
        f.write("# Canva API Configuration\n")
        f.write(f"# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for key, value in env_content.items():
            f.write(f"{key}={value}\n")
    
    print(f"✅ Configuration saved to {env_file}")
    
    # Step 6: Test Connection
    print("\n📋 Step 6: Test API Connection")
    print("-" * 28)
    
    test_response = input("Test the API connection now? (Y/n): ").strip().lower()
    if test_response not in ['n', 'no']:
        print("🧪 Testing API connection...")
        
        # Import and test the API
        try:
            import sys
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from canva_connect_api import CanvaConnectAPI
            
            api = CanvaConnectAPI()
            if api.check_api_connection():
                print("🎉 Setup completed successfully!")
                return True
            else:
                print("❌ API test failed. Please check your token.")
                return False
        except ImportError:
            print("⚠️  Could not test API. Please run manually:")
            print("python3 canva_connect_api.py --test")
    
    # Step 7: Usage Examples
    print("\n🚀 Ready to Use!")
    print("-" * 15)
    print("Try these commands:")
    print()
    print("# Test API connection")
    print("python3 canva_connect_api.py --test")
    print()
    print("# Create LANG 2077 slides")
    print("python3 canva_connect_api.py --create lang2077")
    print()
    print("# Create custom presentation")
    print("python3 canva_connect_api.py --create presentation --title 'My Presentation'")
    print()
    print("# Create and share with collaborators")
    print("python3 canva_connect_api.py --create presentation --collaborators user1@hkbu.edu.hk user2@hkbu.edu.hk")
    print()
    
    return True

def check_requirements():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    missing_packages = []
    
    try:
        import requests
    except ImportError:
        missing_packages.append("requests")
    
    try:
        from dotenv import load_dotenv
    except ImportError:
        missing_packages.append("python-dotenv")
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip3 install " + " ".join(missing_packages))
        return False
    
    print("✅ All dependencies installed")
    return True

def main():
    """Main setup function"""
    print("🎨 Welcome to Canva Connect API CLI Setup")
    print("=" * 45)
    print()
    
    if not check_requirements():
        return
    
    print("This setup will enable you to:")
    print("✅ Create Canva designs via CLI (no browser needed)")
    print("✅ Add text, images, and elements programmatically") 
    print("✅ Share designs with collaborators automatically")
    print("✅ Export designs to PDF, PNG, JPG")
    print("✅ Manage designs and assets via API")
    print()
    
    proceed = input("Ready to set up Canva Connect API? (Y/n): ").strip().lower()
    if proceed in ['n', 'no']:
        print("Setup cancelled.")
        return
    
    success = setup_canva_connect_api()
    
    if success:
        print("\n🎉 Canva Connect API setup complete!")
        print("You can now create presentations via CLI without any browser automation!")
    else:
        print("\n❌ Setup incomplete. Please try again or check the documentation.")

if __name__ == "__main__":
    main()

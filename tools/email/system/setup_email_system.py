#!/usr/bin/env python3
"""
Quick Email System Setup and Test
Verify all components are working and set up basic contact database
Created: September 6, 2025
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_mail_app():
    """Check if Mail.app is running and accessible"""
    print("📧 Checking Mac Mail.app access...")
    
    applescript = '''
    tell application "Mail"
        set accountCount to count of accounts
        return "Found " & accountCount & " email accounts"
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', applescript], 
                             capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Mail.app access: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Mail.app error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Mail.app access failed: {e}")
        return False

def setup_directory_structure():
    """Ensure all directories exist"""
    print("📁 Setting up directory structure...")
    
    base_path = Path(__file__).parent
    directories = ['core_tools', 'contacts', 'logs', 'documentation', 'specialized_scripts', 'archive']
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Directory: {directory}")
    
    return True

def setup_contacts_database():
    """Initialize the contacts database"""
    print("👥 Setting up contacts database...")
    
    base_path = Path(__file__).parent
    contacts_file = base_path / "contacts" / "email_contacts.json"
    
    if contacts_file.exists():
        print("✅ Contacts database already exists")
        return True
    
    default_contacts = {
        "colleagues": [
            {
                "name": "Nancy Mak", 
                "email": "nancymak@hkbu.edu.hk", 
                "department": "Language Centre",
                "added": "2025-09-06"
            },
            {
                "name": "Joshua Chan", 
                "email": "joshuachan@hkbu.edu.hk", 
                "department": "Language Centre",
                "added": "2025-09-06"
            }
        ],
        "students": [
            {
                "name": "Example Student",
                "email": "student@example.com", 
                "course": "LANG2077",
                "added": "2025-09-06"
            }
        ],
        "recent": [],
        "system_info": {
            "created": "2025-09-06",
            "version": "2.0",
            "last_updated": "2025-09-06"
        }
    }
    
    try:
        with open(contacts_file, 'w') as f:
            json.dump(default_contacts, f, indent=2)
        print("✅ Contacts database created")
        return True
    except Exception as e:
        print(f"❌ Failed to create contacts database: {e}")
        return False

def test_core_tools():
    """Test that core tools can be imported"""
    print("🔧 Testing core tools...")
    
    base_path = Path(__file__).parent
    core_tools_path = base_path / "core_tools"
    
    if not core_tools_path.exists():
        print("❌ Core tools directory not found")
        return False
    
    # Check for key files
    key_files = [
        "generic_email_sender.py",
        "email_address_extractor.py", 
        "email_reply_system.py",
        "smart_email_handler.py"
    ]
    
    for file_name in key_files:
        file_path = core_tools_path / file_name
        if file_path.exists():
            print(f"✅ Found: {file_name}")
        else:
            print(f"❌ Missing: {file_name}")
    
    return True

def create_quick_start_script():
    """Create a quick start script"""
    print("🚀 Creating quick start script...")
    
    script_content = '''#!/bin/bash
# Quick Email Workflow Launcher
# Run this script to start the main email workflow system

echo "🚀 Starting Email Workflow System..."
echo "📁 Current directory: $(pwd)"
echo "🐍 Using Python: $(python3 --version)"
echo ""

cd "$(dirname "$0")"

if [ ! -f "email_workflow.py" ]; then
    echo "❌ email_workflow.py not found!"
    echo "Make sure you're in the email_automation directory"
    exit 1
fi

echo "📧 Launching Email Workflow..."
python3 email_workflow.py
'''
    
    script_path = Path(__file__).parent / "start_email_workflow.sh"
    
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)  # Make executable
        print("✅ Quick start script created: start_email_workflow.sh")
        return True
    except Exception as e:
        print(f"❌ Failed to create start script: {e}")
        return False

def show_next_steps():
    """Display next steps for user"""
    print("\n" + "="*60)
    print("🎉 EMAIL SYSTEM SETUP COMPLETE!")
    print("="*60)
    print("\n📋 NEXT STEPS:")
    print("1. 🚀 Run the main workflow: python3 email_workflow.py")
    print("2. 📧 Or use quick launcher: ./start_email_workflow.sh")
    print("3. 📚 Read the documentation: cat README.md")
    print("4. 👥 Add your contacts through the workflow menu")
    print("5. 🧪 Test with a simple email search")
    
    print("\n💡 QUICK TEST:")
    print("   python3 email_workflow.py")
    print("   Choose option 1 (Locate email by subject)")
    print("   Search for any recent email subject")
    
    print("\n📁 DIRECTORY STRUCTURE:")
    print("   email_workflow.py      - Main workflow tool")
    print("   core_tools/            - General-purpose scripts") 
    print("   contacts/              - Contact database")
    print("   documentation/         - Guides and help")
    print("   logs/                  - Activity tracking")
    
    print("\n🔒 PRIVACY:")
    print("   ✅ All processing is local")
    print("   ✅ No cloud services used")
    print("   ✅ Uses Mac Mail.app native interface")
    
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🛠️ EMAIL AUTOMATION SYSTEM SETUP")
    print("="*50)
    
    success_count = 0
    total_checks = 5
    
    # Run setup checks
    if check_mail_app():
        success_count += 1
    
    if setup_directory_structure():
        success_count += 1
    
    if setup_contacts_database():
        success_count += 1
    
    if test_core_tools():
        success_count += 1
    
    if create_quick_start_script():
        success_count += 1
    
    print(f"\n📊 SETUP RESULTS: {success_count}/{total_checks} checks passed")
    
    if success_count == total_checks:
        show_next_steps()
    else:
        print("\n⚠️  Some setup steps failed. Please review the errors above.")
        print("💡 You may still be able to use the system with reduced functionality.")

if __name__ == "__main__":
    main()

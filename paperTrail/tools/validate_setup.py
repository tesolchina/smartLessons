#!/usr/bin/env python3
"""
Paper Trail System Setup Script
Validates folder structure and tool functionality
Created: September 6, 2025
"""

import os
import json
from pathlib import Path
from datetime import datetime

def validate_paper_trail_setup():
    """Validate that the paper trail system is set up correctly"""
    
    print("🔍 Validating Paper Trail System Setup...\n")
    
    # Get paths
    script_dir = Path(__file__).parent
    paper_trail_root = script_dir.parent
    daily_assistant_root = paper_trail_root.parent
    
    print(f"📁 Paper Trail Root: {paper_trail_root}")
    print(f"📁 Daily Assistant Root: {daily_assistant_root}\n")
    
    # Check folder structure
    required_folders = [
        "tools",
        "integrations", 
        "daily_logs",
        "decisions",
        "reports",
        "templates",
        "documentation"
    ]
    
    print("📋 Checking Folder Structure...")
    all_folders_exist = True
    for folder in required_folders:
        folder_path = paper_trail_root / folder
        if folder_path.exists():
            print(f"  ✅ {folder}/")
        else:
            print(f"  ❌ {folder}/ (missing)")
            all_folders_exist = False
    
    # Check key files
    key_files = [
        "MASTER_ACTIVITY_TRAIL.md",
        "README.md", 
        "HOW_IT_WORKS.md",
        "tools/update_paper_trail.py",
        "integrations/setup_obsidian_integration.py",
        "templates/daily_log_template.md",
        "templates/decision_record_template.md"
    ]
    
    print("\n📄 Checking Key Files...")
    all_files_exist = True
    for file_path in key_files:
        full_path = paper_trail_root / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")
            all_files_exist = False
    
    # Test tool imports
    print("\n🔧 Testing Tool Imports...")
    try:
        import sys
        sys.path.insert(0, str(paper_trail_root / "tools"))
        
        # Test update_paper_trail import
        try:
            from update_paper_trail import PaperTrailUpdater
            updater = PaperTrailUpdater()
            print("  ✅ update_paper_trail.py imports successfully")
            print(f"    - Trail file path: {updater.trail_file}")
            print(f"    - Daily logs path: {updater.daily_logs_path}")
        except Exception as e:
            print(f"  ❌ update_paper_trail.py import failed: {e}")
            all_files_exist = False
            
    except Exception as e:
        print(f"  ❌ Tool import test failed: {e}")
        all_files_exist = False
    
    # Summary
    print(f"\n{'='*50}")
    if all_folders_exist and all_files_exist:
        print("🎉 Paper Trail System Setup: COMPLETE")
        print("\n🚀 Ready to use! Try these commands:")
        print("   cd paperTrail/tools && python update_paper_trail.py")
        print("   cd paperTrail && cat MASTER_ACTIVITY_TRAIL.md")
        print("   cd paperTrail/integrations && python setup_obsidian_integration.py")
    else:
        print("⚠️  Paper Trail System Setup: INCOMPLETE")
        print("\n🔧 Some files or folders are missing. Check the errors above.")
        print("   You may need to re-run the setup process.")
    
    print(f"{'='*50}\n")

def create_sample_daily_log():
    """Create a sample daily log for today"""
    paper_trail_root = Path(__file__).parent.parent
    daily_logs_path = paper_trail_root / "daily_logs"
    template_path = paper_trail_root / "templates" / "daily_log_template.md"
    
    today = datetime.now().strftime("%Y-%m-%d")
    sample_log_path = daily_logs_path / f"{today}_sample_daily_log.md"
    
    if template_path.exists() and not sample_log_path.exists():
        # Read template
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Replace placeholders with sample data
        sample_content = template_content.replace("[YYYY-MM-DD]", today)
        sample_content = sample_content.replace("[Morning/Afternoon/Evening]", "Morning")
        sample_content = sample_content.replace("[HH:MM]", "09:00")
        sample_content = sample_content.replace("[Main goal/project for this session]", "Set up Paper Trail System")
        sample_content = sample_content.replace("[High/Medium/Low]", "High")
        
        # Write sample log
        with open(sample_log_path, 'w') as f:
            f.write(sample_content)
            
        print(f"📝 Created sample daily log: {sample_log_path}")
        return True
    
    return False

if __name__ == "__main__":
    validate_paper_trail_setup()
    
    # Ask if user wants to create sample daily log
    response = input("🤔 Create a sample daily log for today? (y/n): ").strip().lower()
    if response in ['y', 'yes']:
        if create_sample_daily_log():
            print("✅ Sample daily log created successfully!")
        else:
            print("ℹ️  Sample daily log not created (may already exist or template missing)")
    
    print("\n📚 For complete system overview, read:")
    print("   paperTrail/HOW_IT_WORKS.md")
    print("   paperTrail/README.md")

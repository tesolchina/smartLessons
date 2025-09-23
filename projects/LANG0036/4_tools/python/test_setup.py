#!/usr/bin/env python3
"""
Quick test script for the Regression Assessment Chatbot
"""

import os
import sys
from pathlib import Path

def test_setup():
    """Test if all required files and configurations are in place."""
    
    print("🧪 Testing Regression Assessor Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"📂 Current directory: {current_dir}")
    
    # Check for required files
    required_files = [
        "regression_assessor.py",
        "mathGuru/mathGuru.json",
        ".env"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    # Check for sample regression files
    print("\\n📊 Available regression analysis files:")
    topic_dirs = Path("../TopicSelectionPM").glob("Topic*")
    regression_files = []
    
    for topic_dir in sorted(topic_dirs):
        regression_file = topic_dir / "Regression_Applications.md"
        if regression_file.exists():
            print(f"✅ {regression_file}")
            regression_files.append(str(regression_file))
        else:
            print(f"❌ Missing: {regression_file}")
    
    # Test API key format
    if Path(".env").exists():
        with open(".env", 'r') as f:
            content = f.read()
            if "OpenRouter Key=" in content:
                print("\\n✅ API key format looks correct")
            else:
                print("\\n❌ API key format issue - should be 'OpenRouter Key=your_key_here'")
                missing_files.append("Correct API key format")
    
    # Test JSON config
    if Path("mathGuru/mathGuru.json").exists():
        try:
            import json
            with open("mathGuru/mathGuru.json", 'r') as f:
                config = json.load(f)
                if "system_prompt" in config and "assessment_prompts" in config:
                    print("✅ Configuration file format is valid")
                else:
                    print("❌ Configuration file missing required fields")
                    missing_files.append("Valid JSON config")
        except json.JSONDecodeError:
            print("❌ Configuration file contains invalid JSON")
            missing_files.append("Valid JSON syntax")
    
    # Summary
    print("\\n" + "=" * 50)
    if missing_files:
        print(f"❌ Setup incomplete. Missing: {', '.join(missing_files)}")
        return False, regression_files
    else:
        print("✅ Setup complete! Ready to assess regression documents.")
        return True, regression_files

def suggest_test_commands(regression_files):
    """Suggest test commands to try."""
    if not regression_files:
        print("\\n📝 No regression files found to test with.")
        return
    
    print("\\n📝 Suggested test commands:")
    print("-" * 30)
    
    # Use the first available file for examples
    test_file = regression_files[0]
    
    print(f"# Quick test (fastest)")
    print(f"python regression_assessor.py '{test_file}' --type quick")
    print()
    
    print(f"# Technical assessment")
    print(f"python regression_assessor.py '{test_file}' --type technical")
    print()
    
    print(f"# Full assessment with output file")
    print(f"python regression_assessor.py '{test_file}' --output test_results.md")
    print()
    
    print(f"# Test all files (run each manually)")
    for i, file_path in enumerate(regression_files[:3], 1):  # Show first 3
        print(f"python regression_assessor.py '{file_path}' --type quick")
    
    if len(regression_files) > 3:
        print(f"# ... and {len(regression_files) - 3} more files")

def main():
    """Run setup test."""
    try:
        # Change to chatbot directory if not already there
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        setup_ok, regression_files = test_setup()
        
        if setup_ok:
            suggest_test_commands(regression_files)
            print("\\n🚀 Ready to run assessments!")
        else:
            print("\\n🛠️  Please fix the missing components before testing.")
            
    except Exception as e:
        print(f"\\n❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
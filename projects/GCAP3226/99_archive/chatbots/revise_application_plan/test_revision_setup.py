#!/usr/bin/env python3
"""
Test script for the Regression Plan Revision Chatbot
"""

import os
import sys
from pathlib import Path

def test_revision_setup():
    """Test if all required files and configurations are in place for revision."""
    
    print("🧪 Testing Regression Plan Revisor Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"📂 Current directory: {current_dir}")
    
    # Check for required files
    required_files = [
        "plan_revisor.py",
        "revision_config.json",
        "../.env"  # API key in parent directory
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    # Check for example input files (Topic 1)
    print("\\n📊 Available test files:")
    topic1_dir = Path("../../TopicSelectionPM/Topic1_BusFrequency")
    
    test_files = {
        "Original Analysis": topic1_dir / "Regression_Applications.md",
        "AI Feedback": topic1_dir / "AI_Assessment_Results.md",
        "Previous Revision": topic1_dir / "Revised_Regression_Framework.md"
    }
    
    available_tests = []
    for file_type, file_path in test_files.items():
        if file_path.exists():
            print(f"✅ {file_type}: {file_path}")
            available_tests.append(file_path)
        else:
            print(f"❌ Missing {file_type}: {file_path}")
    
    # Test JSON config
    if Path("revision_config.json").exists():
        try:
            import json
            with open("revision_config.json", 'r') as f:
                config = json.load(f)
                required_keys = ["system_prompt", "revision_instructions", "output_formatting"]
                if all(key in config for key in required_keys):
                    print("\\n✅ Configuration file format is valid")
                else:
                    print("\\n❌ Configuration file missing required fields")
                    missing_files.append("Valid JSON config")
        except json.JSONDecodeError:
            print("\\n❌ Configuration file contains invalid JSON")
            missing_files.append("Valid JSON syntax")
    
    # Summary
    print("\\n" + "=" * 50)
    if missing_files:
        print(f"❌ Setup incomplete. Missing: {', '.join(missing_files)}")
        return False, available_tests
    else:
        print("✅ Setup complete! Ready to revise regression documents.")
        return True, available_tests

def suggest_test_commands(available_tests):
    """Suggest test commands to try."""
    if len(available_tests) < 2:
        print("\\n📝 Need both original document and feedback to test revision.")
        return
    
    print("\\n📝 Suggested test commands:")
    print("-" * 30)
    
    # Base files for testing
    original = "../../TopicSelectionPM/Topic1_BusFrequency/Regression_Applications.md"
    feedback = "../../TopicSelectionPM/Topic1_BusFrequency/AI_Assessment_Results.md"
    
    print(f"# Methodology-focused revision")
    print(f'python plan_revisor.py "{original}" "{feedback}" "test_methodology_revision.md" --focus methodology')
    print()
    
    print(f"# Technical-focused revision")
    print(f'python plan_revisor.py "{original}" "{feedback}" "test_technical_revision.md" --focus technical')
    print()
    
    print(f"# Policy-focused revision")
    print(f'python plan_revisor.py "{original}" "{feedback}" "test_policy_revision.md" --focus policy')
    print()
    
    print(f"# Comprehensive revision")
    print(f'python plan_revisor.py "{original}" "{feedback}" "test_comprehensive_revision.md"')
    print()
    
    print("# Test other topics (if available):")
    for i in range(2, 8):
        topic_dir = f"../../TopicSelectionPM/Topic{i}_*"
        print(f"# python plan_revisor.py '{topic_dir}/Regression_Applications.md' '{topic_dir}/AI_Assessment_Results.md' '{topic_dir}/Revised_Framework.md'")

def demonstrate_features():
    """Demonstrate key features of the revision system."""
    print("\\n🎯 Revision System Features:")
    print("-" * 30)
    
    features = [
        "✅ Intelligent Change Tracking - Documents all modifications with rationale",
        "✅ Multiple Focus Areas - methodology, technical, policy, practical, comprehensive",
        "✅ Statistical Enhancement - Addresses endogeneity, interactions, diagnostics",
        "✅ Policy Integration - Maintains practical applicability",
        "✅ Quality Assurance - Academic rigor with implementation feasibility",
        "✅ Detailed Output - Executive summary + revision log + enhanced framework"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\\n🔄 Typical Workflow:")
    print("  1. Original regression analysis document")
    print("  2. AI assessment feedback (from regression_assessor.py)")
    print("  3. Revision with plan_revisor.py")
    print("  4. Enhanced framework with change tracking")

def main():
    """Run revision system test."""
    try:
        # Change to revision chatbot directory if not already there
        script_dir = Path(__file__).parent
        os.chdir(script_dir)
        
        setup_ok, available_tests = test_revision_setup()
        
        if setup_ok:
            suggest_test_commands(available_tests)
            demonstrate_features()
            print("\\n🚀 Ready to revise regression analyses!")
        else:
            print("\\n🛠️  Please fix the missing components before testing.")
            
    except Exception as e:
        print(f"\\n❌ Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
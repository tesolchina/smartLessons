#!/usr/bin/env python3
"""
Quick test for the improvement pipeline
"""

import sys
from pathlib import Path

def test_pipeline_setup():
    """Test if the improvement pipeline is ready to run."""
    
    print("🧪 Testing Improvement Pipeline Setup")
    print("=" * 50)
    
    # Check current directory
    current_dir = Path.cwd()
    expected_dir = Path("/Users/simonwang/Documents/Usage/VibeCoding/GCAP3226prep/Chatbots")
    
    if current_dir != expected_dir:
        print(f"📂 Please run from: {expected_dir}")
        print(f"📂 Current directory: {current_dir}")
        return False, []
    
    # Check required files
    required_files = [
        "improvement_pipeline.py",
        "regression_assessor.py",
        "revise_application_plan/plan_revisor.py",
        ".env"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    # Check topic files
    print("\\n📊 Checking available topics:")
    topics_dir = Path("../TopicSelectionPM")
    topic_names = [
        "Topic1_BusFrequency",
        "Topic2_BusStopMerge", 
        "Topic3_BusRoutesCoordination",
        "Topic4_SolidWasteCharging",
        "Topic5_GreenCommunity",
        "Topic6_FluShotParticipation",
        "Topic7_TyphoonSignal"
    ]
    
    available_topics = []
    for i, topic_name in enumerate(topic_names, 1):
        topic_dir = topics_dir / topic_name
        regression_file = topic_dir / "Regression_Applications.md"
        
        if regression_file.exists():
            print(f"✅ Topic {i}: {topic_name}")
            available_topics.append(i)
        else:
            print(f"❌ Topic {i}: Missing {regression_file}")
    
    # Summary
    print("\\n" + "=" * 50)
    if missing_files:
        print(f"❌ Setup incomplete. Missing: {', '.join(missing_files)}")
        return False, []
    else:
        print(f"✅ Setup complete! Ready to process {len(available_topics)} topics.")
        return True, available_topics

def suggest_commands(available_topics):
    """Suggest test commands."""
    if not available_topics:
        print("\\n❌ No topics available for processing")
        return
    
    print("\\n📝 Suggested test commands:")
    print("-" * 30)
    
    # Single topic test
    first_topic = available_topics[0]
    print(f"# Test single topic (Topic {first_topic}):")
    print(f"python improvement_pipeline.py --topics {first_topic}")
    print()
    
    # Multiple topics test
    if len(available_topics) >= 3:
        test_topics = available_topics[:3]
        print(f"# Test first 3 topics:")
        print(f"python improvement_pipeline.py --topics {' '.join(map(str, test_topics))}")
        print()
    
    # All topics
    print(f"# Process all available topics:")
    print(f"python improvement_pipeline.py --topics {' '.join(map(str, available_topics))}")
    print()
    
    # Full pipeline (all 1-7)
    print(f"# Full pipeline (all topics 1-7):")
    print(f"python improvement_pipeline.py")
    print()
    
    print("⚠️  Note: Each topic takes 5-10 minutes to process")
    print(f"   Estimated time for all {len(available_topics)} topics: {len(available_topics) * 7} minutes")

def main():
    """Run setup test."""
    try:
        setup_ok, available_topics = test_pipeline_setup()
        
        if setup_ok:
            suggest_commands(available_topics)
            print("\\n🚀 Ready to run the improvement pipeline!")
        else:
            print("\\n🛠️  Please fix the missing components first.")
            return False
            
        return True
        
    except Exception as e:
        print(f"\\n❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
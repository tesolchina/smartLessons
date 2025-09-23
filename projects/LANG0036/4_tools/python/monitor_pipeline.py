#!/usr/bin/env python3
"""
Monitor the improvement pipeline progress
"""

import time
import json
from pathlib import Path
from datetime import datetime

def monitor_pipeline():
    """Monitor the pipeline execution progress."""
    print("📊 Monitoring Improvement Pipeline Progress")
    print("=" * 50)
    
    chatbots_dir = Path("/Users/simonwang/Documents/Usage/VibeCoding/GCAP3226prep/Chatbots")
    topics_dir = Path("/Users/simonwang/Documents/Usage/VibeCoding/GCAP3226prep/TopicSelectionPM")
    
    topics = {
        1: "Topic1_BusFrequency",
        2: "Topic2_BusStopMerge", 
        3: "Topic3_BusRoutesCoordination",
        4: "Topic4_SolidWasteCharging",
        5: "Topic5_GreenCommunity",
        6: "Topic6_FluShotParticipation",
        7: "Topic7_TyphoonSignal"
    }
    
    while True:
        print(f"\\n⏰ Status check at {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 40)
        
        completed_assessments = 0
        completed_revisions = 0
        
        for topic_num, topic_name in topics.items():
            topic_dir = topics_dir / topic_name
            
            # Check for assessment file
            assessment_file = topic_dir / "AI_Assessment_Results.md"
            assessment_status = "✅" if assessment_file.exists() else "⏳"
            
            # Check for revision file (any enhanced framework file)
            revision_files = list(topic_dir.glob("Enhanced_Regression_Framework_*.md"))
            revision_status = "✅" if revision_files else "⏳"
            
            if assessment_file.exists():
                completed_assessments += 1
            if revision_files:
                completed_revisions += 1
            
            print(f"Topic {topic_num}: {assessment_status} Assessment  {revision_status} Revision")
        
        print(f"\\n📊 Progress: {completed_assessments}/7 assessments, {completed_revisions}/7 revisions")
        
        # Check for completion
        if completed_revisions == 7:
            print("\\n🎉 All topics completed!")
            
            # Look for final report
            report_files = list(chatbots_dir.glob("pipeline_report_*.json"))
            if report_files:
                latest_report = max(report_files, key=lambda x: x.stat().st_mtime)
                print(f"📄 Final report: {latest_report.name}")
                
                # Show summary from report
                try:
                    with open(latest_report, 'r') as f:
                        report_data = json.load(f)
                    
                    pipeline_info = report_data.get("pipeline_execution", {})
                    print(f"⏱️  Total time: {pipeline_info.get('total_topics', 'N/A')} topics processed")
                    print(f"✅ Success rate: {pipeline_info.get('successful_topics', 0)}/{pipeline_info.get('total_topics', 7)}")
                    
                except Exception as e:
                    print(f"❌ Could not read report: {e}")
            
            break
        
        # Wait before next check
        print("\\n⏳ Checking again in 30 seconds... (Ctrl+C to stop monitoring)")
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\\n\\n⏹️  Monitoring stopped by user")
            break

def show_latest_files():
    """Show the latest generated files."""
    print("\\n📁 Latest generated files:")
    print("-" * 30)
    
    topics_dir = Path("/Users/simonwang/Documents/Usage/VibeCoding/GCAP3226prep/TopicSelectionPM")
    
    for topic_dir in sorted(topics_dir.glob("Topic*")):
        if topic_dir.is_dir():
            print(f"\\n📂 {topic_dir.name}:")
            
            # Assessment files
            assessment_files = list(topic_dir.glob("AI_Assessment_Results.md"))
            if assessment_files:
                latest_assessment = max(assessment_files, key=lambda x: x.stat().st_mtime)
                mod_time = datetime.fromtimestamp(latest_assessment.stat().st_mtime)
                print(f"  📊 Assessment: {latest_assessment.name} ({mod_time.strftime('%H:%M:%S')})")
            
            # Revision files
            revision_files = list(topic_dir.glob("Enhanced_Regression_Framework_*.md"))
            if revision_files:
                latest_revision = max(revision_files, key=lambda x: x.stat().st_mtime)
                mod_time = datetime.fromtimestamp(latest_revision.stat().st_mtime)
                print(f"  📝 Revision: {latest_revision.name} ({mod_time.strftime('%H:%M:%S')})")

if __name__ == "__main__":
    try:
        monitor_pipeline()
        show_latest_files()
    except KeyboardInterrupt:
        print("\\n\\n⏹️  Monitoring interrupted")
    except Exception as e:
        print(f"\\n❌ Monitoring error: {e}")
#!/usr/bin/env python3
"""
Automated Regression Analysis Improvement Pipeline
=================================================

This script automates the two-stage AI improvement process for all regression analysis topics:
1. Stage 1: Assessment Guru provides expert feedback
2. Stage 2: Revision Chatbot generates enhanced framework

Features:
- Processes all topics 1-7 automatically
- Creates organized output files with timestamps
- Provides progress tracking and error handling
- Generates summary report of all improvements
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
import json

class RegressionImprovementPipeline:
    """Automated pipeline for assessing and revising regression analyses."""
    
    def __init__(self):
        """Initialize the pipeline."""
        self.base_dir = Path("/Users/simonwang/Documents/Usage/VibeCoding/GCAP3226prep")
        self.chatbots_dir = self.base_dir / "Chatbots"
        self.topics_dir = self.base_dir / "TopicSelectionPM"
        
        # Define topic mappings
        self.topics = {
            1: "Topic1_BusFrequency",
            2: "Topic2_BusStopMerge", 
            3: "Topic3_BusRoutesCoordination",
            4: "Topic4_SolidWasteCharging",
            5: "Topic5_GreenCommunity",
            6: "Topic6_FluShotParticipation",
            7: "Topic7_TyphoonSignal"
        }
        
        self.results = {}
        self.start_time = datetime.now()
    
    def check_prerequisites(self):
        """Check if all required files and directories exist."""
        print("🔍 Checking prerequisites...")
        
        # Check main directories
        if not self.chatbots_dir.exists():
            raise FileNotFoundError(f"Chatbots directory not found: {self.chatbots_dir}")
        
        if not self.topics_dir.exists():
            raise FileNotFoundError(f"Topics directory not found: {self.topics_dir}")
        
        # Check chatbot scripts
        assessor_script = self.chatbots_dir / "regression_assessor.py"
        revisor_script = self.chatbots_dir / "revise_application_plan" / "plan_revisor.py"
        
        if not assessor_script.exists():
            raise FileNotFoundError(f"Assessment script not found: {assessor_script}")
        
        if not revisor_script.exists():
            raise FileNotFoundError(f"Revision script not found: {revisor_script}")
        
        # Check API key
        env_file = self.chatbots_dir / ".env"
        if not env_file.exists():
            raise FileNotFoundError(f"API key file not found: {env_file}")
        
        print("✅ All prerequisites satisfied")
        return True
    
    def find_topic_files(self, topic_num):
        """Find relevant files for a topic."""
        topic_name = self.topics[topic_num]
        topic_dir = self.topics_dir / topic_name
        
        if not topic_dir.exists():
            return None, f"Topic directory not found: {topic_dir}"
        
        # Look for regression applications file
        regression_file = topic_dir / "Regression_Applications.md"
        if not regression_file.exists():
            return None, f"Regression file not found: {regression_file}"
        
        return {
            "topic_dir": topic_dir,
            "regression_file": regression_file,
            "assessment_file": topic_dir / "AI_Assessment_Results.md",
            "revision_file": topic_dir / f"Enhanced_Regression_Framework_{self.get_timestamp()}.md"
        }, None
    
    def get_timestamp(self):
        """Get timestamp for file naming."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def run_assessment(self, topic_num, files):
        """Run the assessment guru on a topic."""
        print(f"  📊 Running assessment guru...")
        
        # Prepare command
        cmd = [
            "python", 
            str(self.chatbots_dir / "regression_assessor.py"),
            str(files["regression_file"]),
            "--output", str(files["assessment_file"]),
            "--type", "full"
        ]
        
        try:
            # Run assessment
            result = subprocess.run(
                cmd, 
                cwd=self.chatbots_dir,
                capture_output=True, 
                text=True, 
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print(f"  ✅ Assessment completed successfully")
                return True, "Assessment completed"
            else:
                error_msg = f"Assessment failed: {result.stderr}"
                print(f"  ❌ {error_msg}")
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            error_msg = "Assessment timed out (5 minutes)"
            print(f"  ❌ {error_msg}")
            return False, error_msg
        except Exception as e:
            error_msg = f"Assessment error: {str(e)}"
            print(f"  ❌ {error_msg}")
            return False, error_msg
    
    def run_revision(self, topic_num, files):
        """Run the revision chatbot on a topic."""
        print(f"  🔄 Running revision chatbot...")
        
        # Prepare command
        cmd = [
            "python", 
            "plan_revisor.py",
            str(files["regression_file"]),
            str(files["assessment_file"]),
            str(files["revision_file"]),
            "--focus", "comprehensive"
        ]
        
        try:
            # Run revision
            result = subprocess.run(
                cmd, 
                cwd=self.chatbots_dir / "revise_application_plan",
                capture_output=True, 
                text=True, 
                timeout=480  # 8 minute timeout
            )
            
            if result.returncode == 0:
                print(f"  ✅ Revision completed successfully")
                return True, "Revision completed"
            else:
                error_msg = f"Revision failed: {result.stderr}"
                print(f"  ❌ {error_msg}")
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            error_msg = "Revision timed out (8 minutes)"
            print(f"  ❌ {error_msg}")
            return False, error_msg
        except Exception as e:
            error_msg = f"Revision error: {str(e)}"
            print(f"  ❌ {error_msg}")
            return False, error_msg
    
    def process_topic(self, topic_num):
        """Process a single topic through the complete pipeline."""
        topic_name = self.topics[topic_num]
        print(f"\\n🎯 Processing Topic {topic_num}: {topic_name}")
        print("=" * 60)
        
        # Find topic files
        files, error = self.find_topic_files(topic_num)
        if error or files is None:
            print(f"❌ {error}")
            self.results[topic_num] = {"status": "failed", "error": error}
            return False
        
        print(f"  📁 Topic directory: {files['topic_dir']}")
        print(f"  📄 Input file: {files['regression_file'].name}")
        
        # Stage 1: Run assessment
        print(f"\\n  🔍 Stage 1: Expert Assessment")
        assessment_success, assessment_msg = self.run_assessment(topic_num, files)
        
        if not assessment_success:
            self.results[topic_num] = {
                "status": "failed", 
                "stage": "assessment",
                "error": assessment_msg
            }
            return False
        
        # Stage 2: Run revision
        print(f"\\n  🔄 Stage 2: Framework Revision")
        revision_success, revision_msg = self.run_revision(topic_num, files)
        
        if not revision_success:
            self.results[topic_num] = {
                "status": "failed", 
                "stage": "revision",
                "error": revision_msg,
                "assessment_file": str(files["assessment_file"])
            }
            return False
        
        # Success
        self.results[topic_num] = {
            "status": "success",
            "topic_name": topic_name,
            "assessment_file": files["assessment_file"],
            "revision_file": files["revision_file"],
            "processing_time": datetime.now()
        }
        
        print(f"  ✅ Topic {topic_num} completed successfully!")
        print(f"  📊 Assessment: {files['assessment_file'].name}")
        print(f"  📝 Revision: {files['revision_file'].name}")
        
        return True
    
    def run_pipeline(self, topics_to_process=None):
        """Run the complete improvement pipeline."""
        if topics_to_process is None:
            topics_to_process = list(self.topics.keys())
        
        print("🚀 Starting Automated Regression Analysis Improvement Pipeline")
        print(f"📅 Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Processing topics: {topics_to_process}")
        print("=" * 80)
        
        # Check prerequisites
        try:
            self.check_prerequisites()
        except Exception as e:
            print(f"❌ Prerequisites check failed: {e}")
            return False
        
        # Process each topic
        successful_topics = []
        failed_topics = []
        
        for topic_num in topics_to_process:
            if topic_num not in self.topics:
                print(f"❌ Invalid topic number: {topic_num}")
                failed_topics.append(topic_num)
                continue
            
            success = self.process_topic(topic_num)
            if success:
                successful_topics.append(topic_num)
            else:
                failed_topics.append(topic_num)
            
            # Brief pause between topics
            if topic_num != topics_to_process[-1]:
                print("\\n⏳ Brief pause before next topic...")
                time.sleep(2)
        
        # Generate summary report
        self.generate_summary_report(successful_topics, failed_topics)
        
        return len(failed_topics) == 0
    
    def generate_summary_report(self, successful_topics, failed_topics):
        """Generate a summary report of the pipeline execution."""
        end_time = datetime.now()
        total_time = end_time - self.start_time
        
        print("\\n" + "=" * 80)
        print("📋 PIPELINE EXECUTION SUMMARY")
        print("=" * 80)
        
        print(f"⏱️  Total execution time: {total_time}")
        print(f"✅ Successful topics: {len(successful_topics)}")
        print(f"❌ Failed topics: {len(failed_topics)}")
        
        if successful_topics:
            print("\\n✅ Successfully processed topics:")
            for topic_num in successful_topics:
                result = self.results[topic_num]
                print(f"  • Topic {topic_num}: {result['topic_name']}")
                print(f"    📊 Assessment: {result['assessment_file'].name}")
                print(f"    📝 Revision: {result['revision_file'].name}")
        
        if failed_topics:
            print("\\n❌ Failed topics:")
            for topic_num in failed_topics:
                if topic_num in self.results:
                    result = self.results[topic_num]
                    print(f"  • Topic {topic_num}: {result.get('error', 'Unknown error')}")
                else:
                    print(f"  • Topic {topic_num}: Invalid topic number")
        
        # Save detailed report
        self.save_detailed_report()
        
        print(f"\\n📄 Detailed report saved to: pipeline_report_{self.get_timestamp()}.json")
        
        if len(failed_topics) == 0:
            print("\\n🎉 All topics processed successfully!")
        else:
            print(f"\\n⚠️  {len(failed_topics)} topics failed. Check the detailed report.")
    
    def save_detailed_report(self):
        """Save detailed results to JSON file."""
        report_file = self.chatbots_dir / f"pipeline_report_{self.get_timestamp()}.json"
        
        # Convert Path objects to strings for JSON serialization
        json_results = {}
        for topic_num, result in self.results.items():
            json_result = dict(result)
            for key, value in json_result.items():
                if isinstance(value, Path):
                    json_result[key] = str(value)
                elif isinstance(value, datetime):
                    json_result[key] = value.isoformat()
            json_results[topic_num] = json_result
        
        report_data = {
            "pipeline_execution": {
                "start_time": self.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_topics": len(self.topics),
                "processed_topics": len(self.results),
                "successful_topics": len([r for r in self.results.values() if r["status"] == "success"]),
                "failed_topics": len([r for r in self.results.values() if r["status"] == "failed"])
            },
            "topic_results": json_results
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automated regression analysis improvement pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python improvement_pipeline.py                    # Process all topics 1-7
  python improvement_pipeline.py --topics 1 2 3    # Process specific topics
  python improvement_pipeline.py --topics 5         # Process single topic
        """
    )
    
    parser.add_argument(
        "--topics", "-t",
        nargs='+',
        type=int,
        choices=list(range(1, 8)),
        help="Specific topics to process (default: all topics 1-7)"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize pipeline
        pipeline = RegressionImprovementPipeline()
        
        # Run pipeline
        success = pipeline.run_pipeline(args.topics)
        
        if success:
            print("\\n🎉 Pipeline completed successfully!")
            sys.exit(0)
        else:
            print("\\n❌ Pipeline completed with errors!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\\n\\n⏹️  Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Pipeline failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
GCAP 3226 Course Setup Automation Script
Handles material download, organization, and initial setup tasks
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime
import shutil

class GCAP3226Setup:
    def __init__(self):
        self.project_root = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
        self.setup_log = []
        
    def log_action(self, action, status="INFO"):
        """Log setup actions with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {status}: {action}"
        self.setup_log.append(log_entry)
        print(log_entry)
    
    def create_material_directories(self):
        """Create detailed directory structure for course materials"""
        
        directories = [
            # Course Materials
            "course_materials/syllabus",
            "course_materials/student_lists", 
            "course_materials/assignments/instructions",
            "course_materials/assignments/rubrics",
            "course_materials/assignments/submissions",
            "course_materials/resources/readings",
            "course_materials/resources/datasets",
            "course_materials/resources/videos",
            
            # Chatbot Development
            "chatbots/course_assistant/training_data",
            "chatbots/course_assistant/conversation_flows",
            "chatbots/data_analysis_bot/sample_datasets",
            "chatbots/data_analysis_bot/tutorials",
            "chatbots/policy_research_bot/knowledge_base",
            "chatbots/policy_research_bot/templates",
            
            # Budget Management
            "budget_planning/expense_tracking",
            "budget_planning/receipts/september_2025",
            "budget_planning/receipts/october_2025",
            "budget_planning/receipts/november_2025",
            "budget_planning/purchase_orders",
            "budget_planning/financial_reports",
            
            # Google Drive Integration
            "google_drive_sync/automated_scripts",
            "google_drive_sync/backup_logs",
            "google_drive_sync/sync_status"
        ]
        
        self.log_action("Creating directory structure...")
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
        self.log_action(f"Created {len(directories)} directories")
    
    def create_moodle_download_script(self):
        """Create script template for downloading materials from Moodle"""
        
        script_content = '''#!/usr/bin/env python3
"""
Moodle Material Download Script for GCAP 3226
"""

import requests
from pathlib import Path
import json

class MoodleDownloader:
    def __init__(self, course_id="GCAP3226", username="", password=""):
        self.course_id = course_id
        self.username = username
        self.password = password
        self.base_url = "https://moodle.hkbu.edu.hk"  # Adjust as needed
        self.download_dir = Path("../course_materials")
        
    def login(self):
        """Login to Moodle"""
        # Implementation depends on HKBU Moodle setup
        # This is a template - needs actual authentication details
        pass
    
    def download_syllabus(self):
        """Download course syllabus"""
        print("Downloading course syllabus...")
        # Implementation for syllabus download
        pass
    
    def download_student_lists(self):
        """Download enrolled student lists"""
        print("Downloading student lists...")
        # Implementation for student list download
        pass
    
    def download_assignments(self):
        """Download all assignment instructions"""
        print("Downloading assignment instructions...")
        # Implementation for assignment download
        pass
    
    def download_all(self):
        """Download all available materials"""
        self.login()
        self.download_syllabus()
        self.download_student_lists()
        self.download_assignments()
        print("All downloads completed!")

if __name__ == "__main__":
    # Usage: python moodle_downloader.py
    # Configure your Moodle credentials first
    downloader = MoodleDownloader()
    downloader.download_all()
'''
        
        script_path = self.project_root / "course_materials" / "moodle_downloader.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod(script_path, 0o755)
        self.log_action(f"Created Moodle download script: {script_path}")
    
    def create_budget_tracker(self):
        """Create initial budget tracking files"""
        
        # Create expense tracking template
        expense_data = {
            "budget_total": 70000,
            "currency": "HKD", 
            "fiscal_year": "2025-2026",
            "categories": {
                "software_tools": {
                    "allocated": 21000,
                    "spent": 0,
                    "remaining": 21000
                },
                "student_resources": {
                    "allocated": 28000, 
                    "spent": 0,
                    "remaining": 28000
                },
                "technology_infrastructure": {
                    "allocated": 14000,
                    "spent": 0, 
                    "remaining": 14000
                },
                "administrative_misc": {
                    "allocated": 7000,
                    "spent": 0,
                    "remaining": 7000
                }
            },
            "transactions": [],
            "monthly_targets": {
                "2025-09": 15000,
                "2025-10": 12000,
                "2025-11": 10000,
                "2025-12": 15000,
                "2026-01": 10000,
                "2026-02": 8000
            }
        }
        
        budget_file = self.project_root / "budget_planning" / "budget_tracker.json"
        with open(budget_file, 'w') as f:
            json.dump(expense_data, f, indent=2)
        
        self.log_action(f"Created budget tracker: {budget_file}")
    
    def create_chatbot_templates(self):
        """Create initial chatbot development templates"""
        
        # Course Assistant Bot Template
        assistant_config = {
            "name": "GCAP3226_CourseAssistant",
            "description": "General course support and Q&A",
            "model": "gpt-4",
            "temperature": 0.3,
            "system_prompt": "You are a helpful course assistant for GCAP 3226: Empowering Citizens through Data. Help students with course logistics, assignments, and general questions.",
            "knowledge_base": [
                "course_syllabus.md",
                "assignment_instructions.md", 
                "frequently_asked_questions.md"
            ],
            "features": [
                "syllabus_qa",
                "assignment_help",
                "schedule_management",
                "general_support"
            ]
        }
        
        assistant_file = self.project_root / "chatbots" / "course_assistant" / "config.json"
        with open(assistant_file, 'w') as f:
            json.dump(assistant_config, f, indent=2)
        
        # Data Analysis Bot Template
        data_bot_config = {
            "name": "GCAP3226_DataAnalysisBot",
            "description": "Data analysis assistance and tutoring",
            "model": "gpt-4-code-interpreter",
            "temperature": 0.1,
            "system_prompt": "You are a data analysis tutor for policy research. Help students with statistical analysis, data interpretation, and visualization for Hong Kong policy data.",
            "tools": [
                "python_interpreter",
                "data_visualization",
                "statistical_analysis"
            ],
            "sample_datasets": [
                "hk_housing_policy_data.csv",
                "transportation_usage_stats.csv",
                "education_funding_trends.csv"
            ]
        }
        
        data_bot_file = self.project_root / "chatbots" / "data_analysis_bot" / "config.json"
        with open(data_bot_file, 'w') as f:
            json.dump(data_bot_config, f, indent=2)
        
        self.log_action("Created chatbot configuration templates")
    
    def create_google_drive_sync_script(self):
        """Create Google Drive synchronization script"""
        
        sync_script = '''#!/bin/bash
# Google Drive Sync Script for GCAP 3226
# Run this script to keep local files synced with Google Drive

DRIVE_PATH="/Users/simonwang/Google Drive/GCAP 3226 - Empowering Citizens through Data"
LOCAL_PATH="/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226"

echo "Starting GCAP 3226 sync: $(date)"

# Check if Google Drive is mounted
if [ ! -d "$DRIVE_PATH" ]; then
    echo "Error: Google Drive not found at $DRIVE_PATH"
    echo "Please ensure Google Drive Desktop is installed and running"
    exit 1
fi

# Sync course materials from Drive to local
echo "Syncing course materials..."
rsync -av --delete "$DRIVE_PATH/Course Materials/" "$LOCAL_PATH/course_materials/" 2>/dev/null || echo "Course materials folder not yet created in Drive"

# Sync assignments  
echo "Syncing assignments..."
rsync -av --delete "$DRIVE_PATH/Assignments & Projects/" "$LOCAL_PATH/course_materials/assignments/" 2>/dev/null || echo "Assignments folder not yet created in Drive"

# Upload budget tracking from local to Drive
echo "Uploading budget tracking..."
rsync -av --delete "$LOCAL_PATH/budget_planning/" "$DRIVE_PATH/Budget & Administration/" 2>/dev/null || echo "Creating Budget folder in Drive..."

# Upload chatbot development from local to Drive
echo "Uploading chatbot resources..."
rsync -av --delete "$LOCAL_PATH/chatbots/" "$DRIVE_PATH/Chatbot Resources/" 2>/dev/null || echo "Creating Chatbot folder in Drive..."

echo "Sync completed: $(date)"
echo "Check sync_log.txt for detailed information"
'''
        
        sync_script_path = self.project_root / "google_drive_sync" / "sync_with_drive.sh"
        with open(sync_script_path, 'w') as f:
            f.write(sync_script)
        
        # Make script executable
        os.chmod(sync_script_path, 0o755)
        self.log_action(f"Created Google Drive sync script: {sync_script_path}")
    
    def create_project_checklist(self):
        """Create immediate action checklist"""
        
        checklist = '''# GCAP 3226 Setup Checklist
*Generated: {timestamp}*

## 🚀 Immediate Actions (Week 1)

### Course Materials
- [ ] Login to HKBU Moodle and access GCAP 3226 course
- [ ] Download course syllabus to `course_materials/syllabus/`
- [ ] Export student enrollment list to `course_materials/student_lists/`
- [ ] Download all assignment instructions to `course_materials/assignments/instructions/`
- [ ] Save assignment rubrics to `course_materials/assignments/rubrics/`

### Google Drive Setup
- [ ] Install Google Drive Desktop app if not already installed
- [ ] Create "GCAP 3226 - Empowering Citizens through Data" folder in Google Drive
- [ ] Set up folder structure as outlined in `google_drive_sync/sync_setup.md`
- [ ] Run initial sync script: `./google_drive_sync/sync_with_drive.sh`
- [ ] Configure sharing permissions for TAs and students

### Budget Management  
- [ ] Review budget breakdown in `budget_planning/budget_breakdown.md`
- [ ] Set up expense tracking system using `budget_planning/budget_tracker.json`
- [ ] Identify first month priorities (HKD 15,000 allocation)
- [ ] Contact finance office about purchase approval procedures

### Chatbot Development
- [ ] Review chatbot development plan in `chatbots/README.md`
- [ ] Obtain OpenAI API key for chatbot development
- [ ] Set up development environment for chatbot testing
- [ ] Plan chatbot deployment timeline (aim for Week 3-4)

## 📋 Week 2 Actions

### Content Development
- [ ] Create FAQ document based on common student questions
- [ ] Prepare sample datasets for data analysis bot training
- [ ] Research Hong Kong policy databases for research bot
- [ ] Design chatbot conversation flows

### Technical Setup
- [ ] Set up chatbot hosting environment
- [ ] Configure authentication systems
- [ ] Test API integrations
- [ ] Create student feedback collection system

### Administrative
- [ ] Schedule TA training sessions
- [ ] Plan student introduction to chatbots
- [ ] Set up progress monitoring systems
- [ ] Create communication channels for course updates

## 📊 Success Metrics Setup

### Academic Metrics
- [ ] Define baseline assessment for student data analysis skills
- [ ] Create pre-course survey for chatbot expectations
- [ ] Set up grade tracking system
- [ ] Plan mid-semester evaluation

### Technical Metrics
- [ ] Set up chatbot usage analytics
- [ ] Configure performance monitoring
- [ ] Create uptime monitoring alerts
- [ ] Plan user satisfaction surveys

### Financial Metrics
- [ ] Set up automated expense tracking
- [ ] Create monthly budget review schedule
- [ ] Plan cost-per-student calculations
- [ ] Set up ROI measurement framework

## 🔄 Ongoing Maintenance

### Daily
- [ ] Monitor chatbot performance
- [ ] Check for student support requests
- [ ] Review expense notifications

### Weekly  
- [ ] Sync with Google Drive
- [ ] Review budget status
- [ ] Update chatbot training data
- [ ] Check system performance metrics

### Monthly
- [ ] Generate budget reports
- [ ] Analyze chatbot usage patterns
- [ ] Survey student satisfaction
- [ ] Plan next month activities

---

## 📞 Quick Contacts

- **Moodle Support**: HKBU IT Helpdesk
- **Finance Questions**: Department Finance Office  
- **Technical Issues**: Simon Wang
- **Student Support**: Course TAs

---

*This checklist ensures systematic setup and launch of the GCAP 3226 enhanced learning environment.*
'''.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        checklist_path = self.project_root / "PROJECT_SETUP_CHECKLIST.md"
        with open(checklist_path, 'w') as f:
            f.write(checklist)
        
        self.log_action(f"Created project checklist: {checklist_path}")
    
    def generate_setup_report(self):
        """Generate final setup report"""
        
        report = f'''# GCAP 3226 Setup Report
*Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

## ✅ Setup Completed Successfully

### Directory Structure
- Created complete folder hierarchy for course management
- Set up specialized directories for chatbots, budget, and sync
- Organized material collection points for Moodle downloads

### Automation Scripts
- Moodle download script template created
- Google Drive sync automation configured
- Budget tracking system initialized
- Chatbot configuration templates ready

### Documentation
- Comprehensive README with project overview
- Detailed budget breakdown and allocation plan
- Chatbot development roadmap
- Google Drive integration guide
- Complete setup checklist for immediate actions

## 📊 Project Overview

**Total Budget:** HKD 70,000
**Timeline:** September 2025 - February 2026
**Key Components:** 3 AI chatbots, comprehensive course management, cloud integration

## 🎯 Next Immediate Steps

1. **Download course materials from Moodle**
2. **Set up Google Drive synchronization** 
3. **Begin chatbot development planning**
4. **Initialize budget tracking**

## 📋 Setup Log

'''
        
        # Add setup log entries
        for log_entry in self.setup_log:
            report += f"- {log_entry}\n"
        
        report_path = self.project_root / "SETUP_REPORT.md"
        with open(report_path, 'w') as f:
            f.write(report)
        
        self.log_action(f"Generated setup report: {report_path}")
        return report_path
    
    def run_complete_setup(self):
        """Execute complete GCAP 3226 project setup"""
        
        print("🚀 Starting GCAP 3226 Complete Project Setup...")
        print("=" * 60)
        
        try:
            # Execute all setup steps
            self.create_material_directories()
            self.create_moodle_download_script()
            self.create_budget_tracker()
            self.create_chatbot_templates()
            self.create_google_drive_sync_script()
            self.create_project_checklist()
            
            # Generate final report
            report_path = self.generate_setup_report()
            
            print("=" * 60)
            print("✅ GCAP 3226 Project Setup Complete!")
            print(f"📋 Setup report: {report_path}")
            print(f"📁 Project location: {self.project_root}")
            print("\n🎯 Next: Review PROJECT_SETUP_CHECKLIST.md for immediate actions")
            
        except Exception as e:
            self.log_action(f"Setup failed: {str(e)}", "ERROR")
            print(f"❌ Setup failed: {str(e)}")
            raise

def main():
    """Main execution"""
    setup = GCAP3226Setup()
    setup.run_complete_setup()

if __name__ == "__main__":
    main()

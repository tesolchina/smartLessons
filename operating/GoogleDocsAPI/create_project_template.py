"""
GCAP 3226 Project Template Creator
Creates a comprehensive project template in Google Drive based on syllabus
"""

import json
from pathlib import Path
from typing import Dict

class GCAP3226TemplateCreator:
    """Creates project templates based on syllabus requirements"""
    
    def __init__(self):
        self.drive_service = None
        self.docs_service = None
        self.parent_folder_id = "1S4JMQSkIWAPhwKqUkKxfC6qqWewD6z8v"  # Your GCAP folder
        self.setup_services()
    
    def setup_services(self):
        """Initialize Google API services"""
        try:
            from googleapiclient.discovery import build
            from auth_setup import authenticate_google_apis
            
            creds = authenticate_google_apis()
            if not creds:
                raise Exception("Authentication failed")
            
            self.drive_service = build('drive', 'v3', credentials=creds)
            self.docs_service = build('docs', 'v1', credentials=creds)
            print("✅ Google API services ready for template creation")
            
        except ImportError:
            print("⚠️  Google API libraries not installed. Using offline mode.")
            self.drive_service = None
            self.docs_service = None
    
    def create_project_template(self) -> str:
        """Create comprehensive project template document"""
        if not self.docs_service or not self.drive_service:
            print("📄 [OFFLINE] Would create project template document")
            return "offline_template_doc"
        
        try:
            # Create the template document
            doc_title = "GCAP3226_Project_Template"
            document = {'title': doc_title}
            
            doc = self.docs_service.documents().create(body=document).execute()
            doc_id = doc.get('documentId')
            
            # Move to GCAP folder
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=self.parent_folder_id,
                removeParents='',
                fields='id, parents'
            ).execute()
            
            # Add comprehensive content
            self.add_template_content(doc_id)
            
            print(f"✅ Created project template: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"❌ Failed to create template: {e}")
            return None
    
    def add_template_content(self, doc_id: str):
        """Add comprehensive project template content"""
        if not self.docs_service:
            return
        
        template_content = """GCAP 3226: Empowering Citizens through Data
Participatory Policy Analysis for Hong Kong
PROJECT TEMPLATE & TEAM WORKSPACE

═══════════════════════════════════════════════════════════════

📋 TEAM INFORMATION

Team Number: _________________ (Team01, Team02, etc.)
Project Title: _________________ (To be decided)

Team Members (4-5 students maximum):
1. Team Leader: _________________ 
   Email: _________________ 
   Student ID: _________________
   Phone: _________________

2. Data Analyst: _________________ 
   Email: _________________ 
   Student ID: _________________
   Phone: _________________

3. Policy Researcher: _________________ 
   Email: _________________ 
   Student ID: _________________
   Phone: _________________

4. Report Writer: _________________ 
   Email: _________________ 
   Student ID: _________________
   Phone: _________________

5. Presenter: _________________ 
   Email: _________________ 
   Student ID: _________________
   Phone: _________________

Team Communication:
□ WhatsApp Group Created: _________________
□ Google Drive Folder Access Confirmed
□ Meeting Schedule Agreed: _________________

═══════════════════════════════════════════════════════════════

🎯 PROJECT OVERVIEW

Project Focus Area (Choose One):
□ Public Housing Policy Analysis
□ Transportation & Infrastructure Policy
□ Education Resource Allocation
□ Healthcare Access & Delivery
□ Environmental Policy Implementation
□ Social Services & Welfare Policy
□ Digital Government Services
□ Youth Employment Programs
□ Elderly Care Policy
□ Community Development Policy

Research Question (Primary):
_________________________________________________________________
_________________________________________________________________

Research Sub-Questions:
1. _________________________________________________________________
2. _________________________________________________________________
3. _________________________________________________________________

Policy Relevance Statement:
_________________________________________________________________
_________________________________________________________________

═══════════════════════════════════════════════════════════════

📅 PROJECT MILESTONES & TIMELINE

PHASE 1: PROJECT PROPOSAL (Weeks 1-3)
□ Week 1: Team Formation & Topic Selection
   Deadline: _________________ 
   Status: ⏳ Pending / ✅ Complete

□ Week 2: Research Question Development
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

□ Week 3: Project Proposal Submission
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

PHASE 2: DATA COLLECTION (Weeks 4-6)
□ Week 4: Data Source Identification
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

□ Week 5: Data Access & Collection
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

□ Week 6: Data Cleaning & Preparation
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

PHASE 3: DATA ANALYSIS (Weeks 7-9)
□ Week 7: Statistical Analysis
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

□ Week 8: Data Visualization
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

□ Week 9: Pattern Identification & Interpretation
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

PHASE 4: REPORT WRITING (Weeks 10-12)
□ Week 10: Draft Report Writing
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

□ Week 11: Peer Review & Revision
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

□ Week 12: Final Report Submission
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

PHASE 5: PRESENTATION (Weeks 13-14)
□ Week 13: Presentation Preparation
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

□ Week 14: Final Presentations
   Deadline: _________________
   Status: ⏳ Pending / ✅ Complete

═══════════════════════════════════════════════════════════════

📊 DATA SOURCES & METHODOLOGY

Primary Data Sources:
□ Census and Statistics Department (Hong Kong)
   Link: _________________
   Access Status: ⏳ Pending / ✅ Obtained

□ Transport Department
   Link: _________________
   Access Status: ⏳ Pending / ✅ Obtained

□ Housing Authority
   Link: _________________
   Access Status: ⏳ Pending / ✅ Obtained

□ Education Bureau
   Link: _________________
   Access Status: ⏳ Pending / ✅ Obtained

□ Department of Health
   Link: _________________
   Access Status: ⏳ Pending / ✅ Obtained

□ Environmental Protection Department
   Link: _________________
   Access Status: ⏳ Pending / ✅ Obtained

Secondary Data Sources:
□ Academic Research Papers
□ Policy Reports & White Papers
□ International Comparison Studies
□ NGO Reports & Surveys

Research Methodology:
□ Quantitative Analysis (Statistical Methods)
□ Qualitative Analysis (Interviews, Surveys)
□ Comparative Analysis (Cross-district, International)
□ Time Series Analysis (Trend Analysis)
□ Geographic Information System (GIS) Analysis

Analysis Tools:
□ Excel (Basic Analysis)
□ SPSS (Statistical Analysis)
□ R Programming (Advanced Statistics)
□ Python (Data Science)
□ Tableau/PowerBI (Visualization)

═══════════════════════════════════════════════════════════════

📝 MEETING LOGS & PROGRESS TRACKING

MEETING 1
Date: _________________
Attendees: _________________
Duration: _________________

Agenda:
1. _________________________________________________________________
2. _________________________________________________________________
3. _________________________________________________________________

Key Decisions:
- _________________________________________________________________
- _________________________________________________________________
- _________________________________________________________________

Action Items:
□ Task: _________________ | Assigned to: _______ | Due: _______
□ Task: _________________ | Assigned to: _______ | Due: _______
□ Task: _________________ | Assigned to: _______ | Due: _______

Next Meeting: _________________

MEETING 2
Date: _________________
Attendees: _________________
Duration: _________________

Agenda:
1. _________________________________________________________________
2. _________________________________________________________________
3. _________________________________________________________________

Key Decisions:
- _________________________________________________________________
- _________________________________________________________________
- _________________________________________________________________

Action Items:
□ Task: _________________ | Assigned to: _______ | Due: _______
□ Task: _________________ | Assigned to: _______ | Due: _______
□ Task: _________________ | Assigned to: _______ | Due: _______

Next Meeting: _________________

[Add more meeting logs as needed]

═══════════════════════════════════════════════════════════════

📈 PROGRESS TRACKING

Overall Project Progress: ____% Complete

Phase Completion Status:
□ Project Proposal: ____% Complete
□ Data Collection: ____% Complete
□ Data Analysis: ____% Complete
□ Report Writing: ____% Complete
□ Presentation: ____% Complete

Individual Contributions:
1. _________________ Contribution: _________________ (____%)
2. _________________ Contribution: _________________ (____%)
3. _________________ Contribution: _________________ (____%)
4. _________________ Contribution: _________________ (____%)
5. _________________ Contribution: _________________ (____%)

Challenges Encountered:
1. _________________________________________________________________
   Solution: _________________________________________________________________

2. _________________________________________________________________
   Solution: _________________________________________________________________

3. _________________________________________________________________
   Solution: _________________________________________________________________

═══════════════════════════════════════════════════════════════

📚 DELIVERABLES CHECKLIST

PROJECT PROPOSAL (Week 3)
□ Research questions clearly defined
□ Literature review completed
□ Methodology outlined
□ Timeline established
□ Data sources identified
□ Submitted to Moodle
□ Feedback received and addressed

DATA COLLECTION REPORT (Week 6)
□ All data sources accessed
□ Data collected and documented
□ Data cleaning completed
□ Data quality assessment done
□ Submitted to Moodle
□ Feedback received and addressed

ANALYSIS REPORT (Week 9)
□ Statistical analysis completed
□ Visualizations created
□ Patterns identified
□ Preliminary findings documented
□ Submitted to Moodle
□ Feedback received and addressed

FINAL REPORT (Week 12)
□ Executive summary (2 pages)
□ Introduction and background
□ Literature review
□ Methodology section
□ Data analysis and findings
□ Policy recommendations
□ Conclusion and limitations
□ References (APA format)
□ Appendices (data, code, etc.)
□ Professional formatting
□ Submitted to Moodle
□ Peer review completed

FINAL PRESENTATION (Week 14)
□ Presentation slides prepared
□ Key findings highlighted
□ Policy recommendations clear
□ Q&A preparation completed
□ Presentation rehearsed
□ Individual speaking parts assigned
□ Presentation delivered
□ Peer evaluations completed

═══════════════════════════════════════════════════════════════

💡 PROJECT NOTES & BRAINSTORMING

Research Ideas:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Data Insights:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Policy Implications:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Discussion Points:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Resources & References:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

═══════════════════════════════════════════════════════════════

📞 CONTACT INFORMATION

Course Instructor: _________________
Email: _________________
Office Hours: _________________

Teaching Assistant: _________________
Email: _________________
Office Hours: _________________

Course Moodle: https://buelearning.hkbu.edu.hk/course/view.php?id=118357
Google Drive Folder: https://drive.google.com/drive/u/0/folders/1S4JMQSkIWAPhwKqUkKxfC6qqWewD6z8v

Emergency Contact (Team Leader): _________________

═══════════════════════════════════════════════════════════════

📋 ASSESSMENT CRITERIA

Project Proposal (10% of final grade)
□ Research question clarity and relevance
□ Literature review quality
□ Methodology appropriateness
□ Timeline feasibility

Data Collection & Analysis (35% of final grade)
□ Data source quality and relevance
□ Analysis method appropriateness
□ Technical execution quality
□ Insight generation capability

Final Report (35% of final grade)
□ Academic writing quality
□ Argument structure and logic
□ Evidence integration
□ Policy recommendation quality
□ Professional presentation

Team Presentation (15% of final grade)
□ Content clarity and organization
□ Visual presentation quality
□ Team coordination
□ Q&A handling

Peer Evaluation (5% of final grade)
□ Individual contribution assessment
□ Team collaboration quality
□ Professional behavior

═══════════════════════════════════════════════════════════════

TEMPLATE USAGE INSTRUCTIONS:

1. Copy this template to each team's folder
2. Rename with team number (e.g., "Team01_Project_Workspace")
3. Fill in team information immediately
4. Update milestones as project progresses
5. Use meeting logs for every team meeting
6. Track progress regularly
7. Check off deliverables as completed

This template serves as your central project management document.
Keep it updated and refer to it regularly for project success!

Last Updated: September 6, 2025
Template Version: 1.0"""

        try:
            requests = [{
                'insertText': {
                    'location': {'index': 1},
                    'text': template_content
                }
            }]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print("✅ Added comprehensive project template content")
            
        except Exception as e:
            print(f"❌ Failed to add template content: {e}")
    
    def create_and_distribute_template(self):
        """Create template and prepare for distribution to teams"""
        print("🚀 Creating GCAP 3226 Project Template...")
        print("=" * 50)
        
        # Create the main template
        template_doc_id = self.create_project_template()
        
        if template_doc_id:
            template_link = f"https://docs.google.com/document/d/{template_doc_id}/edit"
            
            print("\n" + "=" * 50)
            print("🎉 PROJECT TEMPLATE CREATED!")
            print("=" * 50)
            print(f"📄 Template Document: {template_link}")
            print(f"📁 Location: GCAP 3226 Google Drive folder")
            print()
            print("📋 NEXT STEPS:")
            print("1. Review the template content")
            print("2. Copy template to each team folder when teams are formed")
            print("3. Customize for each team's specific project")
            print("4. Share with teams for project management")
            
            return template_doc_id
        
        return None

def main():
    """Create the project template"""
    print("GCAP 3226 Project Template Creator")
    print("=" * 35)
    
    creator = GCAP3226TemplateCreator()
    template_doc_id = creator.create_and_distribute_template()
    
    if template_doc_id:
        print(f"\n✅ Template ready for use!")
        print(f"📋 Based on syllabus requirements and team structure")
        print(f"🎯 Includes all milestones and deliverables")

if __name__ == "__main__":
    main()

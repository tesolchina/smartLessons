#!/usr/bin/env python3
"""
GCAP3056 Tab Content Organizer
Retrieves current document content and reorganizes it into proper tab structure
with designated areas for students, teacher messages, teacher comments, and AI feedback
"""

import sys
import os
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

from auth_setup import authenticate_google_apis
from googleapiclient.errors import HttpError

class GCAP3056TabOrganizer:
    def __init__(self):
        self.drive_service = None
        self.docs_service = None
        self.document_id = "1polOm2WKjwlAGe_YGsffkIJ2a1mGXDMm0IFoKb7ZNoA"
        
    def setup_services(self):
        """Initialize Google API services"""
        print("🔐 Setting up Google API authentication...")
        try:
            from googleapiclient.discovery import build
            
            creds = authenticate_google_apis()
            if not creds:
                print("❌ Failed to get credentials")
                return False
                
            self.drive_service = build('drive', 'v3', credentials=creds)
            self.docs_service = build('docs', 'v1', credentials=creds)
            print("✅ Authentication successful!")
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def get_document_structure(self):
        """Retrieve current document with tabs to understand structure"""
        print("📄 Retrieving document structure...")
        try:
            doc = self.docs_service.documents().get(
                documentId=self.document_id,
                includeTabsContent=True
            ).execute()
            
            print(f"✅ Document retrieved: {doc.get('title', 'Untitled')}")
            
            # Analyze tab structure
            tabs = doc.get('tabs', [])
            print(f"📋 Found {len(tabs)} tabs:")
            
            tab_structure = []
            for i, tab in enumerate(tabs):
                tab_props = tab.get('tabProperties', {})
                tab_title = tab_props.get('title', f'Tab {i+1}')
                tab_id = tab_props.get('tabId')
                
                print(f"  {i+1}. {tab_title} (ID: {tab_id})")
                
                tab_info = {
                    'index': i,
                    'title': tab_title,
                    'id': tab_id,
                    'child_tabs': []
                }
                
                # Check for child tabs
                child_tabs = tab.get('childTabs', [])
                for j, child_tab in enumerate(child_tabs):
                    child_props = child_tab.get('tabProperties', {})
                    child_title = child_props.get('title', f'Child {j+1}')
                    child_id = child_props.get('tabId')
                    
                    print(f"    └── {child_title} (ID: {child_id})")
                    
                    tab_info['child_tabs'].append({
                        'index': j,
                        'title': child_title,
                        'id': child_id
                    })
                
                tab_structure.append(tab_info)
            
            return tab_structure, doc
            
        except Exception as e:
            print(f"❌ Error retrieving document: {e}")
            return None, None
    
    def create_tab_content_template(self, tab_title, content_type="main"):
        """Create standardized content template for each tab"""
        
        template = f"""
{'='*80}
{tab_title.upper()}
{'='*80}

📝 STUDENT WORK AREA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[This section is for students to complete their work]

{self._get_content_by_type(content_type)}

Current Status: □ Not Started □ In Progress □ Under Review □ Complete
Last Updated: [Date]
Updated By: [Student Name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 STUDENT-TEACHER COMMUNICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📤 STUDENT MESSAGES TO TEACHER:
[Students: Use this area to ask questions, request feedback, or update teacher on progress]

• [Date] - [Student Name]: 
• [Date] - [Student Name]: 
• [Date] - [Student Name]: 

📥 TEACHER RESPONSES & GUIDANCE:
[Teacher: Provide feedback, answer questions, and give guidance here]

• [Date] - Instructor: 
• [Date] - Instructor: 
• [Date] - Instructor: 

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 AI ASSISTANT FEEDBACK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 AI ANALYSIS & SUGGESTIONS:
[AI: Automated feedback, suggestions, and analysis will appear here]

• Content Quality Assessment: [To be analyzed]
• Research Gap Identification: [To be analyzed]  
• Writing Improvement Suggestions: [To be analyzed]
• Citation and Reference Check: [To be analyzed]

📊 PROGRESS TRACKING:
• Completion Level: [To be calculated]
• Quality Score: [To be assessed]
• Areas for Improvement: [To be identified]
• Next Steps Recommended: [To be suggested]

🎯 SMART RECOMMENDATIONS:
[AI will provide context-aware suggestions based on current content and course requirements]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        return template
    
    def _get_content_by_type(self, content_type):
        """Get specific content templates based on tab type"""
        
        templates = {
            "membership": """
**👥 TEAM MEMBER INFORMATION:**

**Member 1:**
• Full Name: _______________________________
• Student ID: _______________________________  
• Email Address: ___________________________
• Phone Number: ____________________________
• Academic Major: ___________________________
• Strengths/Skills: _________________________
• Preferred Role in Project: _______________
• Previous Research Experience: ______________

**Member 2:**
[Repeat above format]

**Member 3:**
[Repeat above format]

**Member 4 (if applicable):**
[Repeat above format]

**🎯 PROJECT ADMINISTRATION:**
• Selected Topic: ____________________________
• Research Question (Draft): _______________
• Group Meeting Schedule: ____________________
• Primary Communication Method: ______________
• File Sharing Platform: ____________________
• Project Timeline: __________________________
""",
            
            "research_paper": """
**📊 ARGUMENTATIVE RESEARCH PAPER DEVELOPMENT:**

**🔍 RESEARCH QUESTION & THESIS:**
• Finalized Research Question: _______________
• Thesis Statement: _________________________
• Key Arguments (3-4 main points):
  1. ______________________________________
  2. ______________________________________  
  3. ______________________________________
  4. ______________________________________

**📖 PAPER STRUCTURE & DRAFTS:**

**INTRODUCTION (300-400 words)**
[Draft your introduction here - background, context, research question, thesis]

Current Word Count: _____ / 400
Status: □ Not Started □ Draft □ Under Review □ Final

**LITERATURE REVIEW & EVIDENCE (600-700 words)**  
[Draft your literature review and evidence section here]

Current Word Count: _____ / 700
Status: □ Not Started □ Draft □ Under Review □ Final

**POLICY RECOMMENDATIONS (400-500 words)**
[Draft your policy recommendations here]

Current Word Count: _____ / 500
Status: □ Not Started □ Draft □ Under Review □ Final

**CONCLUSION (200-300 words)**
[Draft your conclusion here]

Current Word Count: _____ / 300
Status: □ Not Started □ Draft □ Under Review □ Final

**📚 REFERENCE LIST (Harvard Style):**
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________
[Continue numbering - aim for 15-20 sources]
""",
            
            "public_sources": """
**🌐 PUBLIC & ACADEMIC SOURCES COLLECTION:**

**📖 ACADEMIC SOURCES:**

**Source 1:**
• Type: □ Journal Article □ Book □ Report □ Conference Paper
• Author(s): _____________________________________
• Title: ________________________________________
• Publication/Journal: ___________________________
• Year: _______ Volume/Issue: ____________________
• Pages: _______________________________________
• DOI/URL: _____________________________________
• Key Findings: _________________________________
• Relevance to Research Question: _______________
• Quality Rating (1-10): _______________________
• Harvard Citation: _____________________________

[Repeat template for Sources 2-10]

**📰 NEWS & MEDIA SOURCES:**

**Source A:**
• Publication: __________________________________
• Author: ______________________________________
• Title: _______________________________________
• Date: _______________________________________
• URL: ________________________________________
• Key Points: __________________________________
• Credibility Assessment: _______________________
• How It Supports Argument: ____________________

[Repeat template for Sources B-F]

**🏢 ORGANIZATIONAL/NGO REPORTS:**
[Similar template for organizational sources]

**📊 SOURCE ANALYSIS:**
• Common Themes Identified: _____________________
• Conflicting Viewpoints: ______________________
• Research Gaps Found: __________________________
• Most Compelling Evidence: _____________________
""",
            
            "government_info": """
**🏛️ GOVERNMENT INFORMATION COLLECTION:**

**📊 ACCESS TO INFORMATION REQUESTS:**

**Request 1:**
• Target Department/Bureau: _____________________
• Contact Person/Office: ________________________
• Information Requested: _______________________
• Request Method: □ Email □ Online Form □ Phone □ In-person
• Date Submitted: _______________________________
• Reference Number: _____________________________
• Expected Response Date: _______________________
• Actual Response Date: _________________________
• Status: □ Pending □ Partial Response □ Complete □ Denied
• Information Received: _________________________
• Quality of Response: __________________________
• Follow-up Required: ___________________________

[Repeat for Requests 2-5]

**📈 GOVERNMENT DATA ANALYSIS:**
• Key Statistical Findings: _____________________
• Policy Gaps Identified: ______________________
• Trends and Patterns: ___________________________
• Data Limitations: _____________________________
• Comparison with Other Jurisdictions: ____________

**💼 STAKEHOLDER MAPPING:**
• Primary Government Contacts: ___________________
• Secondary Contacts: ____________________________
• Community Leaders Contacted: ___________________
• NGO Representatives: ___________________________

**📋 DOCUMENTATION TRACKING:**
• Emails Sent: _____ Responses Received: __________
• Documents Obtained: ____________________________
• Meetings Arranged: _____________________________
• Information Gaps: ______________________________
""",
            
            "brainstorming": """
**💭 BRAINSTORMING & SOLUTION DEVELOPMENT:**

**🧠 PROBLEM ANALYSIS:**
• Core Problem Statement: _______________________
• Problem Scope & Scale: ________________________
• Affected Stakeholders: _______________________
• Current Impact Assessment: ____________________
• Urgency Level: □ Low □ Medium □ High □ Critical

**🔍 EXISTING SOLUTIONS REVIEW:**

**Current Solution 1:**
• Description: __________________________________
• Implementing Organization: ____________________
• Effectiveness Rating (1-10): __________________
• Strengths: ___________________________________
• Weaknesses: __________________________________
• Cost-Benefit Analysis: _______________________
• Stakeholder Feedback: ________________________

[Repeat for Solutions 2-4]

**💡 NEW SOLUTION GENERATION:**

**Innovative Idea 1:**
• Solution Name: ________________________________
• Core Concept: _________________________________
• Implementation Steps: ________________________
• Required Resources: ___________________________
• Timeline: ____________________________________
• Potential Challenges: ________________________
• Success Metrics: _____________________________
• Innovation Level: □ Incremental □ Significant □ Revolutionary

[Repeat for Ideas 2-4]

**🎯 SOLUTION EVALUATION MATRIX:**
[Create comparison table with feasibility, impact, cost scores]

**🏆 RECOMMENDED SOLUTION:**
• Selected Solution: ____________________________
• Justification: _______________________________
• Implementation Plan: __________________________
• Risk Mitigation: _____________________________
""",
            
            "reflection": """
**📖 REFLECTIVE LEARNING JOURNAL:**

**👤 INDIVIDUAL REFLECTIONS:**

**Week _____ Reflection:**
• Date: ________________________________________
• Learning Focus: _______________________________

**What Happened This Week:**
[Describe key activities, experiences, and events]

**Key Learning Moments:**
[Identify significant insights and discoveries]

**Challenges Faced:**
[Document difficulties and how you addressed them]

**Skills Developed:**
[Note new abilities and competencies gained]

**Emotional Journey:**
[Reflect on feelings, motivations, and reactions]

**Connections Made:**
[Link learning to previous knowledge and experiences]

**Future Application:**
[Consider how learning will influence future actions]

**Questions for Further Exploration:**
[Identify areas for continued investigation]

**🤝 GROUP REFLECTION:**
• Team Dynamics Assessment: ____________________
• Communication Effectiveness: __________________
• Collaboration Challenges: ____________________
• Shared Learning Insights: ____________________
• Group Goal Achievement: _______________________

**📊 LEARNING OUTCOMES TRACKING:**
• Research Skills Development: ___________________
• Critical Thinking Growth: ____________________
• Communication Improvement: ____________________
• Civic Engagement Understanding: _______________
""",
            
            "public_writing": """
**📢 PUBLIC WRITING & DISSEMINATION:**

**📝 BLOG POST/ARTICLE DEVELOPMENT:**
• Target Publication: ___________________________
• Target Audience: ______________________________
• Article Title: _______________________________
• Target Word Count: ____________________________
• Current Word Count: ___________________________

**ARTICLE DRAFT:**
[Write your public-facing article here - 800-1000 words]

**📱 SOCIAL MEDIA STRATEGY:**

**Platform 1: Instagram**
• Content Type: □ Infographic □ Carousel □ Video □ Stories
• Key Message: __________________________________
• Visual Elements Planned: ______________________
• Hashtag Strategy: _____________________________
• Posting Schedule: _____________________________

**Platform 2: Twitter/X**
• Thread Structure (5-7 tweets):
  1. Hook: ____________________________________
  2. Problem: _________________________________
  3. Evidence: ________________________________
  4. Solution: ________________________________
  5. Call to Action: __________________________

**📊 ENGAGEMENT TRACKING:**
• Publication Attempts: _________________________
• Media Responses: ______________________________
• Social Media Metrics: _______________________
• Community Feedback: __________________________

**🎯 IMPACT MEASUREMENT:**
• Reach Achieved: _______________________________
• Engagement Rate: ______________________________
• Policy Discussion Generated: __________________
• Stakeholder Responses: _______________________
""",
            
            "project_management": """
**📈 PROJECT MANAGEMENT & COORDINATION:**

**📅 MILESTONE TRACKING:**
[Week-by-week progress chart]

Week 2: □ Complete □ In Progress □ Not Started
- Task: Team formation and topic selection
- Deadline: ___________
- Status: _____________

Week 3: □ Complete □ In Progress □ Not Started  
- Task: Research question development
- Deadline: ___________
- Status: _____________

[Continue for Weeks 4-15]

**⚠️ RISK MANAGEMENT:**
• Identified Risk 1: ____________________________
  - Probability: □ High □ Medium □ Low
  - Impact: □ High □ Medium □ Low
  - Mitigation Strategy: _______________________

[Repeat for additional risks]

**📋 QUALITY ASSURANCE:**
• Review Schedule: _____________________________
• Quality Standards Checklist: __________________
• Peer Review Process: _________________________

**🤝 TEAM COORDINATION:**
• Meeting Minutes Archive: ______________________
• Task Distribution: ___________________________
• Communication Log: ____________________________
• Conflict Resolution Record: __________________
""",
            
            "research_methods": """
**🔍 RESEARCH METHODOLOGY & CITATION:**

**📊 RESEARCH DESIGN:**
• Research Type: □ Exploratory □ Descriptive □ Analytical
• Primary Approach: □ Quantitative □ Qualitative □ Mixed
• Data Collection Strategy: ____________________
• Analysis Framework: ___________________________

**📚 CITATION TRACKING:**

**Source #1:**
• Source Type: _________________________________
• Author: _____________________________________
• Title: ______________________________________
• Publication Details: _________________________
• Page Numbers Used: ___________________________
• Key Quote/Data: ______________________________
• Used in Section: _____________________________
• Harvard Citation: ____________________________

[Repeat for all sources]

**🔍 SOURCE EVALUATION:**
• Authority Assessment: ________________________
• Currency Check: ______________________________
• Accuracy Verification: ______________________
• Purpose Analysis: ____________________________

**📊 DATA ANALYSIS METHODS:**
• Statistical Methods Used: ____________________
• Qualitative Analysis Approach: _______________
• Software/Tools Utilized: ____________________
• Limitations Identified: ______________________

**✅ QUALITY ASSURANCE CHECKLIST:**
□ All sources properly cited in Harvard format
□ Reference list alphabetically ordered  
□ In-text citations match reference list
□ Facts and figures verified
□ Bias and limitations acknowledged
□ Research methodology documented
"""
        }
        
        return templates.get(content_type, "")
    
    def clear_and_reorganize_content(self, tab_structure):
        """Clear existing content and add organized structure"""
        print("🔄 Reorganizing document content...")
        
        try:
            # First, clear all existing content from all tabs
            print("📝 Clearing existing content...")
            
            # Get current document content
            doc = self.docs_service.documents().get(
                documentId=self.document_id,
                includeTabsContent=True
            ).execute()
            
            # Define content mapping for each tab
            tab_content_mapping = {
                "Team Membership": ("membership", "Team membership and project administration"),
                "Argumentative Research Paper": ("research_paper", "Main research paper development"),
                "Public Sources Collection": ("public_sources", "Academic and media source collection"),
                "Government Information": ("government_info", "Government data and Access to Information requests"),
                "Brainstorming & Solutions": ("brainstorming", "Solution development and critical analysis"), 
                "Reflection Journal": ("reflection", "Individual and group learning reflection"),
                "Public Writing": ("public_writing", "Public engagement and media strategy"),
                "Project Management": ("project_management", "Timeline and coordination tracking"),
                "Research Methods": ("research_methods", "Methodology and citation management")
            }
            
            # Process each tab
            all_requests = []
            
            for tab_info in tab_structure:
                tab_title = tab_info['title']
                tab_id = tab_info['id']
                
                # Find matching content type
                content_type = "main"
                for key, (ctype, desc) in tab_content_mapping.items():
                    if key.lower() in tab_title.lower():
                        content_type = ctype
                        break
                
                print(f"📝 Processing tab: {tab_title} (Type: {content_type})")
                
                # Create new content for this tab
                new_content = self.create_tab_content_template(tab_title, content_type)
                
                # Add request to clear and insert new content
                # Note: We'll insert at beginning and let existing content flow after
                all_requests.append({
                    'insertText': {
                        'location': {
                            'tabId': tab_id,
                            'index': 1
                        },
                        'text': new_content + '\n\n' + '='*80 + '\nPREVIOUS CONTENT (if any):\n' + '='*80 + '\n\n'
                    }
                })
                
                # Process child tabs if any
                for child_info in tab_info['child_tabs']:
                    child_title = child_info['title'] 
                    child_id = child_info['id']
                    
                    # Find content type for child tab
                    child_content_type = "main"
                    for key, (ctype, desc) in tab_content_mapping.items():
                        if key.lower() in child_title.lower():
                            child_content_type = ctype
                            break
                    
                    print(f"  📝 Processing child tab: {child_title} (Type: {child_content_type})")
                    
                    child_content = self.create_tab_content_template(child_title, child_content_type)
                    
                    all_requests.append({
                        'insertText': {
                            'location': {
                                'tabId': child_id,
                                'index': 1
                            },
                            'text': child_content + '\n\n' + '='*80 + '\nPREVIOUS CONTENT (if any):\n' + '='*80 + '\n\n'
                        }
                    })
            
            # Execute all requests in batches to avoid overwhelming the API
            batch_size = 5
            for i in range(0, len(all_requests), batch_size):
                batch = all_requests[i:i + batch_size]
                
                print(f"📤 Executing batch {i//batch_size + 1}/{(len(all_requests) + batch_size - 1)//batch_size}")
                
                result = self.docs_service.documents().batchUpdate(
                    documentId=self.document_id,
                    body={'requests': batch}
                ).execute()
                
                print(f"✅ Batch completed")
            
            print("✅ Content reorganization completed!")
            return True
            
        except Exception as e:
            print(f"❌ Error reorganizing content: {e}")
            return False
    
    def run(self):
        """Main execution flow"""
        print("🚀 GCAP3056 Tab Content Organizer")
        print("=" * 60)
        
        # Setup API services
        if not self.setup_services():
            print("❌ Failed to setup Google API services")
            return False
        
        # Get current document structure
        tab_structure, doc = self.get_document_structure()
        if not tab_structure:
            print("❌ Failed to retrieve document structure")
            return False
        
        # Reorganize content
        if not self.clear_and_reorganize_content(tab_structure):
            print("❌ Failed to reorganize content")
            return False
        
        print("\n" + "="*60)
        print("🎉 DOCUMENT REORGANIZATION COMPLETE!")
        print("="*60)
        print(f"📄 Document ID: {self.document_id}")
        print(f"🔗 Access Link: https://docs.google.com/document/d/{self.document_id}/edit")
        print(f"📋 Tabs Processed: {len(tab_structure)}")
        
        print("\n✨ Each tab now includes:")
        print("   📝 Student Work Area - Dedicated space for student content")
        print("   💬 Student-Teacher Communication - Message exchange area")
        print("   🏫 Teacher Response Section - Instructor feedback space")
        print("   🤖 AI Assistant Feedback - Automated analysis and suggestions")
        print("   📊 Progress Tracking - Status updates and completion tracking")
        
        print("\n🎯 Ready for collaborative student project work!")
        
        return True

def main():
    organizer = GCAP3056TabOrganizer()
    success = organizer.run()
    
    if not success:
        print("\n❌ Document reorganization failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

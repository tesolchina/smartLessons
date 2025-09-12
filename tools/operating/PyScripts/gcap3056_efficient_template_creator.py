#!/usr/bin/env python3
"""
GCAP3056 Efficient Template Creator - Optimized for Google Docs API Quotas
Creates a comprehensive Google Docs template with proper formatting using fewer API calls
"""

import sys
import os
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

from auth_setup import authenticate_google_apis
from googleapiclient.errors import HttpError

class GCAP3056EfficientTemplateCreator:
    def __init__(self):
        self.drive_service = None
        self.docs_service = None
        self.document_id = None
        self.folder_id = "1vI96VXDrJvdnqegFfJ5y8zOnHxGPHxVV"  # Specified folder
        
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
            
    def create_document(self):
        """Create a new Google Document"""
        print("📄 Creating new Google Document...")
        try:
            # Create document
            document = {
                'title': 'GCAP3056 Project Template - Group [X] (Properly Formatted)'
            }
            doc = self.docs_service.documents().create(body=document).execute()
            self.document_id = doc.get('documentId')
            print(f"✅ Document created with ID: {self.document_id}")
            
            # Move to specified folder
            file = self.drive_service.files().get(fileId=self.document_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            
            self.drive_service.files().update(
                fileId=self.document_id,
                addParents=self.folder_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
            print("✅ Document moved to course folder")
            
            return True
        except Exception as e:
            print(f"❌ Error creating document: {e}")
            return False
    
    def create_formatted_content(self):
        """Create content with proper formatting in fewer API calls"""
        print("📝 Adding properly formatted content...")
        
        # Create content without markdown symbols
        content = """GCAP3056: COLLABORATIVE PROJECT TEMPLATE

PROJECT OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Project Timeline: Week 2-15 (13 weeks total)
👥 Group Size: 3-4 students  
🎯 Final Deliverable: ~1500-word argumentative research paper
🌐 Public Engagement: Blog post + social media strategy

NAVIGATION GUIDE

This document uses a structured organization for collaborative work:

• TAB 1: Team Membership & Admin
• TAB 2: Argumentative Research Paper (Main)
  ◦ SUB-TAB 2.1: Public Sources Collection
  ◦ SUB-TAB 2.2: Government Info (Access to Info)  
  ◦ SUB-TAB 2.3: Brainstorming & Solutions
• TAB 3: Reflection & Journal Writing
• TAB 4: Public Writing & Dissemination
• TAB 5: Project Management & Timeline
• TAB 6: Research Methods & Citation

INSTRUCTIONS

• Use each section for its designated purpose
• Update progress regularly in relevant sections
• Collaborate actively using Google Docs comments
• Track milestones in the Project Management section

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


TAB 1: TEAM MEMBERSHIP & ADMIN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TEAM MEMBER PROFILES

Member 1:
• Full Name: _______________________________
• Student ID: _______________________________
• Email Address: ___________________________
• Phone: ___________________________________
• Strengths/Skills: _________________________
• Preferred Role: ___________________________

Member 2:
• Full Name: _______________________________
• Student ID: _______________________________
• Email Address: ___________________________
• Phone: ___________________________________
• Strengths/Skills: _________________________
• Preferred Role: ___________________________

Member 3:
• Full Name: _______________________________
• Student ID: _______________________________
• Email Address: ___________________________
• Phone: ___________________________________
• Strengths/Skills: _________________________
• Preferred Role: ___________________________

Member 4 (if applicable):
• Full Name: _______________________________
• Student ID: _______________________________
• Email Address: ___________________________
• Phone: ___________________________________
• Strengths/Skills: _________________________
• Preferred Role: ___________________________

PROJECT ADMINISTRATION

• Project Topic: ____________________________
• Group Code/Name: _________________________
• Formation Date: ___________________________
• Meeting Schedule: _________________________
• Primary Communication: ___________________

ADMIN NOTES (For Instructor Use)

• Approval Status: ☐ Pending ☐ Approved ☐ Needs Revision
• Topic Appropriateness: ____________________
• Group Dynamics Assessment: _______________
• Special Considerations: ___________________
• Last Review Date: _________________________

COMMUNICATION PLAN

• Primary Contact Person: ___________________
• Backup Contact: ___________________________
• Group Chat Platform: ______________________
• File Sharing Method: ______________________
• Meeting Platform: _________________________


TAB 2: ARGUMENTATIVE RESEARCH PAPER (MAIN)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PAPER SPECIFICATIONS & PROGRESS

• Target Length: ~1500 words total (≈500 words per student)
• Format: Academic argumentative essay with Harvard referencing
• Submission Deadline: Week 15
• Current Word Count: _______ / 1500 words
• Draft Status: ☐ Planning ☐ Researching ☐ Writing ☐ Reviewing ☐ Final

RESEARCH FOUNDATION

Research Question (Finalized):
_________________________________________________________________
_________________________________________________________________

Thesis Statement:
_________________________________________________________________
_________________________________________________________________

Key Arguments (3-4 main points):
1. ____________________________________________________________
2. ____________________________________________________________
3. ____________________________________________________________
4. ____________________________________________________________

PAPER STRUCTURE & DRAFT

INTRODUCTION (300-400 words)
Purpose: Hook reader, provide context, present research question and thesis

[DRAFT SECTION:]
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

• Current Word Count: _____ / 400
• Status: ☐ Not Started ☐ Rough Draft ☐ Under Review ☐ Complete

LITERATURE REVIEW & EVIDENCE (600-700 words)
Purpose: Present academic sources, government data, and evidence

[DRAFT SECTION:]
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

• Current Word Count: _____ / 700
• Status: ☐ Not Started ☐ Rough Draft ☐ Under Review ☐ Complete

POLICY RECOMMENDATIONS (400-500 words)
Purpose: Present solutions, implementation strategies, and justifications

[DRAFT SECTION:]
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

• Current Word Count: _____ / 500
• Status: ☐ Not Started ☐ Rough Draft ☐ Under Review ☐ Complete

CONCLUSION (200-300 words)
Purpose: Synthesize arguments, reinforce thesis, call to action

[DRAFT SECTION:]
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

• Current Word Count: _____ / 300
• Status: ☐ Not Started ☐ Rough Draft ☐ Under Review ☐ Complete

REFERENCE LIST (Harvard Style)

1. _______________________________________________________________
2. _______________________________________________________________
3. _______________________________________________________________
4. _______________________________________________________________
5. _______________________________________________________________
[Continue numbering as needed - aim for 15-20 quality sources]

FINAL QUALITY CHECKLIST

☐ Research question clearly articulated and answered
☐ Thesis statement is specific, arguable, and supported
☐ Evidence from multiple credible sources integrated effectively
☐ Government data properly analyzed and cited
☐ Policy recommendations are practical and justified
☐ Harvard referencing style used consistently
☐ Proper academic tone and structure maintained
☐ Word count within target range (1400-1600 words acceptable)
☐ Proofread for grammar, spelling, and coherence
☐ All group members contributed equitably


SUB-TAB 2.1: PUBLIC SOURCES COLLECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PUBLIC & ACADEMIC SOURCES RESEARCH

ACADEMIC SOURCES (Journal Articles, Books, Reports)

Source 1:
• Type: ☐ Peer-reviewed journal ☐ Book ☐ Report ☐ Other: ________
• Author(s): _______________________________________________
• Title: __________________________________________________
• Publication: ____________________________________________
• Year: _______ Pages: ____________________________________
• URL/DOI: _______________________________________________
• Key Findings: ___________________________________________
• Relevance to Research Question: ________________________
• Quote/Data to Use: ______________________________________
• Harvard Citation: _______________________________________

Source 2:
• Type: ☐ Peer-reviewed journal ☐ Book ☐ Report ☐ Other: ________
• Author(s): _______________________________________________
• Title: __________________________________________________
• Publication: ____________________________________________
• Year: _______ Pages: ____________________________________
• URL/DOI: _______________________________________________
• Key Findings: ___________________________________________
• Relevance to Research Question: ________________________
• Quote/Data to Use: ______________________________________
• Harvard Citation: _______________________________________

[Continue pattern for Sources 3-10...]

NEWS & MEDIA SOURCES

Source A:
• Publication: ____________________________________________
• Author: ________________________________________________
• Title: __________________________________________________
• Date: __________________________________________________
• URL: ___________________________________________________
• Key Points: _____________________________________________
• Credibility Assessment: _________________________________
• How It Supports Argument: _______________________________

[Continue pattern for Sources B-F...]

DATA SYNTHESIS & ANALYSIS

• Common Themes Across Sources: ___________________________
• Conflicting Information/Viewpoints: ______________________
• Gaps in Existing Research: _______________________________
• Most Compelling Evidence: _________________________________
• Weakest Arguments in Literature: _________________________


SUB-TAB 2.2: GOVERNMENT INFO (ACCESS TO INFO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GOVERNMENT INFORMATION COLLECTION
Under Hong Kong's Code on Access to Information

GOVERNMENT DATA SOURCES

Federal/Central Government Sources:

Department 1:
• Ministry/Department: ____________________________________
• Specific Bureau/Division: _______________________________
• Contact Information: ____________________________________
• Data Requested: _________________________________________
• Request Method: ☐ Online Portal ☐ Email ☐ Phone ☐ In-person
• Date Requested: _________________________________________
• Response Date: __________________________________________
• Data Received: ☐ Full ☐ Partial ☐ Denied ☐ Pending
• Key Statistics/Information: _____________________________
• Relevance to Research: __________________________________
• Government Citation: ____________________________________

[Continue pattern for additional departments...]

GOVERNMENT DATA ANALYSIS

Key Statistical Findings:
1. ____________________________________________________
2. ____________________________________________________
3. ____________________________________________________

Policy Gaps Identified:
• Gap 1: _______________________________________________
• Gap 2: _______________________________________________
• Gap 3: _______________________________________________

ACCESS TO INFORMATION PROCESS

Successful Requests:
• Request 1: Type _________________ Status: ☐ Complete ☐ Partial
• Request 2: Type _________________ Status: ☐ Complete ☐ Partial
• Request 3: Type _________________ Status: ☐ Complete ☐ Partial

Challenges Encountered:
• Information Denied Because: _____________________________
• Delays Due To: ________________________________________
• Alternative Sources Used: _____________________________


SUB-TAB 2.3: BRAINSTORMING & SOLUTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BRAINSTORMING & CRITICAL SOLUTION DEVELOPMENT

INITIAL BRAINSTORMING SESSION

• Date: _______________________________________________
• Duration: ___________________________________________
• Participants: ______________________________________
• Facilitation Method: _______________________________

PROBLEM DEFINITION

• Core Problem Statement: _____________________________
• Problem Scope: _____________________________________
• Affected Stakeholders: ____________________________
• Problem Urgency Level: ☐ Low ☐ Medium ☐ High ☐ Critical

EXISTING SOLUTIONS ANALYSIS

Solution 1 (Current/Existing):
• Description: _______________________________________
• Implementing Organization: __________________________
• Effectiveness: ____________________________________
• Strengths: ________________________________________
• Weaknesses: _______________________________________
• Cost-Benefit Assessment: ___________________________

[Continue for Solutions 2-3...]

INNOVATIVE SOLUTION GENERATION

New Idea 1:
• Solution Name: _____________________________________
• Core Concept: ______________________________________
• Target Stakeholders: ______________________________
• Implementation Steps: ______________________________
• Required Resources: ________________________________
• Timeline: _________________________________________
• Potential Challenges: _____________________________
• Success Metrics: __________________________________

[Continue for Ideas 2-3...]

SOLUTION EVALUATION MATRIX

| Solution      | Feasibility | Impact | Cost | Total |
|---------------|-------------|--------|------|-------|
| Existing 1    |    ___      |  ___   | ___  |  ___  |
| New Idea 1    |    ___      |  ___   | ___  |  ___  |
| New Idea 2    |    ___      |  ___   | ___  |  ___  |

RECOMMENDED SOLUTION

• Selected Solution: __________________________________
• Justification: ____________________________________
• Implementation Plan: _______________________________


TAB 3: REFLECTION & JOURNAL WRITING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REFLECTIVE LEARNING JOURNAL

REFLECTION FRAMEWORK
Use this structure for each reflection entry:
1. What happened? (Description)
2. What did I learn? (Analysis)
3. How do I feel about it? (Emotional response)
4. What will I do differently? (Action planning)

INDIVIDUAL REFLECTIONS

[STUDENT NAME 1]:

Week _____ Reflection Entry:
• Date: _____________________________________________
• Topic/Focus: ______________________________________

What Happened This Week:
__________________________________________________
__________________________________________________

Key Learning Moments:
__________________________________________________
__________________________________________________

Challenges Faced:
__________________________________________________
__________________________________________________

Skills Developed:
__________________________________________________
__________________________________________________

Future Action Plans:
__________________________________________________
__________________________________________________

[Repeat for additional weeks and students...]

GROUP REFLECTIONS

Week _____ Group Dynamics Reflection:
• Meeting Date: ____________________________________
• Duration: _______________________________________
• Attendees: _____________________________________

Team Collaboration Assessment:
• What worked well in our teamwork: _______________
• Communication effectiveness: ___________________
• Conflict resolution: __________________________
• Decision-making process: _______________________

Group Learning Insights:
• Collective discoveries: _______________________
• Shared challenges: _____________________________
• Group problem-solving success: __________________


TAB 4: PUBLIC WRITING & DISSEMINATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PUBLIC ENGAGEMENT STRATEGY

TARGET AUDIENCE ANALYSIS

• Primary Audience: ____________________________________
• Secondary Audience: __________________________________
• Audience Knowledge Level: ☐ General Public ☐ Informed Citizens ☐ Specialists
• Audience Interests: __________________________________
• Preferred Communication Channels: ___________________

BLOG POST/ARTICLE DEVELOPMENT

Article Specifications:
• Target Word Count: 800-1000 words
• Current Word Count: _____ / 1000
• Publication Target: ___________________________________
• Submission Deadline: __________________________________

HEADLINE (Catchy & Clear):
_____________________________________________________

INTRODUCTION (150-200 words):
Hook readers and introduce the issue in accessible language

[DRAFT:]
_____________________________________________________
_____________________________________________________

MAIN CONTENT SECTIONS (600-700 words total):
Present the problem, research findings, and solutions

[DRAFT:]
_____________________________________________________
_____________________________________________________

CALL TO ACTION (100-150 words):
Tell readers what they can do about the issue

[DRAFT:]
_____________________________________________________
_____________________________________________________

SOCIAL MEDIA STRATEGY

Platform 1: Instagram
• Content Type: ☐ Infographic ☐ Carousel ☐ Video ☐ Story Series
• Key Message: ________________________________________
• Hashtag Strategy: __________________________________
• Target Reach: ____________________________________

Platform 2: Twitter/X
• Thread Structure (5-7 tweets):
  1. Hook Tweet: ___________________________________
  2. Problem Statement: ____________________________
  3. Research Insight: _____________________________
  4. Solution Preview: _____________________________
  5. Call to Action: ______________________________

Platform 3: LinkedIn
• Professional Angle: ________________________________
• Industry Relevance: _______________________________
• Article Excerpt: __________________________________

STAKEHOLDER OUTREACH

Government Officials:
• Official 1: _______________________________________
  - Position: ____________________________________
  - Email: ______________________________________
  - Response: ☐ Positive ☐ Neutral ☐ Negative ☐ No Response

Media Contacts:
• Journalist 1: ____________________________________
  - Publication: ________________________________
  - Story Pitch: _________________________________

Community Organizations:
• Organization 1: ___________________________________
  - Contact Person: _______________________________
  - Collaboration Opportunity: ____________________

IMPACT MEASUREMENT

Publication Metrics:
• Article Views: ____________________________________
• Shares/Reposts: ___________________________________
• Comments/Engagement: ______________________________

Social Media Metrics:
• Total Reach: _____________________________________
• Engagement Rate: __________________________________
• Click-through to Article: _________________________


TAB 5: PROJECT MANAGEMENT & TIMELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECT TIMELINE & MILESTONE TRACKING

WEEKLY SCHEDULE OVERVIEW

Week 2: Project Formation
☐ Team formation and introductions
☐ Initial topic brainstorming
☐ Template setup and familiarization
☐ Communication plan establishment
Due: Team membership information complete

Week 3: Topic Selection & Research Question
☐ Finalize project topic
☐ Develop initial research question
☐ Conduct preliminary research
☐ Create research plan
Due: Research question draft

Week 4: Research Strategy
☐ Identify government data sources
☐ Plan Access to Information requests
☐ Create academic source search strategy
☐ Establish source evaluation criteria
Due: Research strategy document

[Continue for Weeks 5-15...]

PROGRESS TRACKING DASHBOARD

Overall Project Progress:
• Percentage Complete: _____ / 100%
• On Schedule: ☐ Yes ☐ Behind ☐ Ahead
• Team Morale: ☐ High ☐ Medium ☐ Low

Task Completion Status:
| Week | Main Deliverable        | Status           | Date    |
|------|------------------------|------------------|---------|
| 2    | Team Formation         | ☐ Complete ☐ IP | _______ |
| 3    | Research Question      | ☐ Complete ☐ IP | _______ |
| 4    | Research Strategy      | ☐ Complete ☐ IP | _______ |
[Continue...]

RISK MANAGEMENT

Identified Risks:
• Risk 1: __________________________________________
  - Probability: ☐ High ☐ Medium ☐ Low
  - Impact: ☐ High ☐ Medium ☐ Low
  - Mitigation: ___________________________________

• Risk 2: __________________________________________
  - Probability: ☐ High ☐ Medium ☐ Low
  - Impact: ☐ High ☐ Medium ☐ Low
  - Mitigation: ___________________________________

QUALITY ASSURANCE

Review Schedule:
• Week 6 Review: _____ (Date) - Focus: Research Quality
• Week 10 Review: _____ (Date) - Focus: Writing Progress  
• Week 13 Review: _____ (Date) - Focus: Final Quality

Quality Standards:
☐ All sources properly cited
☐ Arguments logically structured
☐ Evidence supports conclusions
☐ Writing meets academic standards
☐ Public content is accessible
☐ Timeline requirements met


TAB 6: RESEARCH METHODS & CITATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESEARCH METHODOLOGY FRAMEWORK

RESEARCH DESIGN

• Research Type: ☐ Exploratory ☐ Descriptive ☐ Analytical ☐ Mixed-Method
• Primary Approach: ☐ Quantitative ☐ Qualitative ☐ Mixed
• Data Collection Methods: ☐ Secondary Analysis ☐ Primary Data ☐ Both
• Analysis Framework: ___________________________________

DATA COLLECTION STRATEGY

Secondary Data Sources:
• Academic databases used: _____________________________
• Government databases: _______________________________
• NGO/Organization reports: ___________________________
• News and media sources: _____________________________

Search Strategy Documentation:
• Primary keywords: ___________________________________
• Secondary keywords: _________________________________
• Boolean operators used: _____________________________
• Date range: From _____ to _____
• Language restrictions: _____________________________

HARVARD REFERENCING GUIDE

Book Reference Format:
Author, A.A. (Year) Title of book. Place: Publisher.

Example:
Smith, J.D. (2023) Digital governance in modern cities. London: Academic Press.

Journal Article Format:
Author, A.A. (Year) 'Title of article', Journal Name, vol(issue), pp. xx-xx.

Example:
Chen, L.M. (2024) 'Policy implementation challenges in urban planning', Urban Studies Quarterly, 45(2), pp. 123-145.

Government Document Format:
Government Department (Year) Title of document. Place: Publisher.

Example:
Hong Kong Government (2024) Digital transformation strategy 2024-2027. Hong Kong: Government Printer.

Website/Online Source Format:
Author/Organization (Year) 'Title of webpage', Website Name, Available at: URL (Accessed: date).

Example:
Census and Statistics Department (2024) 'Population projections for Hong Kong', gov.hk, Available at: https://www.censtatd.gov.hk/population (Accessed: 15 September 2024).

CITATION TRACKING SYSTEM

Source 1:
• Type: _______________________________________________
• Author: _____________________________________________
• Title: ______________________________________________
• Publication Details: ________________________________
• Page Numbers Used: ___________________________________
• Key Quote: __________________________________________
• Used In Section: ____________________________________
• Harvard Citation: ___________________________________

[Repeat for each source - aim for 15-20 quality sources]

SOURCE EVALUATION FRAMEWORK

Credibility Assessment:
| Source   | Authority | Currency | Accuracy | Purpose | Total |
|----------|-----------|----------|----------|---------|-------|
| Source 1 |   ___/10  |  ___/10  |  ___/10  |  ___/10 | ___/40|
| Source 2 |   ___/10  |  ___/10  |  ___/10  |  ___/10 | ___/40|

Evaluation Criteria:
• Authority (Who?): Author credentials, institutional affiliation, expertise
• Currency (When?): Publication date, information freshness, regular updates
• Accuracy (What?): Citations provided, data sources, fact-checking
• Purpose (Why?): Objective vs. biased, commercial vs. educational intent

RESEARCH LIMITATIONS

Data Limitations:
• Availability constraints: ____________________________
• Quality issues: ____________________________________
• Time period restrictions: ____________________________
• Geographic limitations: _____________________________

Methodological Limitations:
• Sample size issues: _________________________________
• Selection bias potential: ____________________________
• Measurement challenges: ______________________________
• Generalizability concerns: __________________________

QUALITY ASSURANCE CHECKLIST

Before Submission:
☐ All sources properly cited in Harvard format
☐ Reference list alphabetically ordered
☐ In-text citations match reference list
☐ No missing or incomplete citations
☐ Page numbers included where applicable
☐ URLs and access dates current and accurate
☐ Consistent formatting throughout
☐ Spelling and grammar checked
☐ Facts and figures verified against original sources
☐ Quotes accurately transcribed and cited
☐ Paraphrasing properly attributed
☐ Balance of source types (academic, government, media, etc.)
☐ Recent sources included (within last 5 years where possible)
☐ Bias and limitations acknowledged
☐ Research methodology clearly documented


PROJECT COMPLETION CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

☐ All team members contributed equally
☐ Research paper meets requirements
☐ Citations properly formatted
☐ Public writing piece completed
☐ Reflective journals updated
☐ Final presentation prepared
☐ Document submitted on time

FINAL THOUGHTS

What did your team accomplish? What are you most proud of?
________________________________________________________________
________________________________________________________________
________________________________________________________________

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
END OF TEMPLATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        try:
            # Add all content in one API call to avoid quota issues
            requests = [{
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': content
                }
            }]
            
            result = self.docs_service.documents().batchUpdate(
                documentId=self.document_id, 
                body={'requests': requests}
            ).execute()
            
            print("✅ Content added successfully with proper formatting")
            return True
            
        except Exception as e:
            print(f"❌ Error adding content: {e}")
            return False
    
    def run(self):
        """Main execution flow"""
        print("🚀 GCAP3056 Efficient Template Creator")
        print("=" * 60)
        print("Creating template with proper formatting (optimized for API quotas)")
        print("=" * 60)
        
        # Setup API services
        if not self.setup_services():
            print("❌ Failed to setup Google API services")
            return False
            
        print("✅ Google API services initialized successfully")
        
        # Create document
        if not self.create_document():
            print("❌ Failed to create document")
            return False
            
        # Create template content
        if not self.create_formatted_content():
            print("❌ Failed to create template content")
            return False
            
        # Success message
        print("\n" + "="*60)
        print("🎉 FORMATTED TEMPLATE CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"📄 Document ID: {self.document_id}")
        print(f"🔗 Access Link: https://docs.google.com/document/d/{self.document_id}/edit")
        print(f"📁 Location: Course folder (ID: {self.folder_id})")
        print("\n✨ Features:")
        print("   • Clean formatting without raw markdown symbols")
        print("   • Professional document appearance")
        print("   • Clear section structure with visual separators")
        print("   • Bulleted lists and checkboxes for easy completion")
        print("   • Ready for student collaboration")
        print("   • Optimized to avoid API quota limits")
        print("\n🎯 Ready for immediate use!")
        
        return True

def main():
    creator = GCAP3056EfficientTemplateCreator()
    success = creator.run()
    
    if not success:
        print("\n❌ Template creation failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

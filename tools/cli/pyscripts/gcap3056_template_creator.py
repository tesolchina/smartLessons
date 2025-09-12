#!/usr/bin/env python3
"""
GCAP3056 Course Project Template Creator
Creates a structured Google Docs template for student projects
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add GoogleDocsAPI to path
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

try:
    from auth_setup import authenticate_google_apis
    from document_editor import DocumentEditor
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError as e:
    print(f"❌ Error importing required modules: {e}")
    print("Make sure GoogleDocsAPI folder contains necessary files")
    sys.exit(1)

class GCAP3056TemplateCreator:
    def __init__(self):
        """Initialize the template creator"""
        self.folder_id = "1vI96VXDrJvdnqegFfJ5y8zOnHxGPHxVV"
        self.credentials = None
        self.docs_service = None
        self.drive_service = None
        
    def setup_services(self):
        """Setup Google API services"""
        try:
            print("🔐 Setting up Google API authentication...")
            self.credentials = authenticate_google_apis()
            
            self.docs_service = build('docs', 'v1', credentials=self.credentials)
            self.drive_service = build('drive', 'v3', credentials=self.credentials)
            print("✅ Google API services initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up services: {e}")
            return False
    
    def create_template_content(self):
        """Generate the template document structure"""
        
        template_content = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': 'GCAP3056: Taking a Stand - Project Template\\n\\n'
                }
            },
            {
                'updateParagraphStyle': {
                    'range': {'startIndex': 1, 'endIndex': 48},
                    'paragraphStyle': {
                        'namedStyleType': 'TITLE',
                        'alignment': 'CENTER'
                    },
                    'fields': 'namedStyleType,alignment'
                }
            }
        ]
        
        # Add sections
        sections = [
            {
                'title': '📋 Tab 1: Team Membership',
                'content': '''
**Team Information**
• Name: [Student Name]
• Student ID: [Student ID]
• Email: [HKBU Email]
• Admin Notes: [For instructor use]

**Project Topic:** [Brief description of chosen topic]
**Date Created:** [Date]

---
'''
            },
            {
                'title': '📝 Tab 2: Argumentative Research Paper (Main)',
                'content': '''
**Research Question:** 
[State your main research question clearly]

**Thesis Statement:** 
[Your main argument/position - approximately 1-2 sentences]

**Target Length:** ~500 words per student
**Current Word Count:** [Update as you write]

**Paper Structure:**
1. **Introduction** (100-150 words)
   - Background context
   - Research question
   - Thesis statement

2. **Literature Review & Evidence** (200-250 words)
   - Academic sources
   - Government data
   - Public information

3. **Analysis & Recommendations** (150-200 words)
   - Critical evaluation
   - Policy recommendations
   - Justification for solutions

4. **Conclusion** (50-100 words)
   - Summary of key points
   - Call to action

**Draft Status:** [ ] Not Started [ ] In Progress [ ] Ready for Review [ ] Complete

---
'''
            },
            {
                'title': '📊 Sub-tab 2.1: Public Sources Information',
                'content': '''
**Academic Literature:**
• [Source 1 - Author, Title, Year, Key Findings]
• [Source 2 - Author, Title, Year, Key Findings]
• [Source 3 - Author, Title, Year, Key Findings]

**News Articles & Media:**
• [Article 1 - Publication, Date, Key Points]
• [Article 2 - Publication, Date, Key Points]

**NGO Reports & Publications:**
• [Report 1 - Organization, Title, Year, Relevant Data]
• [Report 2 - Organization, Title, Year, Relevant Data]

**International Examples:**
• [Country/City 1 - Policy example, Outcomes]
• [Country/City 2 - Policy example, Outcomes]

**Statistical Data:**
• [Data source 1 - Organization, Statistics, Relevance]
• [Data source 2 - Organization, Statistics, Relevance]

**Research Notes:**
[Add your analysis and synthesis of public sources here]

---
'''
            },
            {
                'title': '🏛️ Sub-tab 2.2: Government Information (Code on Access)',
                'content': '''
**Information Requests Sent:**

**Request 1:**
• Department: [Government Department]
• Contact Person: [Name & Email]
• Date Sent: [Date]
• Request Details: [What information you requested]
• Response Received: [ ] Yes [ ] No [ ] Partial
• Response Date: [Date]
• Key Information Obtained: [Summary]
• Follow-up Actions: [If any]

**Request 2:**
• Department: [Government Department]
• Contact Person: [Name & Email]
• Date Sent: [Date]
• Request Details: [What information you requested]
• Response Received: [ ] Yes [ ] No [ ] Partial
• Response Date: [Date]
• Key Information Obtained: [Summary]
• Follow-up Actions: [If any]

**Additional Requests:**
[Add more as needed]

**Government Directory Contacts:**
• [Department 1 - Key contacts identified]
• [Department 2 - Key contacts identified]

**Documentation:**
• Keep copies of all email correspondence
• Save all documents received
• Note any delays or non-responses

---
'''
            },
            {
                'title': '💡 Sub-tab 2.3: Brainstorming & Solution Development',
                'content': '''
**Problem Analysis:**
• **Core Issue:** [Define the main problem clearly]
• **Stakeholders Affected:** [Who is impacted and how]
• **Current Government Response:** [What is being done now]

**Critical Review of Existing Solutions:**
• **Current Policy 1:**
  - Description: [What it is]
  - Strengths: [What works]
  - Weaknesses: [What doesn't work]
  - Evidence: [Data/sources supporting analysis]

• **Current Policy 2:**
  - Description: [What it is]
  - Strengths: [What works]
  - Weaknesses: [What doesn't work]
  - Evidence: [Data/sources supporting analysis]

**Brainstormed Ideas:**
1. [Idea 1 - Brief description]
2. [Idea 2 - Brief description]
3. [Idea 3 - Brief description]
4. [Idea 4 - Brief description]
5. [Idea 5 - Brief description]

**Proposed New Solutions:**
• **Solution 1:** [Detailed description]
  - Implementation steps: [How it would work]
  - Resources needed: [What would be required]
  - Expected outcomes: [What would improve]
  - Potential challenges: [Obstacles to consider]

• **Solution 2:** [Detailed description]
  - Implementation steps: [How it would work]
  - Resources needed: [What would be required]
  - Expected outcomes: [What would improve]
  - Potential challenges: [Obstacles to consider]

**Innovation Elements:**
[What makes your solutions unique or innovative]

---
'''
            },
            {
                'title': '🤔 Tab 3: Reflective Journal Ideas',
                'content': '''
**Weekly Reflections:**

**Week 1 Reflection:**
• What did you learn about government accountability?
• How has your understanding of the "necessary evil" concept evolved?
• What surprised you about the Code on Access to Information?

**Week 2 Reflection:**
• How are you approaching your topic research?
• What challenges have you encountered in finding information?
• How effective are your government information requests?

**Week [X] Reflection:**
• [Add weekly reflection prompts as course progresses]

**Learning Journey:**
• **Biggest Insight:** [What has been your most significant learning]
• **Challenges Faced:** [What difficulties have you encountered]
• **Skills Developed:** [What new abilities have you gained]
• **Personal Growth:** [How has this course changed your perspective]

**AI Chatbot Interactions:**
• **Date:** [When you used the AI assistant]
• **Topic Discussed:** [What you explored]
• **Key Insights:** [What you learned]
• **Follow-up Questions:** [What you want to explore further]

**Critical Thinking Development:**
• How has your ability to analyze government policies improved?
• What questions do you now ask that you didn't before?
• How has your research methodology evolved?

---
'''
            },
            {
                'title': '📢 Tab 4: Writing for the Public',
                'content': '''
**Public Writing Goals:**
• **Target Audience:** [Who you want to reach]
• **Key Message:** [Main point you want to communicate]
• **Call to Action:** [What you want readers to do]

**SCMP Letter to Editor:**
• **Status:** [ ] Planning [ ] Draft [ ] Submitted [ ] Published
• **Topic:** [Subject of your letter]
• **Word Count:** [Aim for 200-400 words]
• **Draft:** [Write your letter here]
• **Submission Date:** [When sent]
• **Response:** [If published or feedback received]

**Opinion Piece:**
• **Status:** [ ] Planning [ ] Draft [ ] Submitted [ ] Published
• **Publication Target:** [Which media outlet]
• **Topic:** [Subject of your piece]
• **Word Count:** [Target length]
• **Angle:** [Your unique perspective]
• **Draft:** [Write your piece here]

**Social Media Strategy:**
• **Platforms:** [Where you'll share - Facebook, Instagram, etc.]
• **Content Plan:** [What you'll post]
• **Hashtags:** [Relevant tags to use]
• **Engagement Goals:** [What response you hope for]

**Community Engagement:**
• **Events Attended:** [Community meetings, forums, etc.]
• **Presentations Given:** [If any]
• **Feedback Received:** [From community members]
• **Impact Measured:** [How you're tracking effectiveness]

---
'''
            },
            {
                'title': '📊 Tab 5: Project Management & Timeline',
                'content': '''
**Project Timeline:**

**Week 1-2: Foundation & Topic Selection**
- [ ] Choose research topic
- [ ] Form research question
- [ ] Identify key stakeholders
- [ ] Begin literature review

**Week 3-4: Research Phase**
- [ ] Send government information requests
- [ ] Gather academic sources
- [ ] Conduct preliminary analysis
- [ ] Start drafting sections

**Week 5-6: Data Collection**
- [ ] Follow up on government requests
- [ ] Interview stakeholders (if applicable)
- [ ] Analyze collected data
- [ ] Refine thesis statement

**Week 7-8: Writing & Development**
- [ ] Complete first draft of paper
- [ ] Write for public (letter/article)
- [ ] Peer review and feedback
- [ ] Revise and improve

**Week 9-10: Finalization**
- [ ] Complete final draft
- [ ] Submit public writing
- [ ] Prepare presentation
- [ ] Final review and polish

**Resource Tracking:**
• **Sources Found:** [Number and quality]
• **Government Responses:** [How many received]
• **Public Engagement:** [Letters submitted, responses received]
• **Challenges Encountered:** [Problems and solutions]

**Quality Checkpoints:**
- [ ] Research question is clear and focused
- [ ] Evidence supports arguments
- [ ] Government data has been incorporated
- [ ] Public writing is engaging and accessible
- [ ] Recommendations are practical and evidence-based

---
'''
            },
            {
                'title': '🔍 Tab 6: Research Methods & Evidence',
                'content': '''
**Research Methodology:**
• **Primary Research Methods:**
  - [ ] Government information requests
  - [ ] Interviews with stakeholders
  - [ ] Surveys (if applicable)
  - [ ] Site visits/observations

• **Secondary Research Methods:**
  - [ ] Academic literature review
  - [ ] Government document analysis
  - [ ] Media content analysis
  - [ ] Comparative policy analysis

**Evidence Evaluation Criteria:**
• **Credibility:** Is the source trustworthy?
• **Currency:** Is the information current?
• **Relevance:** Does it address your research question?
• **Authority:** Who produced this information?
• **Accuracy:** Can you verify the claims?

**Data Organization:**
• **Source Database:** [How you're tracking sources]
• **Note-taking System:** [Your method for organizing information]
• **Citation Management:** [How you're handling references]
• **File Organization:** [How you store documents]

**Research Ethics:**
• Respect for privacy in government requests
• Accurate representation of findings
• Acknowledgment of limitations
• Fair treatment of opposing viewpoints

---
'''
            }
        ]
        
        # Add each section to the document
        current_index = 49  # Start after title
        
        for section in sections:
            # Add section title
            template_content.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': f"\\n{section['title']}\\n"
                }
            })
            
            title_start = current_index + 1
            title_end = current_index + len(section['title']) + 2
            current_index = title_end
            
            # Style the section title
            template_content.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': title_start, 'endIndex': title_end},
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_1'
                    },
                    'fields': 'namedStyleType'
                }
            })
            
            # Add section content
            template_content.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': section['content']
                }
            })
            
            current_index += len(section['content'])
        
        return template_content
    
    def create_document(self):
        """Create the Google Doc template"""
        try:
            print("📄 Creating new Google Document...")
            
            # Create a new document
            doc = self.docs_service.documents().create(body={
                'title': f'GCAP3056 Project Template - {datetime.now().strftime("%Y-%m-%d")}'
            }).execute()
            
            doc_id = doc['documentId']
            print(f"✅ Document created with ID: {doc_id}")
            
            # Add content to the document
            print("✏️ Adding template content...")
            requests = self.create_template_content()
            
            # Execute the batch update
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print("✅ Content added successfully")
            
            # Move document to specified folder
            print("📁 Moving document to specified folder...")
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=self.folder_id,
                removeParents='root'
            ).execute()
            
            print("✅ Document moved to folder successfully")
            
            # Get document URL
            doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
            
            return {
                'doc_id': doc_id,
                'doc_url': doc_url,
                'title': doc['title']
            }
            
        except HttpError as e:
            print(f"❌ HTTP Error creating document: {e}")
            return None
        except Exception as e:
            print(f"❌ Error creating document: {e}")
            return None
    
    def create_additional_suggestions(self):
        """Suggest additional tabs based on the project structure"""
        suggestions = [
            "📈 Tab 7: Data Analysis & Visualization",
            "🌍 Tab 8: International Comparisons", 
            "💰 Tab 9: Budget & Resource Analysis",
            "📞 Tab 10: Stakeholder Contact Log",
            "📅 Tab 11: Meeting Minutes & Notes",
            "🎯 Tab 12: Impact Assessment & Metrics"
        ]
        
        return suggestions

def main():
    """Main execution function"""
    print("🚀 GCAP3056 Project Template Creator")
    print("=" * 50)
    
    creator = GCAP3056TemplateCreator()
    
    # Setup Google API services
    if not creator.setup_services():
        print("❌ Failed to setup Google API services")
        return False
    
    # Create the template document
    result = creator.create_document()
    
    if result:
        print("\\n✅ GCAP3056 Project Template Created Successfully!")
        print(f"📄 Document Title: {result['title']}")
        print(f"🔗 Document URL: {result['doc_url']}")
        print(f"📍 Folder: https://drive.google.com/drive/folders/{creator.folder_id}")
        
        # Show additional tab suggestions
        print("\\n💡 Additional Tab Suggestions:")
        suggestions = creator.create_additional_suggestions()
        for suggestion in suggestions:
            print(f"   • {suggestion}")
        
        print("\\n📋 Template Structure Created:")
        print("   ✓ Tab 1: Team Membership")
        print("   ✓ Tab 2: Argumentative Research Paper (Main)")
        print("   ✓ Sub-tab 2.1: Public Sources Information")
        print("   ✓ Sub-tab 2.2: Government Information (Code on Access)")
        print("   ✓ Sub-tab 2.3: Brainstorming & Solution Development")
        print("   ✓ Tab 3: Reflective Journal Ideas")
        print("   ✓ Tab 4: Writing for the Public")
        print("   ✓ Tab 5: Project Management & Timeline")
        print("   ✓ Tab 6: Research Methods & Evidence")
        
        # Save document info locally
        info_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3056/gcap3056_template_info.md"
        try:
            with open(info_file, 'w', encoding='utf-8') as f:
                f.write(f"""# GCAP3056 Project Template

## Document Information
- **Title:** {result['title']}
- **Document ID:** {result['doc_id']}
- **URL:** {result['doc_url']}
- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Folder:** https://drive.google.com/drive/folders/{creator.folder_id}

## Template Structure
1. Tab 1: Team Membership
2. Tab 2: Argumentative Research Paper (Main)
   - Sub-tab 2.1: Public Sources Information
   - Sub-tab 2.2: Government Information (Code on Access)
   - Sub-tab 2.3: Brainstorming & Solution Development
3. Tab 3: Reflective Journal Ideas
4. Tab 4: Writing for the Public
5. Tab 5: Project Management & Timeline
6. Tab 6: Research Methods & Evidence

## Usage
Students can make copies of this template for their individual or group projects.
""")
            print(f"\\n📝 Template info saved to: {info_file}")
        except Exception as e:
            print(f"⚠️ Could not save template info: {e}")
        
        return True
    else:
        print("❌ Failed to create template document")
        return False

if __name__ == "__main__":
    main()

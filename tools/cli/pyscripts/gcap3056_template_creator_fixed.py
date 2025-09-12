#!/usr/bin/env python3
"""
GCAP3056 Project Template Creator - Fixed Version
Creates a comprehensive Google Docs template for student project groups
"""

import sys
import os
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

from auth_setup import authenticate_google_apis
from googleapiclient.errors import HttpError

class GCAP3056TemplateCreator:
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
                'title': 'GCAP3056 Project Template - Group [X]'
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
            
    def add_content_section(self, content):
        """Add content to document sequentially"""
        try:
            requests = [{
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': content + '\n'
                }
            }]
            
            result = self.docs_service.documents().batchUpdate(
                documentId=self.document_id, 
                body={'requests': requests}
            ).execute()
            return True
        except Exception as e:
            print(f"❌ Error adding content: {e}")
            return False
    
    def create_template_content(self):
        """Create all template sections"""
        print("✏️ Adding template content...")
        
        sections = [
            {
                'title': 'GCAP3056 Project Template - Collaborative Document',
                'content': '''
=================================================================
GCAP3056: COLLABORATIVE PROJECT TEMPLATE
=================================================================

📅 Project Timeline: Week 2-15 (13 weeks total)
👥 Group Size: 3-4 students
🎯 Final Deliverable: ~1500-word argumentative research paper

**Instructions:**
• This is your group's shared workspace
• Each tab serves a specific project phase
• Update regularly and collaborate actively
• Use comments for communication
• Track your progress weekly

**Navigation Guide:**
📋 Tab 1: Team Membership & Project Overview
📝 Tab 2: Argumentative Research Paper (Main)
🏛️ Tab 3: Government Information Collection
💭 Tab 4: Brainstorming & Idea Development
📖 Tab 5: Reflective Journal
📢 Tab 6: Public Writing & Dissemination

=================================================================
'''
            },
            {
                'title': '\n📋 TAB 1: TEAM MEMBERSHIP & PROJECT OVERVIEW',
                'content': '''
-----------------------------------------------------------------
**👥 TEAM MEMBERS:**

**Member 1:**
• Name: ________________
• Student ID: ________________
• Email: ________________
• Strengths: ________________
• Preferred role: ________________

**Member 2:**
• Name: ________________
• Student ID: ________________
• Email: ________________
• Strengths: ________________
• Preferred role: ________________

**Member 3:**
• Name: ________________
• Student ID: ________________
• Email: ________________
• Strengths: ________________
• Preferred role: ________________

**Member 4 (if applicable):**
• Name: ________________
• Student ID: ________________
• Email: ________________
• Strengths: ________________
• Preferred role: ________________

**📞 COMMUNICATION PLAN:**
• Primary communication method: ________________
• Meeting schedule: ________________
• File sharing method: ________________
• Emergency contact plan: ________________

**🎯 PROJECT OVERVIEW:**
• Topic (preliminary): ________________
• Research question: ________________
• Why this topic matters: ________________
• Initial thesis statement: ________________

**📅 MILESTONE TRACKER:**
□ Week 2: Team formation & topic selection
□ Week 4: Research question finalized
□ Week 6: Government data collection complete
□ Week 8: Literature review complete
□ Week 10: First draft complete
□ Week 12: Peer review complete
□ Week 14: Final paper submitted

**🎯 ROLE ASSIGNMENTS:**
• Research coordinator: ________________
• Writing coordinator: ________________
• Data analyst: ________________
• Quality assurance: ________________

-----------------------------------------------------------------
'''
            },
            {
                'title': '\n📝 TAB 2: ARGUMENTATIVE RESEARCH PAPER (MAIN)',
                'content': '''
-----------------------------------------------------------------
**🎯 PAPER SPECIFICATIONS:**
• Target Length: ~1500 words total (~500 words per student)
• Format: Academic argumentative essay
• Citations: Harvard referencing style
• Deadline: Week 15

**📊 CURRENT STATUS:**
• Word count: _____ / 1500
• Sections complete: _____ / 4
• Citations collected: _____ (aim for 15-20)
• Peer reviews: _____ / 2

**🔍 RESEARCH QUESTION:**
[Write your finalized research question here]

**💡 THESIS STATEMENT:**
[Your main argument - 1-2 clear sentences]

**📖 PAPER STRUCTURE:**

**1. INTRODUCTION (300-400 words)**
[Background, context, research question, thesis statement]

Current draft:
________________

Word count: _____ / 400
Status: □ Not started □ Draft □ Review □ Final

**2. LITERATURE REVIEW & EVIDENCE (600-700 words)**
[Academic sources, government data, analysis]

Current draft:
________________

Word count: _____ / 700
Status: □ Not started □ Draft □ Review □ Final

**3. POLICY RECOMMENDATIONS (400-500 words)**
[Solutions, implementation, justification]

Current draft:
________________

Word count: _____ / 500
Status: □ Not started □ Draft □ Review □ Final

**4. CONCLUSION (200-300 words)**
[Summary, call to action, implications]

Current draft:
________________

Word count: _____ / 300
Status: □ Not started □ Draft □ Review □ Final

**📚 REFERENCE LIST:**
[Use Harvard referencing style]

1. ________________
2. ________________
3. ________________
[Continue as needed...]

**✅ QUALITY CHECKLIST:**
□ Research question clearly stated
□ Thesis statement is arguable and specific
□ Evidence supports main argument
□ Sources are credible and current
□ Citations formatted correctly
□ Recommendations are practical
□ Conclusion ties everything together
□ Grammar and style appropriate for academic writing

-----------------------------------------------------------------
'''
            },
            {
                'title': '\n🏛️ TAB 3: GOVERNMENT INFORMATION COLLECTION',
                'content': '''
-----------------------------------------------------------------
**📊 GOVERNMENT DATA SOURCES:**

**Federal Government Sources:**
• Department/Agency: ________________
• Relevant data: ________________
• URL: ________________
• Date accessed: ________________
• Key findings: ________________

• Department/Agency: ________________
• Relevant data: ________________
• URL: ________________
• Date accessed: ________________
• Key findings: ________________

**Provincial Government Sources:**
• Department/Agency: ________________
• Relevant data: ________________
• URL: ________________
• Date accessed: ________________
• Key findings: ________________

**Municipal Government Sources:**
• Department/Agency: ________________
• Relevant data: ________________
• URL: ________________
• Date accessed: ________________
• Key findings: ________________

**📈 DATA ANALYSIS:**
• Pattern 1: ________________
• Pattern 2: ________________
• Pattern 3: ________________

**🎯 KEY INSIGHTS:**
• Main finding 1: ________________
• Main finding 2: ________________
• Main finding 3: ________________

**⚠️ DATA LIMITATIONS:**
• Limitation 1: ________________
• Limitation 2: ________________
• How we addressed these: ________________

**📝 CITATION NOTES:**
[Track all government sources with proper attribution]
________________

-----------------------------------------------------------------
'''
            },
            {
                'title': '\n💭 TAB 4: BRAINSTORMING & IDEA DEVELOPMENT',
                'content': '''
-----------------------------------------------------------------
**🧠 INITIAL BRAINSTORMING SESSION:**

**Meeting Date:** ________________
**Attendees:** ________________

**Topic Ideas Discussed:**
1. ________________
   • Pros: ________________
   • Cons: ________________
   • Feasibility: ___/10

2. ________________
   • Pros: ________________
   • Cons: ________________
   • Feasibility: ___/10

3. ________________
   • Pros: ________________
   • Cons: ________________
   • Feasibility: ___/10

**🎯 SELECTED TOPIC:** ________________
**Reason for selection:** ________________

**🔍 RESEARCH QUESTION DEVELOPMENT:**

**Version 1:** ________________
**Feedback:** ________________

**Version 2:** ________________
**Feedback:** ________________

**Final Version:** ________________
**Why this version:** ________________

**💡 ARGUMENT DEVELOPMENT:**

**Potential Arguments:**
• Argument A: ________________
  - Evidence needed: ________________
  - Strength: ___/10

• Argument B: ________________
  - Evidence needed: ________________
  - Strength: ___/10

• Argument C: ________________
  - Evidence needed: ________________
  - Strength: ___/10

**🎯 CHOSEN ARGUMENT:** ________________

**🔄 ONGOING IDEAS:**
[Use this space for new ideas that emerge during research]

• Idea: ________________
  Date: ________________

• Idea: ________________
  Date: ________________

-----------------------------------------------------------------
'''
            },
            {
                'title': '\n📖 TAB 5: REFLECTIVE JOURNAL',
                'content': '''
-----------------------------------------------------------------
**📝 INDIVIDUAL REFLECTIONS:**

**[Student Name 1]:**

**Week _____ Reflection:**
• What I learned: ________________
• Challenges faced: ________________
• How I contributed: ________________
• Goals for next week: ________________
• Date: ________________

**Week _____ Reflection:**
• What I learned: ________________
• Challenges faced: ________________
• How I contributed: ________________
• Goals for next week: ________________
• Date: ________________

---

**[Student Name 2]:**

**Week _____ Reflection:**
• What I learned: ________________
• Challenges faced: ________________
• How I contributed: ________________
• Goals for next week: ________________
• Date: ________________

**Week _____ Reflection:**
• What I learned: ________________
• Challenges faced: ________________
• How I contributed: ________________
• Goals for next week: ________________
• Date: ________________

---

**[Student Name 3]:**

**Week _____ Reflection:**
• What I learned: ________________
• Challenges faced: ________________
• How I contributed: ________________
• Goals for next week: ________________
• Date: ________________

---

**🤝 GROUP REFLECTIONS:**

**Week _____ Group Reflection:**
• Team dynamics: ________________
• Communication effectiveness: ________________
• What's working well: ________________
• What needs improvement: ________________
• Decisions made: ________________
• Action items: ________________
• Date: ________________

**Week _____ Group Reflection:**
• Team dynamics: ________________
• Communication effectiveness: ________________
• What's working well: ________________
• What needs improvement: ________________
• Decisions made: ________________
• Action items: ________________
• Date: ________________

-----------------------------------------------------------------
'''
            },
            {
                'title': '\n📢 TAB 6: PUBLIC WRITING & DISSEMINATION',
                'content': '''
-----------------------------------------------------------------
**🌐 PUBLIC ENGAGEMENT PLAN:**

**Target Audience:** ________________
**Key Message:** ________________
**Dissemination Goals:** ________________

**📝 BLOG POST/ARTICLE DRAFT:**
**Title:** ________________
**Target Word Count:** 800-1000 words
**Current Word Count:** _____ / 1000

**Introduction (150-200 words):**
[Hook your audience and introduce the issue]
________________

**Main Content (500-600 words):**
[Present your research findings in accessible language]
________________

**Call to Action (150-200 words):**
[What do you want readers to do?]
________________

**📱 SOCIAL MEDIA STRATEGY:**

**Platform 1: Twitter/X**
• Thread outline: ________________
• Key hashtags: ________________
• Target engagement: ________________

**Platform 2: LinkedIn**
• Article summary: ________________
• Professional angle: ________________
• Network strategy: ________________

**Platform 3: [Other]**
• Platform: ________________
• Content approach: ________________
• Audience: ________________

**🎯 IMPACT MEASUREMENT:**
• Metric 1: ________________
• Metric 2: ________________
• Metric 3: ________________

**📧 STAKEHOLDER OUTREACH:**
• Contact 1: ________________ (Title: ________)
  - Email drafted: □ Yes □ No
  - Response received: □ Yes □ No

• Contact 2: ________________ (Title: ________)
  - Email drafted: □ Yes □ No
  - Response received: □ Yes □ No

**📊 ENGAGEMENT TRACKER:**
• Date posted: ________________
• Reach: ________________
• Engagement rate: ________________
• Comments/feedback: ________________
• Lessons learned: ________________

-----------------------------------------------------------------

**🎉 PROJECT COMPLETION CHECKLIST:**
□ All team members contributed equally
□ Research paper meets requirements
□ Citations properly formatted
□ Public writing piece completed
□ Reflective journals updated
□ Final presentation prepared
□ Document submitted on time

**🏆 FINAL THOUGHTS:**
[What did your team accomplish? What are you most proud of?]
________________

=================================================================
END OF TEMPLATE
=================================================================
'''
            }
        ]
        
        # Add each section to the document
        for i, section in enumerate(sections):
            print(f"📝 Adding section {i+1}/7: {section['title'][:50]}...")
            if not self.add_content_section(section['title'] + '\n' + section['content']):
                return False
                
        return True
        
    def run(self):
        """Main execution flow"""
        print("🚀 GCAP3056 Project Template Creator")
        print("=" * 50)
        
        # Setup API services
        if not self.setup_services():
            print("❌ Failed to setup Google API services")
            return False
            
        print("✅ Google API services initialized successfully")
        
        # Create document
        if not self.create_document():
            print("❌ Failed to create document")
            return False
            
        # Add template content
        if not self.create_template_content():
            print("❌ Failed to add template content")
            return False
            
        # Success message
        print("\n🎉 SUCCESS! Template created successfully!")
        print(f"📄 Document ID: {self.document_id}")
        print(f"🔗 Access link: https://docs.google.com/document/d/{self.document_id}/edit")
        print(f"📁 Location: Course folder (ID: {self.folder_id})")
        print("\n✅ The template includes:")
        print("   • Team membership and project overview")
        print("   • Structured research paper sections")
        print("   • Government information collection guide")
        print("   • Brainstorming and development space")
        print("   • Individual and group reflection journals")
        print("   • Public writing and dissemination planning")
        print("\n🎯 Ready for student groups to customize and use!")
        
        return True

def main():
    creator = GCAP3056TemplateCreator()
    success = creator.run()
    
    if not success:
        print("\n❌ Template creation failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

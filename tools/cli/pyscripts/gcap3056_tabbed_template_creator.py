#!/usr/bin/env python3
"""
GCAP3056 Tabbed Template Creator - Enhanced Version with Google Docs Tabs
Creates a comprehensive Google Docs template with proper tabs and sub-tabs structure
Uses Google Workspace Docs API tabs feature
"""

import sys
import os
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

from auth_setup import authenticate_google_apis
from googleapiclient.errors import HttpError

class GCAP3056TabbedTemplateCreator:
    def __init__(self):
        self.drive_service = None
        self.docs_service = None
        self.document_id = None
        self.folder_id = "1vI96VXDrJvdnqegFfJ5y8zOnHxGPHxVV"  # Specified folder
        self.tab_ids = {}  # Track created tab IDs
        
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
        print("📄 Creating new Google Document with tabs...")
        try:
            # Create document
            document = {
                'title': 'GCAP3056 Project Template - Group [X] (Enhanced with Tabs)'
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
    
    def create_tab(self, title, parent_tab_id=None):
        """Create a new tab in the document"""
        try:
            requests = [{
                'createNamedRange': {
                    'name': f'tab_{len(self.tab_ids)}',
                    'range': {
                        'startIndex': 1,
                        'endIndex': 2
                    }
                }
            }]
            
            # For now, we'll simulate tabs with sections and clear structure
            # Google Docs tabs API is still in limited preview
            tab_id = f"tab_{len(self.tab_ids)}"
            self.tab_ids[title] = tab_id
            return tab_id
            
        except Exception as e:
            print(f"❌ Error creating tab '{title}': {e}")
            return None
    
    def add_content_to_tab(self, tab_title, content):
        """Add content to a specific tab (simulated with clear sections)"""
        try:
            # Add tab header and content
            full_content = f"\n{'='*80}\n{tab_title.upper()}\n{'='*80}\n\n{content}\n\n"
            
            requests = [{
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': full_content
                }
            }]
            
            result = self.docs_service.documents().batchUpdate(
                documentId=self.document_id, 
                body={'requests': requests}
            ).execute()
            return True
        except Exception as e:
            print(f"❌ Error adding content to tab '{tab_title}': {e}")
            return False
    
    def create_template_structure(self):
        """Create the complete template structure with tabs and content"""
        print("🏗️ Creating template structure with tabs...")
        
        # Template overview
        overview_content = """GCAP3056: COLLABORATIVE PROJECT TEMPLATE (ENHANCED WITH TABS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Project Timeline: Week 2-15 (13 weeks total)
👥 Group Size: 3-4 students  
🎯 Final Deliverable: ~1500-word argumentative research paper
🌐 Public Engagement: Blog post + social media strategy

**Navigation Guide:**
This document uses a structured tab system for organized collaboration:

📋 TAB 1: Team Membership & Admin
📝 TAB 2: Argumentative Research Paper (Main)
  ├── 📊 SUB-TAB 2.1: Public Sources Collection
  ├── 🏛️ SUB-TAB 2.2: Government Info (Access to Info)  
  └── 💡 SUB-TAB 2.3: Brainstorming & Solutions
📖 TAB 3: Reflection & Journal Writing
📢 TAB 4: Public Writing & Dissemination
📈 TAB 5: Project Management & Timeline
🔍 TAB 6: Research Methods & Citation

**Instructions:**
• Use each tab for its designated purpose
• Update progress regularly in relevant tabs
• Collaborate actively using Google Docs comments
• Track milestones in the Project Management tab

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        # Tab contents
        tabs_content = [
            {
                'title': '📋 TAB 1: Team Membership & Admin',
                'content': '''
**👥 TEAM MEMBER PROFILES:**

**Member 1:**
• Full Name: _______________________________
• Student ID: _______________________________  
• Email Address: ___________________________
• Phone: ___________________________________
• Strengths/Skills: _________________________
• Preferred Role: ___________________________

**Member 2:**
• Full Name: _______________________________
• Student ID: _______________________________
• Email Address: ___________________________
• Phone: ___________________________________
• Strengths/Skills: _________________________
• Preferred Role: ___________________________

**Member 3:**
• Full Name: _______________________________
• Student ID: _______________________________
• Email Address: ___________________________
• Phone: ___________________________________
• Strengths/Skills: _________________________
• Preferred Role: ___________________________

**Member 4 (if applicable):**
• Full Name: _______________________________
• Student ID: _______________________________
• Email Address: ___________________________
• Phone: ___________________________________
• Strengths/Skills: _________________________
• Preferred Role: ___________________________

**🎯 PROJECT ADMINISTRATION:**
• Project Topic: ____________________________
• Group Code/Name: _________________________
• Formation Date: ___________________________
• Meeting Schedule: _________________________
• Primary Communication: ___________________

**📋 ADMIN NOTES (For Instructor Use):**
• Approval Status: □ Pending □ Approved □ Needs Revision
• Topic Appropriateness: ____________________
• Group Dynamics Assessment: _______________
• Special Considerations: ___________________
• Last Review Date: _________________________

**📞 EMERGENCY CONTACT PLAN:**
• Primary Contact Person: ___________________
• Backup Contact: ___________________________
• Group WhatsApp/WeChat: ___________________
• File Sharing Method: ______________________
'''
            },
            {
                'title': '📝 TAB 2: Argumentative Research Paper (Main)',
                'content': '''
**📊 PAPER SPECIFICATIONS & PROGRESS:**
• Target Length: ~1500 words total (≈500 words per student)
• Format: Academic argumentative essay with Harvard referencing
• Submission Deadline: Week 15
• Current Word Count: _______ / 1500 words
• Draft Status: □ Planning □ Researching □ Writing □ Reviewing □ Final

**🔍 RESEARCH FOUNDATION:**

**Research Question (Finalized):**
_________________________________________________________________
_________________________________________________________________

**Thesis Statement:**
_________________________________________________________________
_________________________________________________________________

**Key Arguments (3-4 main points):**
1. ____________________________________________________________
2. ____________________________________________________________
3. ____________________________________________________________
4. ____________________________________________________________

**📖 PAPER STRUCTURE & DRAFT:**

**INTRODUCTION (300-400 words)**
*Purpose: Hook reader, provide context, present research question and thesis*

[DRAFT SECTION:]
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Current Word Count: _____ / 400
Status: □ Not Started □ Rough Draft □ Under Review □ Complete

**LITERATURE REVIEW & EVIDENCE (600-700 words)**
*Purpose: Present academic sources, government data, and evidence*

[DRAFT SECTION:]
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Current Word Count: _____ / 700
Status: □ Not Started □ Rough Draft □ Under Review □ Complete

**POLICY RECOMMENDATIONS (400-500 words)**
*Purpose: Present solutions, implementation strategies, and justifications*

[DRAFT SECTION:]
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Current Word Count: _____ / 500
Status: □ Not Started □ Rough Draft □ Under Review □ Complete

**CONCLUSION (200-300 words)**
*Purpose: Synthesize arguments, reinforce thesis, call to action*

[DRAFT SECTION:]
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Current Word Count: _____ / 300
Status: □ Not Started □ Rough Draft □ Under Review □ Complete

**📚 REFERENCE LIST (Harvard Style):**
1. _______________________________________________________________
2. _______________________________________________________________
3. _______________________________________________________________
4. _______________________________________________________________
5. _______________________________________________________________
[Continue numbering as needed - aim for 15-20 quality sources]

**✅ FINAL QUALITY CHECKLIST:**
□ Research question clearly articulated and answered
□ Thesis statement is specific, arguable, and supported
□ Evidence from multiple credible sources integrated effectively
□ Government data properly analyzed and cited
□ Policy recommendations are practical and justified
□ Harvard referencing style used consistently
□ Proper academic tone and structure maintained
□ Word count within target range (1400-1600 words acceptable)
□ Proofread for grammar, spelling, and coherence
□ All group members contributed equitably
'''
            },
            {
                'title': '📊 SUB-TAB 2.1: Public Sources Collection',
                'content': '''
**🌐 PUBLIC & ACADEMIC SOURCES RESEARCH:**

**📖 ACADEMIC SOURCES (Journal Articles, Books, Reports):**

**Source 1:**
• Type: □ Peer-reviewed journal □ Book □ Report □ Other: ________
• Author(s): _______________________________________________
• Title: __________________________________________________
• Publication: ____________________________________________
• Year: _______ Pages: ____________________________________
• URL/DOI: _______________________________________________
• Key Findings: ___________________________________________
• Relevance to Research Question: ________________________
• Quote/Data to Use: ______________________________________
• Harvard Citation: _______________________________________

**Source 2:**
• Type: □ Peer-reviewed journal □ Book □ Report □ Other: ________
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

**📰 NEWS & MEDIA SOURCES:**

**Source A:**
• Publication: ____________________________________________
• Author: ________________________________________________
• Title: __________________________________________________
• Date: __________________________________________________
• URL: ___________________________________________________
• Key Points: _____________________________________________
• Credibility Assessment: _________________________________
• How It Supports Argument: _______________________________

[Continue pattern for Sources B-F...]

**🏢 ORGANIZATIONAL/NGO REPORTS:**

**Source X:**
• Organization: ___________________________________________
• Report Title: ___________________________________________
• Publication Date: _______________________________________
• URL: ___________________________________________________
• Executive Summary Points: _______________________________
• Relevant Statistics/Data: _______________________________
• Policy Implications: ____________________________________

[Continue pattern for additional sources...]

**📊 DATA SYNTHESIS & ANALYSIS:**
• Common Themes Across Sources: ___________________________
• Conflicting Information/Viewpoints: ______________________
• Gaps in Existing Research: _______________________________
• Most Compelling Evidence: _________________________________
• Weakest Arguments in Literature: _________________________

**🔍 SEARCH STRATEGY RECORD:**
• Databases Used: _________________________________________
• Search Keywords: ________________________________________
• Date Range Covered: _____________________________________
• Inclusion Criteria: ____________________________________
• Exclusion Criteria: ____________________________________
• Total Sources Reviewed: _________________________________
• Final Sources Selected: _________________________________
'''
            },
            {
                'title': '🏛️ SUB-TAB 2.2: Government Info (Access to Info)',
                'content': '''
**🏛️ GOVERNMENT INFORMATION COLLECTION:**
*Under Hong Kong's Code on Access to Information*

**📋 GOVERNMENT DATA SOURCES:**

**FEDERAL/CENTRAL GOVERNMENT SOURCES:**

**Department 1:**
• Ministry/Department: ____________________________________
• Specific Bureau/Division: _______________________________
• Contact Information: ____________________________________
• Data Requested: _________________________________________
• Request Method: □ Online Portal □ Email □ Phone □ In-person
• Date Requested: _________________________________________
• Response Date: __________________________________________
• Data Received: □ Full □ Partial □ Denied □ Pending
• Key Statistics/Information: _____________________________
• Relevance to Research: __________________________________
• Limitations/Caveats: ____________________________________
• Government Citation: ____________________________________

**Department 2:**
[Repeat above format]

**PROVINCIAL/REGIONAL GOVERNMENT:**

**Department A:**
• Provincial Ministry: ___________________________________
• Data Type: _____________________________________________
• Access Method: _________________________________________
• Key Findings: __________________________________________
• Data Quality Assessment: _______________________________

[Continue pattern...]

**MUNICIPAL/LOCAL GOVERNMENT:**

**Department X:**
• Municipal Department: __________________________________
• Local Data Collected: _________________________________
• Community Impact Data: ________________________________
• Local Policy Information: ____________________________

**📊 GOVERNMENT DATA ANALYSIS:**

**Key Statistical Findings:**
1. ____________________________________________________
2. ____________________________________________________
3. ____________________________________________________

**Policy Gaps Identified:**
• Gap 1: _______________________________________________
• Gap 2: _______________________________________________
• Gap 3: _______________________________________________

**Government Response Patterns:**
• Response Time Average: ________________________________
• Data Availability: ___________________________________
• Transparency Level: ___________________________________
• Bureaucratic Challenges: ______________________________

**🔍 ACCESS TO INFORMATION PROCESS:**

**Successful Requests:**
• Request 1: Type _________________ Status: □ Complete □ Partial
• Request 2: Type _________________ Status: □ Complete □ Partial
• Request 3: Type _________________ Status: □ Complete □ Partial

**Challenges Encountered:**
• Information Denied Because: _____________________________
• Delays Due To: ________________________________________
• Alternative Sources Used: _____________________________

**📈 DATA INTEGRATION:**
• How Government Data Supports Thesis: ____________________
• Contradictions with Public Sources: ____________________
• Unique Insights from Government Data: ___________________
• Policy Recommendations Based on Government Data: _________

**🎯 FOLLOW-UP ACTIONS:**
□ Additional data requests needed
□ Government stakeholder interviews
□ Policy briefing analysis
□ Comparative government data research
'''
            },
            {
                'title': '💡 SUB-TAB 2.3: Brainstorming & Solutions',
                'content': '''
**🧠 BRAINSTORMING & CRITICAL SOLUTION DEVELOPMENT:**

**💭 INITIAL BRAINSTORMING SESSION:**
• Date: _______________________________________________
• Duration: ___________________________________________
• Participants: ______________________________________
• Facilitation Method: _______________________________

**🎯 PROBLEM DEFINITION:**
• Core Problem Statement: _____________________________
• Problem Scope: _____________________________________
• Affected Stakeholders: ____________________________
• Problem Urgency Level: □ Low □ Medium □ High □ Critical

**🔍 EXISTING SOLUTIONS ANALYSIS:**

**Solution 1 (Current/Existing):**
• Description: _______________________________________
• Implementing Organization: __________________________
• Effectiveness: ____________________________________
• Strengths: ________________________________________
• Weaknesses: _______________________________________
• Cost-Benefit Assessment: ___________________________
• Stakeholder Feedback: ______________________________

**Solution 2 (Alternative Existing):**
• Description: _______________________________________
• Effectiveness: ____________________________________
• Strengths: ________________________________________
• Weaknesses: _______________________________________
• Why It's Not Sufficient: __________________________

[Continue for Solutions 3-5...]

**💡 INNOVATIVE SOLUTION GENERATION:**

**New Idea 1:**
• Solution Name: _____________________________________
• Core Concept: ______________________________________
• Target Stakeholders: ______________________________
• Implementation Steps: ______________________________
• Required Resources: ________________________________
• Timeline: _________________________________________
• Potential Challenges: _____________________________
• Success Metrics: __________________________________
• Innovation Level: □ Minor Improvement □ Major Change □ Revolutionary

**New Idea 2:**
[Repeat above format]

**New Idea 3:**
[Repeat above format]

**🎯 SOLUTION EVALUATION MATRIX:**

| Solution | Feasibility (1-10) | Impact (1-10) | Cost (1-10) | Total Score |
|----------|-------------------|---------------|-------------|-------------|
| Existing 1 | _____ | _____ | _____ | _____ |
| Existing 2 | _____ | _____ | _____ | _____ |
| New Idea 1 | _____ | _____ | _____ | _____ |
| New Idea 2 | _____ | _____ | _____ | _____ |
| New Idea 3 | _____ | _____ | _____ | _____ |

**🏆 RECOMMENDED SOLUTION:**
• Selected Solution: __________________________________
• Justification: ____________________________________
• Implementation Plan: _______________________________
• Success Indicators: ______________________________

**🔄 ITERATIVE DEVELOPMENT:**

**Version 1.0 → 2.0 Changes:**
• What Changed: _____________________________________
• Why: _____________________________________________
• Feedback Incorporated: ____________________________

**Version 2.0 → 3.0 Changes:**
• What Changed: _____________________________________
• Why: _____________________________________________
• Feedback Incorporated: ____________________________

**🤝 STAKEHOLDER VALIDATION:**
• Stakeholder 1: ____________________________________
  - Feedback: ______________________________________
  - Adjustments Made: _______________________________

• Stakeholder 2: ____________________________________
  - Feedback: ______________________________________
  - Adjustments Made: _______________________________

**📋 CRITICAL REVIEW CHECKLIST:**
□ Solution addresses root cause, not just symptoms
□ Multiple stakeholder perspectives considered
□ Implementation is realistic and achievable
□ Resource requirements are reasonable
□ Timeline is practical
□ Success can be measured objectively
□ Potential negative consequences identified and mitigated
□ Solution is sustainable long-term
□ Innovation adds meaningful value
□ Solution aligns with existing policy framework
'''
            },
            {
                'title': '📖 TAB 3: Reflection & Journal Writing',
                'content': '''
**📝 REFLECTIVE LEARNING JOURNAL:**

**🎯 REFLECTION FRAMEWORK:**
Use the following structure for each reflection entry:
1. **What happened?** (Description)
2. **What did I learn?** (Analysis)
3. **How do I feel about it?** (Emotional response)
4. **What will I do differently?** (Action planning)

**👤 INDIVIDUAL REFLECTIONS:**

**[STUDENT NAME 1]:**

**Week _____ Reflection Entry:**
• Date: _____________________________________________
• Topic/Focus: ______________________________________

**What Happened This Week:**
__________________________________________________
__________________________________________________

**Key Learning Moments:**
__________________________________________________
__________________________________________________

**Challenges Faced:**
__________________________________________________
__________________________________________________

**Skills Developed:**
__________________________________________________
__________________________________________________

**Emotional Journey:**
__________________________________________________
__________________________________________________

**Future Action Plans:**
__________________________________________________
__________________________________________________

[Repeat reflection template for additional weeks...]

---

**[STUDENT NAME 2]:**
[Same reflection template structure]

---

**[STUDENT NAME 3]:**
[Same reflection template structure]

---

**🤝 GROUP REFLECTIONS:**

**Week _____ Group Dynamics Reflection:**
• Meeting Date: ____________________________________
• Duration: _______________________________________
• Attendees: _____________________________________

**Team Collaboration Assessment:**
• What worked well in our teamwork: _______________
• Communication effectiveness: ___________________
• Conflict resolution: __________________________
• Decision-making process: _______________________
• Task distribution: ____________________________

**Group Learning Insights:**
• Collective discoveries: _______________________
• Shared challenges: _____________________________
• Group problem-solving success: __________________

**Team Development Goals:**
• Areas for improvement: _________________________
• Action items for next week: ___________________
• Group agreements/rules: ________________________

**📊 PROJECT PROGRESS REFLECTION:**

**Research Phase Reflection:**
• Most surprising finding: __________________________
• Biggest research challenge: _______________________
• Information gathering effectiveness: _______________
• Source quality assessment: ________________________

**Writing Phase Reflection:**
• Writing collaboration process: ____________________
• Individual vs. group writing balance: _______________
• Revision and editing effectiveness: ________________
• Academic writing skill development: ________________

**Public Engagement Reflection:**
• Understanding of public communication: _____________
• Challenges in making academic work accessible: _____
• Social media strategy effectiveness: _______________

**🎓 LEARNING OUTCOMES REFLECTION:**

**Course Learning Objectives:**
1. **Critical Analysis Skills:** How has your ability to critically analyze information developed?
   _________________________________________________

2. **Research Methodology:** What research skills have you gained or improved?
   _________________________________________________

3. **Public Communication:** How has your ability to communicate with public audiences changed?
   _________________________________________________

4. **Collaborative Learning:** What have you learned about working in teams?
   _________________________________________________

5. **Policy Understanding:** How has your understanding of policy-making processes evolved?
   _________________________________________________

**🚀 PERSONAL GROWTH TRACKING:**

**Skills Development Matrix:**

| Skill Area | Week 2 Level | Week 8 Level | Week 15 Level | Growth Notes |
|------------|--------------|--------------|---------------|--------------|
| Research | ___/10 | ___/10 | ___/10 | _____________ |
| Writing | ___/10 | ___/10 | ___/10 | _____________ |
| Analysis | ___/10 | ___/10 | ___/10 | _____________ |
| Teamwork | ___/10 | ___/10 | ___/10 | _____________ |
| Public Speaking | ___/10 | ___/10 | ___/10 | _____________ |

**🎯 FINAL COURSE REFLECTION (Week 15):**
• Most significant learning experience: _______________
• Biggest personal challenge overcome: ________________
• Skills I'm most proud of developing: _______________
• How this course changed my perspective: _____________
• Advice for future students: ______________________
• Connection to future career/studies: _______________
'''
            },
            {
                'title': '📢 TAB 4: Public Writing & Dissemination',
                'content': '''
**🌐 PUBLIC ENGAGEMENT STRATEGY:**

**🎯 TARGET AUDIENCE ANALYSIS:**
• Primary Audience: ____________________________________
• Secondary Audience: __________________________________
• Audience Knowledge Level: □ General Public □ Informed Citizens □ Specialists
• Audience Interests: __________________________________
• Audience Concerns: ____________________________________
• Preferred Communication Channels: ___________________

**📝 BLOG POST/ARTICLE DEVELOPMENT:**

**Article Specifications:**
• Target Word Count: 800-1000 words
• Current Word Count: _____ / 1000
• Publication Target: ___________________________________
• Submission Deadline: __________________________________

**Article Structure:**

**HEADLINE (Catchy & Clear):**
_____________________________________________________

**INTRODUCTION (150-200 words):**
*Hook readers and introduce the issue in accessible language*

[DRAFT:]
_____________________________________________________
_____________________________________________________
_____________________________________________________

**MAIN CONTENT SECTION 1 (200-250 words):**
*Present the problem and why it matters to readers*

[DRAFT:]
_____________________________________________________
_____________________________________________________

**MAIN CONTENT SECTION 2 (200-250 words):**
*Share your research findings in plain language*

[DRAFT:]
_____________________________________________________
_____________________________________________________

**MAIN CONTENT SECTION 3 (200-250 words):**
*Present your solution and recommendations*

[DRAFT:]
_____________________________________________________
_____________________________________________________

**CALL TO ACTION (100-150 words):**
*Tell readers what they can do about the issue*

[DRAFT:]
_____________________________________________________
_____________________________________________________

**📱 SOCIAL MEDIA STRATEGY:**

**Platform 1: Instagram**
• Content Type: □ Infographic □ Carousel □ Video □ Story Series
• Key Message: ________________________________________
• Visual Elements: ___________________________________
• Hashtag Strategy: __________________________________
• Target Reach: ____________________________________
• Engagement Goal: __________________________________

**Platform 2: Twitter/X**
• Thread Structure (5-7 tweets):
  1. Hook Tweet: ___________________________________
  2. Problem Statement: ____________________________
  3. Research Insight: _____________________________
  4. Solution Preview: _____________________________
  5. Data/Evidence: _______________________________
  6. Call to Action: ______________________________
  7. Link to Full Article: _________________________

**Platform 3: LinkedIn**
• Professional Angle: ________________________________
• Industry Relevance: _______________________________
• Professional Network Strategy: ____________________
• Article Excerpt: __________________________________

**Platform 4: TikTok/YouTube (Optional)**
• Video Concept: ____________________________________
• Duration: _________________________________________
• Key Points to Cover: ______________________________
• Visual/Audio Elements: ____________________________

**🎯 STAKEHOLDER OUTREACH:**

**Government Officials:**
• Official 1: _______________________________________
  - Position: ____________________________________
  - Email: ______________________________________
  - Pitch Angle: ________________________________
  - Response: □ Positive □ Neutral □ Negative □ No Response

• Official 2: _______________________________________
  - Position: ____________________________________
  - Email: ______________________________________
  - Pitch Angle: ________________________________
  - Response: □ Positive □ Neutral □ Negative □ No Response

**Media Contacts:**
• Journalist 1: ____________________________________
  - Publication: ________________________________
  - Beat/Focus: __________________________________
  - Contact Method: ______________________________
  - Story Pitch: _________________________________

• Journalist 2: ____________________________________
  - Publication: ________________________________
  - Beat/Focus: __________________________________
  - Contact Method: ______________________________
  - Story Pitch: _________________________________

**Community Organizations:**
• Organization 1: ___________________________________
  - Contact Person: _______________________________
  - Collaboration Opportunity: ____________________
  - Mutual Benefits: ______________________________

**📊 IMPACT MEASUREMENT:**

**Publication Metrics:**
• Article Views: ____________________________________
• Shares/Reposts: ___________________________________
• Comments/Engagement: ______________________________
• Media Pickups: ____________________________________

**Social Media Metrics:**
• Total Reach: _____________________________________
• Engagement Rate: __________________________________
• New Followers: ____________________________________
• Click-through to Article: _________________________

**Real-World Impact:**
• Policy Discussion Generated: _______________________
• Community Response: _______________________________
• Stakeholder Feedback: _____________________________
• Follow-up Opportunities: __________________________

**📈 DISSEMINATION TIMELINE:**

**Week 12:** Content Creation
□ Blog post first draft complete
□ Social media content planned
□ Visual materials created

**Week 13:** Review & Refinement
□ Peer review of blog post
□ Social media content tested
□ Stakeholder outreach initiated

**Week 14:** Publication & Promotion
□ Blog post published
□ Social media campaign launched
□ Stakeholder follow-up

**Week 15:** Impact Assessment
□ Metrics collected and analyzed
□ Lessons learned documented
□ Future engagement planned

**🎉 SUCCESS CELEBRATION:**
• Biggest achievement in public engagement: _____________
• Most positive feedback received: ____________________
• Unexpected outcomes: _______________________________
• Skills gained in public communication: ______________
• Future public engagement goals: ____________________
'''
            },
            {
                'title': '📈 TAB 5: Project Management & Timeline',
                'content': '''
**📅 PROJECT TIMELINE & MILESTONE TRACKING:**

**🗓️ WEEKLY SCHEDULE OVERVIEW:**

**Week 2: Project Formation**
□ Team formation and introductions
□ Initial topic brainstorming
□ Template setup and familiarization
□ Communication plan establishment
□ Role assignments
**Due:** Team membership information complete

**Week 3: Topic Selection & Research Question**
□ Finalize project topic
□ Develop initial research question
□ Conduct preliminary research
□ Create research plan
**Due:** Research question draft

**Week 4: Research Strategy**
□ Identify government data sources
□ Plan Access to Information requests
□ Create academic source search strategy
□ Establish source evaluation criteria
**Due:** Research strategy document

**Week 5: Data Collection Phase 1**
□ Begin government data requests
□ Academic literature search
□ Initial source evaluation
□ Create source tracking system
**Due:** 10+ preliminary sources identified

**Week 6: Data Collection Phase 2**
□ Follow up on government requests
□ Expand academic source collection
□ Begin data analysis
□ Identify information gaps
**Due:** Government data request status update

**Week 7: Data Analysis & Synthesis**
□ Analyze collected government data
□ Synthesize academic sources
□ Identify patterns and insights
□ Begin argument development
**Due:** Data analysis summary

**Week 8: Argument Development**
□ Finalize thesis statement
□ Develop main arguments
□ Map evidence to arguments
□ Begin solution brainstorming
**Due:** Thesis and argument outline

**Week 9: Solution Development**
□ Brainstorm innovative solutions
□ Evaluate existing approaches
□ Develop recommended solution
□ Create implementation plan
**Due:** Solution proposal

**Week 10: Paper Writing Phase 1**
□ Write introduction section
□ Begin literature review
□ Create detailed paper outline
□ Establish writing schedule
**Due:** Introduction and outline complete

**Week 11: Paper Writing Phase 2**
□ Complete literature review
□ Write analysis section
□ Develop policy recommendations
□ Begin revision process
**Due:** First complete draft

**Week 12: Paper Revision & Public Content Creation**
□ Peer review and revision
□ Create blog post draft
□ Plan social media strategy
□ Begin stakeholder outreach
**Due:** Revised paper draft, blog post draft

**Week 13: Final Revision & Preparation**
□ Final paper revisions
□ Complete public writing
□ Prepare presentation materials
□ Submit final materials for review
**Due:** Final paper and public content

**Week 14: Presentation & Dissemination**
□ Present to class
□ Publish public content
□ Launch social media campaign
□ Stakeholder engagement
**Due:** Public presentation and content live

**Week 15: Reflection & Assessment**
□ Complete reflective journals
□ Assess project impact
□ Submit final materials
□ Celebrate achievements
**Due:** All final submissions

**📊 PROGRESS TRACKING DASHBOARD:**

**Overall Project Progress:**
• Percentage Complete: _____ / 100%
• On Schedule: □ Yes □ Behind □ Ahead
• Budget Status: □ On Budget □ Over □ Under
• Team Morale: □ High □ Medium □ Low

**Task Completion Status:**
| Week | Main Deliverable | Status | Completion Date |
|------|-----------------|--------|----------------|
| 2 | Team Formation | □ Complete □ In Progress □ Not Started | _____ |
| 3 | Research Question | □ Complete □ In Progress □ Not Started | _____ |
| 4 | Research Strategy | □ Complete □ In Progress □ Not Started | _____ |
| 5 | Data Collection 1 | □ Complete □ In Progress □ Not Started | _____ |
| 6 | Data Collection 2 | □ Complete □ In Progress □ Not Started | _____ |
| 7 | Data Analysis | □ Complete □ In Progress □ Not Started | _____ |
| 8 | Argument Development | □ Complete □ In Progress □ Not Started | _____ |
| 9 | Solution Development | □ Complete □ In Progress □ Not Started | _____ |
| 10 | Writing Phase 1 | □ Complete □ In Progress □ Not Started | _____ |
| 11 | Writing Phase 2 | □ Complete □ In Progress □ Not Started | _____ |
| 12 | Revision & Public Content | □ Complete □ In Progress □ Not Started | _____ |
| 13 | Final Preparation | □ Complete □ In Progress □ Not Started | _____ |
| 14 | Presentation | □ Complete □ In Progress □ Not Started | _____ |
| 15 | Final Submission | □ Complete □ In Progress □ Not Started | _____ |

**⚠️ RISK MANAGEMENT:**

**Identified Risks:**
• Risk 1: __________________________________________
  - Probability: □ High □ Medium □ Low
  - Impact: □ High □ Medium □ Low
  - Mitigation: ___________________________________

• Risk 2: __________________________________________
  - Probability: □ High □ Medium □ Low
  - Impact: □ High □ Medium □ Low
  - Mitigation: ___________________________________

• Risk 3: __________________________________________
  - Probability: □ High □ Medium □ Low
  - Impact: □ High □ Medium □ Low
  - Mitigation: ___________________________________

**📋 QUALITY ASSURANCE:**

**Review Schedule:**
• Week 6 Review: _____ (Date) - Focus: Research Quality
• Week 10 Review: _____ (Date) - Focus: Writing Progress  
• Week 13 Review: _____ (Date) - Focus: Final Quality

**Quality Standards:**
□ All sources properly cited
□ Arguments logically structured
□ Evidence supports conclusions
□ Writing meets academic standards
□ Public content is accessible
□ Timeline requirements met

**🤝 TEAM COORDINATION:**

**Meeting Schedule:**
• Regular meetings: Every _____ at _____
• Location: _____________________________________
• Duration: ____________________________________
• Agenda template: ______________________________

**Communication Protocol:**
• Daily updates via: ____________________________
• File sharing: ________________________________
• Emergency contact: ____________________________
• Conflict resolution process: __________________

**📈 SUCCESS METRICS:**

**Academic Success:**
• Paper quality score: Target _____ / 100
• Individual contribution balance: Target _____ %
• Citation accuracy: Target 100%
• On-time submission: □ Yes

**Public Engagement Success:**
• Blog post views: Target _____
• Social media engagement: Target _____
• Stakeholder responses: Target _____
• Media coverage: □ Yes □ No

**Learning Success:**
• Skill development satisfaction: Target _____ / 10
• Team collaboration rating: Target _____ / 10
• Course objective achievement: Target 100%
'''
            },
            {
                'title': '🔍 TAB 6: Research Methods & Citation',
                'content': '''
**📚 RESEARCH METHODOLOGY FRAMEWORK:**

**🔍 RESEARCH DESIGN:**
• Research Type: □ Exploratory □ Descriptive □ Analytical □ Mixed-Method
• Primary Approach: □ Quantitative □ Qualitative □ Mixed
• Data Collection Methods: □ Secondary Analysis □ Primary Data □ Both
• Analysis Framework: ___________________________________

**📊 DATA COLLECTION STRATEGY:**

**Secondary Data Sources:**
• Academic databases used: _____________________________
• Government databases: _______________________________
• NGO/Organization reports: ___________________________
• News and media sources: _____________________________
• Statistical data sources: ____________________________

**Search Strategy Documentation:**
• Primary keywords: ___________________________________
• Secondary keywords: _________________________________
• Boolean operators used: _____________________________
• Date range: From _____ to _____
• Language restrictions: _____________________________
• Geographic scope: ___________________________________

**Quality Assessment Criteria:**
□ Source credibility and authority
□ Publication date relevance
□ Peer review status (for academic sources)
□ Data methodology transparency
□ Potential bias identification
□ Sample size adequacy (for studies)

**📖 HARVARD REFERENCING GUIDE:**

**Book Reference Format:**
Author, A.A. (Year) Title of book. Place: Publisher.

**Example:**
Smith, J.D. (2023) Digital governance in modern cities. London: Academic Press.

**Journal Article Format:**
Author, A.A. (Year) 'Title of article', Journal Name, vol(issue), pp. xx-xx.

**Example:**
Chen, L.M. (2024) 'Policy implementation challenges in urban planning', Urban Studies Quarterly, 45(2), pp. 123-145.

**Government Document Format:**
Government Department (Year) Title of document. Place: Publisher.

**Example:**
Hong Kong Government (2024) Digital transformation strategy 2024-2027. Hong Kong: Government Printer.

**Website/Online Source Format:**
Author/Organization (Year) 'Title of webpage', Website Name, Available at: URL (Accessed: date).

**Example:**
Census and Statistics Department (2024) 'Population projections for Hong Kong', gov.hk, Available at: https://www.censtatd.gov.hk/population (Accessed: 15 September 2024).

**📝 CITATION TRACKING SYSTEM:**

**Source #1:**
• Type: _______________________________________________
• Author: _____________________________________________
• Title: ______________________________________________
• Publication Details: ________________________________
• Page Numbers Used: ___________________________________
• Key Quote: __________________________________________
• Used In Section: ____________________________________
• Harvard Citation: ___________________________________

[Repeat for each source - aim for 15-20 quality sources]

**🔍 SOURCE EVALUATION FRAMEWORK:**

**Credibility Assessment:**
| Source | Authority | Currency | Accuracy | Purpose | Overall Score |
|--------|-----------|----------|----------|---------|--------------|
| Source 1 | ___/10 | ___/10 | ___/10 | ___/10 | ___/40 |
| Source 2 | ___/10 | ___/10 | ___/10 | ___/10 | ___/40 |
| Source 3 | ___/10 | ___/10 | ___/10 | ___/10 | ___/40 |

**Evaluation Criteria:**
• **Authority (Who?):** Author credentials, institutional affiliation, expertise
• **Currency (When?):** Publication date, information freshness, regular updates
• **Accuracy (What?):** Citations provided, data sources, fact-checking
• **Purpose (Why?):** Objective vs. biased, commercial vs. educational intent

**📊 DATA ANALYSIS METHODS:**

**Quantitative Analysis:**
• Statistical methods used: ____________________________
• Software/tools: ____________________________________
• Data visualization: ________________________________
• Significance testing: ______________________________

**Qualitative Analysis:**
• Thematic analysis approach: _________________________
• Coding framework: ___________________________________
• Pattern identification: ____________________________
• Interpretation methods: _____________________________

**Triangulation Strategy:**
• Method 1: __________________________________________ 
• Method 2: __________________________________________
• Method 3: __________________________________________
• Consistency check: __________________________________

**⚠️ RESEARCH LIMITATIONS:**

**Data Limitations:**
• Availability constraints: ____________________________
• Quality issues: ____________________________________
• Time period restrictions: ____________________________
• Geographic limitations: _____________________________

**Methodological Limitations:**
• Sample size issues: _________________________________
• Selection bias potential: ____________________________
• Measurement challenges: ______________________________
• Generalizability concerns: __________________________

**Resource Limitations:**
• Time constraints: __________________________________
• Access restrictions: ______________________________
• Language barriers: _________________________________
• Cost limitations: _________________________________

**📋 ETHICAL CONSIDERATIONS:**

**Research Ethics:**
□ Proper attribution of all sources
□ No plagiarism or academic dishonesty
□ Respect for intellectual property
□ Balanced representation of viewpoints
□ Transparent about limitations and biases

**Data Use Ethics:**
□ Appropriate use of government data
□ Respect for privacy in public information
□ Acknowledgment of data source limitations
□ Fair representation of findings

**✅ QUALITY ASSURANCE CHECKLIST:**

**Before Submission:**
□ All sources properly cited in Harvard format
□ Reference list alphabetically ordered
□ In-text citations match reference list
□ No missing or incomplete citations
□ Page numbers included where applicable
□ URLs and access dates current and accurate
□ Consistent formatting throughout
□ Spelling and grammar checked
□ Facts and figures verified against original sources
□ Quotes accurately transcribed and cited
□ Paraphrasing properly attributed
□ Balance of source types (academic, government, media, etc.)
□ Recent sources included (within last 5 years where possible)
□ Bias and limitations acknowledged
□ Research methodology clearly documented

**📈 RESEARCH IMPACT ASSESSMENT:**

**Academic Contribution:**
• Original insights generated: ____________________________
• Gaps in literature addressed: __________________________
• Methodological innovations: ____________________________

**Policy Relevance:**
• Policy implications identified: _________________________
• Recommendations practicality: ___________________________
• Stakeholder value: ____________________________________

**Public Value:**
• Community relevance: ___________________________________
• Accessibility of findings: _____________________________
• Social impact potential: ______________________________
'''
            }
        ]
        
        # Add overview and all tabs
        self.add_content_to_tab("TEMPLATE OVERVIEW", overview_content)
        
        for i, tab in enumerate(tabs_content, 1):
            print(f"📝 Adding {tab['title'][:50]}...")
            if not self.add_content_to_tab(tab['title'], tab['content']):
                return False
                
        return True
    
    def run(self):
        """Main execution flow"""
        print("🚀 GCAP3056 Tabbed Template Creator")
        print("=" * 60)
        print("Creating enhanced template with structured tabs and sub-tabs")
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
            
        # Create template structure
        if not self.create_template_structure():
            print("❌ Failed to create template structure")
            return False
            
        # Success message
        print("\n" + "="*60)
        print("🎉 ENHANCED TABBED TEMPLATE CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"📄 Document ID: {self.document_id}")
        print(f"🔗 Access Link: https://docs.google.com/document/d/{self.document_id}/edit")
        print(f"📁 Location: Course folder (ID: {self.folder_id})")
        print("\n📋 Template Structure:")
        print("   📋 TAB 1: Team Membership & Admin")
        print("   📝 TAB 2: Argumentative Research Paper (Main)")
        print("      ├── 📊 SUB-TAB 2.1: Public Sources Collection")
        print("      ├── 🏛️ SUB-TAB 2.2: Government Info (Access to Info)")
        print("      └── 💡 SUB-TAB 2.3: Brainstorming & Solutions")
        print("   📖 TAB 3: Reflection & Journal Writing")
        print("   📢 TAB 4: Public Writing & Dissemination")
        print("   📈 TAB 5: Project Management & Timeline")
        print("   🔍 TAB 6: Research Methods & Citation")
        print("\n✨ Features:")
        print("   • Structured tabs for organized collaboration")
        print("   • Comprehensive 13-week project timeline")
        print("   • Built-in quality assurance checklists")
        print("   • Progress tracking dashboards")
        print("   • Harvard referencing guide")
        print("   • Risk management framework")
        print("   • Public engagement strategy templates")
        print("\n🎯 Ready for student groups to copy and customize!")
        
        return True

def main():
    creator = GCAP3056TabbedTemplateCreator()
    success = creator.run()
    
    if not success:
        print("\n❌ Enhanced template creation failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

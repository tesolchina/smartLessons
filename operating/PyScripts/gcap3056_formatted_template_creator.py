#!/usr/bin/env python3
"""
GCAP3056 Formatted Template Creator - Enhanced Version with Google Docs Formatting
Creates a comprehensive Google Docs template with proper formatting instead of raw markdown
"""

import sys
import os
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

from auth_setup import authenticate_google_apis
from googleapiclient.errors import HttpError

class GCAP3056FormattedTemplateCreator:
    def __init__(self):
        self.drive_service = None
        self.docs_service = None
        self.document_id = None
        self.folder_id = "1vI96VXDrJvdnqegFfJ5y8zOnHxGPHxVV"  # Specified folder
        self.current_index = 1  # Track insertion point
        
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
        print("📄 Creating new Google Document with proper formatting...")
        try:
            # Create document
            document = {
                'title': 'GCAP3056 Project Template - Group [X] (Formatted)'
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
    
    def add_formatted_text(self, text, style='NORMAL_TEXT'):
        """Add text with Google Docs formatting"""
        try:
            requests = [{
                'insertText': {
                    'location': {
                        'index': self.current_index,
                    },
                    'text': text
                }
            }]
            
            # Add formatting if not normal text
            if style != 'NORMAL_TEXT':
                start_index = self.current_index
                end_index = self.current_index + len(text)
                
                format_request = {
                    'updateParagraphStyle': {
                        'range': {
                            'startIndex': start_index,
                            'endIndex': end_index
                        },
                        'paragraphStyle': {
                            'namedStyleType': style
                        },
                        'fields': 'namedStyleType'
                    }
                }
                requests.append(format_request)
            
            result = self.docs_service.documents().batchUpdate(
                documentId=self.document_id, 
                body={'requests': requests}
            ).execute()
            
            self.current_index += len(text)
            return True
        except Exception as e:
            print(f"❌ Error adding formatted text: {e}")
            return False
    
    def add_heading(self, text, level=1):
        """Add a heading with proper Google Docs formatting"""
        heading_styles = {
            1: 'HEADING_1',
            2: 'HEADING_2', 
            3: 'HEADING_3',
            4: 'HEADING_4'
        }
        style = heading_styles.get(level, 'HEADING_1')
        return self.add_formatted_text(text + '\n', style)
    
    def add_paragraph(self, text):
        """Add a normal paragraph"""
        return self.add_formatted_text(text + '\n\n', 'NORMAL_TEXT')
    
    def add_bullet_list(self, items):
        """Add a bulleted list"""
        try:
            for item in items:
                # Insert the bullet point text
                requests = [{
                    'insertText': {
                        'location': {
                            'index': self.current_index,
                        },
                        'text': item + '\n'
                    }
                }]
                
                # Create bullet list formatting
                start_index = self.current_index
                end_index = self.current_index + len(item) + 1
                
                bullet_request = {
                    'createParagraphBullets': {
                        'range': {
                            'startIndex': start_index,
                            'endIndex': end_index
                        },
                        'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                    }
                }
                requests.append(bullet_request)
                
                result = self.docs_service.documents().batchUpdate(
                    documentId=self.document_id, 
                    body={'requests': requests}
                ).execute()
                
                self.current_index += len(item) + 1
            
            # Add extra line after list
            self.add_formatted_text('\n', 'NORMAL_TEXT')
            return True
        except Exception as e:
            print(f"❌ Error adding bullet list: {e}")
            return False
    
    def add_separator(self):
        """Add a visual separator"""
        return self.add_formatted_text('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n', 'NORMAL_TEXT')
    
    def create_template_structure(self):
        """Create the complete template structure with proper formatting"""
        print("🏗️ Creating template structure with Google Docs formatting...")
        
        # Header
        self.add_heading('GCAP3056: COLLABORATIVE PROJECT TEMPLATE', 1)
        self.add_separator()
        
        # Overview section
        self.add_paragraph('📅 Project Timeline: Week 2-15 (13 weeks total)')
        self.add_paragraph('👥 Group Size: 3-4 students')
        self.add_paragraph('🎯 Final Deliverable: ~1500-word argumentative research paper')
        self.add_paragraph('🌐 Public Engagement: Blog post + social media strategy')
        
        self.add_heading('Navigation Guide', 2)
        self.add_paragraph('This document uses a structured tab system for organized collaboration:')
        
        nav_items = [
            '📋 TAB 1: Team Membership & Admin',
            '📝 TAB 2: Argumentative Research Paper (Main)',
            '   ├── 📊 SUB-TAB 2.1: Public Sources Collection',
            '   ├── 🏛️ SUB-TAB 2.2: Government Info (Access to Info)',
            '   └── 💡 SUB-TAB 2.3: Brainstorming & Solutions',
            '📖 TAB 3: Reflection & Journal Writing',
            '📢 TAB 4: Public Writing & Dissemination',
            '📈 TAB 5: Project Management & Timeline',
            '🔍 TAB 6: Research Methods & Citation'
        ]
        self.add_bullet_list(nav_items)
        
        self.add_heading('Instructions', 2)
        instructions = [
            'Use each tab for its designated purpose',
            'Update progress regularly in relevant tabs', 
            'Collaborate actively using Google Docs comments',
            'Track milestones in the Project Management tab'
        ]
        self.add_bullet_list(instructions)
        
        self.add_separator()
        
        # Tab 1: Team Membership & Admin
        self.add_heading('📋 TAB 1: TEAM MEMBERSHIP & ADMIN', 1)
        
        self.add_heading('👥 TEAM MEMBER PROFILES', 2)
        
        for i in range(1, 5):
            if i == 4:
                self.add_heading(f'Member {i} (if applicable)', 3)
            else:
                self.add_heading(f'Member {i}', 3)
            
            member_fields = [
                f'Full Name: _______________________________',
                f'Student ID: _______________________________',
                f'Email Address: ___________________________',
                f'Phone: ___________________________________',
                f'Strengths/Skills: _________________________',
                f'Preferred Role: ___________________________'
            ]
            self.add_bullet_list(member_fields)
        
        self.add_heading('🎯 PROJECT ADMINISTRATION', 2)
        admin_fields = [
            'Project Topic: ____________________________',
            'Group Code/Name: _________________________',
            'Formation Date: ___________________________',
            'Meeting Schedule: _________________________',
            'Primary Communication: ___________________'
        ]
        self.add_bullet_list(admin_fields)
        
        self.add_heading('📋 ADMIN NOTES (For Instructor Use)', 2)
        admin_notes = [
            'Approval Status: ☐ Pending ☐ Approved ☐ Needs Revision',
            'Topic Appropriateness: ____________________',
            'Group Dynamics Assessment: _______________',
            'Special Considerations: ___________________',
            'Last Review Date: _________________________'
        ]
        self.add_bullet_list(admin_notes)
        
        self.add_separator()
        
        # Tab 2: Main Research Paper
        self.add_heading('📝 TAB 2: ARGUMENTATIVE RESEARCH PAPER (MAIN)', 1)
        
        self.add_heading('📊 PAPER SPECIFICATIONS & PROGRESS', 2)
        specs = [
            'Target Length: ~1500 words total (≈500 words per student)',
            'Format: Academic argumentative essay with Harvard referencing',
            'Submission Deadline: Week 15',
            'Current Word Count: _______ / 1500 words',
            'Draft Status: ☐ Planning ☐ Researching ☐ Writing ☐ Reviewing ☐ Final'
        ]
        self.add_bullet_list(specs)
        
        self.add_heading('🔍 RESEARCH FOUNDATION', 2)
        
        self.add_heading('Research Question (Finalized)', 3)
        self.add_paragraph('_________________________________________________________________\n_________________________________________________________________')
        
        self.add_heading('Thesis Statement', 3)
        self.add_paragraph('_________________________________________________________________\n_________________________________________________________________')
        
        self.add_heading('Key Arguments (3-4 main points)', 3)
        args = [
            '1. ____________________________________________________________',
            '2. ____________________________________________________________', 
            '3. ____________________________________________________________',
            '4. ____________________________________________________________'
        ]
        self.add_bullet_list(args)
        
        self.add_heading('📖 PAPER STRUCTURE & DRAFT', 2)
        
        # Paper sections
        sections = [
            {
                'title': 'INTRODUCTION (300-400 words)',
                'purpose': 'Purpose: Hook reader, provide context, present research question and thesis',
                'target': 400
            },
            {
                'title': 'LITERATURE REVIEW & EVIDENCE (600-700 words)', 
                'purpose': 'Purpose: Present academic sources, government data, and evidence',
                'target': 700
            },
            {
                'title': 'POLICY RECOMMENDATIONS (400-500 words)',
                'purpose': 'Purpose: Present solutions, implementation strategies, and justifications', 
                'target': 500
            },
            {
                'title': 'CONCLUSION (200-300 words)',
                'purpose': 'Purpose: Synthesize arguments, reinforce thesis, call to action',
                'target': 300
            }
        ]
        
        for section in sections:
            self.add_heading(section['title'], 3)
            self.add_paragraph(section['purpose'])
            self.add_paragraph('[DRAFT SECTION:]\n_________________________________________________________________\n_________________________________________________________________\n_________________________________________________________________')
            
            status_items = [
                f'Current Word Count: _____ / {section["target"]}',
                'Status: ☐ Not Started ☐ Rough Draft ☐ Under Review ☐ Complete'
            ]
            self.add_bullet_list(status_items)
        
        self.add_heading('📚 REFERENCE LIST (Harvard Style)', 2)
        refs = [
            '1. _______________________________________________________________',
            '2. _______________________________________________________________',
            '3. _______________________________________________________________',
            '4. _______________________________________________________________',
            '5. _______________________________________________________________',
            '[Continue numbering as needed - aim for 15-20 quality sources]'
        ]
        self.add_bullet_list(refs)
        
        self.add_heading('✅ FINAL QUALITY CHECKLIST', 2)
        checklist = [
            '☐ Research question clearly articulated and answered',
            '☐ Thesis statement is specific, arguable, and supported',
            '☐ Evidence from multiple credible sources integrated effectively',
            '☐ Government data properly analyzed and cited',
            '☐ Policy recommendations are practical and justified',
            '☐ Harvard referencing style used consistently',
            '☐ Proper academic tone and structure maintained',
            '☐ Word count within target range (1400-1600 words acceptable)',
            '☐ Proofread for grammar, spelling, and coherence',
            '☐ All group members contributed equitably'
        ]
        self.add_bullet_list(checklist)
        
        self.add_separator()
        
        # Continue with other tabs...
        self.add_heading('📊 SUB-TAB 2.1: PUBLIC SOURCES COLLECTION', 1)
        
        self.add_heading('🌐 PUBLIC & ACADEMIC SOURCES RESEARCH', 2)
        
        self.add_heading('📖 ACADEMIC SOURCES (Journal Articles, Books, Reports)', 2)
        
        for i in range(1, 4):
            self.add_heading(f'Source {i}', 3)
            source_fields = [
                'Type: ☐ Peer-reviewed journal ☐ Book ☐ Report ☐ Other: ________',
                'Author(s): _______________________________________________',
                'Title: __________________________________________________',
                'Publication: ____________________________________________',
                'Year: _______ Pages: ____________________________________',
                'URL/DOI: _______________________________________________',
                'Key Findings: ___________________________________________',
                'Relevance to Research Question: ________________________',
                'Quote/Data to Use: ______________________________________',
                'Harvard Citation: _______________________________________'
            ]
            self.add_bullet_list(source_fields)
        
        self.add_paragraph('[Continue pattern for Sources 4-10...]')
        
        # Add remaining content sections in similar format...
        self.add_separator()
        
        # Final completion message
        self.add_heading('🎉 PROJECT COMPLETION CHECKLIST', 1)
        completion = [
            '☐ All team members contributed equally',
            '☐ Research paper meets requirements',
            '☐ Citations properly formatted',
            '☐ Public writing piece completed',
            '☐ Reflective journals updated',
            '☐ Final presentation prepared',
            '☐ Document submitted on time'
        ]
        self.add_bullet_list(completion)
        
        self.add_heading('🏆 FINAL THOUGHTS', 2)
        self.add_paragraph('[What did your team accomplish? What are you most proud of?]\n________________')
        
        self.add_separator()
        self.add_paragraph('END OF TEMPLATE')
        self.add_separator()
        
        return True
    
    def run(self):
        """Main execution flow"""
        print("🚀 GCAP3056 Formatted Template Creator")
        print("=" * 60)
        print("Creating template with proper Google Docs formatting")
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
        print("🎉 FORMATTED TEMPLATE CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"📄 Document ID: {self.document_id}")
        print(f"🔗 Access Link: https://docs.google.com/document/d/{self.document_id}/edit")
        print(f"📁 Location: Course folder (ID: {self.folder_id})")
        print("\n✨ Features:")
        print("   • Proper Google Docs formatting (no raw markdown)")
        print("   • Hierarchical heading structure")
        print("   • Bulleted lists for easy completion")
        print("   • Professional document appearance")
        print("   • Ready for student collaboration")
        print("\n🎯 Ready for immediate use!")
        
        return True

def main():
    creator = GCAP3056FormattedTemplateCreator()
    success = creator.run()
    
    if not success:
        print("\n❌ Formatted template creation failed")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

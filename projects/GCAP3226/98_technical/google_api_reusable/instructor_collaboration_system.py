#!/usr/bin/env python3
"""
Instructor Collaboration System for GCAP3226
Creates a shared Google Doc for instructor notes and automates updates to team folders
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from google_api_client import GoogleAPIClient

class InstructorCollaborationManager:
    def __init__(self):
        """Initialize the instructor collaboration manager"""
        self.client = GoogleAPIClient()
        self.drive_service = self.client.get_drive_service()
        self.docs_service = self.client.get_docs_service()
        self.sheets_service = self.client.get_sheets_service()
        
        # Instructor email addresses
        self.instructors = {
            'simon': 'simonwang@hkbu.edu.hk',
            'talia': 'taliawu@hkbu.edu.hk'  # Replace with actual email
        }
        
        # Team data
        self.teams = {
            'Team_1': {
                'folder_id': '1zGDV77Vih4DxDyH9f6eKnr00Kp4nWyMo',
                'topic': 'Topic 6 - Flu Shot Participation Analysis',
                'members': ['Yeung Wing Yu', 'Kwok Tsz Yau', 'Tsoi Yik Hon', 'SuJiaLu']
            },
            'Team_2': {
                'folder_id': '1KJ8Y1QkDHo7Oull02GdfjP-OO0ZxJS3C',
                'topic': 'Topic 3 - Inter-Company Bus Route Coordination',
                'members': ['Chan Hei Tung', 'Yip Tsz Ying', 'Ko Man Wai', 'Wong Ling Yan Cassy', 'Tsoi Tsz Yan', 'Zi Xing Saul Ma']
            },
            'Team_3': {
                'folder_id': '1Gx9TD1fRxuzNinEIgLMdvC-pTALbf8fD',
                'topic': 'Topic 7 - Typhoon Signal Data Analysis',
                'members': ['Chen Man Ching', 'Hui Man Hei', 'HONG KAM YIN', 'Kung Tsz Lok', 'ZHENG ZIAN', 'Chan Ching Yin']
            },
            'Team_4': {
                'folder_id': '1yYR-KxSfSI3VT4M2yLbIbj4pVEHTS__f',
                'topic': 'Topic 4 - Municipal Solid Waste Charging Scheme',
                'members': ['Liu Wai Man', 'Kwok Lai Ki', 'Chan Tsz Ying', 'Wong Wai Lun']
            },
            'Team_5': {
                'folder_id': '1vgf2jvKYNJu9EO2eD8S_sOOvWSIVL_Dw',
                'topic': 'Topic 5 - Green@Community Recycling Network Analysis',
                'members': ['MAN Wai Yin', 'Chan Chi Ki', 'Tag Tsz Tung', 'HO Chun Chit', 'Xu Jingyi', 'Cheung Kwun Ho']
            },
            'Team_6': {
                'folder_id': '1WlruCUvqQ1IO5EOmYbUX0B4vMjF-zCNo',
                'topic': 'Topic 2 - Bus Stop Merger Optimization',
                'members': ['Tam Tin Chun', 'Chan Dik On', 'Wong Chun Hang']
            }
        }
        
        self.results = {
            'instructor_doc_created': None,
            'team_notes_updated': [],
            'errors': []
        }

    def create_instructor_collaboration_doc(self):
        """Create a shared Google Doc for instructor notes"""
        print("📄 Creating instructor collaboration document...")
        
        try:
            # Create the document
            doc_title = f"GCAP3226 Instructor Notes - {datetime.now().strftime('%Y-%m-%d')}"
            
            document = {
                'title': doc_title
            }
            
            created_doc = self.docs_service.documents().create(body=document).execute()
            doc_id = created_doc['documentId']
            
            # Create the initial content structure
            content = self._generate_instructor_doc_content()
            
            # Insert content into the document
            requests = []
            
            # Insert title and structure
            requests.append({
                'insertText': {
                    'location': {'index': 1},
                    'text': content
                }
            })
            
            # Apply formatting
            requests.extend(self._generate_formatting_requests())
            
            # Execute batch update
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            # Share with instructors
            for instructor_name, email in self.instructors.items():
                permission = {
                    'type': 'user',
                    'role': 'writer',
                    'emailAddress': email
                }
                
                self.drive_service.permissions().create(
                    fileId=doc_id,
                    body=permission,
                    sendNotificationEmail=True,
                    emailMessage=f"Shared GCAP3226 instructor collaboration document for team project notes."
                ).execute()
            
            # Store in main project folder
            main_folder_id = '15TA_J0fV-YitdSAnF1vKI96wUQ-MP7EO'
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=main_folder_id,
                removeParents='root'
            ).execute()
            
            doc_url = f"https://docs.google.com/document/d/{doc_id}"
            
            self.results['instructor_doc_created'] = {
                'title': doc_title,
                'doc_id': doc_id,
                'url': doc_url
            }
            
            print(f"✅ Created instructor collaboration document: {doc_title}")
            print(f"🔗 URL: {doc_url}")
            
            return doc_id
            
        except Exception as e:
            error_msg = f"Error creating instructor collaboration document: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['errors'].append(error_msg)
            return None

    def _generate_instructor_doc_content(self):
        """Generate the content structure for the instructor collaboration document"""
        content = f"""GCAP3226 Team Project Instructor Notes
Generated: {datetime.now().strftime('%B %d, %Y')}
Instructors: Dr. Simon Wang, Dr. Talia Wu

=== INSTRUCTIONS ===
This document is for instructor collaboration on team project notes and feedback.

HOW TO USE:
1. Add notes, observations, and feedback for each team in their respective sections
2. Use the UPDATE button (when created) to automatically sync notes to team folders
3. Date stamp your entries for tracking
4. Use different colors or comments for different types of feedback

SECTIONS:
- Team Progress Notes
- Individual Team Sections (6 teams)
- Action Items and Follow-ups
- General Course Observations

==========================================

TEAM PROGRESS OVERVIEW
Last Updated: {datetime.now().strftime('%B %d, %Y')}

Quick Status Check:
□ Team 1 (Flu Shot) - Status: [Add notes here]
□ Team 2 (Bus Routes) - Status: [Add notes here] 
□ Team 3 (Typhoon) - Status: [Add notes here]
□ Team 4 (Waste) - Status: [Add notes here]
□ Team 5 (Recycling) - Status: [Add notes here]
□ Team 6 (Bus Stops) - Status: [Add notes here]

==========================================

"""
        
        # Add sections for each team
        for team_name, team_data in self.teams.items():
            content += f"""
{team_name.upper()} - {team_data['topic']}
Members: {', '.join(team_data['members'])}
Folder: https://drive.google.com/drive/folders/{team_data['folder_id']}

PROGRESS NOTES:
[Add team progress observations here]

FEEDBACK TO SHARE:
[Add feedback that should be shared with the team]

PRIVATE INSTRUCTOR NOTES:
[Add internal notes, concerns, or observations]

ACTION ITEMS:
[Add specific follow-up actions needed]

LAST UPDATED: {datetime.now().strftime('%Y-%m-%d')} by: [Instructor name]

---

"""
        
        content += """
GENERAL COURSE OBSERVATIONS
==========================================

SUCCESSFUL PRACTICES:
[Note what's working well across teams]

COMMON CHALLENGES:
[Note patterns of difficulty across teams]

COURSE ADJUSTMENTS NEEDED:
[Note any course content or structure changes]

RESOURCE NEEDS:
[Note additional resources or support needed]

==========================================

ACTION ITEMS FOR INSTRUCTORS
□ [Add action items here]
□ [Date stamp completed items]

NEXT REVIEW DATE: [Set next collaborative review date]
"""
        
        return content

    def _generate_formatting_requests(self):
        """Generate formatting requests for the document"""
        # This is a simplified version - you can expand with more detailed formatting
        return [
            # Add basic formatting like bold headers, etc.
            # Due to complexity of Google Docs API formatting, keeping this simple for now
        ]

    def create_team_update_system(self):
        """Create a system to sync instructor notes to team folders"""
        print("⚙️ Setting up team update system...")
        
        try:
            # Create a simple tracking spreadsheet for update management
            spreadsheet_title = "GCAP3226 Instructor Notes - Update Tracker"
            
            spreadsheet = {
                'properties': {
                    'title': spreadsheet_title
                }
            }
            
            created_spreadsheet = self.sheets_service.spreadsheets().create(
                body=spreadsheet
            ).execute()
            
            spreadsheet_id = created_spreadsheet['spreadsheetId']
            
            # Set up the tracking sheet
            tracking_data = [
                ['Team', 'Last Note Update', 'Last Sync to Folder', 'Status', 'Notes'],
                ['Team_1', datetime.now().strftime('%Y-%m-%d'), 'Pending', 'Ready', 'Initial setup'],
                ['Team_2', datetime.now().strftime('%Y-%m-%d'), 'Pending', 'Ready', 'Initial setup'],
                ['Team_3', datetime.now().strftime('%Y-%m-%d'), 'Pending', 'Ready', 'Initial setup'],
                ['Team_4', datetime.now().strftime('%Y-%m-%d'), 'Pending', 'Ready', 'Initial setup'],
                ['Team_5', datetime.now().strftime('%Y-%m-%d'), 'Pending', 'Ready', 'Initial setup'],
                ['Team_6', datetime.now().strftime('%Y-%m-%d'), 'Pending', 'Ready', 'Initial setup'],
            ]
            
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Sheet1!A1',
                valueInputOption='RAW',
                body={'values': tracking_data}
            ).execute()
            
            # Share with instructors
            for instructor_name, email in self.instructors.items():
                permission = {
                    'type': 'user',
                    'role': 'writer',
                    'emailAddress': email
                }
                
                self.drive_service.permissions().create(
                    fileId=spreadsheet_id,
                    body=permission
                ).execute()
            
            print(f"✅ Created update tracking system")
            return spreadsheet_id
            
        except Exception as e:
            error_msg = f"Error creating team update system: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['errors'].append(error_msg)
            return None

    def sync_notes_to_team_folders(self, instructor_doc_id):
        """Sync notes from instructor document to individual team folders"""
        print("🔄 Syncing instructor notes to team folders...")
        
        if not instructor_doc_id:
            print("❌ No instructor document ID provided")
            return
        
        try:
            # Read the instructor document
            doc = self.docs_service.documents().get(documentId=instructor_doc_id).execute()
            doc_content = doc.get('body', {}).get('content', [])
            
            # Extract text content
            full_text = ""
            for element in doc_content:
                if 'paragraph' in element:
                    paragraph = element['paragraph']
                    for text_element in paragraph.get('elements', []):
                        if 'textRun' in text_element:
                            full_text += text_element['textRun']['content']
            
            # For each team, create/update their instructor notes document
            for team_name, team_data in self.teams.items():
                self._update_team_notes(team_name, team_data, full_text)
            
        except Exception as e:
            error_msg = f"Error syncing notes to team folders: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['errors'].append(error_msg)

    def _update_team_notes(self, team_name, team_data, instructor_content):
        """Update or create notes document in a specific team folder"""
        try:
            # Extract team-specific content from instructor notes
            team_section = self._extract_team_section(team_name, instructor_content)
            
            if not team_section:
                print(f"⚠️ No notes found for {team_name}")
                return
            
            # Create team-specific instructor notes document
            doc_title = f"Instructor Notes - {team_name}"
            
            # Check if document already exists
            existing_doc_id = self._find_existing_team_notes_doc(team_data['folder_id'], doc_title)
            
            if existing_doc_id:
                # Update existing document
                self._update_existing_team_doc(existing_doc_id, team_section, team_name)
            else:
                # Create new document
                self._create_new_team_doc(team_data['folder_id'], doc_title, team_section, team_name)
            
            self.results['team_notes_updated'].append({
                'team': team_name,
                'action': 'updated' if existing_doc_id else 'created',
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            error_msg = f"Error updating notes for {team_name}: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['errors'].append(error_msg)

    def _extract_team_section(self, team_name, full_content):
        """Extract team-specific section from instructor notes"""
        # Simple extraction based on team name headers
        team_upper = team_name.upper()
        
        # Find the start of the team section
        start_marker = f"{team_upper} -"
        end_marker = "---"
        
        start_index = full_content.find(start_marker)
        if start_index == -1:
            return None
        
        end_index = full_content.find(end_marker, start_index)
        if end_index == -1:
            # Take until the next team section or end of document
            next_team_index = full_content.find("TEAM_", start_index + 1)
            end_index = next_team_index if next_team_index != -1 else len(full_content)
        
        return full_content[start_index:end_index].strip()

    def _find_existing_team_notes_doc(self, folder_id, doc_title):
        """Check if team notes document already exists"""
        try:
            query = f"parents in '{folder_id}' and name = '{doc_title}'"
            results = self.drive_service.files().list(
                q=query,
                fields="files(id, name)"
            ).execute()
            
            files = results.get('files', [])
            return files[0]['id'] if files else None
            
        except Exception:
            return None

    def _update_existing_team_doc(self, doc_id, content, team_name):
        """Update existing team notes document"""
        # Clear document and add new content
        doc = self.docs_service.documents().get(documentId=doc_id).execute()
        doc_length = len(doc['body']['content'])
        
        requests = [
            {
                'deleteContentRange': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': doc_length - 1
                    }
                }
            },
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': f"Instructor Notes for {team_name}\nLast Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{content}"
                }
            }
        ]
        
        self.docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()
        
        print(f"✅ Updated existing notes for {team_name}")

    def _create_new_team_doc(self, folder_id, doc_title, content, team_name):
        """Create new team notes document"""
        document = {
            'title': doc_title
        }
        
        created_doc = self.docs_service.documents().create(body=document).execute()
        doc_id = created_doc['documentId']
        
        # Add content
        requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': f"Instructor Notes for {team_name}\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{content}"
                }
            }
        ]
        
        self.docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()
        
        # Move to team folder
        self.drive_service.files().update(
            fileId=doc_id,
            addParents=folder_id,
            removeParents='root'
        ).execute()
        
        print(f"✅ Created new notes document for {team_name}")

    def generate_report(self):
        """Generate a summary report of the collaboration system setup"""
        print("\n📋 Generating collaboration system report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'instructor_doc': self.results['instructor_doc_created'],
            'team_updates': self.results['team_notes_updated'],
            'errors': self.results['errors'],
            'summary': {
                'teams_updated': len(self.results['team_notes_updated']),
                'errors_count': len(self.results['errors']),
                'system_ready': self.results['instructor_doc_created'] is not None
            }
        }
        
        # Save report
        report_file = current_dir / 'instructor_collaboration_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {report_file}")
        
        # Display summary
        print("\n" + "="*60)
        print("📊 INSTRUCTOR COLLABORATION SYSTEM REPORT")
        print("="*60)
        
        if self.results['instructor_doc_created']:
            print(f"✅ Instructor collaboration document created")
            print(f"🔗 URL: {self.results['instructor_doc_created']['url']}")
        else:
            print("❌ Failed to create instructor collaboration document")
        
        print(f"✅ Team updates: {len(self.results['team_notes_updated'])}")
        print(f"❌ Errors: {len(self.results['errors'])}")
        
        if self.results['errors']:
            print("\n⚠️ Errors encountered:")
            for error in self.results['errors']:
                print(f"   - {error}")

    def run_setup(self):
        """Execute the complete instructor collaboration system setup"""
        print("🚀 Setting up GCAP3226 Instructor Collaboration System")
        print("="*60)
        
        # Step 1: Create instructor collaboration document
        instructor_doc_id = self.create_instructor_collaboration_doc()
        
        # Step 2: Create update tracking system
        self.create_team_update_system()
        
        # Step 3: Generate report
        self.generate_report()
        
        print("\n🎉 Instructor collaboration system setup completed!")
        
        if instructor_doc_id:
            print(f"\n📋 Next Steps:")
            print(f"1. Access the collaboration document: {self.results['instructor_doc_created']['url']}")
            print(f"2. Add notes and observations for each team")
            print(f"3. Run sync command to update team folders")
            print(f"4. Use tracking spreadsheet to monitor updates")

def main():
    """Main execution function"""
    try:
        manager = InstructorCollaborationManager()
        manager.run_setup()
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
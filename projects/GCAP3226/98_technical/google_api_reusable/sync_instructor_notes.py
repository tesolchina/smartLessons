#!/usr/bin/env python3
"""
Sync Instructor Notes to Team Folders
Reads the instructor collaboration document and updates team-specific notes
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import argparse

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from google_api_client import GoogleAPIClient

class NoteSyncManager:
    def __init__(self, instructor_doc_id=None):
        """Initialize the note sync manager"""
        self.client = GoogleAPIClient()
        self.drive_service = self.client.get_drive_service()
        self.docs_service = self.client.get_docs_service()
        
        self.instructor_doc_id = instructor_doc_id
        
        # Team data
        self.teams = {
            'Team_1': {
                'folder_id': '1zGDV77Vih4DxDyH9f6eKnr00Kp4nWyMo',
                'topic': 'Topic 6 - Flu Shot Participation Analysis',
            },
            'Team_2': {
                'folder_id': '1KJ8Y1QkDHo7Oull02GdfjP-OO0ZxJS3C',
                'topic': 'Topic 3 - Inter-Company Bus Route Coordination',
            },
            'Team_3': {
                'folder_id': '1Gx9TD1fRxuzNinEIgLMdvC-pTALbf8fD',
                'topic': 'Topic 7 - Typhoon Signal Data Analysis',
            },
            'Team_4': {
                'folder_id': '1yYR-KxSfSI3VT4M2yLbIbj4pVEHTS__f',
                'topic': 'Topic 4 - Municipal Solid Waste Charging Scheme',
            },
            'Team_5': {
                'folder_id': '1vgf2jvKYNJu9EO2eD8S_sOOvWSIVL_Dw',
                'topic': 'Topic 5 - Green@Community Recycling Network Analysis',
            },
            'Team_6': {
                'folder_id': '1WlruCUvqQ1IO5EOmYbUX0B4vMjF-zCNo',
                'topic': 'Topic 2 - Bus Stop Merger Optimization',
            }
        }
        
        self.sync_results = {
            'teams_synced': [],
            'errors': [],
            'timestamp': datetime.now().isoformat()
        }

    def find_instructor_doc(self):
        """Find the most recent instructor collaboration document"""
        if self.instructor_doc_id:
            return self.instructor_doc_id
        
        try:
            # Search for instructor collaboration documents
            query = "name contains 'GCAP3226 Instructor Notes'"
            results = self.drive_service.files().list(
                q=query,
                orderBy="modifiedTime desc",
                fields="files(id, name, modifiedTime)"
            ).execute()
            
            files = results.get('files', [])
            if files:
                latest_doc = files[0]
                print(f"📄 Found instructor document: {latest_doc['name']}")
                return latest_doc['id']
            else:
                print("❌ No instructor collaboration document found")
                return None
                
        except Exception as e:
            print(f"❌ Error finding instructor document: {str(e)}")
            return None

    def read_instructor_notes(self, doc_id):
        """Read content from the instructor collaboration document"""
        try:
            print(f"📖 Reading instructor notes from document...")
            
            doc = self.docs_service.documents().get(documentId=doc_id).execute()
            doc_content = doc.get('body', {}).get('content', [])
            
            # Extract text content
            full_text = ""
            for element in doc_content:
                if 'paragraph' in element:
                    paragraph = element['paragraph']
                    for text_element in paragraph.get('elements', []):
                        if 'textRun' in text_element:
                            full_text += text_element['textRun']['content']
            
            print(f"✅ Read {len(full_text)} characters from instructor document")
            return full_text
            
        except Exception as e:
            error_msg = f"Error reading instructor document: {str(e)}"
            print(f"❌ {error_msg}")
            self.sync_results['errors'].append(error_msg)
            return None

    def extract_team_notes(self, full_content):
        """Extract notes for each team from the instructor document"""
        team_notes = {}
        
        for team_name in self.teams.keys():
            try:
                team_section = self._extract_team_section(team_name, full_content)
                if team_section:
                    team_notes[team_name] = team_section
                    print(f"✅ Extracted notes for {team_name}")
                else:
                    print(f"⚠️ No notes found for {team_name}")
                    
            except Exception as e:
                error_msg = f"Error extracting notes for {team_name}: {str(e)}"
                print(f"❌ {error_msg}")
                self.sync_results['errors'].append(error_msg)
        
        return team_notes

    def _extract_team_section(self, team_name, full_content):
        """Extract team-specific section from instructor notes"""
        # Look for team section markers
        team_upper = team_name.upper()
        
        # Find the start of the team section
        start_patterns = [
            f"{team_upper} -",
            f"{team_name.upper()} -",
            f"=== {team_upper} ===",
            f"## {team_upper}"
        ]
        
        start_index = -1
        for pattern in start_patterns:
            start_index = full_content.find(pattern)
            if start_index != -1:
                break
        
        if start_index == -1:
            return None
        
        # Find the end of the section
        end_patterns = [
            "---",
            f"TEAM_{int(team_name.split('_')[1]) + 1}",
            "GENERAL COURSE OBSERVATIONS",
            "ACTION ITEMS FOR INSTRUCTORS"
        ]
        
        end_index = len(full_content)
        for pattern in end_patterns:
            temp_end = full_content.find(pattern, start_index + 1)
            if temp_end != -1:
                end_index = min(end_index, temp_end)
        
        section_content = full_content[start_index:end_index].strip()
        
        # Clean up the section
        lines = section_content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('---'):
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines) if cleaned_lines else None

    def sync_team_folder(self, team_name, team_notes):
        """Sync notes to a specific team folder"""
        try:
            team_data = self.teams[team_name]
            folder_id = team_data['folder_id']
            
            print(f"🔄 Syncing notes for {team_name}...")
            
            # Create or update team notes document
            doc_title = f"Instructor_Notes_for_{team_name}"
            
            # Check if document already exists
            existing_doc_id = self._find_existing_team_doc(folder_id, doc_title)
            
            if existing_doc_id:
                self._update_team_doc(existing_doc_id, team_notes, team_name)
                action = "updated"
            else:
                self._create_team_doc(folder_id, doc_title, team_notes, team_name)
                action = "created"
            
            # Also update the team's README if it exists
            self._update_team_readme(folder_id, team_notes, team_name)
            
            self.sync_results['teams_synced'].append({
                'team': team_name,
                'action': action,
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"✅ {action.capitalize()} notes for {team_name}")
            
        except Exception as e:
            error_msg = f"Error syncing {team_name}: {str(e)}"
            print(f"❌ {error_msg}")
            self.sync_results['errors'].append(error_msg)

    def _find_existing_team_doc(self, folder_id, doc_title):
        """Find existing team notes document"""
        try:
            query = f"parents in '{folder_id}' and name contains 'Instructor_Notes'"
            results = self.drive_service.files().list(
                q=query,
                fields="files(id, name)"
            ).execute()
            
            files = results.get('files', [])
            return files[0]['id'] if files else None
            
        except Exception:
            return None

    def _create_team_doc(self, folder_id, doc_title, team_notes, team_name):
        """Create new team notes document"""
        document = {
            'title': doc_title
        }
        
        created_doc = self.docs_service.documents().create(body=document).execute()
        doc_id = created_doc['documentId']
        
        # Format content for team document
        formatted_content = self._format_team_content(team_notes, team_name)
        
        # Add content
        requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': formatted_content
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

    def _update_team_doc(self, doc_id, team_notes, team_name):
        """Update existing team notes document"""
        # Get current document length
        doc = self.docs_service.documents().get(documentId=doc_id).execute()
        content = doc.get('body', {}).get('content', [])
        
        # Calculate document length
        doc_length = 1
        for element in content:
            if 'paragraph' in element:
                for text_element in element['paragraph'].get('elements', []):
                    if 'textRun' in text_element:
                        doc_length += len(text_element['textRun']['content'])
        
        # Format content for team document
        formatted_content = self._format_team_content(team_notes, team_name)
        
        # Clear and replace content
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
                    'text': formatted_content
                }
            }
        ]
        
        self.docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

    def _format_team_content(self, team_notes, team_name):
        """Format team notes for the individual team document"""
        team_data = self.teams[team_name]
        
        content = f"""Instructor Notes for {team_name}
{team_data['topic']}

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

===============================================

{team_notes}

===============================================

This document is automatically updated from instructor collaboration notes.
For the latest updates, check the main instructor collaboration document.

Document updated by: GCAP3226 Instructor Collaboration System
"""
        return content

    def _update_team_readme(self, folder_id, team_notes, team_name):
        """Update team README with instructor notes section"""
        try:
            # Find README document
            query = f"parents in '{folder_id}' and name contains 'README'"
            results = self.drive_service.files().list(
                q=query,
                fields="files(id, name)"
            ).execute()
            
            files = results.get('files', [])
            if not files:
                return  # No README to update
            
            readme_id = files[0]['id']
            
            # Get current README content
            doc = self.docs_service.documents().get(documentId=readme_id).execute()
            content = doc.get('body', {}).get('content', [])
            
            # Extract current text
            current_text = ""
            for element in content:
                if 'paragraph' in element:
                    for text_element in element['paragraph'].get('elements', []):
                        if 'textRun' in text_element:
                            current_text += text_element['textRun']['content']
            
            # Check if instructor notes section exists
            instructor_section_start = current_text.find("=== INSTRUCTOR NOTES ===")
            
            notes_section = f"""

=== INSTRUCTOR NOTES ===
Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

{team_notes}

=== END INSTRUCTOR NOTES ===
"""
            
            if instructor_section_start != -1:
                # Replace existing section
                section_end = current_text.find("=== END INSTRUCTOR NOTES ===")
                if section_end != -1:
                    section_end += len("=== END INSTRUCTOR NOTES ===")
                    new_text = (current_text[:instructor_section_start] + 
                              notes_section + 
                              current_text[section_end:])
                else:
                    # End marker not found, replace from start marker to end
                    new_text = current_text[:instructor_section_start] + notes_section
            else:
                # Add new section at the end
                new_text = current_text + notes_section
            
            # Update the document
            doc_length = len(current_text) + 1  # +1 for the implicit newline
            
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
                        'text': new_text
                    }
                }
            ]
            
            self.docs_service.documents().batchUpdate(
                documentId=readme_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Updated README for {team_name}")
            
        except Exception as e:
            print(f"⚠️ Could not update README for {team_name}: {str(e)}")

    def sync_all_teams(self):
        """Sync notes to all team folders"""
        print("🚀 Starting team folder sync process...")
        
        # Find instructor document
        doc_id = self.find_instructor_doc()
        if not doc_id:
            print("❌ Cannot proceed without instructor document")
            return False
        
        # Read instructor notes
        instructor_content = self.read_instructor_notes(doc_id)
        if not instructor_content:
            print("❌ Cannot proceed without instructor content")
            return False
        
        # Extract team-specific notes
        team_notes = self.extract_team_notes(instructor_content)
        
        if not team_notes:
            print("⚠️ No team notes found to sync")
            return False
        
        # Sync each team
        for team_name, notes in team_notes.items():
            self.sync_team_folder(team_name, notes)
        
        return True

    def generate_sync_report(self):
        """Generate a report of the sync operation"""
        print("\n📋 Generating sync report...")
        
        # Save detailed report
        report_file = current_dir / f'sync_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(self.sync_results, f, indent=2)
        
        print(f"📄 Detailed report saved to: {report_file}")
        
        # Display summary
        print("\n" + "="*60)
        print("📊 TEAM NOTES SYNC REPORT")
        print("="*60)
        
        print(f"✅ Teams synced: {len(self.sync_results['teams_synced'])}")
        for team_sync in self.sync_results['teams_synced']:
            print(f"   - {team_sync['team']}: {team_sync['action']}")
        
        print(f"❌ Errors: {len(self.sync_results['errors'])}")
        for error in self.sync_results['errors']:
            print(f"   - {error}")
        
        print(f"⏰ Sync completed at: {self.sync_results['timestamp']}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Sync instructor notes to team folders')
    parser.add_argument('--doc-id', help='Instructor collaboration document ID')
    parser.add_argument('--team', help='Sync specific team only (e.g., Team_1)')
    
    args = parser.parse_args()
    
    try:
        manager = NoteSyncManager(instructor_doc_id=args.doc_id)
        
        if args.team:
            # Sync specific team only
            if args.team not in manager.teams:
                print(f"❌ Team '{args.team}' not found")
                return 1
            
            doc_id = manager.find_instructor_doc()
            if not doc_id:
                return 1
            
            instructor_content = manager.read_instructor_notes(doc_id)
            if not instructor_content:
                return 1
            
            team_notes = manager.extract_team_notes(instructor_content)
            if args.team in team_notes:
                manager.sync_team_folder(args.team, team_notes[args.team])
            else:
                print(f"⚠️ No notes found for {args.team}")
        else:
            # Sync all teams
            manager.sync_all_teams()
        
        manager.generate_sync_report()
        
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
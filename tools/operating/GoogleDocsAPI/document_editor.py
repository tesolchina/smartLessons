"""
Document Editor for GCAP 3226 Teams
Provides tools to read and edit team documents programmatically
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any

class DocumentEditor:
    """Editor for team Google Docs with offline fallback"""
    
    def __init__(self):
        self.docs_service = None
        self.team_results = {}
        self.setup_services()
        self.load_team_results()
    
    def setup_services(self):
        """Initialize Google Docs API service"""
        try:
            from googleapiclient.discovery import build
            from auth_setup import authenticate_google_apis
            
            creds = authenticate_google_apis()
            if creds:
                self.docs_service = build('docs', 'v1', credentials=creds)
                print("✅ Google Docs API ready")
            else:
                print("⚠️  Working in offline mode")
                
        except ImportError:
            print("⚠️  Google API libraries not installed. Working offline.")
    
    def load_team_results(self):
        """Load team setup results from file"""
        results_file = Path(__file__).parent / 'team_setup_results.json'
        
        if results_file.exists():
            try:
                with open(results_file, 'r') as f:
                    self.team_results = json.load(f)
                print(f"✅ Loaded {len(self.team_results)} team configurations")
            except Exception as e:
                print(f"⚠️  Could not load team results: {e}")
        else:
            print("⚠️  No team results found. Run team_manager.py first.")
    
    def read_document(self, team_name: str) -> Optional[str]:
        """Read the full content of a team's document"""
        if team_name not in self.team_results:
            print(f"❌ Team {team_name} not found")
            return None
        
        doc_id = self.team_results[team_name]['document_id']
        
        if not self.docs_service or doc_id.startswith('offline_'):
            return f"[OFFLINE MODE] Would read document for {team_name}"
        
        try:
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            content = self.extract_text_content(document.get('body', {}))
            print(f"✅ Read {len(content)} characters from {team_name} document")
            return content
            
        except Exception as e:
            print(f"❌ Failed to read document for {team_name}: {e}")
            return None
    
    def extract_text_content(self, body: Dict) -> str:
        """Extract text content from Google Docs body structure"""
        content = []
        
        for element in body.get('content', []):
            if 'paragraph' in element:
                para_content = self.extract_paragraph_text(element['paragraph'])
                if para_content:
                    content.append(para_content)
            elif 'table' in element:
                table_content = self.extract_table_text(element['table'])
                if table_content:
                    content.append(table_content)
        
        return '\n'.join(content)
    
    def extract_paragraph_text(self, paragraph: Dict) -> str:
        """Extract text from a paragraph element"""
        text_parts = []
        
        for element in paragraph.get('elements', []):
            if 'textRun' in element:
                text_parts.append(element['textRun']['content'])
        
        return ''.join(text_parts).rstrip('\n')
    
    def extract_table_text(self, table: Dict) -> str:
        """Extract text from a table element"""
        table_content = []
        
        for row in table.get('tableRows', []):
            row_content = []
            for cell in row.get('tableCells', []):
                cell_text = []
                for element in cell.get('content', []):
                    if 'paragraph' in element:
                        cell_text.append(self.extract_paragraph_text(element['paragraph']))
                row_content.append(' '.join(cell_text))
            if any(row_content):
                table_content.append(' | '.join(row_content))
        
        return '\n'.join(table_content)
    
    def update_team_members(self, team_name: str, members: List[Dict[str, str]]):
        """Update team member information in the document"""
        if team_name not in self.team_results:
            print(f"❌ Team {team_name} not found")
            return False
        
        doc_id = self.team_results[team_name]['document_id']
        
        if not self.docs_service or doc_id.startswith('offline_'):
            print(f"[OFFLINE MODE] Would update {team_name} with {len(members)} members")
            return True
        
        try:
            # Read current document
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            content = self.extract_text_content(document.get('body', {}))
            
            # Find and replace member placeholders
            requests = []
            member_section_start = content.find("Team Members:")
            
            if member_section_start != -1:
                # Build member text
                member_text = "\n".join([
                    f"✅ {member['name']} - Email: {member['email']}"
                    for member in members
                ])
                
                # Add padding for remaining slots
                for i in range(len(members), 5):
                    member_text += f"\n[ ] Student {i+1} - Name: _____________ Email: _____________"
                
                # Replace the member section
                requests.append({
                    'replaceAllText': {
                        'containsText': {
                            'text': '[ ] Student 1 - Name: _____________ Email: _____________\n[ ] Student 2 - Name: _____________ Email: _____________\n[ ] Student 3 - Name: _____________ Email: _____________\n[ ] Student 4 - Name: _____________ Email: _____________\n[ ] Student 5 - Name: _____________ Email: _____________',
                            'matchCase': False
                        },
                        'replaceText': member_text
                    }
                })
            
            if requests:
                self.docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': requests}
                ).execute()
                print(f"✅ Updated team members for {team_name}")
                return True
            
        except Exception as e:
            print(f"❌ Failed to update team members for {team_name}: {e}")
            return False
    
    def add_meeting_notes(self, team_name: str, date: str, attendees: str, agenda: List[str], notes: str):
        """Add meeting notes to team document"""
        if team_name not in self.team_results:
            print(f"❌ Team {team_name} not found")
            return False
        
        doc_id = self.team_results[team_name]['document_id']
        
        if not self.docs_service or doc_id.startswith('offline_'):
            print(f"[OFFLINE MODE] Would add meeting notes for {team_name}")
            return True
        
        try:
            # Prepare meeting notes text
            agenda_text = "\n".join([f"- {item}" for item in agenda])
            
            meeting_notes = f"""
MEETING NOTES - {date}
Attendees: {attendees}

Agenda:
{agenda_text}

Notes:
{notes}

---
"""
            
            # Find insertion point (after the existing meeting notes section)
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            
            # Insert at the end of the document
            requests = [{
                'insertText': {
                    'location': {'index': len(self.extract_text_content(document.get('body', {}))) + 1},
                    'text': meeting_notes
                }
            }]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Added meeting notes for {team_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to add meeting notes for {team_name}: {e}")
            return False
    
    def list_all_teams(self):
        """List all available teams and their documents"""
        print("📋 GCAP 3226 Team Overview")
        print("=" * 50)
        
        if not self.team_results:
            print("No teams found. Run team_manager.py first.")
            return
        
        for team_name, info in self.team_results.items():
            print(f"\n🏆 {team_name}")
            print(f"   📁 Folder ID: {info['folder_id']}")
            print(f"   📄 Document ID: {info['document_id']}")
            print(f"   🎯 Topic: {info['topic']}")
    
    def bulk_update_all_teams(self, update_data: Dict[str, Any]):
        """Perform bulk updates across all teams"""
        print("🔄 Performing bulk updates...")
        
        results = {}
        for team_name in self.team_results.keys():
            try:
                if 'members' in update_data:
                    members = update_data['members'].get(team_name, [])
                    success = self.update_team_members(team_name, members)
                    results[team_name] = success
                
            except Exception as e:
                print(f"❌ Bulk update failed for {team_name}: {e}")
                results[team_name] = False
        
        successful = sum(results.values())
        total = len(results)
        print(f"✅ Bulk update complete: {successful}/{total} teams updated")

def main():
    """Example usage of DocumentEditor"""
    editor = DocumentEditor()
    
    # List all teams
    editor.list_all_teams()
    
    # Example: Read a document
    # content = editor.read_document("Team01_DataGovernanceFramework")
    # print(content[:200] + "..." if len(content) > 200 else content)
    
    # Example: Update team members
    # example_members = [
    #     {"name": "Alice Wong", "email": "alice@student.edu.hk"},
    #     {"name": "Bob Chen", "email": "bob@student.edu.hk"}
    # ]
    # editor.update_team_members("Team01_DataGovernanceFramework", example_members)
    
    # Example: Add meeting notes
    # editor.add_meeting_notes(
    #     "Team01_DataGovernanceFramework",
    #     "2024-01-15",
    #     "Alice, Bob, Charlie",
    #     ["Project kickoff", "Role assignments", "Timeline review"],
    #     "Great first meeting! Everyone is excited to start working on the data governance framework."
    # )

if __name__ == "__main__":
    main()

"""
GCAP 3226 Simple Team Editor
Works with renamed Team01-Team08 folders
Allows easy project title updates when ready
"""

import json
from pathlib import Path
from typing import Dict, List

class SimpleTeamEditor:
    """Editor for the renamed Team01-Team08 structure"""
    
    def __init__(self):
        self.docs_service = None
        self.drive_service = None
        self.team_results = {}
        self.setup_services()
        self.load_team_results()
    
    def setup_services(self):
        """Initialize Google API services"""
        try:
            from googleapiclient.discovery import build
            from auth_setup import authenticate_google_apis
            
            creds = authenticate_google_apis()
            if creds:
                self.docs_service = build('docs', 'v1', credentials=creds)
                self.drive_service = build('drive', 'v3', credentials=creds)
                print("✅ Google APIs ready for simple team management")
            else:
                print("⚠️  Working in offline mode")
                
        except ImportError:
            print("⚠️  Google API libraries not installed. Working offline.")
    
    def load_team_results(self):
        """Load team results"""
        results_file = Path(__file__).parent / 'gcap3226_teams_results.json'
        
        if results_file.exists():
            try:
                with open(results_file, 'r') as f:
                    self.team_results = json.load(f)
                print(f"✅ Loaded {len(self.team_results)} teams")
            except Exception as e:
                print(f"⚠️  Could not load team results: {e}")
    
    def list_teams(self):
        """List all teams with simple names"""
        print("📋 GCAP 3226 Teams (Simple Names)")
        print("=" * 40)
        
        for team_name, info in self.team_results.items():
            print(f"\n🏆 {team_name}")
            print(f"   📄 Document: https://docs.google.com/document/d/{info['document_id']}/edit")
            print(f"   🎯 Current Status: {info['topic']}")
            if 'old_topic' in info:
                print(f"   📝 Previous Idea: {info['old_topic']}")
    
    def add_students(self, team_name: str, students: List[Dict[str, str]]):
        """Add students to a team"""
        if team_name not in self.team_results:
            print(f"❌ {team_name} not found. Available teams: {list(self.team_results.keys())}")
            return False
        
        doc_id = self.team_results[team_name]['document_id']
        
        if not self.docs_service or doc_id.startswith('offline_'):
            print(f"[OFFLINE] Would add {len(students)} students to {team_name}")
            return True
        
        try:
            # Build student list
            student_lines = []
            for i, student in enumerate(students, 1):
                name = student.get('name', f'Student {i}')
                email = student.get('email', 'email@student.hkbu.edu.hk')
                student_lines.append(f"{i}. Name: {name:<25} Email: {email}")
            
            # Fill remaining slots (up to 5)
            for i in range(len(students) + 1, 6):
                student_lines.append(f"{i}. Name: _________________ Email: _________________")
            
            new_student_section = "\n".join(student_lines)
            
            # Replace student section in document
            requests = [{
                'replaceAllText': {
                    'containsText': {
                        'text': '1. Name: _________________ Email: _________________',
                        'matchCase': False
                    },
                    'replaceText': new_student_section
                }
            }]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Added {len(students)} students to {team_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to add students to {team_name}: {e}")
            return False
    
    def update_project_title(self, team_name: str, project_title: str, project_description: str = ""):
        """Update project title and description for a team when ready"""
        if team_name not in self.team_results:
            print(f"❌ {team_name} not found")
            return False
        
        doc_id = self.team_results[team_name]['document_id']
        
        if not self.docs_service or doc_id.startswith('offline_'):
            print(f"[OFFLINE] Would update {team_name} with project: {project_title}")
            return True
        
        try:
            # Update the project topic in document
            requests = [{
                'replaceAllText': {
                    'containsText': {
                        'text': 'PROJECT TOPIC: Project Topic TBD',
                        'matchCase': False
                    },
                    'replaceText': f'PROJECT TOPIC: {project_title}'
                }
            }]
            
            if project_description:
                requests.append({
                    'replaceAllText': {
                        'containsText': {
                            'text': 'FOCUS AREAS: Team',
                            'matchCase': False
                        },
                        'replaceText': f'FOCUS AREAS: {project_description}'
                    }
                })
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            # Update local results
            self.team_results[team_name]['topic'] = project_title
            self.save_team_results()
            
            print(f"✅ Updated {team_name} project title: {project_title}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update project title for {team_name}: {e}")
            return False
    
    def rename_folder_and_document(self, team_name: str, new_folder_name: str, new_doc_title: str):
        """Rename folder and document when project title is finalized"""
        if team_name not in self.team_results:
            print(f"❌ {team_name} not found")
            return False
        
        folder_id = self.team_results[team_name]['folder_id']
        doc_id = self.team_results[team_name]['document_id']
        
        if not self.drive_service or not self.docs_service:
            print(f"[OFFLINE] Would rename {team_name} to {new_folder_name}")
            return True
        
        try:
            # Rename folder
            self.drive_service.files().update(
                fileId=folder_id,
                body={'name': new_folder_name}
            ).execute()
            
            # Update document title (this changes the document's filename)
            requests = [{
                'replaceAllText': {
                    'containsText': {
                        'text': f'{team_name} - Project Document',
                        'matchCase': False
                    },
                    'replaceText': new_doc_title
                }
            }]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Renamed {team_name} folder to: {new_folder_name}")
            print(f"✅ Updated document title to: {new_doc_title}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to rename {team_name}: {e}")
            return False
    
    def save_team_results(self):
        """Save updated team results"""
        results_file = Path(__file__).parent / 'gcap3226_teams_results.json'
        try:
            with open(results_file, 'w') as f:
                json.dump(self.team_results, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")
    
    def get_team_link(self, team_name: str) -> str:
        """Get direct link to team document"""
        if team_name in self.team_results:
            doc_id = self.team_results[team_name]['document_id']
            return f"https://docs.google.com/document/d/{doc_id}/edit"
        return "Team not found"
    
    def bulk_operations_example(self):
        """Show examples of bulk operations"""
        print("\n📋 BULK OPERATION EXAMPLES:")
        print("=" * 30)
        
        print("\n1. ADD STUDENTS TO MULTIPLE TEAMS:")
        print("editor = SimpleTeamEditor()")
        print("students = [{'name': 'Alice Wong', 'email': 'alice@life.hkbu.edu.hk'}]")
        print("editor.add_students('Team01', students)")
        
        print("\n2. UPDATE PROJECT TITLES WHEN READY:")
        print("editor.update_project_title('Team01', 'Housing Policy Analysis')")
        
        print("\n3. RENAME FOLDERS WITH FINAL PROJECT NAMES:")
        print("editor.rename_folder_and_document('Team01', 'Team01_HousingPolicy', 'Housing Policy Analysis Project')")

def main():
    """Main function with examples"""
    editor = SimpleTeamEditor()
    
    # Show current teams
    editor.list_teams()
    
    # Show example operations
    editor.bulk_operations_example()
    
    print(f"\n🎯 READY FOR USE:")
    print(f"✅ 8 teams with simple names (Team01-Team08)")
    print(f"✅ Easy to add students anytime")
    print(f"✅ Easy to update project titles when decided")
    print(f"✅ Easy to rename folders when projects are finalized")

if __name__ == "__main__":
    main()

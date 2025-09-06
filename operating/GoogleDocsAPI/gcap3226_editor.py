"""
GCAP 3226 Document Editor - For 8 Teams
Manages team documents and student information
"""

import json
from pathlib import Path
from typing import Dict, List

class GCAP3226DocumentEditor:
    """Editor for GCAP 3226 team documents"""
    
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
                print("✅ Google Docs API ready for GCAP 3226")
            else:
                print("⚠️  Working in offline mode")
                
        except ImportError:
            print("⚠️  Google API libraries not installed. Working offline.")
    
    def load_team_results(self):
        """Load GCAP 3226 team setup results"""
        results_file = Path(__file__).parent / 'gcap3226_teams_results.json'
        
        if results_file.exists():
            try:
                with open(results_file, 'r') as f:
                    self.team_results = json.load(f)
                print(f"✅ Loaded {len(self.team_results)} GCAP 3226 teams")
            except Exception as e:
                print(f"⚠️  Could not load team results: {e}")
        else:
            print("⚠️  No GCAP 3226 team results found. Run gcap3226_manager.py first.")
    
    def add_students_to_team(self, team_name: str, students: List[Dict[str, str]]):
        """Add student information to a team document"""
        if team_name not in self.team_results:
            print(f"❌ Team {team_name} not found")
            return False
        
        doc_id = self.team_results[team_name]['document_id']
        
        if not self.docs_service or doc_id.startswith('offline_'):
            print(f"[OFFLINE MODE] Would add {len(students)} students to {team_name}")
            return True
        
        try:
            # Build student information text
            student_lines = []
            for i, student in enumerate(students, 1):
                name = student.get('name', f'Student {i}')
                email = student.get('email', 'email@student.hkbu.edu.hk')
                student_lines.append(f"{i}. Name: {name:<25} Email: {email}")
            
            # Fill remaining slots
            for i in range(len(students) + 1, 6):
                student_lines.append(f"{i}. Name: _________________ Email: _________________")
            
            new_student_section = "\n".join(student_lines)
            
            # Replace the student section
            requests = [{
                'replaceAllText': {
                    'containsText': {
                        'text': '1. Name: _________________ Email: _________________\n2. Name: _________________ Email: _________________\n3. Name: _________________ Email: _________________\n4. Name: _________________ Email: _________________\n5. Name: _________________ Email: _________________',
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
    
    def get_team_document_link(self, team_name: str) -> str:
        """Get direct link to team document"""
        if team_name not in self.team_results:
            return "Team not found"
        
        doc_id = self.team_results[team_name]['document_id']
        return f"https://docs.google.com/document/d/{doc_id}/edit"
    
    def list_all_teams(self):
        """List all GCAP 3226 teams"""
        print("📋 GCAP 3226 Teams Overview")
        print("=" * 40)
        
        for i, (team_name, info) in enumerate(self.team_results.items(), 1):
            print(f"\n🏆 Team {i:02d}: {team_name}")
            print(f"   📄 Document: {self.get_team_document_link(team_name)}")
            print(f"   🎯 Topic: {info['topic']}")
    
    def bulk_add_students(self, student_assignments: Dict[str, List[Dict[str, str]]]):
        """Add students to multiple teams at once"""
        print("🔄 Adding students to teams...")
        
        results = {}
        for team_name, students in student_assignments.items():
            success = self.add_students_to_team(team_name, students)
            results[team_name] = success
            
        successful = sum(results.values())
        total = len(results)
        print(f"✅ Student assignment complete: {successful}/{total} teams updated")

def main():
    """Example usage"""
    editor = GCAP3226DocumentEditor()
    
    # List teams
    editor.list_all_teams()
    
    # Example: Add students to Team01
    # example_students = [
    #     {"name": "Alice Wong", "email": "alice@life.hkbu.edu.hk"},
    #     {"name": "Bob Chen", "email": "bob@life.hkbu.edu.hk"},
    #     {"name": "Carol Liu", "email": "carol@life.hkbu.edu.hk"}
    # ]
    # editor.add_students_to_team("Team01_DataGovernanceFramework", example_students)
    
    print("\n📋 Available commands:")
    print("- editor.add_students_to_team('Team01_DataGovernanceFramework', students)")
    print("- editor.get_team_document_link('Team01_DataGovernanceFramework')")
    print("- editor.bulk_add_students(student_assignments)")

if __name__ == "__main__":
    main()

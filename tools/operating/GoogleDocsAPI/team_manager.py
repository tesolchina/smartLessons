"""
Team Management System for GCAP 3226
Creates and manages Google Drive folders and documents for 10 teams
"""

from pathlib import Path
import json
import time
from typing import Dict, List, Optional

class TeamManager:
    """Manages team folders and documents for GCAP 3226 course"""
    
    def __init__(self, credentials_path: str = None):
        self.credentials_path = credentials_path
        self.drive_service = None
        self.docs_service = None
        self.team_data = {}
        self.setup_services()
        self.load_team_data()
    
    def setup_services(self):
        """Initialize Google API services"""
        try:
            from googleapiclient.discovery import build
            from auth_setup import authenticate_google_apis
            
            creds = authenticate_google_apis()
            if not creds:
                raise Exception("Authentication failed")
            
            self.drive_service = build('drive', 'v3', credentials=creds)
            self.docs_service = build('docs', 'v1', credentials=creds)
            print("✅ Google API services initialized")
            
        except ImportError:
            print("⚠️  Google API libraries not installed. Using offline mode.")
            self.drive_service = None
            self.docs_service = None
    
    def load_team_data(self):
        """Load team configuration"""
        self.team_data = {
            "Team01_DataGovernanceFramework": {
                "topic": "Developing a Data Governance Framework for Educational Institutions",
                "focus": "Policy development and implementation strategies",
                "members": []
            },
            "Team02_PrivacyCompliance": {
                "topic": "Student Privacy and Data Protection in Digital Learning",
                "focus": "GDPR compliance and privacy protection mechanisms",
                "members": []
            },
            "Team03_DataQualityManagement": {
                "topic": "Data Quality Assessment and Management Systems",
                "focus": "Quality metrics and data validation processes",
                "members": []
            },
            "Team04_EthicalAI": {
                "topic": "Ethical Considerations in Educational AI and Analytics",
                "focus": "Bias detection and fairness in algorithmic decisions",
                "members": []
            },
            "Team05_DataSecurity": {
                "topic": "Cybersecurity and Data Breach Prevention",
                "focus": "Security frameworks and incident response planning",
                "members": []
            },
            "Team06_OpenDataInitiatives": {
                "topic": "Open Data Policies and Research Data Management",
                "focus": "Data sharing protocols and repository management",
                "members": []
            },
            "Team07_StudentDataRights": {
                "topic": "Student Data Rights and Consent Management",
                "focus": "Rights frameworks and consent technologies",
                "members": []
            },
            "Team08_DataAnalyticsGovernance": {
                "topic": "Governance of Learning Analytics and Predictive Models",
                "focus": "Algorithmic accountability and transparent analytics",
                "members": []
            },
            "Team09_CrossBorderData": {
                "topic": "Cross-border Data Transfer and International Compliance",
                "focus": "Multi-jurisdictional compliance and data sovereignty",
                "members": []
            },
            "Team10_SustainableDataPractices": {
                "topic": "Sustainable Data Practices and Environmental Impact",
                "focus": "Green computing and sustainable data management",
                "members": []
            }
        }
    
    def create_team_folder(self, team_name: str) -> Optional[str]:
        """Create a Google Drive folder for a team"""
        if not self.drive_service:
            print(f"📁 [OFFLINE] Would create folder: {team_name}")
            return f"offline_folder_{team_name}"
        
        try:
            folder_metadata = {
                'name': f'GCAP3226_{team_name}',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': []  # Root folder, or specify parent folder ID
            }
            
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            folder_id = folder.get('id')
            print(f"✅ Created folder for {team_name}: {folder_id}")
            return folder_id
            
        except Exception as e:
            print(f"❌ Failed to create folder for {team_name}: {e}")
            return None
    
    def create_team_document(self, team_name: str, folder_id: str) -> Optional[str]:
        """Create a Google Doc for team collaboration"""
        if not self.docs_service or not self.drive_service:
            print(f"📄 [OFFLINE] Would create document for: {team_name}")
            return f"offline_doc_{team_name}"
        
        try:
            team_info = self.team_data[team_name]
            
            # Create the document
            doc_title = f"GCAP3226_{team_name}_Project"
            document = {
                'title': doc_title
            }
            
            doc = self.docs_service.documents().create(body=document).execute()
            doc_id = doc.get('documentId')
            
            # Move document to team folder
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=folder_id,
                removeParents='',
                fields='id, parents'
            ).execute()
            
            # Add initial content to document
            self.add_initial_content(doc_id, team_name, team_info)
            
            print(f"✅ Created document for {team_name}: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"❌ Failed to create document for {team_name}: {e}")
            return None
    
    def add_initial_content(self, doc_id: str, team_name: str, team_info: Dict):
        """Add initial template content to team document"""
        if not self.docs_service:
            return
        
        try:
            requests = [
                {
                    'insertText': {
                        'location': {'index': 1},
                        'text': f"""GCAP 3226 - Data Governance in Education
Team: {team_name}

Project Topic: {team_info['topic']}
Focus Area: {team_info['focus']}

Team Members:
[ ] Student 1 - Name: _____________ Email: _____________
[ ] Student 2 - Name: _____________ Email: _____________
[ ] Student 3 - Name: _____________ Email: _____________
[ ] Student 4 - Name: _____________ Email: _____________
[ ] Student 5 - Name: _____________ Email: _____________

Project Timeline:
Week 1-2: Literature review and problem definition
Week 3-4: Framework development
Week 5-6: Implementation planning
Week 7-8: Case study development
Week 9-10: Final presentation preparation

Deliverables:
1. Literature Review (Week 2)
2. Framework Proposal (Week 4)
3. Implementation Plan (Week 6)
4. Case Study Analysis (Week 8)
5. Final Presentation (Week 10)

Meeting Notes:
Date: _________
Attendees: ________________
Agenda:
- 
- 
- 

Action Items:
[ ] Task 1 - Assigned to: _______ Due: _______
[ ] Task 2 - Assigned to: _______ Due: _______
[ ] Task 3 - Assigned to: _______ Due: _______

Resources:
- Course Materials: [Link to Moodle]
- Shared Drive: [This folder]
- Team Communication: [Slack/Email]

Notes:
(Use this space for ongoing project notes and documentation)

"""
                    }
                }
            ]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
        except Exception as e:
            print(f"❌ Failed to add content to document: {e}")
    
    def create_all_teams(self):
        """Create folders and documents for all teams"""
        print("🚀 Creating team folders and documents...")
        print("=" * 50)
        
        results = {}
        
        for team_name in self.team_data.keys():
            print(f"\n📋 Setting up {team_name}...")
            
            # Create folder
            folder_id = self.create_team_folder(team_name)
            if not folder_id:
                continue
            
            # Create document
            doc_id = self.create_team_document(team_name, folder_id)
            
            results[team_name] = {
                'folder_id': folder_id,
                'document_id': doc_id,
                'topic': self.team_data[team_name]['topic']
            }
            
            # Small delay to avoid API rate limits
            if self.drive_service:
                time.sleep(0.5)
        
        # Save results
        self.save_team_results(results)
        self.print_summary(results)
    
    def save_team_results(self, results: Dict):
        """Save team creation results to file"""
        results_file = Path(__file__).parent / 'team_setup_results.json'
        
        try:
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Team setup results saved to: {results_file}")
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")
    
    def print_summary(self, results: Dict):
        """Print setup summary"""
        print("\n" + "=" * 50)
        print("🎉 TEAM SETUP COMPLETE!")
        print("=" * 50)
        
        successful = len([r for r in results.values() if r['folder_id'] and r['document_id']])
        total = len(results)
        
        print(f"✅ Successfully created: {successful}/{total} teams")
        print("\nTeam Structure:")
        
        for team_name, info in results.items():
            status = "✅" if info['folder_id'] and info['document_id'] else "❌"
            print(f"{status} {team_name}")
            print(f"   📁 Folder: {info['folder_id']}")
            print(f"   📄 Document: {info['document_id']}")
            print(f"   🎯 Topic: {info['topic'][:60]}...")
            print()

def main():
    """Main execution function"""
    print("GCAP 3226 Team Management System")
    print("=" * 40)
    
    manager = TeamManager()
    manager.create_all_teams()

if __name__ == "__main__":
    main()

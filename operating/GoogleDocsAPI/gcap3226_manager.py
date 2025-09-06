"""
GCAP 3226 Team Manager - Customized for 8 Teams
Creates 8 teams in specific Google Drive folder with simplified templates
"""

from pathlib import Path
import json
import time
from typing import Dict, List, Optional

class GCAP3226TeamManager:
    """Manages 8 teams for GCAP 3226 course in specific Drive folder"""
    
    def __init__(self):
        self.drive_service = None
        self.docs_service = None
        self.parent_folder_id = "1S4JMQSkIWAPhwKqUkKxfC6qqWewD6z8v"  # Your specific folder
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
        """Load team configuration for 8 teams focused on data governance"""
        self.team_data = {
            "Team01_DataGovernanceFramework": {
                "topic": "Data Governance Framework for Educational Institutions",
                "focus": "Policy development, compliance frameworks, and implementation strategies",
                "members": []
            },
            "Team02_PrivacyProtection": {
                "topic": "Student Privacy and Data Protection",
                "focus": "GDPR compliance, privacy by design, and consent management",
                "members": []
            },
            "Team03_DataQuality": {
                "topic": "Data Quality and Integrity Management",
                "focus": "Quality metrics, validation processes, and data cleansing",
                "members": []
            },
            "Team04_EthicalAI": {
                "topic": "Ethical AI and Algorithmic Governance",
                "focus": "Bias detection, fairness metrics, and ethical AI frameworks",
                "members": []
            },
            "Team05_DataSecurity": {
                "topic": "Educational Data Security and Cybersecurity",
                "focus": "Security frameworks, breach prevention, and incident response",
                "members": []
            },
            "Team06_OpenDataPolicy": {
                "topic": "Open Data Policies and Research Data Management",
                "focus": "Data sharing protocols, repository management, and access controls",
                "members": []
            },
            "Team07_StudentDataRights": {
                "topic": "Student Data Rights and Digital Consent",
                "focus": "Rights frameworks, consent technologies, and student empowerment",
                "members": []
            },
            "Team08_AnalyticsGovernance": {
                "topic": "Learning Analytics and Predictive Model Governance",
                "focus": "Algorithmic accountability, transparent analytics, and ethical predictions",
                "members": []
            }
        }
    
    def create_team_folder(self, team_name: str) -> Optional[str]:
        """Create a team folder inside the specific GCAP 3226 folder"""
        if not self.drive_service:
            print(f"📁 [OFFLINE] Would create folder: {team_name}")
            return f"offline_folder_{team_name}"
        
        try:
            folder_metadata = {
                'name': team_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [self.parent_folder_id]  # Create inside specific folder
            }
            
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            folder_id = folder.get('id')
            print(f"✅ Created folder {team_name}: {folder_id}")
            return folder_id
            
        except Exception as e:
            print(f"❌ Failed to create folder for {team_name}: {e}")
            return None
    
    def create_team_document(self, team_name: str, folder_id: str) -> Optional[str]:
        """Create a simple team document with basic template"""
        if not self.docs_service or not self.drive_service:
            print(f"📄 [OFFLINE] Would create document for: {team_name}")
            return f"offline_doc_{team_name}"
        
        try:
            team_info = self.team_data[team_name]
            
            # Create the document
            doc_title = f"{team_name}_Project"
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
            
            # Add simple content to document
            self.add_simple_template(doc_id, team_name, team_info)
            
            print(f"✅ Created document {team_name}: {doc_id}")
            return doc_id
            
        except Exception as e:
            print(f"❌ Failed to create document for {team_name}: {e}")
            return None
    
    def add_simple_template(self, doc_id: str, team_name: str, team_info: Dict):
        """Add simple template content to team document"""
        if not self.docs_service:
            return
        
        try:
            template_content = f"""GCAP 3226 - Data Governance in Education
{team_name}

PROJECT TOPIC: {team_info['topic']}
FOCUS AREAS: {team_info['focus']}

TEAM MEMBERS (Up to 5 students):
1. Name: _________________ Email: _________________
2. Name: _________________ Email: _________________
3. Name: _________________ Email: _________________
4. Name: _________________ Email: _________________
5. Name: _________________ Email: _________________

PROJECT TIMELINE:
Week 1-3: Research and analysis
Week 4-6: Framework development  
Week 7-9: Implementation planning
Week 10-12: Final presentation

DELIVERABLES:
□ Literature review
□ Policy analysis
□ Implementation framework
□ Final presentation

MEETING NOTES:
Date: _________
Attendees: _________________
Discussion Points:
- 
- 
- 

Action Items:
□ Task: _________________ Assigned to: _______ Due: _______
□ Task: _________________ Assigned to: _______ Due: _______
□ Task: _________________ Assigned to: _______ Due: _______

PROJECT NOTES:
(Use this space for project development notes)


"""
            
            requests = [{
                'insertText': {
                    'location': {'index': 1},
                    'text': template_content
                }
            }]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
        except Exception as e:
            print(f"❌ Failed to add template content: {e}")
    
    def create_all_8_teams(self):
        """Create folders and documents for all 8 teams"""
        print("🚀 Creating 8 GCAP 3226 Teams in Google Drive...")
        print(f"📁 Parent folder: {self.parent_folder_id}")
        print("=" * 60)
        
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
        self.save_results(results)
        self.print_summary(results)
        return results
    
    def save_results(self, results: Dict):
        """Save team creation results"""
        results_file = Path(__file__).parent / 'gcap3226_teams_results.json'
        
        try:
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Results saved to: {results_file}")
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")
    
    def print_summary(self, results: Dict):
        """Print setup summary"""
        print("\n" + "=" * 60)
        print("🎉 GCAP 3226 TEAM SETUP COMPLETE!")
        print("=" * 60)
        
        successful = len([r for r in results.values() if r['folder_id'] and r['document_id']])
        
        print(f"✅ Successfully created: {successful}/8 teams")
        print(f"📁 All teams created in: https://drive.google.com/drive/u/0/folders/{self.parent_folder_id}")
        print()
        
        for i, (team_name, info) in enumerate(results.items(), 1):
            status = "✅" if info['folder_id'] and info['document_id'] else "❌"
            print(f"{status} Team {i:02d}: {team_name}")
            print(f"   📄 Document: https://docs.google.com/document/d/{info['document_id']}/edit")
            print(f"   🎯 Topic: {info['topic']}")
            print()

def main():
    """Main execution"""
    print("GCAP 3226 - 8 Team Setup")
    print("=" * 25)
    
    manager = GCAP3226TeamManager()
    results = manager.create_all_8_teams()
    
    if results:
        print("\n📋 NEXT STEPS:")
        print("1. Check your Google Drive folder for the 8 team folders")
        print("2. Open team documents to verify templates")
        print("3. Use document_editor.py to add student information")
        print("4. Share folder access with students")

if __name__ == "__main__":
    main()

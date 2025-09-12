"""
Template Distributor for GCAP 3226 Teams
Copies the project template to all 8 team folders
"""

import json
from pathlib import Path

class TemplateDistributor:
    """Distributes project template to all team folders"""
    
    def __init__(self):
        self.drive_service = None
        self.team_results = {}
        self.template_doc_id = "1ItVo0XhR2Jmk30pNG5ufgY8A4hFWDiN1Us3YCvdkKhc"
        self.setup_services()
        self.load_team_results()
    
    def setup_services(self):
        """Initialize Google Drive API"""
        try:
            from googleapiclient.discovery import build
            from auth_setup import authenticate_google_apis
            
            creds = authenticate_google_apis()
            if creds:
                self.drive_service = build('drive', 'v3', credentials=creds)
                print("✅ Google Drive API ready for template distribution")
            else:
                print("⚠️  Working in offline mode")
                
        except ImportError:
            print("⚠️  Google API libraries not installed. Working offline.")
    
    def load_team_results(self):
        """Load team folder information"""
        results_file = Path(__file__).parent / 'gcap3226_teams_results.json'
        
        if results_file.exists():
            try:
                with open(results_file, 'r') as f:
                    self.team_results = json.load(f)
                print(f"✅ Loaded {len(self.team_results)} team folders")
            except Exception as e:
                print(f"⚠️  Could not load team results: {e}")
    
    def copy_template_to_team(self, team_name: str) -> str:
        """Copy template document to a specific team folder"""
        if team_name not in self.team_results:
            print(f"❌ Team {team_name} not found")
            return None
        
        if not self.drive_service:
            print(f"[OFFLINE] Would copy template to {team_name}")
            return "offline_copy"
        
        try:
            folder_id = self.team_results[team_name]['folder_id']
            
            # Copy the template document
            copy_metadata = {
                'name': f'{team_name}_Project_Workspace',
                'parents': [folder_id]
            }
            
            copied_file = self.drive_service.files().copy(
                fileId=self.template_doc_id,
                body=copy_metadata
            ).execute()
            
            copied_doc_id = copied_file.get('id')
            print(f"✅ Copied template to {team_name}: {copied_doc_id}")
            
            return copied_doc_id
            
        except Exception as e:
            print(f"❌ Failed to copy template to {team_name}: {e}")
            return None
    
    def distribute_to_all_teams(self):
        """Copy template to all team folders"""
        print("📋 Distributing project template to all teams...")
        print("=" * 55)
        
        distribution_results = {}
        
        for team_name in self.team_results.keys():
            print(f"\n📄 Copying template to {team_name}...")
            copied_doc_id = self.copy_template_to_team(team_name)
            
            if copied_doc_id:
                distribution_results[team_name] = {
                    'template_doc_id': copied_doc_id,
                    'template_link': f"https://docs.google.com/document/d/{copied_doc_id}/edit",
                    'folder_id': self.team_results[team_name]['folder_id']
                }
        
        self.save_distribution_results(distribution_results)
        self.print_distribution_summary(distribution_results)
        
        return distribution_results
    
    def save_distribution_results(self, results: dict):
        """Save template distribution results"""
        results_file = Path(__file__).parent / 'template_distribution_results.json'
        
        try:
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Distribution results saved: {results_file}")
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")
    
    def print_distribution_summary(self, results: dict):
        """Print distribution summary"""
        print("\n" + "=" * 55)
        print("🎉 TEMPLATE DISTRIBUTION COMPLETE!")
        print("=" * 55)
        
        successful = len([r for r in results.values() if r['template_doc_id']])
        
        print(f"✅ Successfully distributed to: {successful}/8 teams")
        print(f"📄 Original template: https://docs.google.com/document/d/{self.template_doc_id}/edit")
        print("\nTeam Project Workspaces:")
        
        for team_name, info in results.items():
            print(f"\n🏆 {team_name}")
            print(f"   📄 Project Workspace: {info['template_link']}")
            print(f"   📁 Team Folder: https://drive.google.com/drive/u/0/folders/{info['folder_id']}")
            print(f"   🎯 Status: Ready for project planning")

def main():
    """Distribute templates to all teams"""
    print("GCAP 3226 Template Distribution")
    print("=" * 32)
    
    distributor = TemplateDistributor()
    results = distributor.distribute_to_all_teams()
    
    if results:
        print("\n📋 NEXT STEPS:")
        print("1. Each team now has their own project workspace")
        print("2. Teams can start filling in their information")
        print("3. Templates include all syllabus requirements")
        print("4. Teams can track progress and manage milestones")

if __name__ == "__main__":
    main()

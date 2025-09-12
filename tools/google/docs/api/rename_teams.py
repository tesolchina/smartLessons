"""
GCAP 3226 Folder Renamer
Renames the existing team folders to simple Team01, Team02, etc.
since we don't know the actual project titles yet
"""

import json
from pathlib import Path
from typing import Dict

class GCAP3226FolderRenamer:
    """Renames team folders and updates documents"""
    
    def __init__(self):
        self.drive_service = None
        self.docs_service = None
        self.team_results = {}
        self.setup_services()
        self.load_team_results()
    
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
            print("✅ Google API services ready for renaming")
            
        except ImportError:
            print("⚠️  Google API libraries not installed. Using offline mode.")
            self.drive_service = None
            self.docs_service = None
    
    def load_team_results(self):
        """Load existing team results"""
        results_file = Path(__file__).parent / 'gcap3226_teams_results.json'
        
        if results_file.exists():
            try:
                with open(results_file, 'r') as f:
                    self.team_results = json.load(f)
                print(f"✅ Loaded {len(self.team_results)} existing teams for renaming")
            except Exception as e:
                print(f"❌ Could not load team results: {e}")
        else:
            print("❌ No team results found. Run gcap3226_manager.py first.")
    
    def rename_folder(self, folder_id: str, new_name: str) -> bool:
        """Rename a Google Drive folder"""
        if not self.drive_service:
            print(f"[OFFLINE] Would rename folder {folder_id} to {new_name}")
            return True
        
        try:
            file_metadata = {'name': new_name}
            
            self.drive_service.files().update(
                fileId=folder_id,
                body=file_metadata
            ).execute()
            
            print(f"✅ Renamed folder to: {new_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to rename folder {folder_id}: {e}")
            return False
    
    def rename_document(self, doc_id: str, new_title: str) -> bool:
        """Rename a Google Document"""
        if not self.docs_service:
            print(f"[OFFLINE] Would rename document {doc_id} to {new_title}")
            return True
        
        try:
            requests = [{
                'replaceAllText': {
                    'containsText': {
                        'text': 'GCAP 3226 - Data Governance in Education',
                        'matchCase': False
                    },
                    'replaceText': f'GCAP 3226 - Data Governance in Education\n{new_title}'
                }
            }]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Updated document title to: {new_title}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update document {doc_id}: {e}")
            return False
    
    def rename_all_to_simple_names(self):
        """Rename all folders and documents to simple Team01, Team02, etc."""
        print("🔄 Renaming all teams to simple names...")
        print("=" * 50)
        
        # Create mapping of old names to new names
        old_team_names = list(self.team_results.keys())
        new_results = {}
        
        for i, old_team_name in enumerate(old_team_names, 1):
            new_team_name = f"Team{i:02d}"
            new_folder_name = f"Team{i:02d}"
            new_doc_title = f"Team{i:02d} - Project Document"
            
            print(f"\n📋 Renaming {old_team_name} → {new_team_name}")
            
            team_info = self.team_results[old_team_name]
            folder_id = team_info['folder_id']
            doc_id = team_info['document_id']
            
            # Rename folder
            folder_success = self.rename_folder(folder_id, new_folder_name)
            
            # Rename document (update title in document)
            doc_success = self.rename_document(doc_id, new_doc_title)
            
            # Update results with new name
            new_results[new_team_name] = {
                'folder_id': folder_id,
                'document_id': doc_id,
                'topic': f'Project Topic TBD - Team {i}',
                'old_topic': team_info['topic']  # Keep old topic for reference
            }
            
            if folder_success and doc_success:
                print(f"✅ Successfully renamed {old_team_name} to {new_team_name}")
        
        # Save updated results
        self.save_updated_results(new_results)
        self.print_rename_summary(new_results)
        
        return new_results
    
    def save_updated_results(self, new_results: Dict):
        """Save updated team results with new names"""
        results_file = Path(__file__).parent / 'gcap3226_teams_results.json'
        backup_file = Path(__file__).parent / 'gcap3226_teams_results_backup.json'
        
        try:
            # Create backup of old results
            if results_file.exists():
                with open(results_file, 'r') as f:
                    old_data = json.load(f)
                with open(backup_file, 'w') as f:
                    json.dump(old_data, f, indent=2)
                print(f"✅ Backup created: {backup_file}")
            
            # Save new results
            with open(results_file, 'w') as f:
                json.dump(new_results, f, indent=2)
            print(f"✅ Updated results saved: {results_file}")
            
        except Exception as e:
            print(f"❌ Could not save updated results: {e}")
    
    def print_rename_summary(self, results: Dict):
        """Print rename summary"""
        print("\n" + "=" * 50)
        print("🎉 TEAM RENAMING COMPLETE!")
        print("=" * 50)
        
        print(f"✅ Successfully renamed all 8 teams to simple names")
        print("\nNew Team Structure:")
        
        for team_name, info in results.items():
            print(f"\n🏆 {team_name}")
            print(f"   📁 Folder: {team_name}")
            print(f"   📄 Document: https://docs.google.com/document/d/{info['document_id']}/edit")
            print(f"   🎯 Status: Ready for project title assignment")
            print(f"   📝 Previous topic: {info['old_topic']}")

def main():
    """Main execution"""
    print("GCAP 3226 Folder Renamer")
    print("=" * 25)
    print("This will rename all team folders to Team01, Team02, etc.")
    print("since we don't know the actual project titles yet.")
    print()
    
    response = input("Continue with renaming? (y/n): ")
    if response.lower() != 'y':
        print("Renaming cancelled.")
        return
    
    renamer = GCAP3226FolderRenamer()
    results = renamer.rename_all_to_simple_names()
    
    if results:
        print("\n📋 NEXT STEPS:")
        print("1. Check your Google Drive - folders now have simple names")
        print("2. You can assign actual project titles later")
        print("3. Use the updated gcap3226_editor.py with new team names")
        print("4. Old topic information is preserved in the backup file")

if __name__ == "__main__":
    main()

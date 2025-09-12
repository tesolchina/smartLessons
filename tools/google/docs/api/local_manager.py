"""
Local File Manager for GCAP 3226 Team System
Provides local backup and offline functionality for team management
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import shutil

class LocalTeamManager:
    """Manages local copies of team data and provides offline functionality"""
    
    def __init__(self, local_workspace: str = None):
        self.local_workspace = Path(local_workspace) if local_workspace else Path(__file__).parent / "local_teams"
        self.team_data_file = Path(__file__).parent / "team_setup_results.json"
        self.team_data = {}
        self.setup_local_workspace()
        self.load_team_data()
    
    def setup_local_workspace(self):
        """Create local workspace structure"""
        self.local_workspace.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.local_workspace / "documents").mkdir(exist_ok=True)
        (self.local_workspace / "backups").mkdir(exist_ok=True)
        (self.local_workspace / "exports").mkdir(exist_ok=True)
        
        print(f"✅ Local workspace ready: {self.local_workspace}")
    
    def load_team_data(self):
        """Load team data from JSON file"""
        if self.team_data_file.exists():
            try:
                with open(self.team_data_file, 'r') as f:
                    self.team_data = json.load(f)
                print(f"✅ Loaded {len(self.team_data)} teams")
            except Exception as e:
                print(f"⚠️  Could not load team data: {e}")
                self.create_sample_data()
        else:
            print("⚠️  No team data found. Creating sample data.")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample team data for testing"""
        self.team_data = {
            "Team01_DataGovernanceFramework": {
                "folder_id": "sample_folder_01",
                "document_id": "sample_doc_01",
                "topic": "Developing a Data Governance Framework for Educational Institutions"
            },
            "Team02_PrivacyCompliance": {
                "folder_id": "sample_folder_02",
                "document_id": "sample_doc_02",
                "topic": "Student Privacy and Data Protection in Digital Learning"
            },
            # Add more sample teams as needed
        }
        
        # Save sample data
        try:
            with open(self.team_data_file, 'w') as f:
                json.dump(self.team_data, f, indent=2)
            print("✅ Sample team data created")
        except Exception as e:
            print(f"❌ Could not create sample data: {e}")
    
    def create_local_document(self, team_name: str, content: str = None) -> str:
        """Create a local markdown document for a team"""
        if team_name not in self.team_data:
            print(f"❌ Team {team_name} not found")
            return None
        
        doc_path = self.local_workspace / "documents" / f"{team_name}.md"
        
        if content is None:
            content = self.get_default_team_template(team_name)
        
        try:
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Created local document: {doc_path}")
            return str(doc_path)
            
        except Exception as e:
            print(f"❌ Failed to create local document: {e}")
            return None
    
    def get_default_team_template(self, team_name: str) -> str:
        """Generate default content template for a team"""
        team_info = self.team_data.get(team_name, {})
        topic = team_info.get('topic', 'Unknown Topic')
        
        template = f"""# GCAP 3226 - Data Governance in Education
## Team: {team_name}

**Project Topic:** {topic}

**Focus Area:** {team_info.get('focus', 'To be determined')}

## Team Members
- [ ] Student 1 - Name: _____________ Email: _____________
- [ ] Student 2 - Name: _____________ Email: _____________
- [ ] Student 3 - Name: _____________ Email: _____________
- [ ] Student 4 - Name: _____________ Email: _____________
- [ ] Student 5 - Name: _____________ Email: _____________

## Project Timeline
- **Week 1-2:** Literature review and problem definition
- **Week 3-4:** Framework development
- **Week 5-6:** Implementation planning
- **Week 7-8:** Case study development
- **Week 9-10:** Final presentation preparation

## Deliverables
1. **Literature Review** (Week 2)
2. **Framework Proposal** (Week 4)
3. **Implementation Plan** (Week 6)
4. **Case Study Analysis** (Week 8)
5. **Final Presentation** (Week 10)

## Meeting Notes

### Meeting 1 - Date: _________
**Attendees:** ________________

**Agenda:**
- 
- 
- 

**Discussion:**


**Action Items:**
- [ ] Task 1 - Assigned to: _______ Due: _______
- [ ] Task 2 - Assigned to: _______ Due: _______
- [ ] Task 3 - Assigned to: _______ Due: _______

---

## Resources
- **Course Materials:** [Link to Moodle]
- **Shared Drive:** [Google Drive Folder]
- **Team Communication:** [Slack/Email/Teams]

## Project Notes
(Use this space for ongoing project notes and documentation)

## References
(Add your research references here)

---
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return template
    
    def read_local_document(self, team_name: str) -> Optional[str]:
        """Read content from local team document"""
        doc_path = self.local_workspace / "documents" / f"{team_name}.md"
        
        if not doc_path.exists():
            print(f"⚠️  Local document not found for {team_name}")
            return None
        
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"✅ Read {len(content)} characters from local document")
            return content
            
        except Exception as e:
            print(f"❌ Failed to read local document: {e}")
            return None
    
    def update_local_document(self, team_name: str, new_content: str) -> bool:
        """Update content in local team document"""
        doc_path = self.local_workspace / "documents" / f"{team_name}.md"
        
        # Create backup first
        if doc_path.exists():
            self.backup_document(team_name)
        
        try:
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Updated local document for {team_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update local document: {e}")
            return False
    
    def backup_document(self, team_name: str) -> bool:
        """Create a backup of team document"""
        doc_path = self.local_workspace / "documents" / f"{team_name}.md"
        
        if not doc_path.exists():
            return False
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.local_workspace / "backups" / f"{team_name}_{timestamp}.md"
        
        try:
            shutil.copy2(doc_path, backup_path)
            print(f"✅ Backup created: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create backup: {e}")
            return False
    
    def create_all_local_documents(self):
        """Create local documents for all teams"""
        print("📝 Creating local documents for all teams...")
        print("=" * 50)
        
        created_count = 0
        
        for team_name in self.team_data.keys():
            doc_path = self.create_local_document(team_name)
            if doc_path:
                created_count += 1
        
        print(f"\n✅ Created {created_count}/{len(self.team_data)} local documents")
        print(f"📁 Documents location: {self.local_workspace / 'documents'}")
    
    def export_team_summary(self) -> str:
        """Export a summary of all teams to a markdown file"""
        summary_path = self.local_workspace / "exports" / f"team_summary_{datetime.now().strftime('%Y%m%d')}.md"
        
        summary_content = f"""# GCAP 3226 - Team Summary
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Course Overview
**Course:** GCAP 3226 - Data Governance in Education  
**Total Teams:** {len(self.team_data)}

## Team List

"""
        
        for team_name, info in self.team_data.items():
            summary_content += f"""### {team_name}
**Topic:** {info.get('topic', 'Unknown')}  
**Folder ID:** `{info.get('folder_id', 'N/A')}`  
**Document ID:** `{info.get('document_id', 'N/A')}`  
**Local Document:** `{team_name}.md`

---

"""
        
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            print(f"✅ Team summary exported: {summary_path}")
            return str(summary_path)
            
        except Exception as e:
            print(f"❌ Failed to export team summary: {e}")
            return None
    
    def list_local_files(self):
        """List all local files and their status"""
        print("📂 Local Team Files")
        print("=" * 30)
        
        documents_dir = self.local_workspace / "documents"
        backups_dir = self.local_workspace / "backups"
        
        print("\n📄 Documents:")
        if documents_dir.exists():
            for doc_file in documents_dir.glob("*.md"):
                size = doc_file.stat().st_size
                modified = datetime.fromtimestamp(doc_file.stat().st_mtime)
                print(f"  ✅ {doc_file.name} ({size} bytes, modified: {modified.strftime('%Y-%m-%d %H:%M')})")
        else:
            print("  (No documents found)")
        
        print("\n💾 Backups:")
        if backups_dir.exists():
            backup_files = list(backups_dir.glob("*.md"))
            if backup_files:
                for backup_file in sorted(backup_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                    modified = datetime.fromtimestamp(backup_file.stat().st_mtime)
                    print(f"  📦 {backup_file.name} ({modified.strftime('%Y-%m-%d %H:%M')})")
                
                if len(backup_files) > 5:
                    print(f"  ... and {len(backup_files) - 5} more backups")
            else:
                print("  (No backups found)")

def main():
    """Example usage of LocalTeamManager"""
    print("GCAP 3226 Local Team Manager")
    print("=" * 35)
    
    manager = LocalTeamManager()
    
    # Create all local documents
    manager.create_all_local_documents()
    
    # List files
    manager.list_local_files()
    
    # Export summary
    manager.export_team_summary()
    
    print(f"\n🎉 Local team management setup complete!")
    print(f"📁 Workspace: {manager.local_workspace}")

if __name__ == "__main__":
    main()

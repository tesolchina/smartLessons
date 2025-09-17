#!/usr/bin/env python3
"""
GCAP 3056 Google Drive Sync Manager
Works with local Google Drive sync folders to create and manage info gathering documents

Usage:
    python gcap3056_drive_sync_manager.py --create-info-gathering-docs
    python gcap3056_drive_sync_manager.py --list-project-folders
    python gcap3056_drive_sync_manager.py --sync-local-to-drive
"""
import sys
import os
import argparse
import json
from pathlib import Path
from datetime import datetime
import shutil

# Google Drive sync path (local Google Drive folder)
GOOGLE_DRIVE_BASE = Path.home() / "Library/CloudStorage/GoogleDrive-simonwanghkteacher@gmail.com/My Drive"

# Project configurations
PROJECT_DOCS = {
    "energy_poverty": {
        "url": "https://docs.google.com/document/d/1IPVnQEKA3cKMCaYWtc4R8-PcFq7n79MYrMq8QLzAHhk/edit?tab=t.0",
        "doc_id": "1IPVnQEKA3cKMCaYWtc4R8-PcFq7n79MYrMq8QLzAHhk",
        "local_dir": "Projects and teams/energy_poverty",
        "drive_folder": None  # To be discovered
    },
    "hko_chatbot": {
        "url": "https://docs.google.com/document/d/1E6NLBbnTE1WNS8aU0xwvZOls6CVLe_0i5LHyjOQ76iw/edit?tab=t.0",
        "doc_id": "1E6NLBbnTE1WNS8aU0xwvZOls6CVLe_0i5LHyjOQ76iw",
        "local_dir": "Projects and teams/hko_chatbot",
        "drive_folder": None
    },
    "chronic_disease_co_care": {
        "url": "https://docs.google.com/document/d/1i0efENpeAYYNchaCSvKwN2HEL2YXGVXYUr4-Lf4X7RA/edit?tab=t.0",
        "doc_id": "1i0efENpeAYYNchaCSvKwN2HEL2YXGVXYUr4-Lf4X7RA",
        "local_dir": "Projects and teams/chronic_disease_co_care",
        "drive_folder": None
    },
    "anti_scamming_education": {
        "url": "https://docs.google.com/document/d/1MQ3Gk1kyNvaw7e-Tc72y41UKMrztIZ21Cj-1STsWZNA/edit?tab=t.8lpba9bjqpel#heading=h.s640o2lk1eg6",
        "doc_id": "1MQ3Gk1kyNvaw7e-Tc72y41UKMrztIZ21Cj-1STsWZNA",
        "local_dir": "Projects and teams/anti_scamming_education",
        "drive_folder": None
    },
    "emergency_alert_system": {
        "url": "https://docs.google.com/document/d/19ND3APGCVjd-UC1ie0kurt9YXlJw-smf1EfuF6szMJ0/edit?tab=t.0",
        "doc_id": "19ND3APGCVjd-UC1ie0kurt9YXlJw-smf1EfuF6szMJ0",
        "local_dir": "Projects and teams/emergency_alert_system",
        "drive_folder": None
    }
}

class GCAP3056DriveSyncManager:
    def __init__(self):
        self.drive_base = GOOGLE_DRIVE_BASE
        print(f"📁 Google Drive base: {self.drive_base}")
        
        if not self.drive_base.exists():
            print(f"❌ Google Drive folder not found: {self.drive_base}")
            print("Please ensure Google Drive desktop app is installed and syncing.")
            sys.exit(1)
    
    def find_project_folders(self):
        """Find project folders in Google Drive"""
        print("🔍 Searching for project folders in Google Drive...")
        
        # Common folder patterns to search
        search_patterns = [
            "GCAP*3056*",
            "*GCAP*3056*",
            "Projects*",
            "*Projects*"
        ]
        
        found_folders = []
        
        for pattern in search_patterns:
            for folder in self.drive_base.glob(pattern):
                if folder.is_dir():
                    found_folders.append(folder)
                    print(f"📂 Found: {folder.relative_to(self.drive_base)}")
        
        # Look for subfolders that might contain our projects
        for folder in found_folders:
            for subfolder in folder.rglob("*"):
                if subfolder.is_dir():
                    folder_name = subfolder.name.lower()
                    for project_name in PROJECT_DOCS.keys():
                        if any(word in folder_name for word in project_name.split('_')):
                            print(f"  📁 Potential project folder: {subfolder.relative_to(self.drive_base)}")
                            PROJECT_DOCS[project_name]['drive_folder'] = subfolder
        
        return found_folders
    
    def list_google_drive_structure(self):
        """List the structure of Google Drive to help identify project folders"""
        print("📋 Google Drive structure:")
        
        # List top-level folders
        for item in sorted(self.drive_base.iterdir()):
            if item.is_dir():
                print(f"📂 {item.name}")
                # Look for course-related folders
                if any(keyword in item.name.lower() for keyword in ['gcap', 'course', 'class', 'project']):
                    for subitem in sorted(item.iterdir())[:10]:  # Limit to first 10 items
                        prefix = "📂" if subitem.is_dir() else "📄"
                        print(f"  {prefix} {subitem.name}")
    
    def create_info_gathering_in_drive(self, project_name):
        """Create info gathering document in Google Drive folder"""
        if project_name not in PROJECT_DOCS:
            print(f"❌ Project '{project_name}' not found")
            return None
        
        drive_folder = PROJECT_DOCS[project_name]['drive_folder']
        if not drive_folder or not drive_folder.exists():
            print(f"❌ Google Drive folder not found for {project_name}")
            print(f"   Please manually locate and set the folder path")
            return None
        
        # Read content from local info gathering file
        local_file = Path(PROJECT_DOCS[project_name]['local_dir']) / "info_gathering.md"
        if not local_file.exists():
            print(f"❌ Local info gathering file not found: {local_file}")
            return None
        
        with open(local_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create Google Drive version
        drive_file = drive_folder / "Info_Gathering.md"
        
        # Add sync header
        sync_header = f"""<!-- GOOGLE DRIVE SYNC -->
<!-- Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->
<!-- Project: {project_name} -->
<!-- Local file: {local_file} -->

"""
        
        drive_content = sync_header + content
        
        with open(drive_file, 'w', encoding='utf-8') as f:
            f.write(drive_content)
        
        print(f"✅ Created: {drive_file}")
        print(f"🔄 Will sync to Google Drive automatically")
        
        # Update local file with Drive location
        updated_content = content.replace("<!-- Google Doc ID: TBD -->", f"<!-- Google Drive File: {drive_file} -->")
        updated_content = updated_content.replace("<!-- Google Doc URL: TBD -->", f"<!-- Google Drive Path: {drive_file.relative_to(self.drive_base)} -->")
        
        with open(local_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        return drive_file
    
    def sync_local_to_drive(self):
        """Copy all local info gathering files to Google Drive folders"""
        print("🔄 Syncing local info gathering files to Google Drive...")
        
        # First find project folders
        self.find_project_folders()
        
        results = {}
        
        for project_name in PROJECT_DOCS.keys():
            print(f"\n📁 Processing {project_name}...")
            drive_file = self.create_info_gathering_in_drive(project_name)
            
            if drive_file:
                results[project_name] = {
                    'drive_file': str(drive_file),
                    'drive_relative_path': str(drive_file.relative_to(self.drive_base)),
                    'status': 'success'
                }
            else:
                results[project_name] = {
                    'status': 'failed',
                    'reason': 'Drive folder not found'
                }
        
        # Save results
        results_file = Path("drive_sync_results.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Results saved to {results_file}")
        return results
    
    def manual_folder_setup(self):
        """Help user manually set up project folder paths"""
        print("🔧 Manual folder setup mode")
        print("Please provide the Google Drive folder paths for each project:")
        
        for project_name in PROJECT_DOCS.keys():
            print(f"\n📁 Project: {project_name}")
            print(f"   Local dir: {PROJECT_DOCS[project_name]['local_dir']}")
            
            # Suggest some possible paths
            print("   Suggested Google Drive paths to check:")
            for possible_path in [
                self.drive_base / "GCAP 3056" / project_name.replace('_', ' ').title(),
                self.drive_base / "GCAP3056" / project_name,
                self.drive_base / "Projects" / project_name,
                self.drive_base / f"GCAP 3056 - Projects" / project_name.replace('_', ' ').title()
            ]:
                if possible_path.exists():
                    print(f"   ✅ Found: {possible_path}")
                    PROJECT_DOCS[project_name]['drive_folder'] = possible_path
                    break
                else:
                    print(f"   ❌ Not found: {possible_path}")
        
        # Save configuration
        config_file = Path("drive_folder_config.json")
        config_data = {}
        for project_name, info in PROJECT_DOCS.items():
            config_data[project_name] = {
                'drive_folder': str(info['drive_folder']) if info['drive_folder'] else None,
                'local_dir': info['local_dir']
            }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        
        print(f"\n💾 Configuration saved to {config_file}")

def main():
    parser = argparse.ArgumentParser(description='GCAP 3056 Google Drive Sync Manager')
    
    # Operations
    parser.add_argument('--list-drive-structure', action='store_true', help='List Google Drive folder structure')
    parser.add_argument('--find-project-folders', action='store_true', help='Find project folders in Google Drive')
    parser.add_argument('--manual-setup', action='store_true', help='Manual folder setup mode')
    parser.add_argument('--sync-local-to-drive', action='store_true', help='Sync local files to Google Drive')
    parser.add_argument('--create-info-gathering-docs', action='store_true', help='Create info gathering docs in Drive')
    
    args = parser.parse_args()
    
    if not any([args.list_drive_structure, args.find_project_folders, args.manual_setup, 
                args.sync_local_to_drive, args.create_info_gathering_docs]):
        print("❌ Please specify an operation")
        parser.print_help()
        sys.exit(1)
    
    manager = GCAP3056DriveSyncManager()
    
    if args.list_drive_structure:
        manager.list_google_drive_structure()
    
    elif args.find_project_folders:
        manager.find_project_folders()
    
    elif args.manual_setup:
        manager.manual_folder_setup()
    
    elif args.sync_local_to_drive or args.create_info_gathering_docs:
        manager.sync_local_to_drive()

if __name__ == "__main__":
    main()

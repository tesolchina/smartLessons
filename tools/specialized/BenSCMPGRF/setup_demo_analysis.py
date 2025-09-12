#!/usr/bin/env python3
"""
Create SimonNotes Subfolder in Ben's Research Folder and Setup Demo Analysis
"""

import sys
from pathlib import Path

# Add GoogleDocsAPI to path
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

try:
    from auth_setup import authenticate_google_apis
    from googleapiclient.discovery import build
    APIS_AVAILABLE = True
except ImportError as e:
    print(f"Google APIs not available: {e}")
    APIS_AVAILABLE = False

def create_simon_notes_subfolder():
    """Create SimonNotes subfolder in Ben's research folder"""
    
    if not APIS_AVAILABLE:
        print("📁 [OFFLINE] Would create SimonNotes subfolder")
        return "offline_subfolder_id"
    
    try:
        creds = authenticate_google_apis()
        if not creds:
            print("❌ Authentication failed")
            return None
            
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Ben's research folder ID
        BEN_RESEARCH_FOLDER = "1Qt6Ak8sHMd7ZpX5T-p_4-pBH0r98L3rs"
        
        # Check if SimonNotes subfolder already exists
        results = drive_service.files().list(
            q=f"name='SimonNotes' and '{BEN_RESEARCH_FOLDER}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
            fields="files(id, name)"
        ).execute()
        
        folders = results.get('files', [])
        
        if folders:
            subfolder_id = folders[0]['id']
            print(f"✅ Found existing SimonNotes subfolder: {subfolder_id}")
            return subfolder_id
        else:
            # Create new SimonNotes subfolder
            folder_metadata = {
                'name': 'SimonNotes',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [BEN_RESEARCH_FOLDER]
            }
            
            folder = drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            subfolder_id = folder.get('id')
            print(f"✅ Created SimonNotes subfolder: {subfolder_id}")
            return subfolder_id
                
    except Exception as e:
        print(f"❌ Error creating SimonNotes subfolder: {e}")
        return None

def setup_demo_analysis_folder():
    """Create local demo analysis folder structure"""
    
    project_path = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/BenSCMPGRF")
    demo_folder = project_path / "demo_analysis"
    
    # Create folder structure
    folders_to_create = [
        demo_folder,
        demo_folder / "sample_letters",
        demo_folder / "llm_outputs", 
        demo_folder / "analysis_reports",
        demo_folder / "sync_to_drive"
    ]
    
    for folder in folders_to_create:
        folder.mkdir(exist_ok=True)
    
    print(f"✅ Demo analysis folder created: {demo_folder}")
    return demo_folder

def main():
    print("=== Setting up SimonNotes Subfolder & Demo Analysis ===")
    print()
    
    # Create SimonNotes subfolder
    print("1️⃣ Creating SimonNotes subfolder in Ben's research folder...")
    subfolder_id = create_simon_notes_subfolder()
    
    # Setup local demo analysis folder
    print("\n2️⃣ Setting up local demo analysis folder...")
    demo_folder = setup_demo_analysis_folder()
    
    print(f"\n✅ Setup complete!")
    if subfolder_id and subfolder_id != "offline_subfolder_id":
        print(f"📂 SimonNotes subfolder: https://drive.google.com/drive/folders/{subfolder_id}")
    print(f"📁 Local demo folder: {demo_folder}")
    
    return subfolder_id, demo_folder

if __name__ == "__main__":
    main()

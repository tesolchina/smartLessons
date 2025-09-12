#!/usr/bin/env python3
"""
Move Google Docs to Ben's Research Folder
Move collaboration documents to: https://drive.google.com/drive/u/0/folders/1Qt6Ak8sHMd7ZpX5T-p_4-pBH0r98L3rs
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

def move_docs_to_ben_folder():
    """Move the collaboration documents to Ben's research folder"""
    
    if not APIS_AVAILABLE:
        print("❌ Google APIs not available")
        return
    
    try:
        # Authenticate
        creds = authenticate_google_apis()
        if not creds:
            print("❌ Authentication failed")
            return
            
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Target folder ID from Ben's link
        BEN_RESEARCH_FOLDER = "1Qt6Ak8sHMd7ZpX5T-p_4-pBH0r98L3rs"
        
        # Document IDs from our previous upload
        documents_to_move = {
            "SCMP_GRF_LLM_Analysis_Project_Plan.md": "1WpGg55XJeHizGv9DvOQmedUZfwiFIAJI",
            "SCMP GRF Project Discussion": "1uZN0Wqh3tKz3uNo9c98brvKUpYTREcXzCjtsPfgesTk"
        }
        
        print("📁 Moving documents to Ben's research folder...")
        print(f"Target folder: https://drive.google.com/drive/folders/{BEN_RESEARCH_FOLDER}")
        print()
        
        for doc_name, doc_id in documents_to_move.items():
            try:
                # Get current parents
                file = drive_service.files().get(fileId=doc_id, fields='parents').execute()
                previous_parents = ",".join(file.get('parents'))
                
                # Move the file to Ben's folder
                file = drive_service.files().update(
                    fileId=doc_id,
                    addParents=BEN_RESEARCH_FOLDER,
                    removeParents=previous_parents,
                    fields='id, parents'
                ).execute()
                
                print(f"✅ Moved: {doc_name}")
                
            except Exception as e:
                print(f"❌ Failed to move {doc_name}: {e}")
        
        print("\n🎉 Documents moved to Ben's research folder!")
        print(f"📂 Access folder: https://drive.google.com/drive/folders/{BEN_RESEARCH_FOLDER}")
        
    except Exception as e:
        print(f"❌ Error moving documents: {e}")

def main():
    print("=== Moving SCMP GRF Docs to Ben's Research Folder ===")
    print()
    move_docs_to_ben_folder()

if __name__ == "__main__":
    main()

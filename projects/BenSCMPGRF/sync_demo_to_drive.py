#!/usr/bin/env python3
"""
Sync Demo Analysis Results to Ben's SimonNotes Subfolder
"""

import sys
from pathlib import Path
import shutil

# Add GoogleDocsAPI to path
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

try:
    from auth_setup import authenticate_google_apis
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    APIS_AVAILABLE = True
except ImportError as e:
    print(f"Google APIs not available: {e}")
    APIS_AVAILABLE = False

def sync_demo_to_drive():
    """Upload demo analysis results to SimonNotes subfolder"""
    
    if not APIS_AVAILABLE:
        print("📤 [OFFLINE] Would sync demo results to Google Drive")
        return
    
    try:
        creds = authenticate_google_apis()
        if not creds:
            print("❌ Authentication failed")
            return
            
        drive_service = build('drive', 'v3', credentials=creds)
        
        # SimonNotes subfolder ID (from previous setup)
        SIMON_NOTES_SUBFOLDER = "1kKgAXnYvHvONE467ZvdYFAW306PrVSZw"
        
        # Local demo analysis files to upload
        demo_dir = Path("./demo_analysis")
        files_to_upload = [
            demo_dir / "sample_letters" / "sample_letters_2020.md",
            demo_dir / "llm_outputs" / "demo_analysis_report_20250910_074138.md",
            demo_dir / "llm_outputs" / "demo_analysis_results_20250910_074138.json"
        ]
        
        print("📤 Uploading demo analysis to SimonNotes subfolder...")
        print(f"Target: https://drive.google.com/drive/folders/{SIMON_NOTES_SUBFOLDER}")
        print()
        
        uploaded_files = []
        
        for file_path in files_to_upload:
            if not file_path.exists():
                print(f"⚠️  File not found: {file_path}")
                continue
            
            try:
                # File metadata
                file_metadata = {
                    'name': file_path.name,
                    'parents': [SIMON_NOTES_SUBFOLDER]
                }
                
                # Determine MIME type
                if file_path.suffix == '.md':
                    mimetype = 'text/markdown'
                elif file_path.suffix == '.json':
                    mimetype = 'application/json'
                else:
                    mimetype = 'text/plain'
                
                # Upload file
                media = MediaFileUpload(
                    str(file_path),
                    mimetype=mimetype,
                    resumable=True
                )
                
                file = drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,name,webViewLink'
                ).execute()
                
                uploaded_files.append({
                    'name': file.get('name'),
                    'id': file.get('id'),
                    'link': file.get('webViewLink')
                })
                
                print(f"✅ Uploaded: {file_path.name}")
                
            except Exception as e:
                print(f"❌ Failed to upload {file_path.name}: {e}")
        
        print(f"\n🎉 Demo sync complete! {len(uploaded_files)} files uploaded")
        print(f"📂 View in SimonNotes: https://drive.google.com/drive/folders/{SIMON_NOTES_SUBFOLDER}")
        
        return uploaded_files
        
    except Exception as e:
        print(f"❌ Error syncing to Google Drive: {e}")
        return []

def create_local_sync_folder():
    """Create sync_to_drive folder with demo results"""
    
    demo_dir = Path("./demo_analysis")
    sync_dir = demo_dir / "sync_to_drive"
    sync_dir.mkdir(exist_ok=True)
    
    # Copy key files to sync folder
    files_to_copy = [
        (demo_dir / "sample_letters" / "sample_letters_2020.md", "Sample_SCMP_Letters_2020.md"),
        (demo_dir / "llm_outputs" / "demo_analysis_report_20250910_074138.md", "LLM_Demo_Analysis_Report.md"),
        (demo_dir / "llm_outputs" / "demo_analysis_results_20250910_074138.json", "LLM_Demo_Results.json")
    ]
    
    for source, target_name in files_to_copy:
        if source.exists():
            target = sync_dir / target_name
            shutil.copy2(source, target)
            print(f"📄 Copied to sync: {target_name}")
    
    print(f"✅ Local sync folder ready: {sync_dir}")
    return sync_dir

def main():
    print("=== Syncing Demo Analysis Results ===")
    print()
    
    # Create local sync folder
    print("1️⃣ Preparing files for sync...")
    sync_dir = create_local_sync_folder()
    
    # Upload to Google Drive
    print("\n2️⃣ Uploading to Ben's SimonNotes subfolder...")
    uploaded = sync_demo_to_drive()
    
    print(f"\n✅ Sync complete!")
    print(f"📁 Local: {sync_dir}")
    if uploaded:
        print(f"☁️  Remote: {len(uploaded)} files in SimonNotes subfolder")
    
    print(f"\n💡 Demo showcases:")
    print(f"   - 3 citizenship discourse types identified")
    print(f"   - Detailed linguistic evidence extraction")
    print(f"   - Argumentation structure analysis") 
    print(f"   - COVID-19 pandemic discourse insights")
    print(f"   - Ready for full corpus analysis scaling")

if __name__ == "__main__":
    main()

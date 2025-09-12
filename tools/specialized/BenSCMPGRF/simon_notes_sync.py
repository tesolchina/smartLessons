#!/usr/bin/env python3
"""
SimonNotes Google Drive Sync
Monitor and sync the SimonNotes folder for SCMP GRF project collaboration
"""

import os
import shutil
import time
from pathlib import Path
from datetime import datetime

# Paths - Update these based on your Google Drive setup
GOOGLE_DRIVE_SIMON_NOTES = Path.home() / "Library/CloudStorage/GoogleDrive-simonwanghkteacher@gmail.com/My Drive/SimonNotes"
PROJECT_PATH = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/BenSCMPGRF")
SYNC_FOLDER = PROJECT_PATH / "synced_from_drive"

def setup_sync_folder():
    """Create sync folder if it doesn't exist"""
    SYNC_FOLDER.mkdir(exist_ok=True)
    print(f"✓ Sync folder ready: {SYNC_FOLDER}")

def sync_simon_notes():
    """Sync documents from SimonNotes Google Drive folder"""
    
    if not GOOGLE_DRIVE_SIMON_NOTES.exists():
        print(f"❌ SimonNotes folder not found in Google Drive")
        print(f"Expected: {GOOGLE_DRIVE_SIMON_NOTES}")
        print("\nTip: Make sure Google Drive is synced and SimonNotes folder exists")
        return 0
    
    print(f"📁 Syncing from: {GOOGLE_DRIVE_SIMON_NOTES}")
    print(f"📁 Syncing to: {SYNC_FOLDER}")
    
    synced_count = 0
    
    # Supported file types for academic collaboration
    supported_extensions = {
        '.pdf', '.docx', '.doc', '.txt', '.md', 
        '.csv', '.xlsx', '.json', '.py'
    }
    
    for file_path in GOOGLE_DRIVE_SIMON_NOTES.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            # Calculate relative path to preserve folder structure
            relative_path = file_path.relative_to(GOOGLE_DRIVE_SIMON_NOTES)
            local_file_path = SYNC_FOLDER / relative_path
            
            # Create directory if needed
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file if it's newer or doesn't exist
            if not local_file_path.exists() or file_path.stat().st_mtime > local_file_path.stat().st_mtime:
                shutil.copy2(file_path, local_file_path)
                print(f"📄 Synced: {relative_path}")
                synced_count += 1
    
    if synced_count > 0:
        print(f"✅ Sync complete! {synced_count} files updated.")
    else:
        print("✅ All files already up to date.")
    
    return synced_count

def list_synced_files():
    """List all synced files with details"""
    print(f"\n📋 Files in {SYNC_FOLDER.name}:")
    
    if not SYNC_FOLDER.exists():
        print("No synced files yet.")
        return
    
    files_found = False
    for file_path in SYNC_FOLDER.rglob('*'):
        if file_path.is_file():
            files_found = True
            relative_path = file_path.relative_to(SYNC_FOLDER)
            size_kb = file_path.stat().st_size // 1024
            modified = datetime.fromtimestamp(file_path.stat().st_mtime)
            print(f"  📄 {relative_path} ({size_kb} KB, {modified.strftime('%Y-%m-%d %H:%M')})")
    
    if not files_found:
        print("  No files synced yet.")

def watch_for_updates():
    """Continuous monitoring mode (optional)"""
    print("\n🔄 Starting continuous sync monitoring...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            synced_count = sync_simon_notes()
            if synced_count > 0:
                print(f"⚡ {synced_count} new/updated files synced at {datetime.now().strftime('%H:%M:%S')}")
            
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        print("\n⏹️  Sync monitoring stopped")

def generate_sync_report():
    """Generate a summary of what's been synced"""
    report_file = PROJECT_PATH / "sync_report.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# SimonNotes Sync Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**Source:** {GOOGLE_DRIVE_SIMON_NOTES}  \n")
        f.write(f"**Local Sync:** {SYNC_FOLDER}  \n\n")
        
        f.write("## Synced Files\n\n")
        
        if SYNC_FOLDER.exists():
            files = list(SYNC_FOLDER.rglob('*'))
            files = [f for f in files if f.is_file()]
            
            if files:
                for file_path in sorted(files):
                    relative_path = file_path.relative_to(SYNC_FOLDER)
                    size_kb = file_path.stat().st_size // 1024
                    modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                    f.write(f"- **{relative_path}** ({size_kb} KB, {modified.strftime('%Y-%m-%d %H:%M')})  \n")
            else:
                f.write("No files synced yet.\n")
        else:
            f.write("Sync folder not initialized.\n")
        
        f.write(f"\n## Next Steps\n\n")
        f.write(f"1. Check synced files in `{SYNC_FOLDER.name}/`  \n")
        f.write(f"2. Review any new literature or documents from Ben  \n")
        f.write(f"3. Update project analysis with new information  \n")
        f.write(f"4. Run sync again to get latest updates  \n")
    
    print(f"📊 Sync report saved: {report_file}")

def main():
    """Main sync function"""
    print("🔄 SimonNotes Google Drive Sync for SCMP GRF Project")
    print("=" * 55)
    
    setup_sync_folder()
    synced_count = sync_simon_notes()
    list_synced_files()
    generate_sync_report()
    
    if synced_count > 0:
        print(f"\n✨ Found {synced_count} new/updated files from Ben's collaboration!")
    
    print(f"\n💡 Tips:")
    print(f"   - Run this script regularly to get Ben's updates")  
    print(f"   - Check {SYNC_FOLDER.name}/ for new literature and documents")
    print(f"   - Add --watch flag for continuous monitoring")
    
    # Optional: continuous monitoring
    import sys
    if '--watch' in sys.argv:
        watch_for_updates()

if __name__ == "__main__":
    main()

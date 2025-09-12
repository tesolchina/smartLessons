#!/usr/bin/env python3
"""
Google Drive Document Sync
Simple script to monitor and sync documents from Google Drive to local DailyAssistant project
"""

import os
import shutil
import time
from pathlib import Path
from datetime import datetime

# Paths
GOOGLE_DRIVE_PATH = Path.home() / "Library/CloudStorage/GoogleDrive-simonwanghkteacher@gmail.com/My Drive/DailyAssistant"
LOCAL_PROJECT_PATH = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant")
SYNC_FOLDER = LOCAL_PROJECT_PATH / "synced_docs"

def setup_sync_folder():
    """Create sync folder if it doesn't exist"""
    SYNC_FOLDER.mkdir(exist_ok=True)
    print(f"✓ Sync folder ready: {SYNC_FOLDER}")

def sync_documents():
    """Sync documents from Google Drive to local folder"""
    if not GOOGLE_DRIVE_PATH.exists():
        print(f"❌ Google Drive folder not found: {GOOGLE_DRIVE_PATH}")
        return
    
    print(f"📁 Syncing from: {GOOGLE_DRIVE_PATH}")
    print(f"📁 Syncing to: {SYNC_FOLDER}")
    
    synced_count = 0
    
    # Supported file types
    supported_extensions = {'.pdf', '.docx', '.txt', '.md', '.doc'}
    
    for file_path in GOOGLE_DRIVE_PATH.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            # Calculate relative path to preserve folder structure
            relative_path = file_path.relative_to(GOOGLE_DRIVE_PATH)
            local_file_path = SYNC_FOLDER / relative_path
            
            # Create directory if needed
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file if it's newer or doesn't exist
            if not local_file_path.exists() or file_path.stat().st_mtime > local_file_path.stat().st_mtime:
                shutil.copy2(file_path, local_file_path)
                print(f"📄 Synced: {relative_path}")
                synced_count += 1
    
    print(f"✅ Sync complete! {synced_count} files updated.")

def list_synced_files():
    """List all synced files"""
    print("\n📋 Currently synced files:")
    if not SYNC_FOLDER.exists():
        print("No synced files yet.")
        return
    
    for file_path in SYNC_FOLDER.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(SYNC_FOLDER)
            size_kb = file_path.stat().st_size // 1024
            print(f"  - {relative_path} ({size_kb} KB)")

def main():
    """Main function"""
    print("🔄 Google Drive Sync for DailyAssistant")
    print("=" * 50)
    
    setup_sync_folder()
    sync_documents()
    list_synced_files()
    
    print(f"\n💡 Tip: Add documents to {GOOGLE_DRIVE_PATH}")
    print("💡 Then run this script again to sync them locally!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Move GCAP3226 materials from LANG0036 project to GCAP3226 archive folder
"""

import os
import shutil
from pathlib import Path

def move_gcap3226_materials():
    """Move GCAP3226 materials to the archive folder"""
    
    # Source and destination paths
    source_dir = Path("/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0036/GCAP3226_materials")
    dest_dir = Path("/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/99_archive/Misc")
    
    print(f"🚀 Moving GCAP3226 materials from LANG0036 to archive...")
    print(f"📂 Source: {source_dir}")
    print(f"📁 Destination: {dest_dir}")
    print()
    
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return False
    
    if not dest_dir.exists():
        print(f"❌ Destination directory not found: {dest_dir}")
        return False
    
    # Count files before moving
    file_count = 0
    for root, dirs, files in os.walk(source_dir):
        file_count += len(files)
    
    print(f"📊 Found {file_count} files to move")
    print()
    
    moved_files = 0
    moved_folders = 0
    
    try:
        # Move each subdirectory and its contents
        for item in source_dir.iterdir():
            if item.is_dir():
                dest_path = dest_dir / item.name
                print(f"📁 Moving folder: {item.name}")
                
                # Count files in this folder
                folder_file_count = 0
                for root, dirs, files in os.walk(item):
                    folder_file_count += len(files)
                
                # Move the entire directory
                shutil.move(str(item), str(dest_path))
                moved_folders += 1
                moved_files += folder_file_count
                print(f"   ✅ Moved {folder_file_count} files")
                
            elif item.is_file():
                dest_path = dest_dir / item.name
                print(f"📄 Moving file: {item.name}")
                shutil.move(str(item), str(dest_path))
                moved_files += 1
                print(f"   ✅ Moved")
        
        print()
        print(f"✅ Successfully moved {moved_files} files in {moved_folders} folders")
        
        # Remove the now-empty source directory
        if source_dir.exists() and not any(source_dir.iterdir()):
            source_dir.rmdir()
            print(f"🗑️  Removed empty source directory: {source_dir.name}")
        
        print()
        print("🎉 GCAP3226 materials successfully moved to archive!")
        return True
        
    except Exception as e:
        print(f"❌ Error moving files: {str(e)}")
        return False

def verify_move():
    """Verify the move was successful"""
    dest_dir = Path("/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/99_archive/Misc")
    source_dir = Path("/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0036/GCAP3226_materials")
    
    print("\n🔍 Verification:")
    
    # Count files in destination
    dest_file_count = 0
    if dest_dir.exists():
        for root, dirs, files in os.walk(dest_dir):
            dest_file_count += len(files)
    
    print(f"📊 Files in destination: {dest_file_count}")
    
    # Check if source directory still exists
    if source_dir.exists():
        source_file_count = 0
        for root, dirs, files in os.walk(source_dir):
            source_file_count += len(files)
        print(f"⚠️  Files remaining in source: {source_file_count}")
    else:
        print("✅ Source directory removed successfully")
    
    # List destination contents
    if dest_dir.exists():
        print(f"\n📁 Contents of {dest_dir}:")
        for item in sorted(dest_dir.iterdir()):
            if item.is_dir():
                file_count = sum(1 for _ in item.rglob('*') if _.is_file())
                print(f"   📁 {item.name}/ ({file_count} files)")
            else:
                print(f"   📄 {item.name}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 GCAP3226 Materials Archive Transfer")
    print("=" * 60)
    
    success = move_gcap3226_materials()
    
    if success:
        verify_move()
    
    print("\n" + "=" * 60)
    print("✅ Transfer complete!" if success else "❌ Transfer failed!")
    print("=" * 60)
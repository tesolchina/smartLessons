#!/usr/bin/env python3
"""
GCAP3226 Materials Preview Script

This script previews what would be moved during consolidation without actually moving anything.
Use this to review the consolidation plan before running the actual consolidation.

Author: AI Assistant
Date: 2025-09-22
"""

import os
from pathlib import Path

# Configuration
SOURCE_DIR = "/Users/simonwang/Documents/Usage/VibeCodingMac/GCAP3226prep"
TARGET_DIR = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226"

# Folder mapping - how to consolidate similar folders
FOLDER_MAPPING = {
    "Materials": "course_materials",
    "Chatbots": "chatbots", 
    "syllabus": "course_materials/syllabus",
    "tools": "scripts",
    "src": "scripts/src",
    "NewTopics": "course_materials/new_topics",
    "TopicSelectionPM": "course_materials/topic_selection",
    "MoodlePost": "course_materials/moodle_posts",
    "temp": "temp_materials"
}

# Files to skip (system files, etc.)
SKIP_FILES = {".DS_Store", ".gitignore", "package.json", "tsconfig.json", "setup.sh"}
SKIP_DIRS = {".git", ".github", ".vscode"}

def get_target_path(source_rel_path, item_name):
    """Determine where an item would be moved to"""
    path_parts = source_rel_path.split(os.sep) if source_rel_path else []
    
    if not path_parts and item_name in FOLDER_MAPPING:
        return FOLDER_MAPPING[item_name]
    else:
        return os.path.join(*path_parts, item_name) if path_parts else item_name

def preview_directory(source_dir, prefix="", rel_path=""):
    """Preview what would be moved from a directory"""
    items = []
    
    try:
        for item in sorted(os.listdir(source_dir)):
            source_item = os.path.join(source_dir, item)
            item_rel_path = os.path.join(rel_path, item) if rel_path else item
            
            if item in SKIP_FILES:
                items.append(f"{prefix}📄 {item} → [SKIPPED - System file]")
                continue
            elif item in SKIP_DIRS:
                items.append(f"{prefix}📁 {item}/ → [SKIPPED - System directory]")
                continue
            
            if os.path.isfile(source_item):
                target_rel = get_target_path(rel_path, item)
                target_full = os.path.join(TARGET_DIR, target_rel)
                
                # Check if target exists
                exists_marker = " [EXISTS - will handle conflict]" if os.path.exists(target_full) else ""
                items.append(f"{prefix}📄 {item} → {target_rel}{exists_marker}")
                
            elif os.path.isdir(source_item):
                target_rel = get_target_path(rel_path, item)
                items.append(f"{prefix}📁 {item}/ → {target_rel}/")
                
                # Recursively preview subdirectory
                sub_items = preview_directory(source_item, prefix + "  ", item_rel_path)
                items.extend(sub_items)
                
    except PermissionError:
        items.append(f"{prefix}❌ Permission denied accessing {source_dir}")
    
    return items

def count_items(source_dir):
    """Count total files and directories"""
    file_count = 0
    dir_count = 0
    
    for root, dirs, files in os.walk(source_dir):
        # Filter out skipped directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        # Count directories (excluding skipped ones)
        dir_count += len([d for d in dirs if d not in SKIP_DIRS])
        
        # Count files (excluding skipped ones)
        file_count += len([f for f in files if f not in SKIP_FILES])
    
    return file_count, dir_count

def main():
    """Main preview function"""
    print("👀 GCAP3226 Materials Consolidation Preview")
    print("=" * 50)
    
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Source directory does not exist: {SOURCE_DIR}")
        return
    
    # Count items
    file_count, dir_count = count_items(SOURCE_DIR)
    print(f"📊 Found {file_count} files and {dir_count} directories to process")
    print()
    
    # Show folder mappings
    print("📋 Folder Mapping Rules:")
    for source, target in FOLDER_MAPPING.items():
        print(f"  {source}/ → {target}/")
    print()
    
    # Show what will be skipped
    print("⏭️ Will Skip:")
    print(f"  Files: {', '.join(SKIP_FILES)}")
    print(f"  Directories: {', '.join(SKIP_DIRS)}")
    print()
    
    # Preview the consolidation
    print("🔍 Consolidation Preview:")
    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print()
    
    preview_items = preview_directory(SOURCE_DIR)
    
    for item in preview_items:
        print(item)
    
    print()
    print("=" * 50)
    print("✅ Preview complete!")
    print()
    print("💡 To proceed with the actual consolidation, run:")
    print("   python scripts/consolidate_materials.py")

if __name__ == "__main__":
    main()
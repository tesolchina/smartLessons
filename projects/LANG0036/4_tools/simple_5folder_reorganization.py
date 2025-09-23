#!/usr/bin/env python3
"""
LANG0036 Simple 5-Folder Reorganization Script
Consolidates everything into just 5 main directories
"""

import os
import shutil
import datetime
from pathlib import Path

def log_message(message):
    """Log message with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def create_simple_structure():
    """Create the 5-folder structure."""
    base_dirs = [
        "1_materials_lessons",      # Course content, lectures, materials
        "2_assessments",           # All assessment related items
        "3_projects",             # Student projects and workspace
        "4_tools",                # Scripts, utilities, chatbots
        "5_miscellaneous"         # Everything else
    ]
    
    for dir_name in base_dirs:
        os.makedirs(dir_name, exist_ok=True)
        log_message(f"Created directory: {dir_name}")
    
    return base_dirs

def move_to_simple_structure():
    """Move all content to the 5-folder structure."""
    moves = []
    
    # Current complex directories to consolidate
    current_dirs = [
        "01_course_content",
        "02_assessments", 
        "03_instructor_tools",
        "03_student_workspace",
        "04_scripts_tools",
        "05_data_resources",
        "05_scripts_utilities", 
        "06_media_files",
        "07_documentation",
        "08_communication",
        "09_archives",
        "10_miscellaneous"
    ]
    
    # Mapping old directories to new simplified structure
    mapping = {
        "01_course_content": "1_materials_lessons",
        "07_documentation": "1_materials_lessons",
        "06_media_files": "1_materials_lessons",  # Course-related media
        
        "02_assessments": "2_assessments",
        
        "03_student_workspace": "3_projects",
        "05_data_resources": "3_projects",  # Project data
        
        "03_instructor_tools": "4_tools",
        "04_scripts_tools": "4_tools", 
        "05_scripts_utilities": "4_tools",
        
        "08_communication": "5_miscellaneous",
        "09_archives": "5_miscellaneous",
        "10_miscellaneous": "5_miscellaneous"
    }
    
    # Move directories
    for old_dir, new_dir in mapping.items():
        if os.path.exists(old_dir):
            # Move contents of old directory to new directory
            old_path = Path(old_dir)
            new_path = Path(new_dir)
            
            if old_path.exists() and old_path.is_dir():
                # Move all contents
                for item in old_path.iterdir():
                    target = new_path / item.name
                    if target.exists():
                        # Handle conflicts by adding suffix
                        counter = 1
                        while target.exists():
                            stem = item.stem if item.is_file() else item.name
                            suffix = item.suffix if item.is_file() else ""
                            target = new_path / f"{stem}_{counter}{suffix}"
                            counter += 1
                    
                    shutil.move(str(item), str(target))
                    moves.append((str(item), str(target)))
                
                # Remove empty old directory
                if old_path.exists() and not any(old_path.iterdir()):
                    old_path.rmdir()
                    log_message(f"Removed empty directory: {old_dir}")
    
    return moves

def handle_remaining_files():
    """Move any remaining loose files."""
    moves = []
    
    # Handle remaining loose files and directories
    exclude_items = {
        ".venv", ".DS_Store", ".git", 
        "1_materials_lessons", "2_assessments", "3_projects", "4_tools", "5_miscellaneous",
        "simple_reorganization.py", "comprehensive_reorganization.py", 
        "reorganization_plan.txt", "REORGANIZATION_SUMMARY.md"
    }
    
    for item in Path('.').iterdir():
        if item.name not in exclude_items:
            # Categorize remaining items
            if item.is_file():
                suffix = item.suffix.lower()
                name = item.name.lower()
                
                # Determine best folder
                if 'lesson' in name or 'week' in name or suffix in ['.md', '.pdf', '.pptx']:
                    target_dir = "1_materials_lessons"
                elif 'assess' in name or 'rubric' in name:
                    target_dir = "2_assessments"  
                elif 'project' in name or 'student' in name:
                    target_dir = "3_projects"
                elif suffix in ['.py', '.js', '.html']:
                    target_dir = "4_tools"
                else:
                    target_dir = "5_miscellaneous"
            else:
                # For directories, make best guess
                dir_name = item.name.lower()
                if any(x in dir_name for x in ['week', 'course', 'material', 'lesson']):
                    target_dir = "1_materials_lessons"
                elif any(x in dir_name for x in ['assess', 'test', 'exam']):
                    target_dir = "2_assessments"
                elif any(x in dir_name for x in ['project', 'student', 'team']):
                    target_dir = "3_projects" 
                elif any(x in dir_name for x in ['tool', 'script', 'bot', 'util']):
                    target_dir = "4_tools"
                else:
                    target_dir = "5_miscellaneous"
            
            # Move item
            target = Path(target_dir) / item.name
            if target.exists():
                counter = 1
                while target.exists():
                    if item.is_file():
                        target = Path(target_dir) / f"{item.stem}_{counter}{item.suffix}"
                    else:
                        target = Path(target_dir) / f"{item.name}_{counter}"
                    counter += 1
            
            shutil.move(str(item), str(target))
            moves.append((str(item), str(target)))
            log_message(f"Moved: {item.name} -> {target_dir}/")
    
    return moves

def main():
    """Main reorganization function."""
    log_message("=== LANG0036 Simple 5-Folder Reorganization ===")
    
    # Create new simple structure
    log_message("Creating simplified 5-folder structure...")
    new_dirs = create_simple_structure()
    
    # Move existing organized content
    log_message("Consolidating existing directories...")
    moves1 = move_to_simple_structure()
    
    # Handle any remaining loose items
    log_message("Moving remaining files...")
    moves2 = handle_remaining_files()
    
    total_moves = len(moves1) + len(moves2)
    
    # Summary
    log_message(f"\n=== Reorganization Complete ===")
    log_message(f"Total items moved: {total_moves}")
    log_message(f"New structure:")
    for i, dir_name in enumerate(new_dirs, 1):
        count = len(list(Path(dir_name).rglob('*')))
        log_message(f"  {i}. {dir_name}: {count} items")
    
    # Show final structure
    log_message(f"\nFinal directory structure:")
    for dir_name in new_dirs:
        if Path(dir_name).exists():
            print(f"\n📁 {dir_name}/")
            subdirs = [d for d in Path(dir_name).iterdir() if d.is_dir()][:5]  # Show first 5 subdirs
            for subdir in subdirs:
                print(f"  └── {subdir.name}/")
            if len(subdirs) == 5 and len(list(Path(dir_name).iterdir())) > 5:
                print(f"  └── ... and more")

if __name__ == "__main__":
    main()
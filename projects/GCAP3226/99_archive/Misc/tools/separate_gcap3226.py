#!/usr/bin/env python3
"""
GCAP3226 Materials Separator
Identifies and moves GCAP3226 materials to a separate folder
"""

import os
import shutil
import datetime
from pathlib import Path

def log_message(message):
    """Log message with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def find_gcap3226_files():
    """Find all files related to GCAP3226."""
    gcap_files = []
    search_patterns = ['GCAP', '3226', 'gcap', 'GCAP3226']
    
    # Search through all directories
    for root, dirs, files in os.walk('.'):
        # Skip .venv directory
        if '.venv' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            file_lower = file.lower()
            
            # Check if file contains GCAP3226 patterns
            if any(pattern.lower() in file_lower for pattern in search_patterns):
                # Additional check to make sure it's GCAP3226 and not other GCAP courses
                if '3226' in file or 'GCAP3226' in file:
                    gcap_files.append(file_path)
                    log_message(f"Found GCAP3226 file: {file_path}")
    
    return gcap_files

def create_gcap3226_folder():
    """Create GCAP3226 folder structure."""
    gcap_folder = "GCAP3226_materials"
    subfolders = [
        "course_content",
        "notebooks", 
        "datasets",
        "tools"
    ]
    
    # Create main folder
    os.makedirs(gcap_folder, exist_ok=True)
    log_message(f"Created folder: {gcap_folder}")
    
    # Create subfolders
    for subfolder in subfolders:
        os.makedirs(os.path.join(gcap_folder, subfolder), exist_ok=True)
        log_message(f"Created subfolder: {gcap_folder}/{subfolder}")
    
    return gcap_folder

def categorize_gcap_file(file_path):
    """Determine which subfolder a GCAP3226 file should go to."""
    file_lower = file_path.lower()
    
    if file_path.endswith('.ipynb'):
        return "notebooks"
    elif any(ext in file_lower for ext in ['.csv', '.json', '.xlsx']):
        return "datasets"
    elif any(ext in file_lower for ext in ['.py', '.js', '.html']):
        return "tools"
    else:
        return "course_content"

def move_gcap3226_files(gcap_files, gcap_folder):
    """Move GCAP3226 files to the new folder."""
    moved_files = []
    
    for file_path in gcap_files:
        try:
            # Determine target subfolder
            subfolder = categorize_gcap_file(file_path)
            target_dir = os.path.join(gcap_folder, subfolder)
            
            # Get just the filename
            filename = os.path.basename(file_path)
            target_path = os.path.join(target_dir, filename)
            
            # Handle duplicates
            counter = 1
            original_target = target_path
            while os.path.exists(target_path):
                name, ext = os.path.splitext(original_target)
                target_path = f"{name}_{counter}{ext}"
                counter += 1
            
            # Move the file
            shutil.move(file_path, target_path)
            moved_files.append((file_path, target_path))
            log_message(f"Moved: {file_path} -> {target_path}")
            
        except Exception as e:
            log_message(f"Error moving {file_path}: {e}")
    
    return moved_files

def main():
    """Main function."""
    log_message("=== GCAP3226 Materials Separator ===")
    
    # Find GCAP3226 files
    log_message("Searching for GCAP3226 materials...")
    gcap_files = find_gcap3226_files()
    
    if not gcap_files:
        log_message("No GCAP3226 files found!")
        return
    
    log_message(f"Found {len(gcap_files)} GCAP3226 files")
    
    # Create GCAP3226 folder
    log_message("Creating GCAP3226 folder structure...")
    gcap_folder = create_gcap3226_folder()
    
    # Show what will be moved
    print(f"\nFiles to be moved:")
    for file_path in gcap_files:
        subfolder = categorize_gcap_file(file_path)
        print(f"  {file_path} -> {gcap_folder}/{subfolder}/")
    
    # Confirm before moving
    confirm = input(f"\nMove {len(gcap_files)} GCAP3226 files? (y/N): ").strip().lower()
    
    if confirm == 'y':
        log_message("Moving GCAP3226 files...")
        moved_files = move_gcap3226_files(gcap_files, gcap_folder)
        
        log_message(f"Successfully moved {len(moved_files)} GCAP3226 files!")
        
        # Show summary
        print(f"\n=== GCAP3226 Separation Complete ===")
        print(f"Moved {len(moved_files)} files to: {gcap_folder}/")
        
        # Show folder contents
        for subfolder in ['course_content', 'notebooks', 'datasets', 'tools']:
            subfolder_path = os.path.join(gcap_folder, subfolder)
            if os.path.exists(subfolder_path):
                count = len([f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))])
                print(f"  {subfolder}/: {count} files")
    else:
        log_message("Operation cancelled.")

if __name__ == "__main__":
    main()
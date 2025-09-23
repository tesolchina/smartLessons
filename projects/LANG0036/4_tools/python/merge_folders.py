#!/usr/bin/env python3
"""
Script to merge LANG0026 folder contents into LANG0036 and delete the source folder.
This script handles file conflicts by creating backup copies with timestamps.
"""

import os
import shutil
import datetime
from pathlib import Path
import sys

def log_message(message):
    """Print timestamped log message"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def handle_conflict(src_path, dest_path):
    """Handle file conflicts by creating backup with timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{dest_path.stem}_backup_{timestamp}{dest_path.suffix}"
    backup_path = dest_path.parent / backup_name
    
    log_message(f"Conflict detected: {dest_path.name}")
    log_message(f"Creating backup: {backup_name}")
    
    # Move existing file to backup
    shutil.move(str(dest_path), str(backup_path))
    return backup_path

def merge_folders(source_dir, target_dir):
    """
    Merge source directory into target directory.
    Handle conflicts by backing up existing files.
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    if not source_path.exists():
        log_message(f"ERROR: Source directory does not exist: {source_dir}")
        return False
    
    if not target_path.exists():
        log_message(f"Creating target directory: {target_dir}")
        target_path.mkdir(parents=True, exist_ok=True)
    
    log_message(f"Starting merge from {source_dir} to {target_dir}")
    
    conflicts = []
    merged_count = 0
    
    # Walk through all files and directories in source
    for root, dirs, files in os.walk(source_path):
        # Calculate relative path from source root
        rel_path = Path(root).relative_to(source_path)
        target_root = target_path / rel_path
        
        # Create directories in target if they don't exist
        if not target_root.exists():
            target_root.mkdir(parents=True, exist_ok=True)
            log_message(f"Created directory: {rel_path}")
        
        # Copy files
        for file in files:
            src_file = Path(root) / file
            dest_file = target_root / file
            
            try:
                if dest_file.exists():
                    # Handle conflict
                    backup_path = handle_conflict(src_file, dest_file)
                    conflicts.append((str(dest_file), str(backup_path)))
                
                # Copy the file
                shutil.copy2(str(src_file), str(dest_file))
                log_message(f"Copied: {rel_path / file}")
                merged_count += 1
                
            except Exception as e:
                log_message(f"ERROR copying {src_file}: {e}")
                return False
    
    log_message(f"Merge completed: {merged_count} files processed")
    
    if conflicts:
        log_message(f"\nConflicts handled ({len(conflicts)} files):")
        for original, backup in conflicts:
            log_message(f"  {original} -> backup created: {Path(backup).name}")
    
    return True

def delete_source_folder(source_dir):
    """Delete the source folder after successful merge"""
    try:
        shutil.rmtree(source_dir)
        log_message(f"Successfully deleted source folder: {source_dir}")
        return True
    except Exception as e:
        log_message(f"ERROR deleting source folder: {e}")
        return False

def main():
    # Define paths
    source_dir = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0026"
    target_dir = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0036"
    
    log_message("=== LANG0026 to LANG0036 Folder Merge Script ===")
    log_message(f"Source: {source_dir}")
    log_message(f"Target: {target_dir}")
    
    # Confirm operation
    response = input("\nProceed with merge? This will move all LANG0026 contents to LANG0036. (y/N): ")
    if response.lower() != 'y':
        log_message("Operation cancelled by user")
        return
    
    # Perform merge
    if merge_folders(source_dir, target_dir):
        log_message("\n=== Merge completed successfully ===")
        
        # Ask for confirmation before deletion
        response = input("\nDelete LANG0026 folder? (y/N): ")
        if response.lower() == 'y':
            if delete_source_folder(source_dir):
                log_message("\n=== Operation completed successfully ===")
            else:
                log_message("\n=== Merge completed, but failed to delete source folder ===")
        else:
            log_message("\n=== Merge completed, source folder preserved ===")
    else:
        log_message("\n=== Merge failed ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
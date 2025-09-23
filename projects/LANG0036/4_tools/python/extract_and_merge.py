#!/usr/bin/env python3
"""
Script to extract ZIP file and merge LANG0026 contents into LANG0036.
Handles the OneDrive ZIP file mentioned in the request.
"""

import os
import shutil
import zipfile
import datetime
from pathlib import Path
import sys

def log_message(message):
    """Print timestamped log message"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def extract_zip_file(zip_path, extract_to):
    """Extract ZIP file to specified location"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        log_message(f"Extracted ZIP file to: {extract_to}")
        return True
    except Exception as e:
        log_message(f"ERROR extracting ZIP file: {e}")
        return False

def merge_directory_contents(source_dir, target_dir):
    """Merge contents of source directory into target directory"""
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    if not source_path.exists():
        log_message(f"Source directory does not exist: {source_dir}")
        return False
    
    target_path.mkdir(parents=True, exist_ok=True)
    
    merged_files = 0
    conflicts = []
    
    for item in source_path.rglob('*'):
        if item.is_file():
            # Calculate relative path
            rel_path = item.relative_to(source_path)
            target_file = target_path / rel_path
            
            # Create parent directories if needed
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Handle file conflicts
            if target_file.exists():
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{target_file.stem}_backup_{timestamp}{target_file.suffix}"
                backup_path = target_file.parent / backup_name
                shutil.move(str(target_file), str(backup_path))
                conflicts.append((str(target_file), str(backup_path)))
                log_message(f"Conflict: {rel_path} -> backup created")
            
            # Copy file
            shutil.copy2(str(item), str(target_file))
            merged_files += 1
            log_message(f"Copied: {rel_path}")
    
    log_message(f"Merged {merged_files} files")
    if conflicts:
        log_message(f"Created {len(conflicts)} backup files for conflicts")
    
    return True

def main():
    # Define paths
    zip_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0026/course_materials/OneDrive_2025-09-23.zip"
    lang0026_dir = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0026"
    lang0036_dir = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0036"
    temp_extract_dir = "/tmp/lang0026_extract"
    
    log_message("=== LANG0026 ZIP Extraction and Merge Script ===")
    
    # Check if ZIP file exists
    if os.path.exists(zip_file):
        log_message(f"Found ZIP file: {zip_file}")
        
        # Extract ZIP file
        log_message("Extracting ZIP file...")
        if extract_zip_file(zip_file, temp_extract_dir):
            # Find extracted content and merge
            extracted_content = Path(temp_extract_dir)
            if extracted_content.exists():
                log_message("Merging extracted content with LANG0036...")
                merge_directory_contents(str(extracted_content), lang0036_dir)
    
    # Check if LANG0026 directory exists and merge it
    if os.path.exists(lang0026_dir):
        log_message(f"Found LANG0026 directory: {lang0026_dir}")
        
        response = input(f"\nMerge LANG0026 folder contents into LANG0036? (y/N): ")
        if response.lower() == 'y':
            log_message("Merging LANG0026 contents...")
            if merge_directory_contents(lang0026_dir, lang0036_dir):
                # Ask about deletion
                response = input(f"\nDelete LANG0026 folder after successful merge? (y/N): ")
                if response.lower() == 'y':
                    try:
                        shutil.rmtree(lang0026_dir)
                        log_message(f"Deleted LANG0026 folder: {lang0026_dir}")
                    except Exception as e:
                        log_message(f"ERROR deleting LANG0026 folder: {e}")
    else:
        log_message(f"LANG0026 directory not found: {lang0026_dir}")
    
    # Clean up temp directory
    if os.path.exists(temp_extract_dir):
        try:
            shutil.rmtree(temp_extract_dir)
            log_message("Cleaned up temporary extraction directory")
        except:
            pass
    
    log_message("=== Script completed ===")

if __name__ == "__main__":
    main()
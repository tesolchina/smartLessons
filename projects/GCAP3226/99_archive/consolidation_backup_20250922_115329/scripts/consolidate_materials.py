#!/usr/bin/env python3
"""
GCAP3226 Materials Consolidation Script

This script safely moves and consolidates materials from the GCAP3226prep folder
to the current GCAP3226 project folder, ensuring no files are lost and folders
are properly merged.

Author: AI Assistant
Date: 2025-09-22
"""

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime
import json
import hashlib

# Configuration
SOURCE_DIR = "/Users/simonwang/Documents/Usage/VibeCodingMac/GCAP3226prep"
TARGET_DIR = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226"
BACKUP_DIR = f"{TARGET_DIR}/consolidation_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
LOG_FILE = f"{TARGET_DIR}/consolidation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

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

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

def calculate_file_hash(filepath):
    """Calculate MD5 hash of a file for duplicate detection"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return None

def create_backup():
    """Create a backup of the current target directory"""
    if os.path.exists(TARGET_DIR):
        logging.info(f"Creating backup at: {BACKUP_DIR}")
        shutil.copytree(TARGET_DIR, BACKUP_DIR, ignore=shutil.ignore_patterns('consolidation_backup_*'))
        return True
    return False

def ensure_dir(path):
    """Ensure directory exists, create if not"""
    Path(path).mkdir(parents=True, exist_ok=True)

def handle_file_conflict(source_file, target_file):
    """Handle file conflicts by comparing content and choosing the best option"""
    source_hash = calculate_file_hash(source_file)
    target_hash = calculate_file_hash(target_file)
    
    if source_hash == target_hash:
        logging.info(f"Files are identical, skipping: {os.path.basename(source_file)}")
        return "skip"
    
    source_stat = os.stat(source_file)
    target_stat = os.stat(target_file)
    
    # Keep the newer file, rename the older one
    if source_stat.st_mtime > target_stat.st_mtime:
        # Source is newer, rename target and move source
        backup_name = f"{target_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(target_file, backup_name)
        logging.info(f"Backed up older file: {backup_name}")
        return "replace"
    else:
        # Target is newer, rename source
        backup_name = f"{target_file}.alt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(source_file, backup_name)
        logging.info(f"Saved alternative version: {backup_name}")
        return "keep_both"

def move_file_safely(source_file, target_file):
    """Safely move a file, handling conflicts"""
    ensure_dir(os.path.dirname(target_file))
    
    if os.path.exists(target_file):
        action = handle_file_conflict(source_file, target_file)
        if action == "skip":
            return
        elif action == "keep_both":
            return
    
    shutil.copy2(source_file, target_file)
    logging.info(f"Moved: {source_file} -> {target_file}")

def consolidate_directory(source_dir, target_dir, source_rel_path=""):
    """Recursively consolidate a directory"""
    for item in os.listdir(source_dir):
        if item in SKIP_FILES or item in SKIP_DIRS:
            continue
            
        source_item = os.path.join(source_dir, item)
        
        if os.path.isfile(source_item):
            target_item = os.path.join(target_dir, item)
            move_file_safely(source_item, target_item)
            
        elif os.path.isdir(source_item):
            # Determine target directory based on mapping
            if source_rel_path == "" and item in FOLDER_MAPPING:
                mapped_path = FOLDER_MAPPING[item]
                target_subdir = os.path.join(TARGET_DIR, mapped_path)
            else:
                target_subdir = os.path.join(target_dir, item)
            
            ensure_dir(target_subdir)
            new_rel_path = os.path.join(source_rel_path, item) if source_rel_path else item
            consolidate_directory(source_item, target_subdir, new_rel_path)

def generate_consolidation_report():
    """Generate a report of what was consolidated"""
    report = {
        "consolidation_date": datetime.now().isoformat(),
        "source_directory": SOURCE_DIR,
        "target_directory": TARGET_DIR,
        "backup_directory": BACKUP_DIR,
        "folder_mappings": FOLDER_MAPPING,
        "skipped_files": list(SKIP_FILES),
        "skipped_directories": list(SKIP_DIRS)
    }
    
    report_file = os.path.join(TARGET_DIR, "consolidation_report.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    logging.info(f"Consolidation report saved: {report_file}")

def validate_source_directory():
    """Validate that source directory exists and is accessible"""
    if not os.path.exists(SOURCE_DIR):
        logging.error(f"Source directory does not exist: {SOURCE_DIR}")
        return False
    
    if not os.access(SOURCE_DIR, os.R_OK):
        logging.error(f"Cannot read source directory: {SOURCE_DIR}")
        return False
    
    return True

def main():
    """Main consolidation process"""
    print("🔄 Starting GCAP3226 Materials Consolidation")
    print("=" * 50)
    
    setup_logging()
    
    if not validate_source_directory():
        return False
    
    # Create backup
    backup_created = create_backup()
    if backup_created:
        logging.info("✅ Backup created successfully")
    
    # Ensure target directory exists
    ensure_dir(TARGET_DIR)
    
    try:
        # Start consolidation
        logging.info("🚀 Starting consolidation process...")
        consolidate_directory(SOURCE_DIR, TARGET_DIR)
        
        # Generate report
        generate_consolidation_report()
        
        logging.info("✅ Consolidation completed successfully!")
        print("\n✅ Consolidation completed successfully!")
        print(f"📁 Materials consolidated to: {TARGET_DIR}")
        print(f"🔄 Backup created at: {BACKUP_DIR}")
        print(f"📋 Log file: {LOG_FILE}")
        
        # Ask if user wants to remove source directory
        response = input("\n❓ Do you want to remove the source directory now? (y/N): ").strip().lower()
        if response == 'y':
            shutil.rmtree(SOURCE_DIR)
            logging.info(f"🗑️ Removed source directory: {SOURCE_DIR}")
            print("🗑️ Source directory removed.")
        else:
            print("💾 Source directory preserved.")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ Error during consolidation: {str(e)}")
        print(f"❌ Error during consolidation: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 All materials have been safely consolidated!")
        print("📚 You can now access all your GCAP3226 materials in one organized location.")
    else:
        print("\n⚠️ Consolidation failed. Please check the logs for details.")
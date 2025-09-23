#!/usr/bin/env python3
"""
CISL Deliverables Cleanup Script
===============================
Remove the current structure to prepare for the correct one based on checklist
"""

import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cleanup_deliverables():
    """Remove the current deliverables structure."""
    onedrive_dir = Path("/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/Summer 2025/CISL-Lang2077-deliverables")
    
    if onedrive_dir.exists():
        logger.info(f"Removing current structure: {onedrive_dir}")
        
        # Create backup of important files first
        backup_dir = Path("/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports/deliverables_backup")
        backup_dir.mkdir(exist_ok=True)
        
        # Backup README and PROJECT_SUMMARY if they exist
        for important_file in ["README.md", "PROJECT_SUMMARY.md"]:
            source = onedrive_dir / important_file
            if source.exists():
                backup_path = backup_dir / f"backup_{important_file}"
                shutil.copy2(source, backup_path)
                logger.info(f"Backed up: {important_file}")
        
        # Remove the entire directory
        shutil.rmtree(onedrive_dir)
        logger.info("✅ Current deliverables structure removed")
        
        # Recreate empty directory
        onedrive_dir.mkdir(parents=True, exist_ok=True)
        logger.info("✅ Empty deliverables directory created")
        
    else:
        logger.info("No existing deliverables directory found")

if __name__ == "__main__":
    cleanup_deliverables()
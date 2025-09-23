#!/usr/bin/env python3
"""
CISL Deliverables Verification Script
=====================================
Quick verification of the organized deliverables structure
"""

import os
from pathlib import Path

def verify_deliverables():
    base_path = Path("/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/Summer 2025/CISL-Lang2077-deliverables")
    
    print("🔍 CISL DELIVERABLES VERIFICATION")
    print("=" * 50)
    
    # Check main folders
    folders = [
        "01_Project_Reports",
        "02_Assessment_Questionnaires",
        "03_Service_Learning_Activities", 
        "04_Course_Materials",
        "05_Technical_Documentation",
        "06_Backup_Files"
    ]
    
    for folder in folders:
        folder_path = base_path / folder
        if folder_path.exists():
            files = list(folder_path.rglob("*.*"))
            print(f"✅ {folder}: {len(files)} files")
            
            # Show subfolder structure for assessment questionnaires
            if folder == "02_Assessment_Questionnaires":
                subfolders = ["PDF_Final", "HTML_Source", "Markdown_Source"]
                for subfolder in subfolders:
                    sub_path = folder_path / subfolder
                    if sub_path.exists():
                        sub_files = list(sub_path.glob("*.*"))
                        print(f"   └── {subfolder}: {len(sub_files)} files")
        else:
            print(f"❌ {folder}: NOT FOUND")
    
    # Check key files
    print("\n📋 KEY DELIVERABLES CHECK:")
    key_files = [
        "README.md",
        "PROJECT_SUMMARY.md",
        "02_Assessment_Questionnaires/PDF_Final/Student_AI_Literacy_Questionnaire.pdf",
        "02_Assessment_Questionnaires/PDF_Final/Teacher_Satisfaction_Questionnaire.pdf",
        "01_Project_Reports/CISL_Final_Report.md"
    ]
    
    for file_path in key_files:
        full_path = base_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size / 1024  # Size in KB
            print(f"✅ {file_path} ({size:.1f} KB)")
        else:
            print(f"❌ {file_path}: NOT FOUND")
    
    print(f"\n📁 Base directory: {base_path}")
    print("=" * 50)

if __name__ == "__main__":
    verify_deliverables()
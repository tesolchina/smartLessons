#!/usr/bin/env python3
"""
Simple Google Drive Sync for GCAP 3056 Info Gathering Documents
Creates markdown files that can be easily copied to Google Drive folders
"""
import sys
from pathlib import Path
from datetime import datetime

# Google Drive base path
GOOGLE_DRIVE_BASE = Path.home() / "Library/CloudStorage/GoogleDrive-simonwanghkteacher@gmail.com/My Drive"

def create_drive_ready_files():
    """Create Google Drive ready versions of all info gathering files"""
    print("📝 Creating Google Drive ready info gathering files...")
    
    # Create a Drive sync folder
    drive_sync_folder = Path("google_drive_sync")
    drive_sync_folder.mkdir(exist_ok=True)
    
    projects = [
        "energy_poverty",
        "hko_chatbot", 
        "chronic_disease_co_care",
        "anti_scamming_education",
        "emergency_alert_system"
    ]
    
    results = []
    
    for project in projects:
        local_file = Path(f"Projects and teams/{project}/info_gathering.md")
        
        if not local_file.exists():
            print(f"❌ Local file not found: {local_file}")
            continue
        
        # Read content
        with open(local_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create Drive-ready version
        project_title = project.replace('_', ' ').title()
        drive_filename = f"{project_title} - Info Gathering.md"
        drive_file = drive_sync_folder / drive_filename
        
        # Add Google Drive header
        drive_header = f"""# {project_title} - Information Gathering

**📁 Google Drive Version**  
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Project:** {project}  
**Local Source:** {local_file}  

---

"""
        
        # Remove local sync headers and add Drive header
        content_lines = content.split('\n')
        content_start = 0
        for i, line in enumerate(content_lines):
            if line.startswith('# ') and 'Information Gathering' in line:
                content_start = i
                break
        
        clean_content = '\n'.join(content_lines[content_start:])
        drive_content = drive_header + clean_content
        
        # Write Drive version
        with open(drive_file, 'w', encoding='utf-8') as f:
            f.write(drive_content)
        
        print(f"✅ Created: {drive_file}")
        results.append({
            'project': project,
            'local_file': str(local_file),
            'drive_file': str(drive_file),
            'title': project_title
        })
    
    return results, drive_sync_folder

def create_sync_instructions(results, sync_folder):
    """Create instructions for manually syncing to Google Drive"""
    instructions_file = sync_folder / "SYNC_INSTRUCTIONS.md"
    
    instructions = f"""# Google Drive Sync Instructions

## Overview
This folder contains Google Drive ready versions of all GCAP 3056 project info gathering documents.

## Created Files
"""
    
    for result in results:
        instructions += f"""
### {result['title']}
- **Local source:** `{result['local_file']}`
- **Drive ready file:** `{result['drive_file']}`
- **Suggested Drive location:** `GCAP 3056/Projects/{result['title']}/`
"""
    
    instructions += f"""

## Manual Sync Steps

### Option 1: Copy to Existing Project Folders
1. Open Google Drive in your browser or desktop app
2. Navigate to your GCAP 3056 course folder
3. For each project, copy the corresponding file to the project folder:

"""
    
    for result in results:
        instructions += f"   - Copy `{result['title']} - Info Gathering.md` to `GCAP 3056/Projects/{result['title']}/`\n"
    
    instructions += f"""

### Option 2: Upload to New Folders
If project folders don't exist yet:
1. Create a new folder structure in Google Drive:
   ```
   GCAP 3056/
   └── Projects/
       ├── Energy Poverty/
       ├── Hko Chatbot/
       ├── Chronic Disease Co Care/
       ├── Anti Scamming Education/
       └── Emergency Alert System/
   ```
2. Upload each info gathering file to its respective folder

### Option 3: Direct Upload
1. Simply upload all files to a folder called "GCAP 3056 Info Gathering"
2. Organize them later as needed

## File Descriptions

Each file contains:
- **Research Questions:** 5 key questions specific to the project
- **Information Needed:** Quantitative data, qualitative insights, policy analysis
- **Potential Arguments:** 4 frameworks for developing strong arguments
- **Sources to Investigate:** Government, academic, industry, and international sources
- **Action Items:** Specific tasks for information gathering

## Collaboration

Once uploaded to Google Drive:
1. Share folders with team members
2. Set appropriate permissions (edit/comment/view)
3. Use Google Docs' collaboration features
4. Track changes and comments

## Sync Back to Local

After making changes in Google Drive:
1. Download updated files from Google Drive
2. Copy content back to local `info_gathering.md` files
3. Update local project folders

---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"📋 Instructions created: {instructions_file}")
    return instructions_file

def main():
    print("🚀 GCAP 3056 Simple Google Drive Sync")
    print("=" * 50)
    
    # Check if Google Drive is accessible
    if GOOGLE_DRIVE_BASE.exists():
        print(f"✅ Google Drive accessible: {GOOGLE_DRIVE_BASE}")
    else:
        print(f"⚠️  Google Drive not found: {GOOGLE_DRIVE_BASE}")
        print("   Files will be created for manual upload")
    
    # Create Drive-ready files
    results, sync_folder = create_drive_ready_files()
    
    # Create instructions
    instructions_file = create_sync_instructions(results, sync_folder)
    
    print(f"\n📊 Summary:")
    print(f"   Created {len(results)} Google Drive ready files")
    print(f"   Files location: {sync_folder}")
    print(f"   Instructions: {instructions_file}")
    
    print(f"\n📝 Next Steps:")
    print(f"   1. Review files in {sync_folder}")
    print(f"   2. Follow instructions in {instructions_file}")
    print(f"   3. Upload files to Google Drive manually")
    print(f"   4. Share with team members for collaboration")

if __name__ == "__main__":
    main()

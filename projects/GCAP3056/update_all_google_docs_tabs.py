#!/usr/bin/env python3
"""
Update All Google Docs Tabs
Systematically updates all project Google Docs with properly formatted markdown content
"""

import os
import sys
import subprocess
from pathlib import Path
from markdown_to_googledocs import MarkdownToGoogleDocsConverter

# Project configuration
PROJECTS = [
    "energy_poverty", 
    "hko_chatbot", 
    "chronic_disease_co_care", 
    "anti_scamming_education", 
    "emergency_alert_system"
]

# Tab mappings
TAB_MAPPINGS = {
    "Writing for the public": "letter_to_editor.md",
    "Engage the government": "government_questions.md", 
    "Argumentative Research Paper": "argumentative_research_paper.md"
}

class GoogleDocsTabUpdater:
    def __init__(self):
        self.converter = MarkdownToGoogleDocsConverter()
        
    def convert_and_upload_tab(self, project_name, tab_name, markdown_file):
        """Convert markdown and upload to specific project tab"""
        markdown_path = f"Projects and teams/{project_name}/{markdown_file}"
        
        if not Path(markdown_path).exists():
            print(f"❌ File not found: {markdown_path}")
            return False
        
        print(f"📝 Processing {project_name} - {tab_name}")
        
        # Convert markdown to Google Docs text
        converted_text = self.converter.convert_file(markdown_path, tab_name)
        
        if not converted_text:
            print(f"❌ Failed to convert {markdown_path}")
            return False
        
        # Save converted text to temp file
        temp_file = f"/tmp/{project_name}_{markdown_file.replace('.md', '')}.txt"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(converted_text)
        
        print(f"✅ Converted {len(converted_text)} characters")
        
        # Upload to Google Docs
        cmd = [
            'python', 
            'gcap3056_google_docs_manager.py',
            '--write-project', project_name,
            '--text', converted_text
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ Uploaded to {project_name} Google Doc")
                return True
            else:
                print(f"❌ Upload failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⏱️ Upload timeout for {project_name} - may need manual authentication")
            return False
        except Exception as e:
            print(f"❌ Error uploading {project_name}: {e}")
            return False
    
    def update_all_projects(self):
        """Update all tabs for all projects"""
        print("🚀 Starting comprehensive Google Docs update...")
        print(f"📊 Updating {len(PROJECTS)} projects × {len(TAB_MAPPINGS)} tabs = {len(PROJECTS) * len(TAB_MAPPINGS)} total updates")
        
        results = {}
        
        for project_name in PROJECTS:
            print(f"\n{'='*60}")
            print(f"📁 PROJECT: {project_name.upper()}")
            print('='*60)
            
            project_results = {}
            
            for tab_name, markdown_file in TAB_MAPPINGS.items():
                success = self.convert_and_upload_tab(project_name, tab_name, markdown_file)
                project_results[tab_name] = {
                    'success': success,
                    'markdown_file': markdown_file
                }
                
                # Small delay between uploads
                if success:
                    import time
                    time.sleep(2)
            
            results[project_name] = project_results
        
        # Print summary
        print(f"\n{'='*60}")
        print("📊 UPLOAD SUMMARY")
        print('='*60)
        
        total_success = 0
        total_attempted = 0
        
        for project_name, project_results in results.items():
            print(f"\n📁 {project_name}:")
            for tab_name, result in project_results.items():
                status = "✅" if result['success'] else "❌"
                print(f"  {status} {tab_name}")
                total_attempted += 1
                if result['success']:
                    total_success += 1
        
        print(f"\n🎯 Overall Success Rate: {total_success}/{total_attempted} ({100*total_success/total_attempted:.1f}%)")
        
        return results
    
    def update_single_project(self, project_name):
        """Update all tabs for a single project"""
        if project_name not in PROJECTS:
            print(f"❌ Unknown project: {project_name}")
            print(f"Available projects: {', '.join(PROJECTS)}")
            return False
        
        print(f"📁 Updating {project_name} project...")
        
        for tab_name, markdown_file in TAB_MAPPINGS.items():
            self.convert_and_upload_tab(project_name, tab_name, markdown_file)
            import time
            time.sleep(2)  # Small delay between uploads
        
        print(f"✅ Completed {project_name} updates")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Update Google Docs tabs with markdown content')
    parser.add_argument('--project', help='Update specific project only')
    parser.add_argument('--all', action='store_true', help='Update all projects (default)')
    parser.add_argument('--list-projects', action='store_true', help='List available projects')
    
    args = parser.parse_args()
    
    updater = GoogleDocsTabUpdater()
    
    if args.list_projects:
        print("📁 Available projects:")
        for i, project in enumerate(PROJECTS, 1):
            print(f"  {i}. {project}")
        print(f"\n📋 Available tabs:")
        for tab_name, file_name in TAB_MAPPINGS.items():
            print(f"  • {tab_name} ← {file_name}")
        return
    
    if args.project:
        updater.update_single_project(args.project)
    else:
        updater.update_all_projects()

if __name__ == "__main__":
    main()

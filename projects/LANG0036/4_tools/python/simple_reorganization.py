#!/usr/bin/env python3
"""
Simple LANG0036 Project Reorganization Script
Excludes virtual environments and focuses on project files only
"""

import os
import shutil
import datetime
from pathlib import Path
from collections import defaultdict

def log_message(message):
    """Log message with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def categorize_file(file_path):
    """Categorize file based on path and extension."""
    path = Path(file_path)
    # Use the file path as provided instead of trying to make it relative
    relative_path = file_path
    suffix = path.suffix.lower()
    name = path.name.lower()
    
    # Documentation files
    if suffix in ['.md', '.txt', '.rst'] or 'readme' in name:
        return 'Documentation'
    
    # Assessment materials
    if 'assessment' in relative_path.lower() or 'rubric' in relative_path.lower():
        return 'Assessment'
    
    # Weekly materials
    if 'week' in relative_path.lower() and any(x in relative_path.lower() for x in ['lesson', 'plan', 'material']):
        return 'Course Content'
    
    # Student work
    if 'student' in relative_path.lower() or 'team' in relative_path.lower() or 'group' in relative_path.lower():
        return 'Student Work'
    
    # Data files
    if suffix in ['.csv', '.json', '.xlsx', '.xls']:
        return 'Data'
    
    # Scripts and code
    if suffix in ['.py', '.js', '.html', '.css', '.vue', '.ipynb']:
        return 'Scripts'
    
    # Media files
    if suffix in ['.pdf', '.docx', '.pptx', '.mp3', '.mp4', '.png', '.jpg', '.jpeg', '.webp']:
        return 'Media'
    
    # Email files
    if suffix in ['.msg']:
        return 'Communication'
    
    # Backup and temporary files
    if 'backup' in name or name.startswith('.') or '_backup_' in name:
        return 'Archives'
    
    return 'Other'

def create_new_structure():
    """Define the new directory structure."""
    return {
        'Course Content': '01_course_content',
        'Assessment': '02_assessments',
        'Student Work': '03_student_workspace',
        'Scripts': '04_scripts_tools',
        'Data': '05_data_resources',
        'Media': '06_media_files',
        'Documentation': '07_documentation',
        'Communication': '08_communication',
        'Archives': '09_archives',
        'Other': '10_miscellaneous'
    }

def analyze_project_files():
    """Analyze project files excluding virtual environments."""
    file_categories = defaultdict(list)
    exclude_dirs = {'.venv', '__pycache__', '.git', 'node_modules'}
    
    for root, dirs, files in os.walk('.'):
        # Remove excluded directories from dirs list to prevent traversal
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.startswith('.DS_Store'):
                continue
                
            file_path = os.path.join(root, file)
            category = categorize_file(file_path)
            file_categories[category].append(file_path)
    
    return file_categories

def generate_reorganization_plan(file_categories):
    """Generate a plan for reorganizing files."""
    new_structure = create_new_structure()
    plan = []
    
    for category, files in file_categories.items():
        target_dir = new_structure.get(category, '10_miscellaneous')
        
        for file_path in files:
            source = Path(file_path)
            
            # Create appropriate subdirectory structure
            if category == 'Course Content':
                if 'week' in file_path.lower():
                    week_match = [part for part in source.parts if 'week' in part.lower()]
                    if week_match:
                        subdir = f"{target_dir}/{week_match[0]}"
                    else:
                        subdir = f"{target_dir}/general"
                else:
                    subdir = f"{target_dir}/general"
            elif category == 'Assessment':
                subdir = f"{target_dir}/materials"
            elif category == 'Student Work':
                if 'team' in file_path.lower() or 'group' in file_path.lower():
                    subdir = f"{target_dir}/group_projects"
                else:
                    subdir = f"{target_dir}/individual"
            elif category == 'Scripts':
                if source.suffix == '.py':
                    subdir = f"{target_dir}/python"
                elif source.suffix in ['.js', '.html', '.css', '.vue']:
                    subdir = f"{target_dir}/web"
                elif source.suffix == '.ipynb':
                    subdir = f"{target_dir}/notebooks"
                else:
                    subdir = f"{target_dir}/other"
            elif category == 'Data':
                subdir = f"{target_dir}/datasets"
            else:
                subdir = target_dir
            
            target = Path(subdir) / source.name
            plan.append({
                'source': source,
                'target': target,
                'category': category
            })
    
    return plan

def main():
    """Main reorganization function."""
    log_message("=== LANG0036 Simple Project Reorganization ===")
    
    # Analyze current structure
    log_message("Analyzing project files (excluding virtual environments)...")
    file_categories = analyze_project_files()
    
    # Show analysis summary
    total_files = sum(len(files) for files in file_categories.values())
    log_message(f"Found {total_files} files in {len(file_categories)} categories:")
    
    for category, files in sorted(file_categories.items()):
        log_message(f"  {category}: {len(files)} files")
    
    # Generate reorganization plan
    log_message("\nGenerating reorganization plan...")
    plan = generate_reorganization_plan(file_categories)
    
    # Save plan to file
    plan_file = "reorganization_plan.txt"
    with open(plan_file, 'w') as f:
        f.write("LANG0036 Project Reorganization Plan\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total files to reorganize: {len(plan)}\n\n")
        
        for category in sorted(file_categories.keys()):
            category_files = [p for p in plan if p['category'] == category]
            if category_files:
                f.write(f"\n{category.upper()} ({len(category_files)} files):\n")
                f.write("-" * 40 + "\n")
                for item in category_files[:10]:  # Show first 10 files
                    f.write(f"  {item['source']} -> {item['target']}\n")
                if len(category_files) > 10:
                    f.write(f"  ... and {len(category_files) - 10} more files\n")
    
    log_message(f"Reorganization plan saved to: {plan_file}")
    
    # Ask for confirmation
    print(f"\nReorganization Summary:")
    print(f"- {len(plan)} files will be moved")
    print(f"- {len(file_categories)} categories identified")
    print(f"- New structure with organized subdirectories")
    
    confirm = input("\nProceed with reorganization? (y/N): ").strip().lower()
    
    if confirm == 'y':
        log_message("Starting file reorganization...")
        execute_reorganization(plan)
    else:
        log_message("Reorganization cancelled. Plan saved for review.")

def execute_reorganization(plan):
    """Execute the reorganization plan."""
    moved_count = 0
    error_count = 0
    
    for item in plan:
        try:
            source = item['source']
            target = item['target']
            
            # Create target directory if it doesn't exist
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the file
            shutil.move(str(source), str(target))
            moved_count += 1
            
            if moved_count % 100 == 0:  # Progress update every 100 files
                log_message(f"Moved {moved_count} files...")
                
        except Exception as e:
            log_message(f"Error moving {source} to {target}: {e}")
            error_count += 1
    
    log_message(f"Reorganization complete!")
    log_message(f"Successfully moved: {moved_count} files")
    if error_count > 0:
        log_message(f"Errors encountered: {error_count} files")

if __name__ == "__main__":
    main()
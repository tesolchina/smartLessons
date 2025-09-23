#!/usr/bin/env python3
"""
Comprehensive LANG0036 Folder Reorganization Script
This script analyzes all files and folders and creates a clean, logical structure.
"""

import os
import shutil
import datetime
from pathlib import Path
import json
import csv
from collections import defaultdict
import re

def log_message(message):
    """Print timestamped log message"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def analyze_directory_structure(root_path):
    """Analyze the directory structure and categorize files."""
    file_analysis = []
    categories = defaultdict(list)
    
    # Directories to exclude from analysis
    exclude_dirs = {'.venv', '__pycache__', '.git', 'node_modules', '.DS_Store'}
    
    for path in Path(root_path).rglob('*'):
        # Skip if any parent directory is in exclude list
        if any(part in exclude_dirs for part in path.parts):
            continue
            
        if path.is_file():
            relative_path = path.relative_to(root_path)
            category = categorize_file(path, relative_path, file_analysis)
            file_analysis.append({
                'path': str(path),
                'category': category,
                'size': path.stat().st_size
            })
            categories[category].append(str(path))
    
    return file_analysis, categories

def categorize_file(file_path, relative_path, analysis):
    """Categorize a file based on its path, name, and extension"""
    
    path_str = str(relative_path).lower()
    file_name = file_path.name.lower()
    file_ext = file_path.suffix.lower()
    
    # Course materials from EEGC folder
    if 'eegc ay 2025-26' in path_str:
        if 'assessment' in path_str and 'confidential' in path_str:
            analysis['categories']['assessments'].append(str(relative_path))
        elif any(x in path_str for x in ['materials for students', 'ppts', 'course files']):
            analysis['categories']['course_materials'].append(str(relative_path))
        elif 'materials for teachers' in path_str:
            analysis['categories']['instructor_tools'].append(str(relative_path))
        else:
            analysis['categories']['course_materials'].append(str(relative_path))
    
    # Weekly content
    elif path_str.startswith('week'):
        analysis['categories']['weekly_content'].append(str(relative_path))
    
    # Assessment materials
    elif 'assessment' in path_str or file_name.startswith(('01_', '02_', '03_', '04_', '05_', '06_', '07_', '08_')):
        analysis['categories']['assessments'].append(str(relative_path))
    
    # Student workspace and projects
    elif any(x in path_str for x in ['02_student_workspace', 'student_management', 'group_projects']):
        analysis['categories']['student_work'].append(str(relative_path))
    
    # Instructor tools
    elif any(x in path_str for x in ['03_instructor_tools', 'chatbots4students', 'new-bytewise-frontend']):
        analysis['categories']['instructor_tools'].append(str(relative_path))
    
    # Data resources
    elif any(x in path_str for x in ['04_data_resources', 'open_data', 'datasets']) or file_ext in ['.csv', '.json', '.dat']:
        analysis['categories']['data_resources'].append(str(relative_path))
    
    # Scripts and utilities
    elif file_ext in ['.py', '.sh', '.js'] or any(x in path_str for x in ['05_scripts_utilities', 'scripts']):
        analysis['categories']['scripts_utilities'].append(str(relative_path))
    
    # Documentation
    elif file_ext in ['.md', '.txt'] or file_name in ['readme', 'notes', 'documentation']:
        analysis['categories']['documentation'].append(str(relative_path))
    
    # Loose files in root
    elif '/' not in str(relative_path):
        analysis['categories']['loose_files'].append(str(relative_path))
    
    # Check for potential duplicates
    if any(x in file_name for x in ['backup', 'copy', '_2', ' 2']):
        analysis['categories']['duplicates'].append(str(relative_path))

def create_new_structure_plan():
    """Define the new organizational structure"""
    
    return {
        '01_course_content': {
            'description': 'All course materials, presentations, and student materials',
            'subdirs': {
                'presentations': 'PowerPoint slides and lecture materials',
                'student_materials': 'PDF and Word documents for students',
                'course_documents': 'Syllabus, rubrics, course info',
                'weekly_modules': 'Organized by week (week01-week13)'
            }
        },
        '02_assessments': {
            'description': 'All assessment materials and student submissions',
            'subdirs': {
                'assessment_templates': 'Assessment instructions and templates',
                'rubrics': 'Grading rubrics and criteria',
                'student_submissions': 'Student work organized by assessment',
                'feedback_tools': 'Moodle feedback and analysis tools'
            }
        },
        '03_student_workspace': {
            'description': 'Student projects and collaborative work',
            'subdirs': {
                'group_projects': 'Team projects by topic',
                'individual_work': 'Individual assignments and reflections',
                'student_management': 'Student lists and group assignments'
            }
        },
        '04_instructor_tools': {
            'description': 'Teaching tools and applications',
            'subdirs': {
                'chatbots': 'AI tutoring applications',
                'frontend_apps': 'Web applications for teaching',
                'analysis_tools': 'Student work analysis tools'
            }
        },
        '05_data_resources': {
            'description': 'Data files and research resources',
            'subdirs': {
                'open_data': 'Public datasets and catalogs',
                'research_data': 'Course-specific data files',
                'archives': 'Historical data and backups'
            }
        },
        '06_scripts_automation': {
            'description': 'Automation scripts and utilities',
            'subdirs': {
                'data_processing': 'Data analysis and processing scripts',
                'course_management': 'Administrative automation',
                'backup_utilities': 'Backup and maintenance scripts'
            }
        },
        '07_documentation': {
            'description': 'Documentation and project notes',
            'subdirs': {
                'course_notes': 'Teaching notes and observations',
                'project_documentation': 'README files and guides',
                'research_notes': 'Academic research and references'
            }
        },
        '08_archives': {
            'description': 'Archived and backup materials',
            'subdirs': {
                'old_versions': 'Previous versions of files',
                'duplicates': 'Duplicate files for review',
                'temp_files': 'Temporary processing files'
            }
        }
    }

def reorganize_files(root_path, analysis, dry_run=True):
    """Reorganize files according to the new structure"""
    
    root = Path(root_path)
    new_structure = create_new_structure_plan()
    
    reorganization_plan = []
    
    # Create new directory structure
    for main_dir, config in new_structure.items():
        new_dir = root / main_dir
        if not dry_run:
            new_dir.mkdir(exist_ok=True)
        
        for subdir, description in config['subdirs'].items():
            sub_path = new_dir / subdir
            if not dry_run:
                sub_path.mkdir(exist_ok=True)
        
        log_message(f"{'Would create' if dry_run else 'Created'} directory: {main_dir}")
    
    # Plan file movements
    file_movements = plan_file_movements(root, analysis, new_structure)
    
    # Execute or log movements
    for old_path, new_path, reason in file_movements:
        reorganization_plan.append({
            'old_path': str(old_path),
            'new_path': str(new_path),
            'reason': reason
        })
        
        if not dry_run:
            try:
                # Create parent directories if needed
                new_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Handle conflicts
                if new_path.exists():
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = f"{new_path.stem}_conflict_{timestamp}{new_path.suffix}"
                    backup_path = new_path.parent / backup_name
                    shutil.move(str(new_path), str(backup_path))
                    log_message(f"Conflict resolved: {new_path.name} -> {backup_name}")
                
                # Move file
                shutil.move(str(old_path), str(new_path))
                log_message(f"Moved: {old_path.name} -> {new_path}")
                
            except Exception as e:
                log_message(f"Error moving {old_path}: {e}")
        else:
            log_message(f"Would move: {old_path} -> {new_path} ({reason})")
    
    return reorganization_plan

def plan_file_movements(root, analysis, new_structure):
    """Plan how files should be moved to new structure"""
    
    movements = []
    
    # Course materials
    for file_path in analysis['categories']['course_materials']:
        old_path = root / file_path
        if 'ppt' in file_path.lower():
            new_path = root / '01_course_content' / 'presentations' / old_path.name
        elif any(x in file_path.lower() for x in ['student', 'material']):
            new_path = root / '01_course_content' / 'student_materials' / old_path.name
        else:
            new_path = root / '01_course_content' / 'course_documents' / old_path.name
        movements.append((old_path, new_path, 'Course material'))
    
    # Assessments
    for file_path in analysis['categories']['assessments']:
        old_path = root / file_path
        if 'rubric' in file_path.lower():
            new_path = root / '02_assessments' / 'rubrics' / old_path.name
        elif 'moodleforum' in file_path.lower():
            new_path = root / '02_assessments' / 'feedback_tools' / old_path.name
        else:
            new_path = root / '02_assessments' / 'assessment_templates' / old_path.name
        movements.append((old_path, new_path, 'Assessment material'))
    
    # Weekly content
    for file_path in analysis['categories']['weekly_content']:
        old_path = root / file_path
        week_match = re.search(r'week(\d+)', file_path.lower())
        if week_match:
            week_num = week_match.group(1).zfill(2)
            new_path = root / '01_course_content' / 'weekly_modules' / f'week{week_num}' / old_path.name
        else:
            new_path = root / '01_course_content' / 'weekly_modules' / 'misc' / old_path.name
        movements.append((old_path, new_path, 'Weekly content'))
    
    # Student work
    for file_path in analysis['categories']['student_work']:
        old_path = root / file_path
        if 'group' in file_path.lower():
            new_path = root / '03_student_workspace' / 'group_projects' / old_path.name
        elif 'management' in file_path.lower():
            new_path = root / '03_student_workspace' / 'student_management' / old_path.name
        else:
            new_path = root / '03_student_workspace' / 'individual_work' / old_path.name
        movements.append((old_path, new_path, 'Student work'))
    
    # Instructor tools
    for file_path in analysis['categories']['instructor_tools']:
        old_path = root / file_path
        if 'chatbot' in file_path.lower():
            new_path = root / '04_instructor_tools' / 'chatbots' / old_path.name
        elif any(x in file_path.lower() for x in ['frontend', 'vue', 'web']):
            new_path = root / '04_instructor_tools' / 'frontend_apps' / old_path.name
        else:
            new_path = root / '04_instructor_tools' / 'analysis_tools' / old_path.name
        movements.append((old_path, new_path, 'Instructor tool'))
    
    # Data resources
    for file_path in analysis['categories']['data_resources']:
        old_path = root / file_path
        if 'open_data' in file_path.lower():
            new_path = root / '05_data_resources' / 'open_data' / old_path.name
        elif old_path.suffix.lower() in ['.csv', '.json', '.dat']:
            new_path = root / '05_data_resources' / 'research_data' / old_path.name
        else:
            new_path = root / '05_data_resources' / 'archives' / old_path.name
        movements.append((old_path, new_path, 'Data resource'))
    
    # Scripts and utilities
    for file_path in analysis['categories']['scripts_utilities']:
        old_path = root / file_path
        if old_path.suffix.lower() == '.py':
            new_path = root / '06_scripts_automation' / 'data_processing' / old_path.name
        else:
            new_path = root / '06_scripts_automation' / 'course_management' / old_path.name
        movements.append((old_path, new_path, 'Script/utility'))
    
    # Documentation
    for file_path in analysis['categories']['documentation']:
        old_path = root / file_path
        if old_path.name.lower() in ['readme.md', 'notes.md']:
            new_path = root / '07_documentation' / 'project_documentation' / old_path.name
        else:
            new_path = root / '07_documentation' / 'course_notes' / old_path.name
        movements.append((old_path, new_path, 'Documentation'))
    
    # Duplicates and loose files
    for file_path in analysis['categories']['duplicates']:
        old_path = root / file_path
        new_path = root / '08_archives' / 'duplicates' / old_path.name
        movements.append((old_path, new_path, 'Duplicate file'))
    
    for file_path in analysis['categories']['loose_files']:
        old_path = root / file_path
        if old_path.suffix.lower() in ['.csv', '.json']:
            new_path = root / '05_data_resources' / 'research_data' / old_path.name
        elif old_path.suffix.lower() == '.py':
            new_path = root / '06_scripts_automation' / 'course_management' / old_path.name
        else:
            new_path = root / '08_archives' / 'temp_files' / old_path.name
        movements.append((old_path, new_path, 'Loose file'))
    
    return movements

def generate_report(analysis, reorganization_plan, output_path):
    """Generate a comprehensive reorganization report"""
    
    report = {
        'timestamp': datetime.datetime.now().isoformat(),
        'summary': {
            'total_files': analysis['total_files'],
            'total_directories': analysis['total_directories'],
            'files_to_move': len(reorganization_plan),
            'file_types': dict(analysis['file_types'])
        },
        'categories': {k: len(v) for k, v in analysis['categories'].items()},
        'reorganization_plan': reorganization_plan
    }
    
    # Write JSON report
    with open(output_path / 'reorganization_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Write human-readable summary
    with open(output_path / 'reorganization_summary.md', 'w') as f:
        f.write("# LANG0036 Comprehensive Reorganization Report\n\n")
        f.write(f"Generated: {report['timestamp']}\n\n")
        
        f.write("## Summary\n")
        f.write(f"- Total files: {report['summary']['total_files']}\n")
        f.write(f"- Total directories: {report['summary']['total_directories']}\n")
        f.write(f"- Files to reorganize: {report['summary']['files_to_move']}\n\n")
        
        f.write("## File Type Distribution\n")
        for ext, count in sorted(report['summary']['file_types'].items()):
            f.write(f"- {ext or 'no extension'}: {count} files\n")
        
        f.write("\n## Category Distribution\n")
        for category, count in report['categories'].items():
            f.write(f"- {category.replace('_', ' ').title()}: {count} files\n")
        
        f.write("\n## New Structure\n")
        structure = create_new_structure_plan()
        for main_dir, config in structure.items():
            f.write(f"\n### {main_dir}\n")
            f.write(f"{config['description']}\n\n")
            for subdir, desc in config['subdirs'].items():
                f.write(f"- **{subdir}**: {desc}\n")
    
    log_message(f"Report generated: {output_path}")

def main():
    """Main execution function"""
    
    root_path = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0036"
    
    log_message("=== LANG0036 Comprehensive Reorganization ===")
    log_message("Starting directory analysis...")
    
    # Analyze current structure
    analysis, categories = analyze_directory_structure(root_path)
    
    log_message(f"Analysis complete: {len(analysis)} files analyzed")
    
    # Generate reorganization plan (dry run first)
    log_message("Generating reorganization plan...")
    reorganization_plan = reorganize_files(root_path, analysis, dry_run=True)
    
    # Generate report
    output_path = Path(root_path)
    generate_report(analysis, reorganization_plan, output_path)
    
    # Ask for confirmation
    print("\n" + "="*60)
    print("REORGANIZATION PLAN SUMMARY:")
    print(f"- {len(reorganization_plan)} files will be moved")
    print(f"- New structure with 8 main directories")
    print(f"- Detailed report saved to reorganization_summary.md")
    print("="*60)
    
    response = input("\nProceed with reorganization? (y/N): ")
    if response.lower() == 'y':
        log_message("Executing reorganization...")
        reorganize_files(root_path, analysis, dry_run=False)
        
        # Clean up empty directories
        log_message("Cleaning up empty directories...")
        for root, dirs, files in os.walk(root_path, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    if not os.listdir(dir_path):  # Empty directory
                        os.rmdir(dir_path)
                        log_message(f"Removed empty directory: {dir_path}")
                except OSError:
                    pass  # Directory not empty or can't be removed
        
        log_message("Reorganization completed!")
    else:
        log_message("Reorganization cancelled. Plan saved for review.")

if __name__ == "__main__":
    main()
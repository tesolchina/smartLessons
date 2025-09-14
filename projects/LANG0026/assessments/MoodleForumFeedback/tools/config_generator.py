#!/usr/bin/env python3
"""
Forum Analysis Configuration Generator
======================================

Interactive tool to generate configuration files for new forum types.
"""

import json
import os
from datetime import datetime

def create_config_template():
    """Interactive configuration file generator"""
    print("🛠️ Forum Analysis Configuration Generator")
    print("=" * 50)
    
    config = {}
    
    # Basic information
    print("\\n📋 Basic Configuration")
    config['analysis_config'] = {
        'name': input("Analysis name: "),
        'description': input("Description: "),
        'version': '1.0'
    }
    
    # Data sources
    print("\\n📁 Data Sources")
    config['data_sources'] = {
        'forum_json': input("Forum JSON file path (relative): "),
        'student_csv': input("Student CSV file path (relative, optional): ") or None,
        'output_directory': input("Output directory (relative): ")
    }
    
    # JSON structure
    print("\\n🔧 JSON Structure Configuration")
    config['json_structure'] = {
        'posts_path': input("Posts array path (e.g., '[0]' for nested array): ") or "[0]",
        'post_fields': {
            'id': input("Post ID field name (default: 'id'): ") or 'id',
            'user': input("User name field (default: 'userfullname'): ") or 'userfullname',
            'parent': input("Parent post field (default: 'parent'): ") or 'parent',
            'subject': input("Subject field (default: 'subject'): ") or 'subject',
            'message': input("Message content field (default: 'message'): ") or 'message',
            'created': input("Creation time field (default: 'created'): ") or 'created',
            'wordcount': input("Word count field (default: 'wordcount'): ") or 'wordcount'
        },
        'instructor_names': []
    }
    
    # Instructor names
    print("\\nInstructor names (press Enter when done):")
    while True:
        instructor = input("Instructor name: ").strip()
        if not instructor:
            break
        config['json_structure']['instructor_names'].append(instructor)
    
    # Student CSV structure (if CSV provided)
    if config['data_sources']['student_csv']:
        print("\\n👥 Student CSV Structure")
        config['student_csv_structure'] = {
            'student_name_column': input("Student name column (default: 'Student Name'): ") or 'Student Name',
            'section_column': input("Section column (default: 'Section Code'): ") or 'Section Code',
            'student_id_column': input("Student ID column (default: 'Student No.'): ") or 'Student No.'
        }
    
    # Assignment components
    print("\\n📝 Assignment Components")
    components = []
    
    while True:
        print(f"\\nComponent {len(components) + 1} (press Enter to finish):")
        component_name = input("Component name: ").strip()
        if not component_name:
            break
        
        component = {
            'name': component_name,
            'emoji': input(f"Emoji for {component_name} (default: 📄): ") or '📄',
            'indicators': [],
            'min_length': int(input(f"Minimum text length for {component_name} (default: 50): ") or 50),
            'required': input(f"Is {component_name} required? (y/n, default: y): ").lower() != 'n'
        }
        
        print(f"Text indicators for {component_name} (press Enter when done):")
        while True:
            indicator = input("Indicator phrase: ").strip()
            if not indicator:
                break
            component['indicators'].append(indicator.lower())
        
        components.append(component)
    
    config['content_classification'] = {
        'assignment_components': components,
        'exclusion_patterns': []
    }
    
    # Exclusion patterns
    print("\\n⚠️ Exclusion Patterns (for template/example content)")
    while True:
        pattern = input("Exclusion pattern (press Enter when done): ").strip()
        if not pattern:
            break
        config['content_classification']['exclusion_patterns'].append(pattern.lower())
    
    # Analysis criteria
    total_components = len(components)
    complete_threshold = int(input(f"\\nComplete submission threshold (out of {total_components}): ") or total_components)
    partial_threshold = int(input(f"Partial submission threshold (out of {total_components}): ") or 1)
    
    config['analysis_criteria'] = {
        'completion_threshold': {
            'complete': complete_threshold,
            'partial': partial_threshold
        },
        'quality_metrics': [
            'content_completeness',
            'language_quality',
            'assignment_adherence'
        ]
    }
    
    # Report generation
    config['report_generation'] = {
        'individual_report': {
            'filename': f"{config['analysis_config']['name'].lower().replace(' ', '_')}_individual_reports.md",
            'title': f"Individual Student Reports - {config['analysis_config']['name']}",
            'include_full_content': True,
            'content_preview_length': 1000
        },
        'overall_report': {
            'filename': 'comprehensive_overall_report.md',
            'title': 'Comprehensive Forum Analysis Report',
            'include_section_breakdown': True,
            'include_participation_stats': True
        }
    }
    
    return config

def save_config(config: dict):
    """Save configuration to file"""
    # Generate filename
    safe_name = config['analysis_config']['name'].lower().replace(' ', '_').replace('-', '_')
    filename = f"config_{safe_name}.json"
    
    # Check if file exists
    if os.path.exists(filename):
        overwrite = input(f"File {filename} exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            filename = input("Enter new filename: ")
    
    # Save file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\\n✅ Configuration saved to: {filename}")
    return filename

def main():
    """Main function"""
    try:
        config = create_config_template()
        filename = save_config(config)
        
        print(f"\\n🎉 Configuration file created successfully!")
        print(f"To test your configuration:")
        print(f"  python3 generic_forum_analyzer.py --validate {filename}")
        print(f"To run analysis:")
        print(f"  python3 generic_forum_analyzer.py {filename}")
        
    except KeyboardInterrupt:
        print("\\n\\n❌ Configuration creation cancelled.")
    except Exception as e:
        print(f"\\n❌ Error creating configuration: {e}")

if __name__ == "__main__":
    main()
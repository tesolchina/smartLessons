#!/usr/bin/env python3
"""
GCAP3226 Moodle Post Generator
===============================

Automatically generate Moodle forum posts from HTML templates with customizable parameters.
This script helps maintain consistency across course content and speeds up post creation.

Usage:
    python generate_post.py --template assignments --type reflective_essay --week 4
    python generate_post.py --template projects --type timeline --output custom_name.html
    python generate_post.py --config assignments/essay_config.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
import re

class MoodlePostGenerator:
    def __init__(self, base_dir: str = None):
        """Initialize the post generator with base directory."""
        if base_dir is None:
            # Auto-detect base directory relative to script location
            script_dir = Path(__file__).parent
            self.base_dir = script_dir.parent
        else:
            self.base_dir = Path(base_dir)
        
        self.templates_dir = self.base_dir / "templates"
        self.forum_posts_dir = self.base_dir / "forum_posts"
        self.configs_dir = self.base_dir / "configs"
        
        # Create directories if they don't exist
        self.forum_posts_dir.mkdir(parents=True, exist_ok=True)
        self.configs_dir.mkdir(parents=True, exist_ok=True)

    def load_template(self, category: str, template_name: str) -> str:
        """Load HTML template from the specified category."""
        template_path = self.templates_dir / category / f"{template_name}_template.html"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration file with template parameters."""
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_default_parameters(self) -> Dict[str, str]:
        """Get default parameters that are commonly used across templates."""
        now = datetime.now()
        
        return {
            'CURRENT_DATE': now.strftime('%B %d, %Y'),
            'CURRENT_YEAR': str(now.year),
            'SEMESTER': 'Fall 2024' if now.month >= 8 else 'Spring 2025',
            'COURSE_CODE': 'GCAP 3226',
            'COURSE_TITLE': 'Empowering Citizens through Data',
            'INSTRUCTOR_EMAIL': 'instructor@hkbu.edu.hk',
            'WHATSAPP_GROUP_URL': 'https://chat.whatsapp.com/GjE8jDoEx5Z2A0KGahSJZt',
            'AI_TUTOR_URL': 'https://smartlessons.hkbu.tech/GCAP3226/reflective-essay-tutor.html',
            'SUBMISSION_METHOD': 'Upload to Moodle assignment portal',
            'LATE_POLICY': '10% deduction per day late',
            'FILE_NAME_FORMAT': 'LastName_FirstName_Assignment_Name.docx'
        }

    def substitute_parameters(self, template_content: str, parameters: Dict[str, Any]) -> str:
        """Replace template placeholders with actual values."""
        content = template_content
        
        # Get default parameters and merge with provided ones
        defaults = self.get_default_parameters()
        all_params = {**defaults, **parameters}
        
        # Replace all placeholder patterns {PARAMETER_NAME}
        for key, value in all_params.items():
            placeholder = f"{{{key}}}"
            content = content.replace(placeholder, str(value))
        
        return content

    def generate_week_structure(self, week_number: int) -> Path:
        """Create week directory structure if it doesn't exist."""
        week_dir = self.forum_posts_dir / f"week{week_number:02d}"
        week_dir.mkdir(parents=True, exist_ok=True)
        return week_dir

    def generate_post(self, 
                     category: str, 
                     template_name: str, 
                     parameters: Dict[str, Any], 
                     output_name: str = None,
                     week: int = None) -> str:
        """Generate a forum post from template and parameters."""
        
        # Load template
        template_content = self.load_template(category, template_name)
        
        # Substitute parameters
        generated_content = self.substitute_parameters(template_content, parameters)
        
        # Determine output location
        if week:
            week_dir = self.generate_week_structure(week)
            if output_name is None:
                output_name = f"{template_name}_week{week:02d}.html"
            output_path = week_dir / output_name
        else:
            if output_name is None:
                output_name = f"{template_name}_{datetime.now().strftime('%Y%m%d')}.html"
            output_path = self.forum_posts_dir / output_name
        
        # Save generated content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(generated_content)
        
        return str(output_path)

    def create_sample_config(self, category: str, template_name: str) -> str:
        """Create a sample configuration file for a template."""
        
        # Sample configurations for different template types
        sample_configs = {
            ('assignments', 'reflective_essay'): {
                'ESSAY_TOPIC': 'Personal Data Experience Reflection',
                'WORD_COUNT': '800-1000',
                'DUE_DATE': 'Friday, Week 5',
                'DUE_DATE_FULL': 'Friday, October 25, 2024 at 11:59 PM',
                'SUBMISSION_FORMAT': 'Microsoft Word document (.docx)',
                'INSTRUCTION_1': 'Reflect on a recent personal experience involving data collection or privacy',
                'INSTRUCTION_2': 'Connect your experience to at least two course concepts or readings',
                'INSTRUCTION_3': 'Analyze the implications for citizen empowerment and data governance',
                'QUESTION_1': 'What data about you was collected, and by whom?',
                'QUESTION_2': 'How did this experience make you feel about data privacy?',
                'QUESTION_3': 'What connections do you see to course concepts?',
                'QUESTION_4': 'How might citizens be better empowered in similar situations?'
            },
            ('projects', 'timeline'): {
                'PROJECT_TITLE': 'Policy Data Analysis Project',
                'PROJECT_WEIGHT': '20% of Final Grade',
                'GROUP_SIZE': '4-6 students',
                'FINAL_DUE_DATE': 'Week 11',
                'MILESTONE_1_DATE': 'Week 5',
                'MILESTONE_2_DATE': 'Week 7',
                'MILESTONE_3_DATE': 'Week 10'
            },
            ('announcements', 'weekly_update'): {
                'WEEK_NUMBER': '4',
                'MAIN_TOPIC': 'Data Collection and Privacy',
                'KEY_ACTIVITIES': 'Reflective essay assignment, guest speaker session',
                'UPCOMING_DEADLINES': 'Essay due Friday, Week 5',
                'ADDITIONAL_NOTES': 'Remember to use the AI tutor for writing support'
            }
        }
        
        config_key = (category, template_name)
        if config_key not in sample_configs:
            # Generic sample config
            config_data = {
                'TITLE': 'Sample Title',
                'DESCRIPTION': 'Sample description',
                'DUE_DATE': 'TBD',
                'INSTRUCTIONS': 'Sample instructions'
            }
        else:
            config_data = sample_configs[config_key]
        
        # Save sample config
        config_path = self.configs_dir / f"{category}_{template_name}_sample.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        
        return str(config_path)

    def list_available_templates(self) -> Dict[str, list]:
        """List all available templates by category."""
        templates = {}
        
        if not self.templates_dir.exists():
            return templates
        
        for category_dir in self.templates_dir.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                templates[category] = []
                
                for template_file in category_dir.glob("*_template.html"):
                    template_name = template_file.stem.replace('_template', '')
                    templates[category].append(template_name)
        
        return templates

    def validate_template(self, template_path: str) -> Dict[str, Any]:
        """Validate template for common issues and extract placeholder information."""
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract all placeholders
        placeholders = re.findall(r'\{([A-Z_]+)\}', content)
        unique_placeholders = list(set(placeholders))
        
        # Check for potential issues
        issues = []
        
        # Check for unclosed HTML tags (basic check)
        if content.count('<div') != content.count('</div>'):
            issues.append("Mismatched <div> tags detected")
        
        # Check for missing alt text in images
        if '<img' in content and 'alt=' not in content:
            issues.append("Images without alt text detected")
        
        # Check for inline styles (should be minimal)
        style_count = content.count('style=')
        if style_count > 50:
            issues.append(f"High number of inline styles ({style_count})")
        
        return {
            'placeholders': unique_placeholders,
            'placeholder_count': len(unique_placeholders),
            'issues': issues,
            'template_size': len(content),
            'is_valid': len(issues) == 0
        }

def main():
    parser = argparse.ArgumentParser(description='Generate Moodle forum posts from templates')
    parser.add_argument('--category', required=True, 
                       choices=['assignments', 'projects', 'announcements', 'discussions', 'reflections'],
                       help='Template category')
    parser.add_argument('--template', required=True, help='Template name (without _template.html suffix)')
    parser.add_argument('--config', help='JSON configuration file path')
    parser.add_argument('--week', type=int, help='Week number for organization')
    parser.add_argument('--output', help='Custom output filename')
    parser.add_argument('--list-templates', action='store_true', help='List all available templates')
    parser.add_argument('--create-sample-config', action='store_true', help='Create sample config file')
    parser.add_argument('--validate', action='store_true', help='Validate template')
    parser.add_argument('--base-dir', help='Base directory for moodle_management system')
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = MoodlePostGenerator(args.base_dir)
    
    # Handle list templates command
    if args.list_templates:
        templates = generator.list_available_templates()
        print("\\n📋 Available Templates:")
        print("=" * 50)
        for category, template_list in templates.items():
            print(f"\\n📁 {category.upper()}:")
            for template in template_list:
                print(f"   • {template}")
        return
    
    # Handle create sample config command
    if args.create_sample_config:
        try:
            config_path = generator.create_sample_config(args.category, args.template)
            print(f"✅ Sample config created: {config_path}")
            print(f"💡 Edit this file and use with: --config {config_path}")
        except Exception as e:
            print(f"❌ Error creating sample config: {e}")
            sys.exit(1)
        return
    
    # Handle validate command
    if args.validate:
        try:
            template_path = generator.templates_dir / args.category / f"{args.template}_template.html"
            validation = generator.validate_template(template_path)
            
            print(f"\\n🔍 Template Validation: {args.template}")
            print("=" * 50)
            print(f"📊 Placeholders found: {validation['placeholder_count']}")
            print(f"📏 Template size: {validation['template_size']} characters")
            print(f"✅ Valid: {validation['is_valid']}")
            
            if validation['placeholders']:
                print(f"\\n🏷️  Placeholders:")
                for placeholder in sorted(validation['placeholders']):
                    print(f"   • {placeholder}")
            
            if validation['issues']:
                print(f"\\n⚠️  Issues found:")
                for issue in validation['issues']:
                    print(f"   • {issue}")
            
        except Exception as e:
            print(f"❌ Error validating template: {e}")
            sys.exit(1)
        return
    
    # Generate post
    try:
        # Load configuration
        if args.config:
            parameters = generator.load_config(args.config)
        else:
            # Use minimal default parameters
            parameters = {
                'TITLE': f"{args.template.replace('_', ' ').title()}",
                'WEEK_NUMBER': str(args.week) if args.week else 'TBD'
            }
        
        # Generate the post
        output_path = generator.generate_post(
            category=args.category,
            template_name=args.template,
            parameters=parameters,
            output_name=args.output,
            week=args.week
        )
        
        print(f"✅ Forum post generated successfully!")
        print(f"📁 Output file: {output_path}")
        print(f"🔗 Ready to copy and paste into Moodle")
        
        # Show template validation info
        template_path = generator.templates_dir / args.category / f"{args.template}_template.html"
        validation = generator.validate_template(template_path)
        
        if not validation['is_valid']:
            print(f"\\n⚠️  Template validation warnings:")
            for issue in validation['issues']:
                print(f"   • {issue}")
        
    except Exception as e:
        print(f"❌ Error generating post: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
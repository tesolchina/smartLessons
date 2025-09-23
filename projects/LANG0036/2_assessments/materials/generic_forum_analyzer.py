#!/usr/bin/env python3
"""
Generic Forum Analysis Engine
=============================

A configurable, instruction-based forum analysis system that can process 
any JSON forum export based on configuration files.

Usage:
    python3 generic_forum_analyzer.py config_file.json
    python3 generic_forum_analyzer.py --list-configs
    python3 generic_forum_analyzer.py --validate config_file.json
"""

import json
import re
import pandas as pd
import os
import sys
import argparse
from collections import defaultdict
from datetime import datetime
from pathlib import Path

class GenericForumAnalyzer:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = {}
        self.posts = []
        self.enrolled_students = {}
        self.student_submissions = defaultdict(list)
        self.instructor_posts = []
        
        # Load configuration
        self._load_config()
        self._validate_config()
    
    def _load_config(self):
        """Load analysis configuration from JSON file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"✅ Configuration loaded: {self.config['analysis_config']['name']}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def _validate_config(self):
        """Validate configuration structure"""
        required_sections = [
            'analysis_config', 'data_sources', 'json_structure', 
            'content_classification', 'report_generation'
        ]
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        print(f"✅ Configuration validated")
    
    def load_data(self):
        """Load forum data and student list based on configuration"""
        print("🔄 Loading data sources...")
        
        # Load forum JSON
        forum_json_path = self.config['data_sources']['forum_json']
        with open(forum_json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # Extract posts based on configured path
        posts_path = self.config['json_structure']['posts_path']
        if posts_path.startswith('[') and posts_path.endswith(']'):
            # Array index access
            index = int(posts_path[1:-1])
            self.posts = raw_data[index] if isinstance(raw_data[index], list) else raw_data
        else:
            self.posts = raw_data
        
        print(f"✅ Forum data loaded: {len(self.posts)} posts")
        
        # Load student enrollment if specified
        if 'student_csv' in self.config['data_sources']:
            self._load_student_data()
        
        # Organize posts
        self._organize_posts()
    
    def _load_student_data(self):
        """Load student enrollment data"""
        csv_path = self.config['data_sources']['student_csv']
        csv_config = self.config.get('student_csv_structure', {})
        
        df = pd.read_csv(csv_path)
        
        name_col = csv_config.get('student_name_column', 'Student Name')
        section_col = csv_config.get('section_column', 'Section Code')
        id_col = csv_config.get('student_id_column', 'Student No.')
        
        for _, row in df.iterrows():
            student_name = str(row[name_col]).strip()
            section = str(row[section_col]).strip()
            student_id = str(row[id_col]).strip()
            
            self.enrolled_students[student_name] = {
                'id': student_id,
                'section': section,
                'participated': False
            }
        
        print(f"✅ Student enrollment loaded: {len(self.enrolled_students)} students")
    
    def _organize_posts(self):
        """Organize posts by user type based on configuration"""
        field_config = self.config['json_structure']['post_fields']
        instructor_names = self.config['json_structure'].get('instructor_names', [])
        
        user_field = field_config['user']
        
        for post in self.posts:
            username = post.get(user_field, 'Unknown')
            
            if username in instructor_names:
                self.instructor_posts.append(post)
            else:
                self.student_submissions[username].append(post)
                # Mark participation if student list loaded
                if username in self.enrolled_students:
                    self.enrolled_students[username]['participated'] = True
        
        print(f"📊 Posts organized: {len(self.student_submissions)} students, {len(self.instructor_posts)} instructor posts")
    
    def clean_html(self, html_content: str) -> str:
        """Remove HTML tags and clean text"""
        text = re.sub(r'<[^>]+>', ' ', html_content)
        text = re.sub(r'\\s+', ' ', text).strip()
        return text
    
    def classify_content(self, text: str) -> list:
        """Classify content based on configured rules"""
        content_types = []
        text_lower = text.lower()
        
        components = self.config['content_classification']['assignment_components']
        exclusions = self.config['content_classification'].get('exclusion_patterns', [])
        
        # Check for exclusion patterns first
        is_excluded = any(pattern.lower() in text_lower for pattern in exclusions)
        if is_excluded:
            return ["⚠️ Template/Example"]
        
        # Check each component
        for component in components:
            indicators = component['indicators']
            min_length = component.get('min_length', 0)
            
            has_indicator = any(indicator.lower() in text_lower for indicator in indicators)
            meets_length = len(text) >= min_length
            
            if has_indicator and meets_length:
                emoji = component.get('emoji', '📄')
                name = component['name']
                content_types.append(f"{emoji} {name}")
        
        return content_types if content_types else ["📄 General Reply"]
    
    def analyze_completion(self, posts: list) -> dict:
        """Analyze completion based on configured components"""
        components = self.config['content_classification']['assignment_components']
        component_found = {comp['name']: False for comp in components}
        
        field_config = self.config['json_structure']['post_fields']
        message_field = field_config['message']
        
        for post in posts:
            message = post.get(message_field, '')
            clean_message = self.clean_html(message)
            content_types = self.classify_content(clean_message)
            
            for component in components:
                component_name = component['name']
                component_marker = f"{component.get('emoji', '📄')} {component_name}"
                if component_marker in content_types:
                    component_found[component_name] = True
        
        completion_config = self.config['analysis_criteria']['completion_threshold']
        total_found = sum(component_found.values())
        
        return {
            'components': component_found,
            'score': total_found,
            'total': len(components),
            'status': self._get_completion_status(total_found, completion_config)
        }
    
    def _get_completion_status(self, score: int, thresholds: dict) -> str:
        """Determine completion status based on score and thresholds"""
        complete_threshold = thresholds['complete']
        partial_threshold = thresholds['partial']
        
        if score >= complete_threshold:
            return "🌟 COMPLETE SUBMISSION"
        elif score >= partial_threshold:
            return "🟡 PARTIAL SUBMISSION"
        else:
            return "❌ NO VALID CONTENT"
    
    def format_timestamp(self, timestamp):
        """Convert timestamp to readable format"""
        try:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return str(timestamp)
    
    def generate_individual_report(self):
        """Generate individual student report based on configuration"""
        report_config = self.config['report_generation']['individual_report']
        field_config = self.config['json_structure']['post_fields']
        
        report_lines = []
        report_lines.append(f"# {report_config['title']}")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**Total Participants:** {len(self.student_submissions)}")
        report_lines.append("")
        
        for student_name, posts in sorted(self.student_submissions.items()):
            posts.sort(key=lambda x: x.get(field_config['created'], 0))
            
            report_lines.append(f"## {student_name}")
            
            # Add section info if available
            if student_name in self.enrolled_students:
                section = self.enrolled_students[student_name]['section']
                report_lines.append(f"**Section:** {section}")
            else:
                report_lines.append("**Section:** NOT IN ENROLLMENT LIST")
            
            report_lines.append(f"**Total Posts:** {len(posts)}")
            report_lines.append("")
            
            # Analyze completion
            completion = self.analyze_completion(posts)
            
            # Add individual posts
            for i, post in enumerate(posts, 1):
                subject = post.get(field_config['subject'], '')
                message = post.get(field_config['message'], '')
                word_count = post.get(field_config['wordcount'], 0)
                created = post.get(field_config['created'], 0)
                
                clean_message = self.clean_html(message)
                content_types = self.classify_content(clean_message)
                
                report_lines.append(f"### Post {i}: {subject}")
                report_lines.append(f"- **Posted:** {self.format_timestamp(created)}")
                report_lines.append(f"- **Word Count:** {word_count}")
                report_lines.append(f"- **Content Type:** {', '.join(content_types)}")
                report_lines.append("")
                
                if report_config.get('include_full_content', False):
                    report_lines.append("**Full Content:**")
                    report_lines.append("```")
                    content_length = report_config.get('content_preview_length', 1000)
                    if len(clean_message) > content_length:
                        report_lines.append(clean_message[:content_length] + "...")
                    else:
                        report_lines.append(clean_message)
                    report_lines.append("```")
                    report_lines.append("")
            
            # Completion summary
            report_lines.append("### Completion Summary")
            report_lines.append(f"**Score:** {completion['score']}/{completion['total']} components")
            
            components = self.config['content_classification']['assignment_components']
            for component in components:
                name = component['name']
                status = "✅" if completion['components'][name] else "❌"
                report_lines.append(f"- {status} {name}")
            
            report_lines.append(f"**Status:** {completion['status']}")
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")
        
        # Save report
        output_dir = self.config['data_sources']['output_directory']
        os.makedirs(output_dir, exist_ok=True)
        filename = report_config['filename']
        
        with open(f"{output_dir}/{filename}", 'w', encoding='utf-8') as f:
            f.write('\\n'.join(report_lines))
        
        print(f"✅ Individual report saved: {output_dir}/{filename}")
    
    def generate_overall_report(self):
        """Generate overall analysis report with section breakdown"""
        report_config = self.config['report_generation']['overall_report']
        
        report_lines = []
        report_lines.append(f"# {report_config['title']}")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.enrolled_students:
            report_lines.append(f"**Total Enrolled Students:** {len(self.enrolled_students)}")
        
        report_lines.append("")
        
        # Overall participation stats
        total_participants = len(self.student_submissions)
        report_lines.append("## Overall Participation Statistics")
        report_lines.append("")
        report_lines.append(f"- **Forum Participants:** {total_participants} students")
        
        if self.enrolled_students:
            no_participation = len([s for s in self.enrolled_students.values() if not s['participated']])
            report_lines.append(f"- **No Participation:** {no_participation} students")
        
        report_lines.append("")
        
        # Section breakdown if available
        if self.enrolled_students and report_config.get('include_section_breakdown', False):
            self._add_section_breakdown(report_lines)
        
        # Completion analysis
        self._add_completion_analysis(report_lines)
        
        # Save report
        output_dir = self.config['data_sources']['output_directory']
        os.makedirs(output_dir, exist_ok=True)
        filename = report_config['filename']
        
        with open(f"{output_dir}/{filename}", 'w', encoding='utf-8') as f:
            f.write('\\n'.join(report_lines))
        
        print(f"✅ Overall report saved: {output_dir}/{filename}")
    
    def _add_section_breakdown(self, report_lines: list):
        """Add section-based analysis to report"""
        # Organize by section
        sections = defaultdict(lambda: {'enrolled': [], 'participants': [], 'no_participation': []})
        
        for student_name, data in self.enrolled_students.items():
            section = data['section']
            sections[section]['enrolled'].append(student_name)
            
            if data['participated']:
                sections[section]['participants'].append(student_name)
            else:
                sections[section]['no_participation'].append(student_name)
        
        report_lines.append("## Section-Based Analysis")
        report_lines.append("")
        
        for section in sorted(sections.keys()):
            data = sections[section]
            total_enrolled = len(data['enrolled'])
            participants = len(data['participants'])
            no_participation = len(data['no_participation'])
            
            report_lines.append(f"### Section {section}")
            report_lines.append(f"- **Total Enrolled:** {total_enrolled}")
            report_lines.append(f"- **Participants:** {participants}")
            report_lines.append(f"- **No Participation:** {no_participation}")
            report_lines.append("")
            
            if data['no_participation']:
                report_lines.append("**Students with No Participation:**")
                for student in data['no_participation']:
                    report_lines.append(f"- {student}")
                report_lines.append("")
    
    def _add_completion_analysis(self, report_lines: list):
        """Add completion quality analysis to report"""
        complete_count = 0
        partial_count = 0
        no_content_count = 0
        
        completion_config = self.config['analysis_criteria']['completion_threshold']
        
        for student_name, posts in self.student_submissions.items():
            completion = self.analyze_completion(posts)
            
            if completion['score'] >= completion_config['complete']:
                complete_count += 1
            elif completion['score'] >= completion_config['partial']:
                partial_count += 1
            else:
                no_content_count += 1
        
        total_participants = len(self.student_submissions)
        
        report_lines.append("## Assignment Completion Quality")
        report_lines.append("")
        
        if total_participants > 0:
            report_lines.append(f"- **Complete Submissions:** {complete_count} ({complete_count/total_participants*100:.1f}%)")
            report_lines.append(f"- **Partial Submissions:** {partial_count} ({partial_count/total_participants*100:.1f}%)")
            report_lines.append(f"- **No Valid Content:** {no_content_count} ({no_content_count/total_participants*100:.1f}%)")
        else:
            report_lines.append("- **No participants found**")
        
        report_lines.append("")
    
    def run_analysis(self):
        """Execute complete analysis workflow"""
        print(f"🚀 Starting {self.config['analysis_config']['name']}")
        print("=" * 60)
        
        self.load_data()
        
        print("\\n📊 Generating reports...")
        self.generate_individual_report()
        self.generate_overall_report()
        
        print("\\n🎉 Analysis complete!")

def list_available_configs():
    """List all available configuration files"""
    config_files = list(Path('.').glob('config_*.json'))
    
    if not config_files:
        print("No configuration files found.")
        return
    
    print("Available Configuration Files:")
    print("=" * 40)
    
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            name = config['analysis_config']['name']
            description = config['analysis_config'].get('description', 'No description')
            print(f"📄 {config_file}")
            print(f"   Name: {name}")
            print(f"   Description: {description}")
            print()
        except Exception as e:
            print(f"❌ {config_file} - Error reading: {e}")

def validate_config(config_file: str):
    """Validate a configuration file"""
    try:
        analyzer = GenericForumAnalyzer(config_file)
        print(f"✅ Configuration file '{config_file}' is valid")
        return True
    except Exception as e:
        print(f"❌ Configuration file '{config_file}' is invalid: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generic Forum Analysis Engine')
    parser.add_argument('config_file', nargs='?', help='Configuration file path')
    parser.add_argument('--list-configs', action='store_true', help='List available configuration files')
    parser.add_argument('--validate', action='store_true', help='Validate configuration file without running analysis')
    
    args = parser.parse_args()
    
    if args.list_configs:
        list_available_configs()
        return
    
    if not args.config_file:
        print("Error: Configuration file required")
        print("Use --list-configs to see available configurations")
        sys.exit(1)
    
    if args.validate:
        if validate_config(args.config_file):
            sys.exit(0)
        else:
            sys.exit(1)
    
    try:
        analyzer = GenericForumAnalyzer(args.config_file)
        analyzer.run_analysis()
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
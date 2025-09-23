#!/usr/bin/env python3
"""
HTML Template Validator for Moodle Management System
===================================================

Validates HTML templates for common issues, placeholder usage, and accessibility.
This tool helps ensure template quality and consistency across the course content.

Usage:
    python validate_html.py --check-all
    python validate_html.py --template assignments/reflective_essay_template.html
    python validate_html.py --category assignments
    python validate_html.py --fix-issues --backup
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Any
from html.parser import HTMLParser
import json

class HTMLTemplateValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.issues = []
        self.placeholders = []
        self.links = []
        self.images = []
        self.styles_count = 0
        
    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        
        # Check for images without alt text
        if tag == 'img':
            has_alt = any(attr[0] == 'alt' for attr in attrs)
            if not has_alt:
                self.issues.append("Image without alt text detected")
            self.images.append(dict(attrs))
        
        # Check for links
        if tag == 'a':
            href = next((attr[1] for attr in attrs if attr[0] == 'href'), None)
            if href:
                self.links.append(href)
        
        # Count inline styles
        if any(attr[0] == 'style' for attr in attrs):
            self.styles_count += 1
    
    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        else:
            self.issues.append(f"Mismatched closing tag: {tag}")
    
    def handle_data(self, data):
        # Find placeholders
        placeholders = re.findall(r'\{([A-Z_]+)\}', data)
        self.placeholders.extend(placeholders)
    
    def error(self, message):
        self.issues.append(f"HTML parsing error: {message}")

class MoodleTemplateValidator:
    def __init__(self, base_dir: str = None):
        """Initialize validator with base directory."""
        if base_dir is None:
            script_dir = Path(__file__).parent
            self.base_dir = script_dir.parent
        else:
            self.base_dir = Path(base_dir)
        
        self.templates_dir = self.base_dir / "templates"
        
        # Define validation rules
        self.required_placeholders = {
            'assignments': ['COURSE_CODE', 'DUE_DATE', 'SUBMISSION_METHOD'],
            'projects': ['COURSE_CODE', 'PROJECT_TITLE', 'FINAL_DUE_DATE'],
            'announcements': ['COURSE_CODE', 'CURRENT_DATE'],
            'discussions': ['COURSE_CODE', 'TOPIC'],
            'reflections': ['COURSE_CODE', 'WORD_COUNT']
        }
        
        self.brand_colors = [
            '#4a90e2',  # Primary blue
            '#28a745',  # Success green
            '#ffc107',  # Warning yellow
            '#17a2b8',  # Info blue
            '#dc3545'   # Danger red
        ]
    
    def validate_template(self, template_path: Path) -> Dict[str, Any]:
        """Validate a single template file."""
        if not template_path.exists():
            return {
                'valid': False,
                'error': f"Template file not found: {template_path}",
                'issues': [],
                'warnings': [],
                'placeholders': [],
                'metrics': {}
            }
        
        # Read template content
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                'valid': False,
                'error': f"Error reading template: {e}",
                'issues': [],
                'warnings': [],
                'placeholders': [],
                'metrics': {}
            }
        
        # Parse HTML
        parser = HTMLTemplateValidator()
        try:
            parser.feed(content)
        except Exception as e:
            parser.issues.append(f"HTML parsing failed: {e}")
        
        # Extract template category from path
        category = template_path.parent.name
        
        # Perform validations
        issues = parser.issues.copy()
        warnings = []
        
        # Check for unclosed tags
        if parser.tag_stack:
            issues.append(f"Unclosed HTML tags: {', '.join(parser.tag_stack)}")
        
        # Check placeholder format
        invalid_placeholders = []
        for placeholder in parser.placeholders:
            if not re.match(r'^[A-Z_]+$', placeholder):
                invalid_placeholders.append(placeholder)
        
        if invalid_placeholders:
            issues.append(f"Invalid placeholder format: {', '.join(invalid_placeholders)}")
        
        # Check required placeholders for category
        if category in self.required_placeholders:
            required = set(self.required_placeholders[category])
            found = set(parser.placeholders)
            missing = required - found
            
            if missing:
                warnings.append(f"Missing recommended placeholders: {', '.join(missing)}")
        
        # Check for brand color usage
        brand_color_usage = 0
        for color in self.brand_colors:
            if color.lower() in content.lower():
                brand_color_usage += 1
        
        if brand_color_usage == 0:
            warnings.append("No brand colors detected in template")
        
        # Check inline styles count
        if parser.styles_count > 50:
            warnings.append(f"High number of inline styles: {parser.styles_count}")
        
        # Check for accessibility issues
        if len(parser.images) > 0:
            images_without_alt = sum(1 for img in parser.images if 'alt' not in img)
            if images_without_alt > 0:
                issues.append(f"{images_without_alt} images without alt text")
        
        # Check for responsive design indicators
        responsive_indicators = ['max-width', 'min-width', '@media', 'viewport']
        has_responsive = any(indicator in content for indicator in responsive_indicators)
        
        if not has_responsive:
            warnings.append("No responsive design indicators found")
        
        # Calculate metrics
        metrics = {
            'file_size': len(content),
            'placeholder_count': len(set(parser.placeholders)),
            'unique_placeholders': len(set(parser.placeholders)),
            'inline_styles': parser.styles_count,
            'links_count': len(parser.links),
            'images_count': len(parser.images),
            'brand_colors_used': brand_color_usage
        }
        
        # Determine overall validity
        is_valid = len(issues) == 0
        
        return {
            'valid': is_valid,
            'issues': issues,
            'warnings': warnings,
            'placeholders': list(set(parser.placeholders)),
            'links': parser.links,
            'metrics': metrics,
            'category': category,
            'template_name': template_path.stem.replace('_template', '')
        }
    
    def validate_category(self, category: str) -> Dict[str, Any]:
        """Validate all templates in a category."""
        category_dir = self.templates_dir / category
        
        if not category_dir.exists():
            return {
                'error': f"Category directory not found: {category}",
                'templates': []
            }
        
        results = {
            'category': category,
            'templates': [],
            'summary': {
                'total': 0,
                'valid': 0,
                'invalid': 0,
                'warnings': 0
            }
        }
        
        # Find all template files
        template_files = list(category_dir.glob("*_template.html"))
        
        for template_file in template_files:
            validation = self.validate_template(template_file)
            results['templates'].append({
                'filename': template_file.name,
                'path': str(template_file),
                'validation': validation
            })
            
            results['summary']['total'] += 1
            if validation['valid']:
                results['summary']['valid'] += 1
            else:
                results['summary']['invalid'] += 1
            
            if validation.get('warnings', []):
                results['summary']['warnings'] += len(validation['warnings'])
        
        return results
    
    def validate_all(self) -> Dict[str, Any]:
        """Validate all templates in all categories."""
        if not self.templates_dir.exists():
            return {
                'error': f"Templates directory not found: {self.templates_dir}",
                'categories': []
            }
        
        results = {
            'validation_date': Path(__file__).stat().st_mtime,
            'categories': [],
            'overall_summary': {
                'total_templates': 0,
                'valid_templates': 0,
                'invalid_templates': 0,
                'total_warnings': 0,
                'categories_count': 0
            }
        }
        
        # Find all category directories
        categories = [d for d in self.templates_dir.iterdir() if d.is_dir()]
        
        for category_dir in categories:
            category_results = self.validate_category(category_dir.name)
            
            if 'error' not in category_results:
                results['categories'].append(category_results)
                
                # Update overall summary
                summary = category_results['summary']
                results['overall_summary']['total_templates'] += summary['total']
                results['overall_summary']['valid_templates'] += summary['valid']
                results['overall_summary']['invalid_templates'] += summary['invalid']
                results['overall_summary']['total_warnings'] += summary['warnings']
                results['overall_summary']['categories_count'] += 1
        
        return results
    
    def print_validation_report(self, results: Dict[str, Any]) -> None:
        """Print a formatted validation report."""
        if 'error' in results:
            print(f"❌ {results['error']}")
            return
        
        # Print overall summary
        if 'overall_summary' in results:
            summary = results['overall_summary']
            print(f"\\n🔍 Template Validation Report")
            print("=" * 50)
            print(f"📊 Total Templates: {summary['total_templates']}")
            print(f"✅ Valid: {summary['valid_templates']}")
            print(f"❌ Invalid: {summary['invalid_templates']}")
            print(f"⚠️  Warnings: {summary['total_warnings']}")
            print(f"📁 Categories: {summary['categories_count']}")
            
            # Calculate success rate
            if summary['total_templates'] > 0:
                success_rate = (summary['valid_templates'] / summary['total_templates']) * 100
                print(f"📈 Success Rate: {success_rate:.1f}%")
        
        # Print category details
        if 'categories' in results:
            for category in results['categories']:
                print(f"\\n📁 {category['category'].upper()}")
                print("-" * 30)
                
                for template in category['templates']:
                    validation = template['validation']
                    status = "✅" if validation['valid'] else "❌"
                    warnings_count = len(validation.get('warnings', []))
                    warning_indicator = f" ⚠️ {warnings_count}" if warnings_count > 0 else ""
                    
                    print(f"  {status} {template['filename']}{warning_indicator}")
                    
                    # Print issues
                    for issue in validation.get('issues', []):
                        print(f"     ❌ {issue}")
                    
                    # Print warnings
                    for warning in validation.get('warnings', []):
                        print(f"     ⚠️  {warning}")
                    
                    # Print metrics summary
                    metrics = validation.get('metrics', {})
                    if metrics:
                        print(f"     📊 {metrics.get('placeholder_count', 0)} placeholders, "
                              f"{metrics.get('file_size', 0)} bytes, "
                              f"{metrics.get('inline_styles', 0)} styles")
        
        # Single template results
        elif 'valid' in results:
            template_name = results.get('template_name', 'Template')
            status = "✅ Valid" if results['valid'] else "❌ Invalid"
            print(f"\\n🔍 {template_name}: {status}")
            
            if results.get('issues'):
                print("\\n❌ Issues:")
                for issue in results['issues']:
                    print(f"   • {issue}")
            
            if results.get('warnings'):
                print("\\n⚠️  Warnings:")
                for warning in results['warnings']:
                    print(f"   • {warning}")
            
            if results.get('placeholders'):
                print(f"\\n🏷️  Placeholders ({len(results['placeholders'])}):")
                for placeholder in sorted(results['placeholders']):
                    print(f"   • {placeholder}")
            
            metrics = results.get('metrics', {})
            if metrics:
                print(f"\\n📊 Metrics:")
                print(f"   • File size: {metrics.get('file_size', 0)} bytes")
                print(f"   • Placeholders: {metrics.get('placeholder_count', 0)}")
                print(f"   • Inline styles: {metrics.get('inline_styles', 0)}")
                print(f"   • Links: {metrics.get('links_count', 0)}")
                print(f"   • Images: {metrics.get('images_count', 0)}")
    
    def fix_common_issues(self, template_path: Path, backup: bool = True) -> bool:
        """Attempt to fix common template issues automatically."""
        if not template_path.exists():
            return False
        
        # Create backup if requested
        if backup:
            backup_path = template_path.with_suffix(f"{template_path.suffix}.backup")
            backup_path.write_text(template_path.read_text(encoding='utf-8'), encoding='utf-8')
            print(f"📁 Backup created: {backup_path}")
        
        try:
            content = template_path.read_text(encoding='utf-8')
            original_content = content
            
            # Fix common placeholder format issues
            content = re.sub(r'\{([a-z_]+)\}', lambda m: f"{{{m.group(1).upper()}}}", content)
            
            # Add alt text to images without it
            content = re.sub(r'<img([^>]*?)(?<!alt=")>', r'<img\1 alt="Image">', content)
            
            # Fix basic HTML structure issues (very simple fixes)
            # This is a basic example - more sophisticated fixes would require proper HTML parsing
            
            if content != original_content:
                template_path.write_text(content, encoding='utf-8')
                print(f"✅ Fixed issues in: {template_path}")
                return True
            else:
                print(f"ℹ️  No fixes needed for: {template_path}")
                return True
                
        except Exception as e:
            print(f"❌ Error fixing template: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Validate HTML templates for Moodle management system')
    
    parser.add_argument('--check-all', action='store_true', help='Validate all templates')
    parser.add_argument('--template', help='Validate specific template file')
    parser.add_argument('--category', help='Validate all templates in category')
    parser.add_argument('--fix-issues', action='store_true', help='Attempt to fix common issues')
    parser.add_argument('--backup', action='store_true', help='Create backups when fixing')
    parser.add_argument('--output-json', help='Output results as JSON file')
    parser.add_argument('--base-dir', help='Base directory for moodle_management system')
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = MoodleTemplateValidator(args.base_dir)
    
    # Determine validation scope
    if args.check_all:
        results = validator.validate_all()
    elif args.category:
        results = validator.validate_category(args.category)
    elif args.template:
        template_path = Path(args.template)
        if not template_path.is_absolute():
            template_path = validator.templates_dir / args.template
        results = validator.validate_template(template_path)
    else:
        print("❌ Please specify validation scope: --check-all, --category, or --template")
        sys.exit(1)
    
    # Fix issues if requested
    if args.fix_issues:
        if args.template:
            template_path = Path(args.template)
            if not template_path.is_absolute():
                template_path = validator.templates_dir / args.template
            validator.fix_common_issues(template_path, args.backup)
        else:
            print("⚠️  Fix mode only works with --template option")
    
    # Output results
    if args.output_json:
        with open(args.output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"📁 Results saved to: {args.output_json}")
    
    # Print report
    validator.print_validation_report(results)
    
    # Exit with error code if validation failed
    if isinstance(results, dict):
        if 'valid' in results and not results['valid']:
            sys.exit(1)
        elif 'overall_summary' in results and results['overall_summary']['invalid_templates'] > 0:
            sys.exit(1)

if __name__ == "__main__":
    main()
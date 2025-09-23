#!/usr/bin/env python3
"""
GCAP3226 Moodle Link Manager
============================

Manage and organize Moodle forum discussion links with search, filtering, and reporting capabilities.

Usage:
    python update_links.py --add "Discussion Title" --url "https://..." --category "assignments"
    python update_links.py --list --filter-category "project" 
    python update_links.py --search "reflection"
    python update_links.py --export --format html
    python update_links.py --validate-links
"""

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
from urllib.parse import urlparse
import webbrowser

class MoodleLinkManager:
    def __init__(self, base_dir: str = None):
        """Initialize the link manager with base directory."""
        if base_dir is None:
            script_dir = Path(__file__).parent
            self.base_dir = script_dir.parent
        else:
            self.base_dir = Path(base_dir)
        
        self.links_dir = self.base_dir / "links_database"
        self.links_file = self.links_dir / "forum_links.csv"
        self.categories_file = self.links_dir / "link_categories.json"
        
        # Ensure directories exist
        self.links_dir.mkdir(parents=True, exist_ok=True)
        
        # Load categories
        self.categories = self.load_categories()
    
    def load_categories(self) -> Dict[str, Any]:
        """Load category definitions from JSON file."""
        if self.categories_file.exists():
            with open(self.categories_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_links(self) -> List[Dict[str, str]]:
        """Load all forum links from CSV file."""
        links = []
        if self.links_file.exists():
            with open(self.links_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                links = list(reader)
        return links
    
    def save_links(self, links: List[Dict[str, str]]) -> None:
        """Save forum links to CSV file."""
        if not links:
            return
        
        fieldnames = [
            'Course Title', 'Forum Type', 'Week', 'Topic', 'Description',
            'Moodle URL', 'Creation Date', 'Status', 'Category', 'Tags'
        ]
        
        with open(self.links_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(links)
    
    def add_link(self, 
                topic: str,
                url: str,
                category: str,
                description: str = "",
                forum_type: str = "discussion",
                week: str = "TBD",
                status: str = "active",
                tags: str = "") -> bool:
        """Add a new forum link to the database."""
        
        # Validate category
        if category not in self.categories.get('categories', {}):
            print(f"⚠️  Warning: Category '{category}' not in predefined categories")
        
        # Load existing links
        links = self.load_links()
        
        # Check for duplicates
        for link in links:
            if link['Moodle URL'] == url:
                print(f"❌ Link already exists: {link['Topic']}")
                return False
        
        # Create new link entry
        new_link = {
            'Course Title': 'GCAP3226',
            'Forum Type': forum_type,
            'Week': week,
            'Topic': topic,
            'Description': description,
            'Moodle URL': url,
            'Creation Date': datetime.now().strftime('%Y-%m-%d'),
            'Status': status,
            'Category': category,
            'Tags': tags
        }
        
        # Add to links and save
        links.append(new_link)
        self.save_links(links)
        
        print(f"✅ Added link: {topic}")
        return True
    
    def update_link(self, url: str, updates: Dict[str, str]) -> bool:
        """Update an existing link by URL."""
        links = self.load_links()
        
        for i, link in enumerate(links):
            if link['Moodle URL'] == url:
                # Update fields
                for key, value in updates.items():
                    if key in link:
                        links[i][key] = value
                
                self.save_links(links)
                print(f"✅ Updated link: {link['Topic']}")
                return True
        
        print(f"❌ Link not found: {url}")
        return False
    
    def delete_link(self, url: str) -> bool:
        """Delete a link by URL."""
        links = self.load_links()
        
        original_count = len(links)
        links = [link for link in links if link['Moodle URL'] != url]
        
        if len(links) < original_count:
            self.save_links(links)
            print(f"✅ Deleted link: {url}")
            return True
        
        print(f"❌ Link not found: {url}")
        return False
    
    def search_links(self, 
                    query: str = None,
                    category: str = None,
                    status: str = None,
                    week: str = None,
                    forum_type: str = None) -> List[Dict[str, str]]:
        """Search and filter links based on criteria."""
        links = self.load_links()
        
        filtered_links = []
        for link in links:
            # Apply filters
            if category and link['Category'] != category:
                continue
            if status and link['Status'] != status:
                continue
            if week and link['Week'] != week:
                continue
            if forum_type and link['Forum Type'] != forum_type:
                continue
            
            # Apply text search
            if query:
                search_text = f"{link['Topic']} {link['Description']} {link['Tags']}".lower()
                if query.lower() not in search_text:
                    continue
            
            filtered_links.append(link)
        
        return filtered_links
    
    def list_links(self, filters: Dict[str, str] = None) -> None:
        """Display links in a formatted table."""
        if filters is None:
            filters = {}
        
        links = self.search_links(**filters)
        
        if not links:
            print("📭 No links found matching criteria")
            return
        
        # Print header
        print(f"\\n📋 Forum Links ({len(links)} found)")
        print("=" * 80)
        
        # Group by category for better organization
        by_category = {}
        for link in links:
            category = link['Category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(link)
        
        for category, category_links in by_category.items():
            category_info = self.categories.get('categories', {}).get(category, {})
            icon = category_info.get('icon', '📎')
            
            print(f"\\n{icon} {category.upper()} ({len(category_links)} links)")
            print("-" * 40)
            
            for link in category_links:
                status_icon = "🟢" if link['Status'] == 'active' else "🟡" if link['Status'] == 'planned' else "⚪"
                print(f"  {status_icon} Week {link['Week']}: {link['Topic']}")
                if link['Description']:
                    print(f"     📝 {link['Description']}")
                print(f"     🔗 {link['Moodle URL']}")
                if link['Tags']:
                    tags = link['Tags'].split(';')
                    print(f"     🏷️  {', '.join(tags)}")
                print()
    
    def validate_links(self) -> Dict[str, List[str]]:
        """Validate all links and check for issues."""
        links = self.load_links()
        results = {
            'valid': [],
            'invalid': [],
            'unreachable': [],
            'warnings': []
        }
        
        print(f"🔍 Validating {len(links)} links...")
        
        for link in links:
            url = link['Moodle URL']
            topic = link['Topic']
            
            # Basic URL format validation
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                results['invalid'].append(f"{topic}: Invalid URL format")
                continue
            
            # Check for placeholder URLs
            if '...' in url or 'TBD' in url or 'example' in url:
                results['warnings'].append(f"{topic}: Placeholder URL detected")
                continue
            
            # Try to reach the URL (optional, can be slow)
            try:
                # Skip actual HTTP requests for Moodle URLs (requires authentication)
                if 'moodle' in url.lower():
                    results['valid'].append(f"{topic}: Moodle URL (not verified)")
                else:
                    response = requests.head(url, timeout=5)
                    if response.status_code < 400:
                        results['valid'].append(f"{topic}: OK ({response.status_code})")
                    else:
                        results['unreachable'].append(f"{topic}: HTTP {response.status_code}")
            except requests.RequestException as e:
                results['unreachable'].append(f"{topic}: Connection error")
        
        # Print results
        print(f"\\n📊 Validation Results:")
        print(f"✅ Valid: {len(results['valid'])}")
        print(f"❌ Invalid: {len(results['invalid'])}")
        print(f"🔗 Unreachable: {len(results['unreachable'])}")
        print(f"⚠️  Warnings: {len(results['warnings'])}")
        
        if results['invalid']:
            print(f"\\n❌ Invalid URLs:")
            for item in results['invalid']:
                print(f"   • {item}")
        
        if results['warnings']:
            print(f"\\n⚠️  Warnings:")
            for item in results['warnings']:
                print(f"   • {item}")
        
        return results
    
    def export_links(self, format_type: str = 'html', output_file: str = None) -> str:
        """Export links in various formats."""
        links = self.load_links()
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"forum_links_export_{timestamp}.{format_type}"
        
        output_path = self.links_dir / output_file
        
        if format_type == 'html':
            self._export_html(links, output_path)
        elif format_type == 'json':
            self._export_json(links, output_path)
        elif format_type == 'markdown':
            self._export_markdown(links, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
        
        print(f"✅ Exported {len(links)} links to: {output_path}")
        return str(output_path)
    
    def _export_html(self, links: List[Dict[str, str]], output_path: Path) -> None:
        """Export links as HTML page."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GCAP3226 Forum Links Directory</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        .header {{ background-color: #4a90e2; color: white; padding: 20px; text-align: center; }}
        .category {{ margin: 20px 0; }}
        .category h2 {{ background-color: #f0f8ff; padding: 10px; border-left: 4px solid #4a90e2; }}
        .link-item {{ background-color: #f9f9f9; margin: 10px 0; padding: 15px; border-radius: 5px; }}
        .link-meta {{ font-size: 0.9em; color: #666; }}
        .tags {{ margin-top: 5px; }}
        .tag {{ background-color: #e0e0e0; padding: 2px 6px; border-radius: 3px; font-size: 0.8em; margin-right: 5px; }}
        .status-active {{ color: green; font-weight: bold; }}
        .status-planned {{ color: orange; font-weight: bold; }}
        .status-archived {{ color: gray; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 GCAP3226 Forum Links Directory</h1>
        <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        <p>Total Links: {len(links)}</p>
    </div>
"""
        
        # Group by category
        by_category = {}
        for link in links:
            category = link['Category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(link)
        
        for category, category_links in sorted(by_category.items()):
            category_info = self.categories.get('categories', {}).get(category, {})
            icon = category_info.get('icon', '📎')
            
            html_content += f"""
    <div class="category">
        <h2>{icon} {category.title()} ({len(category_links)} links)</h2>
"""
            
            for link in category_links:
                status_class = f"status-{link['Status']}"
                tags_html = ""
                if link['Tags']:
                    tags = link['Tags'].split(';')
                    tags_html = '<div class="tags">' + ''.join([f'<span class="tag">{tag.strip()}</span>' for tag in tags]) + '</div>'
                
                html_content += f"""
        <div class="link-item">
            <h3><a href="{link['Moodle URL']}" target="_blank">{link['Topic']}</a></h3>
            <p>{link['Description']}</p>
            <div class="link-meta">
                <strong>Week:</strong> {link['Week']} | 
                <strong>Type:</strong> {link['Forum Type']} | 
                <strong>Status:</strong> <span class="{status_class}">{link['Status']}</span> |
                <strong>Created:</strong> {link['Creation Date']}
            </div>
            {tags_html}
        </div>
"""
            
            html_content += "    </div>"
        
        html_content += """
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _export_json(self, links: List[Dict[str, str]], output_path: Path) -> None:
        """Export links as JSON."""
        export_data = {
            'export_date': datetime.now().isoformat(),
            'total_links': len(links),
            'categories': self.categories,
            'links': links
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    def _export_markdown(self, links: List[Dict[str, str]], output_path: Path) -> None:
        """Export links as Markdown."""
        content = f"""# GCAP3226 Forum Links Directory

**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}  
**Total Links:** {len(links)}

---

"""
        
        # Group by category
        by_category = {}
        for link in links:
            category = link['Category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(link)
        
        for category, category_links in sorted(by_category.items()):
            category_info = self.categories.get('categories', {}).get(category, {})
            icon = category_info.get('icon', '📎')
            
            content += f"""## {icon} {category.title()} ({len(category_links)} links)

"""
            
            for link in category_links:
                status_emoji = "🟢" if link['Status'] == 'active' else "🟡" if link['Status'] == 'planned' else "⚪"
                
                content += f"""### {status_emoji} {link['Topic']}

- **Week:** {link['Week']}
- **Type:** {link['Forum Type']}
- **Status:** {link['Status']}
- **Description:** {link['Description']}
- **URL:** [{link['Moodle URL']}]({link['Moodle URL']})
- **Created:** {link['Creation Date']}
"""
                
                if link['Tags']:
                    tags = link['Tags'].split(';')
                    content += f"- **Tags:** {', '.join([f'`{tag.strip()}`' for tag in tags])}"
                
                content += "\\n\\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    parser = argparse.ArgumentParser(description='Manage Moodle forum links database')
    
    # Add/update operations
    parser.add_argument('--add', action='store_true', help='Add a new link')
    parser.add_argument('--topic', help='Forum topic/title')
    parser.add_argument('--url', help='Moodle forum URL')
    parser.add_argument('--category', help='Link category')
    parser.add_argument('--description', default='', help='Link description')
    parser.add_argument('--forum-type', default='discussion', help='Forum type')
    parser.add_argument('--week', default='TBD', help='Week number')
    parser.add_argument('--status', default='active', help='Link status')
    parser.add_argument('--tags', default='', help='Comma-separated tags')
    
    # Search and list operations
    parser.add_argument('--list', action='store_true', help='List all links')
    parser.add_argument('--search', help='Search links by text')
    parser.add_argument('--filter-category', help='Filter by category')
    parser.add_argument('--filter-status', help='Filter by status')
    parser.add_argument('--filter-week', help='Filter by week')
    parser.add_argument('--filter-type', help='Filter by forum type')
    
    # Management operations
    parser.add_argument('--validate-links', action='store_true', help='Validate all links')
    parser.add_argument('--export', action='store_true', help='Export links')
    parser.add_argument('--format', default='html', choices=['html', 'json', 'markdown'], help='Export format')
    parser.add_argument('--output', help='Output filename')
    parser.add_argument('--open', action='store_true', help='Open exported file')
    
    # System options
    parser.add_argument('--base-dir', help='Base directory for moodle_management system')
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = MoodleLinkManager(args.base_dir)
    
    # Handle add operation
    if args.add:
        if not all([args.topic, args.url, args.category]):
            print("❌ Missing required fields: --topic, --url, --category")
            sys.exit(1)
        
        success = manager.add_link(
            topic=args.topic,
            url=args.url,
            category=args.category,
            description=args.description,
            forum_type=args.forum_type,
            week=args.week,
            status=args.status,
            tags=args.tags
        )
        
        if not success:
            sys.exit(1)
        return
    
    # Handle list operation
    if args.list or args.search or any([args.filter_category, args.filter_status, args.filter_week, args.filter_type]):
        filters = {}
        if args.search:
            filters['query'] = args.search
        if args.filter_category:
            filters['category'] = args.filter_category
        if args.filter_status:
            filters['status'] = args.filter_status
        if args.filter_week:
            filters['week'] = args.filter_week
        if args.filter_type:
            filters['forum_type'] = args.filter_type
        
        manager.list_links(filters)
        return
    
    # Handle validate operation
    if args.validate_links:
        manager.validate_links()
        return
    
    # Handle export operation
    if args.export:
        output_path = manager.export_links(args.format, args.output)
        
        if args.open:
            webbrowser.open(f"file://{Path(output_path).absolute()}")
        
        return
    
    # Default: show help
    parser.print_help()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Hashtag and Wiki-Link Finder for Obsidian Notes
Get a complete list of all hashtags and wiki-links with the notes that contain them
Created: September 6, 2025
"""

import re
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Union, Any

class HashtagAndLinkFinder:
    """Find all hashtags and wiki-links across your Obsidian notes"""
    
    def __init__(self):
        self.vscode_notes = Path(__file__).parent.parent.parent / "obsidian_notes"
        self.obsidian_vault = Path("/Users/simonwang/Documents/Usage/ObSync/Vault4sync")
        
    def extract_hashtags_from_file(self, file_path: Path) -> Set[str]:
        """Extract all hashtags from a single file"""
        if not file_path.exists():
            return set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return set()
        
        # Find hashtags (but not markdown headers)
        # Look for # followed by alphanumeric, underscore, or hyphen
        hashtag_pattern = r'(?:^|\s)#([a-zA-Z0-9_-]+)'
        hashtags = re.findall(hashtag_pattern, content)
        
        # Filter out common markdown patterns and numbers-only tags
        filtered_hashtags = []
        for tag in hashtags:
            # Skip if it's all numbers (likely not a real tag)
            if tag.isdigit():
                continue
            # Skip common CSS color codes
            if len(tag) == 6 and all(c in '0123456789abcdefABCDEF' for c in tag):
                continue
            # Skip single characters
            if len(tag) < 2:
                continue
            filtered_hashtags.append(tag)
        
        return set(filtered_hashtags)
    
    def extract_wikilinks_from_file(self, file_path: Path) -> Set[str]:
        """Extract all [[wiki-links]] from a single file"""
        if not file_path.exists():
            return set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return set()
        
        # Find all [[wiki-links]]
        wikilink_pattern = r'\[\[([^\]]+)\]\]'
        links = re.findall(wikilink_pattern, content)
        
        # Clean up links (remove alias parts if present)
        clean_links = []
        for link in links:
            # If there's a pipe |, take only the part before it
            if '|' in link:
                link = link.split('|')[0].strip()
            clean_links.append(link)
        
        return set(clean_links)
    
    def scan_all_notes(self, location: str = "vscode") -> Dict[str, Any]:
        """Scan all notes and return hashtags and wiki-links with their files"""
        
        # Choose location
        if location == "vscode":
            notes_path = self.vscode_notes
            location_name = "VS Code workspace"
        else:
            notes_path = self.obsidian_vault
            location_name = "Obsidian vault"
        
        if not notes_path.exists():
            print(f"❌ {location_name} not found: {notes_path}")
            return {}
        
        # Dictionaries to store results
        hashtag_to_files = defaultdict(set)
        wikilink_to_files = defaultdict(set)
        
        # Scan all markdown files
        markdown_files = list(notes_path.glob("*.md"))
        
        print(f"📊 Scanning {len(markdown_files)} notes in {location_name}...")
        print(f"📁 Location: {notes_path}")
        print()
        
        for md_file in markdown_files:
            # Extract hashtags
            hashtags = self.extract_hashtags_from_file(md_file)
            for tag in hashtags:
                hashtag_to_files[tag].add(md_file.name)
            
            # Extract wiki-links
            wikilinks = self.extract_wikilinks_from_file(md_file)
            for link in wikilinks:
                wikilink_to_files[link].add(md_file.name)
        
        return {
            'hashtags': hashtag_to_files,
            'wikilinks': wikilink_to_files,
            'total_files': len(markdown_files),
            'location': location_name
        }
    
    def display_hashtags_report(self, results: Dict):
        """Display a formatted report of all hashtags"""
        
        if not results:
            return
        
        hashtags = results['hashtags']
        total_files = results['total_files']
        location = results['location']
        
        print("🏷️  **COMPLETE HASHTAGS REPORT**")
        print("=" * 50)
        print(f"📍 Source: {location}")
        print(f"📊 Total Notes Scanned: {total_files}")
        print(f"🏷️  Unique Hashtags Found: {len(hashtags)}")
        print()
        
        if not hashtags:
            print("❌ No hashtags found in your notes")
            return
        
        # Sort hashtags by number of files (most popular first)
        sorted_hashtags = sorted(hashtags.items(), key=lambda x: len(x[1]), reverse=True)
        
        for i, (hashtag, files) in enumerate(sorted_hashtags, 1):
            print(f"{i:2}. **#{hashtag}**")
            print(f"    📊 Used in {len(files)} note{'s' if len(files) != 1 else ''}")
            print(f"    📄 Files: {', '.join(sorted(files))}")
            print()
    
    def display_wikilinks_report(self, results: Dict):
        """Display a formatted report of all wiki-links"""
        
        if not results:
            return
        
        wikilinks = results['wikilinks']
        total_files = results['total_files']
        location = results['location']
        
        print("🔗 **COMPLETE WIKI-LINKS REPORT**")
        print("=" * 50)
        print(f"📍 Source: {location}")
        print(f"📊 Total Notes Scanned: {total_files}")
        print(f"🔗 Unique Wiki-Links Found: {len(wikilinks)}")
        print()
        
        if not wikilinks:
            print("❌ No wiki-links found in your notes")
            return
        
        # Sort wiki-links by number of files (most referenced first)
        sorted_wikilinks = sorted(wikilinks.items(), key=lambda x: len(x[1]), reverse=True)
        
        for i, (wikilink, files) in enumerate(sorted_wikilinks, 1):
            print(f"{i:2}. **[[{wikilink}]]**")
            print(f"    📊 Referenced in {len(files)} note{'s' if len(files) != 1 else ''}")
            print(f"    📄 Files: {', '.join(sorted(files))}")
            print()
    
    def search_by_hashtag(self, hashtag: str, results: Dict) -> List[str]:
        """Find all notes containing a specific hashtag"""
        hashtags = results.get('hashtags', {})
        
        # Remove # if user included it
        clean_hashtag = hashtag.lstrip('#')
        
        if clean_hashtag in hashtags:
            return list(hashtags[clean_hashtag])
        else:
            return []
    
    def search_by_wikilink(self, wikilink: str, results: Dict) -> List[str]:
        """Find all notes containing a specific wiki-link"""
        wikilinks = results.get('wikilinks', {})
        
        # Remove [[ ]] if user included them
        clean_link = wikilink.strip('[]')
        
        if clean_link in wikilinks:
            return list(wikilinks[clean_link])
        else:
            return []
    
    def generate_cross_reference_report(self, results: Dict):
        """Show which hashtags and wiki-links appear together"""
        print("🔄 **CROSS-REFERENCE ANALYSIS**")
        print("=" * 40)
        
        hashtags = results.get('hashtags', {})
        wikilinks = results.get('wikilinks', {})
        
        # Find files that have both hashtags and wiki-links
        files_with_both = set()
        for files_set in hashtags.values():
            files_with_both.update(files_set)
        for files_set in wikilinks.values():
            if files_set & files_with_both:  # intersection
                files_with_both &= files_set
        
        print(f"📊 Notes with both hashtags AND wiki-links: {len(files_with_both)}")
        
        # Show most connected notes
        file_connection_count = defaultdict(int)
        for hashtag, files in hashtags.items():
            for file in files:
                file_connection_count[file] += 1
        for wikilink, files in wikilinks.items():
            for file in files:
                file_connection_count[file] += 1
        
        if file_connection_count:
            print(f"\n🔗 **Most Connected Notes:**")
            sorted_files = sorted(file_connection_count.items(), key=lambda x: x[1], reverse=True)
            for file, count in sorted_files[:5]:
                print(f"   📄 {file}: {count} connections")

def main():
    """Interactive hashtag and wiki-link finder"""
    print("🏷️  **HASHTAG & WIKI-LINK FINDER**")
    print("🎯 Get complete lists of all hashtags and wiki-links in your notes")
    print("=" * 60)
    
    finder = HashtagAndLinkFinder()
    
    print("📊 **CHOOSE SEARCH LOCATION:**")
    print("1. VS Code workspace (7 synced files)")
    print("2. Full Obsidian vault (all files)")
    print("3. Both locations")
    
    choice = input("\n🔢 Choose option (1-3): ").strip()
    
    if choice == "1":
        locations = ["vscode"]
    elif choice == "2":
        locations = ["obsidian"]
    elif choice == "3":
        locations = ["vscode", "obsidian"]
    else:
        print("Invalid choice, searching full Obsidian vault...")
        locations = ["obsidian"]
    
    for location in locations:
        print(f"\n{'='*60}")
        
        # Scan notes
        results = finder.scan_all_notes(location)
        
        if not results:
            if location == "vscode":
                print("❌ No synced notes found. Run the sync first:")
                print("   cd paperTrail/integrations && python vscode_obsidian_bridge.py")
            else:
                print("❌ Obsidian vault not found or empty")
            continue
    
        # Show hashtags report
        finder.display_hashtags_report(results)
        
        print("\n" + "="*60)
        
        # Show wiki-links report
        finder.display_wikilinks_report(results)
        
        print("\n" + "="*60)
        
        # Show cross-reference analysis
        finder.generate_cross_reference_report(results)
    
    print("\n" + "="*60)
    print("🎯 **INTERACTIVE SEARCH**")
    print("=" * 25)
    print("You can now search for specific hashtags or wiki-links!")
    print()
    print("Examples:")
    print("- Search hashtag: deadline")  
    print("- Search wiki-link: Moodle API")
    print("- Type 'quit' to exit")
    print()
    
    # Use the last results for interactive search
    if 'results' in locals():
        while True:
            query = input("🔍 Search for hashtag or wiki-link (or 'quit'): ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            if not query:
                continue
            
            # Try as hashtag first
            if query.startswith('#') or not query.startswith('[['):
                hashtag_results = finder.search_by_hashtag(query, results)
                if hashtag_results:
                    print(f"🏷️  **#{query.lstrip('#')}** found in:")
                    for file in sorted(hashtag_results):
                        print(f"   📄 {file}")
                    print()
                    continue
            
            # Try as wiki-link
            wikilink_results = finder.search_by_wikilink(query, results)
            if wikilink_results:
                print(f"🔗 **[[{query.strip('[]')}]]** found in:")
                for file in sorted(wikilink_results):
                    print(f"   📄 {file}")
                print()
                continue
            
            print(f"❌ '{query}' not found as hashtag or wiki-link")
            print()

if __name__ == "__main__":
    main()

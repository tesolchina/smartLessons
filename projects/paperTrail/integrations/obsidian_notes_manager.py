#!/usr/bin/env python3
"""
Obsidian Notes Manager - Handle your notes programmatically
Shows exactly how to access and manipulate Obsidian notes from VS Code
Created: September 6, 2025
"""

import re
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set

class ObsidianNotesManager:
    """Programmatically handle Obsidian notes in VS Code"""
    
    def __init__(self):
        self.obsidian_vault = Path("/Users/simonwang/Documents/Usage/ObSync/Vault4sync")
        self.vscode_notes = Path(__file__).parent.parent.parent / "obsidian_notes"
        self.workspace_root = Path(__file__).parent.parent.parent
        
    def list_available_notes(self):
        """Show all Obsidian notes accessible in VS Code"""
        print("📋 **OBSIDIAN NOTES AVAILABLE IN VS CODE:**")
        print("=" * 50)
        
        if self.vscode_notes.exists():
            notes = list(self.vscode_notes.glob("*.md"))
            print(f"🗂️  Location: {self.vscode_notes}")
            print(f"📊 Total Notes: {len(notes)}")
            print()
            
            for i, note in enumerate(notes, 1):
                size = note.stat().st_size
                modified = datetime.fromtimestamp(note.stat().st_mtime)
                print(f"{i}. **{note.name}**")
                print(f"   📏 Size: {size:,} bytes")
                print(f"   🕐 Modified: {modified.strftime('%Y-%m-%d %H:%M')}")
                print()
                
        return notes if self.vscode_notes.exists() else []
    
    def extract_wikilinks(self, note_path: Path) -> List[str]:
        """Extract [[wiki-style links]] from a note"""
        if not note_path.exists():
            return []
        
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all [[wiki-links]]
        wiki_pattern = r'\[\[([^\]]+)\]\]'
        links = re.findall(wiki_pattern, content)
        
        return list(set(links))  # Remove duplicates
    
    def extract_tags(self, note_path: Path) -> List[str]:
        """Extract #tags from a note"""
        if not note_path.exists():
            return []
        
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all #tags (but not markdown headers)
        tag_pattern = r'(?:^|\s)#([a-zA-Z0-9_-]+)'
        tags = re.findall(tag_pattern, content)
        
        return list(set(tags))
    
    def extract_urls(self, note_path: Path) -> List[str]:
        """Extract URLs from a note"""
        if not note_path.exists():
            return []
        
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find URLs
        url_pattern = r'https?://[^\s\)]+'
        urls = re.findall(url_pattern, content)
        
        return urls
    
    def analyze_note_connections(self):
        """Show how your notes are connected"""
        print("🔗 **NOTE CONNECTIONS ANALYSIS:**")
        print("=" * 40)
        
        notes = list(self.vscode_notes.glob("*.md")) if self.vscode_notes.exists() else []
        
        for note in notes:
            print(f"\n📝 **{note.name}**")
            
            # Extract connections
            wiki_links = self.extract_wikilinks(note)
            tags = self.extract_tags(note)
            urls = self.extract_urls(note)
            
            if wiki_links:
                print(f"   🔗 Links to: {', '.join(wiki_links[:3])}{'...' if len(wiki_links) > 3 else ''}")
            
            if tags:
                print(f"   🏷️  Tags: {', '.join(tags[:5])}{'...' if len(tags) > 5 else ''}")
            
            if urls:
                print(f"   🌐 URLs: {len(urls)} found")
    
    def search_notes_content(self, query: str) -> Dict[str, List[str]]:
        """Search for text across all notes"""
        print(f"🔍 **SEARCHING FOR: '{query}'**")
        print("=" * 40)
        
        results = {}
        notes = list(self.vscode_notes.glob("*.md")) if self.vscode_notes.exists() else []
        
        for note in notes:
            with open(note, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find lines containing the query
            lines = content.split('\n')
            matching_lines = [line.strip() for line in lines if query.lower() in line.lower()]
            
            if matching_lines:
                results[note.name] = matching_lines
                print(f"\n📄 **{note.name}**")
                for line in matching_lines[:3]:  # Show first 3 matches
                    print(f"   💡 {line}")
                if len(matching_lines) > 3:
                    print(f"   ... and {len(matching_lines) - 3} more matches")
        
        if not results:
            print("❌ No matches found")
        
        return results
    
    def create_knowledge_graph(self):
        """Generate a simple knowledge graph of your notes"""
        print("🕸️  **KNOWLEDGE GRAPH:**")
        print("=" * 30)
        
        notes = list(self.vscode_notes.glob("*.md")) if self.vscode_notes.exists() else []
        all_tags = set()
        all_links = set()
        
        for note in notes:
            tags = self.extract_tags(note)
            links = self.extract_wikilinks(note)
            all_tags.update(tags)
            all_links.update(links)
        
        print(f"📊 **Statistics:**")
        print(f"   📝 Notes: {len(notes)}")
        print(f"   🏷️  Unique Tags: {len(all_tags)}")
        print(f"   🔗 Unique Links: {len(all_links)}")
        
        if all_tags:
            print(f"\n🏷️  **Most Common Tags:**")
            for tag in list(all_tags)[:5]:
                print(f"   #{tag}")
        
        if all_links:
            print(f"\n🔗 **Wiki Links Found:**")
            for link in list(all_links)[:5]:
                print(f"   [[{link}]]")
    
    def auto_organize_notes(self):
        """Automatically organize notes by type/content"""
        print("🗂️  **AUTO-ORGANIZING NOTES:**")
        print("=" * 35)
        
        notes = list(self.vscode_notes.glob("*.md")) if self.vscode_notes.exists() else []
        categories = {
            'Daily Notes': [],
            'Project Notes': [],
            'Reference Notes': [],
            'API/Technical': [],
            'Other': []
        }
        
        for note in notes:
            name = note.name.lower()
            content = note.read_text(encoding='utf-8')[:500]  # First 500 chars
            
            if any(date_pattern in name for date_pattern in ['2025-', '2024-', 'daily']):
                categories['Daily Notes'].append(note.name)
            elif any(keyword in content.lower() for keyword in ['api', 'key', 'endpoint', 'github']):
                categories['API/Technical'].append(note.name)
            elif any(keyword in content.lower() for keyword in ['project', 'todo', 'task']):
                categories['Project Notes'].append(note.name)
            elif any(keyword in content.lower() for keyword in ['reference', 'note', 'info']):
                categories['Reference Notes'].append(note.name)
            else:
                categories['Other'].append(note.name)
        
        for category, notes_list in categories.items():
            if notes_list:
                print(f"\n📁 **{category}** ({len(notes_list)} notes)")
                for note in notes_list:
                    print(f"   📄 {note}")

def demonstrate_productivity_benefits():
    """Show concrete examples of how this improves productivity"""
    print("\n" + "="*60)
    print("🚀 **PRODUCTIVITY BENEFITS DEMONSTRATION**")
    print("="*60)
    
    print("""
💡 **HERE'S HOW THIS IMPROVES YOUR PRODUCTIVITY:**

1. 🔍 **INSTANT SEARCH ACROSS ALL NOTES:**
   Instead of: Opening Obsidian → Manual search → Switch between notes
   Now: Run script → Search all notes → Get exact matches with context

2. 🔗 **AUTOMATIC CONNECTION DISCOVERY:**
   Instead of: Manually tracking what links to what
   Now: Script shows all connections, tags, and relationships

3. 📊 **BULK NOTE ANALYSIS:**
   Instead of: Opening each note individually
   Now: Analyze all notes at once - find patterns, common themes

4. 🤖 **AUTOMATED ORGANIZATION:**
   Instead of: Manual note sorting and tagging
   Now: Script automatically categorizes by content type

5. 🛠️  **PROGRAMMABLE NOTE OPERATIONS:**
   - Extract all API keys and URLs
   - Find all TODO items across notes  
   - Generate project summaries
   - Auto-tag notes based on content
   - Create daily summaries from multiple sources

6. ⚡ **INTEGRATION WITH YOUR WORKFLOW:**
   - Paper Trail activities → Auto-update relevant project notes
   - Code changes → Update technical documentation notes
   - Email discussions → Add to meeting notes
   - Task completion → Update project status notes

**EXAMPLE USE CASES:**
- "Find all notes mentioning 'chatbot' with API keys"
- "Show me all project TODOs across my knowledge base"
- "What notes are connected to my current project?"
- "Auto-update project status in Obsidian from code commits"
""")

def main():
    """Interactive demonstration"""
    print("🧠 **OBSIDIAN NOTES MANAGER - LIVE DEMONSTRATION**")
    print("🎯 Showing you EXACTLY how to handle your notes programmatically")
    print("\n")
    
    manager = ObsidianNotesManager()
    
    # Show what's available
    available_notes = manager.list_available_notes()
    
    if not available_notes:
        print("❌ No synced notes found. Run the bridge first:")
        print("   cd paperTrail/integrations && python vscode_obsidian_bridge.py")
        return
    
    print("\n" + "="*50)
    print("🔍 **WHAT YOU CAN DO WITH THESE NOTES:**")
    print("="*50)
    
    # Demonstrate capabilities
    print("\n1️⃣ **ANALYZE CONNECTIONS:**")
    manager.analyze_note_connections()
    
    print("\n2️⃣ **SEARCH CONTENT:**")
    manager.search_notes_content("api")
    
    print("\n3️⃣ **KNOWLEDGE GRAPH:**")
    manager.create_knowledge_graph()
    
    print("\n4️⃣ **AUTO-ORGANIZE:**")
    manager.auto_organize_notes()
    
    # Show productivity benefits
    demonstrate_productivity_benefits()
    
    print("\n" + "="*60)
    print("✅ **NEXT STEPS TO USE THIS:**")
    print("="*60)
    print("""
1. 📝 **Edit this script** to add your specific use cases
2. 🔄 **Run it daily** to analyze your growing knowledge base  
3. 🤖 **Automate workflows** like:
   - Extract action items from meeting notes
   - Update project status from daily notes
   - Find related notes when starting new work
   - Generate weekly summaries from daily entries

4. 🔗 **Integrate with your tools:**
   - Auto-update GitHub issues from note TODOs
   - Send email summaries from note analysis
   - Create Paper Trail entries from note insights
""")

if __name__ == "__main__":
    main()

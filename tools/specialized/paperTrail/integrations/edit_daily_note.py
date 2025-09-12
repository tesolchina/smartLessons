#!/usr/bin/env python3
"""
Obsidian Daily Note Editor
Connect to existing Obsidian vault and edit today's note
Created: September 6, 2025
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

class ObsidianDailyNoteEditor:
    """Edit daily notes in an existing Obsidian vault"""
    
    def __init__(self, vault_path: Optional[str] = None):
        self.vault_path = Path(vault_path) if vault_path else None
        self.paper_trail_path = Path(__file__).parent.parent
        self.master_trail = self.paper_trail_path / "MASTER_ACTIVITY_TRAIL.md"
        
    def set_vault_path(self, vault_path: str):
        """Set the path to the Obsidian vault"""
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")
        if not (self.vault_path / ".obsidian").exists():
            raise ValueError(f"Not a valid Obsidian vault (missing .obsidian folder): {vault_path}")
    
    def get_daily_note_path(self, date: Optional[datetime] = None):
        """Get the path to today's daily note"""
        if not self.vault_path:
            raise ValueError("Vault path not set. Use set_vault_path() first.")
            
        if date is None:
            date = datetime.now()
        
        # Common daily note formats
        possible_formats = [
            date.strftime("%Y-%m-%d"),     # 2025-09-06
            date.strftime("%Y%m%d"),       # 20250906
            date.strftime("%m-%d-%Y"),     # 09-06-2025
            date.strftime("%d-%m-%Y"),     # 06-09-2025
            date.strftime("%Y.%m.%d"),     # 2025.09.06
            date.strftime("%B %d, %Y"),    # September 6, 2025
        ]
        
        # Check different possible locations
        possible_locations = [
            self.vault_path,                           # Root
            self.vault_path / "Daily Notes",           # Daily Notes folder
            self.vault_path / "daily",                 # daily folder
            self.vault_path / "Journal",               # Journal folder
            self.vault_path / "Days",                  # Days folder
        ]
        
        for location in possible_locations:
            if not location.exists():
                continue
                
            for format_str in possible_formats:
                note_path = location / f"{format_str}.md"
                if note_path.exists():
                    return note_path
        
        # If no existing note found, create in most common location
        daily_notes_dir = self.vault_path / "Daily Notes"
        if not daily_notes_dir.exists():
            daily_notes_dir.mkdir(exist_ok=True)
        
        return daily_notes_dir / f"{date.strftime('%Y-%m-%d')}.md"
    
    def get_paper_trail_summary(self):
        """Get today's activities from the paper trail"""
        if not self.master_trail.exists():
            return "No paper trail activities found."
        
        today = datetime.now().strftime("%B %d, %Y")
        
        with open(self.master_trail, 'r') as f:
            content = f.read()
        
        # Find today's section
        today_section = f"### **{today}**"
        if today_section in content:
            lines = content.split('\n')
            start_idx = None
            end_idx = None
            
            for i, line in enumerate(lines):
                if today_section in line:
                    start_idx = i
                elif start_idx is not None and line.startswith('### **') and i > start_idx:
                    end_idx = i
                    break
            
            if start_idx is not None:
                if end_idx is None:
                    end_idx = len(lines)
                
                today_content = '\n'.join(lines[start_idx:end_idx]).strip()
                return today_content
        
        return "No activities logged for today yet."
    
    def create_daily_note_template(self, date: Optional[datetime] = None):
        """Create a daily note template with paper trail integration"""
        if date is None:
            date = datetime.now()
        
        formatted_date = date.strftime("%Y-%m-%d")
        display_date = date.strftime("%B %d, %Y")
        
        template = f"""# {display_date}

## 🎯 Today's Focus
- [ ] Primary goal for today
- [ ] Secondary priority  
- [ ] Quick wins to complete

## 📊 Activities & Progress
{self.get_paper_trail_summary()}

## 💭 Notes & Thoughts
- 

## 🧠 Decisions Made
- 

## 📚 Learning & Insights
- 

## 🔗 Connections & Ideas
- 

## 🎯 Tomorrow's Preparation
- [ ] Priority 1:
- [ ] Priority 2: 
- [ ] Prep needed:

---

## 📋 Tags
#{formatted_date} #daily-note #productivity #paper-trail

## 🔄 Paper Trail Integration
*This note is automatically synced with the Daily Assistant Paper Trail system*
- Paper Trail Path: `paperTrail/MASTER_ACTIVITY_TRAIL.md`
- Last Updated: {datetime.now().strftime("%H:%M")}
"""
        return template
    
    def update_daily_note(self, additional_content: str = "", date: Optional[datetime] = None):
        """Update or create today's daily note"""
        note_path = self.get_daily_note_path(date)
        
        if note_path.exists():
            # Read existing note
            with open(note_path, 'r') as f:
                existing_content = f.read()
            
            # Check if paper trail section exists and update it
            paper_trail_summary = self.get_paper_trail_summary()
            
            if "## 📊 Activities & Progress" in existing_content:
                # Update the activities section
                lines = existing_content.split('\n')
                new_lines = []
                in_activities_section = False
                
                for line in lines:
                    if line.startswith("## 📊 Activities & Progress"):
                        new_lines.append(line)
                        new_lines.append(paper_trail_summary)
                        in_activities_section = True
                    elif in_activities_section and line.startswith("## "):
                        # End of activities section
                        in_activities_section = False
                        new_lines.append(line)
                    elif not in_activities_section:
                        new_lines.append(line)
                
                updated_content = '\n'.join(new_lines)
            else:
                # Append paper trail summary
                updated_content = existing_content + f"\n\n## 📊 Activities & Progress (Updated {datetime.now().strftime('%H:%M')})\n{paper_trail_summary}"
            
            # Add any additional content
            if additional_content:
                updated_content += f"\n\n## ✏️ Manual Update ({datetime.now().strftime('%H:%M')})\n{additional_content}"
            
        else:
            # Create new note from template
            updated_content = self.create_daily_note_template(date)
            if additional_content:
                updated_content += f"\n\n## ✏️ Manual Update ({datetime.now().strftime('%H:%M')})\n{additional_content}"
        
        # Write the note
        with open(note_path, 'w') as f:
            f.write(updated_content)
        
        return note_path
    
    def sync_with_paper_trail(self):
        """Sync today's note with current paper trail activities"""
        try:
            note_path = self.update_daily_note()
            print(f"✅ Successfully updated daily note: {note_path}")
            return note_path
        except Exception as e:
            print(f"❌ Error syncing with paper trail: {e}")
            return None

def main():
    """Interactive daily note editor"""
    print("🗓️ Obsidian Daily Note Editor")
    print("=" * 40)
    
    # Set vault path
    vault_path = input("📁 Enter your Obsidian vault path: ").strip()
    if not vault_path:
        vault_path = "/Users/simonwang/Documents/Usage/ObSync/Vault4sync"
        print(f"🔧 Using default vault: {vault_path}")
    
    try:
        editor = ObsidianDailyNoteEditor()
        editor.set_vault_path(vault_path)
        
        # Get today's note path
        today_note_path = editor.get_daily_note_path()
        print(f"📝 Today's note location: {today_note_path}")
        
        # Check if note exists
        if today_note_path.exists():
            print("✅ Today's note already exists")
            with open(today_note_path, 'r') as f:
                current_content = f.read()
            print(f"📄 Current note length: {len(current_content)} characters")
        else:
            print("📝 Today's note will be created")
        
        # Options
        print("\n🎯 What would you like to do?")
        print("1. Sync with Paper Trail (update activities)")
        print("2. Add custom content to today's note")  
        print("3. View current note content")
        print("4. Create/overwrite with template")
        
        choice = input("\n🔢 Enter your choice (1-4): ").strip()
        
        if choice == "1":
            # Sync with paper trail
            result_path = editor.sync_with_paper_trail()
            if result_path:
                print(f"🎉 Daily note updated successfully!")
                print(f"📂 Open in Obsidian: {result_path}")
                
        elif choice == "2":
            # Add custom content
            print("\n📝 Enter content to add to today's note:")
            print("(Type 'END' on a new line when finished)")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            
            custom_content = '\n'.join(lines)
            result_path = editor.update_daily_note(custom_content)
            print(f"✅ Added content to daily note: {result_path}")
            
        elif choice == "3":
            # View current content
            if today_note_path.exists():
                with open(today_note_path, 'r') as f:
                    content = f.read()
                print(f"\n📖 Current note content:")
                print("=" * 50)
                print(content)
                print("=" * 50)
            else:
                print("📝 No note exists for today yet.")
                
        elif choice == "4":
            # Create from template
            result_path = editor.update_daily_note()
            print(f"📄 Created daily note from template: {result_path}")
            
        else:
            print("❌ Invalid choice")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("- Check that the vault path is correct")
        print("- Ensure the vault contains a .obsidian folder")
        print("- Verify you have read/write permissions")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Direct Obsidian Daily Note Editor for Vault4sync
Edit today's note with Paper Trail integration
Created: September 6, 2025
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# Direct vault path
VAULT_PATH = "/Users/simonwang/Documents/Usage/ObSync/Vault4sync"

class DirectObsidianEditor:
    """Direct editor for the specific Obsidian vault"""
    
    def __init__(self):
        self.vault_path = Path(VAULT_PATH)
        self.paper_trail_path = Path(__file__).parent.parent
        self.master_trail = self.paper_trail_path / "MASTER_ACTIVITY_TRAIL.md"
        
        # Validate vault
        if not self.vault_path.exists():
            raise ValueError(f"Vault does not exist: {VAULT_PATH}")
        if not (self.vault_path / ".obsidian").exists():
            print(f"⚠️  Warning: No .obsidian folder found. May not be a proper Obsidian vault.")
    
    def find_todays_note(self):
        """Find today's note in the vault"""
        today = datetime.now()
        
        # Common date formats and locations
        date_formats = [
            today.strftime("%Y-%m-%d"),     # 2025-09-06
            today.strftime("%Y%m%d"),       # 20250906
            today.strftime("%m-%d-%Y"),     # 09-06-2025
            today.strftime("%d-%m-%Y"),     # 06-09-2025
            today.strftime("%Y.%m.%d"),     # 2025.09.06
            today.strftime("%B %d, %Y"),    # September 6, 2025
            today.strftime("%d %B %Y"),     # 6 September 2025
        ]
        
        search_locations = [
            self.vault_path,
            self.vault_path / "Daily Notes",
            self.vault_path / "daily",
            self.vault_path / "Journal",
            self.vault_path / "Days",
            self.vault_path / "notes",
        ]
        
        print(f"🔍 Searching for today's note ({today.strftime('%Y-%m-%d')})...")
        
        # Search for existing notes
        found_notes = []
        for location in search_locations:
            if not location.exists():
                continue
                
            print(f"   📂 Checking: {location}")
            
            for date_format in date_formats:
                note_path = location / f"{date_format}.md"
                if note_path.exists():
                    found_notes.append(note_path)
                    print(f"   ✅ Found: {note_path}")
        
        # Also search for any file modified today
        print(f"   🔍 Searching for files modified today...")
        today_files = []
        try:
            for root, dirs, files in os.walk(self.vault_path):
                for file in files:
                    if file.endswith('.md'):
                        file_path = Path(root) / file
                        mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if mod_time.date() == today.date():
                            today_files.append(file_path)
                            print(f"   📝 Modified today: {file_path}")
        except Exception as e:
            print(f"   ⚠️  Error searching files: {e}")
        
        return found_notes, today_files
    
    def get_paper_trail_activities(self):
        """Get today's activities from paper trail"""
        if not self.master_trail.exists():
            return "📊 No paper trail activities found."
        
        today = datetime.now().strftime("%B %d, %Y")
        
        try:
            with open(self.master_trail, 'r') as f:
                content = f.read()
            
            if f"### **{today}**" in content:
                lines = content.split('\n')
                start_idx = None
                end_idx = None
                
                for i, line in enumerate(lines):
                    if f"### **{today}**" in line:
                        start_idx = i
                    elif start_idx is not None and line.startswith('### **') and i > start_idx:
                        end_idx = i
                        break
                
                if start_idx is not None:
                    if end_idx is None:
                        end_idx = len(lines)
                    
                    today_activities = '\n'.join(lines[start_idx:end_idx]).strip()
                    return today_activities
                    
            return f"📊 No activities logged for {today} yet."
            
        except Exception as e:
            return f"📊 Error reading paper trail: {e}"
    
    def create_todays_note_content(self):
        """Create content for today's note with paper trail integration"""
        today = datetime.now()
        date_str = today.strftime("%Y-%m-%d")
        display_date = today.strftime("%B %d, %Y")
        
        activities = self.get_paper_trail_activities()
        
        content = f"""# {display_date}

## 🎯 Today's Goals
- [ ] Primary focus:
- [ ] Secondary priority:
- [ ] Quick wins:

## 📊 Activities & Progress (Paper Trail Integration)
{activities}

## 💭 Notes & Reflections


## 🧠 Decisions Made


## 📚 Learning & Insights


## 🔗 Connections & Ideas


## 🎯 Tomorrow's Planning
- [ ] Priority 1:
- [ ] Priority 2:
- [ ] Preparation needed:

---

*Updated: {today.strftime("%H:%M")} | Paper Trail Sync: ✅*

#daily-note #{date_str} #paper-trail-sync
"""
        return content
    
    def edit_note(self, note_path: Path, append_content: Optional[str] = None):
        """Edit an existing note or create new one"""
        
        if note_path.exists():
            print(f"📝 Editing existing note: {note_path}")
            
            with open(note_path, 'r') as f:
                existing_content = f.read()
            
            # Update paper trail section if it exists
            activities = self.get_paper_trail_activities()
            
            if "## 📊 Activities & Progress" in existing_content:
                # Replace the paper trail section
                lines = existing_content.split('\n')
                new_lines = []
                skip_until_next_section = False
                
                for line in lines:
                    if line.startswith("## 📊 Activities & Progress"):
                        new_lines.append(line)
                        new_lines.append(activities)
                        skip_until_next_section = True
                    elif skip_until_next_section and line.startswith("## "):
                        # Found next section, stop skipping
                        skip_until_next_section = False
                        new_lines.append(line)
                    elif not skip_until_next_section:
                        new_lines.append(line)
                
                content = '\n'.join(new_lines)
            else:
                # Append paper trail section
                content = existing_content + f"\n\n## 📊 Paper Trail Update ({datetime.now().strftime('%H:%M')})\n{activities}"
            
            # Add any additional content
            if append_content:
                content += f"\n\n## ✏️ Manual Addition ({datetime.now().strftime('%H:%M')})\n{append_content}"
            
        else:
            print(f"📄 Creating new note: {note_path}")
            content = self.create_todays_note_content()
            
            if append_content:
                content += f"\n\n## ✏️ Additional Content\n{append_content}"
            
            # Create directory if needed
            note_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the content
        try:
            with open(note_path, 'w') as f:
                f.write(content)
            print(f"✅ Successfully wrote note: {note_path}")
            return True
        except Exception as e:
            print(f"❌ Error writing note: {e}")
            return False
    
def main():
    """Main function to edit today's note"""
    print("🗓️ Obsidian Daily Note Editor (Direct)")
    print(f"🎯 Vault: {VAULT_PATH}")
    print("=" * 50)
    
    try:
        editor = DirectObsidianEditor()
        
        # Find today's note
        found_notes, today_files = editor.find_todays_note()
        
        if found_notes:
            print(f"\n📋 Found {len(found_notes)} potential today's notes:")
            for i, note in enumerate(found_notes, 1):
                print(f"  {i}. {note}")
                
            # Use the first found note
            target_note = found_notes[0]
            print(f"\n✅ Using: {target_note}")
            
        elif today_files:
            print(f"\n📋 Found {len(today_files)} files modified today:")
            for i, file in enumerate(today_files, 1):
                print(f"  {i}. {file}")
            
            choice = input(f"\n🔢 Choose file to edit (1-{len(today_files)}) or 'n' for new: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(today_files):
                target_note = today_files[int(choice) - 1]
            else:
                # Create new note
                daily_notes_dir = editor.vault_path / "Daily Notes"
                target_note = daily_notes_dir / f"{datetime.now().strftime('%Y-%m-%d')}.md"
                print(f"📝 Will create new note: {target_note}")
        else:
            # Create new note
            daily_notes_dir = editor.vault_path / "Daily Notes"
            target_note = daily_notes_dir / f"{datetime.now().strftime('%Y-%m-%d')}.md"
            print(f"📝 No existing notes found. Creating new: {target_note}")
        
        # Options for editing
        print(f"\n🎯 What would you like to do with the note?")
        print("1. Update with Paper Trail activities")
        print("2. Add custom content")
        print("3. View current content")
        print("4. Full sync and update")
        
        choice = input("\n🔢 Choose option (1-4): ").strip()
        
        if choice == "1":
            # Update with paper trail
            success = editor.edit_note(target_note)
            if success:
                print(f"🎉 Note updated with Paper Trail activities!")
                
        elif choice == "2":
            # Add custom content
            print("\n📝 Enter content to add:")
            print("(Press Enter twice to finish)")
            lines = []
            empty_count = 0
            while empty_count < 2:
                line = input()
                if line.strip() == "":
                    empty_count += 1
                else:
                    empty_count = 0
                lines.append(line)
            
            custom_content = '\n'.join(lines[:-2])  # Remove the last two empty lines
            success = editor.edit_note(target_note, custom_content)
            if success:
                print(f"✅ Added custom content to note!")
                
        elif choice == "3":
            # View content
            if target_note.exists():
                with open(target_note, 'r') as f:
                    content = f.read()
                print(f"\n📖 Current content of {target_note}:")
                print("=" * 60)
                print(content)
                print("=" * 60)
            else:
                print("📝 Note doesn't exist yet.")
                
        elif choice == "4":
            # Full sync
            success = editor.edit_note(target_note)
            if success:
                print(f"🔄 Full sync completed!")
                
        else:
            print("❌ Invalid choice")
        
        print(f"\n📂 Note location: {target_note}")
        print(f"🔗 Open in Obsidian or your preferred editor")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
VS Code Obsidian Bridge - Create synced notes in VS Code workspace
Connects VS Code workspace to Obsidian vault with real-time sync
Created: September 6, 2025
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

class VSCodeObsidianBridge:
    """Create and sync notes between VS Code workspace and Obsidian vault"""
    
    def __init__(self):
        self.vault_path = Path("/Users/simonwang/Documents/Usage/ObSync/Vault4sync")
        self.workspace_path = Path(__file__).parent.parent.parent  # DailyAssistant root
        self.synced_notes_dir = self.workspace_path / "obsidian_notes" 
        self.paper_trail_path = self.workspace_path / "paperTrail"
        
        # Create synced notes directory
        self.synced_notes_dir.mkdir(exist_ok=True)
        
    def create_synced_note(self, note_name: str, content: Optional[str] = None):
        """Create a note that exists in both VS Code workspace and Obsidian vault"""
        
        # Clean note name
        clean_name = note_name.replace(" ", "-").lower()
        if not clean_name.endswith('.md'):
            clean_name += '.md'
        
        # Paths in both locations
        vscode_note_path = self.synced_notes_dir / clean_name
        obsidian_note_path = self.vault_path / clean_name
        
        # Create default content if none provided
        if content is None:
            content = self.create_default_note_content(note_name)
        
        # Write to VS Code workspace
        with open(vscode_note_path, 'w') as f:
            f.write(content)
        
        # Copy to Obsidian vault
        shutil.copy2(vscode_note_path, obsidian_note_path)
        
        print(f"✅ Created synced note:")
        print(f"   📁 VS Code: {vscode_note_path}")
        print(f"   🧠 Obsidian: {obsidian_note_path}")
        
        return vscode_note_path, obsidian_note_path
    
    def create_default_note_content(self, note_name: str):
        """Create default content for a new note with Paper Trail integration"""
        today = datetime.now().strftime("%B %d, %Y")
        timestamp = datetime.now().strftime("%H:%M")
        
        content = f"""# {note_name}

Created: {today} at {timestamp}  
Type: [[Knowledge Note]]  
Status: #active  

## 📝 Overview

Brief description of this note's purpose...

## 🔗 Connections

### Related Notes
- [[]]
- [[]]

### Related Projects
- [[Paper Trail System]]
- [[Daily Assistant]]

## 📊 Content

### Key Points
- 

### Details
- 

### Examples
- 

## 🧠 Insights & Learnings

### What I Discovered
- 

### Connections Made
- 

### Questions Raised
- 

## 🎯 Next Actions

- [ ] 
- [ ] 
- [ ] 

## 📚 References

- Paper Trail: `paperTrail/MASTER_ACTIVITY_TRAIL.md`
- Created from VS Code workspace
- Synced with Obsidian vault

---

*Last updated: {timestamp} | Sync: ✅*

#vscode-created #paper-trail-synced #knowledge-note
"""
        return content
    
    def sync_todays_note_to_workspace(self):
        """Copy today's note from Obsidian to VS Code workspace"""
        today = datetime.now()
        
        # Try different date formats
        possible_names = [
            f"{today.strftime('%Y-%m-%d')}.md",
            f"{today.strftime('%Y%m%d')}.md",
            f"{today.strftime('%B %d, %Y')}.md"
        ]
        
        for note_name in possible_names:
            obsidian_note = self.vault_path / note_name
            if obsidian_note.exists():
                # Copy to VS Code workspace
                vscode_note = self.synced_notes_dir / f"today_{note_name}"
                shutil.copy2(obsidian_note, vscode_note)
                
                # Add Paper Trail integration section
                self.add_paper_trail_integration(vscode_note)
                
                print(f"📋 Synced today's note to VS Code:")
                print(f"   🧠 From: {obsidian_note}")
                print(f"   📁 To: {vscode_note}")
                
                return vscode_note
        
        print("📝 No today's note found in Obsidian. Creating new one...")
        return self.create_todays_note()
    
    def create_todays_note(self):
        """Create today's note in both locations with Paper Trail integration"""
        today = datetime.now()
        note_name = f"Daily Note - {today.strftime('%Y-%m-%d')}"
        
        # Get Paper Trail activities
        activities = self.get_paper_trail_activities()
        
        content = f"""# {today.strftime('%B %d, %Y')}

## 🎯 Today's Focus
- [ ] Primary goal:
- [ ] Secondary priority:  
- [ ] Quick wins:

## 📊 Paper Trail Activities
{activities}

## 💭 Thoughts & Notes

### Key Insights
- 

### Decisions Made  
- 

### Challenges
- 

## 🔗 Connections & Ideas

### Links to Other Notes
- [[]]
- [[]]

### Project Connections
- [[Paper Trail System]]
- [[Daily Assistant]]

## 🎯 Tomorrow's Preparation
- [ ] 
- [ ] 
- [ ] 

---

## 📋 Metadata
Created: {today.strftime('%H:%M')}  
Source: VS Code → Obsidian Sync  
Paper Trail: ✅ Integrated  

#daily-note #paper-trail-sync #vscode-created #{today.strftime('%Y-%m-%d')}
"""
        
        return self.create_synced_note(note_name, content)
    
    def get_paper_trail_activities(self):
        """Get today's activities from Paper Trail"""
        trail_file = self.paper_trail_path / "MASTER_ACTIVITY_TRAIL.md"
        
        if not trail_file.exists():
            return "📊 No Paper Trail activities found."
        
        today = datetime.now().strftime("%B %d, %Y")
        
        try:
            with open(trail_file, 'r') as f:
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
            return f"📊 Error reading Paper Trail: {e}"
    
    def add_paper_trail_integration(self, note_path: Path):
        """Add Paper Trail integration section to an existing note"""
        
        if not note_path.exists():
            return
        
        # Read existing content
        with open(note_path, 'r') as f:
            content = f.read()
        
        # Check if integration already exists
        if "Paper Trail Activities" in content:
            return
        
        # Add integration section
        activities = self.get_paper_trail_activities()
        integration_section = f"""

## 📊 Paper Trail Integration (Added {datetime.now().strftime('%H:%M')})
{activities}

---
*Auto-synced from Paper Trail System*
"""
        
        content += integration_section
        
        # Write back
        with open(note_path, 'w') as f:
            f.write(content)
    
    def list_synced_notes(self):
        """List all synced notes in the workspace"""
        if not self.synced_notes_dir.exists():
            print("📁 No synced notes directory found.")
            return []
        
        notes = list(self.synced_notes_dir.glob("*.md"))
        
        if notes:
            print(f"📋 Found {len(notes)} synced notes:")
            for i, note in enumerate(notes, 1):
                print(f"  {i}. {note.name}")
        else:
            print("📝 No synced notes found.")
        
        return notes
    
    def sync_all_recent_notes(self):
        """Sync all notes modified in the last 24 hours from Obsidian to VS Code"""
        
        if not self.vault_path.exists():
            print(f"❌ Obsidian vault not found: {self.vault_path}")
            return
        
        # Find recent notes in Obsidian vault
        recent_notes = []
        cutoff_time = datetime.now().timestamp() - (24 * 60 * 60)  # 24 hours ago
        
        for note_path in self.vault_path.glob("*.md"):
            if note_path.stat().st_mtime > cutoff_time:
                recent_notes.append(note_path)
        
        if recent_notes:
            print(f"🔄 Syncing {len(recent_notes)} recent notes from Obsidian:")
            
            for note_path in recent_notes:
                vscode_note = self.synced_notes_dir / f"synced_{note_path.name}"
                shutil.copy2(note_path, vscode_note)
                self.add_paper_trail_integration(vscode_note)
                print(f"   ✅ {note_path.name}")
        else:
            print("📝 No recent notes found in Obsidian vault.")

def main():
    """Interactive VS Code Obsidian Bridge"""
    print("🔗 VS Code ↔ Obsidian Bridge")
    print("=" * 40)
    
    bridge = VSCodeObsidianBridge()
    
    print("🎯 What would you like to do?")
    print("1. Sync today's note to VS Code workspace")
    print("2. Create a new synced note")
    print("3. List synced notes in workspace")
    print("4. Sync all recent Obsidian notes")
    print("5. View sync status")
    
    choice = input("\n🔢 Choose option (1-5): ").strip()
    
    try:
        if choice == "1":
            note_path = bridge.sync_todays_note_to_workspace()
            print(f"\n📂 Open in VS Code: {note_path}")
            
        elif choice == "2":
            note_name = input("📝 Enter note name: ").strip()
            if note_name:
                vscode_path, obsidian_path = bridge.create_synced_note(note_name)
                print(f"\n📂 Open in VS Code: {vscode_path}")
                print(f"🧠 Available in Obsidian: {obsidian_path}")
            else:
                print("❌ Note name cannot be empty")
                
        elif choice == "3":
            notes = bridge.list_synced_notes()
            if notes:
                print(f"\n📁 Synced notes location: {bridge.synced_notes_dir}")
                
        elif choice == "4":
            bridge.sync_all_recent_notes()
            print(f"\n📁 All synced to: {bridge.synced_notes_dir}")
            
        elif choice == "5":
            print(f"\n📊 Sync Status:")
            print(f"   🧠 Obsidian Vault: {bridge.vault_path}")
            print(f"   📁 VS Code Workspace: {bridge.synced_notes_dir}")
            print(f"   📊 Paper Trail: {bridge.paper_trail_path}")
            print(f"   ✅ Bridge Active: {'Yes' if bridge.vault_path.exists() else 'No'}")
            
        else:
            print("❌ Invalid choice")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

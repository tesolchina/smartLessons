#!/usr/bin/env python3
"""
Paper Trail Update System
Automatically update the master activity trail with new activities
Created: September 6, 2025
"""

import os
import json
from datetime import datetime
from pathlib import Path

class PaperTrailUpdater:
    """Manage updates to the master activity paper trail"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent  # Go up to DailyAssistant
        self.paper_trail_path = self.base_path / "paperTrail"
        self.trail_file = self.paper_trail_path / "MASTER_ACTIVITY_TRAIL.md"
        self.project_notes = self.base_path / "projectNotes.md"
        self.daily_logs_path = self.paper_trail_path / "daily_logs"
        self.decisions_path = self.paper_trail_path / "decisions"
        
    def log_activity(self, activity_type: str, description: str, status: str = "✅", impact: str = ""):
        """Add a new activity to the trail"""
        timestamp = datetime.now().strftime("%H:%M")
        today = datetime.now().strftime("%B %d, %Y")
        
        # Read current trail
        if self.trail_file.exists():
            with open(self.trail_file, 'r') as f:
                content = f.read()
        else:
            content = ""
        
        # Create new activity entry
        activity_entry = f"| {timestamp} | {description} | {status} | {impact} |"
        
        # Find the activity log section for today
        today_section = f"### **{today}**"
        
        if today_section in content:
            # Add to existing day
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if today_section in line:
                    # Find the table and add new entry
                    j = i + 1
                    while j < len(lines) and not lines[j].startswith('|'):
                        j += 1
                    # Skip header and separator
                    if j < len(lines) and lines[j].startswith('| Time'):
                        j += 2  # Skip header and separator
                    lines.insert(j, activity_entry)
                    break
            
            content = '\n'.join(lines)
        else:
            # Create new day section
            new_section = f"""
{today_section}

| Time | Activity | Status | Impact |
|------|----------|---------|---------|
{activity_entry}

---
"""
            # Insert after the current session header
            content = content.replace(
                "## 📊 **ACTIVITY LOG**",
                f"## 📊 **ACTIVITY LOG**\n{new_section}"
            )
        
        # Write updated content
        with open(self.trail_file, 'w') as f:
            f.write(content)
            
        print(f"✅ Added activity: {description}")
    
    def update_session_summary(self, achievements: list):
        """Update the current session summary"""
        if not self.trail_file.exists():
            print("❌ Trail file not found")
            return
            
        with open(self.trail_file, 'r') as f:
            content = f.read()
        
        # Update achievements section
        achievement_text = "\n".join([f"- {achievement}" for achievement in achievements])
        
        # Find and replace the achievements section
        start_marker = "### 🎯 **Today's Achievements**"
        end_marker = "---"
        
        if start_marker in content:
            start_idx = content.find(start_marker)
            end_idx = content.find(end_marker, start_idx)
            if end_idx != -1:
                new_section = f"""{start_marker}

{achievement_text}

{end_marker}"""
                content = content[:start_idx] + new_section + content[end_idx + 3:]
        
        with open(self.trail_file, 'w') as f:
            f.write(content)
            
        print("✅ Updated session summary")
    
    def add_decision(self, decision_title: str, rationale: str, implementation: str, outcome: str):
        """Add a technical decision to the log"""
        timestamp = datetime.now().strftime("%B %d, %Y")
        
        decision_entry = f"""
#### **{decision_title}** - {timestamp}
- **Rationale**: {rationale}
- **Implementation**: {implementation}  
- **Outcome**: {outcome}
"""
        
        if self.trail_file.exists():
            with open(self.trail_file, 'r') as f:
                content = f.read()
            
            # Add to decision log section
            decision_marker = "### **Key Technical Decisions Made**"
            if decision_marker in content:
                content = content.replace(
                    decision_marker,
                    f"{decision_marker}\n{decision_entry}"
                )
                
                with open(self.trail_file, 'w') as f:
                    f.write(content)
                    
                print(f"✅ Added decision: {decision_title}")
    
    def generate_daily_summary(self):
        """Generate a summary of today's activities"""
        today = datetime.now().strftime("%B %d, %Y")
        
        if not self.trail_file.exists():
            print("❌ Trail file not found")
            return
            
        with open(self.trail_file, 'r') as f:
            content = f.read()
        
        # Extract today's activities
        today_section = f"### **{today}**"
        if today_section in content:
            lines = content.split('\n')
            activities = []
            capturing = False
            
            for line in lines:
                if today_section in line:
                    capturing = True
                    continue
                elif capturing and line.startswith('### **'):
                    break
                elif capturing and line.startswith('| ') and not line.startswith('| Time'):
                    activities.append(line.strip())
            
            print(f"\n📋 **DAILY SUMMARY - {today}**")
            print("="*50)
            for activity in activities:
                if activity and activity != '|------|----------|---------|---------|':
                    parts = [part.strip() for part in activity.split('|')[1:-1]]
                    if len(parts) >= 3:
                        print(f"{parts[0]} - {parts[1]} {parts[2]}")
            print("="*50)
        else:
            print(f"No activities found for {today}")

def main():
    """Interactive paper trail updater"""
    updater = PaperTrailUpdater()
    
    print("📝 PAPER TRAIL UPDATER")
    print("="*30)
    print("1. Log new activity")
    print("2. Add technical decision")
    print("3. Generate daily summary")
    print("4. Update session achievements")
    print("0. Exit")
    
    while True:
        choice = input("\nSelect option (0-4): ").strip()
        
        if choice == "0":
            print("👋 Paper trail updated!")
            break
        elif choice == "1":
            description = input("Activity description: ").strip()
            status = input("Status (✅/⏳/❌) [✅]: ").strip() or "✅"
            impact = input("Impact (optional): ").strip()
            if description:
                updater.log_activity("manual", description, status, impact)
        elif choice == "2":
            title = input("Decision title: ").strip()
            rationale = input("Rationale: ").strip()
            implementation = input("Implementation: ").strip()
            outcome = input("Outcome: ").strip()
            if title and rationale:
                updater.add_decision(title, rationale, implementation, outcome)
        elif choice == "3":
            updater.generate_daily_summary()
        elif choice == "4":
            print("Enter achievements (one per line, empty line to finish):")
            achievements = []
            while True:
                achievement = input("- ").strip()
                if not achievement:
                    break
                achievements.append(achievement)
            if achievements:
                updater.update_session_summary(achievements)
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()

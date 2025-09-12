#!/usr/bin/env python3
"""
Obsidian Vault Finder and Setup
Locate existing Obsidian vaults or help create a new one integrated with Daily Assistant
Created: September 6, 2025
"""

import os
import json
import subprocess
from pathlib import Path

class ObsidianVaultManager:
    """Manage Obsidian vault integration"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.common_vault_locations = [
            Path.home() / "Documents" / "Obsidian",
            Path.home() / "Documents" / "Notes", 
            Path.home() / "Obsidian",
            Path.home() / "Notes",
            Path.home() / "Desktop" / "Obsidian",
            Path.home() / "iCloud Drive (Archive)" / "Documents" / "Obsidian",
            Path.home() / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents",
        ]
    
    def find_existing_vaults(self):
        """Search for existing Obsidian vaults"""
        found_vaults = []
        
        print("🔍 Searching for existing Obsidian vaults...")
        
        # Search common locations
        for location in self.common_vault_locations:
            if location.exists():
                # Check if it's a vault directory (contains .obsidian folder)
                if (location / ".obsidian").exists():
                    found_vaults.append(location)
                    print(f"✅ Found vault: {location}")
                # Check subdirectories
                else:
                    for subdir in location.iterdir():
                        if subdir.is_dir() and (subdir / ".obsidian").exists():
                            found_vaults.append(subdir)
                            print(f"✅ Found vault: {subdir}")
        
        # Search using mdfind (macOS Spotlight)
        try:
            result = subprocess.run(['mdfind', 'kMDItemFSName == ".obsidian"'], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        vault_path = Path(line).parent
                        if vault_path not in found_vaults:
                            found_vaults.append(vault_path)
                            print(f"✅ Found vault (via Spotlight): {vault_path}")
        except:
            pass
        
        if not found_vaults:
            print("❌ No existing Obsidian vaults found")
        
        return found_vaults
    
    def create_daily_assistant_vault(self):
        """Create a new Obsidian vault integrated with Daily Assistant"""
        vault_path = self.base_path.parent / "Daily_Assistant_Vault"
        
        print(f"📁 Creating new Obsidian vault at: {vault_path}")
        
        # Create vault directory structure
        vault_path.mkdir(exist_ok=True)
        (vault_path / ".obsidian").mkdir(exist_ok=True)
        
        # Create basic Obsidian configuration
        obsidian_config = {
            "theme": "system",
            "translucency": False,
            "cssTheme": "",
            "interfaceFontFamily": "",
            "baseFontSize": 16,
            "pluginEnabledStatus": {
                "file-explorer": True,
                "global-search": True,
                "switcher": True,
                "graph": True,
                "backlink": True,
                "outgoing-links": True,
                "tag-pane": True,
                "page-preview": True,
                "daily-notes": True,
                "templates": True,
                "note-composer": True,
                "word-count": True,
                "markdown-importer": True,
                "outline": True
            }
        }
        
        with open(vault_path / ".obsidian" / "app.json", 'w') as f:
            json.dump(obsidian_config, f, indent=2)
        
        # Create workspace configuration
        workspace_config = {
            "main": {
                "id": "daily-assistant-workspace",
                "type": "split",
                "children": [
                    {
                        "id": "main-area",
                        "type": "tabs",
                        "children": [
                            {
                                "id": "daily-notes",
                                "type": "leaf",
                                "state": {
                                    "type": "markdown",
                                    "state": {
                                        "file": "Daily Notes/Index.md",
                                        "mode": "source"
                                    }
                                }
                            }
                        ]
                    }
                ]
            },
            "left": {
                "id": "left-sidebar",
                "type": "split",
                "children": [
                    {
                        "id": "file-explorer",
                        "type": "tabs",
                        "children": [
                            {
                                "id": "file-explorer-tab",
                                "type": "leaf",
                                "state": {"type": "file-explorer"}
                            }
                        ]
                    }
                ]
            }
        }
        
        with open(vault_path / ".obsidian" / "workspace.json", 'w') as f:
            json.dump(workspace_config, f, indent=2)
        
        # Create directory structure
        directories = [
            "Daily Notes",
            "Projects", 
            "Email Automation",
            "Research",
            "Templates",
            "Archive"
        ]
        
        for directory in directories:
            (vault_path / directory).mkdir(exist_ok=True)
        
        # Create initial notes
        self.create_initial_notes(vault_path)
        
        print("✅ Obsidian vault created successfully!")
        return vault_path
    
    def create_initial_notes(self, vault_path):
        """Create initial note structure"""
        
        # Main index note
        index_content = """# Daily Assistant Knowledge Base

Welcome to your integrated Daily Assistant and Obsidian knowledge management system.

## 🗂️ Quick Navigation

- [[Daily Activity Trail]] - Master activity tracking
- [[Email Automation]] - Email workflow documentation  
- [[Research Projects]] - Academic work and analysis
- [[Website Management]] - Content and automation tools
- [[Technical Decisions]] - Architecture and implementation notes

## 📅 Daily Notes

Use the daily notes feature to track daily activities. This integrates with your `MASTER_ACTIVITY_TRAIL.md` system.

## 🔗 Integration

This vault is designed to work seamlessly with your Daily Assistant project located at:
`/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/`

## 🎯 Getting Started

1. Enable daily notes plugin
2. Set up templates for consistent note structure
3. Create project notes for ongoing work
4. Link related concepts and track progress

---

*Last updated: September 6, 2025*
"""
        
        with open(vault_path / "Daily Notes" / "Index.md", 'w') as f:
            f.write(index_content)
        
        # Daily activity trail note
        trail_content = """# Daily Activity Trail

> This note integrates with your `MASTER_ACTIVITY_TRAIL.md` file in the Daily Assistant project.

## Current Session Activities

Link to external file: `MASTER_ACTIVITY_TRAIL.md`

## Key Achievements Today

- [ ] Review and update from external trail file
- [ ] Plan next session priorities  
- [ ] Document decisions and learnings

## Integration Notes

This Obsidian note complements the comprehensive tracking system in your Daily Assistant project. Use this for:

- Quick daily capture
- Cross-linking to project notes
- Visual graph connections
- Template-based note creation

Use the external file for:
- Detailed activity logging
- Technical implementation tracking
- Comprehensive session summaries
- Automated updates from scripts

---

*Template for daily activity tracking*
"""
        
        with open(vault_path / "Daily Notes" / "Daily Activity Trail.md", 'w') as f:
            f.write(trail_content)
        
        # Email automation project note
        email_content = """# Email Automation System

## Overview

Comprehensive email workflow management system for Mac Mail.app automation.

## Key Components

### Main Tools
- `email_workflow.py` - Unified workflow interface
- Contact management system
- Activity logging and tracking

### Directory Structure
- `core_tools/` - General-purpose email tools
- `specialized_scripts/` - Task-specific automation
- `documentation/` - Guides and setup information
- `contacts/` - Contact database management

## Current Status

✅ **Complete system reorganization** - September 6, 2025
- Unified 30+ scripts into single workflow tool
- Organized directory structure  
- Integrated contact management
- Comprehensive documentation

## Usage

```bash
python3 operating/email_automation/email_workflow.py
```

## Links

- [[Daily Activity Trail]] - Track email automation activities
- [[Technical Decisions]] - Architecture decisions for email system

---

*Project documentation for email automation system*
"""
        
        with open(vault_path / "Email Automation" / "Email Automation.md", 'w') as f:
            f.write(email_content)
        
        print("✅ Created initial note structure")
    
    def integrate_with_daily_assistant(self, vault_path):
        """Create integration scripts between vault and Daily Assistant"""
        
        # Create a sync script
        sync_script = f'''#!/bin/bash
# Obsidian-Daily Assistant Sync Script

VAULT_PATH="{vault_path}"
DA_PATH="{self.base_path}"

echo "🔄 Syncing Daily Assistant with Obsidian Vault..."

# Copy master activity trail to vault for reference
cp "$DA_PATH/MASTER_ACTIVITY_TRAIL.md" "$VAULT_PATH/Daily Notes/"

# Copy project documentation
cp "$DA_PATH/projectNotes.md" "$VAULT_PATH/Projects/"

# Copy email automation documentation  
cp "$DA_PATH/operating/email_automation/README.md" "$VAULT_PATH/Email Automation/"

echo "✅ Sync complete!"
'''
        
        sync_script_path = self.base_path / "sync_with_obsidian.sh"
        with open(sync_script_path, 'w') as f:
            f.write(sync_script)
        
        os.chmod(sync_script_path, 0o755)
        print(f"✅ Created sync script: {sync_script_path}")
    
    def show_menu(self):
        """Display the vault management menu"""
        print("\n" + "="*50)
        print("📝 OBSIDIAN VAULT MANAGER")
        print("="*50)
        print("1. Find existing Obsidian vaults")
        print("2. Create new Daily Assistant vault")  
        print("3. Set up vault integration")
        print("4. Open vault in Obsidian")
        print("0. Exit")
        print("="*50)

def main():
    """Main vault management interface"""
    manager = ObsidianVaultManager()
    selected_vault = None
    
    while True:
        manager.show_menu()
        choice = input("\nSelect option (0-4): ").strip()
        
        if choice == "0":
            print("👋 Obsidian integration ready!")
            break
        elif choice == "1":
            vaults = manager.find_existing_vaults()
            if vaults:
                print(f"\n📁 Found {len(vaults)} vault(s):")
                for i, vault in enumerate(vaults, 1):
                    print(f"  {i}. {vault}")
                
                # Let user select a vault
                try:
                    selection = input(f"\nSelect vault (1-{len(vaults)}) or 0 to skip: ").strip()
                    if selection != "0":
                        selected_vault = vaults[int(selection) - 1]
                        print(f"✅ Selected vault: {selected_vault}")
                except (ValueError, IndexError):
                    print("❌ Invalid selection")
        elif choice == "2":
            selected_vault = manager.create_daily_assistant_vault()
        elif choice == "3":
            if selected_vault:
                manager.integrate_with_daily_assistant(selected_vault)
            else:
                print("❌ Please select or create a vault first")
        elif choice == "4":
            if selected_vault:
                try:
                    subprocess.run(['open', str(selected_vault)], check=True)
                    print(f"✅ Opening vault in Obsidian: {selected_vault}")
                except subprocess.CalledProcessError:
                    print(f"❌ Could not open vault. Try opening manually: {selected_vault}")
            else:
                print("❌ Please select or create a vault first")
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()

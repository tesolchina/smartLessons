#!/usr/bin/env python3
"""
Sync files with #deadline hashtag from Obsidian vault to VS Code workspace
"""

import os
import shutil
from pathlib import Path
import re
from datetime import datetime

def find_deadline_files(vault_path):
    """Find all files containing #deadline hashtag"""
    vault = Path(vault_path)
    hashtag_pattern = r'#deadline\b'
    deadline_files = []
    
    for md_file in vault.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if re.search(hashtag_pattern, content, re.IGNORECASE):
                deadline_files.append({
                    'source_path': md_file,
                    'relative_path': md_file.relative_to(vault),
                    'name': md_file.name
                })
                
        except (UnicodeDecodeError, PermissionError):
            continue
            
    return deadline_files

def sync_deadline_files(vault_path, workspace_path):
    """Sync all #deadline files to workspace"""
    
    # Create deadline_files directory in workspace
    deadline_dir = Path(workspace_path) / "deadline_files"
    deadline_dir.mkdir(exist_ok=True)
    
    print(f"🔍 Searching for #deadline files in: {vault_path}")
    print(f"📁 Syncing to: {deadline_dir}")
    print("=" * 60)
    
    deadline_files = find_deadline_files(vault_path)
    
    if not deadline_files:
        print("❌ No files with #deadline hashtag found")
        return
    
    # Create master index file
    index_content = [
        f"# Deadline Files Index",
        f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"",
        f"Found {len(deadline_files)} files containing #deadline hashtag:",
        f"",
    ]
    
    synced_count = 0
    
    for i, file_info in enumerate(deadline_files, 1):
        source_path = file_info['source_path']
        filename = file_info['name']
        
        # Create unique filename if there are duplicates
        target_path = deadline_dir / filename
        counter = 1
        while target_path.exists():
            name_stem = Path(filename).stem
            name_suffix = Path(filename).suffix
            target_path = deadline_dir / f"{name_stem}_{counter:02d}{name_suffix}"
            counter += 1
        
        try:
            # Copy file to deadline directory
            shutil.copy2(source_path, target_path)
            synced_count += 1
            
            # Add to index
            relative_name = target_path.name
            index_content.extend([
                f"{i:2d}. **[{relative_name}](./{relative_name})**",
                f"    - Original: `{file_info['relative_path']}`",
                f"    - Synced: `{target_path.relative_to(Path(workspace_path))}`",
                f""
            ])
            
            print(f"✅ {i:2d}. {relative_name}")
            
        except Exception as e:
            print(f"❌ Failed to sync {filename}: {e}")
            index_content.extend([
                f"{i:2d}. **{filename}** ❌ FAILED",
                f"    - Error: {str(e)[:50]}...",
                f""
            ])
    
    # Write index file
    index_path = deadline_dir / "README_DEADLINE_INDEX.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(index_content))
    
    print("=" * 60)
    print(f"📊 **Sync Summary:**")
    print(f"   • Files found: {len(deadline_files)}")
    print(f"   • Files synced: {synced_count}")
    print(f"   • Sync directory: {deadline_dir}")
    print(f"   • Index file: {index_path}")
    
    # Create a comprehensive deadline overview
    create_deadline_overview(deadline_files, deadline_dir, vault_path)

def create_deadline_overview(deadline_files, deadline_dir, vault_path):
    """Create a comprehensive overview of all deadlines"""
    
    overview_content = [
        f"# 📅 Deadline Overview & Task Manager",
        f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"",
        f"## 📊 Summary",
        f"- **Total files with deadlines:** {len(deadline_files)}",
        f"- **Vault location:** `{vault_path}`",
        f"- **Synced to:** `{deadline_dir}`",
        f"",
        f"## 🎯 Quick Actions",
        f"- [ ] Review all deadline files below",
        f"- [ ] Update priority deadlines",
        f"- [ ] Set reminders for upcoming deadlines", 
        f"- [ ] Archive completed deadline tasks",
        f"",
        f"## 📋 All Deadline Files",
        f""
    ]
    
    # Extract deadline contexts from files
    deadline_contexts = []
    
    for i, file_info in enumerate(deadline_files, 1):
        source_path = file_info['source_path']
        filename = file_info['name']
        
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find lines containing #deadline with context
            lines = content.split('\n')
            deadline_lines = []
            
            for line_num, line in enumerate(lines):
                if re.search(r'#deadline\b', line, re.IGNORECASE):
                    # Get some context around the deadline
                    context_start = max(0, line_num - 1)
                    context_end = min(len(lines), line_num + 2)
                    context_lines = lines[context_start:context_end]
                    
                    deadline_lines.append({
                        'line_num': line_num + 1,
                        'line': line.strip(),
                        'context': context_lines
                    })
            
            overview_content.extend([
                f"### {i}. [{filename}](./{filename})",
                f"**File:** `{file_info['relative_path']}`",
                f""
            ])
            
            if deadline_lines:
                overview_content.append("**Deadline contexts:**")
                for dl in deadline_lines:
                    overview_content.extend([
                        f"- Line {dl['line_num']}: `{dl['line']}`",
                        f"  ```",
                    ])
                    for ctx_line in dl['context']:
                        overview_content.append(f"  {ctx_line}")
                    overview_content.extend([
                        f"  ```",
                        f""
                    ])
            
            overview_content.append("---")
            overview_content.append("")
            
        except Exception as e:
            overview_content.extend([
                f"❌ Could not read deadline contexts: {e}",
                f"",
                f"---",
                f""
            ])
    
    # Write overview file
    overview_path = deadline_dir / "DEADLINE_OVERVIEW.md"
    with open(overview_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(overview_content))
    
    print(f"📋 Created deadline overview: {overview_path}")

def main():
    vault_path = "/Users/simonwang/Documents/Usage/ObSync/Vault4sync"
    workspace_path = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant"
    
    sync_deadline_files(vault_path, workspace_path)

if __name__ == "__main__":
    main()

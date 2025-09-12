#!/usr/bin/env python3
"""
Quick search for #deadline hashtag in Obsidian vault
"""

import os
import re
from pathlib import Path

def search_deadline_hashtag(vault_path):
    """Search for #deadline hashtag in all markdown files"""
    
    vault = Path(vault_path)
    if not vault.exists():
        print(f"❌ Vault path does not exist: {vault_path}")
        return
    
    hashtag_pattern = r'#deadline\b'
    files_with_deadline = []
    
    print(f"🔍 Searching for #deadline hashtag in: {vault_path}")
    print("=" * 60)
    
    # Search through all markdown files
    for md_file in vault.rglob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Find all #deadline occurrences
            matches = re.findall(hashtag_pattern, content, re.IGNORECASE)
            
            if matches:
                files_with_deadline.append({
                    'file': md_file,
                    'count': len(matches),
                    'relative_path': md_file.relative_to(vault)
                })
                
        except (UnicodeDecodeError, PermissionError) as e:
            continue
    
    # Display results
    if files_with_deadline:
        print(f"✅ Found #deadline in {len(files_with_deadline)} files:")
        print()
        
        for i, file_info in enumerate(files_with_deadline, 1):
            print(f"{i:3d}. **{file_info['relative_path']}**")
            print(f"     📊 {file_info['count']} occurrence{'s' if file_info['count'] > 1 else ''}")
            print(f"     📁 {file_info['file'].parent}")
            print()
            
        print(f"📈 **Total Summary:**")
        print(f"   • Files with #deadline: {len(files_with_deadline)}")
        print(f"   • Total #deadline occurrences: {sum(f['count'] for f in files_with_deadline)}")
        
    else:
        print("❌ No files found with #deadline hashtag")
        print("\n🔍 **Troubleshooting suggestions:**")
        print("   • Check if the hashtag is spelled correctly: #deadline")
        print("   • Verify the vault path is correct")
        print("   • Make sure files contain the hashtag with # prefix")

def main():
    vault_path = "/Users/simonwang/Documents/Usage/ObSync/Vault4sync"
    search_deadline_hashtag(vault_path)

if __name__ == "__main__":
    main()

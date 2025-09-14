#!/usr/bin/env python3
"""
Consolidate Individual Letters from Multiple Folders
This script consolidates all high-quality individual letters from various extraction attempts
into a single organized corpus while removing the problematic datasets.
"""

import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any
import re

def analyze_existing_corpora():
    """Analyze existing letter corpora to understand what we have"""
    
    base_dir = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/BenSCMPGRF'
    
    corpora_info = {}
    
    # Check each corpus folder
    folders_to_check = [
        ('individual_letters', 'BAD - Fake letters from failed approach'),
        ('individual_letters_proper', 'MEDIUM - Letters from incomplete content'),
        ('individual_letters_manual', 'GOOD - Manual extraction'),
        ('enhanced_research_corpus', 'EXCELLENT - fetch_webpage approach'),
        ('final_research_corpus', 'GOOD - Early working approach')
    ]
    
    for folder_name, description in folders_to_check:
        folder_path = os.path.join(base_dir, folder_name)
        if os.path.exists(folder_path):
            json_dir = os.path.join(folder_path, 'json')
            if os.path.exists(json_dir):
                letter_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
                corpora_info[folder_name] = {
                    'description': description,
                    'path': folder_path,
                    'json_path': json_dir,
                    'letter_count': len(letter_files),
                    'files': letter_files[:5]  # Sample files
                }
    
    return corpora_info

def load_letter_from_json(file_path: str) -> Dict[str, Any]:
    """Load letter data from JSON file and normalize format"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Normalize different JSON formats
    normalized = {
        'title': '',
        'content': '',
        'author': 'Unknown',
        'source_url': '',
        'content_length': 0,
        'word_count': 0,
        'extraction_source': '',
        'extraction_timestamp': ''
    }
    
    # Handle different JSON structures
    if 'title' in data:
        # Enhanced/final corpus format
        normalized.update({
            'title': data.get('title', ''),
            'content': data.get('content', ''),
            'author': data.get('author', 'Unknown'),
            'source_url': data.get('source_url', ''),
            'content_length': data.get('content_length', len(data.get('content', ''))),
            'word_count': data.get('word_count', len(data.get('content', '').split())),
            'extraction_timestamp': data.get('extraction_timestamp', '')
        })
    elif 'metadata' in data and 'page_info' in data:
        # Individual letters format (bad corpus)
        content = data.get('content', {}).get('text', '')
        normalized.update({
            'title': data.get('metadata', {}).get('topic_summary', ''),
            'content': content,
            'author': data.get('metadata', {}).get('author', 'Unknown'),
            'source_url': data.get('page_info', {}).get('page_url', ''),
            'content_length': len(content),
            'word_count': len(content.split()) if content else 0,
            'extraction_timestamp': data.get('extraction_timestamp', '')
        })
    
    return normalized

def consolidate_letters():
    """Consolidate all good quality letters into a single corpus"""
    
    print("🔄 CONSOLIDATING INDIVIDUAL LETTERS")
    print("=" * 80)
    
    base_dir = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/BenSCMPGRF'
    corpora_info = analyze_existing_corpora()
    
    # Print analysis
    print("📊 Current Letter Corpora Analysis:")
    for folder, info in corpora_info.items():
        quality = "🟢 KEEP" if "GOOD" in info['description'] or "EXCELLENT" in info['description'] else "🔴 REMOVE"
        print(f"   {quality} {folder}: {info['letter_count']} letters - {info['description']}")
    
    # Collect all high-quality letters
    consolidated_letters = []
    sources_used = []
    
    # Priority order: best quality first
    priority_folders = [
        'enhanced_research_corpus',  # Best quality
        'final_research_corpus',     # Good quality  
        'individual_letters_manual'  # Manual extraction
    ]
    
    print(f"\n🔄 Consolidating letters from high-quality sources...")
    
    for folder_name in priority_folders:
        if folder_name in corpora_info:
            info = corpora_info[folder_name]
            json_dir = info['json_path']
            
            print(f"\n📁 Processing {folder_name} ({info['letter_count']} letters)...")
            
            letter_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
            
            for file_name in letter_files:
                file_path = os.path.join(json_dir, file_name)
                try:
                    letter = load_letter_from_json(file_path)
                    letter['extraction_source'] = folder_name
                    letter['original_file'] = file_name
                    
                    # Only include letters with substantial content
                    if letter['content'] and len(letter['content']) > 100:
                        consolidated_letters.append(letter)
                        print(f"   ✅ Added: {letter['title'][:50]}... by {letter['author'][:30]} ({letter['word_count']} words)")
                    else:
                        print(f"   ⚠️  Skipped: {file_name} (insufficient content)")
                        
                except Exception as e:
                    print(f"   ❌ Error loading {file_name}: {e}")
            
            sources_used.append(folder_name)
    
    return consolidated_letters, sources_used, corpora_info

def save_consolidated_corpus(letters: List[Dict[str, Any]], sources: List[str], output_dir: str):
    """Save the consolidated corpus"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    json_dir = os.path.join(output_dir, 'json')
    md_dir = os.path.join(output_dir, 'markdown')
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(md_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Remove duplicates based on content similarity
    unique_letters = []
    seen_content = set()
    
    for letter in letters:
        content_hash = hash(letter['content'][:200])  # Use first 200 chars for dedup
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_letters.append(letter)
        else:
            print(f"   🔄 Removed duplicate: {letter['title'][:50]}...")
    
    # Calculate statistics
    total_words = sum(letter['word_count'] for letter in unique_letters)
    unique_authors = set(letter['author'] for letter in unique_letters if letter['author'] != 'Unknown')
    avg_length = sum(letter['content_length'] for letter in unique_letters) // len(unique_letters) if unique_letters else 0
    
    # Save individual letters
    for i, letter in enumerate(unique_letters, 1):
        # Create safe filename
        author_safe = letter['author'].split(',')[0].replace(' ', '_').replace('.', '').replace('/', '')[:20]
        if author_safe == "Unknown" or not author_safe:
            title_safe = re.sub(r'[^\w\s-]', '', letter['title'])[:30].replace(' ', '_')
            letter_id = f"letter_{i:03d}_{title_safe}"
        else:
            letter_id = f"letter_{i:03d}_{author_safe}"
        
        # Add consolidated metadata
        letter['consolidated_id'] = letter_id
        letter['consolidated_timestamp'] = datetime.now().isoformat()
        
        # Save JSON
        json_file = os.path.join(json_dir, f"{letter_id}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(letter, f, indent=2, ensure_ascii=False)
        
        # Save Markdown
        md_file = os.path.join(md_dir, f"{letter_id}.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"# {letter['title']}\n\n")
            f.write(f"**Author:** {letter['author']}\n\n")
            f.write(f"**Source:** {letter['source_url']}\n\n")
            f.write(f"**Statistics:** {letter['word_count']} words | {letter['content_length']} characters\n\n")
            f.write(f"**Extraction Source:** {letter['extraction_source']}\n\n")
            f.write(f"---\n\n")
            f.write(letter['content'])
            f.write(f"\n\n---\n\n")
            f.write(f"*Letter ID: {letter_id} | Consolidated: {letter['consolidated_timestamp']}*\n")
    
    # Save consolidated summary
    summary = {
        'corpus_info': {
            'name': 'SCMP Letters - Consolidated Research Corpus',
            'consolidation_timestamp': datetime.now().isoformat(),
            'consolidation_method': 'High-quality letters from multiple extraction attempts',
            'source': 'South China Morning Post - Letters to the Editor',
            'sources_consolidated': sources,
            'url': 'https://www.scmp.com/comment/letters'
        },
        'statistics': {
            'total_letters': len(unique_letters),
            'total_words': total_words,
            'average_letter_length_chars': avg_length,
            'average_letter_length_words': total_words // len(unique_letters) if unique_letters else 0,
            'unique_authors': len(unique_authors),
            'letters_with_known_authors': len([l for l in unique_letters if l['author'] != 'Unknown']),
            'duplicates_removed': len(letters) - len(unique_letters)
        },
        'source_breakdown': {
            source: len([l for l in unique_letters if l['extraction_source'] == source])
            for source in sources
        }
    }
    
    summary_file = os.path.join(output_dir, f'consolidated_corpus_summary_{timestamp}.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Save all letters in single file
    all_letters_file = os.path.join(output_dir, f'all_consolidated_letters_{timestamp}.json')
    with open(all_letters_file, 'w', encoding='utf-8') as f:
        json.dump(unique_letters, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ CONSOLIDATED CORPUS CREATED!")
    print(f"📁 Location: {output_dir}")
    print(f"📊 {len(unique_letters)} unique letters (removed {len(letters) - len(unique_letters)} duplicates)")
    print(f"📈 {total_words:,} total words")
    print(f"👥 {len(unique_authors)} unique authors")
    print(f"📄 Summary: {summary_file}")
    
    return summary_file, unique_letters

def cleanup_bad_corpora(corpora_info: Dict[str, Any], keep_folders: List[str]):
    """Remove the bad quality corpora"""
    
    print(f"\n🧹 CLEANING UP BAD CORPORA")
    print("=" * 40)
    
    base_dir = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/BenSCMPGRF'
    
    folders_to_remove = []
    
    for folder_name, info in corpora_info.items():
        if folder_name not in keep_folders and "BAD" in info['description']:
            folders_to_remove.append(folder_name)
    
    if folders_to_remove:
        print(f"⚠️  The following folders contain low-quality data and should be removed:")
        for folder in folders_to_remove:
            info = corpora_info[folder]
            print(f"   🔴 {folder}: {info['letter_count']} letters - {info['description']}")
        
        response = input(f"\nRemove these {len(folders_to_remove)} folders? (y/N): ").strip().lower()
        
        if response == 'y':
            for folder in folders_to_remove:
                folder_path = os.path.join(base_dir, folder)
                try:
                    shutil.rmtree(folder_path)
                    print(f"   ✅ Removed: {folder}")
                except Exception as e:
                    print(f"   ❌ Error removing {folder}: {e}")
        else:
            print(f"   ⏭️  Skipped removal (folders preserved)")
    else:
        print(f"✅ No bad corpora found to remove")

def main():
    """Main consolidation function"""
    
    try:
        # Consolidate letters
        letters, sources, corpora_info = consolidate_letters()
        
        if letters:
            # Create consolidated corpus
            output_dir = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/BenSCMPGRF/consolidated_research_corpus'
            summary_file, unique_letters = save_consolidated_corpus(letters, sources, output_dir)
            
            print(f"\n🎉 CONSOLIDATION COMPLETED!")
            print(f"📊 Consolidated {len(unique_letters)} high-quality individual letters")
            print(f"📚 Sources: {', '.join(sources)}")
            
            # Cleanup bad corpora
            keep_folders = sources + ['consolidated_research_corpus']
            cleanup_bad_corpora(corpora_info, keep_folders)
            
        else:
            print("❌ No letters found to consolidate")
            
    except Exception as e:
        print(f"❌ Error during consolidation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
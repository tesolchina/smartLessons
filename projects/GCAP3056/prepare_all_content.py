#!/usr/bin/env python3
"""
Prepare All Content for Google Docs Upload
Converts all markdown files to Google Docs format in preparation for upload
"""

import os
from pathlib import Path
from markdown_to_googledocs import MarkdownToGoogleDocsConverter

# Projects and their markdown files
PROJECTS = [
    "energy_poverty", 
    "hko_chatbot", 
    "chronic_disease_co_care", 
    "anti_scamming_education", 
    "emergency_alert_system"
]

# Tab mappings
TAB_MAPPINGS = {
    "Writing for the public": "letter_to_editor.md",
    "Engage the government": "government_questions.md", 
    "Argumentative Research Paper": "argumentative_research_paper.md"
}

def prepare_all_content():
    """Convert all markdown files to Google Docs format"""
    converter = MarkdownToGoogleDocsConverter()
    output_dir = Path("/tmp/google_docs_content")
    output_dir.mkdir(exist_ok=True)
    
    print("🔄 Converting all markdown files to Google Docs format...")
    print(f"📁 Output directory: {output_dir}")
    
    results = {}
    
    for project_name in PROJECTS:
        print(f"\n{'='*50}")
        print(f"📁 {project_name.upper()}")
        print('='*50)
        
        project_results = {}
        
        for tab_name, markdown_file in TAB_MAPPINGS.items():
            markdown_path = Path(f"Projects and teams/{project_name}/{markdown_file}")
            
            if not markdown_path.exists():
                print(f"❌ Not found: {markdown_path}")
                project_results[tab_name] = {'status': 'missing', 'file': str(markdown_path)}
                continue
            
            # Convert markdown
            converted_text = converter.convert_file(str(markdown_path), tab_name)
            
            if converted_text:
                # Save converted content
                output_file = output_dir / f"{project_name}_{markdown_file.replace('.md', '')}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(converted_text)
                
                print(f"✅ {tab_name}: {len(converted_text)} chars → {output_file.name}")
                project_results[tab_name] = {
                    'status': 'converted',
                    'file': str(output_file),
                    'length': len(converted_text)
                }
            else:
                print(f"❌ Failed to convert: {markdown_path}")
                project_results[tab_name] = {'status': 'failed', 'file': str(markdown_path)}
        
        results[project_name] = project_results
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 CONVERSION SUMMARY")
    print('='*60)
    
    total_converted = 0
    total_files = 0
    
    for project_name, project_results in results.items():
        print(f"\n📁 {project_name}:")
        for tab_name, result in project_results.items():
            status_icon = {
                'converted': '✅',
                'missing': '❌',
                'failed': '❌'
            }.get(result['status'], '❓')
            
            print(f"  {status_icon} {tab_name}: {result['status']}")
            if result['status'] == 'converted':
                print(f"      Length: {result['length']} characters")
            
            total_files += 1
            if result['status'] == 'converted':
                total_converted += 1
    
    print(f"\n🎯 Conversion Rate: {total_converted}/{total_files} ({100*total_converted/total_files:.1f}%)")
    
    # List all converted files ready for upload
    print(f"\n📋 READY FOR UPLOAD:")
    for file in sorted(output_dir.glob("*.txt")):
        print(f"  📄 {file.name}")
    
    return results

if __name__ == "__main__":
    prepare_all_content()

#!/usr/bin/env python3
"""
Word Document to Markdown Converter
Converts .docx files to .md files using mammoth library
"""

import mammoth
import os
import sys
from pathlib import Path

def convert_docx_to_md(docx_path, output_dir=None):
    """
    Convert a Word document (.docx) to Markdown (.md)
    
    Args:
        docx_path (str): Path to the input .docx file
        output_dir (str): Directory to save the output .md file (default: same as input)
    
    Returns:
        str: Path to the created markdown file
    """
    # Convert path to Path object
    docx_path = Path(docx_path)
    
    # Check if file exists
    if not docx_path.exists():
        raise FileNotFoundError(f"File not found: {docx_path}")
    
    # Determine output directory
    if output_dir is None:
        output_dir = docx_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create output filename (replace .docx with .md and clean up the name)
    output_filename = docx_path.stem.replace(' ', '_').replace('-', '_') + '.md'
    output_path = output_dir / output_filename
    
    try:
        # Convert docx to markdown using mammoth
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_markdown(docx_file)
            markdown_content = result.value
            
            # Check for any conversion warnings
            if result.messages:
                print(f"Conversion warnings for {docx_path.name}:")
                for message in result.messages:
                    print(f"  - {message}")
                print()
        
        # Write markdown content to file
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)
        
        print(f"✅ Successfully converted: {docx_path.name} -> {output_path.name}")
        return str(output_path)
        
    except Exception as e:
        print(f"❌ Error converting {docx_path.name}: {str(e)}")
        raise

def main():
    """Main function to convert specified documents"""
    
    # Define the documents to convert
    base_dir = Path("/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/courseMat")
    
    documents = [
        "Course description.docx",
        "SL course syllabus - Simon-final.docx"
    ]
    
    print("🔄 Starting Word document to Markdown conversion...")
    print("=" * 60)
    
    converted_files = []
    
    for doc in documents:
        doc_path = base_dir / doc
        
        if doc_path.exists():
            try:
                output_path = convert_docx_to_md(doc_path)
                converted_files.append(output_path)
            except Exception as e:
                print(f"Failed to convert {doc}: {e}")
        else:
            print(f"⚠️  File not found: {doc}")
    
    print("\n" + "=" * 60)
    print(f"✨ Conversion complete! Converted {len(converted_files)} documents:")
    for file_path in converted_files:
        print(f"  📄 {Path(file_path).name}")

if __name__ == "__main__":
    main()
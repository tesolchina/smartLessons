#!/usr/bin/env python3
"""
Convert DOCX file to Markdown format
"""

import os
import sys
from pathlib import Path

def convert_with_pypandoc():
    """Convert using pypandoc (requires pandoc to be installed)"""
    try:
        import pypandoc
        
        # Input and output file paths
        input_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/ERPP/students/Ruobin/Research Plan  (9.12).docx"
        output_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/ERPP/students/Ruobin/Research_Plan_9_12.md"
        
        print(f"Converting {input_file} to {output_file}")
        
        # Convert DOCX to Markdown
        output = pypandoc.convert_file(input_file, 'md', outputfile=output_file)
        
        print(f"✅ Successfully converted to {output_file}")
        return True
        
    except ImportError:
        print("❌ pypandoc not available")
        return False
    except Exception as e:
        print(f"❌ Error with pypandoc: {e}")
        return False

def convert_with_python_docx():
    """Convert using python-docx (basic text extraction)"""
    try:
        from docx import Document
        
        # Input and output file paths
        input_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/ERPP/students/Ruobin/Research Plan  (9.12).docx"
        output_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/ERPP/students/Ruobin/Research_Plan_9_12.md"
        
        print(f"Converting {input_file} to {output_file}")
        
        # Load the document
        doc = Document(input_file)
        
        # Extract text and convert to markdown
        markdown_content = []
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if not text:
                markdown_content.append("")
                continue
            
            # Check paragraph style for headers
            style_name = paragraph.style.name.lower()
            
            if 'heading 1' in style_name or 'title' in style_name:
                markdown_content.append(f"# {text}")
            elif 'heading 2' in style_name:
                markdown_content.append(f"## {text}")
            elif 'heading 3' in style_name:
                markdown_content.append(f"### {text}")
            elif 'heading 4' in style_name:
                markdown_content.append(f"#### {text}")
            elif 'heading 5' in style_name:
                markdown_content.append(f"##### {text}")
            elif 'heading 6' in style_name:
                markdown_content.append(f"###### {text}")
            else:
                # Check if paragraph is bold (potential header)
                if paragraph.runs and all(run.bold for run in paragraph.runs if run.text.strip()):
                    markdown_content.append(f"**{text}**")
                else:
                    markdown_content.append(text)
        
        # Write to markdown file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
        
        print(f"✅ Successfully converted to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error with python-docx: {e}")
        return False

def main():
    """Main conversion function"""
    input_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/ERPP/students/Ruobin/Research Plan  (9.12).docx"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return False
    
    print("🔄 Starting DOCX to Markdown conversion...")
    
    # Try pypandoc first (better formatting)
    if convert_with_pypandoc():
        return True
    
    print("⚠️  pypandoc failed, trying python-docx...")
    
    # Fallback to python-docx
    if convert_with_python_docx():
        return True
    
    print("❌ All conversion methods failed")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
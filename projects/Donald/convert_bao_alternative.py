#!/usr/bin/env python3
"""
Alternative converter for large .docx files
"""

import os
from docx import Document
import zipfile
import xml.etree.ElementTree as ET

def extract_text_from_docx_alternative(docx_path):
    """Alternative method to extract text from large .docx files"""
    try:
        # Open as zip file and extract text directly from XML
        with zipfile.ZipFile(docx_path, 'r') as zip_file:
            # Read the main document XML
            doc_xml = zip_file.read('word/document.xml').decode('utf-8')
            
            # Simple text extraction using string manipulation
            # Remove XML tags and extract text content
            import re
            
            # Extract text between XML tags
            text_pattern = r'<w:t[^>]*>([^<]*)</w:t>'
            matches = re.findall(text_pattern, doc_xml)
            text_content = ' '.join(matches)
            
            return text_content
            
    except Exception as e:
        print(f"Alternative extraction failed: {e}")
        return None

def convert_bao_file():
    """Specifically convert the Bao file that failed"""
    bao_path = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/Donald/Geo/SampleAssignments/Bao-Geography Coursework.docx"
    md_path = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/Donald/Geo/SampleAssignments/Bao-Geography Coursework.md"
    
    print("Attempting alternative conversion for Bao file...")
    
    text_content = extract_text_from_docx_alternative(bao_path)
    
    if text_content:
        # Clean up the text and format as markdown
        lines = text_content.split('\n')
        markdown_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                markdown_lines.append(line)
        
        # Write to file
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(markdown_lines))
        
        print(f"✅ Successfully converted Bao file using alternative method")
        return True
    else:
        print("❌ Alternative conversion failed")
        return False

if __name__ == "__main__":
    convert_bao_file()
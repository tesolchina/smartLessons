#!/usr/bin/env python3
"""
Convert Word document (.docx) to Markdown format
"""

import zipfile
import xml.etree.ElementTree as ET
import re
import sys
import os

def extract_text_from_docx(docx_path):
    """Extract text from a Word document and convert to markdown format"""
    try:
        with zipfile.ZipFile(docx_path, 'r') as doc:
            xml_content = doc.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            # Find all text elements and preserve structure
            text_elements = []
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    text_elements.append(elem.text.strip())
            
            # Join and clean up text
            full_text = ' '.join(text_elements)
            
            # Basic markdown formatting
            # Replace multiple spaces with single spaces
            full_text = re.sub(r'\s+', ' ', full_text)
            
            # Try to identify sections and add markdown headers
            # Look for common academic paper structure
            full_text = re.sub(r'\b(Abstract)\b', r'\n\n# \1\n', full_text, flags=re.IGNORECASE)
            full_text = re.sub(r'\b(Introduction)\b', r'\n\n# \1\n', full_text, flags=re.IGNORECASE)
            full_text = re.sub(r'\b(Literature Review|Review of the related literature)\b', r'\n\n# \1\n', full_text, flags=re.IGNORECASE)
            full_text = re.sub(r'\b(Methods?|Methodology)\b', r'\n\n# \1\n', full_text, flags=re.IGNORECASE)
            full_text = re.sub(r'\b(Results?)\b', r'\n\n# \1\n', full_text, flags=re.IGNORECASE)
            full_text = re.sub(r'\b(Discussion)\b', r'\n\n# \1\n', full_text, flags=re.IGNORECASE)
            full_text = re.sub(r'\b(Conclusion)\b', r'\n\n# \1\n', full_text, flags=re.IGNORECASE)
            full_text = re.sub(r'\b(References?)\b', r'\n\n# \1\n', full_text, flags=re.IGNORECASE)
            
            # Look for numbered sections and research questions
            full_text = re.sub(r'(\d+\.\s+[A-Z][^.]*?:)', r'\n\n## \1\n', full_text)
            full_text = re.sub(r'\b(Research Questions?)\b', r'\n\n## \1\n', full_text, flags=re.IGNORECASE)
            
            # Clean up extra whitespace
            full_text = re.sub(r'\n\s*\n\s*\n', '\n\n', full_text)
            full_text = full_text.strip()
            
            return full_text
            
    except Exception as e:
        return f'Error: {str(e)}'

def main():
    # Define paths
    docx_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/goal-setting-chatbot-paper/writing/manuscript 0902.docx'
    output_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/citationAdvice/manuscript_0902.md'
    
    # Check if input file exists
    if not os.path.exists(docx_path):
        print(f"Error: Input file does not exist: {docx_path}")
        return 1
    
    print(f"Converting {docx_path} to Markdown...")
    
    # Extract text and convert to markdown
    markdown_text = extract_text_from_docx(docx_path)
    
    if markdown_text.startswith('Error:'):
        print(f"Failed to convert document: {markdown_text}")
        return 1
    
    # Write to output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        print(f"Successfully converted to: {output_path}")
        print(f"Document length: {len(markdown_text)} characters")
        return 0
    except Exception as e:
        print(f"Error writing output file: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
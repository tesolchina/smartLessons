#!/usr/bin/env python3
"""
Markdown to Google Docs Converter
Converts markdown files to properly formatted text for Google Docs API
Removes markdown syntax and converts to readable format
"""

import re
import argparse
import sys
from pathlib import Path

class MarkdownToGoogleDocsConverter:
    """Convert markdown content to Google Docs formatted text"""
    
    def __init__(self):
        pass
    
    def convert_markdown_to_text(self, markdown_content):
        """Convert markdown content to plain text suitable for Google Docs"""
        
        # Start with original content
        text = markdown_content
        
        # Remove HTML comments
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        
        # Convert headers to simple text with line breaks
        text = re.sub(r'^#{1}\s+(.+)$', r'\1\n' + '='*50, text, flags=re.MULTILINE)
        text = re.sub(r'^#{2}\s+(.+)$', r'\n\1\n' + '-'*30, text, flags=re.MULTILINE)
        text = re.sub(r'^#{3}\s+(.+)$', r'\n\1\n' + '-'*20, text, flags=re.MULTILINE)
        text = re.sub(r'^#{4,6}\s+(.+)$', r'\n\1\n', text, flags=re.MULTILINE)
        
        # Convert bold text
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        
        # Convert italic text
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        
        # Convert code blocks to simple text
        text = re.sub(r'```[\w]*\n(.*?)\n```', r'\1', text, flags=re.DOTALL)
        text = re.sub(r'`(.+?)`', r'\1', text)
        
        # Convert lists to simple format
        text = re.sub(r'^\s*[-*+]\s+(.+)$', r'• \1', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+(.+)$', r'\1', text, flags=re.MULTILINE)
        
        # Convert links to text with URL
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', text)
        
        # Clean up multiple line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove horizontal rules
        text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^===+$', '', text, flags=re.MULTILINE)
        
        # Clean up whitespace
        text = text.strip()
        
        return text
    
    def add_section_header(self, section_name, content):
        """Add a section header to content"""
        header = f"\n{'='*60}\n{section_name.upper()}\n{'='*60}\n\n"
        return header + content + "\n\n"
    
    def convert_file(self, markdown_file, section_name=None):
        """Convert a markdown file to Google Docs text"""
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            converted_text = self.convert_markdown_to_text(markdown_content)
            
            if section_name:
                converted_text = self.add_section_header(section_name, converted_text)
            
            return converted_text
            
        except Exception as e:
            print(f"Error converting {markdown_file}: {e}")
            return None
    
    def preview_conversion(self, markdown_file):
        """Preview the conversion result"""
        converted = self.convert_file(markdown_file)
        if converted:
            print(f"\n{'='*60}")
            print(f"PREVIEW: {Path(markdown_file).name}")
            print('='*60)
            print(converted[:500] + "..." if len(converted) > 500 else converted)
            print(f"\nTotal length: {len(converted)} characters")
        else:
            print(f"Failed to convert {markdown_file}")

def main():
    parser = argparse.ArgumentParser(description='Markdown to Google Docs Converter')
    parser.add_argument('input_file', help='Markdown file to convert')
    parser.add_argument('--section-name', help='Section name to add as header')
    parser.add_argument('--preview', action='store_true', help='Preview conversion result')
    parser.add_argument('--output', help='Output file for converted text')
    
    args = parser.parse_args()
    
    if not Path(args.input_file).exists():
        print(f"Error: File not found: {args.input_file}")
        sys.exit(1)
    
    converter = MarkdownToGoogleDocsConverter()
    
    if args.preview:
        converter.preview_conversion(args.input_file)
    else:
        converted_text = converter.convert_file(args.input_file, args.section_name)
        
        if args.output:
            if converted_text is not None:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(converted_text)
                print(f"Converted text saved to: {args.output}")
            else:
                print("Error: Conversion failed, no output written")
        else:
            if converted_text is not None:
                print(converted_text)
            else:
                print("Error: Conversion failed")

if __name__ == "__main__":
    main()

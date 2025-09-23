#!/usr/bin/env python3
"""
Process the downloaded Google Doc content and convert to readable format.
"""

import os
import re
import html
from pathlib import Path

def clean_html_content(html_content):
    """Extract and clean text content from HTML"""
    
    # Remove script and style elements
    html_content = re.sub(r'<script.*?</script>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<style.*?</style>', '', html_content, flags=re.DOTALL)
    
    # Remove HTML tags but preserve some structure
    html_content = re.sub(r'<p[^>]*>', '\n\n', html_content)
    html_content = re.sub(r'</p>', '', html_content)
    html_content = re.sub(r'<h[1-6][^>]*>', '\n\n## ', html_content)
    html_content = re.sub(r'</h[1-6]>', '\n\n', html_content)
    html_content = re.sub(r'<br[^>]*>', '\n', html_content)
    html_content = re.sub(r'<div[^>]*>', '\n', html_content)
    html_content = re.sub(r'</div>', '', html_content)
    
    # Remove remaining HTML tags
    html_content = re.sub(r'<[^>]+>', '', html_content)
    
    # Decode HTML entities
    html_content = html.unescape(html_content)
    
    # Clean up whitespace
    html_content = re.sub(r'\n\s*\n\s*\n', '\n\n', html_content)
    html_content = re.sub(r'[ \t]+', ' ', html_content)
    html_content = html_content.strip()
    
    return html_content

def process_downloaded_file():
    """Process the downloaded Google Doc file"""
    
    base_path = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/Donald/Geo"
    input_file = os.path.join(base_path, "Donald_Wong_IGCSE_Geo_Coursework.docx")
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return None
    
    print(f"🔄 Processing downloaded file: {input_file}")
    
    try:
        # Read the HTML content
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print(f"📄 File size: {len(html_content)} characters")
        
        # Extract clean text
        clean_text = clean_html_content(html_content)
        
        # Save as plain text
        txt_output = os.path.join(base_path, "Donald_Wong_IGCSE_Geo_Coursework_CLEANED.txt")
        with open(txt_output, 'w', encoding='utf-8') as f:
            f.write(clean_text)
        
        print(f"✅ Cleaned text saved: {txt_output}")
        
        # Save as markdown
        md_output = os.path.join(base_path, "Donald_Wong_IGCSE_Geo_Coursework_DOWNLOADED.md")
        
        # Basic markdown formatting
        markdown_content = clean_text
        markdown_content = f"# Donald Wong IGCSE Geography Coursework\n\n{markdown_content}"
        
        with open(md_output, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Markdown version saved: {md_output}")
        
        # Show preview
        preview = clean_text[:1000] + "..." if len(clean_text) > 1000 else clean_text
        print(f"\n📋 Content preview:\n{'-' * 50}")
        print(preview)
        print(f"{'-' * 50}")
        
        return md_output
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return None

def main():
    print("🧹 Google Doc Content Processor")
    print("=" * 50)
    
    result = process_downloaded_file()
    
    if result:
        print(f"\n🎉 Successfully processed Google Doc!")
        print(f"📝 Markdown file: {result}")
        print("\n💡 You can now:")
        print("1. Review the cleaned content")
        print("2. Compare with the existing draft")
        print("3. Merge improvements into the main document")
    else:
        print("\n❌ Processing failed. Try downloading manually:")
        print("https://docs.google.com/document/d/16iQJdg6hNmmlG6hLFRueRawOhI5l8JT2n8-ezXbtsSQ/edit")

if __name__ == "__main__":
    main()
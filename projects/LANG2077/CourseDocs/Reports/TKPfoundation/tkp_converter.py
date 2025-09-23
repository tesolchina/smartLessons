#!/usr/bin/env python3
"""
TKP Foundation Report Converter
==============================
Convert the TKP Foundation Word document to Markdown and create form filler
"""

import os
from pathlib import Path
import mammoth
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def convert_tkp_doc_to_markdown():
    """Convert TKP Foundation Word document to Markdown."""
    
    # File paths
    reports_dir = Path("/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports")
    tkp_dir = reports_dir / "TKPfoundation"
    
    input_file = tkp_dir / "田家炳基金會 青年品格培育計劃報告表_2024-25_template_LANG2077.docx"
    output_file = tkp_dir / "TKP_Foundation_Report_Template.md"
    
    logger.info(f"Converting {input_file.name} to Markdown...")
    
    try:
        # Convert DOCX to Markdown using mammoth
        with open(input_file, "rb") as docx_file:
            result = mammoth.convert_to_markdown(docx_file)
            markdown_content = result.value
            
            # Clean up the markdown content
            cleaned_content = clean_markdown_content(markdown_content)
            
            # Write to output file
            with open(output_file, 'w', encoding='utf-8') as md_file:
                md_file.write(cleaned_content)
            
            logger.info(f"✅ Successfully converted to: {output_file.name}")
            
            # Print any warnings
            if result.messages:
                logger.warning("Conversion warnings:")
                for message in result.messages:
                    logger.warning(f"  - {message}")
            
            return str(output_file)
            
    except Exception as e:
        logger.error(f"❌ Error converting document: {str(e)}")
        raise

def clean_markdown_content(markdown_content):
    """Clean up the converted markdown content."""
    
    # Add header
    cleaned_content = """# 田家炳基金會 青年品格培育計劃報告表 2024-25
## TKP Foundation Youth Character Development Program Report 2024-25

**Project:** LANG2077 - Language Skills for Human-AI Partnership: Customizing Chatbots to Empower Communities  
**Institution:** Language Centre, Hong Kong Baptist University  
**Reporting Period:** 2024-25 Academic Year

---

"""
    
    # Clean up the content
    lines = markdown_content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove excessive whitespace
        line = line.strip()
        
        # Skip empty lines at the beginning
        if not line and not cleaned_lines:
            continue
            
        # Convert Chinese punctuation and formatting
        line = line.replace('：', ':')
        line = line.replace('（', '(')
        line = line.replace('）', ')')
        
        # Add proper markdown formatting for form fields
        if '____' in line or '______' in line:
            # Replace underscores with form field placeholders
            line = line.replace('____', '[TO BE FILLED]')
            line = line.replace('______', '[TO BE FILLED]')
        
        cleaned_lines.append(line)
    
    # Join the cleaned content
    cleaned_content += '\n'.join(cleaned_lines)
    
    # Add footer
    cleaned_content += """

---

**Document Information:**
- Original Format: Microsoft Word (.docx)
- Converted to: Markdown (.md)
- Conversion Date: September 2025
- Purpose: Template preparation and automated form filling

**Next Steps:**
1. Review and clean up the converted content
2. Add bullet points for elaboration
3. Use Python automation to fill out the Word document
"""
    
    return cleaned_content

if __name__ == "__main__":
    try:
        output_file = convert_tkp_doc_to_markdown()
        print(f"\n🎉 TKP Foundation document successfully converted!")
        print(f"📁 Output file: {output_file}")
        print(f"🔍 Please review the markdown file and provide bullet points for elaboration.")
    except Exception as e:
        print(f"❌ Conversion failed: {str(e)}")
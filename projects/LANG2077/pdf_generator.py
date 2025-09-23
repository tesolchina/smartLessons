#!/usr/bin/env python3
"""
Generate PDF questionnaires from Markdown files
Converts the questionnaires to well-formatted PDF documents
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re

def setup_fonts():
    """Setup fonts for Chinese characters"""
    try:
        # Try to register Chinese fonts (might need to be installed)
        # You can download these fonts or use system fonts
        font_paths = [
            '/System/Library/Fonts/PingFang.ttc',  # macOS
            '/System/Library/Fonts/Helvetica.ttc',  # macOS fallback
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('Chinese', font_path))
                    return 'Chinese'
                except:
                    continue
        
        # Fallback to default fonts
        return 'Helvetica'
    except:
        return 'Helvetica'

def clean_markdown_text(text):
    """Clean markdown formatting for PDF"""
    # Remove markdown headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove markdown bold/italic
    text = re.sub(r'\*\*(.*?)\*\*', r'\\1', text)
    text = re.sub(r'\*(.*?)\*', r'\\1', text)
    # Remove markdown links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\\1', text)
    # Clean up extra whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def process_questionnaire_content(content):
    """Process questionnaire content for PDF formatting"""
    lines = content.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            processed_lines.append('')
            continue
            
        # Skip markdown meta information
        if line.startswith('#') and ('questionnaire' in line.lower() or 'survey' in line.lower()):
            processed_lines.append(line.replace('#', '').strip())
            processed_lines.append('=' * 50)
            continue
            
        # Handle headers
        if line.startswith('###'):
            processed_lines.append('')
            processed_lines.append(line.replace('###', '').strip())
            processed_lines.append('-' * 30)
        elif line.startswith('##'):
            processed_lines.append('')
            processed_lines.append(line.replace('##', '').strip())
            processed_lines.append('=' * 40)
        elif line.startswith('#'):
            continue  # Skip single # headers as they're often duplicates
        
        # Handle list items
        elif line.startswith('- □'):
            processed_lines.append('  ' + line)
        elif line.startswith('□'):
            processed_lines.append('  ' + line)
        
        # Handle regular content
        else:
            processed_lines.append(line)
    
    return '\n'.join(processed_lines)

def create_pdf_questionnaire(md_file_path, output_path, title):
    """Create PDF from markdown questionnaire"""
    
    # Read markdown content
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean and process content
    content = clean_markdown_text(content)
    content = process_questionnaire_content(content)
    
    # Setup PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Setup styles
    styles = getSampleStyleSheet()
    font_name = setup_fonts()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor='black'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=12,
        spaceAfter=10,
        spaceBefore=15,
        textColor='black'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        spaceAfter=6,
        textColor='black'
    )
    
    question_style = ParagraphStyle(
        'Question',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=11,
        spaceAfter=8,
        spaceBefore=8,
        textColor='black'
    )
    
    # Build story
    story = []
    
    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 20))
    
    # Process content
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            story.append(Spacer(1, 6))
            i += 1
            continue
        
        # Check for section headers (lines with === or ---)
        if i + 1 < len(lines) and lines[i + 1].strip().startswith('='):
            story.append(Paragraph(line, heading_style))
            story.append(Spacer(1, 10))
            i += 2
            continue
        elif i + 1 < len(lines) and lines[i + 1].strip().startswith('-'):
            story.append(Paragraph(line, question_style))
            i += 2
            continue
        
        # Regular content
        if line.startswith('**') and line.endswith('**'):
            # Instructions or important notes
            clean_line = line.replace('**', '')
            story.append(Paragraph(f"<b>{clean_line}</b>", normal_style))
        elif '：' in line or ':' in line:
            # Form fields
            story.append(Paragraph(line, normal_style))
        elif line.startswith('  □') or line.startswith('- □'):
            # Multiple choice options
            story.append(Paragraph(line, normal_style))
        elif line.startswith('###') or line.startswith('##'):
            # Questions
            clean_line = line.replace('###', '').replace('##', '').strip()
            story.append(Paragraph(f"<b>{clean_line}</b>", question_style))
        else:
            # Regular text
            story.append(Paragraph(line, normal_style))
        
        i += 1
    
    # Add footer
    story.append(Spacer(1, 30))
    footer_text = "香港浸会大学语言中心 | Language Centre, Hong Kong Baptist University"
    story.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF created: {output_path}")

def main():
    """Main function to generate all PDFs"""
    
    base_dir = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports"
    
    questionnaires = [
        {
            'md_file': 'Student_AI_Literacy_Questionnaire.md',
            'pdf_file': 'Student_AI_Literacy_Questionnaire.pdf',
            'title': '小学生人工智能素养评估问卷\nPrimary School Students AI Literacy Assessment Questionnaire'
        },
        {
            'md_file': 'Teacher_Satisfaction_Questionnaire.md', 
            'pdf_file': 'Teacher_Satisfaction_Questionnaire.pdf',
            'title': '教师对志愿服务学习教学项目满意度调查问卷\nTeacher Satisfaction Survey for Volunteering Service-Learning Teaching Program'
        }
    ]
    
    print("🔄 Converting questionnaires to PDF format...")
    print("=" * 60)
    
    success_count = 0
    
    for q in questionnaires:
        md_path = os.path.join(base_dir, q['md_file'])
        pdf_path = os.path.join(base_dir, q['pdf_file'])
        
        if not os.path.exists(md_path):
            print(f"❌ Markdown file not found: {md_path}")
            continue
        
        try:
            create_pdf_questionnaire(md_path, pdf_path, q['title'])
            success_count += 1
        except Exception as e:
            print(f"❌ Error creating PDF for {q['md_file']}: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"✨ Conversion complete! Successfully created {success_count}/{len(questionnaires)} PDF files.")
    
    if success_count > 0:
        print("\n📄 Generated PDF files:")
        for q in questionnaires:
            pdf_path = os.path.join(base_dir, q['pdf_file'])
            if os.path.exists(pdf_path):
                print(f"  • {q['pdf_file']}")
        
        print("\n📝 Usage:")
        print("  • Student AI Literacy Questionnaire: Use for pre/post assessment")
        print("  • Teacher Satisfaction Questionnaire: Use for program evaluation")

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print("❌ Missing required package. Please install reportlab:")
        print("pip install reportlab")
        print(f"Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
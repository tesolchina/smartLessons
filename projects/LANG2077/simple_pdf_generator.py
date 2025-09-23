#!/usr/bin/env python3
"""
Simple PDF generator for questionnaires using markdown to HTML to PDF
Alternative approach without complex dependencies
"""

import os
import sys
import subprocess
import tempfile

def markdown_to_html(md_content, title):
    """Convert markdown content to HTML"""
    
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        h3 {{
            color: #34495e;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        .form-field {{
            border-bottom: 1px dotted #ccc;
            display: inline-block;
            min-width: 200px;
            margin: 0 5px;
        }}
        .checkbox {{
            margin-right: 10px;
        }}
        .question {{
            margin: 15px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-left: 3px solid #e9ecef;
        }}
        .options {{
            margin-left: 20px;
            margin-top: 8px;
        }}
        .instructions {{
            background-color: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 0.9em;
        }}
        @media print {{
            body {{ margin: 0; }}
            .page-break {{ page-break-before: always; }}
        }}
    </style>
</head>
<body>
"""
    
    # Process markdown content
    lines = md_content.split('\n')
    html_content = ""
    
    for line in lines:
        line = line.strip()
        
        if not line:
            html_content += "<br>"
            continue
            
        # Skip markdown metadata
        if line.startswith('#') and ('questionnaire' in line.lower() or 'survey' in line.lower()):
            html_content += f"<h1>{line.replace('#', '').strip()}</h1>"
            continue
            
        # Headers
        if line.startswith('### '):
            html_content += f"<h3>{line.replace('### ', '')}</h3>"
        elif line.startswith('## '):
            html_content += f"<h2>{line.replace('## ', '')}</h2>"
        elif line.startswith('# '):
            continue  # Skip single # as they're usually duplicates
            
        # Instructions and bold text
        elif line.startswith('**') and line.endswith('**'):
            text = line.replace('**', '')
            html_content += f'<div class="instructions"><strong>{text}</strong></div>'
            
        # Form fields
        elif '___' in line:
            form_line = line.replace('___________________________', '<span class="form-field">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>')
            form_line = form_line.replace('___________', '<span class="form-field">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>')
            html_content += f"<p>{form_line}</p>"
            
        # Checkbox options
        elif line.startswith('- □') or line.startswith('□'):
            clean_line = line.replace('- □', '').replace('□', '').strip()
            html_content += f'<div class="options"><span class="checkbox">☐</span>{clean_line}</div>'
            
        # Regular paragraphs
        else:
            if line:
                html_content += f"<p>{line}</p>"
    
    # Close HTML
    html_content += """
<div class="footer">
    <p>香港浸会大学语文中心 | Language Centre, Hong Kong Baptist University<br>
    LANG2077 Language Skills for Human-AI Partnership: Customizing Chatbots to Empower Communities</p>
</div>
</body>
</html>
"""
    
    return html_template + html_content

def html_to_pdf_weasyprint(html_content, output_path):
    """Convert HTML to PDF using weasyprint (if available)"""
    try:
        import weasyprint
        weasyprint.HTML(string=html_content).write_pdf(output_path)
        return True
    except ImportError:
        return False

def html_to_pdf_system(html_content, output_path):
    """Convert HTML to PDF using system tools"""
    
    # Try different system commands
    commands = [
        # macOS built-in (if available)
        ['wkhtmltopdf', '--page-size', 'A4', '--encoding', 'UTF-8', '-', output_path],
        # Chrome headless (if available)
        ['google-chrome', '--headless', '--disable-gpu', '--print-to-pdf=' + output_path, '--virtual-time-budget=10000', 'data:text/html;charset=utf-8,' + html_content.replace(' ', '%20')],
    ]
    
    for cmd in commands:
        try:
            if cmd[0] == 'wkhtmltopdf':
                process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(input=html_content.encode('utf-8'))
                if process.returncode == 0:
                    return True
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    return True
        except FileNotFoundError:
            continue
        except Exception:
            continue
    
    return False

def create_text_version(md_content, output_path):
    """Create a formatted text version as fallback"""
    
    # Clean markdown
    lines = md_content.split('\n')
    text_content = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            text_content.append('')
            continue
            
        # Clean headers
        if line.startswith('#'):
            clean_line = line.replace('#', '').strip()
            text_content.append('')
            text_content.append(clean_line)
            text_content.append('=' * len(clean_line))
            
        # Clean formatting
        elif line.startswith('**') and line.endswith('**'):
            text_content.append(line.replace('**', ''))
            
        else:
            text_content.append(line)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\\n'.join(text_content))
    
    return True

def main():
    """Main function"""
    
    base_dir = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports"
    
    questionnaires = [
        {
            'md_file': 'Student_AI_Literacy_Questionnaire.md',
            'title': '小学生人工智能素养评估问卷 - Primary School Students AI Literacy Assessment Questionnaire'
        },
        {
            'md_file': 'Teacher_Satisfaction_Questionnaire.md',
            'title': '教师满意度调查问卷 - Teacher Satisfaction Survey'
        }
    ]
    
    print("🔄 Converting questionnaires to PDF format...")
    print("=" * 60)
    
    for q in questionnaires:
        md_path = os.path.join(base_dir, q['md_file'])
        
        if not os.path.exists(md_path):
            print(f"❌ File not found: {md_path}")
            continue
            
        # Read markdown content
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html_content = markdown_to_html(md_content, q['title'])
        
        # Try to create PDF
        base_name = q['md_file'].replace('.md', '')
        html_path = os.path.join(base_dir, f"{base_name}.html")
        pdf_path = os.path.join(base_dir, f"{base_name}.pdf")
        txt_path = os.path.join(base_dir, f"{base_name}_formatted.txt")
        
        # Save HTML version
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ HTML created: {base_name}.html")
        
        # Try PDF conversion
        pdf_success = False
        
        # Try weasyprint first
        pdf_success = html_to_pdf_weasyprint(html_content, pdf_path)
        
        if not pdf_success:
            # Try system commands
            pdf_success = html_to_pdf_system(html_content, pdf_path)
        
        if pdf_success:
            print(f"✅ PDF created: {base_name}.pdf")
        else:
            print(f"⚠️  PDF creation failed for {base_name}, creating formatted text version...")
            if create_text_version(md_content, txt_path):
                print(f"✅ Formatted text created: {base_name}_formatted.txt")
    
    print("\\n" + "=" * 60)
    print("✨ Conversion process completed!")
    print("\\n📄 Available formats:")
    print("  • HTML files: Can be opened in browser and printed to PDF")
    print("  • PDF files: Ready for distribution (if PDF generation succeeded)")
    print("  • Text files: Formatted fallback versions")
    
    print("\\n💡 Tip: If PDF creation failed, you can:")
    print("  1. Open the HTML file in your browser")
    print("  2. Use browser's 'Print to PDF' function")
    print("  3. Install wkhtmltopdf: brew install wkhtmltopdf")

if __name__ == "__main__":
    main()
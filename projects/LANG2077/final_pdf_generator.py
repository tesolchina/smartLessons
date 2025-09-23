#!/usr/bin/env python3
"""
Final PDF generator using browser automation
This will open the HTML files in a browser and save as PDF
"""

import os
import time
import subprocess
from pathlib import Path

def convert_html_to_pdf_via_browser(html_file_path, pdf_output_path):
    """Convert HTML to PDF using browser print function"""
    
    # Try Chrome/Chromium headless
    chrome_commands = [
        'google-chrome',
        'chromium-browser', 
        'chromium',
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    ]
    
    for chrome_cmd in chrome_commands:
        try:
            # Check if Chrome is available
            if chrome_cmd.startswith('/Applications'):
                if not os.path.exists(chrome_cmd):
                    continue
            else:
                result = subprocess.run(['which', chrome_cmd], capture_output=True)
                if result.returncode != 0:
                    continue
            
            # Convert HTML file path to file:// URL
            html_url = f"file://{os.path.abspath(html_file_path)}"
            
            # Chrome headless PDF generation
            cmd = [
                chrome_cmd,
                '--headless',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--print-to-pdf=' + pdf_output_path,
                '--print-to-pdf-no-header',
                '--virtual-time-budget=10000',
                html_url
            ]
            
            print(f"Trying: {chrome_cmd}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(pdf_output_path):
                return True
            else:
                print(f"Chrome command failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"Chrome command timed out")
            continue
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"Error with {chrome_cmd}: {e}")
            continue
    
    return False

def create_instruction_file():
    """Create instruction file for manual PDF creation"""
    
    instruction_content = """# PDF Creation Instructions | PDF生成说明

## English Instructions

### Method 1: Using Browser (Recommended)
1. Open the HTML files in your web browser:
   - Student_AI_Literacy_Questionnaire.html
   - Teacher_Satisfaction_Questionnaire.html

2. Print to PDF:
   - Press Cmd+P (Mac) or Ctrl+P (Windows)
   - Select "Save as PDF" or "Print to PDF"
   - Choose appropriate paper size (A4 recommended)
   - Save with desired filename

### Method 2: Using Online Converters
1. Visit an online HTML to PDF converter
2. Upload the HTML files
3. Download the generated PDFs

## 中文说明

### 方法一：使用浏览器（推荐）
1. 在网页浏览器中打开HTML文件：
   - Student_AI_Literacy_Questionnaire.html
   - Teacher_Satisfaction_Questionnaire.html

2. 打印为PDF：
   - 按下 Cmd+P (Mac) 或 Ctrl+P (Windows)
   - 选择"保存为PDF"或"打印为PDF"
   - 选择合适的纸张大小（推荐A4）
   - 保存为所需文件名

### 方法二：使用在线转换器
1. 访问在线HTML转PDF转换器
2. 上传HTML文件
3. 下载生成的PDF文件

## Files Generated | 生成的文件

- ✅ Student_AI_Literacy_Questionnaire.html (Ready for PDF conversion)
- ✅ Teacher_Satisfaction_Questionnaire.html (Ready for PDF conversion)
- ✅ Student_AI_Literacy_Questionnaire_formatted.txt (Text backup)
- ✅ Teacher_Satisfaction_Questionnaire_formatted.txt (Text backup)

## Quality Note | 质量说明

The HTML files are professionally formatted with:
- Proper Chinese font support
- Print-friendly styling
- Clear section breaks
- Form fields and checkboxes

HTML文件已进行专业格式化，具备：
- 适当的中文字体支持
- 打印友好的样式设计
- 清晰的章节分隔
- 表单字段和复选框
"""
    
    instruction_path = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports/PDF_Creation_Instructions.md"
    
    with open(instruction_path, 'w', encoding='utf-8') as f:
        f.write(instruction_content)
    
    return instruction_path

def main():
    """Main function"""
    
    base_dir = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports"
    
    html_files = [
        'Student_AI_Literacy_Questionnaire.html',
        'Teacher_Satisfaction_Questionnaire.html'
    ]
    
    print("🔄 Attempting PDF conversion using browser automation...")
    print("=" * 60)
    
    success_count = 0
    
    for html_file in html_files:
        html_path = os.path.join(base_dir, html_file)
        pdf_path = os.path.join(base_dir, html_file.replace('.html', '.pdf'))
        
        if not os.path.exists(html_path):
            print(f"❌ HTML file not found: {html_file}")
            continue
        
        print(f"Converting: {html_file}")
        
        if convert_html_to_pdf_via_browser(html_path, pdf_path):
            print(f"✅ PDF created: {html_file.replace('.html', '.pdf')}")
            success_count += 1
        else:
            print(f"⚠️  Automated PDF creation failed for: {html_file}")
    
    # Create instruction file
    instruction_path = create_instruction_file()
    
    print("\\n" + "=" * 60)
    print(f"✨ PDF conversion attempt completed!")
    print(f"📊 Successfully converted: {success_count}/{len(html_files)} files")
    
    if success_count < len(html_files):
        print("\\n📋 Manual PDF creation instructions have been created:")
        print(f"   📄 {os.path.basename(instruction_path)}")
        print("\\n💡 To create PDFs manually:")
        print("   1. Open the HTML files in your browser")
        print("   2. Use Cmd+P (Mac) or Ctrl+P (Windows)")
        print("   3. Select 'Save as PDF'")
    
    print("\\n📁 Available files:")
    for file in os.listdir(base_dir):
        if file.endswith(('.html', '.pdf', '.txt')) and ('Student_AI_Literacy' in file or 'Teacher_Satisfaction' in file):
            print(f"   📄 {file}")

if __name__ == "__main__":
    main()
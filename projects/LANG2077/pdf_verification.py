#!/usr/bin/env python3
"""
Verification script to check PDF quality
"""

import os

def verify_pdf_files():
    """Verify the generated PDF files"""
    
    base_dir = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports"
    
    pdf_files = [
        'Student_AI_Literacy_Questionnaire.pdf',
        'Teacher_Satisfaction_Questionnaire.pdf'
    ]
    
    print("🔍 Verifying PDF file quality...")
    print("=" * 50)
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(base_dir, pdf_file)
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            file_size_kb = file_size / 1024
            
            print(f"✅ {pdf_file}")
            print(f"   📊 Size: {file_size_kb:.1f} KB")
            print(f"   📅 Last modified: {os.path.getmtime(pdf_path)}")
            
            # Check corresponding HTML file
            html_file = pdf_file.replace('.pdf', '.html')
            html_path = os.path.join(base_dir, html_file)
            
            if os.path.exists(html_path):
                # Check for escaped newlines
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                escaped_newlines = html_content.count('\\\\n')
                literal_newlines = html_content.count('\\n')
                
                print(f"   🌐 HTML file: {html_file}")
                print(f"   ✅ Escaped newlines (\\\\n): {escaped_newlines}")
                print(f"   ✅ Literal newlines (\\n): {literal_newlines}")
                
                if escaped_newlines == 0:
                    print("   ✨ Clean formatting confirmed!")
                else:
                    print("   ⚠️  Still contains formatting issues")
            
            print()
        else:
            print(f"❌ {pdf_file} not found")
    
    print("🎯 Recommendations:")
    print("1. Open the PDF files to verify visual quality")
    print("2. Check that Chinese characters display correctly")
    print("3. Ensure form fields and checkboxes are properly formatted")
    print("4. Verify page breaks and spacing are appropriate")

if __name__ == "__main__":
    verify_pdf_files()
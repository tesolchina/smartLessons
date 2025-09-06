#!/usr/bin/env python3
"""
Extract text content from GCAP 3226 syllabus PDF
"""

import PyPDF2
import sys
from pathlib import Path

def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def main():
    pdf_path = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226/course_materials/syllabus/GCAP3226_syllabus.pdf"
    
    if not Path(pdf_path).exists():
        print(f"PDF file not found: {pdf_path}")
        return
    
    print("Extracting text from GCAP 3226 syllabus...")
    text = extract_pdf_text(pdf_path)
    
    # Save extracted text
    output_path = Path(pdf_path).parent / "syllabus_extracted.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Text extracted and saved to: {output_path}")
    
    # Print first 500 characters for preview
    print("\n=== SYLLABUS PREVIEW ===")
    print(text[:1000])

if __name__ == "__main__":
    main()

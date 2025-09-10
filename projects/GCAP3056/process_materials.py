#!/usr/bin/env python3
"""
GCAP 3056 PDF Processing and LLM Summary Pipeline
Convert PDFs to Markdown and generate clean summaries using LLM
"""

import os
import sys
from pathlib import Path
import json
import subprocess
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_directories():
    """Create necessary directories for processing"""
    
    base_dir = Path("./materials")
    
    directories = [
        base_dir / "md_converted",
        base_dir / "llm_summaries",
        base_dir / "processed_outputs"
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        logger.info(f"✅ Directory ready: {directory}")
    
    return directories

def convert_pdf_to_markdown(pdf_path: Path, output_dir: Path) -> Path:
    """Convert PDF to Markdown using various methods"""
    
    logger.info(f"🔄 Converting PDF: {pdf_path.name}")
    
    # Output markdown file
    md_file = output_dir / f"{pdf_path.stem}.md"
    
    try:
        # Method 1: Try using pandoc if available
        result = subprocess.run([
            'pandoc', 
            str(pdf_path), 
            '-t', 'markdown',
            '-o', str(md_file)
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and md_file.exists():
            logger.info(f"✅ Pandoc conversion successful: {md_file.name}")
            return md_file
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        logger.warning("⚠️ Pandoc not available or failed, trying alternative method")
    
    try:
        # Method 2: Try using pdfplumber (if available)
        import pdfplumber
        
        text_content = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_content.append(f"## Page {page_num}\n\n{text}\n\n")
                    
        if text_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(f"# {pdf_path.stem}\n\n")
                f.write("".join(text_content))
            
            logger.info(f"✅ pdfplumber conversion successful: {md_file.name}")
            return md_file
            
    except ImportError:
        logger.warning("⚠️ pdfplumber not available")
    except Exception as e:
        logger.error(f"❌ pdfplumber failed: {e}")
    
    # Method 3: Create placeholder file for manual processing
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# {pdf_path.stem}\n\n")
        f.write("*This file needs manual OCR processing*\n\n")
        f.write(f"Source: {pdf_path.name}\n")
        f.write(f"Conversion needed: Use external OCR tool\n")
    
    logger.warning(f"⚠️ Created placeholder file: {md_file.name}")
    return md_file

def generate_llm_summary(md_file: Path, output_dir: Path) -> Path:
    """Generate LLM summary of markdown content"""
    
    logger.info(f"🤖 Generating LLM summary for: {md_file.name}")
    
    # Read markdown content
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        logger.error(f"❌ Failed to read {md_file.name}: {e}")
        return None
    
    # Create summary file
    summary_file = output_dir / f"{md_file.stem}_summary.md"
    
    # For now, create structured summary template
    # TODO: Integrate with actual LLM API (OpenRouter, etc.)
    
    summary_content = f"""# LLM Summary: {md_file.stem}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Source:** {md_file.name}

## 📋 Key Points

*[LLM-generated key points would go here]*

## 🎯 Main Themes

*[LLM-identified main themes would go here]*

## 📖 Summary

*[LLM-generated concise summary would go here]*

## 🔗 GCAP 3056 Relevance

*[How this content relates to course objectives]*

---

## Original Content Preview

{content[:1000]}{'...' if len(content) > 1000 else ''}

---

**Processing Status:** Template created - needs LLM integration
**Next Steps:** 
1. Integrate OpenRouter API
2. Generate actual summaries
3. Extract course-relevant insights
"""
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    logger.info(f"✅ Summary template created: {summary_file.name}")
    return summary_file

def create_course_overview(processed_files: list, output_dir: Path) -> Path:
    """Create comprehensive course overview from all processed materials"""
    
    logger.info("📚 Creating comprehensive course overview")
    
    overview_file = output_dir / "GCAP3056_Materials_Overview.md"
    
    content = f"""# GCAP 3056: Taking a Stand - Materials Overview

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Documents Processed:** {len(processed_files)}

## 🎯 Course Resources Summary

### 📄 Processed Documents

"""
    
    for i, (pdf_file, md_file, summary_file) in enumerate(processed_files, 1):
        content += f"""
#### {i}. {pdf_file.stem}
- **Source PDF:** `{pdf_file.name}`
- **Markdown:** `{md_file.name}`
- **Summary:** `{summary_file.name if summary_file else 'Not generated'}`
- **Status:** {'✅ Processed' if summary_file else '⚠️ Needs processing'}

"""
    
    content += f"""

## 🚀 Next Steps for Course Preparation

### Immediate Actions:
1. **Review all summaries** for Week 2 content
2. **Extract key examples** for student demonstrations  
3. **Identify assignment materials** from processed documents
4. **Create reading assignments** based on summaries

### LLM Integration Tasks:
1. Set up OpenRouter API connection
2. Generate actual content summaries
3. Extract course-relevant insights
4. Create student-friendly materials

### Additional Resources Integration:
- **Gamma Slides:** https://gamma.app/docs/GCAP-3056-Taking-a-Stand-xztj8pkoylxq8pe?mode=doc
- **YouTube Award Video:** https://www.youtube.com/embed/0_GDNV8Mklc?rel=0
- **LegCo Document:** Needs OCR processing
- **Week 1 Transcript:** Already processed

## 📋 Materials Categories

### Course Structure & Syllabus
- GCAP3056-syllabus.pdf
- GCAP-3056-Taking-a-Stand.pdf

### Methodology & Engagement
- Engaging-the-Legco.pdf
- Public-conversations-with-the-HK-government.pdf
- Highlights-of-the-course-1-Request-info-from-the-government...pdf
- Highlights-of-the-course-2-Express-viewpoints-through-SCMP...pdf

### Success Examples
- Letter-published-on-120th-anniversary-of-SCMP.pdf
- How to write so the Hong Kong government will listen (LinkedIn article)

Ready for Week 2 preparation! 🎓
"""
    
    with open(overview_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info(f"✅ Course overview created: {overview_file.name}")
    return overview_file

def main():
    """Main processing pipeline"""
    
    print("=== GCAP 3056 PDF Processing Pipeline ===")
    print()
    
    # Setup directories
    md_dir, summary_dir, output_dir = setup_directories()
    
    # Find all PDF files
    materials_dir = Path("./materials")
    pdf_files = list(materials_dir.glob("*.pdf"))
    
    if not pdf_files:
        logger.error("❌ No PDF files found in materials directory")
        return
    
    logger.info(f"📄 Found {len(pdf_files)} PDF files to process")
    
    processed_files = []
    
    # Process each PDF
    for pdf_file in pdf_files:
        logger.info(f"\n🔄 Processing: {pdf_file.name}")
        
        # Convert to Markdown
        md_file = convert_pdf_to_markdown(pdf_file, md_dir)
        
        # Generate summary
        summary_file = generate_llm_summary(md_file, summary_dir)
        
        processed_files.append((pdf_file, md_file, summary_file))
        
        logger.info(f"✅ Completed: {pdf_file.name}")
    
    # Create comprehensive overview
    overview_file = create_course_overview(processed_files, output_dir)
    
    print(f"\n🎉 Processing Complete!")
    print(f"📄 Processed {len(processed_files)} documents")
    print(f"📂 Outputs in: materials/processed_outputs/")
    print(f"📋 Overview: {overview_file.name}")
    print(f"\n🚀 Ready for Week 2 course preparation!")

if __name__ == "__main__":
    main()

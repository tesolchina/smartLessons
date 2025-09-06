#!/usr/bin/env python3
"""
GCAP 3226 Course Materials Downloader
=====================================

This script downloads HTML course materials from the GitHub repository 
and converts them to markdown format for local use.

Repository: https://github.com/tesolchina/smartLessons/tree/main/GCAP3226
Target: /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226/course_materials/resources/readings
"""

import requests
import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html2text
from urllib.parse import urljoin, urlparse
import json
import time

class GCAP3226Downloader:
    def __init__(self):
        self.base_url = "https://raw.githubusercontent.com/tesolchina/smartLessons/main/"
        self.github_url = "https://github.com/tesolchina/smartLessons/tree/main/"
        self.output_dir = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226/course_materials/resources/readings")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GCAP3226-Course-Materials-Downloader/1.0'
        })
        
        # HTML to Markdown converter setup
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.ignore_emphasis = False
        self.h2t.body_width = 0  # No line wrapping
        
        # Course materials structure
        self.materials = {
            # Main course files
            "GCAP3226/intro.html": "01_course_introduction.md",
            "GCAP3226/intro_temp.html": "01_course_introduction_temp.md", 
            
            # Week 1 materials
            "GCAP3226/week1/index.html": "02_week1_overview.md",
            "GCAP3226/week1/css/styles.css": "02_week1_styles.css",
            
            # Clean AI tutor versions (newer)
            "clean-aitutor-v2/GCAP3226/intro.html": "03_clean_intro.md",
            "clean-aitutor-v2/GCAP3226/intro_temp.html": "03_clean_intro_temp.md",
            "clean-aitutor-v2/GCAP3226/week1/index.html": "04_clean_week1.md",
            "clean-aitutor-v2/GCAP3226/week1/css/styles.css": "04_clean_week1_styles.css",
            "clean-aitutor-v2/GCAP3226/week1/js/course-app.js": "04_clean_week1_app.js",
            "clean-aitutor-v2/GCAP3226/week1/interactiveLecture.html": "05_interactive_lecture.md",
            
            # Language centre versions
            "LANG0036/week1/index.html": "06_lang0036_week1.md",
        }

    def download_file(self, relative_path, output_filename):
        """Download a file from the GitHub repository."""
        url = self.base_url + relative_path
        print(f"📥 Downloading: {relative_path}")
        print(f"    URL: {url}")
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            content = response.text
            file_extension = Path(relative_path).suffix.lower()
            
            # Determine output path
            output_path = self.output_dir / output_filename
            
            if file_extension in ['.html', '.htm']:
                # Convert HTML to Markdown
                markdown_content = self.convert_html_to_markdown(content, relative_path)
                output_path = output_path.with_suffix('.md')
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                    
            elif file_extension in ['.css', '.js']:
                # Keep CSS and JS as-is but add markdown formatting
                formatted_content = self.format_code_file(content, file_extension)
                output_path = output_path.with_suffix('.md')
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                    
            else:
                # Save other files as-is
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            print(f"    ✅ Saved: {output_path}")
            return True
            
        except requests.RequestException as e:
            print(f"    ❌ Error downloading {relative_path}: {e}")
            return False
        except Exception as e:
            print(f"    ❌ Error processing {relative_path}: {e}")
            return False

    def convert_html_to_markdown(self, html_content, source_path):
        """Convert HTML content to markdown with enhanced formatting."""
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title
        title = "GCAP 3226 Course Material"
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        elif soup.h1:
            title = soup.h1.get_text().strip()
        
        # Create header
        markdown_header = f"""# {title}

**Source:** {source_path}  
**Repository:** https://github.com/tesolchina/smartLessons/tree/main/{source_path}  
**Downloaded:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        # Convert to markdown
        markdown_body = self.h2t.handle(html_content)
        
        # Clean up markdown
        markdown_body = self.clean_markdown(markdown_body)
        
        return markdown_header + markdown_body

    def format_code_file(self, content, file_extension):
        """Format CSS/JS files with markdown syntax highlighting."""
        
        lang = 'css' if file_extension == '.css' else 'javascript'
        
        header = f"""# GCAP 3226 {lang.upper()} File

**Downloaded:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

```{lang}
{content}
```
"""
        return header

    def clean_markdown(self, markdown_text):
        """Clean up converted markdown text."""
        
        # Remove excessive blank lines
        markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)
        
        # Fix heading spacing
        markdown_text = re.sub(r'\n(#+.*?)\n', r'\n\n\1\n\n', markdown_text)
        
        # Clean up list formatting
        markdown_text = re.sub(r'\n(\s*[\*\-\+]\s)', r'\n\1', markdown_text)
        
        # Remove trailing whitespace
        lines = [line.rstrip() for line in markdown_text.split('\n')]
        markdown_text = '\n'.join(lines)
        
        return markdown_text

    def create_index_file(self):
        """Create an index file listing all downloaded materials."""
        
        index_content = f"""# GCAP 3226 Course Materials Index

**Downloaded:** {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Source Repository:** https://github.com/tesolchina/smartLessons/tree/main/GCAP3226

## 📚 Available Materials

### Course Introduction & Overview
- [Course Introduction](01_course_introduction.md) - Main course overview page
- [Course Introduction (Template)](01_course_introduction_temp.md) - Template version
- [Clean Introduction](03_clean_intro.md) - Enhanced clean version  
- [Clean Introduction (Template)](03_clean_intro_temp.md) - Clean template version

### Week 1 Materials
- [Week 1 Overview](02_week1_overview.md) - Week 1 main content
- [Week 1 Styles](02_week1_styles.md) - CSS styling for Week 1
- [Clean Week 1](04_clean_week1.md) - Enhanced Week 1 version
- [Clean Week 1 Styles](04_clean_week1_styles.md) - Enhanced CSS styling
- [Clean Week 1 App](04_clean_week1_app.md) - JavaScript functionality
- [Interactive Lecture](05_interactive_lecture.md) - Interactive lecture content

### Additional Resources  
- [Language Centre Week 1](06_lang0036_week1.md) - Language centre version

## 🎯 Course Focus

**Course Title:** Empowering Citizens through Data - Participatory Policy Analysis for Hong Kong

**Key Learning Areas:**
- Data governance and policy analysis
- Hong Kong government data systems  
- Participatory policy development
- AI-assisted research methods
- Citizen empowerment through data literacy

## 📋 Assessment Structure

**Individual Work (50%):**
- In-class exercises: 10%
- Reflective essays: 20% 
- Human-AI collaboration report: 20%

**Group Work (50%):**
- In-class presentations: 20%
- Final report & poster: 30%

## 🗓️ Course Schedule

- **When:** Tuesdays 9:30-12:20
- **Duration:** 14 weeks
- **Format:** Interactive lectures + group projects
- **Instructor:** Dr. Simon Wang (Language Centre, HKBU)

---

*This index was automatically generated by the GCAP3226 Course Materials Downloader.*
"""
        
        index_path = self.output_dir / "README.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"📋 Created index file: {index_path}")

    def run(self):
        """Download all course materials."""
        
        print("🚀 Starting GCAP 3226 Course Materials Download")
        print(f"📁 Output directory: {self.output_dir}")
        print("="*60)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Track success/failure
        successful_downloads = 0
        failed_downloads = 0
        
        # Download all materials
        for source_path, output_name in self.materials.items():
            success = self.download_file(source_path, output_name)
            if success:
                successful_downloads += 1
            else:
                failed_downloads += 1
            
            # Small delay between requests
            time.sleep(0.5)
        
        # Create index file
        self.create_index_file()
        
        # Summary
        print("="*60)
        print(f"✅ Successfully downloaded: {successful_downloads} files")
        print(f"❌ Failed downloads: {failed_downloads} files")
        print(f"📁 All materials saved to: {self.output_dir}")
        
        if successful_downloads > 0:
            print("\n🎉 Course materials successfully downloaded and converted to markdown!")
            print("📖 Check the README.md file for a complete index of materials.")
        else:
            print("\n⚠️  No materials were successfully downloaded. Check your internet connection.")

def main():
    """Main execution function."""
    downloader = GCAP3226Downloader()
    downloader.run()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Academic Slide Generator CLI - HTML/CSS Based
Creates professional presentation slides without external APIs
Created: September 6, 2025
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

class AcademicSlideGenerator:
    """Generate academic presentation slides using HTML/CSS"""
    
    def __init__(self):
        self.output_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/generated_slides"
        Path(self.output_dir).mkdir(exist_ok=True)
        
        # HKBU Brand Colors
        self.brand_colors = {
            "primary": "#800020",     # Burgundy
            "secondary": "#FFD700",   # Gold
            "text": "#333333",        # Dark gray
            "background": "#FFFFFF",  # White
            "accent": "#F5F5F5"       # Light gray
        }
    
    def create_base_template(self):
        """Create base HTML template for slides"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            background: linear-gradient(135deg, {primary} 0%, {secondary} 100%);
            color: {text};
            line-height: 1.6;
        }
        
        .slide-container {
            width: 100vw;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 40px;
            background: {background};
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .slide {
            max-width: 1200px;
            width: 100%;
            text-align: center;
            padding: 60px;
        }
        
        .slide-header {
            border-bottom: 3px solid {primary};
            padding-bottom: 30px;
            margin-bottom: 50px;
        }
        
        .slide-title {
            font-size: 3.5rem;
            font-weight: bold;
            color: {primary};
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        .slide-subtitle {
            font-size: 2rem;
            color: {text};
            font-weight: 300;
            margin-bottom: 10px;
        }
        
        .slide-content {
            font-size: 1.5rem;
            line-height: 1.8;
            margin-bottom: 40px;
        }
        
        .slide-footer {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 1.2rem;
            color: {secondary};
            font-weight: 500;
        }
        
        .logo {
            position: absolute;
            top: 30px;
            right: 30px;
            width: 120px;
            height: auto;
        }
        
        .bullet-list {
            text-align: left;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .bullet-item {
            font-size: 1.8rem;
            margin: 20px 0;
            padding: 15px 25px;
            background: {accent};
            border-left: 5px solid {primary};
            border-radius: 5px;
            transition: transform 0.3s ease;
        }
        
        .bullet-item:hover {
            transform: translateX(10px);
            background: white;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .highlight {
            color: {primary};
            font-weight: bold;
        }
        
        .secondary-highlight {
            color: {secondary};
            font-weight: bold;
        }
        
        @media print {
            .slide-container {
                page-break-after: always;
                height: 100vh;
                margin: 0;
            }
        }
        
        @media (max-width: 768px) {
            .slide-title { font-size: 2.5rem; }
            .slide-subtitle { font-size: 1.5rem; }
            .slide-content { font-size: 1.2rem; }
            .bullet-item { font-size: 1.4rem; }
        }
    </style>
</head>
<body>
    {content}
    
    <script>
        // Navigation with arrow keys
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide-container');
        
        function showSlide(n) {
            slides.forEach(slide => slide.style.display = 'none');
            if (slides[n]) {
                slides[n].style.display = 'flex';
                currentSlide = n;
            }
        }
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowRight' || e.key === ' ') {
                if (currentSlide < slides.length - 1) {
                    showSlide(currentSlide + 1);
                }
            } else if (e.key === 'ArrowLeft') {
                if (currentSlide > 0) {
                    showSlide(currentSlide - 1);
                }
            }
        });
        
        // Show first slide initially
        if (slides.length > 0) {
            showSlide(0);
        }
        
        // Add slide numbers
        slides.forEach((slide, index) => {
            const slideNumber = document.createElement('div');
            slideNumber.style.position = 'absolute';
            slideNumber.style.bottom = '10px';
            slideNumber.style.right = '30px';
            slideNumber.style.fontSize = '1rem';
            slideNumber.style.color = '#666';
            slideNumber.textContent = `${index + 1} / ${slides.length}`;
            slide.appendChild(slideNumber);
        });
    </script>
</body>
</html>
"""
    
    def generate_lang2077_slides(self):
        """Generate LANG 2077 presentation slides"""
        
        print("🎓 Generating LANG 2077 Academic Presentation...")
        
        slides_data = {
            "title": "LANG 2077 Course Introduction",
            "slides": [
                {
                    "type": "title",
                    "title": "LANG 2077",
                    "subtitle": "Language Skills for human-AI partnership:",
                    "content": "Customizing Chatbots to Empower Communities",
                    "footer": "Dr. Simon Wang | Language Centre, HKBU | Fall 2025"
                },
                {
                    "type": "content",
                    "title": "What Students Will Learn",
                    "subtitle": "Learning Outcomes & Objectives",
                    "content": [
                        "<span class='highlight'>Language Skills Development</span>",
                        "• Academic communication in AI contexts",
                        "• Technical writing for AI applications", 
                        "• Cross-cultural communication strategies",
                        "",
                        "<span class='highlight'>AI Partnership Skills</span>",
                        "• Understanding AI capabilities and limitations",
                        "• Effective human-AI collaboration",
                        "• Prompt engineering and chatbot interaction",
                        "",
                        "<span class='highlight'>Community Engagement</span>",
                        "• Identifying community needs",
                        "• Designing solutions with community partners",
                        "• Presenting results to stakeholders"
                    ]
                },
                {
                    "type": "content", 
                    "title": "Empowering Communities Through AI",
                    "subtitle": "Service Learning Component",
                    "content": [
                        "<span class='secondary-highlight'>Community Partner Collaboration</span>",
                        "• Work with local NGOs and organizations",
                        "• Identify real community challenges", 
                        "• Co-design AI-enhanced solutions",
                        "",
                        "<span class='secondary-highlight'>Chatbot Customization Projects</span>",
                        "• Develop task-specific chatbots",
                        "• Adapt language for target audiences",
                        "• Test and iterate with community feedback",
                        "",
                        "<span class='secondary-highlight'>Student Deliverables & Impact</span>",
                        "• Final presentation to community partners",
                        "• Reflection essays on AI ethics",
                        "• Portfolio of customized AI tools"
                    ]
                }
            ]
        }
        
        # Generate slides HTML
        slides_html = self._generate_slides_html(slides_data)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"LANG2077_slides_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(slides_html)
        
        print(f"✅ Slides generated successfully!")
        print(f"📁 File: {filepath}")
        print(f"🌐 Open in browser to view/present")
        print(f"🖨️  Use browser's Print to PDF for sharing")
        
        return filepath
    
    def _generate_slides_html(self, slides_data):
        """Generate complete HTML for slides"""
        
        template = self.create_base_template()
        slides_content = ""
        
        for i, slide in enumerate(slides_data["slides"]):
            slide_html = f"""
            <div class="slide-container">
                <div class="slide">
                    <div class="slide-header">
                        <h1 class="slide-title">{slide['title']}</h1>
                        {f'<h2 class="slide-subtitle">{slide["subtitle"]}</h2>' if slide.get('subtitle') else ''}
                    </div>
                    <div class="slide-content">
                        {self._format_slide_content(slide['content'])}
                    </div>
                    {f'<div class="slide-footer">{slide["footer"]}</div>' if slide.get('footer') else ''}
                </div>
            </div>
            """
            slides_content += slide_html
        
        # Format template with brand colors and content
        formatted_html = template.format(
            title=slides_data["title"],
            content=slides_content,
            **self.brand_colors
        )
        
        return formatted_html
    
    def _format_slide_content(self, content):
        """Format slide content based on type"""
        if isinstance(content, str):
            return f'<p style="font-size: 2.2rem; font-weight: 300;">{content}</p>'
        elif isinstance(content, list):
            formatted_items = []
            for item in content:
                if item.strip() == "":
                    formatted_items.append('<div style="margin: 30px 0;"></div>')
                elif item.startswith("•"):
                    formatted_items.append(f'<div class="bullet-item">{item}</div>')
                else:
                    formatted_items.append(f'<div class="bullet-item" style="background: white; border-left: none; font-weight: bold;">{item}</div>')
            return f'<div class="bullet-list">{"".join(formatted_items)}</div>'
        
        return str(content)
    
    def create_custom_slides(self, title, slides_content):
        """Create custom slides from provided content"""
        
        print(f"🎨 Creating custom presentation: {title}")
        
        slides_data = {
            "title": title,
            "slides": slides_content
        }
        
        slides_html = self._generate_slides_html(slides_data)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_title.replace(' ', '_')}_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(slides_html)
        
        print(f"✅ Custom slides created!")
        print(f"📁 File: {filepath}")
        
        return filepath
    
    def create_collaboration_package(self, slides_file, collaborators):
        """Create a collaboration package with sharing instructions"""
        
        base_name = os.path.splitext(os.path.basename(slides_file))[0]
        package_dir = os.path.join(self.output_dir, f"{base_name}_collaboration")
        os.makedirs(package_dir, exist_ok=True)
        
        # Copy slides file to package
        import shutil
        shutil.copy2(slides_file, package_dir)
        
        # Create sharing instructions
        sharing_file = os.path.join(package_dir, "SHARING_INSTRUCTIONS.md")
        
        with open(sharing_file, 'w', encoding='utf-8') as f:
            f.write(f"""# Presentation Collaboration Package
            
## 📋 Files Included
- `{os.path.basename(slides_file)}` - Main presentation (HTML)

## 🚀 How to Share & Collaborate

### Option 1: Email Sharing
1. **Attach the HTML file** to email
2. **Recipients can open** directly in any browser
3. **No software required** - works on any device

### Option 2: Cloud Storage (Recommended)
1. **Upload to Google Drive/Dropbox/OneDrive**
2. **Share link** with collaborators: {', '.join(collaborators)}
3. **Collaborators can download** and view locally
4. **For editing**: Share source content separately

### Option 3: Web Hosting
1. **Upload to website/server** 
2. **Share direct URL** for instant access
3. **Works on mobile devices**

## 🎯 Collaboration Workflow

### For Collaborators:
1. **Download/Access** the HTML file
2. **Open in browser** (Chrome, Firefox, Safari, Edge)
3. **Use arrow keys** to navigate slides
4. **Print to PDF** for sharing/reviewing
5. **Send feedback** via email or comments

### For Content Changes:
- Contact presentation creator: Dr. Simon Wang (simonwang@hkbu.edu.hk)
- Provide specific slide numbers and suggested changes
- Changes will be implemented and new version shared

## 🖥️ Presentation Features
- **Keyboard Navigation**: Arrow keys or spacebar
- **Responsive Design**: Works on all screen sizes
- **Print Ready**: Use browser Print → Save as PDF
- **No Internet Required**: Works offline after download

## 📧 Collaborator List
{chr(10).join(f"- {email}" for email in collaborators)}

## 💡 Tips
- **Fullscreen Mode**: Press F11 for presentation mode
- **Mobile Viewing**: Swipe left/right on touchscreens  
- **Sharing**: File is completely self-contained
- **Editing**: Contact creator for content modifications
""")
        
        print(f"📦 Collaboration package created: {package_dir}")
        print(f"📧 Ready to share with: {', '.join(collaborators)}")
        
        return package_dir

def main():
    parser = argparse.ArgumentParser(description="Academic Slide Generator CLI")
    parser.add_argument("--type", choices=["lang2077", "custom"], default="lang2077",
                       help="Type of presentation to create")
    parser.add_argument("--title", help="Custom presentation title")
    parser.add_argument("--collaborators", nargs="*", default=[],
                       help="Email addresses of collaborators")
    parser.add_argument("--open", action="store_true", help="Open generated slides in browser")
    
    args = parser.parse_args()
    
    generator = AcademicSlideGenerator()
    
    if args.type == "lang2077":
        slides_file = generator.generate_lang2077_slides()
    else:
        if not args.title:
            args.title = input("Enter presentation title: ")
        # For custom slides, you could add more input methods
        print("Custom slide creation - extend this for your needs")
        return
    
    # Create collaboration package if collaborators specified
    if args.collaborators:
        generator.create_collaboration_package(slides_file, args.collaborators)
    
    # Open in browser if requested
    if args.open:
        import webbrowser
        webbrowser.open(f"file://{slides_file}")
        print("🌐 Slides opened in browser")

if __name__ == "__main__":
    main()

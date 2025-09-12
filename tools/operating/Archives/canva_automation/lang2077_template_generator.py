#!/usr/bin/env python3
"""
LANG 2077 Slides Template Generator
Creates structured content for manual use in presentation software
Created: September 6, 2025
"""

import os
import json
from datetime import datetime

def create_slides_template():
    """Create LANG 2077 slides template"""
    
    print("🎓 LANG 2077 Course Slides Template Generator")
    print("=" * 50)
    
    # Define slide content
    slides_data = {
        "presentation_title": "LANG 2077 Course Introduction",
        "course_full_name": "Language Skills for human-AI partnership: Customizing Chatbots to Empower Communities",
        "instructor": "Dr. Simon Wang",
        "department": "Language Centre, HKBU",
        "semester": "Fall 2025",
        "slides": [
            {
                "slide_number": 1,
                "title": "LANG 2077",
                "subtitle": "Language Skills for human-AI partnership:",
                "main_content": "Customizing Chatbots to Empower Communities",
                "footer": "Dr. Simon Wang | Language Centre, HKBU | Fall 2025",
                "design_notes": [
                    "Use HKBU official colors (burgundy and gold)",
                    "Include HKBU logo in top right corner",
                    "Large, bold title font",
                    "Professional academic layout"
                ]
            },
            {
                "slide_number": 2,
                "title": "What Students Will Learn",
                "subtitle": "Learning Outcomes & Objectives",
                "main_content": [
                    "• Language Skills Development",
                    "  - Academic communication in AI contexts",
                    "  - Technical writing for AI applications",
                    "  - Cross-cultural communication strategies",
                    "",
                    "• AI Partnership Skills", 
                    "  - Understanding AI capabilities and limitations",
                    "  - Effective human-AI collaboration",
                    "  - Prompt engineering and chatbot interaction",
                    "",
                    "• Community Engagement",
                    "  - Identifying community needs",
                    "  - Designing solutions with community partners",
                    "  - Presenting results to stakeholders"
                ],
                "design_notes": [
                    "Use bullet points with indentation",
                    "Color-code different skill categories", 
                    "Include icons for each skill area",
                    "Keep text readable but comprehensive"
                ]
            },
            {
                "slide_number": 3,
                "title": "Empowering Communities Through AI",
                "subtitle": "Service Learning Component",
                "main_content": [
                    "• Community Partner Collaboration",
                    "  - Work with local NGOs and organizations",
                    "  - Identify real community challenges",
                    "  - Co-design AI-enhanced solutions",
                    "",
                    "• Chatbot Customization Projects",
                    "  - Develop task-specific chatbots",
                    "  - Adapt language for target audiences",
                    "  - Test and iterate with community feedback",
                    "",
                    "• Student Deliverables & Impact",
                    "  - Final presentation to community partners",
                    "  - Reflection essays on AI ethics",
                    "  - Portfolio of customized AI tools"
                ],
                "design_notes": [
                    "Include community partner logos if available",
                    "Use images showing collaboration",
                    "Highlight the service learning aspect",
                    "Show the practical impact of the course"
                ]
            }
        ],
        "additional_slides": [
            {
                "suggested_slide": "Course Structure & Timeline",
                "content": "Week-by-week breakdown of activities and assignments"
            },
            {
                "suggested_slide": "Assessment Methods",
                "content": "Grading rubrics, participation expectations, project criteria"
            },
            {
                "suggested_slide": "Required Resources",
                "content": "Textbooks, software, online platforms students will use"
            },
            {
                "suggested_slide": "Contact Information",
                "content": "Office hours, email, course website, support resources"
            }
        ]
    }
    
    # Create output directory
    output_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG2077/presentation_materials"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as JSON for programmatic use
    json_file = os.path.join(output_dir, "lang2077_slides_data.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(slides_data, f, indent=2, ensure_ascii=False)
    
    # Create markdown version for easy reading
    md_file = os.path.join(output_dir, "lang2077_slides_content.md")
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# {slides_data['presentation_title']}\n\n")
        f.write(f"**Course:** {slides_data['course_full_name']}  \n")
        f.write(f"**Instructor:** {slides_data['instructor']}  \n")
        f.write(f"**Department:** {slides_data['department']}  \n")
        f.write(f"**Semester:** {slides_data['semester']}  \n\n")
        f.write("---\n\n")
        
        for slide in slides_data['slides']:
            f.write(f"## Slide {slide['slide_number']}: {slide['title']}\n\n")
            if slide.get('subtitle'):
                f.write(f"**{slide['subtitle']}**\n\n")
            
            if isinstance(slide['main_content'], list):
                for item in slide['main_content']:
                    f.write(f"{item}\n")
            else:
                f.write(f"{slide['main_content']}\n")
            
            f.write(f"\n*Footer: {slide.get('footer', '')}*\n\n")
            
            f.write("### Design Notes:\n")
            for note in slide['design_notes']:
                f.write(f"- {note}\n")
            f.write("\n---\n\n")
        
        f.write("## Additional Suggested Slides:\n\n")
        for suggestion in slides_data['additional_slides']:
            f.write(f"- **{suggestion['suggested_slide']}**: {suggestion['content']}\n")
    
    # Create PowerPoint template instructions
    ppt_file = os.path.join(output_dir, "powerpoint_creation_guide.md")
    with open(ppt_file, 'w', encoding='utf-8') as f:
        f.write("# PowerPoint Creation Guide for LANG 2077\n\n")
        f.write("## Quick Setup Instructions:\n\n")
        f.write("1. **Open PowerPoint** and create a new presentation\n")
        f.write("2. **Choose HKBU template** or professional academic theme\n")
        f.write("3. **Set slide size** to 16:9 widescreen format\n")
        f.write("4. **Apply consistent fonts**: Calibri or Arial for readability\n\n")
        
        f.write("## Color Scheme (HKBU Brand):\n")
        f.write("- **Primary**: Burgundy (#800020)\n")
        f.write("- **Secondary**: Gold (#FFD700)\n")
        f.write("- **Text**: Dark gray (#333333)\n")
        f.write("- **Background**: White or light cream\n\n")
        
        f.write("## Slide-by-Slide Instructions:\n\n")
        
        for slide in slides_data['slides']:
            f.write(f"### Slide {slide['slide_number']}: {slide['title']}\n")
            f.write("**Layout**: Title and Content\n\n")
            f.write("**Content to add:**\n")
            
            if isinstance(slide['main_content'], list):
                for item in slide['main_content']:
                    if item.strip():  # Skip empty lines
                        f.write(f"- {item.strip()}\n")
            else:
                f.write(f"- {slide['main_content']}\n")
            
            f.write(f"\n**Footer text**: {slide.get('footer', '')}\n\n")
            f.write("**Visual elements to add:**\n")
            for note in slide['design_notes']:
                f.write(f"- {note}\n")
            f.write("\n---\n\n")
    
    # Create Canva template instructions
    canva_file = os.path.join(output_dir, "canva_creation_guide.md")
    with open(canva_file, 'w', encoding='utf-8') as f:
        f.write("# Canva Creation Guide for LANG 2077\n\n")
        f.write("## Getting Started:\n\n")
        f.write("1. **Go to canva.com** and log in with simonwang@hkbu.edu.hk\n")
        f.write("2. **Click 'Create a design'** → Choose 'Presentation'\n")
        f.write("3. **Search templates** for 'academic presentation' or 'university'\n")
        f.write("4. **Select a professional template** with burgundy/gold colors if available\n\n")
        
        f.write("## Template Customization:\n\n")
        f.write("### Slide 1 - Title Slide:\n")
        f.write(f"- **Main title**: LANG 2077\n")
        f.write(f"- **Subtitle**: Language Skills for human-AI partnership: Customizing Chatbots to Empower Communities\n")
        f.write(f"- **Footer**: Dr. Simon Wang | Language Centre, HKBU | Fall 2025\n")
        f.write("- **Add HKBU logo** in top-right corner\n\n")
        
        for slide in slides_data['slides'][1:]:  # Skip slide 1 as it's already covered
            f.write(f"### Slide {slide['slide_number']} - {slide['title']}:\n")
            f.write(f"- **Title**: {slide['title']}\n")
            if slide.get('subtitle'):
                f.write(f"- **Subtitle**: {slide['subtitle']}\n")
            f.write("- **Content**:\n")
            
            if isinstance(slide['main_content'], list):
                for item in slide['main_content']:
                    if item.strip():
                        f.write(f"  {item}\n")
            else:
                f.write(f"  {slide['main_content']}\n")
            f.write("\n")
    
    print(f"✅ Slides template created successfully!")
    print(f"📁 Files saved in: {output_dir}")
    print("\n📋 Created files:")
    print(f"  - {os.path.basename(json_file)} (structured data)")
    print(f"  - {os.path.basename(md_file)} (readable content)")
    print(f"  - {os.path.basename(ppt_file)} (PowerPoint guide)")
    print(f"  - {os.path.basename(canva_file)} (Canva guide)")
    
    print("\n🎯 Next steps:")
    print("  1. Review the content in the markdown file")
    print("  2. Choose PowerPoint or Canva for creation")
    print("  3. Follow the respective creation guide")
    print("  4. Customize colors and add HKBU branding")
    print("  5. Add any additional slides as needed")
    
    return True

if __name__ == "__main__":
    create_slides_template()

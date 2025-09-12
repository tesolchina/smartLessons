#!/usr/bin/env python3
"""
GCAP3056 Moodle Forum Post Generator
Creates rich HTML content for Moodle forums based on course materials and expectations
"""

import os
from datetime import datetime
from pathlib import Path

def read_file_content(file_path):
    """Read content from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def generate_course_expectations_recap():
    """Generate HTML recap of course expectations and week 2 overview"""
    
    # Read the course expectations transcript
    expectations_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3056/materials/Course Expectations Overview_otter_ai.txt"
    expectations_content = read_file_content(expectations_file)
    
    # Read syllabus content
    syllabus_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3056/materials/md_converted/GCAP3056-syllabus.md"
    syllabus_content = read_file_content(syllabus_file)
    
    # Read course overview
    overview_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3056/materials/md_converted/GCAP-3056-Taking-a-Stand.md"
    overview_content = read_file_content(overview_file)
    
    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GCAP3056 Week 2: Media and Research Literature - Course Expectations Recap</title>
</head>
<body>
    <div style="font-family: Arial, sans-serif; font-size: 16px; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px;">
        
        <h1 style="color: #d73527; font-size: 24px; text-align: center; border-bottom: 3px solid #d73527; padding-bottom: 10px;">
            📚 GCAP3056: Taking a Stand - Week 2 Overview
        </h1>
        
        <div style="background-color: #f8f9fa; padding: 15px; border-left: 5px solid #007bff; margin-bottom: 20px;">
            <h2 style="color: #007bff; font-size: 20px; margin-top: 0;">🎯 Course Foundation Recap</h2>
            <p style="font-size: 16px; margin-bottom: 15px;">
                Last week, we established the fundamental premise of our course: <strong>government as a necessary evil</strong>. While the state imposes taxation and potentially restricts our freedom, it provides essential services like police protection, schools, and hospitals that we depend on.
            </p>
            <div style="background-color: white; padding: 10px; border-radius: 5px; margin: 10px 0;">
                <strong>💡 Key Concept:</strong> Since we are taxpayers, we have a <em>service provider-customer relationship</em> with the government, which creates the foundation for accountability.
            </div>
        </div>

        <h2 style="color: #28a745; font-size: 20px; border-bottom: 2px solid #28a745; padding-bottom: 5px;">
            🔍 How We Hold Government Accountable
        </h2>
        
        <div style="display: grid; grid-template-columns: 1fr; gap: 15px; margin-bottom: 20px;">
            <div style="background-color: #e8f5e8; padding: 15px; border-radius: 8px;">
                <h3 style="color: #155724; font-size: 18px; margin-top: 0;">📋 Code on Access to Information</h3>
                <p style="margin-bottom: 10px;">
                    Our primary tool for requesting information from the government. This enables us to:
                </p>
                <ul style="margin-left: 20px;">
                    <li>Email government staff directly using the publicly available government directory</li>
                    <li>Raise questions about policies and decisions</li>
                    <li>Gather evidence for our research projects</li>
                </ul>
            </div>
            
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px;">
                <h3 style="color: #856404; font-size: 18px; margin-top: 0;">🗳️ Alternative Forms of Accountability</h3>
                <p>While we cannot vote out the Hong Kong government directly:</p>
                <ul style="margin-left: 20px;">
                    <li><strong>"Voting by feet"</strong> - the option to relocate (though not practical for everyone)</li>
                    <li><strong>Active engagement</strong> through information requests and public discourse</li>
                    <li><strong>Media participation</strong> - writing letters to editors and opinion pieces</li>
                </ul>
            </div>
        </div>

        <h2 style="color: #dc3545; font-size: 20px; border-bottom: 2px solid #dc3545; padding-bottom: 5px;">
            📅 Assessment Timeline & Expectations
        </h2>
        
        <div style="background-color: #f8d7da; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #721c24; font-size: 18px; margin-top: 0;">🎯 <strong>Week 10 = Key Deadline</strong></h3>
            <p style="font-size: 16px; margin-bottom: 10px;">
                <strong>Goal:</strong> Complete all major components by Week 10, leaving the final weeks for refinement and bonus work.
            </p>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr; gap: 15px; margin-bottom: 20px;">
            <div style="background-color: #d4edda; padding: 15px; border-radius: 8px;">
                <h4 style="color: #155724; font-size: 17px; margin-top: 0;">1. 📝 Argumentative Research Paper</h4>
                <ul style="margin-left: 20px; font-size: 15px;">
                    <li><strong>Length:</strong> ~500 words per student</li>
                    <li><strong>Target:</strong> Draft complete by Week 10</li>
                    <li><strong>Focus:</strong> Policy recommendations based on research insights</li>
                </ul>
            </div>
            
            <div style="background-color: #d1ecf1; padding: 15px; border-radius: 8px;">
                <h4 style="color: #0c5460; font-size: 17px; margin-top: 0;">2. 🤝 Community Engagement Portfolio (40%)</h4>
                <ul style="margin-left: 20px; font-size: 15px;">
                    <li>Evidence of contacting government officials</li>
                    <li>Evidence of writing for the public</li>
                    <li>Documentation of community engagement activities</li>
                    <li><strong>Target:</strong> Draft by Week 10</li>
                </ul>
            </div>
            
            <div style="background-color: #f3e5f5; padding: 15px; border-radius: 8px;">
                <h4 style="color: #6f42c1; font-size: 17px; margin-top: 0;">3. 📖 Reflective Learning Journal</h4>
                <ul style="margin-left: 20px; font-size: 15px;">
                    <li>Weekly Moodle forum responses</li>
                    <li>Interactions with AI chatbot discussions</li>
                    <li>Ongoing reflection on learning process</li>
                </ul>
            </div>
        </div>

        <h2 style="color: #6c757d; font-size: 20px; border-bottom: 2px solid #6c757d; padding-bottom: 5px;">
            🚀 Week 2 Focus: Media and Research Literature
        </h2>
        
        <div style="background-color: #e9ecef; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <p style="font-size: 16px; margin-bottom: 10px;">
                This week, we begin <strong>topic exploration</strong> and establish our <strong>project-based learning approach</strong>. 
                Rather than traditional lectures, we'll focus on:
            </p>
            <ul style="margin-left: 20px; font-size: 15px;">
                <li>Small group meetings and collaborative work</li>
                <li>Hands-on project development</li>
                <li>Connecting academic research with real-world policy issues</li>
                <li>Building skills in accessing and analyzing government information</li>
            </ul>
        </div>

        <div style="background-color: #fff; border: 2px solid #007bff; padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: #007bff; font-size: 19px; margin-top: 0;">📢 Expected Outcomes</h3>
            <p style="font-size: 16px; margin-bottom: 15px;">
                <strong>Grade Distribution Target:</strong>
            </p>
            <div style="font-size: 15px; text-align: left; margin: 0 auto; display: inline-block;">
                <p>🅰️ <strong>20-25%</strong> of students → A range</p>
                <p>🅱️ <strong>~70%</strong> of students → B range</p>
                <p>🅲️ <strong>Small percentage</strong> → C range</p>
            </div>
            <p style="font-size: 14px; margin-top: 15px; font-style: italic;">
                Meeting Week 10 deadlines typically ensures B-range performance, with A-range grades for exceptional work in final weeks.
            </p>
        </div>

        <div style="margin-top: 30px; padding: 15px; background-color: #f1f3f4; border-radius: 8px; text-align: center;">
            <p style="font-size: 14px; color: #666; margin: 0;">
                <strong>Discussion Questions for This Week:</strong><br>
                • How can we effectively use the Code on Access to Information?<br>
                • What social issues in Hong Kong deserve our research attention?<br>
                • How can academic research translate into practical policy recommendations?
            </p>
        </div>
        
        <footer style="margin-top: 20px; text-align: center; font-size: 14px; color: #666; border-top: 1px solid #dee2e6; padding-top: 15px;">
            <p>GCAP3056: Taking a Stand - Dr. Simon Wang<br>
            Generated on {datetime.now().strftime('%B %d, %Y')}</p>
        </footer>
        
    </div>
</body>
</html>"""

    return html_content

def save_html_post(content, filename):
    """Save HTML content to file"""
    output_path = f"/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3056/moodle_posts/{filename}"
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ HTML post saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return None

def main():
    """Main execution function"""
    print("🚀 Generating GCAP3056 Moodle Forum Post...")
    print("=" * 50)
    
    # Generate the HTML content
    html_content = generate_course_expectations_recap()
    
    # Save the HTML file
    filename = f"week2_course_expectations_recap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    output_path = save_html_post(html_content, filename)
    
    if output_path:
        print(f"\n📄 Moodle Forum Post Generated Successfully!")
        print(f"📍 Location: {output_path}")
        print(f"\n📋 Content Overview:")
        print("   ✓ Course foundation recap")
        print("   ✓ Government accountability methods")
        print("   ✓ Assessment timeline and expectations")
        print("   ✓ Week 2 focus areas")
        print("   ✓ Grade distribution overview")
        print(f"\n🎨 Features:")
        print("   • Large, readable font (16px base)")
        print("   • Color-coded sections for easy navigation")
        print("   • Moodle-compatible HTML (no external CSS/JS)")
        print("   • Mobile-responsive design")
        print("   • Professional formatting with clear hierarchy")

if __name__ == "__main__":
    main()

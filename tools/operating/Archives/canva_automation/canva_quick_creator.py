#!/usr/bin/env python3
"""
Canva Quick Creator - Manual Guidance
Opens Canva and provides step-by-step instructions for slide creation
No browser automation - just guided manual process
Created: September 6, 2025
"""

import webbrowser
import time
from datetime import datetime

class CanvaQuickCreator:
    """Guided Canva slide creation without automation"""
    
    def __init__(self):
        self.email = "simonwang@hkbu.edu.hk"
        self.course = "LANG 2077"
        
    def create_lang2077_slides(self):
        """Guide user through LANG 2077 slide creation"""
        
        print("🎓 LANG 2077 Quick Slide Creator")
        print("=" * 40)
        print()
        
        # Step 1: Open Canva
        print("📋 Step 1: Opening Canva Presentations")
        print("🌐 Opening https://www.canva.com/create/presentations/")
        webbrowser.open("https://www.canva.com/create/presentations/")
        
        input("Press Enter after Canva loads...")
        
        # Step 2: Login guidance
        print("\n📋 Step 2: Login to Canva")
        print(f"👤 Use email: {self.email}")
        print("🔐 Enter your password when prompted")
        
        input("Press Enter after logging in...")
        
        # Step 3: Template selection
        print("\n📋 Step 3: Choose Template")
        print("🔍 In the search box, type: 'academic presentation university'")
        print("🎨 Select a professional template with clean design")
        print("💡 Look for templates with:")
        print("   • Clean, professional layout")
        print("   • Title slide format")
        print("   • Good contrast for text")
        
        input("Press Enter after selecting template...")
        
        # Step 4: Content guidance
        print("\n📋 Step 4: Add Content")
        print("📝 Replace the template text with LANG 2077 content:")
        print()
        
        # Slide 1 content
        print("🔸 SLIDE 1 (Title):")
        print("   Title: LANG 2077")
        print("   Subtitle: Language Skills for human-AI partnership:")
        print("   Main text: Customizing Chatbots to Empower Communities")
        print("   Footer: Dr. Simon Wang | Language Centre, HKBU | Fall 2025")
        print()
        
        input("Press Enter after completing Slide 1...")
        
        # Guide for adding more slides
        print("\n📋 Step 5: Add More Slides")
        print("➕ Click 'Add page' or '+' to create new slides")
        print()
        
        # Slide 2 content
        print("🔸 SLIDE 2:")
        print("   Title: What Students Will Learn")
        print("   Subtitle: Learning Outcomes & Objectives")
        print("   Content:")
        print("   • Language Skills Development")
        print("     - Academic communication in AI contexts")
        print("     - Technical writing for AI applications")
        print("   • AI Partnership Skills")
        print("     - Understanding AI capabilities and limitations") 
        print("     - Effective human-AI collaboration")
        print("   • Community Engagement")
        print("     - Identifying community needs")
        print("     - Designing solutions with community partners")
        print()
        
        input("Press Enter after completing Slide 2...")
        
        # Slide 3 content
        print("🔸 SLIDE 3:")
        print("   Title: Empowering Communities Through AI")
        print("   Subtitle: Service Learning Component")
        print("   Content:")
        print("   • Community Partner Collaboration")
        print("     - Work with local NGOs and organizations")
        print("     - Identify real community challenges")
        print("   • Chatbot Customization Projects")
        print("     - Develop task-specific chatbots")
        print("     - Adapt language for target audiences")
        print("   • Student Deliverables & Impact")
        print("     - Final presentation to community partners")
        print("     - Reflection essays on AI ethics")
        print()
        
        input("Press Enter after completing Slide 3...")
        
        # Step 6: Branding
        print("\n📋 Step 6: Apply HKBU Branding")
        print("🎨 Customize colors and branding:")
        print("   • Primary color: Burgundy (#800020)")
        print("   • Secondary color: Gold (#FFD700)")
        print("   • Add HKBU logo if available")
        print("   • Use professional fonts (Arial, Helvetica)")
        print()
        print("💡 To change colors:")
        print("   1. Select text or elements")
        print("   2. Click color picker") 
        print("   3. Enter hex codes above")
        
        input("Press Enter after applying branding...")
        
        # Step 7: Finalize
        print("\n📋 Step 7: Finalize Presentation")
        print("✅ Final checklist:")
        print("   □ All slide content added")
        print("   □ HKBU colors applied")
        print("   □ Consistent fonts throughout")
        print("   □ Logo added (if available)")
        print("   □ Spelling and grammar checked")
        
        # Step 8: Save and name
        print("\n📋 Step 8: Save Presentation")
        print("💾 Click on the title area (usually says 'Untitled Design')")
        print(f"📝 Rename to: LANG2077_Course_Introduction_{datetime.now().strftime('%Y%m%d')}")
        print("🔄 Canva auto-saves your work")
        
        input("Press Enter after saving...")
        
        # Completion
        print("\n🎉 LANG 2077 Slides Created Successfully!")
        print("📋 What you can do now:")
        print("   • Present directly from Canva")
        print("   • Download as PDF for sharing")
        print("   • Download as PowerPoint (.pptx)")
        print("   • Share link with colleagues for viewing")
        print("   • Duplicate for other courses")
        
        print(f"\n📧 Your slides are saved in your Canva account: {self.email}")
        print("🔗 Access anytime at: https://www.canva.com/")
        
        return True
    
    def quick_start_other_course(self, course_name):
        """Quick start for other courses"""
        
        print(f"🎓 {course_name} Quick Slide Creator")
        print("=" * 40)
        
        print("🌐 Opening Canva...")
        webbrowser.open("https://www.canva.com/create/presentations/")
        
        print(f"\n📝 Creating slides for: {course_name}")
        print("📋 Follow these steps:")
        print("1. Login with your account")
        print("2. Search for 'academic presentation' template") 
        print("3. Replace with your course content")
        print("4. Apply HKBU branding (burgundy #800020, gold #FFD700)")
        print("5. Save with course name and date")
        
        input("Press Enter when slides are ready...")
        print(f"✅ {course_name} slides created!")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Canva Quick Creator - Guided Manual Process")
    parser.add_argument("--course", default="LANG2077", help="Course name")
    
    args = parser.parse_args()
    
    creator = CanvaQuickCreator()
    
    if args.course.upper() == "LANG2077":
        creator.create_lang2077_slides()
    else:
        creator.quick_start_other_course(args.course)

if __name__ == "__main__":
    main()

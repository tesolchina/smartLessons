#!/usr/bin/env python3
"""
LANG 2077 Course Slides Creator
Specialized script for creating LANG 2077 course introduction slides
Created: September 6, 2025
"""

import os
import sys
import argparse

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_lang2077_slides(keep_open=False):
    """Create LANG 2077 course slides using Canva CLI"""
    
    print("🎓 LANG 2077 Course Slides Creator")
    print("=" * 50)
    
    # Slide content for LANG 2077
    slides_data = {
        "slide_1_content": [
            "LANG 2077",
            "Language Skills for human-AI partnership:",
            "Customizing Chatbots to Empower Communities", 
            "Dr. Simon Wang | Language Centre, HKBU | Fall 2025"
        ],
        "slide_2_content": [
            "What Students Will Learn",
            "• Language Skills Development",
            "• AI Partnership Skills",
            "• Community Engagement"
        ],
        "slide_3_content": [
            "Empowering Communities Through AI",
            "• Community Partner Collaboration", 
            "• Chatbot Customization Projects",
            "• Student Deliverables & Impact"
        ]
    }
    
    try:
        # Import canva_cli here to handle missing dependencies gracefully
        try:
            from canva_cli import CanvaCLI
        except ImportError:
            print("❌ Canva CLI dependencies not installed.")
            print("📦 Please install dependencies first:")
            print("   cd /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation")
            print("   pip3 install -r requirements.txt")
            return False
        
        # Initialize Canva CLI
        canva = CanvaCLI()
        
        # Setup browser
        if not canva.setup_driver():
            return False
        
        # Login
        if not canva.login():
            return False
        
        # Create presentation design
        print("📊 Creating presentation for LANG 2077...")
        if not canva.create_design("presentation", "academic university course"):
            return False
        
        # Add slide 1 content
        print("📝 Adding Slide 1 content...")
        canva.add_text_to_design(slides_data["slide_1_content"])
        
        # Note: For multiple slides, this would need more sophisticated navigation
        # For now, we create the base presentation and user can duplicate/edit
        
        # Save the design
        canva.save_design("LANG2077_Course_Introduction_Slides")
        
        print("✅ LANG 2077 slides created successfully!")
        print("📋 Next steps:")
        print("   1. Open the created design in Canva")
        print("   2. Duplicate slides for additional content")
        print("   3. Add the remaining slide content:")
        print(f"      - Slide 2: {slides_data['slide_2_content']}")
        print(f"      - Slide 3: {slides_data['slide_3_content']}")
        print("   4. Add images and HKBU branding")
        print("   5. Adjust colors and formatting")
        
        if keep_open:
            input("Press Enter to close browser...")
        
        canva.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating LANG 2077 slides: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    import subprocess
    
    print("📦 Installing Canva CLI dependencies...")
    
    requirements_path = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/requirements.txt"
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="LANG 2077 Course Slides Creator")
    parser.add_argument("--install-deps", action="store_true", help="Install required dependencies")
    parser.add_argument("--keep-open", action="store_true", help="Keep browser open")
    
    args = parser.parse_args()
    
    if args.install_deps:
        if install_dependencies():
            print("🔄 Dependencies installed. Run the script again without --install-deps")
        return
    
    # Create LANG 2077 slides
    create_lang2077_slides(args.keep_open)

if __name__ == "__main__":
    main()

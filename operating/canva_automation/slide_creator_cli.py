#!/usr/bin/env python3
"""
Unified Slide Creation CLI - Multiple Output Formats
Create professional presentations without external APIs
Created: September 6, 2025
"""

import os
import sys
import argparse
from datetime import datetime

def show_available_methods():
    """Show all available slide creation methods"""
    print("🎯 Available Slide Creation Methods")
    print("=" * 50)
    print()
    print("1. 📊 PowerPoint CLI (Recommended)")
    print("   • Creates native .pptx files")
    print("   • Works with PowerPoint, Google Slides, Keynote")
    print("   • Real-time collaboration supported")
    print("   • Command: python3 powerpoint_cli.py")
    print()
    print("2. 🌐 HTML/CSS Generator")
    print("   • Creates interactive web presentations")
    print("   • Works in any browser")
    print("   • Keyboard navigation built-in")
    print("   • Command: python3 academic_slide_generator.py")
    print()
    print("3. 🤝 Collaboration Helper (No API needed)")
    print("   • Creates step-by-step guides")
    print("   • Email templates included")
    print("   • Works with manual Canva creation")
    print("   • Command: python3 canva_collaboration_helper.py")
    print()
    print("4. 📝 Template Generator")
    print("   • Creates structured content")
    print("   • Multiple format guides")
    print("   • Ready-to-use templates")
    print("   • Command: python3 lang2077_template_generator.py")

def check_dependencies():
    """Check which dependencies are available"""
    print("🔍 Checking Available Tools...")
    print()
    
    methods = []
    
    # Check PowerPoint CLI
    try:
        import pptx
        methods.append("✅ PowerPoint CLI - Ready")
        pptx_available = True
    except ImportError:
        methods.append("❌ PowerPoint CLI - Missing python-pptx")
        pptx_available = False
    
    # HTML generator is always available (no external deps)
    methods.append("✅ HTML/CSS Generator - Ready")
    
    # Collaboration helper is always available
    methods.append("✅ Collaboration Helper - Ready")
    
    # Template generator is always available
    methods.append("✅ Template Generator - Ready")
    
    for method in methods:
        print(f"   {method}")
    
    print()
    if not pptx_available:
        print("📦 To install PowerPoint support:")
        print("   pip3 install python-pptx")
        print()
    
    return pptx_available

def install_dependencies():
    """Install missing dependencies"""
    print("📦 Installing dependencies...")
    import subprocess
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
        print("✅ python-pptx installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install python-pptx")
        return False

def create_lang2077_slides_unified(format_type, collaborators=None, open_result=False):
    """Create LANG 2077 slides using specified format"""
    
    print(f"🎓 Creating LANG 2077 slides in {format_type} format...")
    
    if format_type == "powerpoint":
        try:
            from powerpoint_cli import PowerPointCLI
            ppt_cli = PowerPointCLI()
            result = ppt_cli.create_lang2077_presentation(collaborators)
            
            if open_result:
                import subprocess
                subprocess.run(["open", result])
            
            return result
        except ImportError:
            print("❌ PowerPoint CLI not available. Install python-pptx first.")
            return None
    
    elif format_type == "html":
        from academic_slide_generator import AcademicSlideGenerator
        generator = AcademicSlideGenerator()
        result = generator.generate_lang2077_slides()
        
        if collaborators:
            generator.create_collaboration_package(result, collaborators)
        
        if open_result:
            import webbrowser
            webbrowser.open(f"file://{result}")
        
        return result
    
    elif format_type == "template":
        from lang2077_template_generator import create_slides_template
        create_slides_template()
        return "Template created in presentation_materials/"
    
    elif format_type == "collaboration":
        from canva_collaboration_helper import create_lang2077_collaboration
        return create_lang2077_collaboration()

def main():
    parser = argparse.ArgumentParser(description="Unified Slide Creation CLI")
    parser.add_argument("--format", choices=["powerpoint", "html", "template", "collaboration"], 
                       default="powerpoint", help="Output format")
    parser.add_argument("--collaborators", nargs="*", default=[],
                       help="Email addresses of collaborators")
    parser.add_argument("--open", action="store_true", help="Open result after creation")
    parser.add_argument("--check", action="store_true", help="Check available methods")
    parser.add_argument("--install", action="store_true", help="Install missing dependencies")
    parser.add_argument("--list", action="store_true", help="List all available methods")
    
    args = parser.parse_args()
    
    if args.list:
        show_available_methods()
        return
    
    if args.check:
        check_dependencies()
        return
    
    if args.install:
        install_dependencies()
        return
    
    # Default collaborators for HKBU
    if not args.collaborators:
        args.collaborators = [
            "department.head@hkbu.edu.hk",
            "course.coordinator@hkbu.edu.hk",
            "teaching.assistant@hkbu.edu.hk"
        ]
    
    # Create slides
    result = create_lang2077_slides_unified(args.format, args.collaborators, args.open)
    
    if result:
        print()
        print("🎯 Next Steps:")
        print("1. Review the generated content")
        print("2. Share with collaborators if needed")
        print("3. Customize branding and colors")
        print("4. Present or distribute as needed")
        
        if args.collaborators:
            print()
            print("👥 Collaborators to notify:")
            for email in args.collaborators:
                print(f"   - {email}")

if __name__ == "__main__":
    main()

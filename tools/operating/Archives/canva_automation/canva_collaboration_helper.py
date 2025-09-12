#!/usr/bin/env python3
"""
Canva Collaboration Helper - No Browser Automation Required
Generates collaboration instructions and shareable templates
Created: September 6, 2025
"""

import os
import json
import webbrowser
from datetime import datetime

class CanvaCollaborationHelper:
    """Helper for Canva collaboration without browser automation"""
    
    def __init__(self):
        self.collaborators = []
        self.project_name = ""
        self.content_data = {}
    
    def create_collaboration_guide(self, project_name, collaborators, slide_content):
        """Create a step-by-step collaboration guide"""
        
        self.project_name = project_name
        self.collaborators = collaborators
        self.content_data = slide_content
        
        print(f"📋 Creating collaboration guide for {project_name}")
        print("=" * 50)
        
        # Create output directory
        output_dir = f"/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/collaboration_guides"
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        guide_file = os.path.join(output_dir, f"{project_name.lower()}_collaboration_guide_{timestamp}.md")
        
        # Generate collaboration guide
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(f"# {project_name} - Collaborative Presentation Guide\n\n")
            f.write(f"**Created:** {datetime.now().strftime('%B %d, %Y at %H:%M')}\n")
            f.write(f"**Project Lead:** Dr. Simon Wang (simonwang@hkbu.edu.hk)\n\n")
            
            # Step-by-step creation process
            f.write("## 🚀 Quick Start - Create & Share in Canva\n\n")
            f.write("### Step 1: Create the Presentation\n")
            f.write("1. Go to **[canva.com](https://www.canva.com)** and log in with `simonwang@hkbu.edu.hk`\n")
            f.write("2. Click **'Create a design'** → Choose **'Presentation'**\n")
            f.write("3. Search for **'academic presentation university'** template\n")
            f.write("4. Select a professional template with HKBU colors (burgundy/gold)\n\n")
            
            f.write("### Step 2: Add Content (Use the content below)\n")
            
            # Add slide content
            for i, slide in enumerate(slide_content.get('slides', []), 1):
                f.write(f"\n#### Slide {i}: {slide.get('title', f'Slide {i}')}\n")
                if slide.get('subtitle'):
                    f.write(f"**Subtitle:** {slide['subtitle']}\n\n")
                
                if isinstance(slide.get('main_content'), list):
                    f.write("**Content:**\n")
                    for item in slide['main_content']:
                        if item.strip():
                            f.write(f"- {item.strip()}\n")
                else:
                    f.write(f"**Content:** {slide.get('main_content', '')}\n")
                
                if slide.get('footer'):
                    f.write(f"\n*Footer: {slide['footer']}*\n")
                f.write("\n")
            
            f.write("### Step 3: Share with Collaborators\n")
            f.write("1. Click the **'Share'** button (top right)\n")
            f.write("2. Add each collaborator email:\n")
            
            for email in collaborators:
                f.write(f"   - `{email}` (Can edit)\n")
            
            f.write("\n3. **Optional:** Get shareable link for broader access\n")
            f.write("4. Click **'Send invitations'**\n\n")
            
            f.write("### Step 4: Collaborative Editing Instructions\n")
            f.write("**For Collaborators:**\n")
            f.write("- You'll receive an email invitation from Canva\n")
            f.write("- Click the link to open the presentation\n")
            f.write("- You can edit text, add images, change colors simultaneously\n")
            f.write("- All changes are saved automatically\n")
            f.write("- Use comments feature for discussions\n\n")
            
            # Collaboration workflow
            f.write("## 👥 Collaboration Workflow\n\n")
            f.write("### Roles & Responsibilities:\n")
            f.write(f"- **Project Lead:** {slide_content.get('instructor', 'Dr. Simon Wang')} - Overall coordination\n")
            
            role_assignments = [
                ("Content Review", collaborators[0] if len(collaborators) > 0 else "TBD"),
                ("Visual Design", collaborators[1] if len(collaborators) > 1 else "TBD"),
                ("Technical Review", collaborators[2] if len(collaborators) > 2 else "TBD"),
                ("Final Approval", "Dr. Simon Wang")
            ]
            
            for role, assignee in role_assignments:
                f.write(f"- **{role}:** {assignee}\n")
            
            f.write("\n### Timeline:\n")
            f.write("- **Day 1:** Initial content creation and sharing\n")
            f.write("- **Day 2-3:** Collaborative editing and content refinement\n")
            f.write("- **Day 4:** Visual design and HKBU branding\n")
            f.write("- **Day 5:** Final review and approval\n\n")
            
            # Technical details
            f.write("## 🔧 Technical Details\n\n")
            f.write("### HKBU Branding Guidelines:\n")
            f.write("- **Primary Color:** Burgundy (#800020)\n")
            f.write("- **Secondary Color:** Gold (#FFD700)\n")
            f.write("- **Fonts:** Professional (Calibri, Arial, or Canva equivalent)\n")
            f.write("- **Logo:** Add HKBU logo to all slides (top-right corner)\n\n")
            
            f.write("### Collaboration Features to Use:\n")
            f.write("- **Real-time editing:** Multiple people can edit simultaneously\n")
            f.write("- **Comments:** Use for feedback and discussions\n")
            f.write("- **Version history:** Access previous versions if needed\n")
            f.write("- **Permissions:** Everyone has edit access, project lead has admin access\n\n")
            
            # Contact information
            f.write("## 📞 Contact Information\n\n")
            f.write("**Questions or Issues:**\n")
            f.write("- Email: simonwang@hkbu.edu.hk\n")
            f.write("- Office: Language Centre, HKBU\n")
            f.write("- Phone: [Your phone number]\n\n")
            
            f.write("**Canva Support:**\n")
            f.write("- Help Center: help.canva.com\n")
            f.write("- Live Chat: Available in Canva interface\n\n")
            
            # Action items
            f.write("## ✅ Action Items Checklist\n\n")
            f.write("**For Project Lead (Dr. Simon Wang):**\n")
            f.write("- [ ] Create initial presentation in Canva\n")
            f.write("- [ ] Add basic content structure\n")
            f.write("- [ ] Send collaboration invitations\n")
            f.write("- [ ] Monitor progress and provide guidance\n\n")
            
            f.write("**For Each Collaborator:**\n")
            f.write("- [ ] Accept Canva invitation email\n")
            f.write("- [ ] Review assigned section\n")
            f.write("- [ ] Make necessary edits and improvements\n")
            f.write("- [ ] Add comments for discussion points\n")
            f.write("- [ ] Notify team when section is complete\n\n")
        
        # Create email template
        email_file = os.path.join(output_dir, f"{project_name.lower()}_invitation_email_{timestamp}.txt")
        self._create_invitation_email_template(email_file)
        
        # Generate summary
        print(f"✅ Collaboration guide created successfully!")
        print(f"📁 Files saved in: {output_dir}")
        print(f"📋 Guide file: {os.path.basename(guide_file)}")
        print(f"📧 Email template: {os.path.basename(email_file)}")
        
        return guide_file, email_file
    
    def _create_invitation_email_template(self, email_file):
        """Create email template for inviting collaborators"""
        
        with open(email_file, 'w', encoding='utf-8') as f:
            f.write(f"Subject: Collaboration Invitation - {self.project_name} Presentation\n\n")
            f.write("Dear Colleague,\n\n")
            f.write(f"You're invited to collaborate on the {self.project_name} presentation in Canva.\n\n")
            f.write("What you need to do:\n")
            f.write("1. Accept the Canva collaboration invitation (separate email)\n")
            f.write("2. Review the attached collaboration guide\n")
            f.write("3. Edit your assigned sections in the presentation\n")
            f.write("4. Use comments for any questions or suggestions\n\n")
            f.write("Timeline: We aim to complete this by [DATE]\n\n")
            f.write("The presentation covers:\n")
            
            for i, slide in enumerate(self.content_data.get('slides', []), 1):
                f.write(f"- Slide {i}: {slide.get('title', f'Slide {i}')}\n")
            
            f.write(f"\nIf you have any questions, please contact me at simonwang@hkbu.edu.hk\n\n")
            f.write("Best regards,\n")
            f.write(f"{self.content_data.get('instructor', 'Dr. Simon Wang')}\n")
            f.write(f"{self.content_data.get('department', 'Language Centre, HKBU')}\n")
    
    def open_canva_directly(self):
        """Open Canva in browser for manual creation"""
        print("🌐 Opening Canva in your browser...")
        webbrowser.open("https://www.canva.com/create/presentations/")
        print("✅ Canva opened - follow the collaboration guide to create and share!")

def create_lang2077_collaboration():
    """Create collaboration setup for LANG 2077 course"""
    
    print("🎓 LANG 2077 Collaborative Presentation Setup")
    print("=" * 50)
    
    # Course data
    project_name = "LANG2077_Course_Introduction"
    
    collaborators = [
        "department.head@hkbu.edu.hk",
        "course.coordinator@hkbu.edu.hk", 
        "teaching.assistant@hkbu.edu.hk",
        "admin.support@hkbu.edu.hk"
    ]
    
    slide_content = {
        "course_code": "LANG 2077",
        "course_title": "Language Skills for human-AI partnership: Customizing Chatbots to Empower Communities",
        "instructor": "Dr. Simon Wang",
        "department": "Language Centre, HKBU",
        "semester": "Fall 2025",
        "slides": [
            {
                "title": "LANG 2077",
                "subtitle": "Language Skills for human-AI partnership:",
                "main_content": "Customizing Chatbots to Empower Communities",
                "footer": "Dr. Simon Wang | Language Centre, HKBU | Fall 2025"
            },
            {
                "title": "What Students Will Learn",
                "subtitle": "Learning Outcomes & Objectives",
                "main_content": [
                    "• Language Skills Development",
                    "  - Academic communication in AI contexts",
                    "  - Technical writing for AI applications",
                    "• AI Partnership Skills", 
                    "  - Understanding AI capabilities and limitations",
                    "  - Effective human-AI collaboration",
                    "• Community Engagement",
                    "  - Identifying community needs",
                    "  - Designing solutions with community partners"
                ]
            },
            {
                "title": "Empowering Communities Through AI",
                "subtitle": "Service Learning Component",
                "main_content": [
                    "• Community Partner Collaboration",
                    "  - Work with local NGOs and organizations",
                    "• Chatbot Customization Projects", 
                    "  - Develop task-specific chatbots",
                    "• Student Deliverables & Impact",
                    "  - Final presentation to community partners"
                ]
            }
        ]
    }
    
    # Create collaboration helper
    helper = CanvaCollaborationHelper()
    guide_file, email_file = helper.create_collaboration_guide(project_name, collaborators, slide_content)
    
    print("\n🎯 Next Steps:")
    print("1. Review the collaboration guide")
    print("2. Open Canva manually to create the presentation")
    print("3. Use the email template to invite collaborators")
    print("4. Follow the step-by-step process in the guide")
    
    # Ask if user wants to open Canva now
    response = input("\n🌐 Open Canva in browser now? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        helper.open_canva_directly()
    
    return guide_file, email_file

if __name__ == "__main__":
    create_lang2077_collaboration()

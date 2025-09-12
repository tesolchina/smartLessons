#!/usr/bin/env python3
"""
Quick Email Draft for Service Learning Reply
Create a simple email draft file for replying to Nancy and Joshua
"""

import os
from datetime import datetime


def create_simple_draft():
    """Create a simple email draft."""
    
    google_slides_link = "https://docs.google.com/presentation/d/1_6aRzEFlUnvTPSSG5vtgFTKhxo5NpajnynDekjiiNgs/edit?usp=sharing"
    
    draft = f"""To: Nancy Guo <nancyguo@hkbu.edu.hk>, Joshua Chan <joshuachan@hkbu.edu.hk>
Subject: Re: Departmental Meeting - Service Learning Course - Google Slides Ready

Dear Nancy and Joshua,

Hope this finds you well!

I've created a collaborative Google Slides presentation for our joint Service Learning sharing session:

🔗 {google_slides_link}

**What's ready:**
• Title slide with all three presenters
• Your individual sections with placeholder content
• Professional HKBU design with colorful backgrounds
• Anyone with the link can edit

**Structure:**
1. Title - Service Learning Sharing Session
2. Dr. Joshua Chan - Service Learning Methods  
3. Dr. Nancy Guo - Language Learning & Impact
4. Dr. Simon Wang - LANG 2077 Integration
5. Discussion & Q&A

Please feel free to add your content to your respective sections. The slides are ready for collaborative editing before our departmental meeting.

Looking forward to our presentation!

Best,
Simon

---
Dr. Simon H. Wang
HKBU Language Centre
simonwang@hkbu.edu.hk"""

    # Save to desktop for easy access
    desktop_path = os.path.expanduser("~/Desktop")
    filename = f"Service_Learning_Email_Draft_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    filepath = os.path.join(desktop_path, filename)
    
    with open(filepath, 'w') as f:
        f.write(draft)
    
    print("📧 Service Learning Email Draft Created")
    print("=" * 40)
    print("✅ Draft saved to Desktop")
    print(f"📁 File: {filename}")
    print(f"🔗 Google Slides: {google_slides_link}")
    
    print("\n📋 Draft Content:")
    print("-" * 20)
    print(draft)
    
    print(f"\n💡 Next Steps:")
    print("1. Open the draft file on your Desktop")
    print("2. Copy the content")
    print("3. Create new email in Mail.app")
    print("4. Paste content and send")
    
    return filepath


if __name__ == "__main__":
    create_simple_draft()

#!/usr/bin/env python3
"""
Get Presentation Info
Get the details of the created presentation and set up sharing manually.
"""

def get_presentation_info():
    """Get info about the created presentation."""
    
    presentation_id = "1_6aRzEFlUnvTPSSG5vtgFTKhxo5NpajnynDekjiiNgs"
    presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    
    print("🎉 Your New Service Learning Presentation is Ready!")
    print("=" * 60)
    print(f"📄 Presentation ID: {presentation_id}")
    print(f"🔗 Link: {presentation_url}")
    print("\n📋 Slide Structure:")
    print("   1. Title slide - Service Learning Sharing Session")
    print("   2. Dr. Joshua Chan - Service Learning Methods")
    print("   3. Dr. Nancy Guo - Language Learning & Impact")
    print("   4. Dr. Simon Wang - LANG 2077 Integration")
    print("   5. Thank You & Discussion")
    
    print("\n🎨 Features Created:")
    print("   ✅ Professional title with all three presenters")
    print("   ✅ Colorful backgrounds for each slide")
    print("   ✅ Structured content placeholders")
    print("   ✅ Ready for collaborative editing")
    
    print("\n🔓 To Share with Edit Access:")
    print("   1. Open the presentation link above")
    print("   2. Click 'Share' button (top right)")
    print("   3. Change 'Restricted' to 'Anyone with the link'")
    print("   4. Set permission to 'Editor'")
    print("   5. Click 'Copy link' to share")
    
    print(f"\n🚀 Open your presentation: {presentation_url}")
    
    # Copy link to clipboard
    try:
        import subprocess
        subprocess.run(['pbcopy'], input=presentation_url, text=True, check=True)
        print("📋 Link copied to clipboard!")
    except:
        pass
    
    return presentation_url


if __name__ == "__main__":
    get_presentation_info()

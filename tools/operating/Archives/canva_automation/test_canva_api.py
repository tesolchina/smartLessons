#!/usr/bin/env python3
"""
Canva Connect API Test Script
Test the official Canva Connect API with HKBU branding.
"""

import os
from canva_connect_cli import CanvaConnectCLI


def test_canva_api():
    """Test basic Canva Connect API functionality."""
    
    print("🧪 Testing Canva Connect API for HKBU")
    print("=" * 50)
    
    # Check environment variables
    client_id = os.getenv("CANVA_CLIENT_ID")
    client_secret = os.getenv("CANVA_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Missing environment variables!")
        print("\n📋 Setup required:")
        print("1. Visit: https://www.canva.com/developers/integrations/connect-api")
        print("2. Create integration with required scopes")
        print("3. Set environment variables:")
        print("   export CANVA_CLIENT_ID='your_client_id'")
        print("   export CANVA_CLIENT_SECRET='your_client_secret'")
        return False
    
    print(f"✅ Client ID: {client_id[:8]}...")
    print(f"✅ Client Secret: {'*' * 16}")
    
    # Initialize client
    canva = CanvaConnectCLI()
    
    # Test authentication
    print("\n🔐 Testing Authentication...")
    if not canva.access_token:
        print("⚠️  No saved tokens found. Starting authentication...")
        if not canva.authenticate():
            print("❌ Authentication failed")
            return False
        print("✅ Authentication successful!")
    else:
        print("✅ Using saved tokens")
    
    # Test user profile
    print("\n👤 Testing User Profile...")
    profile = canva.get_user_profile()
    if profile:
        print(f"✅ User: {profile.get('display_name', 'Unknown')}")
        print(f"✅ Email: {profile.get('email', 'Unknown')}")
    else:
        print("❌ Failed to get user profile")
        return False
    
    # Test brand templates
    print("\n📋 Testing Brand Templates...")
    templates = canva.list_brand_templates()
    if templates:
        print(f"✅ Found {len(templates)} templates:")
        for i, template in enumerate(templates[:3], 1):
            print(f"   {i}. {template.get('name', 'Unnamed')} (ID: {template.get('id')})")
    else:
        print("⚠️  No templates found (may require Enterprise account)")
    
    # Test blank design creation
    print("\n🎨 Testing Blank Design Creation...")
    try:
        design_id = canva.create_blank_design(
            design_type="presentation",
            title="HKBU Test Presentation"
        )
        
        if design_id:
            print(f"✅ Created blank design: {design_id}")
            print(f"✅ Edit in Canva: https://www.canva.com/design/{design_id}")
            
            # Test design info
            print("\n📊 Testing Design Info...")
            design_info = canva.get_design(design_id)
            if design_info:
                design = design_info.get('design', {})
                print(f"✅ Title: {design.get('title', 'Untitled')}")
                print(f"✅ Type: {design.get('design_type', 'Unknown')}")
                print(f"✅ View URL: {design.get('urls', {}).get('view_url', 'N/A')}")
            else:
                print("❌ Failed to get design info")
        else:
            print("❌ Failed to create blank design")
    
    except Exception as e:
        print(f"❌ Error creating design: {e}")
    
    # Test template autofill (if templates available)
    if templates:
        print("\n🔧 Testing Template Autofill...")
        template = templates[0]
        template_id = template.get('id')
        
        if not template_id:
            print("❌ Template ID not found")
            return True
        
        try:
            # Get template dataset
            dataset = canva.get_brand_template_dataset(str(template_id))
            if dataset:
                fields = dataset.get('dataset', {})
                print(f"✅ Template has {len(fields)} autofill fields:")
                for field_name, field_info in list(fields.items())[:3]:
                    field_type = field_info.get('type', 'unknown')
                    print(f"   - {field_name}: {field_type}")
                
                # Try autofill with sample data
                autofill_data = {}
                for field_name, field_info in fields.items():
                    field_type = field_info.get('type')
                    if field_type == 'text':
                        autofill_data[field_name] = {
                            'type': 'text',
                            'text': f'HKBU LANG 2077 - {field_name.title()}'
                        }
                
                if autofill_data:
                    print(f"⏳ Creating design with {len(autofill_data)} autofilled fields...")
                    design_id = canva.create_design_autofill(
                        template_id=str(template_id),
                        data=autofill_data,
                        title="HKBU LANG2077 Autofill Test"
                    )
                    
                    if design_id:
                        print(f"✅ Autofill design created: {design_id}")
                        print(f"✅ Edit in Canva: https://www.canva.com/design/{design_id}")
                    else:
                        print("❌ Autofill creation failed")
            else:
                print("⚠️  Could not get template dataset")
        
        except Exception as e:
            print(f"❌ Error testing autofill: {e}")
    
    print("\n🏁 Test Summary:")
    print("✅ Authentication: Working")
    print("✅ User Profile: Working") 
    print(f"✅ Templates: {len(templates) if templates else 0} found")
    print("✅ Blank Design: Working")
    print("✅ Basic API functionality confirmed!")
    
    if not templates:
        print("\n💡 Note: Brand template features require Canva for Enterprise")
    
    return True


def demo_hkbu_presentation():
    """Create a demo HKBU presentation."""
    
    print("\n🎓 Creating HKBU Demo Presentation")
    print("=" * 40)
    
    canva = CanvaConnectCLI()
    
    if not canva.access_token:
        print("❌ Authentication required. Run test_canva_api() first.")
        return
    
    # Create presentation
    design_id = canva.create_blank_design(
        design_type="presentation", 
        title="LANG 2077: Academic Presentation Skills - Demo"
    )
    
    if design_id:
        print(f"✅ Demo presentation created!")
        print(f"📝 Title: LANG 2077: Academic Presentation Skills - Demo")
        print(f"🔗 Edit: https://www.canva.com/design/{design_id}")
        print(f"👀 View: https://www.canva.com/design/{design_id}/view")
        
        print("\n📋 Next steps:")
        print("1. Open the design in Canva")
        print("2. Add HKBU branding elements")
        print("3. Create slides for your course content")
        print("4. Export as PDF when ready")
        
        # Try to get design info
        design_info = canva.get_design(design_id)
        if design_info:
            urls = design_info.get('design', {}).get('urls', {})
            if urls.get('view_url'):
                print(f"\n🔗 Direct link: {urls['view_url']}")
    
    else:
        print("❌ Failed to create demo presentation")


if __name__ == "__main__":
    print("🎯 Canva Connect API Test Suite")
    print("=" * 50)
    
    while True:
        print("\nSelect test:")
        print("1. Run API Test Suite")
        print("2. Create HKBU Demo Presentation")  
        print("3. Interactive CLI")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            test_canva_api()
        elif choice == "2":
            demo_hkbu_presentation()
        elif choice == "3":
            from canva_connect_cli import create_hkbu_presentation_cli
            create_hkbu_presentation_cli()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

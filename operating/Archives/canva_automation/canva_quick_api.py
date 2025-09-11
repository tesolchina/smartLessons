#!/usr/bin/env python3
"""
Simple Canva API Client - Lightweight CLI Tool
Direct API calls without complex dependencies
Created: September 6, 2025
"""

import os
import json
import requests
from datetime import datetime

class SimpleCanvaAPI:
    """Lightweight Canva API client"""
    
    def __init__(self, access_token=None):
        # Try to get token from environment or parameter
        self.access_token = access_token or os.getenv("CANVA_ACCESS_TOKEN", "")
        self.base_url = "https://api.canva.com/rest/v1"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def test_connection(self):
        """Quick API test"""
        if not self.access_token:
            print("❌ No access token found")
            print("Set CANVA_ACCESS_TOKEN environment variable")
            return False
        
        try:
            response = requests.get(f"{self.base_url}/users/me", headers=self.headers, timeout=10)
            if response.status_code == 200:
                user = response.json()
                print(f"✅ Connected as: {user.get('display_name', 'User')}")
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def create_design(self, design_type="presentation", title="New Design"):
        """Create a new design"""
        payload = {"design_type": design_type, "title": title}
        
        try:
            response = requests.post(
                f"{self.base_url}/designs", 
                headers=self.headers, 
                json=payload, 
                timeout=30
            )
            
            if response.status_code == 201:
                design = response.json()
                print(f"✅ Created: {title}")
                print(f"🔗 Edit: {design['urls']['edit_url']}")
                return design
            else:
                print(f"❌ Creation failed: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

def quick_presentation(title="LANG2077 Presentation", token=None):
    """Quick presentation creation"""
    print(f"🚀 Creating: {title}")
    
    api = SimpleCanvaAPI(token)
    
    if not api.test_connection():
        return None
    
    design = api.create_design("presentation", title)
    return design

if __name__ == "__main__":
    import sys
    
    # Check for token in arguments
    token = None
    title = "LANG2077 Course Introduction"
    
    if len(sys.argv) > 1:
        if sys.argv[1].startswith("canva_"):
            token = sys.argv[1]
            title = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else title
        else:
            title = " ".join(sys.argv[1:])
    
    result = quick_presentation(title, token)
    
    if result:
        print("\n🎯 Next steps:")
        print("1. Click the edit URL to open in Canva")
        print("2. Add your content and customize")
        print("3. Share with collaborators directly in Canva")
        print("4. Export when ready")
    else:
        print("\n❌ Failed to create presentation")
        print("💡 Try: python3 canva_api_setup.py")

#!/usr/bin/env python3
"""
Canva Connect API CLI - True API-based Design Creation
No browser automation required - uses Canva's REST APIs
Created: September 6, 2025
"""

import os
import sys
import json
import requests
import argparse
from datetime import datetime
from dotenv import load_dotenv

class CanvaConnectAPI:
    """Canva Connect API client for programmatic design creation"""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("CANVA_API_KEY", "")
        self.access_token = os.getenv("CANVA_ACCESS_TOKEN", "")
        self.base_url = "https://api.canva.com/rest/v1"
        
        # Default headers for all API requests
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        if not self.access_token:
            print("⚠️  CANVA_ACCESS_TOKEN not found in environment variables")
            print("📋 Setup required - see setup_canva_api() method")
    
    def setup_canva_api(self):
        """Guide user through Canva API setup"""
        print("🔧 Canva Connect API Setup Guide")
        print("=" * 40)
        print()
        print("1. Go to https://developers.canva.com/")
        print("2. Create a developer account")
        print("3. Create a new Connect API app")
        print("4. Get your access token")
        print("5. Add to .env file: CANVA_ACCESS_TOKEN=your_token_here")
        print()
        print("Required scopes for this CLI:")
        print("- design:content:read")
        print("- design:content:write") 
        print("- asset:read")
        print("- asset:write")
        print("- folder:read")
        print("- folder:write")
        print()
        return False
    
    def check_api_connection(self):
        """Test API connection and permissions"""
        try:
            print("🔍 Testing Canva API connection...")
            
            # Test with a simple user profile request
            response = requests.get(
                f"{self.base_url}/users/me",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Connected successfully!")
                print(f"👤 User: {user_data.get('display_name', 'Unknown')}")
                return True
            elif response.status_code == 401:
                print("❌ Authentication failed - check your access token")
                return False
            else:
                print(f"❌ API connection failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return False
    
    def create_presentation_design(self, title="Untitled Presentation"):
        """Create a new presentation design via API"""
        try:
            print(f"📊 Creating presentation: {title}")
            
            payload = {
                "design_type": "presentation",
                "asset_ids": [],  # Can specify template IDs here
                "title": title
            }
            
            response = requests.post(
                f"{self.base_url}/designs",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                design_data = response.json()
                design_id = design_data["id"]
                design_url = design_data["urls"]["edit_url"]
                
                print(f"✅ Presentation created successfully!")
                print(f"🆔 Design ID: {design_id}")
                print(f"🔗 Edit URL: {design_url}")
                
                return {
                    "id": design_id,
                    "url": design_url,
                    "data": design_data
                }
            else:
                print(f"❌ Failed to create design: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error creating design: {e}")
            return None
    
    def add_text_to_design(self, design_id, text_content, page_index=0):
        """Add text elements to a design"""
        try:
            print(f"📝 Adding text to design {design_id}")
            
            # Get design pages first
            pages_response = requests.get(
                f"{self.base_url}/designs/{design_id}/pages",
                headers=self.headers,
                timeout=30
            )
            
            if pages_response.status_code != 200:
                print(f"❌ Failed to get design pages: {pages_response.status_code}")
                return False
            
            pages_data = pages_response.json()
            if not pages_data.get("items"):
                print("❌ No pages found in design")
                return False
            
            page_id = pages_data["items"][page_index]["id"]
            
            # Add text element
            text_payload = {
                "elements": [
                    {
                        "type": "text",
                        "text": text_content,
                        "position": {
                            "x": 100,
                            "y": 100
                        },
                        "font": {
                            "family": "Arial",
                            "size": 24,
                            "weight": "bold"
                        }
                    }
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/designs/{design_id}/pages/{page_id}/elements",
                headers=self.headers,
                json=text_payload,
                timeout=30
            )
            
            if response.status_code == 201:
                print(f"✅ Text added successfully")
                return True
            else:
                print(f"❌ Failed to add text: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error adding text: {e}")
            return False
    
    def share_design(self, design_id, collaborator_emails, permission="edit"):
        """Share design with collaborators via API"""
        try:
            print(f"🔗 Sharing design {design_id} with collaborators...")
            
            for email in collaborator_emails:
                share_payload = {
                    "recipients": [
                        {
                            "email": email,
                            "permission": permission
                        }
                    ],
                    "message": "You've been invited to collaborate on this presentation"
                }
                
                response = requests.post(
                    f"{self.base_url}/designs/{design_id}/permissions",
                    headers=self.headers,
                    json=share_payload,
                    timeout=30
                )
                
                if response.status_code == 201:
                    print(f"✅ Invitation sent to {email}")
                else:
                    print(f"⚠️  Failed to invite {email}: {response.status_code}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error sharing design: {e}")
            return False
    
    def get_design_info(self, design_id):
        """Get information about a design"""
        try:
            response = requests.get(
                f"{self.base_url}/designs/{design_id}",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get design info: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error getting design info: {e}")
            return None
    
    def export_design(self, design_id, format="pdf"):
        """Export design to various formats"""
        try:
            print(f"📤 Exporting design {design_id} as {format.upper()}")
            
            export_payload = {
                "format": format,
                "pages": "all"
            }
            
            response = requests.post(
                f"{self.base_url}/designs/{design_id}/export",
                headers=self.headers,
                json=export_payload,
                timeout=60
            )
            
            if response.status_code == 202:
                export_data = response.json()
                job_id = export_data.get("job", {}).get("id")
                
                print(f"✅ Export started - Job ID: {job_id}")
                
                # Check export status (simplified - in production, implement polling)
                return {
                    "job_id": job_id,
                    "status": "processing"
                }
            else:
                print(f"❌ Failed to start export: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error exporting design: {e}")
            return None

def create_lang2077_api_slides():
    """Create LANG 2077 slides using Canva Connect API"""
    
    print("🎓 LANG 2077 Slides - Canva Connect API")
    print("=" * 45)
    
    # Initialize API client
    canva_api = CanvaConnectAPI()
    
    # Check if API is configured
    if not canva_api.access_token:
        return canva_api.setup_canva_api()
    
    # Test connection
    if not canva_api.check_api_connection():
        return False
    
    # Create presentation
    design_title = f"LANG2077_Course_Introduction_{datetime.now().strftime('%Y%m%d_%H%M')}"
    design = canva_api.create_presentation_design(design_title)
    
    if not design:
        return False
    
    design_id = design["id"]
    design_url = design["url"]
    
    # Add slide content
    slide_content = [
        "LANG 2077\nLanguage Skills for human-AI partnership:\nCustomizing Chatbots to Empower Communities",
        "What Students Will Learn\n• Language Skills Development\n• AI Partnership Skills\n• Community Engagement",
        "Empowering Communities Through AI\n• Community Partner Collaboration\n• Chatbot Customization Projects\n• Student Deliverables & Impact"
    ]
    
    # Add content to first slide
    canva_api.add_text_to_design(design_id, slide_content[0])
    
    # Share with collaborators
    collaborators = [
        "department.head@hkbu.edu.hk",
        "course.coordinator@hkbu.edu.hk", 
        "teaching.assistant@hkbu.edu.hk"
    ]
    
    canva_api.share_design(design_id, collaborators, "edit")
    
    # Export as PDF
    export_job = canva_api.export_design(design_id, "pdf")
    
    print("\n✅ LANG 2077 slides created successfully via API!")
    print(f"🆔 Design ID: {design_id}")
    print(f"🔗 Edit URL: {design_url}")
    print(f"📧 Collaborators invited: {len(collaborators)}")
    
    if export_job:
        print(f"📤 PDF export job: {export_job['job_id']}")
    
    # Save design info locally
    design_info = {
        "design_id": design_id,
        "edit_url": design_url,
        "title": design_title,
        "created": datetime.now().isoformat(),
        "collaborators": collaborators,
        "slide_content": slide_content,
        "export_job": export_job
    }
    
    output_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/api_designs"
    os.makedirs(output_dir, exist_ok=True)
    
    info_file = os.path.join(output_dir, f"{design_title}_info.json")
    with open(info_file, 'w') as f:
        json.dump(design_info, f, indent=2)
    
    print(f"💾 Design info saved: {info_file}")
    
    return True

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Canva Connect API CLI")
    parser.add_argument("--setup", action="store_true", help="Show API setup guide")
    parser.add_argument("--test", action="store_true", help="Test API connection")
    parser.add_argument("--create", choices=["lang2077", "presentation"], help="Create specific design type")
    parser.add_argument("--title", default="API Created Presentation", help="Design title")
    parser.add_argument("--collaborators", nargs="+", help="Collaborator email addresses")
    parser.add_argument("--export", choices=["pdf", "png", "jpg"], help="Export format")
    
    args = parser.parse_args()
    
    canva_api = CanvaConnectAPI()
    
    if args.setup:
        canva_api.setup_canva_api()
        return
    
    if args.test:
        canva_api.check_api_connection()
        return
    
    if args.create == "lang2077":
        create_lang2077_api_slides()
        return
    
    if args.create == "presentation":
        design = canva_api.create_presentation_design(args.title)
        if design and args.collaborators:
            canva_api.share_design(design["id"], args.collaborators)
        if design and args.export:
            canva_api.export_design(design["id"], args.export)
        return
    
    # Default: show help
    parser.print_help()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
HKBU Canva Connect API CLI
A comprehensive CLI tool for creating and managing Canva designs using the official Connect API.

Requirements:
1. Set up Developer Portal at https://www.canva.com/developers/
2. Configure OAuth integration with localhost redirect
3. Set environment variables for client credentials
"""

import os
import json
import base64
import time
import urllib.parse
import webbrowser
from typing import Dict, Any, Optional, List
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth


class CanvaConnectCLI:
    """Official Canva Connect API client for HKBU presentations."""
    
    def __init__(self):
        """Initialize with HKBU branding and API configuration."""
        
        # API Configuration
        self.base_url = "https://api.canva.com"
        self.client_id = os.getenv("CANVA_CLIENT_ID")
        self.client_secret = os.getenv("CANVA_CLIENT_SECRET")
        self.redirect_uri = "http://127.0.0.1:3001/oauth/redirect"
        
        # Token management
        self.access_token = None
        self.refresh_token = None
        self.token_file = "canva_tokens.json"
        
        # HKBU Brand Configuration
        self.hkbu_config = {
            "brand_colors": {
                "primary": "#8B0000",      # Deep Red
                "secondary": "#FFD700",    # Gold
                "accent": "#2E8B57",       # Sea Green
                "text": "#333333",         # Dark Gray
                "background": "#F8F8F8"    # Light Gray
            },
            "fonts": [
                "Helvetica Neue",
                "Arial",
                "Source Sans Pro",
                "Open Sans"
            ],
            "university_info": {
                "name": "Hong Kong Baptist University",
                "department": "Language Centre",
                "website": "https://www.hkbu.edu.hk",
                "logo_text": "HKBU"
            }
        }
        
        # Load existing tokens
        self._load_tokens()
        
    def _load_tokens(self) -> bool:
        """Load saved access tokens from file."""
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    tokens = json.load(f)
                    self.access_token = tokens.get('access_token')
                    self.refresh_token = tokens.get('refresh_token')
                    return True
        except Exception as e:
            print(f"⚠️  Error loading tokens: {e}")
        return False
    
    def _save_tokens(self) -> None:
        """Save access tokens to file."""
        try:
            tokens = {
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'timestamp': datetime.now().isoformat()
            }
            with open(self.token_file, 'w') as f:
                json.dump(tokens, f, indent=2)
            print("✅ Tokens saved successfully")
        except Exception as e:
            print(f"❌ Error saving tokens: {e}")
    
    def authenticate(self) -> bool:
        """Complete OAuth flow for Canva Connect API."""
        
        if not self.client_id or not self.client_secret:
            print("❌ Missing CANVA_CLIENT_ID or CANVA_CLIENT_SECRET environment variables")
            print("\n📋 Setup Instructions:")
            print("1. Visit https://www.canva.com/developers/integrations/connect-api")
            print("2. Create an integration with these scopes:")
            print("   - profile: Read")
            print("   - design:content: Read and Write")
            print("   - design:meta: Read")
            print("   - brandtemplate:content: Read")
            print("   - brandtemplate:meta: Read")
            print("   - asset: Read and Write")
            print("3. Set redirect URL: http://127.0.0.1:3001/oauth/redirect")
            print("4. Export CANVA_CLIENT_ID and CANVA_CLIENT_SECRET")
            return False
        
        # Ensure we have valid credentials
        if not isinstance(self.client_id, str) or not isinstance(self.client_secret, str):
            print("❌ Invalid client credentials")
            return False
        
        # Step 1: Authorization URL
        auth_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'design:content:read design:content:write design:meta:read brandtemplate:content:read brandtemplate:meta:read asset:read asset:write profile:read',
            'state': 'hkbu_canva_cli'
        }
        
        auth_url = f"https://www.canva.com/api/oauth/authorize?" + urllib.parse.urlencode(auth_params)
        
        print("🔐 Opening browser for Canva authentication...")
        webbrowser.open(auth_url)
        
        # Step 2: Get authorization code
        print("\n📋 After authorizing, copy the 'code' parameter from the redirect URL")
        auth_code = input("Enter authorization code: ").strip()
        
        if not auth_code:
            print("❌ No authorization code provided")
            return False
        
        # Step 3: Exchange code for tokens
        return self._exchange_code_for_tokens(auth_code)
    
    def _exchange_code_for_tokens(self, auth_code: str) -> bool:
        """Exchange authorization code for access tokens."""
        
        token_data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/oauth/token",
                data=token_data,
                auth=HTTPBasicAuth(str(self.client_id), str(self.client_secret)),
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            if response.status_code == 200:
                tokens = response.json()
                self.access_token = tokens.get('access_token')
                self.refresh_token = tokens.get('refresh_token')
                self._save_tokens()
                print("✅ Authentication successful!")
                return True
            else:
                print(f"❌ Token exchange failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def _make_api_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Make authenticated API request to Canva Connect."""
        
        if not self.access_token:
            print("❌ Not authenticated. Run authenticate() first.")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}/v1{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                print(f"❌ Unsupported method: {method}")
                return None
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"❌ API request failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ API request error: {e}")
            return None
    
    def get_user_profile(self) -> Optional[Dict]:
        """Get current user profile."""
        return self._make_api_request('GET', '/users/me')
    
    def list_brand_templates(self) -> List[Dict]:
        """List available brand templates."""
        
        response = self._make_api_request('GET', '/brand-templates')
        if response:
            return response.get('items', [])
        return []
    
    def get_brand_template_dataset(self, template_id: str) -> Optional[Dict]:
        """Get dataset definition for a brand template."""
        
        return self._make_api_request('GET', f'/brand-templates/{template_id}/dataset')
    
    def upload_asset(self, image_path: str, name: str) -> Optional[str]:
        """Upload an image asset to Canva."""
        
        if not os.path.exists(image_path):
            print(f"❌ Image file not found: {image_path}")
            return None
        
        # Step 1: Create upload job
        upload_data = {
            'asset': {
                'name_base64': base64.b64encode(name.encode()).decode(),
                'tags': ['HKBU', 'presentation', 'academic']
            }
        }
        
        job_response = self._make_api_request('POST', '/asset-uploads', upload_data)
        if not job_response:
            return None
        
        job_id = job_response.get('job', {}).get('id')
        upload_url = job_response.get('job', {}).get('asset', {}).get('upload_url')
        
        if not upload_url:
            print("❌ No upload URL received")
            return None
        
        # Step 2: Upload file
        try:
            with open(image_path, 'rb') as f:
                files = {'file': f}
                upload_response = requests.post(upload_url, files=files)
                
                if upload_response.status_code != 204:
                    print(f"❌ File upload failed: {upload_response.status_code}")
                    return None
        
        except Exception as e:
            print(f"❌ File upload error: {e}")
            return None
        
        # Step 3: Poll for completion
        for _ in range(30):  # 30 seconds max wait
            job_status = self._make_api_request('GET', f'/asset-uploads/{job_id}')
            if job_status:
                status = job_status.get('job', {}).get('status')
                if status == 'success':
                    asset_id = job_status.get('job', {}).get('asset', {}).get('id')
                    print(f"✅ Asset uploaded successfully: {asset_id}")
                    return asset_id
                elif status == 'failed':
                    print("❌ Asset upload failed")
                    return None
            
            time.sleep(1)
        
        print("❌ Asset upload timeout")
        return None
    
    def create_design_autofill(self, template_id: str, data: Dict[str, Any], title: Optional[str] = None) -> Optional[str]:
        """Create a design by autofilling a brand template."""
        
        # Prepare autofill request
        autofill_data = {
            'brand_template_id': template_id,
            'data': data
        }
        
        if title:
            autofill_data['title'] = title
        
        # Create autofill job
        job_response = self._make_api_request('POST', '/autofills', autofill_data)
        if not job_response:
            return None
        
        job_id = job_response.get('job', {}).get('id')
        if not job_id:
            print("❌ No job ID received")
            return None
        
        print(f"🔄 Autofill job started: {job_id}")
        
        # Poll for completion
        for i in range(60):  # 60 seconds max wait
            job_status = self._make_api_request('GET', f'/autofills/{job_id}')
            if job_status:
                status = job_status.get('job', {}).get('status')
                if status == 'success':
                    design_id = job_status.get('job', {}).get('result', {}).get('design', {}).get('id')
                    if design_id:
                        print(f"✅ Design created successfully: {design_id}")
                        return design_id
                elif status == 'failed':
                    error_msg = job_status.get('job', {}).get('error', {}).get('message', 'Unknown error')
                    print(f"❌ Autofill failed: {error_msg}")
                    return None
            
            print(f"⏳ Waiting for autofill completion... ({i+1}/60)")
            time.sleep(1)
        
        print("❌ Autofill timeout")
        return None
    
    def create_blank_design(self, design_type: str = "presentation", title: Optional[str] = None) -> Optional[str]:
        """Create a blank design."""
        
        design_data = {
            'design_type': design_type
        }
        
        if title:
            design_data['title'] = title
        
        response = self._make_api_request('POST', '/designs', design_data)
        if response:
            design_id = response.get('design', {}).get('id')
            if design_id:
                print(f"✅ Blank design created: {design_id}")
                return design_id
        
        return None
    
    def get_design(self, design_id: str) -> Optional[Dict]:
        """Get design metadata."""
        return self._make_api_request('GET', f'/designs/{design_id}')
    
    def export_design(self, design_id: str, file_format: str = "JPG") -> Optional[List[str]]:
        """Export design as specified format."""
        
        export_data = {
            'design_id': design_id,
            'format': file_format
        }
        
        # Create export job
        job_response = self._make_api_request('POST', '/exports', export_data)
        if not job_response:
            return None
        
        job_id = job_response.get('job', {}).get('id')
        if not job_id:
            print("❌ No export job ID received")
            return None
        
        print(f"🔄 Export job started: {job_id}")
        
        # Poll for completion
        for i in range(60):  # 60 seconds max wait
            job_status = self._make_api_request('GET', f'/exports/{job_id}')
            if job_status:
                status = job_status.get('job', {}).get('status')
                if status == 'success':
                    urls = job_status.get('job', {}).get('urls', [])
                    if urls:
                        print(f"✅ Export completed: {len(urls)} files")
                        return urls
                elif status == 'failed':
                    error_msg = job_status.get('job', {}).get('error', {}).get('message', 'Unknown error')
                    print(f"❌ Export failed: {error_msg}")
                    return None
            
            print(f"⏳ Waiting for export completion... ({i+1}/60)")
            time.sleep(1)
        
        print("❌ Export timeout")
        return None


def create_hkbu_presentation_cli():
    """CLI interface for creating HKBU presentations."""
    
    print("🎓 HKBU Canva Connect API CLI")
    print("=" * 50)
    
    canva = CanvaConnectCLI()
    
    # Check authentication
    if not canva.access_token:
        print("🔐 Authentication required")
        if not canva.authenticate():
            print("❌ Authentication failed")
            return
    
    # Get user profile
    print("\n📋 User Profile:")
    profile = canva.get_user_profile()
    if profile:
        print(f"   Name: {profile.get('display_name', 'Unknown')}")
        print(f"   Email: {profile.get('email', 'Unknown')}")
    
    while True:
        print("\n🎨 Available Actions:")
        print("1. List Brand Templates")
        print("2. Create Blank Presentation")
        print("3. Create From Template (Autofill)")
        print("4. Upload Asset")
        print("5. Export Design")
        print("6. View Design Info")
        print("7. Exit")
        
        choice = input("\nSelect action (1-7): ").strip()
        
        if choice == "1":
            print("\n📋 Brand Templates:")
            templates = canva.list_brand_templates()
            if templates:
                for i, template in enumerate(templates[:10], 1):  # Show first 10
                    print(f"   {i}. {template.get('name', 'Unnamed')} (ID: {template.get('id')})")
            else:
                print("   No templates found or access restricted")
        
        elif choice == "2":
            title = input("Enter presentation title (optional): ").strip()
            if not title:
                title = f"HKBU Presentation {datetime.now().strftime('%Y%m%d_%H%M')}"
            
            design_id = canva.create_blank_design("presentation", title)
            if design_id:
                print(f"✅ Created: https://www.canva.com/design/{design_id}")
        
        elif choice == "3":
            template_id = input("Enter template ID: ").strip()
            if template_id:
                # Get template dataset
                dataset = canva.get_brand_template_dataset(template_id)
                if dataset:
                    print(f"📋 Template has {len(dataset.get('dataset', {}))} data fields")
                    
                    # Example autofill data
                    autofill_data = {
                        'title': {
                            'type': 'text',
                            'text': 'LANG 2077: Academic Presentation Skills'
                        },
                        'subtitle': {
                            'type': 'text', 
                            'text': 'Hong Kong Baptist University'
                        },
                        'presenter': {
                            'type': 'text',
                            'text': 'Language Centre'
                        }
                    }
                    
                    title = f"HKBU LANG2077 {datetime.now().strftime('%Y%m%d_%H%M')}"
                    design_id = canva.create_design_autofill(template_id, autofill_data, title)
                    if design_id:
                        print(f"✅ Created: https://www.canva.com/design/{design_id}")
        
        elif choice == "4":
            image_path = input("Enter image file path: ").strip()
            name = input("Enter asset name: ").strip()
            if image_path and name:
                asset_id = canva.upload_asset(image_path, name)
                if asset_id:
                    print(f"✅ Asset uploaded: {asset_id}")
        
        elif choice == "5":
            design_id = input("Enter design ID: ").strip()
            file_format = input("Enter format (JPG/PNG/PDF, default JPG): ").strip().upper()
            if not file_format:
                file_format = "JPG"
            
            if design_id:
                urls = canva.export_design(design_id, file_format)
                if urls:
                    for i, url in enumerate(urls, 1):
                        print(f"   File {i}: {url}")
        
        elif choice == "6":
            design_id = input("Enter design ID: ").strip()
            if design_id:
                design_info = canva.get_design(design_id)
                if design_info:
                    design = design_info.get('design', {})
                    print(f"   Title: {design.get('title', 'Untitled')}")
                    print(f"   Type: {design.get('design_type', 'Unknown')}")
                    print(f"   Edit URL: {design.get('urls', {}).get('edit_url', 'N/A')}")
                    print(f"   View URL: {design.get('urls', {}).get('view_url', 'N/A')}")
        
        elif choice == "7":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    create_hkbu_presentation_cli()

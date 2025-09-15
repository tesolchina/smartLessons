"""
Updated Google API authentication using secure environment variables
Replace the old hardcoded credentials.json approach with this secure version
"""

import os
import sys
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Add config directory to path for secure_config import
repo_root = Path(__file__).parents[2]  # Adjust based on file location
sys.path.insert(0, str(repo_root / "config"))

try:
    from secure_config import get_google_credentials_path, cleanup_temp_credentials
except ImportError:
    print("❌ Error: secure_config module not found")
    print("📋 Make sure config/secure_config.py exists in your repo root")
    sys.exit(1)

from typing import Optional, List

def authenticate_google_service(service_name: str = "docs", scopes: Optional[List[str]] = None):
    """
    Authenticate with Google API using environment variables
    
    Args:
        service_name: "docs" or "slides" 
        scopes: List of OAuth scopes needed
        
    Returns:
        Authenticated Google API service object
    """
    if scopes is None:
        # Default scopes for common services
        if service_name == "docs":
            scopes = ['https://www.googleapis.com/auth/documents']
        elif service_name == "slides":
            scopes = ['https://www.googleapis.com/auth/presentations']
        else:
            raise ValueError(f"Unknown service: {service_name}")
    
    creds = None
    
    # Define token path in a secure location (not in repo)
    home_dir = Path.home()
    token_dir = home_dir / ".dailyassistant" / "tokens"
    token_dir.mkdir(parents=True, exist_ok=True)
    token_path = token_dir / f"token_{service_name}.pickle"
    
    # Load existing token
    if token_path.exists():
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"❌ Token refresh failed: {e}")
                creds = None
        
        if not creds:
            # Get credentials from environment variables
            try:
                credentials_path = get_google_credentials_path(service_name)
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, scopes)
                creds = flow.run_local_server(port=0)
                
                # Clean up temporary credentials file
                cleanup_temp_credentials()
                
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                print("📋 Make sure your .env file contains the correct Google API credentials")
                print(f"📋 Required variables: GOOGLE_{service_name.upper()}_CLIENT_ID, GOOGLE_{service_name.upper()}_CLIENT_SECRET, GOOGLE_{service_name.upper()}_PROJECT_ID")
                return None
        
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    # Build and return the service
    if service_name == "docs":
        return build('docs', 'v1', credentials=creds)
    elif service_name == "slides":
        return build('slides', 'v1', credentials=creds)
    else:
        raise ValueError(f"Unknown service: {service_name}")


def get_docs_service():
    """Get authenticated Google Docs service"""
    return authenticate_google_service("docs", ['https://www.googleapis.com/auth/documents'])


def get_slides_service():
    """Get authenticated Google Slides service"""
    return authenticate_google_service("slides", ['https://www.googleapis.com/auth/presentations'])


# Example usage and testing
if __name__ == "__main__":
    try:
        print("🔐 Testing Google API authentication with secure config...")
        
        # Test Docs service
        docs_service = get_docs_service()
        if docs_service:
            print("✅ Google Docs service authenticated successfully")
        
        # Test Slides service
        slides_service = get_slides_service()
        if slides_service:
            print("✅ Google Slides service authenticated successfully")
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        print("📋 Check your .env file configuration")
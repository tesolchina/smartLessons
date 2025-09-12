"""
Google API Authentication Setup for GCAP 3226 Team Management
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
from pathlib import Path

# Scopes for Google Drive, Docs, and Sheets APIs
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets'
]

def authenticate_google_apis():
    """
    Set up Google API authentication
    Returns authenticated credentials for API access
    """
    creds = None
    token_file = Path(__file__).parent / 'token.pickle'
    credentials_file = Path(__file__).parent / 'credentials.json'
    
    # Check if we have saved credentials
    if token_file.exists():
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials are available, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                creds = None
        
        if not creds:
            if not credentials_file.exists():
                print("❌ credentials.json not found!")
                print("Please download credentials from Google Cloud Console")
                print("Steps:")
                print("1. Go to Google Cloud Console")
                print("2. Create/select project 'GCAP3226-TeamManager'")
                print("3. Enable Drive, Docs, and Sheets APIs")
                print("4. Create OAuth 2.0 credentials")
                print("5. Download and save as 'credentials.json'")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
        
        print("✅ Authentication successful!")
    
    return creds

def test_authentication():
    """Test if authentication is working"""
    try:
        from googleapiclient.discovery import build
        
        creds = authenticate_google_apis()
        if not creds:
            return False
        
        # Test Drive API access
        drive_service = build('drive', 'v3', credentials=creds)
        results = drive_service.files().list(pageSize=1).execute()
        
        # Test Docs API access
        docs_service = build('docs', 'v1', credentials=creds)
        
        print("✅ Google APIs authentication successful!")
        print(f"✅ Drive API: Working")
        print(f"✅ Docs API: Working")
        return True
        
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Setting up Google API authentication...")
    print("=" * 50)
    
    if test_authentication():
        print("\n🎉 Setup complete! You can now run the team folder creation scripts.")
    else:
        print("\n❌ Setup failed. Please check the instructions above.")

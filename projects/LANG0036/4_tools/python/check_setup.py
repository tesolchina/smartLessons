"""
Quick Client Info Display

Shows information about your OAuth client configuration
"""

import json

def display_client_info():
    """Display information about the OAuth client"""
    
    client_id = "584822767688-sljrj83d92o8l3efd7urg3il9unlca1b.apps.googleusercontent.com"
    
    print("🔑 Google OAuth Client Information")
    print("=" * 50)
    print(f"Client ID: {client_id}")
    print(f"Project ID: {client_id.split('-')[0]}")
    print(f"Domain: {client_id.split('.')[-1]}")
    
    print("\n📋 Current Setup Status:")
    
    # Check credentials file
    try:
        with open('credentials/client_credentials.json', 'r') as f:
            creds = json.load(f)
            
        client_secret = creds['installed']['client_secret']
        
        if client_secret == 'REPLACE_WITH_YOUR_CLIENT_SECRET':
            print("❌ Client secret not configured")
            print("   → Need to get client secret from Google Cloud Console")
        else:
            print("✅ Client secret configured")
            print(f"   → Secret: {client_secret[:10]}...")
            
    except FileNotFoundError:
        print("❌ Credentials file not found")
    except Exception as e:
        print(f"❌ Error reading credentials: {e}")
    
    # Check token file
    try:
        with open('credentials/token.json', 'r') as f:
            token = json.load(f)
        print("✅ Authentication token exists")
        print("   → You've already authenticated with Google")
    except FileNotFoundError:
        print("⚠️  No authentication token found")
        print("   → You'll need to authenticate when first running the script")
    
    print("\n🎯 Next Steps:")
    print("1. Get your client secret from Google Cloud Console")
    print("2. Update credentials/client_credentials.json")
    print("3. Run: python simple_drive_test.py")
    print("4. Authenticate in browser when prompted")
    print("5. Start using the Google Drive API!")

if __name__ == "__main__":
    display_client_info()
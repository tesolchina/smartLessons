"""
Quick Test Script for Google API Setup

Run this script to verify your Google API setup is working correctly.
"""

from google_api_client import GoogleAPIClient

def main():
    """Test Google API functionality"""
    print("🧪 Google API Quick Test")
    print("=" * 40)
    
    try:
        # Initialize client
        print("🔧 Initializing Google API client...")
        client = GoogleAPIClient()
        
        # Test connection
        print("🔍 Testing connection...")
        if not client.test_connection():
            print("❌ Connection test failed")
            return
        
        # Test Drive API
        print("\n📁 Testing Google Drive...")
        recent_files = client.list_files(max_results=3)
        print(f"✅ Found {len(recent_files)} recent files")
        
        # Test folder creation
        print("\n📂 Testing folder creation...")
        test_folder = client.create_folder("API_Test_Folder")
        print(f"✅ Created test folder: {test_folder['webViewLink']}")
        
        # Test document creation
        print("\n📄 Testing document creation...")
        test_doc = client.create_document("API_Test_Document", test_folder['id'])
        print(f"✅ Created test document: {test_doc['webViewLink']}")
        
        # Test spreadsheet creation
        print("\n📊 Testing spreadsheet creation...")
        test_sheet = client.create_spreadsheet("API_Test_Spreadsheet", test_folder['id'])
        print(f"✅ Created test spreadsheet: {test_sheet['webViewLink']}")
        
        print("\n" + "=" * 40)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 40)
        print("✅ Google API client is ready to use")
        print("✅ Authentication working")
        print("✅ Drive API working")
        print("✅ File creation working")
        
        print(f"\n🔗 Test folder: {test_folder['webViewLink']}")
        print("\n📋 You can now:")
        print("• Use the GoogleAPIClient in your projects")
        print("• Create folders, documents, and spreadsheets")
        print("• Manage file permissions")
        print("• Read and write to Google Sheets")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify credentials_template.json exists")
        print("3. Make sure required APIs are enabled in Google Cloud Console")
        print("4. Try deleting token.json and re-authenticating")

if __name__ == "__main__":
    main()
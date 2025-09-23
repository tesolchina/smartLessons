"""
Quick Google Drive Test - Manual Authentication

This script attempts to create folders and docs with manual OAuth flow.
We'll try to get the client secret from the Google Cloud Console.
"""

import webbrowser
import json
import os

def open_google_console():
    """Open Google Cloud Console to get client secret"""
    client_id = "584822767688-sljrj83d92o8l3efd7urg3il9unlca1b.apps.googleusercontent.com"
    project_id = "584822767688"
    
    console_url = f"https://console.cloud.google.com/apis/credentials?project={project_id}"
    
    print("🌐 Opening Google Cloud Console...")
    print(f"Project ID: {project_id}")
    print(f"Client ID: {client_id}")
    print("\nIn the console:")
    print("1. Find your OAuth 2.0 Client ID")
    print("2. Click on the pencil icon to edit")
    print("3. Copy the 'Client Secret'")
    print("4. Come back here and paste it")
    
    webbrowser.open(console_url)
    
    return input("\nPaste your Client Secret here: ").strip()

def setup_credentials():
    """Set up credentials with user input"""
    print("🔧 Setting up Google API credentials...")
    
    # Check if we already have credentials
    creds_file = 'credentials/client_credentials.json'
    
    if os.path.exists(creds_file):
        with open(creds_file, 'r') as f:
            creds = json.load(f)
        
        if creds['installed']['client_secret'] != 'REPLACE_WITH_YOUR_CLIENT_SECRET':
            print("✅ Credentials already configured!")
            return True
    
    # Get client secret from user
    print("❌ Client secret needed...")
    client_secret = open_google_console()
    
    if not client_secret:
        print("❌ No client secret provided")
        return False
    
    # Update credentials file
    client_config = {
        "installed": {
            "client_id": "584822767688-sljrj83d92o8l3efd7urg3il9unlca1b.apps.googleusercontent.com",
            "project_id": "gcap3226-project",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": client_secret,
            "redirect_uris": ["http://localhost"]
        }
    }
    
    # Create credentials directory
    os.makedirs('credentials', exist_ok=True)
    
    # Save credentials
    with open(creds_file, 'w') as f:
        json.dump(client_config, f, indent=2)
    
    print("✅ Credentials saved!")
    return True

def test_drive_access():
    """Test Google Drive access and create folders/docs"""
    try:
        from simple_drive_test import authenticate, create_course_folder
        from googleapiclient.errors import HttpError
        
        print("\n🔐 Authenticating with Google...")
        service = authenticate()
        
        if not service:
            print("❌ Authentication failed")
            return False
        
        print("✅ Authentication successful!")
        
        # Create course folder
        print("\n📁 Creating course folder...")
        folder = create_course_folder(service)
        
        if folder:
            print(f"✅ Course folder created: {folder['name']}")
            print(f"🔗 Link: {folder['webViewLink']}")
            
            # Create a test document
            print("\n📄 Creating test document...")
            doc_metadata = {
                'name': 'GCAP3226_Test_Document',
                'parents': [folder['id']],
                'mimeType': 'application/vnd.google-apps.document'
            }
            
            doc = service.files().create(
                body=doc_metadata,
                fields='id,name,webViewLink'
            ).execute()
            
            print(f"✅ Test document created: {doc['name']}")
            print(f"🔗 Link: {doc['webViewLink']}")
            
            # Create a test spreadsheet
            print("\n📊 Creating test spreadsheet...")
            sheet_metadata = {
                'name': 'GCAP3226_Team_Assignments',
                'parents': [folder['id']],
                'mimeType': 'application/vnd.google-apps.spreadsheet'
            }
            
            sheet = service.files().create(
                body=sheet_metadata,
                fields='id,name,webViewLink'
            ).execute()
            
            print(f"✅ Test spreadsheet created: {sheet['name']}")
            print(f"🔗 Link: {sheet['webViewLink']}")
            
            return True
        
        return False
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all Google API packages are installed")
        return False
    except HttpError as e:
        print(f"❌ Google API error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def create_team_folders():
    """Create sample team folders"""
    try:
        from simple_drive_test import authenticate
        from googleapiclient.errors import HttpError
        
        service = authenticate()
        if not service:
            return False
        
        # Sample teams
        teams = [
            {"name": "Team_Alpha", "members": ["student1@example.com", "student2@example.com"]},
            {"name": "Team_Beta", "members": ["student3@example.com", "student4@example.com"]},
            {"name": "Team_Gamma", "members": ["student5@example.com", "student6@example.com"]}
        ]
        
        print(f"\n👥 Creating folders for {len(teams)} sample teams...")
        
        # Get course folder first
        query = "name='GCAP3226_Course_Materials' and mimeType='application/vnd.google-apps.folder'"
        results = service.files().list(q=query).execute()
        course_folders = results.get('files', [])
        
        parent_id = course_folders[0]['id'] if course_folders else None
        
        created_folders = []
        
        for team in teams:
            try:
                # Create team folder
                folder_metadata = {
                    'name': f"GCAP3226_{team['name']}",
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                
                if parent_id:
                    folder_metadata['parents'] = [parent_id]
                
                folder = service.files().create(
                    body=folder_metadata,
                    fields='id,name,webViewLink'
                ).execute()
                
                print(f"📁 Created: {folder['name']}")
                print(f"   Link: {folder['webViewLink']}")
                
                # Create template files in the folder
                templates = [
                    {'name': 'Team_Project_Plan', 'type': 'application/vnd.google-apps.document'},
                    {'name': 'Data_Analysis_Sheet', 'type': 'application/vnd.google-apps.spreadsheet'},
                    {'name': 'Final_Presentation', 'type': 'application/vnd.google-apps.presentation'}
                ]
                
                for template in templates:
                    file_metadata = {
                        'name': template['name'],
                        'parents': [folder['id']],
                        'mimeType': template['type']
                    }
                    
                    file = service.files().create(
                        body=file_metadata,
                        fields='id,name'
                    ).execute()
                    
                    print(f"   📄 Created: {file['name']}")
                
                created_folders.append({
                    'team': team['name'],
                    'folder': folder,
                    'status': 'success'
                })
                
            except HttpError as e:
                print(f"❌ Failed to create folder for {team['name']}: {e}")
                created_folders.append({
                    'team': team['name'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        print(f"\n📊 Summary: {len([f for f in created_folders if f['status'] == 'success'])}/{len(teams)} teams created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating team folders: {e}")
        return False

def main():
    """Main function"""
    print("🚀 GCAP3226 - Create Folders and Docs")
    print("=" * 50)
    
    # Setup credentials
    if not setup_credentials():
        print("❌ Could not set up credentials")
        return
    
    # Test basic access
    print("\n🧪 Testing Google Drive access...")
    if not test_drive_access():
        print("❌ Could not access Google Drive")
        return
    
    # Ask if user wants to create team folders
    create_teams = input("\n❓ Create sample team folders? (y/n): ").lower().strip()
    
    if create_teams == 'y':
        create_team_folders()
    
    print("\n🎉 Done! Check your Google Drive for the new folders and files.")
    print("\nNext steps:")
    print("• Customize the team names and members")
    print("• Run the full team_setup.py script with your real data")
    print("• Set up your Google Sheets with team assignments")

if __name__ == "__main__":
    main()
"""
Create Team Folders and Docs for GCAP3226

This script will create folders and template documents for your teams.
"""

import json
from simple_drive_test import authenticate
from googleapiclient.errors import HttpError

def create_team_structure():
    """Create team folders and template documents"""
    
    print("🚀 Creating GCAP3226 Team Structure")
    print("=" * 50)
    
    # Authenticate
    service = authenticate()
    if not service:
        print("❌ Authentication failed")
        return
    
    # Get the course folder ID
    course_folder_id = "15TA_J0fV-YitdSAnF1vKI96wUQ-MP7EO"  # From previous output
    
    # Sample teams (you can customize these)
    teams = [
        {"name": "Alpha", "topic": "Data Privacy in Healthcare"},
        {"name": "Beta", "topic": "AI Ethics in Education"}, 
        {"name": "Gamma", "topic": "Smart City Governance"},
        {"name": "Delta", "topic": "Digital Identity Management"}
    ]
    
    print(f"👥 Creating folders for {len(teams)} teams...")
    
    created_items = []
    
    for team in teams:
        try:
            print(f"\n📁 Setting up Team {team['name']}...")
            
            # Create team folder
            folder_metadata = {
                'name': f"Team_{team['name']}_{team['topic'].replace(' ', '_')}",
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [course_folder_id]
            }
            
            folder = service.files().create(
                body=folder_metadata,
                fields='id,name,webViewLink'
            ).execute()
            
            print(f"✅ Created folder: {folder['name']}")
            print(f"   🔗 Link: {folder['webViewLink']}")
            
            # Create template documents in the folder
            templates = [
                {
                    'name': 'Project_Proposal',
                    'type': 'application/vnd.google-apps.document',
                    'content': f"# Team {team['name']} - {team['topic']}\n\n## Project Overview\n\n## Team Members\n\n## Timeline\n\n## Deliverables"
                },
                {
                    'name': 'Data_Analysis_Worksheet', 
                    'type': 'application/vnd.google-apps.spreadsheet'
                },
                {
                    'name': 'Final_Presentation',
                    'type': 'application/vnd.google-apps.presentation'
                },
                {
                    'name': 'Meeting_Notes',
                    'type': 'application/vnd.google-apps.document'
                },
                {
                    'name': 'Literature_Review',
                    'type': 'application/vnd.google-apps.document'
                }
            ]
            
            team_files = []
            
            for template in templates:
                file_metadata = {
                    'name': f"{template['name']}_{team['name']}",
                    'parents': [folder['id']],
                    'mimeType': template['type']
                }
                
                file = service.files().create(
                    body=file_metadata,
                    fields='id,name,webViewLink'
                ).execute()
                
                print(f"   📄 Created: {file['name']}")
                
                team_files.append({
                    'name': file['name'],
                    'id': file['id'],
                    'link': file['webViewLink'],
                    'type': template['type']
                })
            
            created_items.append({
                'team': team['name'],
                'topic': team['topic'],
                'folder': {
                    'name': folder['name'],
                    'id': folder['id'],
                    'link': folder['webViewLink']
                },
                'files': team_files,
                'status': 'success'
            })
            
        except HttpError as e:
            print(f"❌ Error creating team {team['name']}: {e}")
            created_items.append({
                'team': team['name'],
                'topic': team['topic'],
                'status': 'failed',
                'error': str(e)
            })
    
    # Save results
    with open('team_creation_results.json', 'w') as f:
        json.dump(created_items, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEAM CREATION SUMMARY")
    print("=" * 60)
    
    successful = [item for item in created_items if item['status'] == 'success']
    failed = [item for item in created_items if item['status'] == 'failed']
    
    print(f"✅ Successfully created: {len(successful)} teams")
    print(f"❌ Failed: {len(failed)} teams")
    
    if successful:
        print(f"\n🎉 Created teams and folders:")
        for item in successful:
            print(f"📁 Team {item['team']}: {item['topic']}")
            print(f"   Link: {item['folder']['link']}")
            print(f"   Files: {len(item['files'])} template documents created")
    
    if failed:
        print(f"\n❌ Failed teams:")
        for item in failed:
            print(f"   Team {item['team']}: {item.get('error', 'Unknown error')}")
    
    print(f"\n📄 Results saved to: team_creation_results.json")
    print(f"\n🔗 Main course folder: https://drive.google.com/drive/folders/{course_folder_id}")
    
    return created_items

if __name__ == "__main__":
    create_team_structure()
#!/usr/bin/env python3
"""
Grant Talia (wutian1025@gmail.com) editor access to all team folders
"""

import json
from google_api_client import GoogleAPIClient

def grant_talia_access():
    """Grant Talia editor access to all team folders"""
    print("👥 Granting Talia editor access to all team folders")
    print("=" * 60)
    
    # Load team data
    try:
        with open('team_folders_created.json', 'r') as f:
            team_data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: team_folders_created.json not found.")
        return False
    
    # Initialize API client
    try:
        api_client = GoogleAPIClient()
        drive_service = api_client.get_drive_service()
        print("🔧 Connected to Drive API")
    except Exception as e:
        print(f"❌ Error connecting to Drive API: {e}")
        return False
    
    talia_email = "wutian1025@gmail.com"
    success_count = 0
    total_teams = 0
    
    # Process each team
    for team in team_data.get("teams", []):
        total_teams += 1
        team_name = team.get("team_name")
        folder_id = team.get("folder_id")
        
        if not folder_id:
            print(f"❌ No folder ID found for {team_name}")
            continue
        
        try:
            permission = {
                'type': 'user',
                'role': 'writer',
                'emailAddress': talia_email
            }
            drive_service.permissions().create(
                fileId=folder_id,
                body=permission
            ).execute()
            print(f"✅ {team_name}: Granted {talia_email} editor access")
            success_count += 1
        except Exception as e:
            print(f"❌ {team_name}: Failed to grant access - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 SUMMARY: {success_count}/{total_teams} team folders updated")
    print(f"✅ Talia ({talia_email}) now has editor access to {success_count} team folders")
    print("=" * 60)
    
    return success_count == total_teams

if __name__ == "__main__":
    grant_talia_access()
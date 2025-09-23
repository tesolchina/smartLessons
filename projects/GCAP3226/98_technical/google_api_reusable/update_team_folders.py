#!/usr/bin/env python3
"""
Update all GCAP3226 team folders:
1. Add Talia (wutian1025@gmail.com) as editor to all folders
2. Rename documents:
   - Literature_Review → Reflection_Essays
   - Project_Proposal → Project_Report  
   - Analysis_Worksheet → Data_Analysis_Worksheet
3. Update meeting notes with team membership, topics, and WhatsApp links
"""

import json
import sys
from google_api_client import GoogleAPIClient

def load_team_data():
    """Load existing team data from the previous run"""
    try:
        with open('team_folders_created.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: team_folders_created.json not found. Run create_gcap3226_teams.py first.")
        sys.exit(1)

def update_team_folders():
    """Main function to update all team folders"""
    print("🔄 Updating GCAP3226 Team Folders")
    print("=" * 60)
    
    # Load team data
    team_data = load_team_data()
    
    # Initialize API client
    try:
        api_client = GoogleAPIClient()
        drive_service = api_client.get_drive_service()
        docs_service = api_client.get_docs_service()
        print("🔧 Connected to Google APIs")
    except Exception as e:
        print(f"❌ Error connecting to Google APIs: {e}")
        return False
    
    # Talia's email
    talia_email = "wutian1025@gmail.com"
    
    # Document rename mappings
    rename_mappings = {
        "Literature_Review": "Reflection_Essays",
        "Project_Proposal": "Project_Report",
        "Analysis_Worksheet": "Data_Analysis_Worksheet"
    }
    
    # Team information for meeting notes
    team_info = {
        "Team_1": {
            "topic": "Topic 6",
            "members": [
                "Yeung Wing Yu (opheliasheep123@gmail.com, 97728503)",
                "Kwok Tsz Yau (kwoktszyau2004@gmail.com, 96232165)",
                "Tsoi Yik Hon (⚠️ Gmail needed, 61722240)",
                "SuJiaLu (⚠️ Gmail needed, 53986330)"
            ],
            "whatsapp": "⚠️ WhatsApp group not yet created"
        },
        "Team_2": {
            "topic": "Topic 3", 
            "members": [
                "Chan Hei Tung (adriennecht@gmail.com, 92107071)",
                "Yip Tsz Ying (⚠️ Gmail needed, 93118850)",
                "Ko Man Wai (⚠️ Gmail needed)",
                "Wong Ling Yan Cassy (⚠️ Gmail needed)",
                "Tsoi Tsz Yan (tsoitszyannn@gmail.com, 61597468)",
                "Zi Xing Saul Ma (⚠️ Gmail needed)"
            ],
            "whatsapp": "https://chat.whatsapp.com/Lq16DaYCqb326p8mlXBwJ0"
        },
        "Team_3": {
            "topic": "Topic 7",
            "members": [
                "Chen Man Ching (chenwenjing1023@gmail.com, 60450640)",
                "Hui Man Hei (shuaimangguo0813@gmail.com, 90158707)",
                "HONG KAM YIN (hhkamyin369@gmail.com, 52261355)",
                "Kung Tsz Lok (joannakung3009@gmail.com, 56850521)",
                "ZHENG ZIAN (⚠️ Gmail needed, ID missing)",
                "Chan Ching Yin (Leonchanchingyin@gmail.com, 69935955)"
            ],
            "whatsapp": "https://chat.whatsapp.com/E5U0JTMcXAiIO8kdLUtpIi"
        },
        "Team_4": {
            "topic": "Topic 4",
            "members": [
                "Liu Wai Man (lwm95820542@gmail.com, 95820542)",
                "Kwok Lai Ki (kinkikwoki116@gmail.com, 59842385)",
                "Chan Tsz Ying (⚠️ Gmail needed, 51923705)",
                "Wong Wai Lun (aw07133@gmail.com, 59182048)"
            ],
            "whatsapp": "https://chat.whatsapp.com/G5ocJeK5GgjCFBVBseVcre"
        },
        "Team_5": {
            "topic": "Topic 5",
            "members": [
                "MAN Wai Yin (manyin201612@gmail.com, 95821706)",
                "Chan Chi Ki (cks171302@gmail.com, 91845208)",
                "Tag Tsz Tung (jessie.one.air@gmail.com, 60485775)",
                "HO Chun Chit (tony030824@gmail.com, 54819060)",
                "Xu Jingyi (zjldbzq1314@gmail.com, 84902278)",
                "Cheung Kwun Ho (⚠️ Gmail needed, 65733021)"
            ],
            "whatsapp": "https://chat.whatsapp.com/E93BYRjp2FuClTcmzVxPc0"
        },
        "Team_6": {
            "topic": "Topic 2",
            "members": [
                "Tam Tin Chun (tamtinchun@gmail.com, 92250633)",
                "Chan Dik On (chandikon7@gmail.com, 44144124)",
                "Wong Chun Hang (qazwedc12369@gmail.com, 67351119)"
            ],
            "whatsapp": "https://chat.whatsapp.com/E9hLnEJmoy11GPrzlSGYrj"
        }
    }
    
    update_summary = {
        "talia_access_granted": [],
        "documents_renamed": [],
        "meeting_notes_updated": [],
        "errors": []
    }
    
    # Process each team
    for team in team_data.get("teams", []):
        team_name = team.get("team_name")
        if not team_name:
            continue
            
        print(f"\n👥 Updating {team_name}")
        folder_id = team.get("folder_id")
        files = team.get("files", [])
        
        if not folder_id:
            print(f"❌ No folder ID found for {team_name}")
            continue
        
        # 1. Grant Talia editor access to the team folder
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
            print(f"✅ Granted {talia_email} editor access to folder")
            update_summary["talia_access_granted"].append(team_name)
        except Exception as e:
            error_msg = f"Failed to grant access to {team_name} folder: {e}"
            print(f"❌ {error_msg}")
            update_summary["errors"].append(error_msg)
        
        # 2. Rename documents
        meeting_notes_id = None
        for file_info in files:
            file_id = file_info.get("id")
            current_name = file_info.get("name", "")
            
            # Track meeting notes ID for later update
            if "Meeting_Notes" in current_name:
                meeting_notes_id = file_id
            
            # Check if this document needs renaming
            new_name = None
            for old_pattern, new_pattern in rename_mappings.items():
                if old_pattern in current_name:
                    new_name = current_name.replace(old_pattern, new_pattern)
                    break
            
            if new_name and file_id:
                try:
                    drive_service.files().update(
                        fileId=file_id,
                        body={'name': new_name}
                    ).execute()
                    print(f"✅ Renamed: {current_name} → {new_name}")
                    update_summary["documents_renamed"].append({
                        "team": team_name,
                        "old_name": current_name,
                        "new_name": new_name
                    })
                except Exception as e:
                    error_msg = f"Failed to rename {current_name} in {team_name}: {e}"
                    print(f"❌ {error_msg}")
                    update_summary["errors"].append(error_msg)
        
        # 3. Update meeting notes with team information
        if meeting_notes_id and team_name in team_info:
            try:
                team_details_info = team_info[team_name]
                
                # Create content for meeting notes
                content = f"""# {team_name} Meeting Notes

## Team Information

**Topic**: {team_details_info['topic']}

**WhatsApp Group**: {team_details_info['whatsapp']}

## Team Members:
"""
                for member in team_details_info['members']:
                    content += f"- {member}\n"
                
                content += """
---

## Meeting Log

### Meeting 1 - [Date]
**Agenda:**
- 

**Discussion:**
- 

**Action Items:**
- 

**Next Meeting:** [Date/Time]

---

### Meeting 2 - [Date]
**Agenda:**
- 

**Discussion:**
- 

**Action Items:**
- 

**Next Meeting:** [Date/Time]

---

*Add new meetings above this line*
"""
                
                # Update the document
                requests = [
                    {
                        'insertText': {
                            'location': {'index': 1},
                            'text': content
                        }
                    }
                ]
                
                docs_service.documents().batchUpdate(
                    documentId=meeting_notes_id,
                    body={'requests': requests}
                ).execute()
                
                print(f"✅ Updated meeting notes with team information")
                update_summary["meeting_notes_updated"].append(team_name)
                
            except Exception as e:
                error_msg = f"Failed to update meeting notes for {team_name}: {e}"
                print(f"❌ {error_msg}")
                update_summary["errors"].append(error_msg)
    
    # Save update summary
    with open('team_updates_summary.json', 'w') as f:
        json.dump(update_summary, f, indent=2)
    
    # Print final summary
    print("\n" + "=" * 60)
    print("📊 UPDATE SUMMARY")
    print("=" * 60)
    print(f"✅ Talia access granted: {len(update_summary['talia_access_granted'])} teams")
    print(f"✅ Documents renamed: {len(update_summary['documents_renamed'])} documents")
    print(f"✅ Meeting notes updated: {len(update_summary['meeting_notes_updated'])} teams")
    print(f"❌ Errors encountered: {len(update_summary['errors'])}")
    
    if update_summary['errors']:
        print("\n🚨 Errors:")
        for error in update_summary['errors']:
            print(f"   - {error}")
    
    print(f"\n📄 Detailed results saved to: team_updates_summary.json")
    print("🎉 Team folder updates completed!")
    
    return len(update_summary['errors']) == 0

if __name__ == "__main__":
    success = update_team_folders()
    sys.exit(0 if success else 1)
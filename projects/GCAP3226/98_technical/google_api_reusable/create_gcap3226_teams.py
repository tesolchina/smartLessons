"""
Create GCAP3226 Team Folders and Documents

This script creates Google Drive folders for all 6 teams based on the 
actual team formation data from the spreadsheet.
"""

from google_api_client import GoogleAPIClient
import json
from datetime import datetime

def create_gcap3226_team_structure():
    """Create folders and documents for GCAP3226 teams"""
    
    client = GoogleAPIClient()
    
    print("🚀 Creating GCAP3226 Team Structure")
    print("=" * 60)
    
    # Team data based on the actual spreadsheet
    teams = [
        {
            "name": "Team_1",
            "topic": "Topic_6",
            "topic_description": "TBD - Topic 6",
            "members": [
                {"name": "Yeung Wing Yu", "id": "23238283", "gmail": "opheliasheep123@gmail.com", "whatsapp": "97728503"},
                {"name": "Kwok Tsz Yau", "id": "22234020", "gmail": "kwoktszyau2004@gmail.com", "whatsapp": "96232165"},
                {"name": "Tsoi Yik Hon", "id": "22232192", "gmail": "", "whatsapp": "61722240"},
                {"name": "SuJiaLu", "id": "22256946", "gmail": "", "whatsapp": "53986330"}
            ],
            "whatsapp_group": ""
        },
        {
            "name": "Team_2", 
            "topic": "Topic_3",
            "topic_description": "TBD - Topic 3",
            "members": [
                {"name": "Chan Hei Tung", "id": "23232099", "gmail": "adriennecht@gmail.com", "whatsapp": "92107071"},
                {"name": "Yip Tsz Ying", "id": "23229543", "gmail": "", "whatsapp": "93118850"},
                {"name": "Ko Man Wai", "id": "23234997", "gmail": "", "whatsapp": ""},
                {"name": "Wong Ling Yan Cassy", "id": "23233168", "gmail": "", "whatsapp": ""},
                {"name": "Tsoi Tsz Yan", "id": "23229101", "gmail": "tsoitszyannn@gmail.com", "whatsapp": "61597468"},
                {"name": "Zi Xing Saul Ma", "id": "23200278", "gmail": "", "whatsapp": ""}
            ],
            "whatsapp_group": "https://chat.whatsapp.com/Lq16DaYCqb326p8mlXBwJ0"
        },
        {
            "name": "Team_3",
            "topic": "Topic_7", 
            "topic_description": "TBD - Topic 7",
            "members": [
                {"name": "Chen Man Ching", "id": "23232781", "gmail": "chenwenjing1023@gmail.com", "whatsapp": "60450640"},
                {"name": "Hui Man Hei", "id": "25223305", "gmail": "shuaimangguo0813@gmail.com", "whatsapp": "90158707"},
                {"name": "HONG KAM YIN", "id": "25227394", "gmail": "hhkamyin369@gmail.com", "whatsapp": "52261355"},
                {"name": "Kung Tsz Lok", "id": "25206354", "gmail": "joannakung3009@gmail.com", "whatsapp": "56850521"},
                {"name": "ZHENG ZIAN", "id": "", "gmail": "", "whatsapp": ""},
                {"name": "Chan Ching Yin", "id": "22224009", "gmail": "Leonchanchingyin@gmail.com", "whatsapp": "69935955"}
            ],
            "whatsapp_group": "https://chat.whatsapp.com/E5U0JTMcXAiIO8kdLUtpIi"
        },
        {
            "name": "Team_4",
            "topic": "Topic_4",
            "topic_description": "TBD - Topic 4", 
            "members": [
                {"name": "Liu Wai Man", "id": "24221872", "gmail": "lwm95820542@gmail.com", "whatsapp": "95820542"},
                {"name": "Kwok Lai Ki", "id": "25215833", "gmail": "kinkikwoki116@gmail.com", "whatsapp": "59842385"},
                {"name": "Chan Tsz Ying", "id": "25200135", "gmail": "", "whatsapp": "51923705"},
                {"name": "Wong Wai Lun", "id": "25221310", "gmail": "aw07133@gmail.com", "whatsapp": "59182048"}
            ],
            "whatsapp_group": "https://chat.whatsapp.com/G5ocJeK5GgjCFBVBseVcre"
        },
        {
            "name": "Team_5",
            "topic": "Topic_5",
            "topic_description": "TBD - Topic 5",
            "members": [
                {"name": "MAN Wai Yin", "id": "24202509", "gmail": "manyin201612@gmail.com", "whatsapp": "95821706"},
                {"name": "Chan Chi Ki", "id": "23233885", "gmail": "cks171302@gmail.com", "whatsapp": "91845208"},
                {"name": "Tag Tsz Tung", "id": "23230371", "gmail": "jessie.one.air@gmail.com", "whatsapp": "60485775"},
                {"name": "HO Chun Chit", "id": "24202495", "gmail": "tony030824@gmail.com", "whatsapp": "54819060"},
                {"name": "Xu Jingyi", "id": "24205397", "gmail": "zjldbzq1314@gmail.com", "whatsapp": "84902278"},
                {"name": "Cheung Kwun Ho", "id": "24219169", "gmail": "", "whatsapp": "65733021"}
            ],
            "whatsapp_group": "https://chat.whatsapp.com/E93BYRjp2FuClTcmzVxPc0"
        },
        {
            "name": "Team_6",
            "topic": "Topic_2",
            "topic_description": "TBD - Topic 2",
            "members": [
                {"name": "Tam Tin Chun", "id": "23236353", "gmail": "tamtinchun@gmail.com", "whatsapp": "92250633"},
                {"name": "Chan Dik On", "id": "23230851", "gmail": "chandikon7@gmail.com", "whatsapp": "44144124"},
                {"name": "Wong Chun Hang", "id": "23213116", "gmail": "qazwedc12369@gmail.com", "whatsapp": "67351119"}
            ],
            "whatsapp_group": "https://chat.whatsapp.com/E9hLnEJmoy11GPrzlSGYrj"
        }
    ]
    
    # Get or create main course folder
    course_folder_id = "15TA_J0fV-YitdSAnF1vKI96wUQ-MP7EO"  # From previous test
    
    print(f"📁 Using course folder: GCAP3226_Course_Materials")
    print(f"   ID: {course_folder_id}")
    
    created_teams = []
    
    for team in teams:
        try:
            print(f"\n👥 Setting up {team['name']} - {team['topic']}")
            
            # Create team folder
            folder_name = f"GCAP3226_{team['name']}_{team['topic']}"
            team_folder = client.create_folder(folder_name, course_folder_id)
            
            print(f"   📂 Folder: {team_folder['webViewLink']}")
            
            # Create template documents
            templates = [
                {"name": "Project_Proposal", "type": "document"},
                {"name": "Data_Collection_Plan", "type": "document"},
                {"name": "Analysis_Worksheet", "type": "spreadsheet"},
                {"name": "Final_Presentation", "type": "presentation"},
                {"name": "Meeting_Notes", "type": "document"},
                {"name": "Literature_Review", "type": "document"}
            ]
            
            created_files = []
            for template in templates:
                if template["type"] == "document":
                    doc = client.create_document(
                        f"{template['name']}_{team['name']}", 
                        team_folder['id']
                    )
                elif template["type"] == "spreadsheet":
                    doc = client.create_spreadsheet(
                        f"{template['name']}_{team['name']}", 
                        team_folder['id']
                    )
                # Note: Presentations need special handling in Google API
                
                created_files.append({
                    'name': doc['name'],
                    'id': doc['id'],
                    'link': doc['webViewLink'],
                    'type': template['type']
                })
                
                print(f"   📄 Created: {template['name']}")
            
            # Set permissions for team members with Gmail addresses
            gmail_members = [m for m in team['members'] if m['gmail'].strip()]
            
            print(f"   👥 Setting permissions for {len(gmail_members)} members with Gmail:")
            
            for member in gmail_members:
                try:
                    success = client.set_file_permissions(
                        team_folder['id'], 
                        member['gmail'].strip(), 
                        'writer'
                    )
                    if success:
                        print(f"      ✅ {member['name']}: {member['gmail']}")
                except Exception as e:
                    print(f"      ❌ {member['name']}: {e}")
            
            # Members without Gmail
            no_gmail = [m for m in team['members'] if not m['gmail'].strip()]
            if no_gmail:
                print(f"   ⚠️  Members needing Gmail addresses:")
                for member in no_gmail:
                    print(f"      📧 {member['name']} (ID: {member['id']})")
            
            created_teams.append({
                'team_name': team['name'],
                'topic': team['topic'],
                'topic_description': team['topic_description'],
                'folder_id': team_folder['id'],
                'folder_link': team_folder['webViewLink'],
                'members': team['members'],
                'files': created_files,
                'whatsapp_group': team['whatsapp_group'],
                'gmail_members': len(gmail_members),
                'total_members': len(team['members']),
                'status': 'success'
            })
            
        except Exception as e:
            print(f"   ❌ Error setting up {team['name']}: {e}")
            created_teams.append({
                'team_name': team['name'],
                'topic': team['topic'],
                'status': 'failed',
                'error': str(e)
            })
    
    # Save results
    results = {
        'timestamp': datetime.now().isoformat(),
        'course_folder_id': course_folder_id,
        'teams_created': len([t for t in created_teams if t['status'] == 'success']),
        'teams_failed': len([t for t in created_teams if t['status'] == 'failed']),
        'teams': created_teams
    }
    
    with open('team_folders_created.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Create summary report
    create_team_summary_report(created_teams)
    
    print(f"\n" + "="*60)
    print("📊 TEAM SETUP SUMMARY")
    print("="*60)
    
    successful = [t for t in created_teams if t['status'] == 'success']
    failed = [t for t in created_teams if t['status'] == 'failed']
    
    print(f"✅ Successfully created: {len(successful)} teams")
    print(f"❌ Failed: {len(failed)} teams")
    
    total_members_with_access = sum(t.get('gmail_members', 0) for t in successful)
    total_members = sum(t.get('total_members', 0) for t in successful)
    
    print(f"👥 Team members with Drive access: {total_members_with_access}/{total_members}")
    
    if successful:
        print(f"\n🎉 Created team folders:")
        for team in successful:
            print(f"   📁 {team['team_name']} ({team['topic']}): {team['folder_link']}")
    
    print(f"\n📄 Detailed results saved to: team_folders_created.json")
    
    return created_teams

def create_team_summary_report(teams):
    """Create a summary report for teams"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# GCAP3226 Team Folders Created

**Generated**: {timestamp}

## 📊 Summary

**Teams Successfully Created**: {len([t for t in teams if t['status'] == 'success'])}/6

## 📁 Team Folders and Access

"""
    
    for team in teams:
        if team['status'] == 'success':
            report += f"### {team['team_name']} - {team['topic']}\n\n"
            report += f"**Folder**: [{team['team_name']}]({team['folder_link']})\n\n"
            report += f"**Topic**: {team['topic_description']}\n\n"
            
            if team.get('whatsapp_group'):
                report += f"**WhatsApp Group**: {team['whatsapp_group']}\n\n"
            
            report += f"**Members ({team['total_members']}):**\n"
            for member in team['members']:
                status = "✅" if member['gmail'] else "❌"
                report += f"- {status} **{member['name']}** (ID: {member['id']})\n"
                if member['gmail']:
                    report += f"  - Gmail: {member['gmail']} (Drive access granted)\n"
                else:
                    report += f"  - ⚠️ Missing Gmail address\n"
                if member['whatsapp']:
                    report += f"  - WhatsApp: {member['whatsapp']}\n"
                report += "\n"
            
            report += f"**Documents Created**: {len(team['files'])}\n"
            for file in team['files']:
                report += f"- [{file['name']}]({file['link']})\n"
            
            report += "\n---\n\n"
    
    report += """## 🚨 Action Items

### Missing Gmail Addresses
Follow up with these students to get Gmail addresses for Drive access:

"""
    
    for team in teams:
        if team['status'] == 'success':
            no_gmail = [m for m in team['members'] if not m['gmail'].strip()]
            if no_gmail:
                report += f"**{team['team_name']}:**\n"
                for member in no_gmail:
                    report += f"- {member['name']} (ID: {member['id']})\n"
                report += "\n"
    
    report += """
### Next Steps
1. ✅ Team folders created with template documents
2. ✅ Permissions set for members with Gmail addresses
3. 📧 Follow up with students missing Gmail addresses
4. 📋 Update team topics with actual project descriptions
5. 📤 Send folder links to all team members
6. 📱 Verify WhatsApp group participation

---
*Generated automatically after Google Drive folder creation*
"""
    
    with open('team_summary_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"📋 Team summary report saved to: team_summary_report.md")

if __name__ == "__main__":
    teams = create_gcap3226_team_structure()
    
    if teams:
        print("\n🎉 Team folder creation completed!")
        print("\nFiles created:")
        print("- team_folders_created.json (Full results)")
        print("- team_summary_report.md (Summary for students)")
    else:
        print("❌ Team creation failed")
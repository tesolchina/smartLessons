"""
Example: Manage Team Assignments

This example shows how to read team data from a Google Sheet
and create folders with appropriate permissions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from google_api_client import GoogleAPIClient
import pandas as pd

def manage_team_assignments(spreadsheet_id, sheet_range="Teams!A:E"):
    """Read team assignments and create folders with permissions"""
    
    client = GoogleAPIClient()
    
    print("📊 Reading team assignments from Google Sheets...")
    
    # Read team data
    data = client.read_sheet_data(spreadsheet_id, sheet_range)
    
    if not data:
        print("❌ No data found in spreadsheet")
        return
    
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(data[1:], columns=data[0])  # Skip header row
    print(f"📋 Found {len(df)} student assignments")
    
    # Group by team
    teams = df.groupby('Team')
    
    print(f"👥 Creating folders for {len(teams)} teams...")
    
    # Create main course folder if needed
    course_folder = client.create_folder("GCAP3226_Team_Projects")
    
    results = []
    
    for team_name, members in teams:
        print(f"\n📁 Setting up Team: {team_name}")
        
        # Create team folder
        team_folder = client.create_folder(
            f"Team_{team_name}", 
            course_folder['id']
        )
        
        # Get member emails
        member_emails = members['Email'].tolist()
        member_names = members['Student_Name'].tolist()
        
        print(f"   Members: {', '.join(member_names)}")
        
        # Set permissions for team members
        for email in member_emails:
            success = client.set_file_permissions(
                team_folder['id'], 
                email.strip(), 
                'writer'
            )
            if success:
                print(f"   ✅ Access granted to {email}")
        
        # Create template files
        templates = [
            "Project_Plan",
            "Data_Analysis", 
            "Meeting_Notes",
            "Final_Report"
        ]
        
        created_files = []
        for template in templates:
            if template == "Data_Analysis":
                doc = client.create_spreadsheet(
                    f"{template}_{team_name}", 
                    team_folder['id']
                )
            else:
                doc = client.create_document(
                    f"{template}_{team_name}", 
                    team_folder['id']
                )
            
            created_files.append(doc)
            print(f"   📄 Created: {template}")
        
        results.append({
            'team': team_name,
            'folder_link': team_folder['webViewLink'],
            'members': member_names,
            'files': len(created_files)
        })
    
    # Update spreadsheet with folder links
    print(f"\n📊 Updating spreadsheet with folder links...")
    
    # Prepare update data
    update_data = [['Team', 'Folder_Link']]  # Header
    for result in results:
        update_data.append([result['team'], result['folder_link']])
    
    # Write back to sheet
    client.write_sheet_data(
        spreadsheet_id, 
        "Teams!F1:G" + str(len(update_data)), 
        update_data
    )
    
    print("✅ Spreadsheet updated with folder links")
    
    # Print summary
    print(f"\n📊 SUMMARY")
    print("=" * 40)
    for result in results:
        print(f"Team {result['team']}: {result['files']} files created")
        print(f"  🔗 {result['folder_link']}")
    
    return results

# Example usage
if __name__ == "__main__":
    # Replace with your actual spreadsheet ID
    spreadsheet_id = "1lLcG1FMW7lYqw_O8kCs74nFJjFOwsuAe--Prg3qd45A"
    
    try:
        results = manage_team_assignments(spreadsheet_id)
        print(f"\n🎉 Successfully set up {len(results)} teams!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure:")
        print("1. Spreadsheet ID is correct")
        print("2. Sheet has columns: Team, Student_Name, Email")
        print("3. You have access to the spreadsheet")
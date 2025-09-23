#!/usr/bin/env python3
"""
Check which students are not assigned to any group yet
by comparing enrolled students with group assignments
"""

import json
import pandas as pd
from google_api_client import GoogleAPIClient

def find_unassigned_students():
    """Find students who are not assigned to any group"""
    print("🔍 Checking for unassigned students")
    print("=" * 60)
    
    # Initialize API client
    try:
        api_client = GoogleAPIClient()
        sheets_service = api_client.get_sheets_service()
        print("🔧 Connected to Sheets API")
    except Exception as e:
        print(f"❌ Error connecting to Sheets API: {e}")
        return
    
    # Load team data to get assigned students
    try:
        with open('team_folders_created.json', 'r') as f:
            team_data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: team_folders_created.json not found.")
        return
    
    # Get all assigned students from teams
    assigned_students = set()
    assigned_student_details = []
    
    for team in team_data.get("teams", []):
        team_name = team.get("team_name", "")
        for member in team.get("members", []):
            student_name = member.get("name", "").strip()
            student_id = member.get("id", "").strip()
            
            if student_name:
                assigned_students.add(student_name.lower())
                assigned_student_details.append({
                    "name": student_name,
                    "id": student_id,
                    "team": team_name
                })
    
    print(f"📊 Found {len(assigned_students)} students assigned to teams")
    
    # Get enrolled students list
    enrollment_sheet_id = "1kMj-9Rto9NLtEpYSpDhAFwS7ylGHE2CSu0jRABKSNDg"
    enrollment_range = "A:C"  # Simplified range
    
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=enrollment_sheet_id,
            range=enrollment_range
        ).execute()
        
        enrolled_data = result.get('values', [])
        print(f"📋 Retrieved {len(enrolled_data)} rows from enrollment sheet")
        
    except Exception as e:
        print(f"❌ Error reading enrollment sheet: {e}")
        return
    
    # Process enrolled students
    enrolled_students = []
    unassigned_students = []
    
    # Skip header row
    for row in enrolled_data[1:]:
        if len(row) >= 2:
            student_id = row[0].strip() if len(row) > 0 else ""
            student_name = row[1].strip() if len(row) > 1 else ""
            chinese_name = row[2].strip() if len(row) > 2 else ""
            
            if student_name:
                enrolled_students.append({
                    "id": student_id,
                    "name": student_name,
                    "chinese_name": chinese_name
                })
                
                # Check if this student is assigned to a team
                if student_name.lower() not in assigned_students:
                    unassigned_students.append({
                        "id": student_id,
                        "name": student_name,
                        "chinese_name": chinese_name
                    })
    
    print(f"👥 Total enrolled students: {len(enrolled_students)}")
    print(f"🏷️  Students assigned to teams: {len(assigned_students)}")
    print(f"❌ Students NOT assigned to teams: {len(unassigned_students)}")
    
    # Display results
    if unassigned_students:
        print("\n🚨 UNASSIGNED STUDENTS:")
        print("-" * 60)
        for student in unassigned_students:
            print(f"📝 {student['name']} (ID: {student['id']})")
            if student['chinese_name']:
                print(f"   Chinese Name: {student['chinese_name']}")
        
        # Save to file
        unassigned_df = pd.DataFrame(unassigned_students)
        unassigned_df.to_csv('unassigned_students.csv', index=False)
        print(f"\n📄 Unassigned students saved to: unassigned_students.csv")
        
    else:
        print("\n✅ All enrolled students are assigned to teams!")
    
    # Also check for potential name mismatches
    print("\n🔍 CHECKING FOR POTENTIAL NAME MISMATCHES:")
    print("-" * 60)
    
    assigned_names = [detail['name'] for detail in assigned_student_details]
    enrolled_names = [student['name'] for student in enrolled_students]
    
    # Find names in teams that don't exactly match enrollment
    team_only_names = []
    for assigned_name in assigned_names:
        exact_match = False
        for enrolled_name in enrolled_names:
            if assigned_name.lower() == enrolled_name.lower():
                exact_match = True
                break
        if not exact_match:
            team_only_names.append(assigned_name)
    
    if team_only_names:
        print("⚠️  Names in teams that don't exactly match enrollment:")
        for name in team_only_names:
            print(f"   - {name}")
        print("\n💡 These might be name variations or typos")
    else:
        print("✅ All team member names match enrollment records")
    
    # Summary report
    summary = {
        "total_enrolled": len(enrolled_students),
        "total_assigned": len(assigned_students),
        "total_unassigned": len(unassigned_students),
        "unassigned_students": unassigned_students,
        "potential_name_mismatches": team_only_names
    }
    
    with open('unassigned_students_report.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📊 Complete report saved to: unassigned_students_report.json")
    
    return unassigned_students

if __name__ == "__main__":
    find_unassigned_students()
"""
Fixed Student Data Extractor - Handle Data Structure Issues
"""

from google_api_client import GoogleAPIClient
import json
from datetime import datetime

def extract_spreadsheet_id(url):
    """Extract spreadsheet ID from Google Sheets URL"""
    if '/d/' in url:
        return url.split('/d/')[1].split('/')[0]
    return url

def safe_read_data(client, spreadsheet_id, description):
    """Safely read data from spreadsheet with error handling"""
    
    print(f"📊 Reading {description}...")
    print(f"Spreadsheet ID: {spreadsheet_id}")
    
    possible_ranges = [
        "A:Z", "Sheet1!A:Z", "Teams!A:Z", 
        "Form Responses 1!A:Z", "Team Formation!A:Z"
    ]
    
    for range_name in possible_ranges:
        try:
            data = client.read_sheet_data(spreadsheet_id, range_name)
            if data and len(data) > 0:
                print(f"✅ Found data in range: {range_name}")
                print(f"   Rows: {len(data)}")
                if data:
                    print(f"   Headers: {data[0]}")
                    print(f"   Sample row: {data[1] if len(data) > 1 else 'No data rows'}")
                return data, range_name
        except Exception as e:
            print(f"❌ Range {range_name} failed: {e}")
    
    return None, None

def analyze_team_data(data):
    """Analyze team formation data"""
    
    if not data or len(data) < 2:
        return {"error": "No team data available"}
    
    headers = data[0]
    rows = data[1:]
    
    print(f"\n📋 Team Formation Analysis:")
    print(f"Headers: {headers}")
    print(f"Data rows: {len(rows)}")
    
    # Extract team information
    teams = {}
    students = []
    
    for i, row in enumerate(rows):
        try:
            # Pad row if shorter than headers
            while len(row) < len(headers):
                row.append('')
            
            # Create student record
            student_info = {}
            for j, header in enumerate(headers):
                student_info[header] = row[j] if j < len(row) else ''
            
            students.append(student_info)
            
            # Extract team info
            team_id = student_info.get('Team 1', '').strip()
            if team_id and team_id not in teams:
                teams[team_id] = []
            
            if team_id:
                teams[team_id].append(student_info)
                
        except Exception as e:
            print(f"❌ Error processing row {i+2}: {e}")
    
    return {
        "headers": headers,
        "total_students": len(students),
        "teams": teams,
        "students": students,
        "team_count": len(teams)
    }

def analyze_student_list(data):
    """Analyze official student list"""
    
    if not data or len(data) < 2:
        return {"error": "No student list data available"}
    
    headers = data[0]
    rows = data[1:]
    
    print(f"\n📚 Student List Analysis:")
    print(f"Headers: {headers}")
    print(f"Data rows: {len(rows)}")
    
    students = []
    
    for i, row in enumerate(rows):
        try:
            # Handle variable row lengths
            student_info = {}
            for j, header in enumerate(headers):
                student_info[header] = row[j] if j < len(row) else ''
            
            students.append(student_info)
            
        except Exception as e:
            print(f"❌ Error processing student row {i+2}: {e}")
    
    return {
        "headers": headers,
        "total_students": len(students),
        "students": students
    }

def create_detailed_report(team_analysis, student_analysis):
    """Create detailed group formation report"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# GCAP3226 Group Formation and Topic Selection Update

**Generated**: {timestamp}

## 📊 Summary

"""
    
    # Team formation summary
    if "error" not in team_analysis:
        report += f"""### Team Formation Data
- **Total Responses**: {team_analysis['total_students']}
- **Number of Teams**: {team_analysis['team_count']}
- **Data Columns**: {', '.join(team_analysis['headers'])}

"""
        
        # List teams and members
        if team_analysis['teams']:
            report += "### Team Assignments\n\n"
            for team_id, members in team_analysis['teams'].items():
                if team_id:
                    report += f"#### {team_id}\n"
                    for member in members:
                        name = member.get('name ', '').strip()
                        student_id = member.get('student ID', '').strip()
                        gmail = member.get('Gmail ', '').strip()
                        whatsapp = member.get('WhatsApp ', '').strip()
                        
                        report += f"- **{name}** (ID: {student_id})\n"
                        if gmail:
                            report += f"  - Gmail: {gmail}\n"
                        if whatsapp:
                            report += f"  - WhatsApp: {whatsapp}\n"
                        report += "\n"
                    report += "\n"
    
    # Student list summary
    if "error" not in student_analysis:
        report += f"""### Official Student List
- **Total Students**: {student_analysis['total_students']}
- **Data Columns**: {', '.join(student_analysis['headers'])}

"""
    
    # Missing information
    report += """## 🚨 Missing Information Check

"""
    
    if "error" not in team_analysis:
        missing_gmail = []
        missing_whatsapp = []
        missing_drive_links = []
        
        for student in team_analysis['students']:
            name = student.get('name ', '').strip()
            if name:
                if not student.get('Gmail ', '').strip():
                    missing_gmail.append(name)
                if not student.get('WhatsApp ', '').strip():
                    missing_whatsapp.append(name)
                if not student.get('Google drive folder link', '').strip() or \
                   student.get('Google drive folder link', '').strip() == 'teacher to provide':
                    missing_drive_links.append(name)
        
        if missing_gmail:
            report += f"### Missing Gmail Addresses ({len(missing_gmail)} students)\n"
            for name in missing_gmail:
                report += f"- {name}\n"
            report += "\n"
        
        if missing_whatsapp:
            report += f"### Missing WhatsApp Numbers ({len(missing_whatsapp)} students)\n"
            for name in missing_whatsapp:
                report += f"- {name}\n"
            report += "\n"
        
        if missing_drive_links:
            report += f"### Need Google Drive Folder Links ({len(missing_drive_links)} students)\n"
            for name in missing_drive_links:
                report += f"- {name}\n"
            report += "\n"
    
    report += """## 🎯 Next Steps

1. **Complete Missing Information**: Contact students to provide missing Gmail/WhatsApp details
2. **Create Google Drive Folders**: Set up team folders with appropriate permissions
3. **Set Up WhatsApp Groups**: Create communication channels for each team
4. **Assign Topics**: Finalize project topics for each team
5. **Send Notifications**: Email students with their team assignments and folder links

## 📞 Action Items

- [ ] Follow up with students missing Gmail addresses
- [ ] Follow up with students missing WhatsApp numbers  
- [ ] Create Google Drive folders for all teams
- [ ] Set up team WhatsApp groups
- [ ] Finalize project topics and assign to teams
- [ ] Email team assignments to all students

---
*Generated automatically from Google Sheets data*
"""
    
    return report

def main():
    """Main extraction and analysis function"""
    
    print("🚀 GCAP3226 Group Formation Analysis (Fixed)")
    print("=" * 60)
    
    try:
        client = GoogleAPIClient()
        
        # URLs from your request
        team_url = "https://docs.google.com/spreadsheets/d/1lLcG1FMW7lYqw_O8kCs74nFJjFOwsuAe--Prg3qd45A/edit?usp=drivesdk"
        student_url = "https://docs.google.com/spreadsheets/d/1kMj-9Rto9NLtEpYSpDhAFwS7ylGHE2CSu0jRABKSNDg/edit?gid=482956640#gid=482956640"
        
        team_id = extract_spreadsheet_id(team_url)
        student_id = extract_spreadsheet_id(student_url)
        
        # Read data safely
        team_data, team_range = safe_read_data(client, team_id, "team formation data")
        student_data, student_range = safe_read_data(client, student_id, "student list data")
        
        # Analyze data
        print("\n" + "="*60)
        print("📊 ANALYZING DATA")
        print("="*60)
        
        team_analysis = analyze_team_data(team_data)
        student_analysis = analyze_student_list(student_data)
        
        # Create report
        report = create_detailed_report(team_analysis, student_analysis)
        
        # Save files
        report_file = "group_formation_update.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save raw data
        raw_data = {
            'timestamp': datetime.now().isoformat(),
            'team_formation': team_analysis,
            'student_list': student_analysis,
            'raw_team_data': team_data,
            'raw_student_data': student_data
        }
        
        with open("student_data_analysis.json", 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Report saved to: {report_file}")
        print(f"📊 Raw data saved to: student_data_analysis.json")
        
        # Print summary
        print(f"\n📋 SUMMARY:")
        if "error" not in team_analysis:
            print(f"✅ Team formation: {team_analysis['total_students']} students in {team_analysis['team_count']} teams")
        if "error" not in student_analysis:
            print(f"✅ Student list: {student_analysis['total_students']} official students")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 Analysis completed successfully!")
    else:
        print("❌ Analysis failed")
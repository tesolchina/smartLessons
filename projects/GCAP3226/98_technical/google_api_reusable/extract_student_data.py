"""
Extract Student Group Information from Google Sheets

This script reads the team formation and student list spreadsheets
and creates a comprehensive report.
"""

from google_api_client import GoogleAPIClient
import pandas as pd
from datetime import datetime

def extract_spreadsheet_id(url):
    """Extract spreadsheet ID from Google Sheets URL"""
    if '/d/' in url:
        return url.split('/d/')[1].split('/')[0]
    return url

def read_team_formation_data():
    """Read team formation and topic selection data"""
    
    client = GoogleAPIClient()
    
    # Team formation spreadsheet
    team_url = "https://docs.google.com/spreadsheets/d/1lLcG1FMW7lYqw_O8kCs74nFJjFOwsuAe--Prg3qd45A/edit?usp=drivesdk"
    team_id = extract_spreadsheet_id(team_url)
    
    print(f"📊 Reading team formation data...")
    print(f"Spreadsheet ID: {team_id}")
    
    # Try different sheet ranges to find the data
    possible_ranges = [
        "A:Z",  # Full sheet
        "Sheet1!A:Z",
        "Teams!A:Z", 
        "Form Responses 1!A:Z",
        "Team Formation!A:Z"
    ]
    
    team_data = None
    for range_name in possible_ranges:
        try:
            data = client.read_sheet_data(team_id, range_name)
            if data and len(data) > 1:  # Has header + data
                print(f"✅ Found data in range: {range_name}")
                team_data = data
                break
        except Exception as e:
            print(f"❌ Range {range_name} failed: {e}")
    
    return team_data, team_id

def read_student_list_data():
    """Read student list data"""
    
    client = GoogleAPIClient()
    
    # Student list spreadsheet
    student_url = "https://docs.google.com/spreadsheets/d/1kMj-9Rto9NLtEpYSpDhAFwS7ylGHE2CSu0jRABKSNDg/edit?gid=482956640#gid=482956640"
    student_id = extract_spreadsheet_id(student_url)
    
    print(f"📋 Reading student list data...")
    print(f"Spreadsheet ID: {student_id}")
    
    # Try different ranges
    possible_ranges = [
        "A:Z",
        "Sheet1!A:Z", 
        "Students!A:Z",
        "Class List!A:Z"
    ]
    
    student_data = None
    for range_name in possible_ranges:
        try:
            data = client.read_sheet_data(student_id, range_name)
            if data and len(data) > 1:
                print(f"✅ Found data in range: {range_name}")
                student_data = data
                break
        except Exception as e:
            print(f"❌ Range {range_name} failed: {e}")
    
    return student_data, student_id

def analyze_data(team_data, student_data):
    """Analyze and cross-reference the data"""
    
    print("\n" + "="*60)
    print("📊 DATA ANALYSIS")
    print("="*60)
    
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'team_formation': {},
        'student_list': {},
        'missing_students': [],
        'extra_students': [],
        'summary': {}
    }
    
    if team_data:
        print(f"\n📋 Team Formation Data ({len(team_data)} rows):")
        print("Headers:", team_data[0] if team_data else "No data")
        
        if len(team_data) > 1:
            # Convert to DataFrame for easier analysis
            df_teams = pd.DataFrame(team_data[1:], columns=team_data[0])
            
            print(f"Columns: {list(df_teams.columns)}")
            print(f"Sample data (first 3 rows):")
            for i, row in df_teams.head(3).iterrows():
                print(f"  Row {i+2}: {dict(row)}")
            
            analysis['team_formation'] = {
                'total_responses': len(df_teams),
                'columns': list(df_teams.columns),
                'sample_data': df_teams.head(3).to_dict('records')
            }
    
    if student_data:
        print(f"\n📚 Student List Data ({len(student_data)} rows):")
        print("Headers:", student_data[0] if student_data else "No data")
        
        if len(student_data) > 1:
            df_students = pd.DataFrame(student_data[1:], columns=student_data[0])
            
            print(f"Columns: {list(df_students.columns)}")
            print(f"Sample data (first 3 rows):")
            for i, row in df_students.head(3).iterrows():
                print(f"  Row {i+2}: {dict(row)}")
            
            analysis['student_list'] = {
                'total_students': len(df_students),
                'columns': list(df_students.columns),
                'sample_data': df_students.head(3).to_dict('records')
            }
    
    return analysis

def create_group_formation_report(analysis):
    """Create a comprehensive group formation report"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# GCAP3226 Group Formation and Topic Selection Update

**Generated**: {timestamp}

## 📊 Data Summary

### Team Formation Responses
- **Total Responses**: {analysis['team_formation'].get('total_responses', 'Not available')}
- **Data Columns**: {analysis['team_formation'].get('columns', 'Not available')}

### Official Student List  
- **Total Students**: {analysis['student_list'].get('total_students', 'Not available')}
- **Data Columns**: {analysis['student_list'].get('columns', 'Not available')}

## 📋 Detailed Analysis

### Team Formation Data Structure
"""
    
    if 'team_formation' in analysis and analysis['team_formation']:
        report += "```\n"
        for col in analysis['team_formation'].get('columns', []):
            report += f"- {col}\n"
        report += "```\n\n"
        
        if 'sample_data' in analysis['team_formation']:
            report += "**Sample Responses**:\n"
            for i, record in enumerate(analysis['team_formation']['sample_data']):
                report += f"{i+1}. {record}\n\n"
    
    if 'student_list' in analysis and analysis['student_list']:
        report += "### Student List Data Structure\n"
        report += "```\n"
        for col in analysis['student_list'].get('columns', []):
            report += f"- {col}\n"
        report += "```\n\n"
        
        if 'sample_data' in analysis['student_list']:
            report += "**Sample Student Records**:\n"
            for i, record in enumerate(analysis['student_list']['sample_data']):
                report += f"{i+1}. {record}\n\n"
    
    report += """
## 🎯 Next Steps

1. **Data Verification**: Cross-reference team formation responses with official student list
2. **Missing Information Check**: Identify students who haven't submitted team preferences
3. **Group Assignment**: Form balanced teams based on preferences and topics
4. **WhatsApp Group Creation**: Set up communication channels for each team
5. **Google Drive Setup**: Create team folders and collaborative documents

## 📞 Action Items

- [ ] Verify all student emails are valid Gmail addresses
- [ ] Check for duplicate responses or missing students
- [ ] Assign students to teams based on topic preferences
- [ ] Create WhatsApp groups for team communication
- [ ] Set up Google Drive folders with appropriate permissions
- [ ] Send team assignments and folder links to students

---
*This report was generated automatically from Google Sheets data*
"""
    
    return report

def main():
    """Main function to extract and analyze data"""
    
    print("🚀 GCAP3226 Group Formation Analysis")
    print("=" * 60)
    
    try:
        # Read team formation data
        team_data, team_id = read_team_formation_data()
        
        # Read student list data
        student_data, student_id = read_student_list_data()
        
        # Analyze data
        analysis = analyze_data(team_data, student_data)
        
        # Create report
        report = create_group_formation_report(analysis)
        
        # Save report
        output_file = "group_formation_update.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 Report saved to: {output_file}")
        
        # Also save raw data analysis
        import json
        with open("data_analysis.json", 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Raw analysis saved to: data_analysis.json")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    analysis = main()
    
    if analysis:
        print("\n🎉 Analysis completed successfully!")
        print("\nFiles created:")
        print("- group_formation_update.md (Human-readable report)")
        print("- data_analysis.json (Raw data for further processing)")
    else:
        print("❌ Analysis failed")
#!/usr/bin/env python3
"""
Fill SL Activities Table with data from CISL report
Based on the service-learning period from 23 May to 6 June
"""

import pandas as pd
from datetime import datetime, timedelta
import openpyxl

def create_sl_activities():
    """
    Create service-learning activities based on the CISL report
    SL period: 23 May to 6 June (2.5 weeks)
    """
    
    # Read the existing Excel file
    excel_path = '/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports/Table for SL activities_Template (Updated).xlsx'
    
    # Read the current data
    df_existing = pd.read_excel(excel_path)
    print("Current Excel content:")
    print(df_existing)
    print("\n" + "="*60 + "\n")
    
    # Create new activities based on the CISL report
    activities = []
    
    # Activity 1: Arrival and orientation
    activities.append({
        'Activity ': 'Arrival and orientation at Henan rural primary school',
        'Date': '2024-05-23',
        'Start Time ': '09:00:00',
        'End Time': '17:00:00',
        'Venue': 'Primary school in village, Henan Province',
        'Virtual / Physical': 'Physical',
        'Local / Non-local': 'Non-local'
    })
    
    # Activity 2: AI project team formation
    activities.append({
        'Activity ': 'Formation of 9 AI project teams and initial planning',
        'Date': '2024-05-24',
        'Start Time ': '10:00:00',
        'End Time': '16:00:00',
        'Venue': 'Primary school in village, Henan Province',
        'Virtual / Physical': 'Physical',
        'Local / Non-local': 'Non-local'
    })
    
    # Activity 3: Teaching classes - Week 1
    activities.append({
        'Activity ': 'Teaching classes to 80+ students across 6 grades (Week 1)',
        'Date': '2024-05-27',
        'Start Time ': '08:30:00',
        'End Time': '15:30:00',
        'Venue': 'Primary school in village, Henan Province',
        'Virtual / Physical': 'Physical',
        'Local / Non-local': 'Non-local'
    })
    
    # Activity 4: HTML/JavaScript game development
    activities.append({
        'Activity ': 'Development of educational games using HTML and JavaScript',
        'Date': '2024-05-29',
        'Start Time ': '14:00:00',
        'End Time': '18:00:00',
        'Venue': 'Primary school in village, Henan Province',
        'Virtual / Physical': 'Physical',
        'Local / Non-local': 'Non-local'
    })
    
    # Activity 5: Teaching classes - Week 2
    activities.append({
        'Activity ': 'Continued teaching delivery with prepared lesson plans',
        'Date': '2024-06-03',
        'Start Time ': '08:30:00',
        'End Time': '15:30:00',
        'Venue': 'Primary school in village, Henan Province',
        'Virtual / Physical': 'Physical',
        'Local / Non-local': 'Non-local'
    })
    
    # Activity 6: Cultural heritage exploration
    activities.append({
        'Activity ': 'Exploration of Chenqiao historic site and tourism potential',
        'Date': '2024-06-04',
        'Start Time ': '10:00:00',
        'End Time': '16:00:00',
        'Venue': 'Chenqiao area (陈桥兵变), Henan Province',
        'Virtual / Physical': 'Physical',
        'Local / Non-local': 'Non-local'
    })
    
    # Activity 7: AI project presentations
    activities.append({
        'Activity ': 'Final AI project presentations by 9 student teams',
        'Date': '2024-06-05',
        'Start Time ': '13:00:00',
        'End Time': '17:00:00',
        'Venue': 'Primary school in village, Henan Province',
        'Virtual / Physical': 'Physical',
        'Local / Non-local': 'Non-local'
    })
    
    # Activity 8: Program conclusion and departure
    activities.append({
        'Activity ': 'Program wrap-up, reflection session, and departure',
        'Date': '2024-06-06',
        'Start Time ': '09:00:00',
        'End Time': '14:00:00',
        'Venue': 'Primary school in village, Henan Province',
        'Virtual / Physical': 'Physical',
        'Local / Non-local': 'Non-local'
    })
    
    # Remove example rows and add new activities
    df_new = pd.DataFrame(activities)
    
    print("New activities to be added:")
    print(df_new.to_string(index=False))
    print(f"\nTotal activities: {len(activities)}")
    
    # Save to a new Excel file
    output_path = '/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports/Table for SL activities_Filled.xlsx'
    
    # Write to Excel
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_new.to_excel(writer, sheet_name='Sheet1', index=False)
    
    print(f"\n✅ New Excel file created: {output_path}")
    
    # Also save a backup version with both examples and new data
    backup_path = '/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports/Table for SL activities_Complete.xlsx'
    
    # Combine existing examples with new activities
    df_complete = pd.concat([df_existing, df_new], ignore_index=True)
    
    with pd.ExcelWriter(backup_path, engine='openpyxl') as writer:
        df_complete.to_excel(writer, sheet_name='Sheet1', index=False)
    
    print(f"✅ Complete file with examples: {backup_path}")
    
    return df_new

if __name__ == "__main__":
    print("🔄 Filling SL Activities Table based on CISL report...")
    print("📅 Service-Learning Period: 23 May to 6 June 2024")
    print("=" * 60)
    
    try:
        result_df = create_sl_activities()
        print("\n✨ Task completed successfully!")
        print("📊 Activities have been extracted from the CISL report and formatted for the Excel table.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check if the required packages are installed and files are accessible.")
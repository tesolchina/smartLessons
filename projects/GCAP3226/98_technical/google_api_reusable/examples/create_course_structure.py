"""
Example: Create Course Structure

This example shows how to create a complete course folder structure
with team folders and template documents.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from google_api_client import GoogleAPIClient

def create_course_structure(course_name, teams):
    """Create a complete course structure with team folders"""
    
    client = GoogleAPIClient()
    
    print(f"🎓 Creating structure for: {course_name}")
    print("=" * 50)
    
    # Create main course folder
    course_folder = client.create_folder(f"{course_name}_Course_Materials")
    print(f"📁 Main folder: {course_folder['webViewLink']}")
    
    # Create subfolders
    subfolders = [
        "01_Lectures",
        "02_Assignments", 
        "03_Resources",
        "04_Team_Projects"
    ]
    
    created_subfolders = {}
    for subfolder in subfolders:
        folder = client.create_folder(subfolder, course_folder['id'])
        created_subfolders[subfolder] = folder
        print(f"  📂 {subfolder}")
    
    # Create team folders
    team_parent = created_subfolders["04_Team_Projects"]
    
    print(f"\n👥 Creating {len(teams)} team folders...")
    
    for team in teams:
        # Create team folder
        team_folder = client.create_folder(
            f"Team_{team['name']}_{team['topic'].replace(' ', '_')}", 
            team_parent['id']
        )
        
        print(f"  📁 Team {team['name']}: {team['topic']}")
        
        # Create template documents for each team
        templates = [
            {"name": "Project_Proposal", "type": "document"},
            {"name": "Data_Analysis", "type": "spreadsheet"},
            {"name": "Final_Presentation", "type": "presentation"},
            {"name": "Meeting_Notes", "type": "document"}
        ]
        
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
            # Note: Presentations require different handling
            
            print(f"    📄 {template['name']}")
    
    print(f"\n🎉 Course structure created successfully!")
    print(f"🔗 Access here: {course_folder['webViewLink']}")
    
    return course_folder

# Example usage
if __name__ == "__main__":
    # Sample course data
    course_name = "GCAP3226"
    
    teams = [
        {"name": "Alpha", "topic": "Data Privacy in Healthcare"},
        {"name": "Beta", "topic": "AI Ethics in Education"},
        {"name": "Gamma", "topic": "Smart City Governance"},
        {"name": "Delta", "topic": "Digital Identity Management"}
    ]
    
    # Create the structure
    create_course_structure(course_name, teams)
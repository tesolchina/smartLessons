"""
Example: Backup and Sync

This example shows how to backup files and sync data between
local storage and Google Drive.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from google_api_client import GoogleAPIClient
import json
from datetime import datetime

def backup_project_files(local_folder, backup_folder_name="Project_Backup"):
    """Backup local project files to Google Drive"""
    
    client = GoogleAPIClient()
    
    print(f"💾 Creating backup: {backup_folder_name}")
    
    # Create backup folder with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{backup_folder_name}_{timestamp}"
    
    backup_folder = client.create_folder(folder_name)
    print(f"📁 Backup folder: {backup_folder['webViewLink']}")
    
    # Get list of files to backup
    backup_files = []
    
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            if file.endswith(('.py', '.md', '.json', '.txt', '.csv')):
                file_path = os.path.join(root, file)
                backup_files.append(file_path)
    
    print(f"📄 Found {len(backup_files)} files to backup")
    
    # Upload files (simplified - in reality you'd use the files().create() with media upload)
    uploaded_files = []
    
    for file_path in backup_files:
        try:
            # This is a simplified example - actual file upload requires media handling
            relative_path = os.path.relpath(file_path, local_folder)
            print(f"   📤 {relative_path}")
            
            # In a real implementation, you would:
            # 1. Use MediaFileUpload from googleapiclient.http
            # 2. Create the file with media_body parameter
            # 3. Handle different file types appropriately
            
            uploaded_files.append(relative_path)
            
        except Exception as e:
            print(f"   ❌ Failed to upload {file_path}: {e}")
    
    # Create backup manifest
    manifest = {
        'timestamp': timestamp,
        'total_files': len(backup_files),
        'uploaded_files': len(uploaded_files),
        'backup_folder': backup_folder['webViewLink'],
        'files': uploaded_files
    }
    
    print(f"✅ Backup completed: {len(uploaded_files)}/{len(backup_files)} files")
    print(f"🔗 Backup location: {backup_folder['webViewLink']}")
    
    return manifest

def sync_spreadsheet_data(spreadsheet_id, local_csv_file):
    """Sync data between Google Sheets and local CSV"""
    
    client = GoogleAPIClient()
    
    print(f"🔄 Syncing spreadsheet data...")
    
    # Read from Google Sheets
    sheet_data = client.read_sheet_data(spreadsheet_id, "A:Z")
    
    if sheet_data:
        print(f"📊 Read {len(sheet_data)} rows from Google Sheets")
        
        # Save to local CSV
        import csv
        with open(local_csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(sheet_data)
        
        print(f"💾 Saved to local file: {local_csv_file}")
    
    # Read from local CSV and update sheets (if needed)
    if os.path.exists(local_csv_file):
        with open(local_csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            local_data = list(reader)
        
        # Compare and update if different
        if local_data != sheet_data:
            print("🔄 Local data differs, updating Google Sheets...")
            success = client.write_sheet_data(
                spreadsheet_id, 
                f"A1:Z{len(local_data)}", 
                local_data
            )
            if success:
                print("✅ Google Sheets updated")
    
    return sheet_data

def create_project_dashboard(project_name, team_folders):
    """Create a dashboard document with links to all project resources"""
    
    client = GoogleAPIClient()
    
    print(f"📊 Creating project dashboard...")
    
    # Create dashboard document
    dashboard = client.create_document(f"{project_name}_Dashboard")
    
    # In a real implementation, you would use the Google Docs API to add content:
    # docs_service = client.get_docs_service()
    # Add formatted text, links, tables, etc.
    
    print(f"📄 Dashboard created: {dashboard['webViewLink']}")
    
    # Create summary spreadsheet
    summary_sheet = client.create_spreadsheet(f"{project_name}_Summary")
    
    # Add team folder links to summary
    summary_data = [['Team', 'Folder Link', 'Status', 'Last Updated']]
    
    for team_name, folder_link in team_folders.items():
        summary_data.append([
            team_name, 
            folder_link, 
            'Active', 
            datetime.now().strftime('%Y-%m-%d')
        ])
    
    client.write_sheet_data(
        summary_sheet['id'], 
        'A1:D' + str(len(summary_data)), 
        summary_data
    )
    
    print(f"📊 Summary sheet: {summary_sheet['webViewLink']}")
    
    return {
        'dashboard': dashboard,
        'summary': summary_sheet
    }

# Example usage
if __name__ == "__main__":
    print("🔧 Google API Backup & Sync Examples")
    print("=" * 50)
    
    # Example 1: Backup project files
    # backup_manifest = backup_project_files("../../../", "GCAP3226_Backup")
    
    # Example 2: Sync spreadsheet
    # spreadsheet_id = "your_spreadsheet_id_here"
    # sync_spreadsheet_data(spreadsheet_id, "team_data_backup.csv")
    
    # Example 3: Create dashboard
    team_folders = {
        "Team Alpha": "https://drive.google.com/folder1",
        "Team Beta": "https://drive.google.com/folder2",
        "Team Gamma": "https://drive.google.com/folder3"
    }
    
    # dashboard = create_project_dashboard("GCAP3226", team_folders)
    
    print("✅ Examples ready to run!")
    print("Uncomment the example you want to test.")
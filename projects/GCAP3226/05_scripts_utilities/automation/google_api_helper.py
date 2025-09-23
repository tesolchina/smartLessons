"""
Google API Helper for GCAP3226 Course Management

This module provides functionality to:
- Read team formation data from Google Sheets
- Create Google Drive folders for each team
- Set up permissions and template files
- Automate course administration tasks
"""

import os
import json
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path

from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleAPIHelper:
    """Helper class for Google API operations"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Google API services
        
        Args:
            config: Configuration dictionary with API settings
        """
        self.config = config
        self.credentials = self._get_credentials()
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        self.docs_service = build('docs', 'v1', credentials=self.credentials)
    
    def _get_credentials(self) -> Credentials:
        """Get Google API credentials from service account file"""
        service_account_file = self.config['SERVICE_ACCOUNT_FILE']
        scopes = self.config['SCOPES']
        
        if not os.path.exists(service_account_file):
            raise FileNotFoundError(f"Service account file not found: {service_account_file}")
        
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=scopes
        )
        
        return credentials
    
    def read_team_assignments(self, range_name: str = 'Teams!A:F') -> pd.DataFrame:
        """
        Read team assignment data from Google Sheets
        
        Args:
            range_name: Sheet range to read (default: 'Teams!A:F')
            
        Returns:
            DataFrame with team assignment data
        """
        try:
            spreadsheet_id = self.config['SPREADSHEET_ID']
            
            sheet = self.sheets_service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                raise ValueError("No data found in spreadsheet")
            
            # Convert to DataFrame
            df = pd.DataFrame(values[1:], columns=values[0])
            
            # Clean and validate data
            df = df.dropna(subset=['Team', 'Student_Name', 'Email'])
            
            print(f"📊 Read {len(df)} team assignments from spreadsheet")
            return df
            
        except HttpError as error:
            print(f"❌ Error reading spreadsheet: {error}")
            raise
    
    def create_team_folder(self, team_name: str, parent_folder_id: Optional[str] = None) -> str:
        """
        Create a Google Drive folder for a team
        
        Args:
            team_name: Name of the team
            parent_folder_id: ID of parent folder (optional)
            
        Returns:
            ID of created folder
        """
        try:
            folder_name = f"GCAP3226_Team_{team_name.replace(' ', '_')}"
            
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_folder_id:
                folder_metadata['parents'] = [parent_folder_id]
            
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id,name,webViewLink'
            ).execute()
            
            folder_id = folder.get('id')
            folder_link = folder.get('webViewLink')
            
            print(f"📁 Created folder for {team_name}: {folder_link}")
            return folder_id
            
        except HttpError as error:
            print(f"❌ Error creating folder for {team_name}: {error}")
            raise
    
    def set_folder_permissions(self, folder_id: str, email_list: List[str], role: str = 'writer') -> None:
        """
        Set permissions for a Google Drive folder
        
        Args:
            folder_id: ID of the folder
            email_list: List of email addresses to grant access
            role: Permission role ('reader', 'writer', 'owner')
        """
        try:
            for email in email_list:
                permission = {
                    'type': 'user',
                    'role': role,
                    'emailAddress': email.strip()
                }
                
                self.drive_service.permissions().create(
                    fileId=folder_id,
                    body=permission,
                    sendNotificationEmail=True,
                    emailMessage=f"You have been added to your GCAP3226 team folder. Happy collaborating!"
                ).execute()
            
            print(f"✅ Set permissions for {len(email_list)} team members")
            
        except HttpError as error:
            print(f"❌ Error setting permissions: {error}")
            raise
    
    def create_template_files(self, folder_id: str, templates: Dict[str, Dict]) -> List[Dict]:
        """
        Create template files in a team folder
        
        Args:
            folder_id: ID of the team folder
            templates: Dictionary of template configurations
            
        Returns:
            List of created file information
        """
        created_files = []
        
        try:
            for template_key, template_config in templates.items():
                file_name = template_config['name']
                file_type = template_config['type']
                
                # Set MIME type based on file type
                mime_types = {
                    'document': 'application/vnd.google-apps.document',
                    'spreadsheet': 'application/vnd.google-apps.spreadsheet',
                    'presentation': 'application/vnd.google-apps.presentation'
                }
                
                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id],
                    'mimeType': mime_types.get(file_type, 'application/vnd.google-apps.document')
                }
                
                file = self.drive_service.files().create(
                    body=file_metadata,
                    fields='id,name,webViewLink'
                ).execute()
                
                created_files.append({
                    'name': file_name,
                    'id': file.get('id'),
                    'link': file.get('webViewLink'),
                    'type': file_type
                })
            
            print(f"📄 Created {len(created_files)} template files")
            return created_files
            
        except HttpError as error:
            print(f"❌ Error creating template files: {error}")
            raise
    
    def setup_all_teams(self, team_data: pd.DataFrame, templates: Dict) -> List[Dict]:
        """
        Set up folders and files for all teams
        
        Args:
            team_data: DataFrame with team assignment data
            templates: Template configuration dictionary
            
        Returns:
            List of setup results for each team
        """
        results = []
        parent_folder_id = self.config.get('COURSE_FOLDER_ID')
        
        # Group by team
        teams = team_data.groupby('Team')
        
        print(f"🚀 Setting up {len(teams)} teams...")
        
        for team_name, members in teams:
            try:
                print(f"\n📋 Setting up team: {team_name}")
                
                # Create folder
                folder_id = self.create_team_folder(team_name, parent_folder_id)
                
                # Get member emails
                member_emails = members['Email'].tolist()
                member_names = members['Student_Name'].tolist()
                
                # Set permissions
                self.set_folder_permissions(folder_id, member_emails)
                
                # Create template files
                files = self.create_template_files(folder_id, templates)
                
                # Get folder link
                folder = self.drive_service.files().get(
                    fileId=folder_id,
                    fields='webViewLink'
                ).execute()
                
                team_result = {
                    'team_name': team_name,
                    'folder_id': folder_id,
                    'folder_link': folder.get('webViewLink'),
                    'members': [
                        {'name': name, 'email': email} 
                        for name, email in zip(member_names, member_emails)
                    ],
                    'files': files,
                    'status': 'success'
                }
                
                results.append(team_result)
                print(f"✅ Team {team_name} setup completed")
                
            except Exception as error:
                print(f"❌ Failed to setup team {team_name}: {error}")
                results.append({
                    'team_name': team_name,
                    'status': 'failed',
                    'error': str(error)
                })
        
        return results
    
    def update_team_folders_in_sheet(self, setup_results: List[Dict], 
                                    range_name: str = 'Teams!G:H') -> None:
        """
        Update the spreadsheet with folder links
        
        Args:
            setup_results: Results from team setup
            range_name: Range to update with folder links
        """
        try:
            # Prepare data for update
            values = [['Folder_Link', 'Setup_Status']]  # Headers
            
            for result in setup_results:
                if result['status'] == 'success':
                    values.append([result['folder_link'], 'Completed'])
                else:
                    values.append(['', f"Failed: {result.get('error', 'Unknown error')}"])
            
            body = {'values': values}
            
            spreadsheet_id = self.config['SPREADSHEET_ID']
            
            result = self.sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"📊 Updated spreadsheet with {result.get('updatedCells', 0)} cells")
            
        except HttpError as error:
            print(f"❌ Error updating spreadsheet: {error}")
            raise
    
    def get_folder_contents(self, folder_id: str) -> List[Dict]:
        """
        Get contents of a Google Drive folder
        
        Args:
            folder_id: ID of the folder
            
        Returns:
            List of files in the folder
        """
        try:
            query = f"'{folder_id}' in parents and trashed=false"
            
            results = self.drive_service.files().list(
                q=query,
                fields="files(id, name, mimeType, modifiedTime, webViewLink)"
            ).execute()
            
            items = results.get('files', [])
            return items
            
        except HttpError as error:
            print(f"❌ Error getting folder contents: {error}")
            raise


def test_api_connection(config: Dict[str, Any]) -> bool:
    """
    Test Google API connection
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        api_helper = GoogleAPIHelper(config)
        
        # Test Sheets API
        sheets_service = api_helper.sheets_service
        spreadsheet_id = config['SPREADSHEET_ID']
        
        result = sheets_service.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        ).execute()
        
        print(f"✅ Successfully connected to Google Sheets: {result.get('properties', {}).get('title')}")
        
        # Test Drive API
        drive_service = api_helper.drive_service
        results = drive_service.files().list(pageSize=1).execute()
        
        print("✅ Successfully connected to Google Drive")
        
        return True
        
    except Exception as error:
        print(f"❌ API connection test failed: {error}")
        return False


if __name__ == "__main__":
    # Example configuration
    config = {
        'SERVICE_ACCOUNT_FILE': 'credentials/gcap3226-service-account.json',
        'SPREADSHEET_ID': 'your_spreadsheet_id_here',
        'COURSE_FOLDER_ID': 'your_course_folder_id_here',
        'SCOPES': [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/documents'
        ]
    }
    
    # Test connection
    if test_api_connection(config):
        print("🎉 Google API setup is working correctly!")
    else:
        print("❌ Please check your configuration and credentials")
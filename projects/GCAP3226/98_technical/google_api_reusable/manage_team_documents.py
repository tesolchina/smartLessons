#!/usr/bin/env python3
"""
GCAP3226 Team Management Script
Handles Google Drive document management tasks:
1. Rename documents: Reflection_Essays_Team_X -> Presentation_outreach_Team_X
2. Create Google Slides presentations for each team
3. Create a master spreadsheet with tabs for each team
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from google_api_client import GoogleAPIClient

class GCAP3226TeamManager:
    def __init__(self):
        """Initialize the team manager with Google API client"""
        self.client = GoogleAPIClient()
        self.drive_service = self.client.get_drive_service()
        self.sheets_service = self.client.get_sheets_service()
        self.slides_service = self.client.get_slides_service()
        
        # Team data with folder IDs and details
        self.teams = {
            'Team_1': {
                'folder_id': '1zGDV77Vih4DxDyH9f6eKnr00Kp4nWyMo',
                'topic': 'Topic 6 - Flu Shot Participation Analysis',
                'members': ['Yeung Wing Yu', 'Kwok Tsz Yau', 'Tsoi Yik Hon', 'SuJiaLu']
            },
            'Team_2': {
                'folder_id': '1KJ8Y1QkDHo7Oull02GdfjP-OO0ZxJS3C',
                'topic': 'Topic 3 - Inter-Company Bus Route Coordination',
                'members': ['Chan Hei Tung', 'Yip Tsz Ying', 'Ko Man Wai', 'Wong Ling Yan Cassy', 'Tsoi Tsz Yan', 'Zi Xing Saul Ma']
            },
            'Team_3': {
                'folder_id': '1Gx9TD1fRxuzNinEIgLMdvC-pTALbf8fD',
                'topic': 'Topic 7 - Typhoon Signal Data Analysis',
                'members': ['Chen Man Ching', 'Hui Man Hei', 'HONG KAM YIN', 'Kung Tsz Lok', 'ZHENG ZIAN', 'Chan Ching Yin']
            },
            'Team_4': {
                'folder_id': '1yYR-KxSfSI3VT4M2yLbIbj4pVEHTS__f',
                'topic': 'Topic 4 - Municipal Solid Waste Charging Scheme',
                'members': ['Liu Wai Man', 'Kwok Lai Ki', 'Chan Tsz Ying', 'Wong Wai Lun']
            },
            'Team_5': {
                'folder_id': '1vgf2jvKYNJu9EO2eD8S_sOOvWSIVL_Dw',
                'topic': 'Topic 5 - Green@Community Recycling Network Analysis',
                'members': ['MAN Wai Yin', 'Chan Chi Ki', 'Tag Tsz Tung', 'HO Chun Chit', 'Xu Jingyi', 'Cheung Kwun Ho']
            },
            'Team_6': {
                'folder_id': '1WlruCUvqQ1IO5EOmYbUX0B4vMjF-zCNo',
                'topic': 'Topic 2 - Bus Stop Merger Optimization',
                'members': ['Tam Tin Chun', 'Chan Dik On', 'Wong Chun Hang']
            }
        }
        
        self.results = {
            'renamed_docs': [],
            'created_slides': [],
            'master_spreadsheet': None,
            'errors': []
        }

    def find_and_rename_documents(self):
        """Find and rename Reflection_Essays documents to Presentation_outreach"""
        print("🔍 Finding and renaming documents...")
        
        for team_name, team_data in self.teams.items():
            folder_id = team_data['folder_id']
            
            try:
                # Search for documents with "Reflection_Essays" in the name
                query = f"parents in '{folder_id}' and name contains 'Reflection_Essays'"
                results = self.drive_service.files().list(
                    q=query,
                    fields="files(id, name, mimeType)"
                ).execute()
                
                files = results.get('files', [])
                
                for file in files:
                    old_name = file['name']
                    
                    # Generate new name
                    if 'Reflection_Essays' in old_name:
                        new_name = old_name.replace('Reflection_Essays', 'Presentation_outreach')
                        
                        # Rename the file
                        self.drive_service.files().update(
                            fileId=file['id'],
                            body={'name': new_name}
                        ).execute()
                        
                        self.results['renamed_docs'].append({
                            'team': team_name,
                            'old_name': old_name,
                            'new_name': new_name,
                            'file_id': file['id']
                        })
                        
                        print(f"✅ {team_name}: Renamed '{old_name}' -> '{new_name}'")
                
            except Exception as e:
                error_msg = f"Error renaming documents for {team_name}: {str(e)}"
                print(f"❌ {error_msg}")
                self.results['errors'].append(error_msg)

    def create_team_presentations(self):
        """Create Google Slides presentations for each team"""
        print("\n🎨 Creating team presentations...")
        
        for team_name, team_data in self.teams.items():
            try:
                # Create a new presentation
                presentation_title = f"{team_name} - {team_data['topic']}"
                
                presentation = {
                    'title': presentation_title
                }
                
                created_presentation = self.slides_service.presentations().create(
                    body=presentation
                ).execute()
                
                presentation_id = created_presentation['presentationId']
                
                # Add content to the first slide
                slide_id = created_presentation['slides'][0]['objectId']
                
                # Add title and content
                requests = [
                    {
                        'replaceAllText': {
                            'containsText': {
                                'text': 'Click to add title'
                            },
                            'replaceText': f'GCAP3226 - {team_name}'
                        }
                    },
                    {
                        'replaceAllText': {
                            'containsText': {
                                'text': 'Click to add subtitle'
                            },
                            'replaceText': team_data['topic']
                        }
                    }
                ]
                
                self.slides_service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={'requests': requests}
                ).execute()
                
                # Move presentation to team folder
                self.drive_service.files().update(
                    fileId=presentation_id,
                    addParents=team_data['folder_id'],
                    removeParents='root'
                ).execute()
                
                self.results['created_slides'].append({
                    'team': team_name,
                    'title': presentation_title,
                    'presentation_id': presentation_id,
                    'url': f"https://docs.google.com/presentation/d/{presentation_id}"
                })
                
                print(f"✅ {team_name}: Created presentation '{presentation_title}'")
                
            except Exception as e:
                error_msg = f"Error creating presentation for {team_name}: {str(e)}"
                print(f"❌ {error_msg}")
                self.results['errors'].append(error_msg)

    def create_master_spreadsheet(self):
        """Create a master spreadsheet with tabs for each team"""
        print("\n📊 Creating master spreadsheet...")
        
        try:
            # Create new spreadsheet
            spreadsheet_title = "GCAP3226 - Team Resources Master Sheet"
            
            spreadsheet = {
                'properties': {
                    'title': spreadsheet_title
                }
            }
            
            created_spreadsheet = self.sheets_service.spreadsheets().create(
                body=spreadsheet
            ).execute()
            
            spreadsheet_id = created_spreadsheet['spreadsheetId']
            
            # Get the default sheet ID to rename it
            default_sheet_id = created_spreadsheet['sheets'][0]['properties']['sheetId']
            
            # Prepare batch requests
            requests = []
            
            # Rename the first sheet to "Overview"
            requests.append({
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': default_sheet_id,
                        'title': 'Overview'
                    },
                    'fields': 'title'
                }
            })
            
            # Add sheets for each team
            for team_name in self.teams.keys():
                requests.append({
                    'addSheet': {
                        'properties': {
                            'title': team_name
                        }
                    }
                })
            
            # Execute batch update
            self.sheets_service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={'requests': requests}
            ).execute()
            
            # Add content to Overview sheet
            overview_data = [
                ['GCAP3226 Team Resources Overview', '', '', ''],
                ['Generated:', '2025-09-23', '', ''],
                ['', '', '', ''],
                ['Team', 'Topic', 'Members', 'Drive Folder'],
            ]
            
            for team_name, team_data in self.teams.items():
                overview_data.append([
                    team_name,
                    team_data['topic'],
                    f"{len(team_data['members'])} members",
                    f"https://drive.google.com/drive/folders/{team_data['folder_id']}"
                ])
            
            # Update Overview sheet
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range='Overview!A1',
                valueInputOption='RAW',
                body={'values': overview_data}
            ).execute()
            
            # Add content to each team sheet
            for team_name, team_data in self.teams.items():
                team_data_sheet = [
                    [f'{team_name} Resources', '', ''],
                    ['Topic:', team_data['topic'], ''],
                    ['', '', ''],
                    ['Team Members:', '', ''],
                ]
                
                for i, member in enumerate(team_data['members'], 1):
                    team_data_sheet.append([f'{i}.', member, ''])
                
                team_data_sheet.extend([
                    ['', '', ''],
                    ['Resources & Links:', '', ''],
                    ['Type', 'Name', 'Link'],
                    ['Drive Folder', f'{team_name} Main Folder', f"https://drive.google.com/drive/folders/{team_data['folder_id']}"],
                    ['Document', 'Project Report', 'TBD'],
                    ['Document', 'Data Analysis Worksheet', 'TBD'],
                    ['Document', 'Presentation Outreach', 'TBD'],
                    ['Document', 'Meeting Notes', 'TBD'],
                    ['Slides', 'Team Presentation', 'TBD'],
                ])
                
                # Update team sheet
                self.sheets_service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range=f'{team_name}!A1',
                    valueInputOption='RAW',
                    body={'values': team_data_sheet}
                ).execute()
            
            self.results['master_spreadsheet'] = {
                'title': spreadsheet_title,
                'spreadsheet_id': spreadsheet_id,
                'url': f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
            }
            
            print(f"✅ Created master spreadsheet: '{spreadsheet_title}'")
            print(f"🔗 URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
            
        except Exception as e:
            error_msg = f"Error creating master spreadsheet: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['errors'].append(error_msg)

    def generate_report(self):
        """Generate a summary report of all actions taken"""
        print("\n📋 Generating summary report...")
        
        report = {
            'timestamp': '2025-09-23',
            'summary': {
                'documents_renamed': len(self.results['renamed_docs']),
                'presentations_created': len(self.results['created_slides']),
                'master_spreadsheet_created': self.results['master_spreadsheet'] is not None,
                'errors_count': len(self.results['errors'])
            },
            'details': self.results
        }
        
        # Save report to file
        report_file = current_dir / 'team_management_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {report_file}")
        
        # Display summary
        print("\n" + "="*60)
        print("📊 SUMMARY REPORT")
        print("="*60)
        print(f"✅ Documents renamed: {report['summary']['documents_renamed']}")
        print(f"✅ Presentations created: {report['summary']['presentations_created']}")
        print(f"✅ Master spreadsheet: {'Created' if report['summary']['master_spreadsheet_created'] else 'Failed'}")
        print(f"❌ Errors: {report['summary']['errors_count']}")
        
        if self.results['master_spreadsheet']:
            print(f"\n🔗 Master Spreadsheet: {self.results['master_spreadsheet']['url']}")
        
        if self.results['errors']:
            print("\n⚠️ Errors encountered:")
            for error in self.results['errors']:
                print(f"   - {error}")

    def run_all_tasks(self):
        """Execute all team management tasks"""
        print("🚀 Starting GCAP3226 Team Management Tasks")
        print("="*60)
        
        # Task 1: Rename documents
        self.find_and_rename_documents()
        
        # Task 2: Create presentations
        self.create_team_presentations()
        
        # Task 3: Create master spreadsheet
        self.create_master_spreadsheet()
        
        # Task 4: Generate report
        self.generate_report()
        
        print("\n🎉 All tasks completed!")

def main():
    """Main execution function"""
    try:
        manager = GCAP3226TeamManager()
        manager.run_all_tasks()
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
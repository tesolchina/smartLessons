#!/usr/bin/env python3
"""
Update GCAP3226 Master Spreadsheet with Direct Links
Populates each team tab with actual Google Drive document links
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

class SpreadsheetLinksUpdater:
    def __init__(self):
        """Initialize the spreadsheet updater with Google API client"""
        self.client = GoogleAPIClient()
        self.drive_service = self.client.get_drive_service()
        self.sheets_service = self.client.get_sheets_service()
        
        # Master spreadsheet ID from previous creation
        self.spreadsheet_id = "1yqJL5bDJW4N5YVKZFChKRJg5sI394mLbWIW-amamsEw"
        
        # Team data with folder IDs and document info
        self.teams = {
            'Team_1': {
                'folder_id': '1zGDV77Vih4DxDyH9f6eKnr00Kp4nWyMo',
                'topic': 'Topic 6 - Flu Shot Participation Analysis',
                'members': ['Yeung Wing Yu', 'Kwok Tsz Yau', 'Tsoi Yik Hon', 'SuJiaLu'],
                'presentation_id': '1y1J68c6MsDh-Cr9Yo7po6WfWRCFmOPUJqwJdQB6rD8k',
                'outreach_doc_id': '1jw9Il-7M_Az4MyiDvpovO85zu6c2gOOHtryB3cvOgv0'
            },
            'Team_2': {
                'folder_id': '1KJ8Y1QkDHo7Oull02GdfjP-OO0ZxJS3C',
                'topic': 'Topic 3 - Inter-Company Bus Route Coordination',
                'members': ['Chan Hei Tung', 'Yip Tsz Ying', 'Ko Man Wai', 'Wong Ling Yan Cassy', 'Tsoi Tsz Yan', 'Zi Xing Saul Ma'],
                'presentation_id': '1zX1Ruo6gDrXdg-Fe0s0CD0uiupXws_-zhBpMLSHMKoQ',
                'outreach_doc_id': '1gyDuHzUVeu7tsRSbdjchvk-qnGUBY5G4PxQw_xiiqMI'
            },
            'Team_3': {
                'folder_id': '1Gx9TD1fRxuzNinEIgLMdvC-pTALbf8fD',
                'topic': 'Topic 7 - Typhoon Signal Data Analysis',
                'members': ['Chen Man Ching', 'Hui Man Hei', 'HONG KAM YIN', 'Kung Tsz Lok', 'ZHENG ZIAN', 'Chan Ching Yin'],
                'presentation_id': '1njgegVqclzPpNoHbKonc4DJISC_YblZQB4TjBmiKey0',
                'outreach_doc_id': '1aQpajFFnWYKUTgNIfEynEh7-aGnKrpKqvLvdDs6YLcY'
            },
            'Team_4': {
                'folder_id': '1yYR-KxSfSI3VT4M2yLbIbj4pVEHTS__f',
                'topic': 'Topic 4 - Municipal Solid Waste Charging Scheme',
                'members': ['Liu Wai Man', 'Kwok Lai Ki', 'Chan Tsz Ying', 'Wong Wai Lun'],
                'presentation_id': '1dxTayyp0Cu5mrP_FmNfiEsYPRlOylWwX2-RkkcMciA0',
                'outreach_doc_id': '1ZobycX4pkblt_IIAY4XboXk9RO9KiZ8Wv2xmyOQe3zQ'
            },
            'Team_5': {
                'folder_id': '1vgf2jvKYNJu9EO2eD8S_sOOvWSIVL_Dw',
                'topic': 'Topic 5 - Green@Community Recycling Network Analysis',
                'members': ['MAN Wai Yin', 'Chan Chi Ki', 'Tag Tsz Tung', 'HO Chun Chit', 'Xu Jingyi', 'Cheung Kwun Ho'],
                'presentation_id': '10INBQvYBSJMMt28Y9kBUv3aZQFbvnTRfiCV9et5I-HQ',
                'outreach_doc_id': '1Yvq_8cChdYU7CagNlGZXJerReoNAGg1stVEGHkjtcWA'
            },
            'Team_6': {
                'folder_id': '1WlruCUvqQ1IO5EOmYbUX0B4vMjF-zCNo',
                'topic': 'Topic 2 - Bus Stop Merger Optimization',
                'members': ['Tam Tin Chun', 'Chan Dik On', 'Wong Chun Hang'],
                'presentation_id': '13hSo13-G7Q9cijEw7DPnE-GvNSc48JOqbfC5aagRhJA',
                'outreach_doc_id': '1eyr2zNqE38qHLZRgqljJfl7VKx0Fwc4odIKYC6nwITQ'
            }
        }
        
        self.results = {
            'teams_updated': [],
            'documents_found': {},
            'errors': []
        }

    def scan_team_folder_documents(self, team_name: str, folder_id: str):
        """Scan a team folder to find all documents and their types"""
        print(f"🔍 Scanning {team_name} folder for documents...")
        
        try:
            # Search for all files in the team folder
            query = f"parents in '{folder_id}'"
            results = self.drive_service.files().list(
                q=query,
                fields="files(id, name, mimeType, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            team_docs = {
                'google_docs': [],
                'google_sheets': [],
                'google_slides': [],
                'other_files': []
            }
            
            for file in files:
                file_info = {
                    'id': file['id'],
                    'name': file['name'],
                    'link': file['webViewLink'],
                    'mime_type': file['mimeType']
                }
                
                if file['mimeType'] == 'application/vnd.google-apps.document':
                    team_docs['google_docs'].append(file_info)
                elif file['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                    team_docs['google_sheets'].append(file_info)
                elif file['mimeType'] == 'application/vnd.google-apps.presentation':
                    team_docs['google_slides'].append(file_info)
                else:
                    team_docs['other_files'].append(file_info)
            
            self.results['documents_found'][team_name] = team_docs
            
            print(f"✅ {team_name}: Found {len(team_docs['google_docs'])} docs, {len(team_docs['google_sheets'])} sheets, {len(team_docs['google_slides'])} slides")
            
            return team_docs
            
        except Exception as e:
            error_msg = f"Error scanning {team_name} folder: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['errors'].append(error_msg)
            return None

    def update_team_spreadsheet_tab(self, team_name: str, team_data: dict, documents: dict):
        """Update a specific team tab with document links"""
        print(f"📝 Updating {team_name} spreadsheet tab...")
        
        try:
            # Prepare the data for the team sheet
            sheet_data = [
                [f'{team_name} Resources', '', ''],
                ['Topic:', team_data['topic'], ''],
                ['Folder Link:', f"https://drive.google.com/drive/folders/{team_data['folder_id']}", ''],
                ['', '', ''],
                ['Team Members:', '', ''],
            ]
            
            # Add team members
            for i, member in enumerate(team_data['members'], 1):
                sheet_data.append([f'{i}.', member, ''])
            
            # Add resources section
            sheet_data.extend([
                ['', '', ''],
                ['📄 GOOGLE DOCUMENTS', '', ''],
                ['Document Name', 'Link', 'Notes'],
            ])
            
            # Add Google Docs
            if documents and documents['google_docs']:
                for doc in documents['google_docs']:
                    sheet_data.append([doc['name'], doc['link'], 'Google Doc'])
            else:
                sheet_data.append(['No Google Docs found', '', ''])
            
            # Add Google Sheets section
            sheet_data.extend([
                ['', '', ''],
                ['📊 GOOGLE SHEETS', '', ''],
                ['Sheet Name', 'Link', 'Notes'],
            ])
            
            if documents and documents['google_sheets']:
                for sheet in documents['google_sheets']:
                    sheet_data.append([sheet['name'], sheet['link'], 'Google Sheet'])
            else:
                sheet_data.append(['No Google Sheets found', '', ''])
            
            # Add Google Slides section
            sheet_data.extend([
                ['', '', ''],
                ['🎯 GOOGLE SLIDES', '', ''],
                ['Presentation Name', 'Link', 'Notes'],
            ])
            
            if documents and documents['google_slides']:
                for slide in documents['google_slides']:
                    sheet_data.append([slide['name'], slide['link'], 'Google Slides'])
            else:
                sheet_data.append(['No Google Slides found', '', ''])
            
            # Add other files section
            if documents and documents['other_files']:
                sheet_data.extend([
                    ['', '', ''],
                    ['📁 OTHER FILES', '', ''],
                    ['File Name', 'Link', 'Type'],
                ])
                
                for file in documents['other_files']:
                    file_type = file['mime_type'].split('/')[-1] if '/' in file['mime_type'] else file['mime_type']
                    sheet_data.append([file['name'], file['link'], file_type])
            
            # Clear the existing content and update with new data
            # First, clear the sheet
            self.sheets_service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=f'{team_name}!A1:Z100'
            ).execute()
            
            # Then update with new content
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f'{team_name}!A1',
                valueInputOption='RAW',
                body={'values': sheet_data}
            ).execute()
            
            self.results['teams_updated'].append({
                'team': team_name,
                'docs_count': len(documents['google_docs']) if documents else 0,
                'sheets_count': len(documents['google_sheets']) if documents else 0,
                'slides_count': len(documents['google_slides']) if documents else 0,
                'other_count': len(documents['other_files']) if documents else 0
            })
            
            print(f"✅ {team_name}: Spreadsheet tab updated successfully")
            
        except Exception as e:
            error_msg = f"Error updating {team_name} spreadsheet tab: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['errors'].append(error_msg)

    def update_overview_tab(self):
        """Update the overview tab with summary information"""
        print("📋 Updating Overview tab...")
        
        try:
            overview_data = [
                ['GCAP3226 Team Resources Overview', '', '', ''],
                ['Generated:', '2025-09-23', '', ''],
                ['Spreadsheet ID:', self.spreadsheet_id, '', ''],
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
            
            # Add document summary
            overview_data.extend([
                ['', '', '', ''],
                ['DOCUMENT SUMMARY', '', '', ''],
                ['Team', 'Google Docs', 'Google Sheets', 'Google Slides'],
            ])
            
            for team_update in self.results['teams_updated']:
                overview_data.append([
                    team_update['team'],
                    str(team_update['docs_count']),
                    str(team_update['sheets_count']),
                    str(team_update['slides_count'])
                ])
            
            # Clear and update overview
            self.sheets_service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range='Overview!A1:Z100'
            ).execute()
            
            self.sheets_service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range='Overview!A1',
                valueInputOption='RAW',
                body={'values': overview_data}
            ).execute()
            
            print("✅ Overview tab updated successfully")
            
        except Exception as e:
            error_msg = f"Error updating Overview tab: {str(e)}"
            print(f"❌ {error_msg}")
            self.results['errors'].append(error_msg)

    def generate_report(self):
        """Generate a summary report of the spreadsheet update"""
        print("\n📋 Generating update report...")
        
        report = {
            'timestamp': '2025-09-23',
            'spreadsheet_id': self.spreadsheet_id,
            'spreadsheet_url': f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}",
            'summary': {
                'teams_processed': len(self.results['teams_updated']),
                'total_documents_found': sum(
                    len(docs['google_docs']) + len(docs['google_sheets']) + 
                    len(docs['google_slides']) + len(docs['other_files'])
                    for docs in self.results['documents_found'].values()
                ),
                'errors_count': len(self.results['errors'])
            },
            'details': self.results
        }
        
        # Save report to file
        report_file = current_dir / 'spreadsheet_update_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Report saved to: {report_file}")
        
        # Display summary
        print("\n" + "="*60)
        print("📊 SPREADSHEET UPDATE SUMMARY")
        print("="*60)
        print(f"✅ Teams processed: {report['summary']['teams_processed']}")
        print(f"✅ Documents catalogued: {report['summary']['total_documents_found']}")
        print(f"❌ Errors: {report['summary']['errors_count']}")
        
        print(f"\n🔗 Updated Spreadsheet: {report['spreadsheet_url']}")
        
        if self.results['errors']:
            print("\n⚠️ Errors encountered:")
            for error in self.results['errors']:
                print(f"   - {error}")
        
        # Display document counts by team
        print("\n📊 Documents by Team:")
        for team_name, docs in self.results['documents_found'].items():
            total = len(docs['google_docs']) + len(docs['google_sheets']) + len(docs['google_slides']) + len(docs['other_files'])
            print(f"   {team_name}: {total} total ({len(docs['google_docs'])} docs, {len(docs['google_sheets'])} sheets, {len(docs['google_slides'])} slides)")

    def run_update(self):
        """Execute the complete spreadsheet update process"""
        print("🚀 Starting GCAP3226 Spreadsheet Links Update")
        print("="*60)
        
        # Step 1: Scan all team folders for documents
        for team_name, team_data in self.teams.items():
            documents = self.scan_team_folder_documents(team_name, team_data['folder_id'])
            
            # Step 2: Update the team's spreadsheet tab
            if documents is not None:
                self.update_team_spreadsheet_tab(team_name, team_data, documents)
        
        # Step 3: Update the overview tab
        self.update_overview_tab()
        
        # Step 4: Generate report
        self.generate_report()
        
        print("\n🎉 Spreadsheet update completed!")

def main():
    """Main execution function"""
    try:
        updater = SpreadsheetLinksUpdater()
        updater.run_update()
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
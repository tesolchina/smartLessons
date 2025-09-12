# Generic Google Drive Project Manager

## Upload Files and Create Collaboration Documents for Any Project

import os
import sys
from pathlib import Path
import json
from datetime import datetime

# Add current directory to path for auth_setup
sys.path.append(str(Path(__file__).parent))

try:
    from auth_setup import authenticate_google_apis
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    APIS_AVAILABLE = True
except ImportError as e:
    print(f"Google APIs not available: {e}")
    APIS_AVAILABLE = False

class GenericProjectDriveManager:
    """Generic Google Drive manager for any project collaboration"""
    
    def __init__(self, project_path: str = "./", project_name: str = "Project"):
        self.project_path = Path(project_path)
        self.project_name = project_name
        self.setup_services()
        
    def setup_services(self):
        """Initialize Google API services"""
        if not APIS_AVAILABLE:
            print("📄 [OFFLINE MODE] Google APIs not available")
            self.drive_service = None
            self.docs_service = None
            return
            
        try:
            creds = authenticate_google_apis()
            if creds:
                self.drive_service = build('drive', 'v3', credentials=creds)
                self.docs_service = build('docs', 'v1', credentials=creds)
                print("✅ Google API services initialized")
            else:
                print("❌ Failed to authenticate with Google APIs")
                self.drive_service = None
                self.docs_service = None
        except Exception as e:
            print(f"❌ API setup error: {e}")
            self.drive_service = None
            self.docs_service = None
    
    def create_simon_notes_folder(self) -> str:
        """Create or find SimonNotes folder in Google Drive"""
        if not self.drive_service:
            print("📁 [OFFLINE] Would create SimonNotes folder")
            return "offline_folder_id"
        
        try:
            # Search for existing SimonNotes folder
            results = self.drive_service.files().list(
                q="name='SimonNotes' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields="files(id, name)"
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                folder_id = folders[0]['id']
                print(f"✅ Found existing SimonNotes folder: {folder_id}")
                return folder_id
            else:
                # Create new folder
                folder_metadata = {
                    'name': 'SimonNotes',
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                
                folder = self.drive_service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                
                folder_id = folder.get('id')
                print(f"✅ Created SimonNotes folder: {folder_id}")
                return folder_id
                
        except Exception as e:
            print(f"❌ Error with SimonNotes folder: {e}")
            return None
    
    def upload_project_plan(self, folder_id: str) -> dict:
        """Upload LLM Analysis Project Plan to Google Drive"""
        if not self.drive_service:
            print("📄 [OFFLINE] Would upload project plan")
            return {"file_id": "offline_file", "web_link": "offline_link"}
        
        try:
            plan_file = self.project_path / "LLM_Analysis_Project_Plan.md"
            
            if not plan_file.exists():
                print(f"❌ Project plan file not found: {plan_file}")
                return None
            
            # File metadata
            file_metadata = {
                'name': 'SCMP_GRF_LLM_Analysis_Project_Plan.md',
                'parents': [folder_id],
                'description': 'LLM-Enhanced Research Plan for SCMP Letters Citizenship Discourse Analysis'
            }
            
            # Upload file
            media = MediaFileUpload(
                str(plan_file),
                mimetype='text/markdown',
                resumable=True
            )
            
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            # Set sharing permissions (anyone with link can view)
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            
            self.drive_service.permissions().create(
                fileId=file.get('id'),
                body=permission
            ).execute()
            
            result = {
                'file_id': file.get('id'),
                'name': file.get('name'),
                'web_link': file.get('webViewLink')
            }
            
            print(f"✅ Uploaded project plan: {result['web_link']}")
            return result
            
        except Exception as e:
            print(f"❌ Error uploading project plan: {e}")
            return None
    
    def create_collaboration_doc(self, folder_id: str) -> dict:
        """Create Google Doc for Ben collaboration"""
        if not self.docs_service or not self.drive_service:
            print("📄 [OFFLINE] Would create collaboration document")
            return {"doc_id": "offline_doc", "web_link": "offline_link"}
        
        try:
            # Create document
            doc_title = f"SCMP GRF Project Discussion - {datetime.now().strftime('%B %Y')}"
            document = {
                'title': doc_title
            }
            
            doc = self.docs_service.documents().create(body=document).execute()
            doc_id = doc.get('documentId')
            
            # Move to SimonNotes folder
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=folder_id,
                fields='id,parents'
            ).execute()
            
            # Add content to document
            self.setup_collaboration_content(doc_id)
            
            # Set sharing permissions (anyone with link can edit)
            permission = {
                'type': 'anyone', 
                'role': 'writer'
            }
            
            self.drive_service.permissions().create(
                fileId=doc_id,
                body=permission
            ).execute()
            
            # Get web link
            file_info = self.drive_service.files().get(
                fileId=doc_id,
                fields='webViewLink'
            ).execute()
            
            result = {
                'doc_id': doc_id,
                'title': doc_title,
                'web_link': file_info.get('webViewLink')
            }
            
            print(f"✅ Created collaboration doc: {result['web_link']}")
            return result
            
        except Exception as e:
            print(f"❌ Error creating collaboration doc: {e}")
            return None
    
    def setup_collaboration_content(self, doc_id: str):
        """Add initial content to collaboration document"""
        if not self.docs_service:
            return
        
        content = f"""SCMP GRF Project Discussion & Updates
Generated: {datetime.now().strftime('%B %d, %Y')}

=== PROJECT STATUS UPDATE REQUEST ===

Hi Ben,

I've been working on the SCMP letters corpus analysis project and have made significant progress. Please see the attached project plan for full details.

🔄 CORPUS BUILDING UPDATE REQUEST

Current Status (from my end):
✅ Complete 6-year SCMP letters corpus downloaded (2018-2023)
✅ ~250,000 lines across 14 files 
✅ Existing processing tools (splitLetters06.py, metadata extraction)
✅ OpenRouter API configured for LLM analysis
✅ Research framework based on your GRF application analyzed

Questions for you:
1. How is the corpus building progressing on your end?
2. Are there additional data sources we should sync?
3. Any specific preprocessing requirements I should know about?

📄 LATEST GRF APPLICATION

Could you share:
- Your most recent GRF application (if different from the 2022/23 version I analyzed)
- Any updates to the research questions or methodology
- Current timeline and deliverable expectations

📚 RESEARCH LITERATURE SHARING

Please add any relevant literature to this folder:
- Recent papers on citizenship discourse in Hong Kong
- CDA methodology references  
- Corpus linguistics approaches you're using
- Hong Kong political discourse studies

I'll also add relevant papers I find during the research.

🤖 LLM INTEGRATION APPROACH

The plan outlines using LLM automation for:
- Citizenship type classification (5 categories: civic duty, democratic participation, cultural belonging, patriotic loyalty, oppositional critique)
- Argumentation structure analysis
- Temporal discourse shift detection across political events
- Issue classification and urgency assessment

Validation framework includes human-LLM comparison on 100 sample letters.

=== NEXT STEPS DISCUSSION ===

1. Review the attached project plan
2. Sync our corpus data and processing approaches
3. Coordinate LLM analysis pipeline development
4. Plan academic paper structure and conference submissions

Please add your thoughts, updates, and questions below:

[Ben's Response Section]




[Simon's Follow-up Notes]


---

📁 Related Files in This Folder:
- SCMP_GRF_LLM_Analysis_Project_Plan.md
- Research literature PDFs
- Corpus processing scripts
- Analysis results (to be added)
"""
        
        try:
            requests = [
                {
                    'insertText': {
                        'location': {'index': 1},
                        'text': content
                    }
                }
            ]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print("✅ Added collaboration content to document")
            
        except Exception as e:
            print(f"❌ Error adding content: {e}")
    
    def generate_summary_report(self, uploads: dict) -> dict:
        """Generate summary of all uploads and links"""
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'folder_created': uploads.get('folder_id') is not None,
            'project_plan_uploaded': uploads.get('project_plan') is not None,
            'collaboration_doc_created': uploads.get('collaboration_doc') is not None,
            'access_links': {},
            'next_actions': [
                'Share links with Ben via email/message',
                'Wait for Ben to add corpus updates and literature',
                'Sync folder contents to local project',
                'Begin LLM analysis pipeline development'
            ]
        }
        
        if uploads.get('project_plan'):
            summary['access_links']['project_plan'] = uploads['project_plan']['web_link']
        
        if uploads.get('collaboration_doc'):
            summary['access_links']['collaboration_doc'] = uploads['collaboration_doc']['web_link']
        
        return summary

def main():
    """Execute Google Drive setup and uploads"""
    
    print("=== SCMP GRF Project - Google Drive Integration ===")
    print("Creating SimonNotes folder and collaboration documents")
    print()
    
    # Initialize manager
    manager = GenericProjectDriveManager("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/BenSCMPGRF", "SCMP GRF Project")
    
    # Results tracking
    uploads = {}
    
    # Step 1: Create SimonNotes folder
    print("1️⃣ Creating SimonNotes folder...")
    folder_id = manager.create_simon_notes_folder()
    uploads['folder_id'] = folder_id
    
    if not folder_id:
        print("❌ Cannot proceed without folder. Exiting.")
        return
    
    # Step 2: Upload project plan
    print("\n2️⃣ Uploading LLM Analysis Project Plan...")
    project_plan_result = manager.upload_project_plan(folder_id)
    uploads['project_plan'] = project_plan_result
    
    # Step 3: Create collaboration document
    print("\n3️⃣ Creating collaboration document with Ben...")
    collab_doc_result = manager.create_collaboration_doc(folder_id)
    uploads['collaboration_doc'] = collab_doc_result
    
    # Step 4: Generate summary
    print("\n4️⃣ Generating summary report...")
    summary = manager.generate_summary_report(uploads)
    
    # Save summary locally
    summary_file = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/BenSCMPGRF/drive_upload_summary.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"💾 Summary saved to: {summary_file}")
    
    # Display results
    print("\n" + "="*60)
    print("🎉 GOOGLE DRIVE SETUP COMPLETE")
    print("="*60)
    
    if summary['access_links']:
        print("\n📂 Access Links:")
        for doc_type, link in summary['access_links'].items():
            print(f"  {doc_type}: {link}")
    
    print("\n📋 Next Actions:")
    for i, action in enumerate(summary['next_actions'], 1):
        print(f"  {i}. {action}")
    
    print(f"\n📁 All files organized in Google Drive SimonNotes folder")
    print(f"🔗 Share folder link with Ben for full access")
    
    return summary

if __name__ == "__main__":
    summary = main()

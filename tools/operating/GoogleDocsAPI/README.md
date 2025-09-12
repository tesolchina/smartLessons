# Google Docs API Setup for GCAP 3226 Team Management

*Created: September 6, 2025*

## 🎯 Project Goal

Create automated Google Docs API integration to:
- Generate team folders (1 folder + 1 doc per team)
- Manage team member information (names, emails, up to 5 members)
- Focus on data governance projects
- Enable script-based document editing and synchronization

## 🔧 API Setup Requirements

### Prerequisites
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Required Google Cloud Setup
1. **Google Cloud Console Project**
   - Create new project: "GCAP3226-TeamManager"
   - Enable Google Drive API
   - Enable Google Docs API
   - Enable Google Sheets API (for team data)

2. **Authentication Setup**
   - Create service account credentials
   - Download credentials JSON file
   - Set up OAuth 2.0 for user access

## 📁 Simple Team Structure

### Each Team Gets:
```
Team [XX] - [Data Governance Topic]/
└── Team_[XX]_Project_Document.docx
```

### Team Document Template:
```
# Team [XX] - Data Governance Project

## Team Information
- **Team Number**: [XX]
- **Project Topic**: [Data Governance Focus Area]
- **Members**: (Up to 5)
  1. Name: [Student Name] | Email: [student@hkbu.edu.hk]
  2. Name: [Student Name] | Email: [student@hkbu.edu.hk]
  3. Name: [Student Name] | Email: [student@hkbu.edu.hk]
  4. Name: [Student Name] | Email: [student@hkbu.edu.hk]
  5. Name: [Student Name] | Email: [student@hkbu.edu.hk]

## Data Governance Focus Area
- **Selected Topic**: [Choose from list below]
- **Research Question**: [To be defined by team]
- **Data Sources**: [Government databases, surveys, etc.]

## Project Timeline
- **Week 1-2**: Team formation and topic selection
- **Week 3-4**: Data collection planning
- **Week 5-8**: Data analysis and governance assessment
- **Week 9-12**: Report writing and recommendations
- **Week 13-14**: Presentation preparation

## Notes and Updates
[Team members can edit this section collaboratively]
```

## 🏛️ Data Governance Project Topics (10 Options)

1. **Government Open Data Policy Effectiveness**
2. **Personal Data Privacy in Smart City Initiatives**
3. **Healthcare Data Sharing and Patient Privacy**
4. **Education Data Governance in Digital Learning**
5. **Financial Data Security in Digital Banking**
6. **Transportation Data Ethics and Public Access**
7. **Social Media Data Governance and Youth**
8. **Environmental Data Transparency and Policy**
9. **Housing Data Analytics and Privacy Rights**
10. **Employment Data Governance and Discrimination**

## 🔧 Google Docs API Implementation

### 1. Authentication Setup
```python
# auth_setup.py
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets'
]

def authenticate_google_apis():
    """Set up Google API authentication"""
    creds = None
    
    # Check if we have saved credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds
```

### 2. Team Folder Creation
```python
# create_team_folders.py
from googleapiclient.discovery import build
from auth_setup import authenticate_google_apis

class TeamFolderManager:
    def __init__(self):
        self.creds = authenticate_google_apis()
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        
        # Main course folder ID
        self.course_folder_id = "1S4JMQSkIWAPhwKqUkKxfC6qqWewD6z8v"
    
    def create_team_folder(self, team_number, topic="TBD"):
        """Create a team folder with template document"""
        
        # Create team folder
        folder_name = f"Team {team_number:02d} - {topic}"
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [self.course_folder_id]
        }
        
        folder = self.drive_service.files().create(body=folder_metadata).execute()
        folder_id = folder.get('id')
        
        # Create team document
        doc_name = f"Team_{team_number:02d}_Project_Document"
        doc = self.docs_service.documents().create(
            body={'title': doc_name}
        ).execute()
        
        doc_id = doc.get('documentId')
        
        # Move document to team folder
        self.drive_service.files().update(
            fileId=doc_id,
            addParents=folder_id,
            removeParents=self.course_folder_id
        ).execute()
        
        # Add template content to document
        self.setup_document_template(doc_id, team_number, topic)
        
        return {
            'team_number': team_number,
            'folder_id': folder_id,
            'folder_name': folder_name,
            'doc_id': doc_id,
            'doc_name': doc_name
        }
    
    def setup_document_template(self, doc_id, team_number, topic):
        """Add template content to team document"""
        
        template_content = f"""Team {team_number:02d} - Data Governance Project

Team Information
Team Number: {team_number:02d}
Project Topic: {topic}
Members: (Up to 5)
1. Name: [Student Name] | Email: [student@hkbu.edu.hk]
2. Name: [Student Name] | Email: [student@hkbu.edu.hk]
3. Name: [Student Name] | Email: [student@hkbu.edu.hk]
4. Name: [Student Name] | Email: [student@hkbu.edu.hk]
5. Name: [Student Name] | Email: [student@hkbu.edu.hk]

Data Governance Focus Area
Selected Topic: [Choose from provided list]
Research Question: [To be defined by team]
Data Sources: [Government databases, surveys, etc.]

Project Timeline
Week 1-2: Team formation and topic selection
Week 3-4: Data collection planning
Week 5-8: Data analysis and governance assessment
Week 9-12: Report writing and recommendations
Week 13-14: Presentation preparation

Notes and Updates
[Team members can edit this section collaboratively]
"""
        
        requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': template_content
                }
            }
        ]
        
        self.docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

def create_all_teams():
    """Create folders and documents for all 10 teams"""
    
    data_governance_topics = [
        "Government Open Data Policy",
        "Personal Data Privacy in Smart Cities", 
        "Healthcare Data Sharing",
        "Education Data Governance",
        "Financial Data Security",
        "Transportation Data Ethics",
        "Social Media Data Governance",
        "Environmental Data Transparency",
        "Housing Data Analytics",
        "Employment Data Governance"
    ]
    
    manager = TeamFolderManager()
    team_info = []
    
    for i in range(1, 11):
        topic = data_governance_topics[i-1] if i <= len(data_governance_topics) else "TBD"
        result = manager.create_team_folder(i, topic)
        team_info.append(result)
        print(f"Created: Team {i:02d} - {topic}")
    
    return team_info

if __name__ == "__main__":
    teams = create_all_teams()
    print(f"Successfully created {len(teams)} team folders and documents!")
```

### 3. Document Reading and Writing
```python
# document_manager.py
from googleapiclient.discovery import build
from auth_setup import authenticate_google_apis
import re

class DocumentManager:
    def __init__(self):
        self.creds = authenticate_google_apis()
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
    
    def read_team_document(self, doc_id):
        """Read content from team document"""
        doc = self.docs_service.documents().get(documentId=doc_id).execute()
        content = self.extract_text_from_doc(doc)
        return content
    
    def extract_text_from_doc(self, doc):
        """Extract text content from document structure"""
        full_text = ""
        content = doc.get('body').get('content')
        
        for element in content:
            if 'paragraph' in element:
                elements = element.get('paragraph').get('elements')
                for elem in elements:
                    if 'textRun' in elem:
                        full_text += elem.get('textRun').get('content')
        
        return full_text
    
    def update_team_members(self, doc_id, team_members):
        """Update team member information in document"""
        
        # Build replacement requests
        requests = []
        
        for i, member in enumerate(team_members[:5], 1):
            old_text = f"{i}. Name: [Student Name] | Email: [student@hkbu.edu.hk]"
            new_text = f"{i}. Name: {member['name']} | Email: {member['email']}"
            
            requests.append({
                'replaceAllText': {
                    'containsText': {'text': old_text},
                    'replaceText': new_text
                }
            })
        
        if requests:
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
    
    def add_project_notes(self, doc_id, notes):
        """Add notes to the project document"""
        
        # Find the Notes section and append content
        doc = self.docs_service.documents().get(documentId=doc_id).execute()
        content = self.extract_text_from_doc(doc)
        
        # Find insertion point (after "Notes and Updates")
        notes_section_pos = content.find("Notes and Updates")
        if notes_section_pos != -1:
            # Calculate insertion index
            insertion_index = notes_section_pos + len("Notes and Updates\n")
            
            requests = [{
                'insertText': {
                    'location': {'index': insertion_index},
                    'text': f"\n{notes}\n"
                }
            }]
            
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()

def example_usage():
    """Example of how to use the document manager"""
    
    doc_manager = DocumentManager()
    
    # Example team members
    team_members = [
        {'name': 'Alice Wong', 'email': 'alice.wong@hkbu.edu.hk'},
        {'name': 'Bob Chen', 'email': 'bob.chen@hkbu.edu.hk'},
        {'name': 'Carol Li', 'email': 'carol.li@hkbu.edu.hk'},
        {'name': 'David Kim', 'email': 'david.kim@hkbu.edu.hk'}
    ]
    
    # Update team document (replace with actual doc ID)
    doc_id = "your_document_id_here"
    doc_manager.update_team_members(doc_id, team_members)
    doc_manager.add_project_notes(doc_id, "Team meeting scheduled for next week.")
    
    print("Document updated successfully!")

if __name__ == "__main__":
    example_usage()
```

### 4. Local Sync Integration
```python
# local_sync.py
import os
import json
from pathlib import Path
import shutil

class LocalSyncManager:
    def __init__(self, local_drive_path="/Users/simonwang/Google Drive"):
        self.local_drive_path = Path(local_drive_path)
        self.course_folder = self.local_drive_path / "GCAP 3226 - Student Teams"
        
    def sync_team_data(self, team_info_list):
        """Create local tracking files for team documents"""
        
        # Create local tracking directory
        tracking_dir = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226/team_tracking")
        tracking_dir.mkdir(exist_ok=True)
        
        # Save team information locally
        team_data = {
            'teams': team_info_list,
            'last_sync': str(datetime.now()),
            'course_folder_id': "1S4JMQSkIWAPhwKqUkKxfC6qqWewD6z8v"
        }
        
        with open(tracking_dir / "team_documents.json", 'w') as f:
            json.dump(team_data, f, indent=2)
        
        print(f"Team data synced locally to {tracking_dir}")
    
    def check_local_changes(self):
        """Check for local changes in Google Drive sync folder"""
        
        if not self.course_folder.exists():
            print(f"Local Google Drive folder not found: {self.course_folder}")
            return []
        
        # Look for team folders
        team_folders = [f for f in self.course_folder.iterdir() 
                       if f.is_dir() and "Team" in f.name]
        
        return team_folders

if __name__ == "__main__":
    sync_manager = LocalSyncManager()
    local_folders = sync_manager.check_local_changes()
    print(f"Found {len(local_folders)} local team folders")
```

## 📋 Setup Instructions

### Step 1: Google Cloud Setup (10 minutes)
1. Go to Google Cloud Console
2. Create new project: "GCAP3226-TeamManager"
3. Enable APIs: Drive, Docs, Sheets
4. Create service account and download credentials.json

### Step 2: Install Dependencies (2 minutes)
```bash
cd /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 3: Run Initial Setup (5 minutes)
```bash
python auth_setup.py  # First-time authentication
python create_team_folders.py  # Create all 10 team folders
```

### Step 4: Test Document Management (3 minutes)
```bash
python document_manager.py  # Test reading/writing documents
```

## 🎯 Benefits of This Approach

### Simplified Structure
- ✅ One folder + one document per team
- ✅ Clear team member tracking
- ✅ Focus on data governance topics
- ✅ Automated creation and management

### API Integration
- ✅ Programmatic document editing
- ✅ Automated team setup
- ✅ Local and cloud synchronization
- ✅ Scalable for future semesters

### Data Governance Focus
- ✅ 10 relevant topics prepared
- ✅ Hong Kong policy context
- ✅ Clear project structure
- ✅ Collaborative editing enabled

---

*This setup provides a streamlined, API-driven approach to team management while maintaining simplicity and focus on data governance projects.*

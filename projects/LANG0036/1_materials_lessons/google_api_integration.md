# Google API Integration for Course Management

## 🎯 **Project Goals**
- Access Google Sheets for team formation and topic selection
- Create Google Drive folders for each group automatically
- Edit and manage files programmatically
- Streamline course administration

---

## 🔧 **Google APIs Available**

### **1. Google Drive API**
- **Create/manage folders and files**
- **Set permissions and sharing**
- **Upload/download files**
- **Organize course materials**

### **2. Google Sheets API**
- **Read/write spreadsheet data**
- **Track team formations**
- **Manage topic selections**
- **Automate data processing**

### **3. Google Docs API**
- **Create and edit documents**
- **Generate assignment templates**
- **Collaborative document management**

---

## 🚀 **Setup Requirements**

### **Step 1: Enable Google APIs**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Google Drive API
   - Google Sheets API
   - Google Docs API (optional)

### **Step 2: Create Credentials**
1. Go to "Credentials" in Google Cloud Console
2. Create credentials → Service Account
3. Download the JSON key file
4. Or use OAuth 2.0 for user authentication

### **Step 3: Install Python Libraries**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install google-api-python-client
pip install pandas  # for data manipulation
```

---

## 💻 **Code Examples**

### **Google Sheets Integration**
```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

# Authentication
SERVICE_ACCOUNT_FILE = 'path/to/service-account-key.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Build services
sheets_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

# Read team formation data
def read_team_data(spreadsheet_id, range_name):
    sheet = sheets_service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    
    values = result.get('values', [])
    return pd.DataFrame(values[1:], columns=values[0])

# Update spreadsheet
def update_team_data(spreadsheet_id, range_name, values):
    body = {'values': values}
    
    result = sheets_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()
    
    return result
```

### **Google Drive Folder Management**
```python
# Create folder for each group
def create_group_folder(group_name, parent_folder_id=None):
    folder_metadata = {
        'name': f'Group_{group_name}',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    if parent_folder_id:
        folder_metadata['parents'] = [parent_folder_id]
    
    folder = drive_service.files().create(
        body=folder_metadata,
        fields='id'
    ).execute()
    
    return folder.get('id')

# Set folder permissions
def set_folder_permissions(folder_id, email_list):
    for email in email_list:
        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': email
        }
        
        drive_service.permissions().create(
            fileId=folder_id,
            body=permission,
            sendNotificationEmail=True
        ).execute()

# Create template files in folder
def create_template_files(folder_id, templates):
    created_files = []
    
    for template_name, template_content in templates.items():
        file_metadata = {
            'name': template_name,
            'parents': [folder_id],
            'mimeType': 'application/vnd.google-apps.document'
        }
        
        file = drive_service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()
        
        created_files.append({
            'name': template_name,
            'id': file.get('id')
        })
    
    return created_files
```

### **Complete Team Setup Automation**
```python
def setup_teams_from_sheet(spreadsheet_id, course_folder_id):
    # Read team data
    team_data = read_team_data(spreadsheet_id, 'Teams!A:E')
    
    # Group by team
    teams = team_data.groupby('Team')
    
    setup_results = []
    
    for team_name, members in teams:
        # Create folder
        folder_id = create_group_folder(team_name, course_folder_id)
        
        # Get member emails
        member_emails = members['Email'].tolist()
        
        # Set permissions
        set_folder_permissions(folder_id, member_emails)
        
        # Create template files
        templates = {
            'Project_Proposal.docx': '',
            'Meeting_Notes.docx': '',
            'Data_Analysis.docx': '',
            'Final_Report.docx': ''
        }
        
        files = create_template_files(folder_id, templates)
        
        setup_results.append({
            'team': team_name,
            'folder_id': folder_id,
            'members': member_emails,
            'files': files
        })
        
        print(f"✅ Setup completed for {team_name}")
    
    return setup_results
```

---

## 🛠️ **Practical Implementation**

### **Configuration File**
```python
# config.py
GOOGLE_CONFIGS = {
    'SERVICE_ACCOUNT_FILE': 'credentials/gcap3226-service-account.json',
    'SPREADSHEET_ID': 'your_google_sheet_id_here',
    'COURSE_FOLDER_ID': 'your_course_folder_id_here',
    'SCOPES': [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/documents'
    ]
}

TEAM_TEMPLATES = {
    'Project_Proposal': {
        'name': 'GCAP3226_Project_Proposal_Template',
        'type': 'document'
    },
    'Data_Collection': {
        'name': 'Data_Collection_Worksheet',
        'type': 'spreadsheet'
    },
    'Presentation': {
        'name': 'Final_Presentation_Template',
        'type': 'presentation'
    }
}
```

### **Main Execution Script**
```python
# team_setup.py
from google_api_helper import GoogleAPIHelper
from config import GOOGLE_CONFIGS, TEAM_TEMPLATES
import json

def main():
    # Initialize API helper
    api_helper = GoogleAPIHelper(GOOGLE_CONFIGS)
    
    print("🚀 Starting team setup automation...")
    
    # Read current team assignments
    teams = api_helper.read_team_assignments()
    
    # Create folders and setup for each team
    results = api_helper.setup_all_teams(teams, TEAM_TEMPLATES)
    
    # Save results
    with open('team_setup_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("✅ Team setup completed!")
    print(f"📁 Created {len(results)} team folders")
    
    # Update spreadsheet with folder links
    api_helper.update_team_folders_in_sheet(results)
    
    print("📊 Spreadsheet updated with folder links")

if __name__ == "__main__":
    main()
```

---

## 🔐 **Security Best Practices**

### **1. Service Account vs OAuth**
- **Service Account**: For automated scripts (recommended)
- **OAuth 2.0**: For user-interactive applications

### **2. Credential Management**
```python
# Store credentials securely
import os
from pathlib import Path

# Use environment variables
SERVICE_ACCOUNT_KEY = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY')

# Or store in secure location
CRED_PATH = Path.home() / '.gcap3226' / 'credentials.json'
```

### **3. Permission Management**
- Use least privilege principle
- Regular audit of folder permissions
- Remove access when students complete course

---

## 📋 **Implementation Checklist**

- [ ] Set up Google Cloud Project
- [ ] Enable required APIs
- [ ] Create service account credentials
- [ ] Install Python dependencies
- [ ] Test basic API connectivity
- [ ] Implement team data reading
- [ ] Create folder automation
- [ ] Set up permission management
- [ ] Test with sample data
- [ ] Deploy for course use

---

## 🎯 **Expected Workflow**

1. **Students fill team formation Google Sheet**
2. **Run automation script**
3. **Folders created automatically for each team**
4. **Permissions set for team members**
5. **Template files created in each folder**
6. **Spreadsheet updated with folder links**
7. **Email notifications sent to team members**

---

*This implementation will streamline your course administration and provide seamless integration with Google Workspace for GCAP3226.*
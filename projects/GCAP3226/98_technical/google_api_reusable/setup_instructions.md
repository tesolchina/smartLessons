# Google API Setup Instructions

## 🚀 **Quick Setup for Any Project**

### Step 1: Copy Files
Copy this entire folder to your new project:
```
google_api_reusable/
├── credentials_template.json ✅ Ready to use
├── google_api_client.py     ✅ Universal client
├── quick_test.py           ✅ Test script
├── requirements.txt        ✅ Dependencies
└── examples/               ✅ Sample code
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Test Connection
```bash
python quick_test.py
```

### Step 4: Start Using
```python
from google_api_client import GoogleAPIClient

# Initialize (handles authentication automatically)
client = GoogleAPIClient()

# Use any Google service
drive = client.get_drive_service()
sheets = client.get_sheets_service()
docs = client.get_docs_service()

# Or use convenience methods
folder = client.create_folder("My Project Folder")
doc = client.create_document("My Document", folder['id'])
```

## 🔧 **Available Services**

- **Google Drive**: Files, folders, permissions
- **Google Sheets**: Read, write, format spreadsheets  
- **Google Docs**: Create, edit documents
- **Gmail**: Send, read emails
- **Google Calendar**: Events, scheduling

## 🔒 **Authentication Details**

- **Client ID**: `584822767688-sljrj83d92o8l3efd7urg3il9unlca1b.apps.googleusercontent.com`
- **Client Secret**: `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`
- **Scopes**: Configured for Drive, Sheets, Docs by default
- **Token Storage**: Automatic refresh and storage

## 📋 **Common Use Cases**

### Create Project Structure
```python
client = GoogleAPIClient()

# Create main folder
project_folder = client.create_folder("My New Project")

# Create documents
client.create_document("Project Plan", project_folder['id'])
client.create_spreadsheet("Data Analysis", project_folder['id'])

# Set permissions
client.set_file_permissions(project_folder['id'], "team@example.com", "writer")
```

### Read/Write Spreadsheets
```python
# Read data
data = client.read_sheet_data("spreadsheet_id", "Sheet1!A1:C10")

# Write data
new_data = [["Name", "Email", "Role"], ["John", "john@example.com", "Admin"]]
client.write_sheet_data("spreadsheet_id", "Sheet1!A1:C2", new_data)
```

### Manage Files
```python
# List files
recent_files = client.list_files("mimeType='application/pdf'", max_results=20)

# Create folders with hierarchy
parent = client.create_folder("Course Materials")
team1 = client.create_folder("Team Alpha", parent['id'])
team2 = client.create_folder("Team Beta", parent['id'])
```

## 🚨 **Troubleshooting**

### "Credentials not found"
- Make sure `credentials_template.json` exists in the folder
- Check that the file has valid JSON format

### "Authentication failed"
- Run `python quick_test.py` to debug
- Check internet connection
- Verify the client secret is correct

### "Permission denied"
- Enable required APIs in Google Cloud Console:
  - Google Drive API
  - Google Sheets API  
  - Google Docs API
- Check OAuth consent screen is configured

### "Token expired"
- Delete `token.json` file and re-authenticate
- The client will automatically handle token refresh

## 📞 **Support**

For specific project needs:
1. Check the `examples/` folder for sample code
2. Run `python quick_test.py` to verify setup
3. Use the built-in error messages for debugging

---

**Last Updated**: September 22, 2025  
**Tested With**: GCAP3226 Project ✅
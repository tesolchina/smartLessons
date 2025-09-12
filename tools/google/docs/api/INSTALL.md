# Google Docs API Installation Guide

## Quick Setup

Run this script to install all required packages for the GCAP 3226 team management system:

```bash
# Install Google API packages
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install google-api-python-client

# Alternative: Install all at once
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Package Details

### Core Google API Packages
- **google-auth**: Authentication and authorization library
- **google-auth-oauthlib**: OAuth 2.0 helpers for Google APIs  
- **google-auth-httplib2**: HTTP transport adapter
- **google-api-python-client**: Google API client library

### Installation Verification

After installation, run this to verify:

```python
# Test import
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    print("✅ All Google API packages installed successfully!")
except ImportError as e:
    print(f"❌ Missing package: {e}")
```

## Usage Flow

1. **Install packages** (above)
2. **Run authentication setup**: `python auth_setup.py`
3. **Create team structure**: `python team_manager.py`
4. **Edit documents**: `python document_editor.py`
5. **Manage locally**: `python local_manager.py`

## Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "GCAP3226-TeamManager"
3. Enable APIs:
   - Google Drive API
   - Google Docs API
   - Google Sheets API (optional)
4. Create OAuth 2.0 credentials
5. Download as `credentials.json`
6. Place in the GoogleDocsAPI folder

## Troubleshooting

### Common Issues

**ImportError**: Install packages with pip as shown above

**Authentication Failed**: 
- Check `credentials.json` is in the correct location
- Ensure APIs are enabled in Google Cloud Console
- Run `python auth_setup.py` to re-authenticate

**Offline Mode**: 
- Scripts will work in offline mode for testing
- Use `local_manager.py` for offline document management

## Files Overview

- `auth_setup.py` - Google API authentication
- `team_manager.py` - Create team folders and documents
- `document_editor.py` - Read and edit team documents  
- `local_manager.py` - Local backup and offline management
- `requirements.txt` - Package dependencies (generated)

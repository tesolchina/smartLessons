# Google API Automation for GCAP3226

This folder contains scripts to automate Google Drive folder creation and management for student teams in GCAP3226.

## Files

- `google_api_helper.py` - Main helper class for Google API operations
- `team_setup.py` - Script to automate team folder creation
- `config.json` - Configuration file (needs customization)
- `test_setup.py` - Quick test script to verify setup
- `requirements.txt` - Python package dependencies

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google API credentials:**
   - Follow the guide in `../../../google_api_integration.md`
   - Place your service account JSON file in `credentials/` folder

3. **Configure the system:**
   - Edit `config.json` with your actual IDs and settings
   - Update SPREADSHEET_ID with your Google Sheets ID
   - Update COURSE_FOLDER_ID with your course folder ID (optional)

4. **Test the setup:**
   ```bash
   python test_setup.py
   ```

5. **Run team setup (test mode first):**
   ```bash
   python team_setup.py --test-only
   ```

6. **Create team folders:**
   ```bash
   python team_setup.py
   ```

## Configuration

Edit `config.json` to customize:
- Spreadsheet ID and ranges
- Template files for each team
- Permission settings
- Notification messages

## Features

- ✅ Read team assignments from Google Sheets
- ✅ Create individual team folders in Google Drive
- ✅ Set up appropriate permissions for team members
- ✅ Create template files (documents, spreadsheets, presentations)
- ✅ Update spreadsheet with folder links
- ✅ Comprehensive error handling and logging
- ✅ Test mode for safe verification

## Support

For issues or questions, refer to the main documentation in `google_api_integration.md`.
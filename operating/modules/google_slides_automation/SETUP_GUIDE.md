# Google Slides Automation Setup Guide

Upload PowerPoint presentations to Google Slides and set sharing permissions automatically.

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
cd /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/google_slides_automation
pip install -r requirements.txt
```

### 2. Google Cloud Console Setup

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create or select a project**
3. **Enable APIs**:
   - Google Slides API
   - Google Drive API

#### Enable APIs:
- Go to "APIs & Services" > "Library"
- Search for "Google Slides API" → Enable
- Search for "Google Drive API" → Enable

### 3. Create OAuth Credentials

1. **Go to "APIs & Services" > "Credentials"**
2. **Click "Create Credentials" > "OAuth 2.0 Client ID"**
3. **Configure consent screen** (if first time):
   - User Type: External
   - App name: "HKBU LANG 2077 Slides"
   - User support email: your email
   - Developer email: your email
4. **Create OAuth Client**:
   - Application type: Desktop application
   - Name: "HKBU Slides Uploader"
5. **Download JSON file** and rename to `credentials.json`
6. **Place in this folder**: `/Users/simonwang/.../google_slides_automation/credentials.json`

### 4. Run the Upload Script

```bash
python3 google_slides_uploader.py
```

## 🎯 Features

### Automatic Upload
- ✅ Finds your latest PowerPoint presentation
- ✅ Uploads to Google Slides
- ✅ Sets "anyone with link can edit" permissions
- ✅ Returns shareable link

### Interactive Manager
```bash
python3 -c "from google_slides_uploader import interactive_slides_manager; interactive_slides_manager()"
```

### Batch Processing
Upload multiple presentations at once with custom titles and permissions.

## 📊 Usage Examples

### Basic Upload
```python
from google_slides_uploader import GoogleSlidesUploader

uploader = GoogleSlidesUploader()
uploader.setup_credentials()

# Upload PowerPoint
result = uploader.upload_powerpoint_to_slides(
    'LANG2077_slides.pptx',
    title='LANG 2077: AI Partnership Skills'
)

# Set sharing permissions
uploader.set_sharing_permissions(result['id'], 'anyone', 'writer')

# Get shareable link
link = uploader.get_shareable_link(result['id'])
print(f"Share this link: {link}")
```

### Advanced Usage
```python
# Upload with custom settings
result = uploader.upload_powerpoint_to_slides(
    pptx_path='/path/to/slides.pptx',
    title='Custom Title'
)

# Different permission levels
uploader.set_sharing_permissions(result['id'], 'anyone', 'reader')  # View only
uploader.set_sharing_permissions(result['id'], 'anyone', 'writer')  # Can edit
uploader.set_sharing_permissions(result['id'], 'anyone', 'commenter')  # Can comment
```

## 🔐 Authentication Flow

1. **First run**: Opens browser for Google authentication
2. **Consent**: Grant permissions for Slides and Drive access
3. **Token saved**: Future runs use saved credentials
4. **Auto-refresh**: Handles token expiration automatically

## 📁 File Structure

```
google_slides_automation/
├── google_slides_uploader.py    # Main upload script
├── requirements.txt             # Python dependencies  
├── credentials.json            # OAuth credentials (you create)
├── token.pickle               # Saved auth tokens (auto-created)
├── upload_result.json         # Last upload details
└── SETUP_GUIDE.md            # This file
```

## 🎓 LANG 2077 Integration

### Automatic Detection
- Finds PowerPoint files from canva_automation folder
- Uses latest modified file
- Applies HKBU branding and course title

### Sharing Settings
- Default: "Anyone with link can edit"
- Perfect for student collaboration
- Easy sharing via link

## 🚨 Troubleshooting

### Common Issues

**"credentials.json not found"**
- Download OAuth credentials from Google Cloud Console
- Rename to exactly `credentials.json`
- Place in the google_slides_automation folder

**"Permission denied" errors**
- Check if APIs are enabled in Google Cloud Console
- Verify OAuth consent screen is configured
- Try refreshing authentication: delete `token.pickle`

**"Quota exceeded" errors**
- Google Slides API has usage limits
- Wait a few minutes between uploads
- Consider batching operations

### Reset Authentication
```bash
# Delete saved token to re-authenticate
rm token.pickle
python3 google_slides_uploader.py
```

## 📈 Advanced Features

### Batch Upload Multiple Files
```python
pptx_files = [
    'LANG2077_week1.pptx',
    'LANG2077_week2.pptx', 
    'LANG2077_week3.pptx'
]

for file in pptx_files:
    result = uploader.upload_powerpoint_to_slides(file)
    uploader.set_sharing_permissions(result['id'], 'anyone', 'writer')
    print(f"Uploaded: {result['name']} - {result['url']}")
```

### Custom Sharing Settings
```python
# Different permission levels
permissions = {
    'students': ('anyone', 'writer'),      # Can edit
    'instructors': ('anyone', 'reader'),   # View only
    'reviewers': ('anyone', 'commenter')   # Can comment
}

for role, (type, level) in permissions.items():
    uploader.set_sharing_permissions(presentation_id, type, level)
```

## 🔗 Useful Links

- **Google Cloud Console**: https://console.cloud.google.com/
- **Google Slides API Docs**: https://developers.google.com/slides
- **Google Drive API Docs**: https://developers.google.com/drive
- **OAuth Setup Guide**: https://developers.google.com/workspace/guides/create-credentials

## ✅ Next Steps

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Set up Google Cloud project** and download credentials
3. **Run upload script**: `python3 google_slides_uploader.py`
4. **Share the link** with students for collaboration

Your LANG 2077 slides will be uploaded and ready for "anyone with link can edit" sharing! 🎓

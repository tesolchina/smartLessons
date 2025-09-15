# 🔐 Security Migration Guide: Moving from Hardcoded Credentials to Environment Variables

## ⚠️ CRITICAL SECURITY UPDATE

**All Google API credentials have been removed from the repository and moved to environment variables to prevent accidental exposure.**

## What Changed

### ❌ Old (Insecure) Approach
```python
# DON'T DO THIS ANYMORE - credentials exposed in repo
credentials_path = '/path/to/credentials.json'
token_path = '/path/to/token.pickle'
```

### ✅ New (Secure) Approach
```python
# USE THIS - credentials loaded from environment variables
from config.google_auth_secure import get_docs_service, get_slides_service

# Get authenticated service directly
docs_service = get_docs_service()
slides_service = get_slides_service()
```

## Setup Instructions

### 1. Create Your .env File
```bash
# Copy the template
cp .env.template .env

# Edit with your actual credentials
nano .env
```

### 2. Get Your Google API Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create new one)
3. Enable APIs: Google Docs API, Google Slides API
4. Create OAuth 2.0 Client ID credentials
5. Download the JSON file and extract these values:

### 3. Fill in .env File
```bash
# Google Docs API
GOOGLE_DOCS_CLIENT_ID="your-client-id.apps.googleusercontent.com"
GOOGLE_DOCS_CLIENT_SECRET="GOCSPX-your-client-secret"
GOOGLE_DOCS_PROJECT_ID="your-project-id"

# Google Slides API  
GOOGLE_SLIDES_CLIENT_ID="your-client-id.apps.googleusercontent.com"
GOOGLE_SLIDES_CLIENT_SECRET="GOCSPX-your-client-secret"
GOOGLE_SLIDES_PROJECT_ID="your-project-id"
```

## Code Migration Examples

### Before (Insecure)
```python
def authenticate():
    creds = None
    token_path = '/absolute/path/to/token.pickle'
    credentials_path = '/absolute/path/to/credentials.json'
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('docs', 'v1', credentials=creds)
```

### After (Secure)
```python
from config.google_auth_secure import get_docs_service

def get_authenticated_service():
    return get_docs_service()
```

## Files That Need Updates

### High Priority (Contains hardcoded paths)
- `projects/Donald/add_visible_message.py`
- `projects/Donald/debug_comments.py` 
- `projects/Donald/comment_donald_only.py`
- `projects/Donald/add_academic_comments.py`
- `tools/cli/pyscripts/reference_letter_doc_creator.py`
- `tools/google/slides/automation/legacy_modules/google_slides_modules/google_slides_uploader.py`

### Update Pattern
Replace authentication functions with:
```python
# At the top of the file
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2] / "config"))
from google_auth_secure import get_docs_service, get_slides_service

# Replace your authenticate() function with:
def authenticate():
    return get_docs_service()  # or get_slides_service()
```

## Security Benefits

✅ **No credentials in version control**  
✅ **Environment variable isolation**  
✅ **Automatic temp file cleanup**  
✅ **Secure token storage in user home directory**  
✅ **Easy credential rotation**  
✅ **No accidental exposure in commits**

## Token Storage

Tokens are now stored securely in:
```
~/.dailyassistant/tokens/
├── token_docs.pickle
└── token_slides.pickle
```

This is outside your repository and won't be accidentally committed.

## Troubleshooting

### "Module not found: secure_config"
- Make sure you're running from the repository root
- Check that `config/secure_config.py` exists
- Add the config path to your Python path

### "Missing required Google credentials"
- Check your `.env` file exists in repo root
- Verify all required environment variables are set
- Make sure variable names match exactly (case sensitive)

### "Authentication failed"
- Check your Google Cloud Console project settings
- Ensure APIs are enabled
- Verify OAuth client ID is correctly configured
- Check that redirect URI includes `http://localhost`

## Testing Your Setup

```bash
# Test the secure config system
cd /path/to/DailyAssistant
python3 config/secure_config.py

# Test Google authentication
python3 config/google_auth_secure.py
```

## URGENT: Historical Cleanup

**Your Git history still contains the exposed credentials!**

If you've already pushed commits with credentials, you need to:

1. **Immediately revoke the exposed credentials** in Google Cloud Console
2. **Generate new credentials** 
3. **Clean git history** (optional but recommended):
   ```bash
   # Use git filter-branch or BFG Repo Cleaner to remove sensitive files
   # from git history - this is advanced and can break things
   ```

## Questions?

- Check `config/secure_config.py` for implementation details
- See `config/google_auth_secure.py` for authentication examples
- Review `.env.template` for required variables

---

**Remember: NEVER commit .env files or any files containing real credentials!**
# Google API Authentication Instructions

## Current Status
✅ Google API credentials are set up
🔄 OAuth authorization is in progress
📋 Waiting for you to complete authorization

## Steps to Complete Authentication

### 1. Visit the Authorization URL
Copy and paste this URL into your browser:

```
https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=452791587294-ekajpgekfo12mcl379fmmgl70idf1ai4.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A61194%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdocuments&state=vjhmW3n5JJ7kMQuFRGAG721Zs9ZieA&access_type=offline
```

### 2. Authorize the Application
1. Sign in to your Google account
2. Review the permissions request (access to Google Docs)
3. Click "Allow" to authorize the application

### 3. Complete the Process
- The browser will redirect to localhost
- The terminal will show a success message
- A `token.pickle` file will be created for future use

## What This Enables

Once authenticated, you'll be able to:

### Read Operations
```bash
# Read all project documents
python gcap3056_google_docs_manager.py --read-all

# Read specific project
python gcap3056_google_docs_manager.py --read-project "energy_poverty"

# Sync all documents locally
python gcap3056_google_docs_manager.py --sync-all
```

### Write Operations
```bash
# Add text to a project document
python gcap3056_google_docs_manager.py --write-project "energy_poverty" --text "Your update here"

# Add timestamp update
python gcap3056_google_docs_manager.py --write-project "energy_poverty" --add-timestamp --timestamp-message "Weekly progress update"
```

## Project Documents Available

1. **energy_poverty** - Energy poverty research project
2. **hko_chatbot** - HKO chatbot development
3. **chronic_disease_co_care** - Chronic disease co-care pilot scheme
4. **anti_scamming_education** - Anti-scamming education emergency alert system
5. **emergency_alert_system** - Emergency Alert System project

## Next Steps After Authentication

1. Test reading a document: `python gcap3056_google_docs_manager.py --read-project "energy_poverty"`
2. Sync all documents locally: `python gcap3056_google_docs_manager.py --sync-all`
3. Try adding an update: `python gcap3056_google_docs_manager.py --write-project "energy_poverty" --add-timestamp`

The authentication only needs to be done once. After that, the script will automatically use the saved credentials.

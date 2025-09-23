# Google Drive API Setup Guide for GCAP3226

## 🔧 Quick Setup Steps

You have the **Client ID**: `584822767688-sljrj83d92o8l3efd7urg3il9unlca1b.apps.googleusercontent.com`

Now you need to get the **Client Secret** to complete the setup.

### Step 1: Get Your Client Secret

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Select your project** (or create one if needed)
3. **Navigate to**: APIs & Services > Credentials
4. **Find your OAuth 2.0 Client ID**: `584822767688-sljrj83d92o8l3efd7urg3il9unlca1b`
5. **Click on the client ID** to view details
6. **Copy the Client Secret**

### Step 2: Update Credentials File

Edit the file: `credentials/client_credentials.json`

Replace `"REPLACE_WITH_YOUR_CLIENT_SECRET"` with your actual client secret.

### Step 3: Enable Required APIs

In Google Cloud Console, enable these APIs:
- ✅ Google Drive API
- ✅ Google Sheets API (for team management)
- ✅ Google Docs API (for document creation)

### Step 4: Test the Connection

Run the test script:
```bash
python simple_drive_test.py
```

This will:
- Open a browser for OAuth authentication
- Test your Google Drive access
- List your recent files
- Create a course folder
- Verify everything is working

### Step 5: Run Team Setup (Once Working)

After the test succeeds, you can:
```bash
python team_setup.py --test-only    # Test mode first
python team_setup.py                # Create actual team folders
```

## 🔒 Security Notes

- Keep your `client_secret` private
- The `token.json` file will be created automatically after first authentication
- You only need to authenticate once - the token will be refreshed automatically

## 🚨 Troubleshooting

**If you get "client_secret not found" error:**
- Make sure you've replaced the placeholder in `client_credentials.json`

**If you get "OAuth error":**
- Check that the redirect URI is set to `http://localhost` in Google Cloud Console
- Make sure the APIs are enabled

**If you get "Permission denied":**
- Check that your Google account has access to create folders in Drive

## 📋 What This Will Do

Once set up, the scripts can:
- ✅ Read team assignments from Google Sheets
- ✅ Create individual folders for each team
- ✅ Set appropriate permissions for team members  
- ✅ Create template files (docs, sheets, presentations)
- ✅ Update your spreadsheet with folder links
- ✅ Automate the entire team workspace setup

Ready to test? Run `python simple_drive_test.py` once you have your client secret!
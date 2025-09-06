# Mail.app Access Setup Guide

## macOS Permissions Required

### 1. **System Preferences → Privacy & Security**

#### Automation Permissions
1. Open **System Preferences** → **Security & Privacy** → **Privacy**
2. Select **Automation** from the left sidebar
3. Look for **Terminal** or **Python** (depending on how you're running scripts)
4. Enable access to **Mail.app**

#### AppleScript Permissions  
1. In the same **Privacy** section
2. Select **Apple Events** (if available)
3. Grant permission for **Terminal/Python** to send Apple Events to **Mail**

### 2. **Mail.app Permissions**

#### First Run Setup
1. **Open Mail.app** first (make sure it's running)
2. **Run the script** - you'll get a permission dialog
3. **Click "Allow"** when prompted about AppleScript access
4. **Grant permissions** for automation

## Quick Permission Test

Let's test if the permissions are working:

```bash
# Test basic Mail.app access
osascript -e 'tell application "Mail" to get name of every account'
```

If this works, you should see your email account names listed.

## Manual Permission Setup Steps

### Step 1: Enable Mail.app Automation
1. **Open System Preferences**
2. **Security & Privacy** → **Privacy** 
3. **Automation** → Find **Terminal** or **Python**
4. **Check the box** next to **Mail**

### Step 2: Test Basic Access
Run this simple test:

```bash
# Basic connectivity test
osascript -e 'tell application "Mail" to get (count of messages in inbox)'
```

### Step 3: Grant AppleScript Access
When you first run any Mail script, macOS will ask:
- **"Terminal wants to control Mail"** → Click **"OK"**
- **"Python wants access to control Mail"** → Click **"Allow"**

## Common Issues & Solutions

### Issue 1: "Not authorized to send Apple events"
**Solution**: 
1. Go to **System Preferences** → **Security & Privacy** → **Privacy**
2. **Automation** → Enable **Terminal** → **Mail**

### Issue 2: Mail.app not responding
**Solution**:
1. **Quit Mail.app completely** (⌘Q)
2. **Restart Mail.app**  
3. **Run the script again**

### Issue 3: Permission dialogs keep appearing
**Solution**:
1. **Always click "Allow"** or "OK"
2. **Check "Don't ask again"** if available
3. **Restart Terminal** after granting permissions

## Verification Commands

### Test 1: Account Access
```bash
osascript -e 'tell application "Mail" to get name of every account'
```

### Test 2: Inbox Count
```bash
osascript -e 'tell application "Mail" to get (count of messages in inbox)'
```

### Test 3: Recent Email Subject
```bash
osascript -e 'tell application "Mail" to get subject of message 1 of inbox'
```

## After Setup is Complete

Once permissions are configured, these scripts will work:
- `forward_and_archive.py` 
- `quick_forward.py`
- `screening_test_email_extractor.py`
- `mail_app_retrieval.py`

## Next Steps

1. **Complete the permission setup** above
2. **Test with verification commands**
3. **Run the email forward script** again
4. **Search for your "Logs Panel..." email**

---

**Important**: You need to go through this setup **once** and then all Mail.app automation will work seamlessly!

# 🚀 True CLI Canva Creation - API Guide

## No Browser, No GUI - Pure Command Line!

This guide shows you how to create Canva presentations using **only CLI commands** via Canva's Connect API.

## 🔧 Quick Setup (5 minutes)

### Step 1: Get Canva API Access
```bash
# Run the interactive setup
python3 canva_api_setup.py
```

This will:
1. Guide you through creating a Canva developer account
2. Help you create a Connect API app
3. Get your access token
4. Save configuration automatically
5. Test the connection

### Step 2: Set Environment Variable (Alternative)
If you already have a token:
```bash
export CANVA_ACCESS_TOKEN="canva_your_token_here"
```

## 🎯 Usage Examples

### Test Your Connection
```bash
python3 canva_connect_api.py --test
```

### Create LANG 2077 Slides (Full Automation)
```bash
python3 canva_connect_api.py --create lang2077
```
This will:
- ✅ Create presentation via API
- ✅ Add course content automatically  
- ✅ Invite collaborators
- ✅ Generate PDF export
- ✅ Save design info locally

### Create Custom Presentation
```bash
# Basic presentation
python3 canva_connect_api.py --create presentation --title "My Presentation"

# With collaborators
python3 canva_connect_api.py --create presentation \
  --title "Team Project" \
  --collaborators user1@hkbu.edu.hk user2@hkbu.edu.hk

# With export
python3 canva_connect_api.py --create presentation \
  --title "Final Presentation" \
  --export pdf
```

### Quick & Simple Creation
```bash
# Super simple - just create and open
python3 canva_quick_api.py "My Presentation Title"

# With your token
python3 canva_quick_api.py canva_your_token "Presentation Title"
```

## 📊 What Each Tool Does

### `canva_connect_api.py` - Full Featured API Client
- ✅ Complete design creation and management
- ✅ Add text, elements, and content
- ✅ Share with collaborators automatically
- ✅ Export to PDF, PNG, JPG
- ✅ Manage design permissions
- ✅ Full error handling and logging

### `canva_quick_api.py` - Minimal Quick Creator
- ✅ Fast presentation creation
- ✅ Minimal dependencies
- ✅ Perfect for simple use cases
- ✅ Lightweight and fast

### `canva_api_setup.py` - Interactive Setup Assistant
- ✅ Guides through API setup
- ✅ Tests connections
- ✅ Saves configuration
- ✅ Opens browser for account creation

## 🎓 LANG 2077 Specific Commands

### Create Complete Course Presentation
```bash
# Full automation - creates slides, adds content, invites team
python3 canva_connect_api.py --create lang2077
```

This creates:
- **Slide 1**: Course title and info
- **Slide 2**: Learning outcomes
- **Slide 3**: Community impact
- **Collaborators**: Department head, coordinator, TA
- **Export**: PDF ready for sharing

### Customize LANG 2077 Creation
```bash
# Different collaborators
python3 canva_connect_api.py --create lang2077 \
  --collaborators custom1@hkbu.edu.hk custom2@hkbu.edu.hk

# Different export format
python3 canva_connect_api.py --create lang2077 --export png
```

## 🔗 API vs Browser Automation

| Feature | Browser Automation | Canva Connect API |
|---------|-------------------|-------------------|
| **Speed** | Slow (opens browser) | Fast (direct API) |
| **Reliability** | Fragile (UI changes) | Stable (API contract) |
| **Resources** | High (Chrome process) | Low (HTTP requests) |
| **Automation** | Limited | Full programmatic control |
| **Headless** | Possible but complex | Always headless |
| **Collaboration** | Manual sharing | Automatic invitations |
| **Export** | Manual download | Programmatic export |

## 🎯 Workflow Comparison

### Old Way (Browser Automation):
1. ❌ Open Chrome browser
2. ❌ Navigate to canva.com
3. ❌ Log in manually
4. ❌ Find templates
5. ❌ Click and type content
6. ❌ Share manually
7. ❌ Export manually

### New Way (API):
1. ✅ `python3 canva_connect_api.py --create lang2077`
2. ✅ Done! (Everything automated)

## 🔐 Security & Configuration

### Environment Variables
```bash
# Required
export CANVA_ACCESS_TOKEN="canva_your_token_here"

# Optional
export CANVA_EMAIL="simonwang@hkbu.edu.hk"
export DEFAULT_EXPORT_FORMAT="pdf"
```

### Configuration Files
- `.env` - Main configuration
- `.env.api` - API-specific settings
- API designs saved to `api_designs/` folder

## 🚨 Troubleshooting

### "No access token found"
```bash
# Run setup
python3 canva_api_setup.py

# Or set manually
export CANVA_ACCESS_TOKEN="your_token"
```

### "Authentication failed"
- Check token is correct and starts with `canva_`
- Verify scopes are enabled in Canva developer console
- Token might be expired - generate new one

### "API connection failed"
- Check internet connection
- Verify api.canva.com is accessible
- Try the test command: `python3 canva_connect_api.py --test`

## 🎉 Benefits of API Approach

1. **True CLI**: No browser windows, no GUI
2. **Fast**: Direct API calls vs browser automation
3. **Reliable**: Stable API vs changing web interfaces
4. **Scalable**: Can create hundreds of designs programmatically
5. **Collaborative**: Built-in sharing and permissions
6. **Integrated**: Easy to incorporate into scripts and workflows

## 📋 Next Steps

1. **Run setup**: `python3 canva_api_setup.py`
2. **Test connection**: `python3 canva_connect_api.py --test`  
3. **Create slides**: `python3 canva_connect_api.py --create lang2077`
4. **Customize**: Modify scripts for your specific needs
5. **Automate**: Integrate into larger workflows

You now have **true CLI access** to Canva without any browser automation! 🚀

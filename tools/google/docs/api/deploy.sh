#!/bin/bash

# GCAP 3226 Google Docs API Deployment Script
# This script guides you through the complete setup process

echo "🚀 GCAP 3226 Google Docs API Deployment Guide"
echo "============================================="

# Check if credentials.json exists
CREDS_FILE="/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI/credentials.json"

if [ ! -f "$CREDS_FILE" ]; then
    echo ""
    echo "❌ STEP 1: Missing credentials.json file"
    echo ""
    echo "Please follow these steps:"
    echo "1. 🌐 Go to: https://console.cloud.google.com/"
    echo "2. 📁 Create project: 'CourseDriveManage'"
    echo "3. 🔧 Enable APIs: Drive API, Docs API, Sheets API"
    echo "4. 🔑 Create OAuth 2.0 Desktop credentials"
    echo "5. 📥 Download and save as: credentials.json"
    echo "6. 📂 Place file at: $CREDS_FILE"
    echo ""
    echo "Then run this script again!"
    exit 1
fi

echo "✅ Found credentials.json file"
echo ""

# Test authentication
echo "🔐 STEP 2: Testing Google API authentication..."
cd /Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI
python auth_setup.py

# Check if authentication was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Authentication successful!"
    echo ""
    echo "🏗️  STEP 3: Ready to create team structure?"
    echo "This will create 10 Google Drive folders and documents"
    echo ""
    read -p "Create team folders and documents? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🚀 Creating team structure..."
        python team_manager.py
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "🎉 DEPLOYMENT COMPLETE!"
            echo "======================"
            echo "✅ 10 team folders created in Google Drive"
            echo "✅ 10 team documents created with templates"
            echo "✅ Local backup system ready"
            echo ""
            echo "📋 Next steps:"
            echo "- Use document_editor.py to manage team documents"
            echo "- Use local_manager.py for offline backup"
            echo "- Check team_setup_results.json for folder/document IDs"
            echo ""
            echo "🎯 Your GCAP 3226 team management system is ready!"
        else
            echo "❌ Team creation failed. Check the error messages above."
        fi
    else
        echo "⏸️  Team creation skipped. You can run 'python team_manager.py' later."
    fi
else
    echo "❌ Authentication failed. Please check your credentials.json file."
fi

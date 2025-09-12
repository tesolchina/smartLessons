#!/bin/bash

echo "🔧 CourseDriveManage OAuth Setup Checker"
echo "========================================"
echo ""
echo "Project: CourseDriveManage"
echo "User: simonwanghkteacher@gmail.com"
echo ""

# Check if user has completed OAuth setup
echo "❓ OAUTH SETUP CHECKLIST:"
echo ""
echo "Have you completed these steps in Google Cloud Console?"
echo "https://console.cloud.google.com/apis/credentials/consent"
echo ""
echo "✅ 1. Set User Type to 'External'?"
read -p "   (y/n): " step1

echo "✅ 2. Set App name to 'CourseDriveManage'?"
read -p "   (y/n): " step2

echo "✅ 3. Added your email as User support email?"
read -p "   (y/n): " step3

echo "✅ 4. Added required scopes (Drive, Docs, Sheets APIs)?"
read -p "   (y/n): " step4

echo "✅ 5. Added simonwanghkteacher@gmail.com as TEST USER?"
read -p "   (y/n): " step5

echo "✅ 6. Set Publishing status to 'Testing'?"
read -p "   (y/n): " step6

echo ""

# Check if all steps completed
if [[ "$step1" == "y" && "$step2" == "y" && "$step3" == "y" && "$step4" == "y" && "$step5" == "y" && "$step6" == "y" ]]; then
    echo "🎉 OAuth setup complete! Testing authentication..."
    echo ""
    python auth_setup.py
else
    echo "❌ OAuth setup incomplete!"
    echo ""
    echo "📋 Please complete the missing steps:"
    
    if [[ "$step1" != "y" ]]; then
        echo "   - Set User Type to 'External'"
    fi
    if [[ "$step2" != "y" ]]; then
        echo "   - Set App name to 'CourseDriveManage'"
    fi
    if [[ "$step3" != "y" ]]; then
        echo "   - Add your email as User support email"
    fi
    if [[ "$step4" != "y" ]]; then
        echo "   - Add required scopes (Drive, Docs, Sheets)"
    fi
    if [[ "$step5" != "y" ]]; then
        echo "   - Add simonwanghkteacher@gmail.com as TEST USER (CRITICAL!)"
    fi
    if [[ "$step6" != "y" ]]; then
        echo "   - Set Publishing status to 'Testing'"
    fi
    
    echo ""
    echo "🌐 Go to: https://console.cloud.google.com/apis/credentials/consent"
    echo "Then run this script again!"
fi

🔧 OAUTH CONFIGURATION FOR "CourseDriveManage" PROJECT
=======================================================

PROJECT: CourseDriveManage
USER: simonwanghkteacher@gmail.com

✅ STEP-BY-STEP OAUTH CONSENT SCREEN SETUP:

1. 🌐 OPEN OAUTH CONSENT SCREEN:
   https://console.cloud.google.com/apis/credentials/consent
   (Make sure you're in the "CourseDriveManage" project)

2. 📝 OAUTH CONSENT SCREEN CONFIGURATION:

   USER TYPE:
   ✅ Select: "External"
   
   APP INFORMATION:
   ✅ App name: CourseDriveManage
   ✅ User support email: simonwanghkteacher@gmail.com
   ✅ App logo: (skip - optional)
   ✅ App domain: (skip - not needed for testing)
   
   AUTHORIZED DOMAINS:
   ✅ Leave empty (not needed for local development)
   
   DEVELOPER CONTACT:
   ✅ Developer email: simonwanghkteacher@gmail.com

3. 🔧 SCOPES CONFIGURATION:
   Click "ADD OR REMOVE SCOPES" and add:
   ✅ https://www.googleapis.com/auth/drive
   ✅ https://www.googleapis.com/auth/documents  
   ✅ https://www.googleapis.com/auth/spreadsheets

4. 👤 TEST USERS (CRITICAL STEP!):
   ✅ Add test user: simonwanghkteacher@gmail.com
   ✅ Click "ADD USERS"
   ✅ Save changes

5. 💾 REVIEW AND SAVE:
   ✅ Review all settings
   ✅ Save and continue through all steps
   ✅ Publishing status should be: "Testing"

🎯 IMPORTANT NOTES:
- Your app name "CourseDriveManage" will appear in authorization screens
- Adding yourself as a test user allows you to bypass verification
- "Testing" status is perfect for development - no public verification needed
- You can add up to 100 test users if needed for your course

✅ AFTER CONFIGURATION:
Your OAuth error should be resolved and authentication should work!

🔄 NEXT STEPS:
1. Complete the OAuth setup above
2. Run: python auth_setup.py
3. Authorize the app when browser opens
4. Run: python team_manager.py to create team structure

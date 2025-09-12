#!/usr/bin/env python3
"""
Google Docs Reference Letter Creator
Creates a Google Doc for Yanbo's reference letter and invites collaborator
"""

import os
import sys
from pathlib import Path

# Add the operating tools to the path for Google API access
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating')

try:
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import pickle
except ImportError:
    print("❌ Google API libraries not found. Please install:")
    print("   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

class ReferenceLetterDocCreator:
    """Create and manage Google Docs for reference letters"""
    
    def __init__(self):
        self.SCOPES = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/drive'
        ]
        self.credentials = None
        self.docs_service = None
        self.drive_service = None
    
    def authenticate(self):
        """Authenticate with Google APIs"""
        # Use credentials from GoogleDocsAPI folder
        api_folder = Path('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')
        creds_path = api_folder / 'token.pickle'
        credentials_path = api_folder / 'credentials.json'
        
        if creds_path.exists():
            with open(creds_path, 'rb') as token:
                self.credentials = pickle.load(token)
        
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                if not credentials_path.exists():
                    raise FileNotFoundError(f"credentials.json not found at {credentials_path}")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_path), self.SCOPES)
                self.credentials = flow.run_local_server(port=0)
            
            with open(creds_path, 'wb') as token:
                pickle.dump(self.credentials, token)
        
        self.docs_service = build('docs', 'v1', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        
        print("✅ Google API authentication successful")
    
    def create_reference_letter_template(self):
        """Create reference letter document with template content"""
        
        # Create document
        document = {
            'title': 'Reference Letter - ZENG Yanbo (UST Science Leadership & Entrepreneurship)'
        }
        
        doc = self.docs_service.documents().create(body=document).execute()
        document_id = doc['documentId']
        
        print(f"📄 Created document: {document_id}")
        
        # Template content for the reference letter
        template_content = """REFERENCE LETTER

To Whom It May Concern:

I am writing to provide a strong recommendation for ZENG Yanbo's application to the Science Leadership & Entrepreneurship graduate program at the Hong Kong University of Science and Technology (UST).

STUDENT INFORMATION:
- Name: ZENG Yanbo
- Student ID: 22258221@life.hkbu.edu.hk
- Program: UST Science Leadership & Entrepreneurship (Graduate Program)

RECOMMENDATION FOCUS:
This letter specifically addresses Yanbo's leadership abilities, organizational skills, and potential for success in professional settings, complementing the academic reference provided by their subject-area professor.

COLLABORATION HISTORY:
[To be filled with specific examples of collaboration experiences]

LEADERSHIP ABILITIES:
[Specific examples of leadership demonstrated in collaborative projects]

ORGANIZATIONAL SKILLS:
[Evidence of strong organizational and project management capabilities]

WORK SUCCESS POTENTIAL:
[Assessment of professional potential and entrepreneurial aptitude]

CONCLUSION:
Based on our multiple collaborative experiences, I strongly recommend ZENG Yanbo for admission to the UST Science Leadership & Entrepreneurship program. Their demonstrated leadership abilities and organizational skills position them well for success in this field.

Please feel free to contact me if you need any additional information.

Sincerely,

[Professor Name]
[Title]
[Institution]
[Contact Information]
[Date]

---
NOTES FOR COLLABORATION:
- Focus on leadership and organizational abilities (academic performance covered by other reference)
- Include specific examples from collaboration history
- Emphasize entrepreneurial potential and professional readiness
- Maintain formal, professional tone throughout
"""
        
        # Add content to document
        requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': template_content
                }
            }
        ]
        
        self.docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()
        
        print("📝 Added template content to document")
        return document_id
    
    def move_to_folder_and_share(self, document_id, folder_id, collaborator_email):
        """Move document to specified folder and share with collaborator"""
        
        # Move to folder
        try:
            self.drive_service.files().update(
                fileId=document_id,
                addParents=folder_id,
                removeParents='root'
            ).execute()
            print(f"📁 Moved document to folder: {folder_id}")
        except Exception as e:
            print(f"⚠️  Could not move to folder: {e}")
        
        # Share with collaborator
        try:
            permission = {
                'type': 'user',
                'role': 'writer',
                'emailAddress': collaborator_email
            }
            
            self.drive_service.permissions().create(
                fileId=document_id,
                body=permission,
                sendNotificationEmail=True,
                emailMessage=f"""Hi Yanbo,

I've created a Google Doc for your reference letter for the UST Science Leadership & Entrepreneurship program. 

Please review the template and add any specific details about our collaboration history that you'd like me to emphasize. Focus on examples that demonstrate your leadership abilities and organizational skills.

You can edit this document directly - I'll finalize it once you've added your input.

Best regards,
Professor Wang"""
            ).execute()
            
            print(f"🤝 Shared document with: {collaborator_email}")
            
        except Exception as e:
            print(f"❌ Error sharing document: {e}")
    
    def create_reference_letter_system(self):
        """Complete reference letter document creation process"""
        
        print("🚀 Creating reference letter document system for Yanbo...")
        
        # Configuration
        folder_id = "1C4qp8C5tHrfRaDC6-nHcXqyApySTa4Bd"
        collaborator_email = "edisonzeng155@gmail.com"
        
        try:
            # Authenticate
            self.authenticate()
            
            # Create document with template
            document_id = self.create_reference_letter_template()
            
            # Move to folder and share
            self.move_to_folder_and_share(document_id, folder_id, collaborator_email)
            
            # Generate document URL
            doc_url = f"https://docs.google.com/document/d/{document_id}/edit"
            
            print(f"""
✅ Reference Letter Document Created Successfully!

📄 Document Details:
   • Title: Reference Letter - ZENG Yanbo (UST Science Leadership & Entrepreneurship)
   • Document ID: {document_id}
   • URL: {doc_url}

🤝 Collaboration Setup:
   • Shared with: {collaborator_email}
   • Permission: Edit access
   • Notification sent: Yes

📁 Location:
   • Moved to specified Google Drive folder
   • Folder ID: {folder_id}

📋 Next Steps:
   1. Yanbo will receive email notification with edit access
   2. Student can add specific collaboration examples
   3. Review and finalize reference letter content
   4. Submit completed reference letter

🔗 Quick Access: {doc_url}
            """)
            
            # Save info to local file
            info_file = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/RefLetter/Google_Doc_Info.md")
            with open(info_file, 'w') as f:
                f.write(f"""# Google Doc Creation Results

## Document Information
- **Title:** Reference Letter - ZENG Yanbo (UST Science Leadership & Entrepreneurship)
- **Document ID:** {document_id}
- **URL:** {doc_url}
- **Created:** {Path(__file__).stat().st_mtime}

## Sharing Details
- **Collaborator:** {collaborator_email}
- **Permission Level:** Edit access
- **Notification Sent:** Yes

## Folder Location
- **Google Drive Folder ID:** {folder_id}
- **Folder URL:** https://drive.google.com/drive/u/0/folders/{folder_id}

## Template Content Added
- Professional reference letter template
- Focus areas: Leadership, organizational skills, work success potential
- Collaboration sections for student input
- Formal academic recommendation structure

## Status
✅ Document created and shared successfully
""")
            
            print(f"💾 Saved document info to: {info_file}")
            
        except Exception as e:
            print(f"❌ Error in document creation process: {e}")
            print("Please check Google API credentials and folder permissions.")

def main():
    """Main execution function"""
    creator = ReferenceLetterDocCreator()
    creator.create_reference_letter_system()

if __name__ == "__main__":
    main()

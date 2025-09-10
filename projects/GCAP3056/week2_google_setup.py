#!/usr/bin/env python3
"""
GCAP 3056 Week 2 Preparation: Google Drive Setup and Google Form Creation
- Set up GCAP 3056 Google Drive folder structure
- Move existing course document to correct folder
- Create Google Form for group leader registration
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add GoogleDocsAPI to path
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

try:
    from auth_setup import authenticate_google_apis
    from googleapiclient.discovery import build
    APIS_AVAILABLE = True
except ImportError as e:
    print(f"Google APIs not available: {e}")
    APIS_AVAILABLE = False

class GCAP3056DriveManager:
    """Manage GCAP 3056 Google Drive folders and forms"""
    
    def __init__(self):
        self.setup_services()
        
    def setup_services(self):
        """Initialize Google API services"""
        if not APIS_AVAILABLE:
            print("📄 [OFFLINE MODE] Google APIs not available")
            self.drive_service = None
            self.docs_service = None
            self.forms_service = None
            return
            
        try:
            creds = authenticate_google_apis()
            if creds:
                self.drive_service = build('drive', 'v3', credentials=creds)
                self.docs_service = build('docs', 'v1', credentials=creds)
                self.forms_service = build('forms', 'v1', credentials=creds)
                print("✅ Google API services initialized")
            else:
                print("❌ Failed to authenticate with Google APIs")
                self.drive_service = None
                self.docs_service = None
                self.forms_service = None
        except Exception as e:
            print(f"❌ API setup error: {e}")
            self.drive_service = None
            self.docs_service = None
            self.forms_service = None

    def create_course_folder_structure(self, parent_folder_id: str) -> dict:
        """Create GCAP 3056 folder structure in Google Drive"""
        
        if not self.drive_service:
            print("❌ Drive service not available")
            return None
            
        print("📂 Creating GCAP 3056 folder structure...")
        
        try:
            # Main GCAP 3056 folder
            main_folder = {
                'name': 'GCAP 3056 Fall 2025',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]
            }
            
            main_result = self.drive_service.files().create(body=main_folder).execute()
            main_folder_id = main_result.get('id')
            
            print(f"✅ Created main folder: GCAP 3056 Fall 2025")
            
            # Subfolders
            subfolders = [
                'Course Materials',
                'Group Projects',
                'Assessment Submissions',
                'Student Resources',
                'Group Registrations'
            ]
            
            folder_structure = {
                'main_folder': {
                    'id': main_folder_id,
                    'name': 'GCAP 3056 Fall 2025',
                    'link': f"https://drive.google.com/drive/folders/{main_folder_id}"
                },
                'subfolders': {}
            }
            
            for subfolder_name in subfolders:
                subfolder = {
                    'name': subfolder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [main_folder_id]
                }
                
                subfolder_result = self.drive_service.files().create(body=subfolder).execute()
                subfolder_id = subfolder_result.get('id')
                
                folder_structure['subfolders'][subfolder_name] = {
                    'id': subfolder_id,
                    'name': subfolder_name,
                    'link': f"https://drive.google.com/drive/folders/{subfolder_id}"
                }
                
                print(f"✅ Created subfolder: {subfolder_name}")
            
            return folder_structure
            
        except Exception as e:
            print(f"❌ Error creating folder structure: {e}")
            return None

    def move_document_to_folder(self, doc_id: str, target_folder_id: str, doc_title: str = None) -> bool:
        """Move existing document to target folder"""
        
        if not self.drive_service:
            print("❌ Drive service not available")
            return False
            
        try:
            # Get current parents
            file_info = self.drive_service.files().get(
                fileId=doc_id, 
                fields='parents,name'
            ).execute()
            
            current_parents = ','.join(file_info.get('parents'))
            actual_title = file_info.get('name', doc_title or 'Unknown Document')
            
            # Move to new folder
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=target_folder_id,
                removeParents=current_parents,
                fields='id,parents'
            ).execute()
            
            print(f"✅ Moved document '{actual_title}' to target folder")
            return True
            
        except Exception as e:
            print(f"❌ Error moving document: {e}")
            return False

    def create_group_registration_form(self, responses_folder_id: str) -> dict:
        """Create Google Form for group leader registration"""
        
        if not self.forms_service:
            print("❌ Forms service not available")
            return None
            
        try:
            # Create the form
            form = {
                "info": {
                    "title": "GCAP 3056 - Group Leader Registration",
                    "description": "Please complete this form to register your group and indicate your topic preferences. Only GROUP LEADERS should fill out this form."
                }
            }
            
            form_result = self.forms_service.forms().create(body=form).execute()
            form_id = form_result.get('formId')
            
            print(f"✅ Created Google Form: {form_result.get('info', {}).get('title')}")
            
            # Add questions to the form
            questions = [
                {
                    "title": "Group Leader Information",
                    "description": "Please provide your details as the group leader",
                    "required": True,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                {
                    "title": "Group Leader Name",
                    "required": True,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                {
                    "title": "Group Leader Student ID",
                    "required": True,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                {
                    "title": "Group Leader Gmail Address",
                    "required": True,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                {
                    "title": "Group Leader Major/Program",
                    "required": True,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": False
                            }
                        }
                    }
                },
                {
                    "title": "Group Members Information",
                    "description": "Please list ALL group members (including yourself) with: Name, Student ID, Gmail, Major - one per line",
                    "required": True,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                {
                    "title": "Primary Topic Preference",
                    "description": "Choose your group's primary area of interest",
                    "required": True,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": "Public Health & Healthcare Policy"},
                                    {"value": "Traditional Chinese Medicine Integration"},
                                    {"value": "Education Policy & Cultural Affairs"},
                                    {"value": "Housing & Urban Development"},
                                    {"value": "Transportation Policy"},
                                    {"value": "Environmental Policy & Climate Change"},
                                    {"value": "Smart Cities & Technology"},
                                    {"value": "Constitutional Affairs & Governance"},
                                    {"value": "Other (please specify in next question)"}
                                ]
                            }
                        }
                    }
                },
                {
                    "title": "Other Topic or Specific Focus",
                    "description": "If you selected 'Other' above, or want to specify a particular focus within your chosen area, please describe here",
                    "required": False,
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                },
                {
                    "title": "Government Department/Agency of Interest",
                    "description": "Which government department or agency would you like to request information from using CAIP? (e.g., Department of Health, Education Bureau, Transport Department, etc.)",
                    "required": False,
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {
                                "paragraph": True
                            }
                        }
                    }
                }
            ]
            
            # Add questions to form
            requests = []
            for i, question in enumerate(questions):
                request = {
                    "createItem": {
                        "item": {
                            "title": question["title"],
                            "description": question.get("description", ""),
                            "questionItem": question["questionItem"]
                        },
                        "location": {"index": i}
                    }
                }
                requests.append(request)
            
            # Apply all questions at once
            if requests:
                self.forms_service.forms().batchUpdate(
                    formId=form_id,
                    body={"requests": requests}
                ).execute()
                
                print(f"✅ Added {len(requests)} questions to form")
            
            # Get form URL
            form_url = f"https://docs.google.com/forms/d/{form_id}/edit"
            public_url = f"https://docs.google.com/forms/d/{form_id}/viewform"
            
            # Move form to responses folder if provided
            if responses_folder_id and self.drive_service:
                try:
                    # Forms are automatically created in the root, move to our folder
                    file_info = self.drive_service.files().get(
                        fileId=form_id, 
                        fields='parents'
                    ).execute()
                    
                    current_parents = ','.join(file_info.get('parents', []))
                    
                    self.drive_service.files().update(
                        fileId=form_id,
                        addParents=responses_folder_id,
                        removeParents=current_parents,
                        fields='id,parents'
                    ).execute()
                    
                    print(f"✅ Moved form to Group Registrations folder")
                except Exception as e:
                    print(f"⚠️ Could not move form to folder: {e}")
            
            return {
                'form_id': form_id,
                'edit_url': form_url,
                'public_url': public_url,
                'title': 'GCAP 3056 - Group Leader Registration'
            }
            
        except Exception as e:
            print(f"❌ Error creating form: {e}")
            return None

    def generate_week2_setup_summary(self, folder_structure: dict, form_info: dict, moved_doc: bool) -> str:
        """Generate summary report for Week 2 setup"""
        
        summary = f"""# GCAP 3056 Week 2 Setup Complete

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Setup Status:** {'✅ Complete' if folder_structure and form_info else '❌ Partial'}

## 📂 Google Drive Folder Structure Created

### Main Course Folder:
- **Folder:** {folder_structure['main_folder']['name']}
- **Link:** {folder_structure['main_folder']['link']}
- **ID:** {folder_structure['main_folder']['id']}

### Subfolders Created:
"""
        
        for name, info in folder_structure['subfolders'].items():
            summary += f"- **{name}:** {info['link']}\n"
        
        summary += f"""

## 📝 Google Form Created

### Group Registration Form:
- **Title:** {form_info['title']}
- **Public URL (for students):** {form_info['public_url']}
- **Edit URL (for instructor):** {form_info['edit_url']}
- **Form ID:** {form_info['form_id']}

### Form Features:
- Group leader personal information collection
- Complete group membership details
- Topic preference selection (8 main categories + other)
- Government department targeting
- CAIP request planning

## 📄 Document Management

### Course Document:
- **Status:** {'✅ Moved to Course Materials folder' if moved_doc else '❌ Not moved - check document ID'}
- **Original:** https://docs.google.com/document/d/1fqrraqaRkANg9r0jArxvx7_W2xo0QlSCvDRYXdWvQ0o/edit

## 🚀 Week 2 Class Implementation

### For Class Tomorrow:
1. **Show students the folder structure** - demonstrate organization
2. **Share the registration form link** - only group leaders complete
3. **Explain group formation process** - 3-5 students per group optimal
4. **Discuss topic selection** - emphasize Chinese Medicine focus opportunities
5. **Timeline CAIP requests** - must start by Week 3-4

### Student Instructions:
```
📋 GCAP 3056 Group Formation Instructions

1. Form groups of 3-5 students
2. Choose ONE group leader
3. Group leader completes registration form: {form_info['public_url']}
4. Select primary topic area (health policy recommended for CM students)
5. Identify target government department for information requests
6. Submit by [deadline - suggest end of Week 2]
```

### Instructor Dashboard:
- **Form Responses:** Monitor through Google Forms interface
- **Folder Management:** All submissions will go to Group Registrations folder
- **Group Tracking:** Use form data to create group project folders

## 📊 Next Steps After Registration

### Week 3 Preparation:
- [ ] Review form responses and finalize groups
- [ ] Create individual group folders within Group Projects
- [ ] Prepare CAIP request templates for each group's target department
- [ ] Schedule individual group consultations
- [ ] Share folder access with group members

### Assessment Integration:
- Use folder structure for portfolio submissions
- Group projects managed through dedicated folders
- Assessment rubrics shared via Course Materials folder

---

**Ready for Week 2 group formation session! 🎯**
"""
        
        return summary

def main():
    """Execute Week 2 preparation setup"""
    
    print("=== GCAP 3056 Week 2 Preparation Setup ===")
    print()
    
    # Initialize manager
    manager = GCAP3056DriveManager()
    
    if not manager.drive_service:
        print("❌ Cannot proceed without Google Drive access")
        return
    
    # Target folder ID from your notes
    TARGET_FOLDER_ID = "1h1KDGUtGCHL2EsS-LKLbZZhjmVNn8GmM"
    
    # Document to move
    COURSE_DOC_ID = "1fqrraqaRkANg9r0jArxvx7_W2xo0QlSCvDRYXdWvQ0o"
    
    print("📂 Step 1: Creating folder structure...")
    folder_structure = manager.create_course_folder_structure(TARGET_FOLDER_ID)
    
    if not folder_structure:
        print("❌ Failed to create folder structure")
        return
    
    print(f"\n📄 Step 2: Moving course document...")
    course_materials_folder_id = folder_structure['subfolders']['Course Materials']['id']
    moved_doc = manager.move_document_to_folder(
        COURSE_DOC_ID, 
        course_materials_folder_id,
        "GCAP 3056 Course Notes"
    )
    
    print(f"\n📝 Step 3: Creating group registration form...")
    registrations_folder_id = folder_structure['subfolders']['Group Registrations']['id']
    form_info = manager.create_group_registration_form(registrations_folder_id)
    
    if not form_info:
        print("❌ Failed to create registration form")
        return
    
    print(f"\n📊 Step 4: Generating setup summary...")
    summary = manager.generate_week2_setup_summary(folder_structure, form_info, moved_doc)
    
    # Save summary locally
    summary_file = Path("./week2_setup_summary.md")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ Setup summary saved: {summary_file}")
    
    print("\n🎉 Week 2 Setup Complete!")
    print(f"📂 Main Folder: {folder_structure['main_folder']['link']}")
    print(f"📝 Registration Form: {form_info['public_url']}")
    print(f"📄 Setup Details: {summary_file}")
    print(f"\n🚀 Ready for tomorrow's class!")

if __name__ == "__main__":
    main()

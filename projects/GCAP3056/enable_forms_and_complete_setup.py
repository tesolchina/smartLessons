#!/usr/bin/env python3
"""
Complete GCAP 3056 Week 2 Setup After Forms API is Enabled
Run this after enabling Google Forms API in the console
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

def create_group_registration_form():
    """Create the Google Form for group registration"""
    
    if not APIS_AVAILABLE:
        print("❌ Google APIs not available")
        return None
        
    try:
        creds = authenticate_google_apis()
        if not creds:
            print("❌ Failed to authenticate")
            return None
            
        forms_service = build('forms', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        
        print("✅ Forms API connected successfully!")
        
        # Create the form (only title allowed initially)
        form_body = {
            "info": {
                "title": "GCAP 3056 Fall 2025 - Group Leader Registration"
            }
        }
        
        result = forms_service.forms().create(body=form_body).execute()
        form_id = result['formId']
        
        print(f"✅ Created form: {result['info']['title']}")
        
        # First, update the form description
        description_request = {
            "requests": [{
                "updateFormInfo": {
                    "info": {
                        "description": """📋 Group Formation for GCAP 3056: Taking a Stand

⚠️ IMPORTANT: Only GROUP LEADERS should complete this form.

This form collects information about your group's topic preferences and membership details. Please ensure all information is accurate as this will be used to:
• Set up your group's project folders
• Coordinate CAIP requests with government departments  
• Manage assessment submissions throughout the semester

Complete this form by the end of Week 2."""
                    },
                    "updateMask": "description"
                }
            }]
        }
        
        forms_service.forms().batchUpdate(
            formId=form_id,
            body=description_request
        ).execute()
        
        print("✅ Updated form description")
        
        # Now add all questions in one batch request
        requests = [
            # Group Leader Personal Info
            {
                "createItem": {
                    "item": {
                        "title": "Group Leader Name",
                        "description": "Your full name as the group leader",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {"paragraph": False}
                            }
                        }
                    },
                    "location": {"index": 0}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Group Leader Student ID",
                        "description": "Your university student ID number",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {"paragraph": False}
                            }
                        }
                    },
                    "location": {"index": 1}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Group Leader Gmail Address",
                        "description": "Gmail address for Google Drive folder sharing",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {"paragraph": False}
                            }
                        }
                    },
                    "location": {"index": 2}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Group Leader Major/Program",
                        "description": "Your academic program (e.g., Bachelor of Chinese Medicine, Master of Social Work)",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {"paragraph": False}
                            }
                        }
                    },
                    "location": {"index": 3}
                }
            },
            # Group Members Info
            {
                "createItem": {
                    "item": {
                        "title": "Complete Group Membership List",
                        "description": """List ALL group members (including yourself) with the following format:
                        
Name: [Full Name]
Student ID: [ID Number]
Gmail: [Gmail Address] 
Major: [Program/Major]

Separate each member with a blank line. Include 3-5 members total.""",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    "location": {"index": 4}
                }
            },
            # Topic Selection
            {
                "createItem": {
                    "item": {
                        "title": "Primary Research Topic Area",
                        "description": "Choose your group's main area of policy interest. Consider your academic background when selecting.",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "🏥 Public Health & Healthcare Policy (Recommended for Chinese Medicine students)"},
                                        {"value": "🌿 Traditional Chinese Medicine Integration & Regulation"},
                                        {"value": "🎓 Education Policy & Cultural Affairs"},
                                        {"value": "🏠 Housing & Urban Development Policy"},
                                        {"value": "🚇 Transportation & Infrastructure Policy"},
                                        {"value": "🌱 Environmental Policy & Climate Change"},
                                        {"value": "🏙️ Smart Cities & Technology Policy"},
                                        {"value": "⚖️ Constitutional Affairs & Legal Framework"},
                                        {"value": "🔄 Other Policy Area (specify below)"}
                                    ]
                                }
                            }
                        }
                    },
                    "location": {"index": 5}
                }
            },
            {
                "createItem": {
                    "item": {
                        "title": "Specific Research Focus or Other Topic",
                        "description": "If you selected 'Other' above, please specify your topic area. Otherwise, describe your specific focus within your chosen category (e.g., 'elderly healthcare services,' 'university admission policies,' 'public housing waiting times').",
                        "questionItem": {
                            "question": {
                                "required": False,
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    "location": {"index": 6}
                }
            },
            # Government Department Targeting
            {
                "createItem": {
                    "item": {
                        "title": "Target Government Department/Agency",
                        "description": """Which government department would you like to request information from using the Code on Access to Information (CAIP)?

Examples:
• Department of Health (health policies)
• Education Bureau (education policies)
• Transport Department (transportation)
• Housing Department (public housing)
• Environmental Protection Department (environment)
• Innovation & Technology Bureau (smart cities)

This will help us prepare your CAIP request templates.""",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    "location": {"index": 7}
                }
            },
            # Additional Information
            {
                "createItem": {
                    "item": {
                        "title": "Additional Comments or Questions",
                        "description": "Any special considerations, accessibility needs, or questions about the group project process?",
                        "questionItem": {
                            "question": {
                                "required": False,
                                "textQuestion": {"paragraph": True}
                            }
                        }
                    },
                    "location": {"index": 8}
                }
            }
        ]
        
        # Apply all questions
        forms_service.forms().batchUpdate(
            formId=form_id,
            body={"requests": requests}
        ).execute()
        
        print(f"✅ Added {len(requests)} questions to form")
        
        # Get URLs
        edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"
        public_url = f"https://docs.google.com/forms/d/{form_id}/viewform"
        
        return {
            'form_id': form_id,
            'edit_url': edit_url,
            'public_url': public_url,
            'title': 'GCAP 3056 Fall 2025 - Group Leader Registration'
        }
        
    except Exception as e:
        print(f"❌ Error creating form: {e}")
        return None

def main():
    """Complete the Week 2 setup"""
    print("=== Completing GCAP 3056 Week 2 Setup ===")
    print("🔧 Creating Google Form for group registration...")
    
    form_info = create_group_registration_form()
    
    if form_info:
        print(f"\n🎉 SUCCESS! Week 2 setup complete!")
        print(f"\n📝 Group Registration Form Created:")
        print(f"   • Title: {form_info['title']}")
        print(f"   • Public URL: {form_info['public_url']}")
        print(f"   • Edit URL: {form_info['edit_url']}")
        
        # Save form info
        form_details = {
            'created': datetime.now().isoformat(),
            'form_info': form_info,
            'instructions': {
                'for_students': f"Group leaders complete this form: {form_info['public_url']}",
                'for_instructor': f"Manage form responses: {form_info['edit_url']}",
                'deadline': 'End of Week 2 (September 13, 2025)'
            }
        }
        
        with open('week2_form_details.json', 'w') as f:
            json.dump(form_details, f, indent=2)
        
        print(f"\n📄 Form details saved to: week2_form_details.json")
        
        # Create instruction sheet for tomorrow's class
        class_instructions = f"""# GCAP 3056 Week 2 - Group Formation Instructions

## For Students (Display in class):

### 📋 Group Formation Process:
1. **Form groups of 3-5 students**
2. **Choose ONE group leader per group** 
3. **Group leader completes registration form by Friday**
4. **Link:** {form_info['public_url']}

### 🎯 Topic Selection Recommendations:
- **Chinese Medicine students:** Consider health policy topics
- **All students:** Think about your academic expertise 
- **Government departments:** We'll help you target the right agency

### ⏰ Timeline:
- **Today:** Form groups, choose leaders
- **By Friday:** Leaders complete registration
- **Next week:** Receive project folders and CAIP templates

---

## For Instructor Reference:

### 📊 Form Management:
- **Edit/View Responses:** {form_info['edit_url']}
- **Monitor registrations** throughout the week
- **Follow up** with groups that haven't registered by Thursday

### 📂 Google Drive Structure Created:
- Main folder with all subfolders ready
- Course materials organized
- Group project folders will be created after registration

### 🚀 Next Steps:
- Week 3: Create individual group folders based on registrations
- Prepare CAIP request templates for each group's target department
- Schedule individual group consultations

**Ready for successful group formation! 🎉**
"""
        
        with open('week2_class_instructions.md', 'w') as f:
            f.write(class_instructions)
        
        print(f"📋 Class instructions saved to: week2_class_instructions.md")
        print(f"\n🚀 You're ready for tomorrow's Week 2 class!")
        
    else:
        print("❌ Failed to create form. Check that Google Forms API is enabled and try again.")

if __name__ == "__main__":
    main()

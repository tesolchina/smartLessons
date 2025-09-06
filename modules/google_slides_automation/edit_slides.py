#!/usr/bin/env python3
"""
Google Slides Direct Editor
Edit Google Slides presentations directly via API.
"""

import os
import json
from datetime import datetime


def edit_google_slides():
    """Edit the Google Slides presentation directly."""
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        import pickle
        
        print("📦 Google API libraries loaded")
        
    except ImportError as e:
        print(f"❌ Missing library: {e}")
        print("Run: pip3 install google-api-python-client google-auth-oauthlib")
        return False
    
    # Scopes needed for editing
    SCOPES = [
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/presentations'
    ]
    
    # Your Google Slides presentation ID (from the link)
    PRESENTATION_ID = '1PaRmFXBMaAnN72YEmW_KM5PXjPsPEgnuwrU34sav-D0'
    
    try:
        # Load or create credentials
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        print("✅ Authentication successful")
        
        # Build services
        slides_service = build('slides', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        
        print(f"📄 Editing presentation: {PRESENTATION_ID}")
        
        # Get current presentation
        presentation = slides_service.presentations().get(
            presentationId=PRESENTATION_ID
        ).execute()
        
        print(f"📋 Current title: {presentation.get('title', 'No title')}")
        print(f"📊 Slides count: {len(presentation.get('slides', []))}")
        
        # Prepare batch update requests
        requests = []
        
        # 1. Update the main title slide
        title_slide_id = presentation['slides'][0]['objectId']
        
        # Find the title text box
        title_elements = []
        for element in presentation['slides'][0]['pageElements']:
            if 'shape' in element and element['shape'].get('shapeType') == 'TEXT_BOX':
                shape_id = element['objectId']
                
                # Check if this contains title text
                text_content = element['shape'].get('text', {})
                if text_content:
                    title_elements.append(shape_id)
        
        if title_elements:
            # Update title - replace existing text
            new_title = "Service Learning Sharing Session\nJoint Presentation by Dr. Joshua Chan, Dr. Nancy Guo & Dr. Simon Wang"
            
            requests.append({
                'deleteText': {
                    'objectId': title_elements[0],
                    'textRange': {
                        'type': 'ALL'
                    }
                }
            })
            
            requests.append({
                'insertText': {
                    'objectId': title_elements[0],
                    'insertionIndex': 0,
                    'text': new_title
                }
            })
            
            # Style the title
            requests.append({
                'updateTextStyle': {
                    'objectId': title_elements[0],
                    'textRange': {
                        'type': 'ALL'
                    },
                    'style': {
                        'fontSize': {'magnitude': 32, 'unit': 'PT'},
                        'foregroundColor': {
                            'opaqueColor': {'rgbColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8}}
                        },
                        'bold': True
                    },
                    'fields': 'fontSize,foregroundColor,bold'
                }
            })
        
        # 2. Add placeholder slides for Dr. Chan and Dr. Guo
        
        # Dr. Chan's slide
        requests.append({
            'createSlide': {
                'insertionIndex': 1,
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_BODY'
                }
            }
        })
        
        # Dr. Guo's slide  
        requests.append({
            'createSlide': {
                'insertionIndex': 2,
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_BODY'
                }
            }
        })
        
        print("⏳ Applying updates...")
        
        # Execute the batch update
        slides_service.presentations().batchUpdate(
            presentationId=PRESENTATION_ID,
            body={'requests': requests}
        ).execute()
        
        print("✅ Basic structure updated!")
        
        # Get the updated presentation to add content to new slides
        updated_presentation = slides_service.presentations().get(
            presentationId=PRESENTATION_ID
        ).execute()
        
        # Add content to Dr. Chan's slide (now slide 2)
        chan_slide_id = updated_presentation['slides'][1]['objectId']
        chan_requests = []
        
        # Find text elements in the slide
        chan_elements = []
        for element in updated_presentation['slides'][1]['pageElements']:
            if 'shape' in element and element['shape'].get('shapeType') == 'TEXT_BOX':
                chan_elements.append(element['objectId'])
        
        if len(chan_elements) >= 2:  # Title and body
            # Add title
            chan_requests.append({
                'insertText': {
                    'objectId': chan_elements[0],
                    'insertionIndex': 0,
                    'text': 'Dr. Joshua Chan\nService Learning in Language Education'
                }
            })
            
            # Add body content
            chan_requests.append({
                'insertText': {
                    'objectId': chan_elements[1],
                    'insertionIndex': 0,
                    'text': '• Service Learning methodology\n• Community engagement strategies\n• Student learning outcomes\n• [Content to be added by Dr. Chan]'
                }
            })
            
            # Style Dr. Chan's content
            chan_requests.append({
                'updateTextStyle': {
                    'objectId': chan_elements[0],
                    'textRange': {'type': 'ALL'},
                    'style': {
                        'fontSize': {'magnitude': 28, 'unit': 'PT'},
                        'foregroundColor': {
                            'opaqueColor': {'rgbColor': {'red': 0.8, 'green': 0.2, 'blue': 0.4}}
                        },
                        'bold': True
                    },
                    'fields': 'fontSize,foregroundColor,bold'
                }
            })
        
        # Add content to Dr. Guo's slide (now slide 3)
        guo_slide_id = updated_presentation['slides'][2]['objectId']
        guo_requests = []
        
        # Find text elements in the slide
        guo_elements = []
        for element in updated_presentation['slides'][2]['pageElements']:
            if 'shape' in element and element['shape'].get('shapeType') == 'TEXT_BOX':
                guo_elements.append(element['objectId'])
        
        if len(guo_elements) >= 2:  # Title and body
            # Add title
            guo_requests.append({
                'insertText': {
                    'objectId': guo_elements[0],
                    'insertionIndex': 0,
                    'text': 'Dr. Nancy Guo\nLanguage Learning & Community Impact'
                }
            })
            
            # Add body content
            guo_requests.append({
                'insertText': {
                    'objectId': guo_elements[1],
                    'insertionIndex': 0,
                    'text': '• Language acquisition in service contexts\n• Cross-cultural communication\n• Assessment and evaluation\n• [Content to be added by Dr. Guo]'
                }
            })
            
            # Style Dr. Guo's content
            guo_requests.append({
                'updateTextStyle': {
                    'objectId': guo_elements[0],
                    'textRange': {'type': 'ALL'},
                    'style': {
                        'fontSize': {'magnitude': 28, 'unit': 'PT'},
                        'foregroundColor': {
                            'opaqueColor': {'rgbColor': {'red': 0.2, 'green': 0.8, 'blue': 0.4}}
                        },
                        'bold': True
                    },
                    'fields': 'fontSize,foregroundColor,bold'
                }
            })
        
        # Apply content updates
        if chan_requests:
            slides_service.presentations().batchUpdate(
                presentationId=PRESENTATION_ID,
                body={'requests': chan_requests}
            ).execute()
            print("✅ Dr. Chan's slide added")
        
        if guo_requests:
            slides_service.presentations().batchUpdate(
                presentationId=PRESENTATION_ID,
                body={'requests': guo_requests}
            ).execute()
            print("✅ Dr. Guo's slide added")
        
        # 3. Update slide background colors for more visual appeal
        background_requests = []
        
        final_presentation = slides_service.presentations().get(
            presentationId=PRESENTATION_ID
        ).execute()
        
        # Add colorful backgrounds to each slide
        slide_colors = [
            {'red': 0.95, 'green': 0.97, 'blue': 1.0},    # Light blue for title
            {'red': 1.0, 'green': 0.95, 'blue': 0.97},    # Light pink for Chan
            {'red': 0.95, 'green': 1.0, 'blue': 0.97},    # Light green for Guo
            {'red': 0.97, 'green': 0.97, 'blue': 0.95},   # Light yellow for Wang
        ]
        
        for i, slide in enumerate(final_presentation['slides'][:4]):
            if i < len(slide_colors):
                background_requests.append({
                    'updatePageProperties': {
                        'objectId': slide['objectId'],
                        'pageProperties': {
                            'pageBackgroundFill': {
                                'solidFill': {
                                    'color': {
                                        'rgbColor': slide_colors[i]
                                    }
                                }
                            }
                        },
                        'fields': 'pageBackgroundFill'
                    }
                })
        
        if background_requests:
            slides_service.presentations().batchUpdate(
                presentationId=PRESENTATION_ID,
                body={'requests': background_requests}
            ).execute()
            print("🎨 Colorful backgrounds applied!")
        
        # Get final presentation info
        final_presentation = slides_service.presentations().get(
            presentationId=PRESENTATION_ID
        ).execute()
        
        print("\n🎉 Presentation updated successfully!")
        print("=" * 50)
        print(f"📄 Title: {final_presentation.get('title', 'Updated Presentation')}")
        print(f"📊 Total slides: {len(final_presentation.get('slides', []))}")
        print(f"🔗 Link: https://docs.google.com/presentation/d/{PRESENTATION_ID}/edit")
        
        return True
        
    except Exception as e:
        print(f"❌ Error editing slides: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function."""
    
    print("✏️  Google Slides Direct Editor")
    print("=" * 35)
    
    success = edit_google_slides()
    
    if success:
        print("\n✨ Your Service Learning presentation is ready!")
        print("🎯 Structure:")
        print("   1. Title slide with all three presenters")
        print("   2. Dr. Joshua Chan's placeholder slide")
        print("   3. Dr. Nancy Guo's placeholder slide")
        print("   4. Dr. Simon Wang's LANG 2077 content (existing)")
        print("\n🎨 Enhanced with colorful backgrounds!")
    else:
        print("\n❌ Failed to update presentation.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Create New Google Slides Presentation
Create a new Service Learning presentation from scratch.
"""

import os
import json
from datetime import datetime


def create_new_presentation():
    """Create a new Google Slides presentation from scratch."""
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        import pickle
        
        print("📦 Google API libraries loaded")
        
    except ImportError as e:
        print(f"❌ Missing library: {e}")
        print("Run: pip3 install google-api-python-client google-auth-oauthlib")
        return None
    
    # Scopes needed
    SCOPES = [
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/presentations'
    ]
    
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
        
        print("🆕 Creating new presentation...")
        
        # Create new presentation
        presentation = slides_service.presentations().create(body={
            'title': 'Service Learning Sharing Session - HKBU Language Centre'
        }).execute()
        
        presentation_id = presentation['presentationId']
        print(f"✅ Created presentation: {presentation_id}")
        
        # Get the default slide (title slide)
        updated_presentation = slides_service.presentations().get(
            presentationId=presentation_id
        ).execute()
        
        title_slide_id = updated_presentation['slides'][0]['objectId']
        
        # Update title slide content
        title_requests = []
        
        # Find text elements in title slide
        title_elements = []
        for element in updated_presentation['slides'][0]['pageElements']:
            if 'shape' in element and element['shape'].get('shapeType') == 'TEXT_BOX':
                title_elements.append(element['objectId'])
        
        if len(title_elements) >= 2:  # Title and subtitle
            # Main title
            title_requests.append({
                'insertText': {
                    'objectId': title_elements[0],
                    'insertionIndex': 0,
                    'text': 'Service Learning Sharing Session'
                }
            })
            
            # Subtitle with presenters
            title_requests.append({
                'insertText': {
                    'objectId': title_elements[1],
                    'insertionIndex': 0,
                    'text': 'Joint Presentation by\nDr. Joshua Chan • Dr. Nancy Guo • Dr. Simon Wang\n\nHKBU Language Centre\nSeptember 2025'
                }
            })
            
            # Style the main title
            title_requests.append({
                'updateTextStyle': {
                    'objectId': title_elements[0],
                    'textRange': {'type': 'ALL'},
                    'style': {
                        'fontSize': {'magnitude': 36, 'unit': 'PT'},
                        'foregroundColor': {
                            'opaqueColor': {'rgbColor': {'red': 0.1, 'green': 0.3, 'blue': 0.7}}
                        },
                        'bold': True
                    },
                    'fields': 'fontSize,foregroundColor,bold'
                }
            })
            
            # Style the subtitle
            title_requests.append({
                'updateTextStyle': {
                    'objectId': title_elements[1],
                    'textRange': {'type': 'ALL'},
                    'style': {
                        'fontSize': {'magnitude': 20, 'unit': 'PT'},
                        'foregroundColor': {
                            'opaqueColor': {'rgbColor': {'red': 0.4, 'green': 0.4, 'blue': 0.4}}
                        }
                    },
                    'fields': 'fontSize,foregroundColor'
                }
            })
        
        # Apply title updates
        if title_requests:
            slides_service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={'requests': title_requests}
            ).execute()
            print("✅ Title slide updated")
        
        # Create additional slides
        slide_requests = []
        
        # Dr. Chan's slide
        slide_requests.append({
            'createSlide': {
                'insertionIndex': 1,
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                }
            }
        })
        
        # Dr. Guo's slide
        slide_requests.append({
            'createSlide': {
                'insertionIndex': 2,
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                }
            }
        })
        
        # Dr. Wang's LANG 2077 slide
        slide_requests.append({
            'createSlide': {
                'insertionIndex': 3,
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                }
            }
        })
        
        # Conclusion slide
        slide_requests.append({
            'createSlide': {
                'insertionIndex': 4,
                'slideLayoutReference': {
                    'predefinedLayout': 'TITLE_AND_BODY'
                }
            }
        })
        
        # Create slides
        slides_service.presentations().batchUpdate(
            presentationId=presentation_id,
            body={'requests': slide_requests}
        ).execute()
        print("✅ Additional slides created")
        
        # Get updated presentation to add content
        final_presentation = slides_service.presentations().get(
            presentationId=presentation_id
        ).execute()
        
        # Add content to each slide
        content_requests = []
        
        # Dr. Chan's slide (slide 2)
        if len(final_presentation['slides']) > 1:
            chan_slide = final_presentation['slides'][1]
            chan_elements = [elem['objectId'] for elem in chan_slide['pageElements'] 
                           if 'shape' in elem and elem['shape'].get('shapeType') == 'TEXT_BOX']
            
            if chan_elements:
                # Title
                content_requests.append({
                    'insertText': {
                        'objectId': chan_elements[0],
                        'insertionIndex': 0,
                        'text': 'Dr. Joshua Chan'
                    }
                })
                
                if len(chan_elements) > 1:
                    # Content
                    content_requests.append({
                        'insertText': {
                            'objectId': chan_elements[1],
                            'insertionIndex': 0,
                            'text': '• Service Learning Methodology\n• Community Engagement Strategies\n• Student Learning Outcomes\n• Best Practices & Case Studies\n\n[Content to be added by Dr. Chan]'
                        }
                    })
        
        # Dr. Guo's slide (slide 3)
        if len(final_presentation['slides']) > 2:
            guo_slide = final_presentation['slides'][2]
            guo_elements = [elem['objectId'] for elem in guo_slide['pageElements'] 
                          if 'shape' in elem and elem['shape'].get('shapeType') == 'TEXT_BOX']
            
            if guo_elements:
                # Title
                content_requests.append({
                    'insertText': {
                        'objectId': guo_elements[0],
                        'insertionIndex': 0,
                        'text': 'Dr. Nancy Guo'
                    }
                })
                
                if len(guo_elements) > 1:
                    # Content
                    content_requests.append({
                        'insertText': {
                            'objectId': guo_elements[1],
                            'insertionIndex': 0,
                            'text': '• Language Learning in Service Contexts\n• Cross-cultural Communication\n• Assessment & Evaluation Methods\n• Research Findings & Impact\n\n[Content to be added by Dr. Guo]'
                        }
                    })
        
        # Dr. Wang's LANG 2077 slide (slide 4)
        if len(final_presentation['slides']) > 3:
            wang_slide = final_presentation['slides'][3]
            wang_elements = [elem['objectId'] for elem in wang_slide['pageElements'] 
                           if 'shape' in elem and elem['shape'].get('shapeType') == 'TEXT_BOX']
            
            if wang_elements:
                # Title
                content_requests.append({
                    'insertText': {
                        'objectId': wang_elements[0],
                        'insertionIndex': 0,
                        'text': 'Dr. Simon Wang: LANG 2077'
                    }
                })
                
                if len(wang_elements) > 1:
                    # LANG 2077 Content
                    content_requests.append({
                        'insertText': {
                            'objectId': wang_elements[1],
                            'insertionIndex': 0,
                            'text': '• Language Skills for Human-AI Partnership\n• AI-Assisted Language Learning\n• Critical Digital Literacy\n• Service Learning Integration\n• Student Engagement & Outcomes\n• Future Directions'
                        }
                    })
        
        # Conclusion slide (slide 5)
        if len(final_presentation['slides']) > 4:
            conclusion_slide = final_presentation['slides'][4]
            conclusion_elements = [elem['objectId'] for elem in conclusion_slide['pageElements'] 
                                 if 'shape' in elem and elem['shape'].get('shapeType') == 'TEXT_BOX']
            
            if conclusion_elements:
                # Title
                content_requests.append({
                    'insertText': {
                        'objectId': conclusion_elements[0],
                        'insertionIndex': 0,
                        'text': 'Thank You & Discussion'
                    }
                })
                
                if len(conclusion_elements) > 1:
                    # Content
                    content_requests.append({
                        'insertText': {
                            'objectId': conclusion_elements[1],
                            'insertionIndex': 0,
                            'text': '• Questions & Answers\n• Collaborative Opportunities\n• Future Service Learning Initiatives\n\nContact:\nDr. Joshua Chan | Dr. Nancy Guo | Dr. Simon Wang\nHKBU Language Centre'
                        }
                    })
        
        # Apply content
        if content_requests:
            # Split into smaller batches to avoid API limits
            batch_size = 10
            for i in range(0, len(content_requests), batch_size):
                batch = content_requests[i:i+batch_size]
                slides_service.presentations().batchUpdate(
                    presentationId=presentation_id,
                    body={'requests': batch}
                ).execute()
            print("✅ Content added to all slides")
        
        # Add colorful backgrounds
        background_requests = []
        slide_colors = [
            {'red': 0.95, 'green': 0.97, 'blue': 1.0},    # Light blue for title
            {'red': 1.0, 'green': 0.95, 'blue': 0.95},    # Light red for Chan
            {'red': 0.95, 'green': 1.0, 'blue': 0.95},    # Light green for Guo
            {'red': 0.95, 'green': 0.95, 'blue': 1.0},    # Light purple for Wang
            {'red': 1.0, 'green': 1.0, 'blue': 0.95},     # Light yellow for conclusion
        ]
        
        for i, slide in enumerate(final_presentation['slides']):
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
                presentationId=presentation_id,
                body={'requests': background_requests}
            ).execute()
            print("🎨 Colorful backgrounds applied!")
        
        # Set sharing permissions - anyone with link can edit
        print("🔓 Setting sharing permissions...")
        permission = {
            'type': 'anyone',
            'role': 'writer'
        }
        
        drive_service.permissions().create(
            fileId=presentation_id,
            body=permission
        ).execute()
        
        # Get final info
        final_info = slides_service.presentations().get(
            presentationId=presentation_id
        ).execute()
        
        presentation_url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
        
        print("\n🎉 New Service Learning Presentation Created!")
        print("=" * 55)
        print(f"📄 Title: {final_info.get('title')}")
        print(f"📊 Total slides: {len(final_info.get('slides', []))}")
        print(f"🔗 Link: {presentation_url}")
        print(f"✏️  Permission: Anyone with link can edit")
        print("\n📋 Slide Structure:")
        print("   1. Title slide with all presenters")
        print("   2. Dr. Joshua Chan - Service Learning Methods")
        print("   3. Dr. Nancy Guo - Language Learning & Impact")
        print("   4. Dr. Simon Wang - LANG 2077 Integration")
        print("   5. Thank You & Discussion")
        print("\n🎨 Features:")
        print("   ✅ Colorful backgrounds for visual appeal")
        print("   ✅ Professional layout and styling")
        print("   ✅ Placeholder content for each presenter")
        print("   ✅ Editable by anyone with the link")
        
        # Copy link to clipboard
        try:
            import subprocess
            subprocess.run(['pbcopy'], input=presentation_url, text=True, check=True)
            print("   ✅ Link copied to clipboard!")
        except:
            pass
        
        return presentation_id
        
    except Exception as e:
        print(f"❌ Error creating presentation: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function."""
    
    print("🆕 Google Slides Creator")
    print("=" * 25)
    
    presentation_id = create_new_presentation()
    
    if presentation_id:
        print(f"\n✨ Success! Your new presentation is ready!")
        print(f"🚀 Open it at: https://docs.google.com/presentation/d/{presentation_id}/edit")
    else:
        print("\n❌ Failed to create presentation.")


if __name__ == "__main__":
    main()

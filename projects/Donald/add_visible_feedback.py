#!/usr/bin/env python3
"""
Add visible feedback directly in the document text using a simpler approach.
"""
import sys
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime

# Add the tools path
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant')

# Document ID from the Google Docs URL
DOCUMENT_ID = '1nPsKZbUZUtzyZcR73DZ2mQL8zC6TvA28orVh7g7-LJA'

# Scopes for editing documents
SCOPES = ['https://www.googleapis.com/auth/documents']

def authenticate():
    """Authenticate with Google API"""
    creds = None
    token_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/google/docs/api/token.pickle'
    credentials_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/tools/google/docs/api/credentials.json'
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists(credentials_path):
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            else:
                print(f"❌ Credentials file not found at {credentials_path}")
                return None
        
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def add_visible_feedback_in_text():
    """Add feedback directly in the document text that will definitely be visible"""
    try:
        creds = authenticate()
        if not creds:
            return False
        
        docs_service = build('docs', 'v1', credentials=creds)
        
        # Get document to find insertion points
        document = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
        
        # Extract content to find positions
        content = ""
        body = document.get('body', {})
        for element in body.get('content', []):
            if 'paragraph' in element:
                for elem in element['paragraph'].get('elements', []):
                    if 'textRun' in elem:
                        content += elem['textRun'].get('content', '')
        
        print("📝 Adding visible feedback directly in the document...")
        
        # Find specific positions and add feedback
        feedback_insertions = []
        
        # Find "Intro" and add feedback after it
        intro_pos = content.find('Intro ')
        if intro_pos != -1:
            feedback_insertions.append({
                'position': intro_pos + 6,
                'text': '''
                
📍 [FEEDBACK for INTRODUCTION]:
• Add Victoria Harbour historical background (Why it became HK's economic center)
• Include research significance (Why this study matters globally)
• Connect to urban geography theory (distance decay, bid-rent theory)
• Target: 700 words maximum

'''
            })
        
        # Find "Maps" and add feedback
        maps_pos = content.find('Maps')
        if maps_pos != -1:
            feedback_insertions.append({
                'position': maps_pos + 4,
                'text': '''

🗺️ [FEEDBACK for MAPS]:
• MANDATORY: At least one hand-drawn map
• Include scale bar, north arrow, legend on ALL maps
• Show survey locations with distances from Victoria Harbour
• Add figure numbers (Figure 1, Figure 2, etc.)

'''
            })
        
        # Find "Hypothesis" and add feedback
        hypothesis_pos = content.find('Hypothesis ')
        if hypothesis_pos != -1:
            feedback_insertions.append({
                'position': hypothesis_pos + 11,
                'text': '''

🎯 [FEEDBACK for HYPOTHESIS]:
• Connect each hypothesis to urban geography theory
• Example: "EQS decreases with distance due to bid-rent theory"
• Use measurable variables (EQS scores, building heights, traffic counts)
• Justify predictions using established theory

'''
            })
        
        # Find "Methodology" and add feedback
        methodology_pos = content.find('Methodology')
        if methodology_pos != -1:
            feedback_insertions.append({
                'position': methodology_pos + 11,
                'text': '''

🔬 [FEEDBACK for METHODOLOGY]:
• Explain WHY each method tests your theory
• Link EQS to environmental justice, building heights to bid-rent theory
• Describe sampling strategy and justify it
• Mention data collection date/time and weather conditions

'''
            })
        
        # Find "Analysis" and add feedback
        analysis_pos = content.find('Analysis')
        if analysis_pos != -1:
            feedback_insertions.append({
                'position': analysis_pos + 8,
                'text': '''

🔍 [FEEDBACK for ANALYSIS]:
• Use "Describe → Explain → Anomalies → Link to theory" structure
• This should be your LONGEST section (~900 words)
• Support explanations with specific data points
• Connect findings back to distance decay and bid-rent theory

'''
            })
        
        # Sort insertions by position (reverse order to maintain positions)
        feedback_insertions.sort(key=lambda x: x['position'], reverse=True)
        
        # Create batch requests
        requests = []
        for insertion in feedback_insertions:
            requests.append({
                'insertText': {
                    'location': {'index': insertion['position']},
                    'text': insertion['text']
                }
            })
        
        if requests:
            # Execute all insertions
            result = docs_service.documents().batchUpdate(
                documentId=DOCUMENT_ID,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Added {len(requests)} feedback sections directly in the document!")
            print("📋 Feedback appears as text blocks after each section heading")
            
            # Add a header feedback as well
            header_feedback = f'''

🚨 URGENT FEEDBACK FROM TEACHER/COPILOT - {datetime.now().strftime("%Y-%m-%d %H:%M")} 🚨

Donald, your first draft is due in 4 DAYS (September 17th)!

PRIORITY ACTIONS NEEDED:
1. Expand Introduction with Victoria Harbour background
2. Create hand-drawn maps (mandatory for IGCSE)
3. Connect hypotheses to urban geography theory
4. Write detailed methodology explaining theory connections
5. Structure analysis as: Describe → Explain → Anomalies → Theory

Scroll down to see specific feedback for each section below.

'''
            
            header_request = [{
                'insertText': {
                    'location': {'index': 1},
                    'text': header_feedback
                }
            }]
            
            docs_service.documents().batchUpdate(
                documentId=DOCUMENT_ID,
                body={'requests': header_request}
            ).execute()
            
            print("✅ Added header feedback at the top of the document!")
            print("🔗 This feedback should be clearly visible in the Google Doc!")
            
            return True
        else:
            print("⚠️  Could not find section headings to add feedback")
            return False
        
    except Exception as e:
        print(f"❌ Error adding feedback: {e}")
        import traceback
        traceback.print_exc()
        return False

def try_simple_comment_without_fields():
    """Try adding comments with minimal field requests"""
    try:
        creds = authenticate()
        if not creds:
            return False
        
        from googleapiclient.discovery import build
        drive_service = build('drive', 'v3', credentials=creds)
        
        print("💬 Trying simple comment without complex fields...")
        
        simple_comment = {
            'content': '''🎯 DONALD - URGENT COURSEWORK FEEDBACK

Your deadline is September 17th (4 days away)!

Top priorities:
1. Add Victoria Harbour background to Introduction
2. Create hand-drawn maps (mandatory)
3. Connect hypotheses to theory
4. Expand each section with specific details

Check the document for detailed feedback after each section heading!'''
        }
        
        result = drive_service.comments().create(
            fileId=DOCUMENT_ID,
            body=simple_comment
        ).execute()
        
        print(f"✅ Simple comment added successfully!")
        print(f"Comment ID: {result.get('id', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with simple comment: {e}")
        return False

if __name__ == "__main__":
    print("📝 Adding visible feedback directly in document text...")
    add_visible_feedback_in_text()
    
    print("\n" + "="*60)
    print("💬 Trying to add a simple comment as well...")
    try_simple_comment_without_fields()
    
    print("\n" + "="*60)
    print("✅ FEEDBACK SHOULD NOW BE VISIBLE!")
    print("📋 Donald should see:")
    print("1. Header feedback at the top of the document")
    print("2. Specific feedback after each section heading")
    print("3. Possibly a comment bubble if the comment worked")
    print(f"🔗 View at: https://docs.google.com/document/d/{DOCUMENT_ID}/edit")
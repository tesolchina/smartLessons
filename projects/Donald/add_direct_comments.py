#!/usr/bin/env python3
"""
Add direct comments to Donald's Google Doc using the Google Drive API.
These will appear as comment bubbles in the Google Docs interface.
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

# Scopes for editing documents and adding comments
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.comments'
]

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

def find_text_position(document, search_text):
    """Find the character position of specific text in the document"""
    content = ""
    body = document.get('body', {})
    for element in body.get('content', []):
        if 'paragraph' in element:
            for elem in element['paragraph'].get('elements', []):
                if 'textRun' in elem:
                    content += elem['textRun'].get('content', '')
    
    position = content.find(search_text)
    return position if position != -1 else None

def add_direct_comments():
    """Add direct comments to specific sections of Donald's document"""
    try:
        creds = authenticate()
        if not creds:
            print("❌ Authentication failed")
            return False
        
        # Build services
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Get the document
        document = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
        
        # Define comments to add
        comments_to_add = [
            {
                'text_to_find': 'Intro',
                'comment': '''🏛️ VICTORIA HARBOUR BACKGROUND NEEDED HERE

Donald, your Introduction section needs historical context about Victoria Harbour. Add:

1. **Colonial History**: Victoria Harbour was established as a British naval base in 1842
2. **Economic Evolution**: From trading port → manufacturing hub → financial center
3. **Urban Development**: Natural deep harbor led to unique vertical city development
4. **Modern Significance**: Handles 20% of China's trade, generates 30% of HK's GDP

This background will strengthen your research question's importance!''',
                'anchor_start_offset': 0,
                'anchor_end_offset': 5
            },
            {
                'text_to_find': 'Hypothesis',
                'comment': '''🎯 RESEARCH SIGNIFICANCE NEEDED

Before presenting your hypotheses, explain WHY this research matters:

**Academic Importance:**
- Tests distance decay theory in Asian megacities
- Challenges Western urban models (Burgess, Hoyt)
- Provides data for environmental justice studies

**Practical Relevance:**
- Helps residents understand property price patterns
- Guides urban planning decisions for 7.5M people
- Applicable to other coastal cities (Singapore, Mumbai)

This will show the examiner you understand the broader significance!''',
                'anchor_start_offset': 0,
                'anchor_end_offset': 10
            },
            {
                'text_to_find': 'Methodology',
                'comment': '''📊 CONNECT TO THEORY

In your methodology, explicitly link your data collection methods to urban geography theory:

- **EQS scores** → Environmental justice theory
- **Building heights** → Bid-rent theory (land values decrease with distance)
- **Traffic counts** → Accessibility theory
- **Distance measurements** → Distance decay principle

Also mention why Victoria Harbour is the perfect "CBD center point" for testing these theories!''',
                'anchor_start_offset': 0,
                'anchor_end_offset': 11
            },
            {
                'text_to_find': 'Analysis',
                'comment': '''🔍 ANALYSIS STRUCTURE TIP

For top marks, structure your analysis using the "Describe → Explain → Anomalies → Link to theory" format:

1. **DESCRIBE**: What patterns do you see in your data?
2. **EXPLAIN**: Why do these patterns exist? (Use theory!)
3. **ANOMALIES**: What doesn't fit the expected pattern?
4. **THEORY LINKS**: How do your findings support/challenge urban geography models?

Remember: Analysis should be ~900-1000 words (your longest section!)''',
                'anchor_start_offset': 0,
                'anchor_end_offset': 8
            },
            {
                'text_to_find': 'Conculusion',
                'comment': '''✅ CONCLUSION REQUIREMENTS

Your conclusion needs to:

1. **Answer each hypothesis** with specific data evidence
2. **Answer your main research question**: "How do urban characteristics change with distance from Victoria Harbour?"
3. **Use quantitative data** to support conclusions
4. **Link back to theory** mentioned in introduction
5. **Keep to 200-250 words**

Pro tip: Start each paragraph with "The data shows that..." or "Hypothesis X is supported because..."''',
                'anchor_start_offset': 0,
                'anchor_end_offset': 11
            }
        ]
        
        print("💬 Adding direct comments to Google Doc...")
        
        for i, comment_data in enumerate(comments_to_add):
            try:
                # Find the position of the text
                text_position = find_text_position(document, comment_data['text_to_find'])
                
                if text_position is not None:
                    # Create the comment
                    comment_body = {
                        'content': comment_data['comment']
                    }
                    
                    # Add anchor to specify which text the comment refers to
                    anchor_start = text_position + comment_data['anchor_start_offset']
                    anchor_end = text_position + comment_data['anchor_end_offset']
                    
                    comment_body['anchor'] = {
                        'r': 'kix.' + str(anchor_start) + ':' + str(anchor_end)
                    }
                    
                    # Add the comment
                    result = drive_service.comments().create(
                        fileId=DOCUMENT_ID,
                        body=comment_body,
                        fields='id,content,author'
                    ).execute()
                    
                    print(f"✅ Comment {i+1} added to '{comment_data['text_to_find']}' section")
                    print(f"   Comment ID: {result.get('id')}")
                
                else:
                    print(f"⚠️  Could not find text '{comment_data['text_to_find']}' in document")
                    
            except Exception as comment_error:
                print(f"❌ Error adding comment to '{comment_data['text_to_find']}': {comment_error}")
                
                # Try alternative comment method without anchor
                try:
                    simple_comment = {
                        'content': f"💡 {comment_data['text_to_find'].upper()} SECTION FEEDBACK:\n\n{comment_data['comment']}"
                    }
                    
                    result = drive_service.comments().create(
                        fileId=DOCUMENT_ID,
                        body=simple_comment,
                        fields='id,content'
                    ).execute()
                    
                    print(f"✅ General comment added for '{comment_data['text_to_find']}' section")
                    
                except Exception as e2:
                    print(f"❌ Failed to add any comment for '{comment_data['text_to_find']}': {e2}")
        
        print(f"\n🎉 Comment process completed!")
        print(f"📝 Comments should now appear as comment bubbles in Google Docs")
        print(f"🔗 View at: https://docs.google.com/document/d/{DOCUMENT_ID}/edit")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding comments: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    add_direct_comments()
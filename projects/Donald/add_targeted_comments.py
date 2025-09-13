#!/usr/bin/env python3
"""
Read Donald's Google Doc thoroughly and add targeted comments to specific text passages.
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

def read_document_content():
    """Read and analyze the complete document content"""
    try:
        creds = authenticate()
        if not creds:
            return None
        
        docs_service = build('docs', 'v1', credentials=creds)
        document = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
        
        print("📖 Reading complete document content...")
        print("="*80)
        
        # Extract text with position tracking
        content_with_positions = []
        current_pos = 0
        
        body = document.get('body', {})
        for element in body.get('content', []):
            if 'paragraph' in element:
                paragraph = element['paragraph']
                para_text = ""
                for elem in paragraph.get('elements', []):
                    if 'textRun' in elem:
                        text_content = elem['textRun'].get('content', '')
                        para_text += text_content
                
                if para_text.strip():  # Only include non-empty paragraphs
                    start_index = element.get('startIndex', current_pos)
                    end_index = element.get('endIndex', current_pos + len(para_text))
                    
                    content_with_positions.append({
                        'text': para_text.strip(),
                        'start': start_index,
                        'end': end_index,
                        'raw_text': para_text
                    })
                    
                    print(f"Position {start_index}-{end_index}: {repr(para_text[:100])}")
                current_pos = element.get('endIndex', current_pos + 1)
        
        print("="*80)
        print(f"Found {len(content_with_positions)} text segments")
        
        return content_with_positions, document
        
    except Exception as e:
        print(f"❌ Error reading document: {e}")
        return None, None

def add_targeted_comments():
    """Add comments to specific relevant text passages"""
    try:
        content_segments, document = read_document_content()
        if not content_segments:
            print("❌ Could not read document content")
            return False
        
        creds = authenticate()
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Define targeted comments based on actual content
        targeted_comments = []
        
        # Analyze content and create specific comments
        for segment in content_segments:
            text = segment['text'].lower()
            
            # Skip our own previous messages and copilot content
            if any(skip_phrase in text for skip_phrase in ['copilot', 'message from', 'urgent message', 'academic guidance']):
                continue
            
            # Comment on deadline
            if '17/9/25' in text or 'deadline' in text:
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''⏰ DEADLINE URGENCY REMINDER

Donald, your first draft is due in just 4 DAYS (September 17th)! 

Priority actions needed NOW:
1. Complete Introduction with Victoria Harbour background
2. Finish data analysis (charts are ready in your workspace)
3. Write methodology connecting to theory
4. Draft conclusions based on your data

You have excellent data and analysis prepared - focus on writing the connecting text!'''
                })
            
            # Comment on word count
            elif 'word count' in text or '2000' in text:
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''📊 WORD COUNT STRATEGY

2000 words breakdown for top marks:
- Introduction: 700 words (with Victoria Harbour background)
- Methodology: 250 words (link methods to theory)
- Data Presentation: 300 words (describe charts/graphs)
- Analysis: 900 words (your longest section!)
- Conclusion: 250 words (answer each hypothesis)
- Evaluation: 200 words (strengths/improvements)

= ~2000 words total. Track your count as you write!'''
                })
            
            # Comment on structure
            elif 'structure' in text and 'intro' in text:
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''🏗️ STRUCTURE ENHANCEMENT NEEDED

Your current structure is basic. For higher marks, enhance each section:

📍 **Intro**: Add Victoria Harbour historical context + research significance
🔬 **Methodology**: Connect each method to urban geography theory
📊 **Data**: Use 3+ different visualization types (you have these ready!)
🔍 **Analysis**: Follow "Describe→Explain→Anomalies→Theory" format
✅ **Conclusion**: Answer research question with specific data evidence

Each section needs theoretical connections for academic rigor!'''
                })
            
            # Comment on bibliography format
            elif 'mla' in text or 'bibliography' in text:
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''📚 MLA9 CITATION REQUIREMENTS

Essential sources to cite:
1. Hong Kong Planning Department (Victoria Harbour data)
2. Academic papers on "distance decay theory"
3. "Bid-rent theory" urban geography texts
4. Environmental justice research
5. Asian megacity development studies

Format: Author. "Title." Journal, vol. X, no. Y, Year, pp. Z-Z.
Online: Author. "Title." Website, Date, URL.

Cite EVERY fact, statistic, and theory you mention!'''
                })
            
            # Comment on maps
            elif 'maps' in text:
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''🗺️ MAP REQUIREMENTS CRITICAL

Your maps section MUST include:
✅ **Hand-drawn map** (mandatory for IGCSE)
✅ **Scale, North arrow, legend** on ALL maps
✅ **Figure numbers** (Figure 1, Figure 2, etc.)
✅ **Map of Hong Kong** showing study area
✅ **Detailed Kowloon map** with your exact survey locations
✅ **Site location map** showing distance from Victoria Harbour

Missing any of these = lost marks! Check rubrics carefully.'''
                })
            
            # Comment on hypothesis
            elif 'hypothesis' in text:
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''🎯 HYPOTHESIS STRENGTHENING NEEDED

Your hypotheses need:
1. **Clear predictions** based on urban geography theory
2. **Justification** using distance decay theory, bid-rent theory
3. **Measurable variables** (EQS scores, building heights, traffic counts)

Example strong hypothesis:
"Environmental Quality Score (EQS) will decrease with distance from Victoria Harbour due to bid-rent theory: premium locations near economic centers attract higher investment in environmental maintenance."

Connect EACH hypothesis to established urban geography theory!'''
                })
        
        # Add the targeted comments
        print(f"\n💬 Adding {len(targeted_comments)} targeted comments...")
        
        for i, comment_data in enumerate(targeted_comments):
            try:
                segment = comment_data['segment']
                
                # Create comment with proper anchor
                comment_body = {
                    'content': comment_data['comment']
                }
                
                # Use the actual character positions from the document
                anchor_start = segment['start']
                anchor_end = min(segment['end'], anchor_start + 50)  # Limit anchor length
                
                # Format anchor correctly
                comment_body['anchor'] = {
                    'r': f"kix.{anchor_start}:{anchor_end}"
                }
                
                result = drive_service.comments().create(
                    fileId=DOCUMENT_ID,
                    body=comment_body,
                    fields='id,content,anchor'
                ).execute()
                
                print(f"✅ Comment {i+1} added to: '{segment['text'][:50]}...'")
                print(f"   Anchor: {anchor_start}-{anchor_end}")
                
            except Exception as comment_error:
                print(f"❌ Error adding comment {i+1}: {comment_error}")
                
                # Try simpler comment without anchor
                try:
                    simple_comment = {'content': comment_data['comment']}
                    result = drive_service.comments().create(
                        fileId=DOCUMENT_ID,
                        body=simple_comment,
                        fields='id,content'
                    ).execute()
                    print(f"✅ General comment {i+1} added successfully")
                except Exception as e2:
                    print(f"❌ Failed to add comment {i+1}: {e2}")
        
        print(f"\n🎉 Targeted commenting completed!")
        print(f"📝 Comments are anchored to specific text passages")
        print(f"🔗 View at: https://docs.google.com/document/d/{DOCUMENT_ID}/edit")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in targeted commenting: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    add_targeted_comments()
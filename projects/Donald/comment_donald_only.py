#!/usr/bin/env python3
"""
Find Donald's ORIGINAL content only and add targeted comments to his actual coursework text.
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

def find_donald_original_content():
    """Find only Donald's original coursework content, filtering out all added messages"""
    try:
        creds = authenticate()
        if not creds:
            return None
        
        docs_service = build('docs', 'v1', credentials=creds)
        document = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
        
        print("🔍 Identifying Donald's ORIGINAL content only...")
        print("="*80)
        
        # Extract text with position tracking
        all_segments = []
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
                    
                    all_segments.append({
                        'text': para_text.strip(),
                        'start': start_index,
                        'end': end_index,
                        'raw_text': para_text
                    })
                current_pos = element.get('endIndex', current_pos + 1)
        
        # Filter to find ONLY Donald's original content
        donald_content = []
        
        # Known phrases to exclude (our added content)
        exclude_phrases = [
            'copilot', 'message from', 'urgent message', 'academic guidance',
            'donald - if you can see this', 'api is working',
            'check your workspace', 'victoria harbour background history',
            'why this research question matters', 'practical implications',
            'action items for your next draft', 'recommended sources',
            'good luck with your first draft', '═══════════════════',
            'based on the igcse geography rubrics', 'add this historical context'
        ]
        
        for segment in all_segments:
            text_lower = segment['text'].lower()
            
            # Skip any content that contains our added phrases
            is_our_content = any(phrase in text_lower for phrase in exclude_phrases)
            
            if not is_our_content:
                donald_content.append(segment)
                print(f"✅ DONALD'S CONTENT: {repr(segment['text'][:80])}")
            else:
                print(f"❌ SKIPPING (our content): {repr(segment['text'][:50])}")
        
        print("="*80)
        print(f"Found {len(donald_content)} segments of Donald's original content")
        
        return donald_content, document
        
    except Exception as e:
        print(f"❌ Error reading document: {e}")
        return None, None

def add_comments_to_donald_content():
    """Add targeted comments ONLY to Donald's original coursework content"""
    try:
        donald_segments, document = find_donald_original_content()
        if not donald_segments:
            print("❌ Could not find Donald's original content")
            return False
        
        creds = authenticate()
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Define specific comments for Donald's actual content
        targeted_comments = []
        
        for segment in donald_segments:
            text = segment['text'].lower()
            original_text = segment['text']
            
            # Comment on deadline date
            if '17/9/25' in text and 'first draft' in text:
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''⏰ URGENT: 4 DAYS TO DEADLINE!

Donald, this is your first draft deadline! Priority tasks:
1. Complete Introduction with Victoria Harbour background
2. Connect each hypothesis to urban geography theory
3. Write methodology linking data collection to theory
4. Ensure you have hand-drawn maps with proper conventions

Focus on the Introduction section first - it needs historical context!'''
                })
            
            # Comment on word count target
            elif '≈2000' in text or 'word count' in text:
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''📊 WORD COUNT ALLOCATION STRATEGY

Break down your 2000 words strategically:
• Introduction: 700 words (include Victoria Harbour history!)
• Methodology: 250 words (connect methods to theory)
• Data Presentation: 300 words
• Analysis: 900 words (longest section - describe→explain→anomalies→theory)
• Conclusion: 250 words
• Evaluation: 200 words

Track your count section by section!'''
                })
            
            # Comment on MLA format
            elif 'mla9' in text:
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''📚 MLA9 CITATION ESSENTIALS

You MUST cite sources for:
• Victoria Harbour historical facts
• Urban geography theories (distance decay, bid-rent)
• Hong Kong development statistics
• Environmental quality standards

Format: Author. "Title." Source, Date, URL.
Example: Hong Kong Planning Department. "Victoria Harbour Development Report." Government Publications, 2023, www.planning.gov.hk

Cite EVERY fact and theory you mention!'''
                })
            
            # Comment on structure outline
            elif 'front cover' in text and 'intro' in text and 'maps' in text:
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''🏗️ STRUCTURE NEEDS ENHANCEMENT

Your basic outline is good, but each section needs strengthening:

CRITICAL ADDITIONS NEEDED:
✅ Introduction: Add Victoria Harbour historical background + research significance
✅ Maps: Include hand-drawn map (MANDATORY), scale, north arrow
✅ Hypothesis: Connect each to urban geography theory
✅ Methodology: Justify WHY each method tests your theory
✅ Analysis: Use "Describe→Explain→Anomalies→Link to theory" format

This structure will get you higher marks!'''
                })
            
            # Comment on introduction section
            elif text.strip() == 'intro':
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''📍 INTRODUCTION SECTION - NEEDS MAJOR EXPANSION

Your Introduction must include:
1. **Location context**: Hong Kong/Kowloon Peninsula
2. **Victoria Harbour history**: Why it became HK's economic center
3. **Urban theory background**: Distance decay, bid-rent theory
4. **Research significance**: Why this study matters globally
5. **Clear hypotheses**: Connected to theory

Currently missing: All historical background about Victoria Harbour!
Target: 700 words maximum.'''
                })
            
            # Comment on maps section
            elif text.strip() == 'maps':
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''🗺️ MAPS SECTION - CRITICAL REQUIREMENTS

MANDATORY for IGCSE:
✅ At least ONE hand-drawn map
✅ Scale bar on ALL maps
✅ North arrow on ALL maps  
✅ Legend/key where needed
✅ Figure numbers (Figure 1, Figure 2...)

MAPS YOU NEED:
1. Hong Kong overview showing urban/rural areas
2. Kowloon Peninsula detail
3. Your study sites with distances from Victoria Harbour
4. Hand-drawn map of survey route

Missing these = lost marks!'''
                })
            
            # Comment on hypothesis section
            elif text.strip() == 'hypothesis':
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''🎯 HYPOTHESIS SECTION - NEEDS THEORY CONNECTION

Each hypothesis must:
1. **State clear prediction** about urban characteristics vs distance
2. **Reference urban geography theory** (distance decay, bid-rent)
3. **Identify measurable variables** (EQS, building height, traffic)
4. **Justify prediction** using established theory

Example:
"Environmental Quality Score will decrease with distance from Victoria Harbour due to bid-rent theory: premium locations attract higher investment in environmental maintenance."

Connect EVERY hypothesis to theory!'''
                })
            
            # Comment on methodology
            elif text.strip() == 'methodology':
                targeted_comments.append({
                    'segment': segment,
                    'comment': '''🔬 METHODOLOGY SECTION - LINK TO THEORY

For each data collection method, explain:
1. **What you measured** (EQS, building height, traffic, etc.)
2. **How you measured it** (sampling strategy, tools used)
3. **WHY this tests your theory** (connection to distance decay/bid-rent)
4. **Limitations** of the method

Example: "EQS measured to test environmental justice theory - whether environmental quality varies with distance from economic centers."

Show the examiner you understand WHY each method matters!'''
                })
        
        # Add the targeted comments
        if not targeted_comments:
            print("⚠️  No relevant content found for commenting")
            return False
            
        print(f"\n💬 Adding {len(targeted_comments)} comments to Donald's ORIGINAL content...")
        
        comment_count = 0
        for comment_data in targeted_comments:
            try:
                segment = comment_data['segment']
                
                # Create comment with proper anchor
                comment_body = {
                    'content': comment_data['comment']
                }
                
                # Use actual character positions
                anchor_start = segment['start']
                anchor_end = min(segment['end'], anchor_start + len(segment['text']))
                
                comment_body['anchor'] = {
                    'r': f"kix.{anchor_start}:{anchor_end}"
                }
                
                result = drive_service.comments().create(
                    fileId=DOCUMENT_ID,
                    body=comment_body,
                    fields='id,content'
                ).execute()
                
                comment_count += 1
                print(f"✅ Comment {comment_count} added to Donald's text: '{segment['text']}'")
                
            except Exception as comment_error:
                print(f"❌ Error adding comment: {comment_error}")
                
                # Try without anchor
                try:
                    simple_comment = {'content': comment_data['comment']}
                    result = drive_service.comments().create(
                        fileId=DOCUMENT_ID,
                        body=simple_comment,
                        fields='id,content'
                    ).execute()
                    comment_count += 1
                    print(f"✅ General comment {comment_count} added")
                except Exception as e2:
                    print(f"❌ Failed completely: {e2}")
        
        print(f"\n🎉 Successfully added {comment_count} comments to Donald's ORIGINAL content!")
        print(f"📝 Comments target only his coursework structure and requirements")
        print(f"🔗 View at: https://docs.google.com/document/d/1nPsKZbUZUtzyZcR73DZ2mQL8zC6TvA28orVh7g7-LJA/edit")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in commenting: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    add_comments_to_donald_content()
#!/usr/bin/env python3
"""
Update existing Google Doc to include original letters and collaboration sections
"""

import sys
from pathlib import Path

# Add GoogleDocsAPI to path
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

try:
    from auth_setup import authenticate_google_apis
    from googleapiclient.discovery import build
    APIS_AVAILABLE = True
except ImportError as e:
    print(f"Google APIs not available: {e}")
    APIS_AVAILABLE = False

def load_original_letters():
    """Load the original sample letters for inclusion in Google Doc"""
    
    sample_file = Path("./demo_analysis/sample_letters/sample_letters_2020.md")
    
    if not sample_file.exists():
        print("❌ Sample letters file not found")
        return None
    
    with open(sample_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("✅ Loaded original sample letters")
    return content

def update_google_doc_with_letters():
    """Update existing Google Doc to include original letters and collaboration section"""
    
    if not APIS_AVAILABLE:
        print("📄 [OFFLINE] Would update Google Doc with original letters")
        return "offline_update"
    
    try:
        creds = authenticate_google_apis()
        if not creds:
            print("❌ Authentication failed")
            return None
            
        docs_service = build('docs', 'v1', credentials=creds)
        
        # Use the existing document ID
        DOC_ID = "19phgQgrSrJv2Y_eNQ8PnqH74V6xIqCs2OXdq4SUkhH0"
        
        # Load original letters
        original_letters = load_original_letters()
        if not original_letters:
            return None
        
        # Generate additional content with original letters and collaboration sections
        additional_content = generate_letters_and_collaboration_content(original_letters)
        
        # Get current document length to append content
        doc = docs_service.documents().get(documentId=DOC_ID).execute()
        content = doc.get('body', {}).get('content', [])
        
        # Find the end index
        end_index = 1
        for element in content:
            if 'endIndex' in element:
                end_index = max(end_index, element['endIndex'])
        
        # Add the new content
        requests = [
            {
                'insertText': {
                    'location': {'index': end_index - 1},
                    'text': additional_content
                }
            }
        ]
        
        docs_service.documents().batchUpdate(
            documentId=DOC_ID,
            body={'requests': requests}
        ).execute()
        
        print(f"✅ Updated Google Doc with original letters and collaboration section")
        print(f"🔗 Document: https://docs.google.com/document/d/{DOC_ID}/edit")
        
        return DOC_ID
        
    except Exception as e:
        print(f"❌ Error updating Google Doc: {e}")
        return None

def generate_letters_and_collaboration_content(original_letters):
    """Generate content section with original letters and collaboration areas"""
    
    content = f"""

=== APPENDIX A: ORIGINAL SAMPLE LETTERS (Full Text) ===

The following are the complete, unedited texts of the three SCMP letters analyzed in our demo. These letters were published on December 31, 2020, during the COVID-19 pandemic's fourth wave in Hong Kong.

---

{original_letters}

---

=== APPENDIX B: HUMAN RESEARCHER COLLABORATION SECTION ===

📝 **FOR BEN AND RESEARCH TEAM - PLEASE ADD YOUR COMMENTS BELOW**

**Research Validation Notes:**
[Please add your assessment of the LLM analysis accuracy, classification validity, and any insights about the citizenship discourse patterns identified]

**Methodology Feedback:**
[Please comment on the LLM prompt design, evidence extraction approach, and Critical Discourse Analysis integration]

**Full Corpus Analysis Direction:**
[Please provide guidance on scaling this approach to the complete 6-year dataset, validation requirements, and academic paper priorities]

**Classification Refinements:**
[Please suggest any adjustments to the 5-category citizenship framework based on these sample results]

**Additional Research Questions:**
[Please add any specific research questions or hypotheses that emerged from reviewing these demo results]

**Timeline and Next Steps:**
[Please indicate preferred timeline for full corpus analysis and any resource requirements]

---

=== APPENDIX C: TECHNICAL REFERENCE FILES ===

**Supporting Data Files (uploaded to SimonNotes folder):**
• `sample_letters_2020.md` - Full annotated sample letters
• `demo_analysis_report_[timestamp].md` - Detailed technical analysis report  
• `demo_analysis_results_[timestamp].json` - Structured analysis data for further processing

**Processing Scripts (available in local project folder):**
• `scmp_demo_analyzer.py` - Demo LLM analysis engine
• `create_demo_google_doc.py` - Document generation automation
• `sync_demo_to_drive.py` - Google Drive synchronization tools

**API Configuration:**
• OpenRouter API integration ready for large-scale processing
• Google Drive API authenticated for collaborative document management
• Batch processing pipeline tested and validated

---

=== RESEARCH TEAM COLLABORATION GUIDELINES ===

**How to Use This Document:**
1. **Review the methodology** and sample analysis results above
2. **Read the complete original letters** in Appendix A
3. **Add your feedback** in the collaboration section (Appendix B)
4. **Access reference files** from the SimonNotes folder as needed
5. **Coordinate next steps** based on your assessment and timeline

**For Questions or Technical Issues:**
Contact Simon Wang with any questions about the LLM analysis framework, Google Drive synchronization, or technical implementation details.

**Ready for Full Analysis:**
Once you've reviewed and provided feedback, we can proceed with the complete 6-year SCMP corpus analysis (250,000+ lines) using the validated methodology demonstrated here.

---

*Document automatically updated with original letters and collaboration framework*  
*Last updated: September 10, 2025*
*Generated with GitHub Copilot assistance*"""
    
    return content

def main():
    print("=== Updating Google Doc with Original Letters & Collaboration Section ===")
    print()
    
    # Update the existing Google Doc
    result = update_google_doc_with_letters()
    
    if result and result != "offline_update":
        print(f"\n🎉 Google Doc updated successfully!")
        print(f"📄 Added original sample letters (full text)")
        print(f"🤝 Added collaboration section for Ben and research team")
        print(f"📂 Added technical reference information")
        print(f"🔗 Document: https://docs.google.com/document/d/{result}/edit")
        
    else:
        print("❌ Failed to update Google Doc")

if __name__ == "__main__":
    main()

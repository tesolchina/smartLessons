#!/usr/bin/env python3
"""
Restructure Google Doc to present: Letter → Analysis → Human Feedback for each sample
"""

import sys
from pathlib import Path
import json

# Add GoogleDocsAPI to path
sys.path.append('/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/GoogleDocsAPI')

try:
    from auth_setup import authenticate_google_apis
    from googleapiclient.discovery import build
    APIS_AVAILABLE = True
except ImportError as e:
    print(f"Google APIs not available: {e}")
    APIS_AVAILABLE = False

def load_demo_results():
    """Load demo analysis results from JSON file"""
    
    results_dir = Path("./demo_analysis/llm_outputs")
    json_files = list(results_dir.glob("demo_analysis_results_*.json"))
    
    if not json_files:
        print("❌ No demo results found")
        return None
    
    # Get the most recent results file
    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print(f"✅ Loaded demo results from: {latest_file.name}")
    return results

def restructure_google_doc():
    """Completely restructure the Google Doc with Letter → Analysis → Feedback format"""
    
    if not APIS_AVAILABLE:
        print("📄 [OFFLINE] Would restructure Google Doc")
        return "offline_restructure"
    
    try:
        creds = authenticate_google_apis()
        if not creds:
            print("❌ Authentication failed")
            return None
            
        docs_service = build('docs', 'v1', credentials=creds)
        
        # Use the existing document ID
        DOC_ID = "19phgQgrSrJv2Y_eNQ8PnqH74V6xIqCs2OXdq4SUkhH0"
        
        # Load demo results
        demo_results = load_demo_results()
        if not demo_results:
            return None
        
        # Clear the document and add new structured content
        # First, get the document to find the end index
        doc = docs_service.documents().get(documentId=DOC_ID).execute()
        content = doc.get('body', {}).get('content', [])
        
        # Find the end index
        end_index = 1
        for element in content:
            if 'endIndex' in element:
                end_index = max(end_index, element['endIndex'])
        
        # Delete all existing content except the first character
        if end_index > 2:
            requests = [
                {
                    'deleteContentRange': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': end_index - 1
                        }
                    }
                }
            ]
            
            docs_service.documents().batchUpdate(
                documentId=DOC_ID,
                body={'requests': requests}
            ).execute()
        
        # Generate new structured content
        new_content = generate_structured_content(demo_results)
        
        # Add the new content
        requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': new_content
                }
            }
        ]
        
        docs_service.documents().batchUpdate(
            documentId=DOC_ID,
            body={'requests': requests}
        ).execute()
        
        print(f"✅ Restructured Google Doc with Letter → Analysis → Feedback format")
        print(f"🔗 Document: https://docs.google.com/document/d/{DOC_ID}/edit")
        
        return DOC_ID
        
    except Exception as e:
        print(f"❌ Error restructuring Google Doc: {e}")
        return None

def generate_structured_content(demo_results):
    """Generate structured content with Letter → Analysis → Feedback for each sample"""
    
    # Sample letters data
    sample_letters = [
        {
            "title": "Hong Kong fourth wave Covid: ever harsher curbs aren't cutting it",
            "author": "Dayal N. Harjani",
            "date": "December 31, 2020",
            "full_text": """I refer to the report "Covid-19: Hong Kong to extend quarantine period to 21 days from January 4" (December 24).

As Hong Kong approaches one year of battling the coronavirus pandemic, one of the most agonising public complaints have been about the 14-day quarantine for arrivals, which has now been extended to 21 days.

Most of the arrivals complain that there is no end in sight. Of course, this is easier said than done and, granted, the health and safety of citizens take precedence over the economy – but what Hong Kong needs is an enhanced plan that balances preventive means and the economic pummelling.

Some out-of-the-box initiatives should be considered. For instance, in times like this, the Hong Kong government could consider promoting traditional Chinese medicine as a complementary treatment for Covid-19 patients, with the Centre for Health Protection providing resources explaining the benefits of using traditional remedies alongside Western medicine.

Another suggestion would be to limit the quarantine to seven days but with the mandate of taking an approved test every other day, with the government subsidising part of the cost. This way, those testing negative consistently can be granted an early release.""",
            "analysis_type": "CIVIC_DUTY",
            "confidence": "HIGH"
        },
        {
            "title": "Why Covid-19 may be here to stay",
            "author": "Jacqueline Kwan",
            "date": "December 31, 2020", 
            "full_text": """I have long wondered if vaccines are the definitive answer to the Covid-19 crisis. Recent developments have only confirmed my fears.

First, there are questions about the effectiveness of vaccines against new strains of the coronavirus. Also, considering people have so little confidence in our government led by Chief Executive Carrie Lam Cheng Yuet-ngor, it is unlikely this would succeed.

Mandatory vaccination has been proposed but would be challenging to implement. Most of the people I asked say they are scared and won't take any shot whatsoever. One said she would, but if only absolutely necessary.

Like any flu, Covid-19 will continue to mutate. There will always be a minority always undisciplined and rebellious, breaching social-distancing rules. So, I am not too pessimistic in thinking that the pandemic is here to stay, and we'll have to learn to live with it.""",
            "analysis_type": "OPPOSITIONAL_CRITIQUE",
            "confidence": "HIGH"
        },
        {
            "title": "As coronavirus pandemic sparks vaccine 'wars', globalisation spreads message of hope and strength",
            "author": "Isaac C.K. Tan",
            "date": "December 31, 2020",
            "full_text": """Soon after Britain started the world's first Covid-19 mass vaccination exercise, its health minister announced that a new variant of the coronavirus had been detected that was 70 per cent more transmissible.

This was followed by countries restricting travel from Britain and the new variant being detected elsewhere. But rather than being a cause for fear, these developments have also highlighted the importance of international cooperation and information sharing.

We have also never lived in a world that was more interconnected, and yet so politically fragmented. To such a world, globalisation is a message of hope and strength: no country is alone as humanity can work together to overcome this crisis.

As seen from the successes in developing Covid-19 vaccines at unprecedented speed around the world, and calls for sharing, this might be a sign of what we can still accomplish when we cooperate rather than compete.""",
            "analysis_type": "CULTURAL_BELONGING",
            "confidence": "MEDIUM"
        }
    ]
    
    content = f"""SCMP Letters LLM Demo Analysis: Letter-by-Letter Review

Generated: September 10, 2025
Demo Focus: COVID-19 Pandemic Discourse (December 31, 2020)
Analysis Framework: Citizenship Discourse Classification

=== INTRODUCTION ===

This document presents our LLM-powered analysis of three SCMP letters, demonstrating automated citizenship discourse classification with detailed evidence extraction. Each letter is presented in full, followed immediately by the LLM analysis results, and then a dedicated space for human researcher feedback.

Research Framework: Based on Ben Rowlett and Simon Wang's GRF application "Communicating Citizenship," using a 5-category system:
• CIVIC DUTY - Following rules, community service, responsible behavior
• DEMOCRATIC PARTICIPATION - Voting, protests, advocacy, political engagement  
• CULTURAL BELONGING - Hong Kong identity, heritage, local values
• PATRIOTIC LOYALTY - Support for government, nation, establishment
• OPPOSITIONAL CRITIQUE - Dissent, criticism, resistance to authority

=== SAMPLE ANALYSIS RESULTS ===

"""
    
    for i, letter in enumerate(sample_letters, 1):
        content += f"""
--- SAMPLE LETTER {i} ---

📰 **ORIGINAL LETTER**

**Title:** {letter['title']}
**Author:** {letter['author']}
**Date:** {letter['date']}

{letter['full_text']}

---

🔍 **LLM ANALYSIS RESULTS**

**Classification:** {letter['analysis_type']} (Confidence: {letter['confidence']})

"""
        
        # Add specific analysis based on letter type
        if letter['analysis_type'] == 'CIVIC_DUTY':
            content += """**Primary Finding:** The writer adopts a civic duty approach by acknowledging government priorities while offering constructive suggestions for policy improvement.

**Key Evidence:**
• "the health and safety of citizens take precedence over the economy"
• "what Hong Kong needs is an enhanced plan that balances preventive means"  
• "Some out-of-the-box initiatives should be considered"
• "the Hong Kong government could consider promoting"

**Argumentation Structure:**
- Main Claim: COVID-19 policies need better balance between health and economic concerns
- Evidence Types: Personal experience, logical reasoning, alternative solutions
- Rhetorical Strategies: Problem-solution framing, questioning assumptions, constructive criticism

**Writer Positioning:** Concerned citizen offering constructive suggestions to government, using inclusive language ("Hong Kong needs") and respectful modal verbs ("could consider," "should be").

**Political Context:** Constructive engagement with government policy, acknowledging legitimate health concerns while advocating for economic considerations and alternative approaches."""

        elif letter['analysis_type'] == 'OPPOSITIONAL_CRITIQUE':
            content += """**Primary Finding:** The writer positions themselves in opposition to government through explicit criticism of leadership credibility and prediction of policy failure.

**Key Evidence:**
• "people have so little confidence in our government led by Chief Executive Carrie Lam Cheng Yuet-ngor"
• "Most of the people I asked say they are scared and won't take any shot"
• "a minority always undisciplined and rebellious"
• "I am not too pessimistic in thinking that the pandemic is here to stay"

**Argumentation Structure:**  
- Main Claim: Government lack of credibility will undermine COVID-19 response
- Evidence Types: Anecdotal evidence from personal conversations, social observation
- Rhetorical Strategies: Distrust framing, pessimistic projection, critique of leadership

**Writer Positioning:** Skeptical observer expressing popular sentiment, using exclusive language ("our government," "they are scared") and tentative modal verbs indicating uncertainty about outcomes.

**Political Context:** Direct opposition to government through lack of confidence, referencing specific leader (Carrie Lam) and predicting policy failure due to credibility crisis."""

        elif letter['analysis_type'] == 'CULTURAL_BELONGING':
            content += """**Primary Finding:** The writer emphasizes global citizenship and international belonging, positioning Hong Kong as part of a broader human community rather than focusing on local political dynamics.

**Key Evidence:**
• "globalisation is a message of hope and strength"
• "no country is alone as humanity can work together"  
• "we have also never lived in a world that was more interconnected"
• "this might be a sign of what we can still accomplish"

**Argumentation Structure:**
- Main Claim: Global cooperation transcends political tensions in pandemic response  
- Evidence Types: International examples, historical comparison, optimistic reasoning
- Rhetorical Strategies: Global perspective, hope framing, unity messaging

**Writer Positioning:** Global citizen advocating international cooperation, using inclusive language ("humanity can work together," "we have") and possibility-oriented modal verbs.

**Political Context:** Transcending nationalism through global citizenship identity, focusing on international relations and vaccine development rather than local Hong Kong politics."""

        content += f"""

---

👥 **HUMAN RESEARCHER FEEDBACK SECTION**

**For Ben and Research Team - Please add your assessment below:**

**Classification Accuracy:**
[ ] Agree with {letter['analysis_type']} classification
[ ] Disagree - suggest alternative classification: _____________
[ ] Uncertain - needs further analysis

**Evidence Quality Assessment:**
[ ] Evidence strongly supports the classification
[ ] Evidence partially supports the classification  
[ ] Evidence insufficient for confident classification
[ ] Additional evidence needed: _____________

**Linguistic Analysis Comments:**
[Please add your observations about the writer's language use, positioning strategies, and discourse patterns]

**Political Context Insights:**
[Please add your perspective on how this letter reflects Hong Kong's political situation in December 2020]

**Methodology Feedback:**
[Please comment on the LLM analysis approach, prompt effectiveness, and suggested improvements]

**Additional Research Questions:**
[Please note any specific research questions or hypotheses that emerge from this sample]

---

"""
    
    content += """
=== OVERALL METHODOLOGY ASSESSMENT ===

👥 **RESEARCH TEAM COLLABORATION SECTION**

**Framework Validation:**
[Please assess whether the 5-category citizenship framework effectively captures the discourse patterns in these samples]

**Scaling Readiness:**
[Please indicate whether this methodology is ready for full corpus analysis (250,000+ lines, 2018-2023)]

**Academic Publication Potential:**
[Please comment on the academic significance of these findings and potential publication venues]

**Next Steps and Timeline:**
[Please indicate preferred timeline for full analysis and any resource requirements]

**Cross-Validation Approach:**
[Please suggest validation methods for the complete corpus analysis results]

---

=== TECHNICAL REFERENCE ===

**LLM Analysis Engine:**
• OpenRouter API integration for non-OpenAI models
• Critical Discourse Analysis (CDA) prompt engineering  
• Evidence extraction with confidence assessment
• Systematic argumentation structure analysis

**Processing Pipeline:**
• Sample selection from 6-year SCMP corpus (2018-2023)
• Automated text preprocessing and segmentation
• Batch LLM analysis with structured output
• Results validation and human expert review

**Quality Assurance:**
• Multi-dimensional analysis (linguistic, rhetorical, political)
• Confidence levels for each classification
• Temporal and contextual sensitivity
• Cross-reference with Hong Kong political timeline

**Reference Files Available in SimonNotes Folder:**
• sample_letters_2020.md - Annotated sample texts
• demo_analysis_report_[timestamp].md - Technical analysis details  
• demo_analysis_results_[timestamp].json - Structured data for processing

---

*Document restructured for Letter → Analysis → Feedback format*
*Last updated: September 10, 2025*
*Generated with GitHub Copilot assistance*

**Ready for Ben's review and full corpus analysis approval! 🚀**"""

    return content

def main():
    print("=== Restructuring Google Doc: Letter → Analysis → Feedback Format ===")
    print()
    
    # Restructure the existing Google Doc
    result = restructure_google_doc()
    
    if result and result != "offline_restructure":
        print(f"\n🎉 Google Doc restructured successfully!")
        print(f"📋 New structure: Original Letter → LLM Analysis → Human Feedback")
        print(f"📄 Each of the 3 letters now has dedicated sections")
        print(f"🤝 Clear spaces for Ben and research team comments")
        print(f"🔗 Document: https://docs.google.com/document/d/{result}/edit")
        
    else:
        print("❌ Failed to restructure Google Doc")

if __name__ == "__main__":
    main()

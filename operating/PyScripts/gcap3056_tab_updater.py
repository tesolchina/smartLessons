#!/usr/bin/env python3
"""
GCAP3056 Google Doc Tab Updater

Purpose:
  Update an EXISTING Google Doc (with real tabs already created manually) by
  inserting formatted content (no raw markdown like # or *) into specific tabs
  and sub-tabs matched by their titles.

Features:
  • Fetch document with includeTabsContent=True
  • Build a mapping: tab title -> tabId (recursive traversal including child tabs)
  • Match target tabs case-insensitively (emoji and surrounding spaces tolerated)
  • Insert structured content segments with Google Docs paragraph styles
  • Avoid creating a new document
  • Safe: skips tabs that are not found; never deletes existing content unless
    --clear flag supplied (clears only target tab body content)

Usage (examples):
  python3 gcap3056_tab_updater.py \
      --doc 1polOm2WKjwlAGe_YGsffkIJ2a1mGXDMm0IFoKb7ZNoA \
      --tabs "📋 TAB 1: Team Membership & Admin" "💡 SUB-TAB 2.3: Brainstorming & Solutions"

  python3 gcap3056_tab_updater.py --doc <ID> --all  # update all known sections

Add --clear to wipe existing content inside selected tabs before inserting new content.

Extending:
  Edit the CONTENT_DEFINITIONS dict below to adjust or add tab content.
"""

from __future__ import annotations
import sys
import os
import argparse
import unicodedata
from typing import Dict, List, Tuple, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'GoogleDocsAPI'))
from auth_setup import authenticate_google_apis  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

# --------------------------------------------------------------------------------------
# Content model
# Each tab's content is a list of (style, text) segments.
# style: HEADING_1, HEADING_2, NORMAL_TEXT, BULLETED (converted to list), or BLANK
# --------------------------------------------------------------------------------------

ContentSegment = Tuple[str, str]

CONTENT_DEFINITIONS: Dict[str, List[ContentSegment]] = {
    # Keys must match (case-insensitive) the actual tab titles in the document.
    "MEMBERSHIP AND ADMIN": [
        ("HEADING_1", "Team Membership Overview"),
        ("NORMAL_TEXT", "Fill in accurate information for each member. Avoid duplicates. Tables below will auto-convert for structured tracking."),
        ("HEADING_2", "Members"),
        ("NORMAL_TEXT", "Complete roster (add/remove rows as needed)."),
        ("HEADING_2", "Communication Plan"),
        ("NORMAL_TEXT", "Clarify primary + backup channels and expected response windows."),
        ("HEADING_2", "Availability Schedule"),
        ("NORMAL_TEXT", "Weekly availability for scheduling synchronisation."),
        ("HEADING_2", "Role Assignments"),
        ("NORMAL_TEXT", "Assign primaries & backups; update when roles shift."),
        ("HEADING_2", "Risk Log"),
        ("NORMAL_TEXT", "Track emerging risks early; keep mitigation owners clear."),
        ("HEADING_2", "Decision Log"),
        ("NORMAL_TEXT", "Record high-impact decisions with rationale for transparency."),
        ("HEADING_2", "Roles & Responsibilities"),
        ("BULLETED", "Project Lead – overall coordination"),
        ("BULLETED", "Research Lead – sources & evidence integrity"),
        ("BULLETED", "Writing Lead – narrative + clarity"),
        ("BULLETED", "Engagement Lead – government & public outreach"),
        ("BULLETED", "Data/Visual Lead – infographic & presentation"),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Use this area to update roster changes, availability, risk notes."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Write any admin or support requests here (date + concise message)."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: leave confirmations, decisions, action flags.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI assistant may suggest workload balance, missing roles, or communication risks.)"),
    ],
    "ARGUMENTATIVE RESEARCH PAPER": [
        ("HEADING_1", "Argumentative Research Paper – Draft Workspace"),
        ("HEADING_2", "Working Thesis"),
        ("NORMAL_TEXT", "State the current thesis in one clear sentence. Revise as evidence evolves."),
        ("HEADING_2", "Research Questions"),
        ("BULLETED", "Primary question:"),
        ("BULLETED", "Secondary question 1:"),
        ("BULLETED", "Secondary question 2:"),
        ("HEADING_2", "Evidence Log (summaries only)"),
        ("NORMAL_TEXT", "List sources with 1–line relevance notes. Full details live in collection tabs."),
        ("HEADING_2", "Counterarguments / Rebuttals"),
        ("BULLETED", "Counterargument:"),
        ("BULLETED", "Rebuttal:"),
        ("HEADING_2", "Outline (living)"),
        ("BULLETED", "Intro – context & hook"),
        ("BULLETED", "Background – key definitions"),
        ("BULLETED", "Body Section 1 – claim + evidence"),
        ("BULLETED", "Body Section 2 – claim + evidence"),
        ("BULLETED", "Body Section 3 – counterargument + rebuttal"),
        ("BULLETED", "Conclusion – synthesis + call to action"),
        ("HEADING_2", "Draft Progress Log"),
        ("NORMAL_TEXT", "Date – What improved – Remaining gaps"),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Add current paragraph drafts or targeted rewrite tasks."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Clarify uncertainties about argument strength or structure."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: prioritize thesis focus, coherence, evidence sufficiency.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may flag weak logic, unsupported claims, or structural redundancy.)"),
    ],
    "COLLECTING PUBLICLY AVAILABLE INFO": [
        ("HEADING_1", "Public Sources – Collection Workspace"),
        ("HEADING_2", "Search Strategy"),
        ("BULLETED", "Keywords used:"),
        ("BULLETED", "Platforms (news, NGO, academic):"),
        ("BULLETED", "Date range:"),
        ("HEADING_2", "Source Inventory"),
        ("NORMAL_TEXT", "Format: Source / Type (news, report, dataset) / Date / Reliability note"),
        ("HEADING_2", "Key Extracted Data"),
        ("NORMAL_TEXT", "Summaries only. Avoid pasting long passages."),
        ("HEADING_2", "Gaps / Next Search Iteration"),
        ("NORMAL_TEXT", "List missing perspectives or statistics."),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Add new sources with date + credibility rating."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Flag access barriers or source reliability concerns."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: suggest refinement of search scope or verification.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may propose new search queries or triangulation steps.)"),
    ],
    "REQUEST INFO FROM THE GOV": [
        ("HEADING_1", "Government Information Requests – Code on Access"),
        ("HEADING_2", "Request Log"),
        ("NORMAL_TEXT", "Format: Date / Department / Info Requested / Basis / Status / Next Action"),
        ("HEADING_2", "Draft Request Templates"),
        ("NORMAL_TEXT", "Maintain polite, specific, justified wording."),
        ("HEADING_2", "Response Tracking"),
        ("BULLETED", "Pending (sent, awaiting acknowledgment)"),
        ("BULLETED", "Clarification requested"),
        ("BULLETED", "Fulfilled"),
        ("BULLETED", "Refused (record reason + appeal option)"),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Paste drafted request text for review."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Ask about scope narrowing, wording, or escalation."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: suggest precision, legal framing, tone.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may propose clarifying phrasing or structural tightening.)"),
    ],
    "CRTICAL REVIEW OF EXISTING SOLUTIONS": [
        ("HEADING_1", "Critical Review & Idea Generation"),
        ("NORMAL_TEXT", "Use this structured space to evaluate existing solutions and evolve innovations."),
        ("HEADING_2", "Evaluation Dimensions"),
        ("BULLETED", "Feasibility (1–10)"),
        ("BULLETED", "Impact (1–10)"),
        ("BULLETED", "Cost / Resource Intensity"),
        ("BULLETED", "Stakeholder Acceptance"),
        ("BULLETED", "Alignment with Evidence"),
        ("HEADING_2", "Existing Solutions Assessed"),
        ("NORMAL_TEXT", "List: Solution / Strength / Weakness / Opportunity"),
        ("HEADING_2", "Shortlisted New Ideas"),
        ("NORMAL_TEXT", "Top 2–3 with concise justification."),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Expand comparative notes, rationale, metrics."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Clarify evaluation criteria or ranking disputes."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: highlight missing risk analysis or evidence gaps.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may suggest alternative framing or hybrid solutions.)"),
    ],
    "RECOMMENDATIONS": [
        ("HEADING_1", "Recommendations Development"),
        ("HEADING_2", "Decision Criteria"),
        ("BULLETED", "Effectiveness"),
        ("BULLETED", "Equity"),
        ("BULLETED", "Sustainability"),
        ("BULLETED", "Practicality"),
        ("BULLETED", "Political viability"),
        ("HEADING_2", "Option Comparison"),
        ("NORMAL_TEXT", "Format: Option / Score summary / Key trade-off"),
        ("HEADING_2", "Final Recommendation Statement"),
        ("NORMAL_TEXT", "One paragraph persuasive justification."),
        ("HEADING_2", "Implementation Outline"),
        ("BULLETED", "Phase 1 – Setup"),
        ("BULLETED", "Phase 2 – Pilot"),
        ("BULLETED", "Phase 3 – Scale"),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Draft evolving recommendation text here."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Questions about feasibility or scope."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: challenge unsupported assumptions.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may flag unclear metrics or missing risk mitigation.)"),
    ],
    "SUBMIT TO LEGCO AND FURTHER ENGAGEMENT": [
        ("HEADING_1", "LegCo Submission & Engagement Tracking"),
        ("HEADING_2", "Submission Components"),
        ("BULLETED", "Cover letter"),
        ("BULLETED", "Executive summary"),
        ("BULLETED", "Evidence appendix"),
        ("BULLETED", "Supporting visuals"),
        ("HEADING_2", "Stakeholder Engagement Plan"),
        ("NORMAL_TEXT", "List targeted stakeholders + objective + method."),
        ("HEADING_2", "Follow-up Actions"),
        ("NORMAL_TEXT", "Track post-submission responses or meetings."),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Log outreach attempts (date + outcome)."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Escalation needs or strategic queries."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: advise on sequencing or targeting.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may suggest additional stakeholders or framing.)"),
    ],
    "REFLECTIVE LEARNING JOURNALS": [
        ("HEADING_1", "Reflective Journal Workspace"),
        ("HEADING_2", "Purpose"),
        ("NORMAL_TEXT", "Link experience → insight → adjustment. Stay evidence-based."),
        ("HEADING_2", "Weekly Reflection Template"),
        ("BULLETED", "What happened?"),
        ("BULLETED", "Why significant?"),
        ("BULLETED", "What did I learn?"),
        ("BULLETED", "What will I change next?"),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Add dated entries below."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Clarify expectations or reflective depth."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: prompt deeper analysis or connections.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may suggest reflective prompts or patterns seen.)"),
    ],
    "COMMUNITY ENGAGEMENT": [
        ("HEADING_1", "Community Engagement Progress"),
        ("HEADING_2", "Metrics"),
        ("BULLETED", "% Draft Complete"),
        ("BULLETED", "Government Replies Received"),
        ("BULLETED", "Public Pieces Published"),
        ("BULLETED", "Risks Identified / Mitigated"),
        ("HEADING_2", "Weekly Activity Log"),
        ("NORMAL_TEXT", "Format: Date – Action – Outcome – Next Step"),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Record outreach, publication progress, barriers."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Raise strategic or ethical concerns."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: guidance on prioritization or compliance.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may recommend timing or audience adjustments.)"),
    ],
    "WRITING FOR THE PUBLIC": [
        ("HEADING_1", "Public Writing Development"),
        ("HEADING_2", "Target Audience Definition"),
        ("NORMAL_TEXT", "Clarify demographics, knowledge level, motivations."),
        ("HEADING_2", "Outlet / Platform Candidates"),
        ("BULLETED", "News / Opinion"),
        ("BULLETED", "NGO blog"),
        ("BULLETED", "Community forum"),
        ("HEADING_2", "Angle & Framing Ideas"),
        ("BULLETED", "Problem framing"),
        ("BULLETED", "Human impact story"),
        ("BULLETED", "Policy urgency"),
        ("HEADING_2", "Draft Log"),
        ("NORMAL_TEXT", "Date – Piece – Status – Next revision focus"),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Insert paragraph drafts or pitch outlines."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Request review or suitability check."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: clarity, tone, audience fit.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may suggest simplification or engagement hooks.)"),
    ],
    "ENGAGE THE GOVERNMENT": [
        ("HEADING_1", "Government Engagement Tracking"),
        ("HEADING_2", "Target Agencies / Contacts"),
        ("NORMAL_TEXT", "Format: Agency / Contact / Relevance / Status"),
        ("HEADING_2", "Contact Log"),
        ("NORMAL_TEXT", "Date – Method – Outcome – Follow-up"),
        ("HEADING_2", "Meeting / Call Notes"),
        ("NORMAL_TEXT", "Summaries only. Action items bold in original doc later if needed."),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Plan next wave of outreach here."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Escalation, protocol questions."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: suggest sequencing or escalation thresholds.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may propose alternative contacts or phrasing.)"),
    ],
    "INFOGRAPHIC AND PRESENTATION": [
        ("HEADING_1", "Infographic & Presentation Workspace"),
        ("HEADING_2", "Core Message"),
        ("NORMAL_TEXT", "State the single take-away the audience must remember."),
        ("HEADING_2", "Data Sources (validated)"),
        ("BULLETED", "Source / Data Type / Reliability"),
        ("HEADING_2", "Visual Concepts"),
        ("BULLETED", "Chart / Purpose"),
        ("BULLETED", "Diagram / Purpose"),
        ("HEADING_2", "Slide / Panel Outline"),
        ("BULLETED", "Intro context"),
        ("BULLETED", "Problem scale"),
        ("BULLETED", "Current gaps"),
        ("BULLETED", "Proposed solution"),
        ("BULLETED", "Impact projection"),
        ("HEADING_2", "Design Task Board"),
        ("BULLETED", "Asset / Owner / Due"),
        ("HEADING_2", "Student Workspace"),
        ("NORMAL_TEXT", "Draft slide text or figure notes."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Ask about tone, complexity, or prioritization."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: comment on clarity or overload.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may suggest simplification or narrative flow tweaks.)"),
    ],
    # Per-member tabs
    "MEMBER 1": [
        ("HEADING_1", "Member 1 – Personal Contribution Log"),
        ("HEADING_2", "Weekly Contributions"),
        ("NORMAL_TEXT", "Date – Task – Outcome – Time spent"),
        ("HEADING_2", "Skill Development"),
        ("NORMAL_TEXT", "Track new tools, processes, or insights."),
        ("HEADING_2", "Reflection"),
        ("NORMAL_TEXT", "Brief note on challenges + next improvement focus."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Support needed or blockers."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: milestone alignment, encouragement.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may propose productivity or learning suggestions.)"),
    ],
    "MEMBER 2": [
        ("HEADING_1", "Member 2 – Personal Contribution Log"),
        ("HEADING_2", "Weekly Contributions"),
        ("NORMAL_TEXT", "Date – Task – Outcome – Time spent"),
        ("HEADING_2", "Skill Development"),
        ("NORMAL_TEXT", "Track new tools, processes, or insights."),
        ("HEADING_2", "Reflection"),
        ("NORMAL_TEXT", "Brief note on challenges + next improvement focus."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Support needed or blockers."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: milestone alignment, encouragement.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may propose productivity or learning suggestions.)"),
    ],
    "MEMBER 3": [
        ("HEADING_1", "Member 3 – Personal Contribution Log"),
        ("HEADING_2", "Weekly Contributions"),
        ("NORMAL_TEXT", "Date – Task – Outcome – Time spent"),
        ("HEADING_2", "Skill Development"),
        ("NORMAL_TEXT", "Track new tools, processes, or insights."),
        ("HEADING_2", "Reflection"),
        ("NORMAL_TEXT", "Brief note on challenges + next improvement focus."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Support needed or blockers."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: milestone alignment, encouragement.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may propose productivity or learning suggestions.)"),
    ],
    "MEMBER 4": [
        ("HEADING_1", "Member 4 – Personal Contribution Log"),
        ("HEADING_2", "Weekly Contributions"),
        ("NORMAL_TEXT", "Date – Task – Outcome – Time spent"),
        ("HEADING_2", "Skill Development"),
        ("NORMAL_TEXT", "Track new tools, processes, or insights."),
        ("HEADING_2", "Reflection"),
        ("NORMAL_TEXT", "Brief note on challenges + next improvement focus."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Support needed or blockers."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: milestone alignment, encouragement.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may propose productivity or learning suggestions.)"),
    ],
    "MEMBER 5": [
        ("HEADING_1", "Member 5 – Personal Contribution Log"),
        ("HEADING_2", "Weekly Contributions"),
        ("NORMAL_TEXT", "Date – Task – Outcome – Time spent"),
        ("HEADING_2", "Skill Development"),
        ("NORMAL_TEXT", "Track new tools, processes, or insights."),
        ("HEADING_2", "Reflection"),
        ("NORMAL_TEXT", "Brief note on challenges + next improvement focus."),
        ("HEADING_2", "Messages to Instructor"),
        ("NORMAL_TEXT", "Support needed or blockers."),
        ("HEADING_2", "Instructor Feedback"),
        ("NORMAL_TEXT", "(Instructor: milestone alignment, encouragement.)"),
        ("HEADING_2", "AI Support Comments"),
        ("NORMAL_TEXT", "(AI may propose productivity or learning suggestions.)"),
    ],
}

# --------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------

def normalize(title: str) -> str:
    # Lowercase, strip, remove some variation selectors / extra spaces
    nf = unicodedata.normalize('NFKC', title or "")
    return ''.join(ch for ch in nf.lower().strip() if unicodedata.category(ch) != 'Cf')


def convert_markdown_tables_for_single_tab(docs_service, document_id: str, norm_tab_title: str):
    """Detect markdown tables in a single tab and convert them to real tables.
    This mirrors logic of external converter but simplified & resilient.
    """
    def flatten(doc: dict) -> Dict[str, dict]:
        m: Dict[str, dict] = {}
        def add(t: dict):
            props = t.get('tabProperties', {})
            title = props.get('title', '')
            if title:
                m[normalize(title)] = t
            for c in t.get('childTabs', []) or []:
                add(c)
        for t in doc.get('tabs', []) or []:
            add(t)
        return m

    def extract_lines(tab: dict):
        body = tab.get('documentTab', {}).get('body', {})
        out = []
        for elem in body.get('content', []) or []:
            para = elem.get('paragraph')
            if not para:
                continue
            text = ''.join(r.get('textRun', {}).get('content', '') for r in para.get('elements', []) if r.get('textRun'))
            if text.strip():
                out.append((text, elem))
        return out

    def detect(lines):
        blocks = []
        i = 0
        while i < len(lines)-1:
            header, h_elem = lines[i]
            sep, s_elem = lines[i+1]
            if '|' in header and '|' in sep and set(sep.replace('|','').strip()) <= {'-',' ',':'}:
                cols = [c.strip() for c in header.split('|') if c.strip()]
                if len(cols) >= 2:
                    j = i+2
                    rows = [cols]
                    while j < len(lines):
                        txt,_el = lines[j]
                        if '|' in txt:
                            rc = [c.strip() for c in txt.split('|') if c.strip()]
                            if len(rc)==len(cols):
                                rows.append(rc)
                                j+=1
                                continue
                        break
                    start = h_elem.get('startIndex')
                    end = lines[j-1][1].get('endIndex')
                    if start and end and end>start:
                        blocks.append({'start': start, 'end': end, 'rows': rows})
                    i = j
                    continue
            i+=1
        return blocks

    processed_total = 0
    while True:
        doc = docs_service.documents().get(documentId=document_id, includeTabsContent=True).execute()
        tab_map = flatten(doc)
        tab = tab_map.get(norm_tab_title)
        if not tab:
            break
        tab_id = tab.get('tabProperties', {}).get('tabId')
        if not tab_id:
            break
        lines = extract_lines(tab)
        blocks = detect(lines)
        if not blocks:
            break
        # Always process only first detected block to keep indices valid
        blk = blocks[0]
        start = blk['start']
        end = blk['end']
        if not (start and end and end > start):
            break
        rows = blk['rows']
        cols = len(rows[0])
        # Delete markdown block
        try:
            docs_service.documents().batchUpdate(documentId=document_id, body={'requests':[{
                'deleteContentRange': {'range': {'tabId': tab_id,'startIndex': start,'endIndex': end-1}}
            }]}).execute()
        except Exception:
            break
        # Insert table at same start
        try:
            docs_service.documents().batchUpdate(documentId=document_id, body={'requests':[{
                'insertTable': {'rows': len(rows),'columns': cols,'location': {'tabId': tab_id,'index': start}}
            }]}).execute()
        except Exception:
            break
        # Populate
        doc = docs_service.documents().get(documentId=document_id, includeTabsContent=True).execute()
        tab = flatten(doc).get(norm_tab_title)
        if not tab:
            break
        table_elem = None
        for elem in tab.get('documentTab',{}).get('body',{}).get('content',[]) or []:
            if 'table' in elem and elem.get('startIndex',0) >= start:
                table_elem = elem
                break
        if not table_elem:
            break
        table = table_elem.get('table', {})
        cell_reqs: List[dict] = []
        for r_i, row in enumerate(table.get('tableRows', [])[:len(rows)]):
            for c_i, cell in enumerate(row.get('tableCells', [])[:cols]):
                text = rows[r_i][c_i]
                if not text:
                    continue
                cell_content = cell.get('content', [])
                if not cell_content:
                    continue
                p_start = cell_content[0].get('startIndex')
                if p_start is None:
                    continue
                insert_at = p_start + 1
                cell_reqs.append({'insertText': {'location': {'tabId': tab_id,'index': insert_at},'text': text}})
                if r_i == 0:
                    cell_reqs.append({'updateTextStyle': {'range': {'tabId': tab_id,'startIndex': insert_at,'endIndex': insert_at+len(text)},'textStyle': {'bold': True},'fields': 'bold'}})
        for i in range(0, len(cell_reqs), 90):
            try:
                docs_service.documents().batchUpdate(documentId=document_id, body={'requests': cell_reqs[i:i+90]}).execute()
            except Exception:
                break
        processed_total += 1
    if processed_total:
        print(f"   ↳ Converted {processed_total} markdown table block(s) to real tables")


def flatten_tabs(doc: dict) -> Dict[str, dict]:
    """Create mapping of normalized title -> tab object (includes child tabs)."""
    mapping: Dict[str, dict] = {}

    def add(tab: dict):
        props = tab.get('tabProperties', {})
        title = props.get('title', '')
        if title:
            mapping[normalize(title)] = tab
        for child in tab.get('childTabs', []) or []:
            add(child)

    for t in doc.get('tabs', []) or []:
        add(t)
    return mapping


def compute_tab_end_index(tab: dict) -> int:
    doc_tab = tab.get('documentTab', {})
    body = doc_tab.get('body', {})
    content = body.get('content', []) or []
    # Last structural element endIndex typically gives insertion point
    if not content:
        return 1  # body starts at index 1
    last = content[-1]
    return last.get('endIndex', 1)


def build_requests_for_segments(tab_id: str, start_index: int, segments: List[ContentSegment], include_toc: bool = True) -> List[dict]:
    requests: List[dict] = []
    # Ensure a valid starting insertion point (minimum 1)
    cursor = max(1, start_index)
    if include_toc:
        # Build a simple text-based TOC placeholder (real dynamic TOC unsupported with current field)
        toc_header = "TABLE OF CONTENTS (auto-outline)\n"
        requests.append({
            'insertText': {
                'location': {'tabId': tab_id, 'index': cursor},
                'text': toc_header
            }
        })
        cursor += len(toc_header)
    # Icon mapping for nicer visual layout
    ICONS = {
        'student workspace': '🧑\u200d🎓 ',
        'messages to instructor': '📨 ',
        'instructor feedback': '🧑\u200d🏫 ',
        'ai support comments': '🤖 ',
        'working thesis': '🎯 ',
        'research questions': '❓ ',
        'evidence log (summaries only)': '📚 ',
        'counterarguments / rebuttals': '⚖️ ',
        'outline (living)': '🗂️ ',
        'draft progress log': '🕒 ',
        'evaluation dimensions': '🧪 ',
        'existing solutions assessed': '📊 ',
        'shortlisted new ideas': '💡 ',
        'option comparison': '📈 ',
        'final recommendation statement': '✅ ',
        'implementation outline': '🛠️ ',
        'submission components': '🗂️ ',
        'stakeholder engagement plan': '👥 ',
        'follow-up actions': '🔁 ',
        'weekly reflection template': '🪞 ',
        'metrics': '📏 ',
        'weekly activity log': '🗓️ ',
        'target audience definition': '🎯 ',
        'outlet / platform candidates': '📰 ',
        'angle & framing ideas': '🧭 ',
        'draft log': '✍️ ',
        'target agencies / contacts': '🏛️ ',
        'contact log': '📞 ',
        'meeting / call notes': '📝 ',
        'core message': '💬 ',
        'data sources (validated)': '📂 ',
        'visual concepts': '🖼️ ',
        'slide / panel outline': '📑 ',
        'design task board': '🗃️ ',
        'weekly contributions': '📅 ',
        'skill development': '🧠 ',
        'reflection': '🔍 ',
    }

    def embellish(text: str, style_type: Optional[str]) -> str:
        if style_type and style_type.startswith('HEADING_'):
            low = text.lower().strip()
            if not any(text.startswith(prefix) for prefix in ICONS.values()):
                icon = ICONS.get(low)
                if icon:
                    return icon + text
        return text

    BOX_HEADINGS = {
        'student workspace', 'messages to instructor', 'instructor feedback', 'ai support comments'
    }

    # Markdown table templates: heading (lower-case) -> (header columns, row_count, placeholder token)
    MARKDOWN_TABLE_TEMPLATES: Dict[str, tuple] = {
        'source inventory': (['Source','Type','Date','Reliability','Key Note'], 4, '...'),
        'request log': (['Date','Department','Info Requested','Status','Next Action'], 4, '...'),
        'existing solutions assessed': (['Solution','Strength','Weakness','Opportunity'], 4, '...'),
        'shortlisted new ideas': (['Idea','Rationale','Score'], 3, '...'),
        'option comparison': (['Option','Score Summary','Trade-off'], 5, '...'),
        'weekly activity log': (['Date','Action','Outcome','Next Step'], 6, '...'),
        'draft log': (['Date','Piece','Status','Revision Focus'], 5, '...'),
        'contact log': (['Date','Method','Outcome','Follow-up'], 6, '...'),
        'design task board': (['Asset','Owner','Due','Status'], 6, '...'),
        'weekly contributions': (['Date','Task','Outcome','Time'], 6, '...'),
        'evidence log (summaries only)': (['Source','Relevance','Note'], 6, '...'),
        'metrics': (['Metric','Current','Target','Notes'], 6, '...'),
        'submission components': (['Component','Status','Owner','Notes'], 6, '...'),
    'members': (['Name','Student ID','HKBU Email','Alt Email (Gmail)','Preferred Role','Strengths / Notes'], 10, ''),
    'communication plan': (['Channel','Purpose','Frequency','Expected Response Time','Owner','Notes'], 6, ''),
    'availability schedule': (['Member','Weekday / Period','Available Slots','Timezone','Constraints','Notes'], 8, ''),
    'role assignments': (['Role','Primary Member','Backup','Start Date','Status','Notes'], 6, ''),
    'risk log': (['Risk','Likelihood','Impact','Mitigation','Owner','Status'], 6, ''),
    'decision log': (['Date','Decision','Rationale','Owner','Follow-up','Status'], 8, ''),
        'student workspace': (['Student Notes'], 6, ' '),
        'messages to instructor': (['Message','Date'], 5, ' '),
        'instructor feedback': (['Feedback','Date'], 5, ' '),
        'ai support comments': (['AI Suggestion','Date'], 5, ' '),
    }

    seen_heading = False

    for style, text in segments:
        if style == 'HR':
            divider = "────────────────────────────────────────\n"
            requests.append({
                'insertText': {
                    'location': {'tabId': tab_id, 'index': cursor},
                    'text': divider
                }
            })
            cursor += len(divider)
            continue
        if style == 'BLANK':
            insert_text = "\n"
            style_type = None
        elif style == 'BULLETED':
            # Insert paragraph then apply bullet later
            clean = text.strip()
            if not clean:
                continue
            insert_text = clean + "\n"
            style_type = 'BULLETED'
        else:
            # embellish heading text with icons
            style_type = style
            adjusted = embellish(text.strip(), style_type)
            insert_text = adjusted + ("\n\n" if style_type.startswith('HEADING_') else "\n")

        # Automatically insert a horizontal rule before secondary headings (HEADING_2) except the first heading encountered
        if style_type and style_type.startswith('HEADING_'):
            if seen_heading and style_type == 'HEADING_2':
                divider = "────────────────────────────────────────\n"
                requests.append({
                    'insertText': {
                        'location': {'tabId': tab_id, 'index': cursor},
                        'text': divider
                    }
                })
                cursor += len(divider)
            seen_heading = True

        requests.append({
            'insertText': {
                'location': {
                    'tabId': tab_id,
                    'index': cursor
                },
                'text': insert_text
            }
        })
        # After insertion, we can style range using length of inserted text
        length = len(insert_text)
        if style_type and style_type.startswith('HEADING_'):
            requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'tabId': tab_id,
                        'startIndex': cursor,
                        'endIndex': cursor + length
                    },
                    'paragraphStyle': {
                        'namedStyleType': style_type
                    },
                    'fields': 'namedStyleType'
                }
            })
        elif style_type == 'BULLETED':
            requests.append({
                'createParagraphBullets': {
                    'range': {
                        'tabId': tab_id,
                        'startIndex': cursor,
                        'endIndex': cursor + length
                    },
                    'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                }
            })
        cursor += length

        # Add ASCII box placeholder after certain headings
        if style_type and style_type.startswith('HEADING_'):
            core = text.lower().strip()
            # Minimal placeholder area for feedback/comment sections
            # Insert markdown tables for both workspace and data sections
            if core in MARKDOWN_TABLE_TEMPLATES:
                headers, rows, placeholder = MARKDOWN_TABLE_TEMPLATES[core]
                header_line = ' | '.join(headers) + '\n'
                sep_line = ' | '.join(['---']*len(headers)) + '\n'
                body_lines = ''
                for _ in range(rows):
                    body_lines += ' | '.join([placeholder]*len(headers)) + '\n'
                table_md = header_line + sep_line + body_lines + '\n'
                requests.append({
                    'insertText': {
                        'location': {'tabId': tab_id, 'index': cursor},
                        'text': table_md
                    }
                })
                cursor += len(table_md)
                # Add visual divider and spacing after each table for clarity
                spacer = '────────────────────────────────────────\n\n'
                requests.append({
                    'insertText': {
                        'location': {'tabId': tab_id, 'index': cursor},
                        'text': spacer
                    }
                })
                cursor += len(spacer)
    return requests


def clear_tab_content(tab: dict, tab_id: str) -> List[dict]:
    doc_tab = tab.get('documentTab', {})
    body = doc_tab.get('body', {})
    content = body.get('content', []) or []
    if not content:
        return []
    # Determine safe deletion span
    first = content[0]
    last = content[-1]
    start = first.get('startIndex', 1)
    end = last.get('endIndex', start)
    # If almost empty or invalid span, skip
    if end - start <= 1:
        return []
    return [{
        'deleteContentRange': {
            'range': {
                'tabId': tab_id,
                'startIndex': start,
                'endIndex': end - 1  # keep trailing newline anchor
            }
        }
    }]


def update_tabs(document_id: str, target_titles: List[str], clear: bool = False, convert_tables: bool = True):
    creds = authenticate_google_apis()
    if not creds:
        print("❌ Authentication failed (no credentials).")
        return 1
    docs = build('docs', 'v1', credentials=creds)
    try:
        doc = docs.documents().get(documentId=document_id, includeTabsContent=True).execute()
    except HttpError as e:
        print(f"❌ Failed to fetch document: {e}")
        return 1

    tab_map = flatten_tabs(doc)
    print(f"📑 Found {len(tab_map)} tabs (including sub-tabs).")
    # Debug: list discovered titles
    print("Discovered tab titles:")
    for raw_norm, tab in tab_map.items():
        title = tab.get('tabProperties', {}).get('title', '')
        print(f"  - {title}")

    # Build normalized target list
    wanted_norm = {normalize(t): t for t in (target_titles or [])}
    if not target_titles:
        # If none specified, use all that we have definitions for
        wanted_norm = {normalize(k): k for k in CONTENT_DEFINITIONS.keys()}

    processed = 0
    for norm_title, original_title in wanted_norm.items():
        tab = tab_map.get(norm_title)
        if not tab:
            print(f"⚠️  Tab not found (skip): {original_title}")
            continue
        tab_id = tab.get('tabProperties', {}).get('tabId')
        if not tab_id:
            print(f"⚠️  Missing tabId for: {original_title}")
            continue
        segments = CONTENT_DEFINITIONS.get(original_title.upper()) or CONTENT_DEFINITIONS.get(original_title) or []
        if not segments:
            print(f"⚠️  No content definition for: {original_title} (skip)")
            continue
        print(f"🛠️  Updating tab: {original_title}")
        # Phase 1: clear if requested
        if clear:
            del_reqs = clear_tab_content(tab, tab_id)
            if del_reqs:
                try:
                    docs.documents().batchUpdate(documentId=document_id, body={'requests': del_reqs}).execute()
                except HttpError as e:
                    print(f"❌ Clear failed for {original_title}: {e}")
                    continue
        # Fetch fresh tab content if cleared to recompute end index
        if clear:
            try:
                doc_refreshed = docs.documents().get(documentId=document_id, includeTabsContent=True).execute()
                # Recompute tab reference
                refreshed_map = flatten_tabs(doc_refreshed)
                tab = refreshed_map.get(norm_title, tab)
            except Exception:
                pass
        end_index = compute_tab_end_index(tab) if not clear else 1
        insert_reqs = build_requests_for_segments(tab_id, end_index, segments, include_toc=True if clear else False)
        # Execute insertion (chunked)
        insertion_failed = False
        for i in range(0, len(insert_reqs), 95):
            chunk = insert_reqs[i:i+95]
            try:
                docs.documents().batchUpdate(documentId=document_id, body={'requests': chunk}).execute()
            except HttpError as e:
                print(f"❌ Insert failed for {original_title} (chunk {i}): {e}")
                insertion_failed = True
                break
        if insertion_failed:
            continue

        # After insertion, optionally convert markdown tables
        if convert_tables:
            try:
                convert_markdown_tables_for_single_tab(docs, document_id, norm_title)
            except Exception as conv_e:
                print(f"⚠️  Table auto-conversion skipped for {original_title}: {conv_e}")
        else:
            print(f"   ↳ Skipped auto-conversion (leaving markdown tables as-is) for {original_title}")
        processed += 1
    if processed:
        print(f"✅ Updated {processed} tab(s).\nDocument: https://docs.google.com/document/d/{document_id}/edit")
    else:
        print("ℹ️  No tabs updated.")
    return 0


def parse_args():
    ap = argparse.ArgumentParser(description="Update content inside existing Google Doc tabs.")
    ap.add_argument('--doc', required=True, help='Document ID')
    ap.add_argument('--tabs', nargs='*', help='Explicit tab titles to update (default: all defined)')
    ap.add_argument('--clear', action='store_true', help='Clear existing tab content before inserting new content')
    ap.add_argument('--no-convert', action='store_true', help='Do not auto-convert markdown tables to real tables (leave raw markdown)')
    return ap.parse_args()


def main():
    args = parse_args()
    return update_tabs(args.doc, args.tabs or [], clear=args.clear, convert_tables=not args.no_convert)


if __name__ == '__main__':
    sys.exit(main())

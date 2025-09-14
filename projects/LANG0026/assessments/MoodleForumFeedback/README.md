# LANG0026 Moodle Forum Analysis
**Course:** LANG0026 - Language and Global Citizenship  
**Instructor:** Dr. WANG Simon H  
**Generated:** September 15, 2025

## 📁 Folder Structure

This directory contains analysis of two separate Moodle forum discussions with comprehensive student participation tracking and section-based reporting.

### 🎥 VideoTranscriptAnalysis/
**Forum Topic:** Student Video Transcript Submission and Analysis  
**Assignment Components:**
- Step 1: Raw Transcript (unedited video transcription)
- Step 2: Error Analysis (pronunciation, grammar, technical issues)
- Step 3: Self-Assessment (content, language, fluency analysis)

**Key Files:**
- `discussion-video-transcript.json` - Raw forum data
- `video_transcript_individual_reports.md` - Individual student analysis
- `comprehensive_overall_report.md` - Section-based statistics
- `nested_reply_analyzer.py` - Corrected analysis handling nested replies
- `complete_forum_transcript_report.md` - Full transcript content

### 📝 ReviseOutlineAnalysis/
**Forum Topic:** Essay Outline Revision with First Principle Thinking  
**Assignment Components:**
- Original Outline submission
- Revision Planning notes
- Revised Outline with improvements
- Self-Reflection on learning process

**Key Files:**
- `Revise-outline.json` - Raw forum data
- `revise_outline_individual_reports.md` - Individual student analysis
- `comprehensive_overall_report.md` - Section-based statistics

## 📊 Analysis Framework

### Student List Cross-Reference
- **Enrollment Data:** `../0036students.xls` (56 total students)
- **Section Organization:** Students grouped by sections 36, 37, 38
- **Participation Tracking:** Cross-reference forum participants with official enrollment

### Analysis Methodology
1. **Content Type Recognition:** Automated classification of forum post content
2. **Completion Tracking:** Component-by-component progress assessment  
3. **Section Breakdown:** Participation statistics by class section
4. **Quality Assessment:** Content coherence, language quality, fluency indicators

### Technical Implementation
- **Nested Reply Handling:** Corrected analysis capturing multi-post assignments
- **HTML Cleaning:** Proper text extraction from forum HTML content
- **Cross-Reference Validation:** Name matching between enrollment and forum data
- **Statistical Reporting:** Comprehensive participation and completion metrics

## 🔍 Key Findings

### Video Transcript Forum
- **Participants:** 21 students from forum posts
- **Complete Submissions:** 17 students (81.0% of participants)
- **Critical Discovery:** Nested reply structure required corrected analysis methodology

### Revise Outline Forum  
- **Participants:** 30 students from forum posts
- **Assignment Focus:** Internet benefits vs. risks essay outline development
- **Learning Method:** First principle thinking approach for deeper analysis

### Cross-Forum Analysis
- **Both Forums:** Students participating in both discussions
- **Section Gaps:** Identification of non-participating students by section
- **Enrollment Variance:** ~35 students with no forum participation across both assignments

## 🛠️ Analysis Tools

- `dual_forum_analyzer.py` - Comprehensive analysis system for both forums
- Individual analyzer scripts for specific forum analysis
- Section-based reporting with enrollment cross-reference
- HTML content cleaning and text processing
- Automated content type classification

## 📋 Usage Notes

1. **Data Sources:** JSON exports from Moodle forum, Excel enrollment data
2. **Report Generation:** Run `dual_forum_analyzer.py` for comprehensive analysis
3. **Nested Replies:** Use `nested_reply_analyzer.py` for video transcript forum specifically
4. **Updates:** Re-run analysis scripts when new forum data is available

---
**Technical Contact:** Analysis system documentation and methodology validation available in individual script headers.
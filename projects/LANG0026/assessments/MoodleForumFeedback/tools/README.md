# Analysis Tools for LANG0026 Forum Data
**Course:** LANG0026 - Language and Global Citizenship  
**Purpose:** Python analysis scripts for Moodle forum data processing

## 🛠️ Main Analysis Tools

### **dual_forum_analyzer.py**
**Primary comprehensive analysis system**
- **Purpose:** Analyzes both Video Transcript and Revise Outline forums simultaneously
- **Input:** `discussion-video-transcript.json`, `Revise-outline.json`, `0036students.csv`
- **Output:** Individual and overall reports for both forums with section breakdown
- **Features:** 
  - Cross-reference with student enrollment data
  - Section-based participation analysis
  - Content type classification for both forum types
  - Completion tracking and statistics
- **Usage:** `python3 dual_forum_analyzer.py`

### **csv_student_viewer.py**  
**Student enrollment data viewer**
- **Purpose:** View and analyze student enrollment CSV data
- **Input:** `0036students.csv`
- **Output:** Console display of enrollment statistics
- **Features:**
  - Student count by section
  - Program distribution analysis
  - Data quality check
  - Sample record display
- **Usage:** `python3 csv_student_viewer.py`

## 📝 Video Transcript Analysis Tools

### **nested_reply_analyzer.py**
**Corrected video transcript analysis**
- **Purpose:** Properly handles nested forum replies for video transcript assignments
- **Critical Fix:** Addresses nested reply structure where students post multi-step assignments
- **Input:** `discussion-video-transcript.json`
- **Components Analyzed:**
  - Step 1: Raw Transcript
  - Step 2: Error Analysis  
  - Step 3: Self-Assessment
- **Usage:** `python3 nested_reply_analyzer.py`

### **complete_forum_transcript_report.py**
**Full transcript content reporter**
- **Purpose:** Generates comprehensive report with ALL student forum replies
- **Output:** Complete transcript content for every post
- **Features:** Full text preservation, content type identification
- **Usage:** `python3 complete_forum_transcript_report.py`

### **transcript_analyzer.py**
**Original video transcript analyzer**
- **Purpose:** Initial analysis system (before nested reply correction)
- **Status:** Legacy - use `nested_reply_analyzer.py` instead
- **Note:** Kept for reference and comparison

### **enhanced_section_reporter.py**
**Section-based video transcript reporting**
- **Purpose:** Organize video transcript analysis by student sections
- **Input:** Video transcript data + student enrollment list
- **Output:** Section-organized reports with cross-reference validation
- **Usage:** `python3 enhanced_section_reporter.py`

### **section_organizer.py**
**Student list cross-reference tool**
- **Purpose:** Cross-reference forum participants with official enrollment
- **Features:** Identify missing students, section organization
- **Usage:** `python3 section_organizer.py`

## 🔧 Usage Instructions

### Quick Start
```bash
# For comprehensive analysis of both forums:
python3 tools/dual_forum_analyzer.py

# For video transcript specific analysis:
python3 tools/nested_reply_analyzer.py

# For student enrollment overview:
python3 tools/csv_student_viewer.py
```

### File Dependencies
All scripts expect to be run from the main MoodleForumFeedback directory:
```
MoodleForumFeedback/
├── discussion-video-transcript.json
├── Revise-outline.json  
├── ../0036students.csv
└── tools/ (Python scripts)
```

### Analysis Workflow
1. **Data Preparation:** Ensure JSON files and CSV student list are in place
2. **Primary Analysis:** Run `dual_forum_analyzer.py` for comprehensive reports
3. **Specific Analysis:** Use individual tools for focused analysis
4. **Results:** Check generated reports in analysis subfolders

## 📊 Technical Notes

### Content Type Classification
- **Video Transcript:** Raw Transcript, Error Analysis, Self-Assessment
- **Outline Revision:** Original Outline, Revision Planning, Revised Outline, Self-Reflection

### Cross-Reference Validation
- Student names matched between forum posts and enrollment data
- Section assignment validation and participation tracking
- Missing student identification for follow-up

### Data Processing
- HTML tag removal from forum content
- Nested reply aggregation for complete submissions
- Timestamp conversion and formatting
- Word count analysis and content length validation

---
**Maintenance:** Update file paths in scripts if directory structure changes  
**Contact:** Scripts documented for LANG0026 course analysis workflow
# LANG0026 Moodle Forum Feedback Analysis

## Project Overview

This project analyzes student video transcripts from the LANG0026 forum discussion to assess:
1. **Participation**: Whether students have submitted their transcripts
2. **Content Quality**: Coherence between the three required questions
3. **Language Assessment**: Vocabulary range, accuracy, and module-specific terminology
4. **Individual & Class Reports**: Detailed feedback for each student and overall class trends

## Data Source

**File**: `/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback/discussion-video-transcript.json`

**Structure Discovered**:
- JSON array containing 36 forum posts from Moodle export
- Includes instructor posts (Dr. WANG Simon H) and student responses
- Each post contains: user_id, full_name, subject, message (HTML), word_count, timestamps
- Student responses include transcripts, self-assessments, and template examples

## Analysis System Created

**Script**: `transcript_analyzer.py`

### Key Features:
- **Data Processing**: Extracts clean text from HTML, identifies templates vs. actual submissions
- **Transcript Detection**: Automatically identifies transcript sections in student responses
- **Content Analysis**: Evaluates coherence between identity, background, and global citizenship
- **Language Assessment**: Analyzes vocabulary diversity, module-specific terms, sentence complexity
- **Fluency Evaluation**: Based on self-reported issues and transcript characteristics

### Assessment Criteria:
1. **Content Coherence (1-5)**: Connection between the three questions
2. **Language Quality (1-5)**: Vocabulary range and module-specific terminology
3. **Fluency Indicators (1-5)**: Based on self-assessment and transcript quality

## Analysis Results (2025-09-15)

### Class Overview:
- **Total Students**: 31
- **Participation Rate**: 83.9% (26 students submitted transcripts)
- **Average Scores**:
  - Content Coherence: 3.3/5
  - Language Quality: 3.2/5  
  - Fluency: 2.8/5

### Key Findings:

#### Most Common Issues:
1. **Self-reported fluency issues** (50% of students)
2. **Self-reported pronunciation difficulties** (50% of students)
3. **Lack of clear connections between questions** (34.6% of students)
4. **Limited module-specific vocabulary** (19.2% of students)

#### Common Strengths:
1. **Complete question coverage** (73.1% addressed all three questions)
2. **Well-structured presentations** (61.5% used proper format)
3. **Positive delivery confidence** (61.5% self-assessed positively)
4. **Relevant terminology use** (50% incorporated appropriate terms)

#### Students Needing Support:
- **CAO Wing Yan**: Requires individual consultation
- **JIN Zijie**: Requires individual consultation

### Generated Reports:
1. **`individual_student_reports.md`**: Detailed analysis for each student
2. **`class_overview_report.md`**: Overall class trends and recommendations

## Recommendations for Instruction

### Immediate Actions:
1. **Fluency Support**: Provide pronunciation guides for key global citizenship terms
2. **Practice Opportunities**: Offer low-stakes speaking practice sessions
3. **Coherence Training**: Help students connect personal identity to global citizenship concepts

### Individual Support:
- Schedule consultations with students scoring below 2.5 average
- Focus on logical narrative development exercises
- Provide additional vocabulary development resources

## System Capabilities

The analysis system can:
- ✅ **Check Participation**: Identify who has/hasn't submitted transcripts
- ✅ **Content Evaluation**: Assess narrative coherence and question connections
- ✅ **Language Analysis**: Evaluate vocabulary range and academic terminology
- ✅ **Individual Reports**: Generate detailed feedback for each student
- ✅ **Class Overview**: Identify common issues and trends
- ✅ **Actionable Recommendations**: Provide specific improvement suggestions

## Technical Notes

- **LLM Integration Ready**: The system is designed to send processed transcripts to LLM for deeper analysis
- **Scalable**: Can handle multiple course sections and repeated assessments
- **Customizable**: Scoring criteria and assessment focus areas are easily adjustable
- **Export Friendly**: Generates markdown reports suitable for sharing with students and administration

## Next Steps for Future Use

1. **LLM Enhancement**: Send individual transcripts to language models for more detailed linguistic analysis
2. **Rubric Integration**: Align scoring with official course rubrics
3. **Longitudinal Tracking**: Compare student progress across multiple video assignments
4. **Automated Feedback**: Generate personalized learning recommendations for each student

---

**Last Updated**: 2025-09-15 05:21:00  
**Status**: Complete - Analysis system operational and reports generated

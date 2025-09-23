# Assessment Management Module

**Purpose**: Assessment design, grading workflows, and AI-assisted evaluation  
**Last Updated**: September 5, 2025

## 📊 Assessment Framework

### Assessment Types
1. **Formative Assessments** (Ongoing)
   - Weekly Moodle forum participation
   - In-class activity completion
   - Peer feedback exercises

2. **Summative Assessments** (Graded)
   - Module 1: Reading Skills Assessment (25%)
   - Module 2: Writing Skills Assessment (25%)  
   - Final Portfolio: Integrated Skills (50%)

## 🤖 AI-Assisted Grading System

### Grading Workflow
```
1. Student Submission → 
2. AI Initial Analysis → 
3. Human Review & Adjustment → 
4. Final Grade & Feedback → 
5. Student Delivery
```

### AI Grading Tools
- **Content Analysis**: Automated evaluation of argument structure
- **Language Assessment**: Grammar, vocabulary, and clarity analysis
- **Plagiarism Detection**: AI-powered originality checking
- **Rubric Application**: Consistent criteria application

### Grading Scripts
```python
# Example AI grading integration
from src.course_admin import AssessmentGrader

grader = AssessmentGrader()
results = grader.evaluate_submissions(
    folder_path="submissions/",
    rubric="module1_rubric.json",
    ai_assist=True
)
```

## 📋 Assessment Instructions

### Module 1: Academic Reading Skills
**Duration**: 90 minutes  
**Format**: Mixed (Multiple choice + Short essay)  

#### Instructions for Students
```markdown
## Module 1 Assessment: Academic Reading Skills

### Part A: Reading Comprehension (40 points)
- Read the provided academic article
- Answer 20 multiple-choice questions
- Time limit: 30 minutes

### Part B: Critical Analysis (60 points)  
- Write a 500-word critical evaluation
- Focus on argument structure and evidence
- Time limit: 60 minutes

### Submission Guidelines
- Submit through Moodle by [Date] 11:59 PM
- Use academic writing style
- Include proper citations
- Word count must be clearly indicated
```

#### Grading Rubric
| Criteria | Excellent (A) | Good (B) | Satisfactory (C) | Needs Improvement (D/F) |
|----------|---------------|----------|------------------|------------------------|
| Comprehension | 36-40 pts | 32-35 pts | 28-31 pts | 0-27 pts |
| Critical Analysis | 54-60 pts | 48-53 pts | 42-47 pts | 0-41 pts |
| Language Use | 9-10 pts | 8 pts | 7 pts | 0-6 pts |

## 📊 Grade Management

### Marksheet Template
```csv
Student_ID,Name,Module1_Part_A,Module1_Part_B,Total_Module1,Comments,Feedback_Sent
S001,Alice Chan,35,52,87,Excellent analysis,2025-09-15
S002,Bob Lee,32,45,77,Good comprehension,2025-09-15
```

### Grade Tracking System
- **Digital Marksheets**: CSV/Excel format with automated calculations
- **Grade Distribution Analysis**: Statistical overview of class performance
- **Individual Progress Tracking**: Per-student performance over time
- **Intervention Alerts**: Automated identification of at-risk students

## 🔄 Grading Workflow

### 1. Pre-Assessment Setup
- [ ] Finalize assessment instructions
- [ ] Prepare grading rubrics
- [ ] Set up AI grading parameters
- [ ] Create digital marksheets
- [ ] Test submission systems

### 2. During Assessment Period  
- [ ] Monitor submission rates
- [ ] Provide technical support
- [ ] Address student queries
- [ ] Backup all submissions

### 3. Grading Process
- [ ] Run AI initial analysis
- [ ] Review AI recommendations
- [ ] Apply human judgment
- [ ] Calculate final grades
- [ ] Prepare individual feedback

### 4. Post-Grading
- [ ] Deliver grades and feedback
- [ ] Update grade records
- [ ] Analyze class performance
- [ ] Plan follow-up actions
- [ ] Archive assessment materials

## 🛠️ Grading Tools and Scripts

### Assessment Analysis Tool
```bash
# Analyze assessment results
python tools/assessment_analyzer.py --input submissions/ --rubric rubrics/module1.json
```

### Grade Calculator
```bash  
# Calculate final grades with weighting
python tools/grade_calculator.py --marksheet grades.csv --weights module1:25,module2:25,portfolio:50
```

### Feedback Generator
```bash
# Generate personalized feedback using AI
python tools/feedback_generator.py --submissions submissions/ --template feedback_template.txt
```

## 📁 Files Structure
```
assessment_management/
├── README.md (this file)
├── instructions/
│   ├── module1_assessment.md
│   ├── module2_assessment.md
│   └── final_portfolio.md
├── rubrics/
│   ├── module1_rubric.json
│   ├── module2_rubric.json
│   └── portfolio_rubric.json
├── marksheets/
│   ├── class_marksheet_2025.csv
│   ├── individual_progress/
│   └── grade_analytics/
├── scripts/
│   ├── ai_grading_assistant.py
│   ├── grade_calculator.py
│   └── feedback_generator.py
└── workflows/
    ├── grading_checklist.md
    └── feedback_guidelines.md
```

## 📈 Assessment Analytics

### Performance Metrics
- **Class Average**: Track overall performance trends
- **Grade Distribution**: Monitor grade patterns and fairness
- **Learning Outcomes**: Measure achievement of course objectives
- **Improvement Tracking**: Identify student progress over time

### Reporting Dashboard
- Weekly performance summaries
- Module comparison analytics
- Individual student progress reports
- Class performance benchmarking

---
*This module supports comprehensive assessment management with AI-assisted grading*

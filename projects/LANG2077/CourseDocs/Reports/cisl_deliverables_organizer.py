#!/usr/bin/env python3
"""
CISL LANG2077 Deliverables Organizer
=====================================

This script organizes all CISL project deliverables into a structured folder
in the OneDrive directory for submission and sharing.

Author: AI Assistant
Date: September 2025
Project: LANG2077 - Language Skills for Human-AI Partnership
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CISLDeliverablesOrganizer:
    def __init__(self):
        # Source paths
        self.reports_dir = Path("/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs/Reports")
        self.course_docs_dir = Path("/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG2077/CourseDocs")
        
        # Destination path
        self.onedrive_dir = Path("/Users/simonwang/Library/CloudStorage/OneDrive-HongKongBaptistUniversity/Summer 2025/CISL-Lang2077-deliverables")
        
        # Create timestamp for backup
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def create_folder_structure(self):
        """Create the organized folder structure in OneDrive."""
        folders = [
            "01_Project_Reports",
            "02_Assessment_Questionnaires", 
            "02_Assessment_Questionnaires/PDF_Final",
            "02_Assessment_Questionnaires/HTML_Source",
            "02_Assessment_Questionnaires/Markdown_Source",
            "03_Service_Learning_Activities",
            "04_Course_Materials",
            "05_Technical_Documentation",
            "06_Backup_Files"
        ]
        
        logger.info("Creating folder structure...")
        for folder in folders:
            folder_path = self.onedrive_dir / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created: {folder_path}")
    
    def copy_project_reports(self):
        """Copy main project reports and CISL documentation."""
        logger.info("Copying project reports...")
        
        report_files = [
            ("CISL_report.md", "01_Project_Reports/CISL_Final_Report.md"),
            ("CISL.md", "01_Project_Reports/CISL_Summary.md"),
            ("PDF_Creation_Instructions.md", "05_Technical_Documentation/PDF_Creation_Instructions.md"),
            ("Questionnaire_Package_Summary.md", "05_Technical_Documentation/Questionnaire_Package_Summary.md"),
            ("SL_Activities_Fill_Summary.md", "05_Technical_Documentation/SL_Activities_Fill_Summary.md")
        ]
        
        for source_file, dest_path in report_files:
            source = self.reports_dir / source_file
            destination = self.onedrive_dir / dest_path
            if source.exists():
                shutil.copy2(source, destination)
                logger.info(f"Copied: {source_file} -> {dest_path}")
            else:
                logger.warning(f"Source file not found: {source_file}")
    
    def copy_assessment_questionnaires(self):
        """Copy all assessment questionnaire files (PDF, HTML, Markdown)."""
        logger.info("Copying assessment questionnaires...")
        
        # PDF files (final versions)
        pdf_files = [
            "Student_AI_Literacy_Questionnaire.pdf",
            "Teacher_Satisfaction_Questionnaire.pdf"
        ]
        
        for pdf_file in pdf_files:
            source = self.reports_dir / pdf_file
            destination = self.onedrive_dir / "02_Assessment_Questionnaires/PDF_Final" / pdf_file
            if source.exists():
                shutil.copy2(source, destination)
                logger.info(f"Copied PDF: {pdf_file}")
        
        # HTML files (source for printing)
        html_files = [
            "Student_AI_Literacy_Questionnaire.html",
            "Teacher_Satisfaction_Questionnaire.html"
        ]
        
        for html_file in html_files:
            source = self.reports_dir / html_file
            destination = self.onedrive_dir / "02_Assessment_Questionnaires/HTML_Source" / html_file
            if source.exists():
                shutil.copy2(source, destination)
                logger.info(f"Copied HTML: {html_file}")
        
        # Markdown files (editable source)
        md_files = [
            ("Student_AI_Literacy_Questionnaire.md", "Student_AI_Literacy_Questionnaire_Final.md"),
            ("Teacher_Satisfaction_Questionnaire.md", "Teacher_Satisfaction_Questionnaire_Final.md"),
            ("Student_AI_Literacy_Questionnaire_Long.md", "Student_AI_Literacy_Questionnaire_Original.md"),
            ("Teacher_Satisfaction_Questionnaire_Long.md", "Teacher_Satisfaction_Questionnaire_Original.md"),
            ("InstructorQuestionnaire.md", "InstructorQuestionnaire_Cleaned.md")
        ]
        
        for source_file, dest_file in md_files:
            source = self.reports_dir / source_file
            destination = self.onedrive_dir / "02_Assessment_Questionnaires/Markdown_Source" / dest_file
            if source.exists():
                shutil.copy2(source, destination)
                logger.info(f"Copied Markdown: {source_file} -> {dest_file}")
    
    def copy_service_learning_activities(self):
        """Copy service learning activity files."""
        logger.info("Copying service learning activities...")
        
        sl_files = [
            ("Table for SL activities_Complete.xlsx", "SL_Activities_Complete.xlsx"),
            ("Table for SL activities_Filled.xlsx", "SL_Activities_Filled.xlsx"),
            ("Table for SL activities_Template (Updated).xlsx", "SL_Activities_Template.xlsx")
        ]
        
        for source_file, dest_file in sl_files:
            source = self.reports_dir / source_file
            destination = self.onedrive_dir / "03_Service_Learning_Activities" / dest_file
            if source.exists():
                shutil.copy2(source, destination)
                logger.info(f"Copied SL Activity: {source_file} -> {dest_file}")
    
    def copy_course_materials(self):
        """Copy course materials from courseMat folder."""
        logger.info("Copying course materials...")
        
        course_mat_dir = self.course_docs_dir / "courseMat"
        dest_dir = self.onedrive_dir / "04_Course_Materials"
        
        if course_mat_dir.exists():
            # Copy all files from courseMat
            for file_path in course_mat_dir.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(course_mat_dir)
                    destination = dest_dir / relative_path
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, destination)
                    logger.info(f"Copied course material: {relative_path}")
        
        # Also copy any converted markdown files
        md_course_files = [
            "Course_Description.md",
            "SL_Course_Syllabus_Simon_Final.md"
        ]
        
        for md_file in md_course_files:
            source = course_mat_dir / md_file
            if source.exists():
                destination = dest_dir / md_file
                shutil.copy2(source, destination)
                logger.info(f"Copied course markdown: {md_file}")
    
    def create_backup_files(self):
        """Create backup of important files with versioning."""
        logger.info("Creating backup files...")
        
        backup_files = [
            "Student_AI_Literacy_Questionnaire_formatted.txt",
            "Teacher_Satisfaction_Questionnaire_formatted.txt",
            "InstructorQuestionnaire_backup.md",
            "PDF_Cleanup_Report.md"
        ]
        
        for backup_file in backup_files:
            source = self.reports_dir / backup_file
            if source.exists():
                dest_name = f"{self.timestamp}_{backup_file}"
                destination = self.onedrive_dir / "06_Backup_Files" / dest_name
                shutil.copy2(source, destination)
                logger.info(f"Created backup: {dest_name}")
    
    def create_readme(self):
        """Create a comprehensive README file for the deliverables."""
        readme_content = f"""# CISL LANG2077 Project Deliverables
## Language Skills for Human-AI Partnership: Customizing Chatbots to Empower Communities

**Project Code:** LANG2077  
**Instructor:** Prof. Simon Wang  
**Institution:** Language Centre, Hong Kong Baptist University  
**Semester:** Summer 2025  
**Service Location:** Henan Province, China  
**Generated:** {datetime.now().strftime("%B %d, %Y at %H:%M")}

---

## 📁 Folder Structure

### 01_Project_Reports
- **CISL_Final_Report.md** - Complete CISL service-learning report
- **CISL_Summary.md** - Executive summary of project outcomes

### 02_Assessment_Questionnaires
#### PDF_Final/ (Ready for Distribution)
- **Student_AI_Literacy_Questionnaire.pdf** - Pre/post assessment for primary students (13 questions)
- **Teacher_Satisfaction_Questionnaire.pdf** - Teacher evaluation survey (15 questions)

#### HTML_Source/ (Print-Ready Versions)
- **Student_AI_Literacy_Questionnaire.html** - HTML source for student questionnaire
- **Teacher_Satisfaction_Questionnaire.html** - HTML source for teacher questionnaire

#### Markdown_Source/ (Editable Versions)
- **Student_AI_Literacy_Questionnaire_Final.md** - Final shortened version (13 questions)
- **Teacher_Satisfaction_Questionnaire_Final.md** - Final shortened version (15 questions)
- **Student_AI_Literacy_Questionnaire_Original.md** - Original longer version (20 questions)
- **Teacher_Satisfaction_Questionnaire_Original.md** - Original longer version (27 questions)
- **InstructorQuestionnaire_Cleaned.md** - Cleaned instructor questionnaire

### 03_Service_Learning_Activities
- **SL_Activities_Complete.xlsx** - Complete activity records
- **SL_Activities_Filled.xlsx** - Filled activity template
- **SL_Activities_Template.xlsx** - Template for future use

### 04_Course_Materials
- Original course documents (DOCX format)
- Converted markdown versions
- Course syllabus and descriptions

### 05_Technical_Documentation
- **PDF_Creation_Instructions.md** - Instructions for generating PDFs
- **Questionnaire_Package_Summary.md** - Documentation of questionnaire development
- **SL_Activities_Fill_Summary.md** - Service learning activities documentation

### 06_Backup_Files
- Timestamped backup versions of important files
- Formatted text versions for reference

---

## 🎯 Project Overview

This service-learning project involved 31 Hong Kong Baptist University students teaching AI literacy to over 80 primary school students in rural Henan Province during a 2.5-week immersion program (May 23 - June 6, 2025).

### Key Achievements:
- ✅ Delivered comprehensive AI education to rural primary students
- ✅ Created bilingual assessment tools for pre/post evaluation
- ✅ Developed sustainable educational resources
- ✅ Facilitated professional development for local teachers
- ✅ Fostered cross-cultural educational collaboration

### Assessment Tools Created:
1. **Student AI Literacy Questionnaire** (Bilingual Chinese/English)
   - 13 questions across 3 sections: Basic Understanding, Skills & Experience, Attitudes & Thoughts
   - Designed for rural primary school context
   - Pre/post assessment format

2. **Teacher Satisfaction Survey** (Bilingual Chinese/English)
   - 15 questions across 4 sections: Project Evaluation, Volunteer Assessment, Teaching Content, Support & Improvement
   - Comprehensive feedback collection tool

---

## 📊 Project Impact

- **Direct Beneficiaries:** 80+ primary school students across 6 grade levels
- **Indirect Beneficiaries:** Local teaching staff, future program participants
- **Location:** Rural primary school in Henan Province, China
- **Duration:** 2.5 weeks intensive program
- **Team Size:** 31 university student volunteers

---

## 🔧 Technical Details

- **Questionnaire Development:** Created using Markdown → HTML → PDF workflow
- **Languages:** Bilingual Chinese/English for rural school context
- **Format:** Professional PDF questionnaires ready for field distribution
- **Version Control:** Multiple versions maintained for flexibility

---

## 📞 Contact Information

**Primary Contact:** Prof. Simon Wang  
**Institution:** Language Centre, Hong Kong Baptist University  
**Project:** LANG2077 - Language Skills for Human-AI Partnership  
**Email:** [Contact through university]

---

## 📝 File Generation Log

This deliverables package was automatically generated on {datetime.now().strftime("%Y-%m-%d at %H:%M:%S")} using the CISL Deliverables Organizer script.

For technical documentation and file generation details, see the Technical_Documentation folder.

---

*© 2025 Language Centre, Hong Kong Baptist University. All rights reserved.*
"""
        
        readme_path = self.onedrive_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        logger.info("Created comprehensive README.md")
    
    def create_project_summary(self):
        """Create a one-page project summary for quick reference."""
        summary_content = f"""# LANG2077 Project Summary | 项目摘要

## English Summary
**Project:** Language Skills for Human-AI Partnership: Customizing Chatbots to Empower Communities  
**Duration:** May 23 - June 6, 2025 (2.5 weeks)  
**Location:** Rural Primary School, Henan Province, China  
**Participants:** 31 HKBU students → 80+ local primary students  

### Key Deliverables:
- ✅ Bilingual AI literacy assessment questionnaires (Student & Teacher)
- ✅ Complete service-learning activity documentation
- ✅ Technical resources and lesson plans
- ✅ Comprehensive project evaluation and impact report

### Assessment Tools:
1. **Student AI Literacy Questionnaire** - 13 questions, pre/post format
2. **Teacher Satisfaction Survey** - 15 questions, comprehensive evaluation

---

## 中文摘要
**项目:** 语言技能促进人机合作：定制聊天机器人赋能社区  
**时间:** 2025年5月23日-6月6日 (2.5周)  
**地点:** 河南省乡村小学  
**参与者:** 31名港浸大学生 → 80多名当地小学生  

### 主要成果:
- ✅ 双语AI素养评估问卷 (学生版和教师版)
- ✅ 完整的服务学习活动文档
- ✅ 技术资源和教学计划
- ✅ 综合项目评估和影响报告

### 评估工具:
1. **学生AI素养问卷** - 13题，前后测试格式
2. **教师满意度调查** - 15题，综合评估

---

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**Institution:** 香港浸会大学语文中心 | Language Centre, HKBU
"""
        
        summary_path = self.onedrive_dir / "PROJECT_SUMMARY.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        logger.info("Created project summary")
    
    def run(self):
        """Execute the complete deliverables organization process."""
        logger.info("=" * 60)
        logger.info("CISL LANG2077 Deliverables Organization Started")
        logger.info("=" * 60)
        
        try:
            # Create folder structure
            self.create_folder_structure()
            
            # Copy all deliverables
            self.copy_project_reports()
            self.copy_assessment_questionnaires()
            self.copy_service_learning_activities()
            self.copy_course_materials()
            self.create_backup_files()
            
            # Create documentation
            self.create_readme()
            self.create_project_summary()
            
            logger.info("=" * 60)
            logger.info("✅ CISL Deliverables Organization Completed Successfully!")
            logger.info(f"📁 All files organized in: {self.onedrive_dir}")
            logger.info("=" * 60)
            
            # Print summary
            self.print_completion_summary()
            
        except Exception as e:
            logger.error(f"❌ Error during organization: {str(e)}")
            raise
    
    def print_completion_summary(self):
        """Print a summary of completed operations."""
        print(f"""
🎉 CISL LANG2077 DELIVERABLES SUCCESSFULLY ORGANIZED!

📁 Destination: {self.onedrive_dir}

📋 Organized Content:
├── 01_Project_Reports (CISL reports and summaries)
├── 02_Assessment_Questionnaires
│   ├── PDF_Final (Ready for distribution)
│   ├── HTML_Source (Print-ready versions)
│   └── Markdown_Source (Editable versions)
├── 03_Service_Learning_Activities (Excel files)
├── 04_Course_Materials (Course docs and syllabus)
├── 05_Technical_Documentation (Process documentation)
├── 06_Backup_Files (Timestamped backups)
├── README.md (Comprehensive project documentation)
└── PROJECT_SUMMARY.md (Quick reference guide)

🎯 Key Deliverables:
✅ Student AI Literacy Questionnaire (PDF + sources)
✅ Teacher Satisfaction Survey (PDF + sources)
✅ Complete CISL project report
✅ Service learning activities documentation
✅ Course materials and technical docs

📊 Ready for: CISL submission, stakeholder sharing, future reference

Generated: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
""")

if __name__ == "__main__":
    organizer = CISLDeliverablesOrganizer()
    organizer.run()
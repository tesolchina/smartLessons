#!/usr/bin/env python3
"""
Student List and Section Organizer for LANG0026
===============================================

This script reads the student list from Excel and cross-references it with 
Moodle forum participants to identify missing submissions and organize 
reports by section.
"""

import pandas as pd
import json
import re
from typing import Dict, List, Set
from dataclasses import dataclass

@dataclass
class Student:
    """Student information from the official list"""
    name: str
    section: str
    student_id: str = ""
    
@dataclass
class ForumParticipant:
    """Student who participated in the forum"""
    name: str
    user_id: int
    has_transcript: bool
    message: str
    
class StudentSectionOrganizer:
    """Organizes students by section and checks participation"""
    
    def __init__(self, excel_file: str, json_file: str):
        self.excel_file = excel_file
        self.json_file = json_file
        self.students_by_section = {}
        self.forum_participants = {}
        self.missing_students = []
        
    def load_student_list(self):
        """Load the official student list from Excel"""
        try:
            # Try reading the Excel file
            df = pd.read_excel(self.excel_file)
            print(f"✅ Loaded Excel file with {len(df)} rows")
            print(f"📋 Columns: {list(df.columns)}")
            
            # Display first few rows to understand structure
            print("\n📊 First 5 rows:")
            print(df.head())
            
            # Try to identify name and section columns
            name_columns = [col for col in df.columns if 'name' in col.lower() or 'student' in col.lower()]
            section_columns = [col for col in df.columns if 'section' in col.lower() or 'class' in col.lower()]
            
            print(f"\n🔍 Potential name columns: {name_columns}")
            print(f"🔍 Potential section columns: {section_columns}")
            
            return df
            
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            return None
    
    def load_forum_data(self):
        """Load forum participants from JSON"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            discussions = raw_data[0] if isinstance(raw_data[0], list) else raw_data
            
            for post in discussions:
                if post.get('userfullname') == 'Dr. WANG Simon H':
                    continue
                    
                name = post.get('userfullname', 'Unknown')
                user_id = post.get('userid', 0)
                message = post.get('message', '')
                
                # Check if has transcript
                has_transcript = self.check_has_transcript(message)
                
                self.forum_participants[name] = ForumParticipant(
                    name=name,
                    user_id=user_id,
                    has_transcript=has_transcript,
                    message=message
                )
            
            print(f"✅ Loaded {len(self.forum_participants)} forum participants")
            return True
            
        except Exception as e:
            print(f"❌ Error loading forum data: {e}")
            return False
    
    def check_has_transcript(self, message: str) -> bool:
        """Check if the message contains an actual transcript"""
        # Remove HTML tags
        clean_message = re.sub(r'<[^>]+>', ' ', message)
        
        # Template indicators
        template_indicators = [
            "Here's a sample reply template",
            "adaptable, empathetic, and curious",
            "[Name]", "[location]", "[hometown/country]",
            "This is a template that should be substantially modified"
        ]
        
        for indicator in template_indicators:
            if indicator.lower() in clean_message.lower():
                return False
        
        # Look for transcript indicators
        transcript_patterns = [
            r"(?:step 1|raw transcript|unedited.*transcript)",
            r"my name is",
            r"hello.*everyone",
            r"hi.*everyone"
        ]
        
        for pattern in transcript_patterns:
            if re.search(pattern, clean_message, re.IGNORECASE):
                if len(clean_message) > 100:  # Substantial content
                    return True
        
        return False
    
    def analyze_participation(self, df):
        """Analyze participation gaps"""
        if df is None:
            print("❌ Cannot analyze - no student data loaded")
            return
        
        print("\n📊 PARTICIPATION ANALYSIS")
        print("=" * 50)
        
        # Extract student data from Excel
        students_in_class = {}
        for _, row in df.iterrows():
            student_name = row['Student Name']
            section = row['Section Code']
            student_no = row['Student No.']
            
            students_in_class[student_name] = {
                'section': section,
                'student_no': student_no,
                'participated': False,
                'has_transcript': False
            }
        
        # Cross-reference with forum participants
        forum_names = set(self.forum_participants.keys())
        class_names = set(students_in_class.keys())
        
        print(f"📋 Total students in class: {len(class_names)}")
        print(f"💬 Forum participants: {len(forum_names)}")
        
        # Find matches and missing students
        matched_students = []
        missing_students = []
        
        for class_name in class_names:
            found_match = False
            for forum_name in forum_names:
                if self.names_match(class_name, forum_name):
                    students_in_class[class_name]['participated'] = True
                    students_in_class[class_name]['has_transcript'] = self.forum_participants[forum_name].has_transcript
                    matched_students.append((class_name, forum_name))
                    found_match = True
                    break
            
            if not found_match:
                missing_students.append(class_name)
        
        print(f"✅ Matched students: {len(matched_students)}")
        print(f"❌ Missing students: {len(missing_students)}")
        
        if missing_students:
            print("\n⚠️ Students who haven't participated:")
            for student in missing_students:
                section = students_in_class[student]['section']
                student_no = students_in_class[student]['student_no']
                print(f"  - {student} (Section {section}, ID: {student_no})")
        
        # Store for report generation
        self.students_data = students_in_class
        self.matched_students = matched_students
        self.missing_students = missing_students
        
        return students_in_class
    
    def names_match(self, class_name: str, forum_name: str) -> bool:
        """Check if two names refer to the same student"""
        # Simple matching - can be improved with fuzzy matching if needed
        class_parts = class_name.upper().split()
        forum_parts = forum_name.upper().split()
        
        # Check if surnames match (usually last part of name)
        if len(class_parts) >= 2 and len(forum_parts) >= 2:
            class_surname = class_parts[-1]
            forum_surname = forum_parts[-1]
            
            # Check if given names match (usually first part)
            class_given = class_parts[0]
            forum_given = forum_parts[0]
            
            # Match if both surname and given name match
            if class_surname == forum_surname and class_given == forum_given:
                return True
            
            # Also check middle name combinations
            if class_surname == forum_surname:
                # Check if any part of the given names match
                for class_part in class_parts[:-1]:
                    for forum_part in forum_parts[:-1]:
                        if class_part == forum_part and len(class_part) > 2:
                            return True
        
        return False
        
    def generate_section_report(self):
        """Generate a report organized by sections"""
        print("\n📋 SECTION-BASED REPORT GENERATION")
        print("=" * 50)
        
        if not hasattr(self, 'students_data'):
            print("❌ No student data available. Run analyze_participation first.")
            return
        
        # Load existing analysis results
        analysis_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback/individual_student_reports.md"
        
        try:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                existing_analysis = f.read()
        except:
            existing_analysis = ""
        
        # Group students by section
        sections = {}
        for student_name, data in self.students_data.items():
            section = data['section']
            if section not in sections:
                sections[section] = []
            sections[section].append((student_name, data))
        
        # Generate new report
        report = "# LANG0026 Individual Student Reports by Section\n\n"
        report += f"**Analysis Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Course:** LANG0036 Section 36\n\n"
        
        # Overall statistics
        total_students = len(self.students_data)
        participated = sum(1 for data in self.students_data.values() if data['participated'])
        has_transcripts = sum(1 for data in self.students_data.values() if data['has_transcript'])
        
        report += "## Overall Statistics\n\n"
        report += f"- **Total Students Enrolled:** {total_students}\n"
        report += f"- **Forum Participants:** {participated}\n"
        report += f"- **Submitted Transcripts:** {has_transcripts}\n"
        report += f"- **Participation Rate:** {(participated/total_students*100):.1f}%\n"
        report += f"- **Transcript Submission Rate:** {(has_transcripts/total_students*100):.1f}%\n\n"
        
        # Section breakdown
        for section in sorted(sections.keys()):
            report += f"## Section {section}\n\n"
            
            section_students = sections[section]
            section_participated = sum(1 for _, data in section_students if data['participated'])
            section_transcripts = sum(1 for _, data in section_students if data['has_transcript'])
            
            report += f"**Section Statistics:**\n"
            report += f"- Students: {len(section_students)}\n"
            report += f"- Participated: {section_participated}\n"
            report += f"- Submitted Transcripts: {section_transcripts}\n\n"
            
            for student_name, data in sorted(section_students):
                report += f"### {student_name} (ID: {data['student_no']})\n\n"
                
                if not data['participated']:
                    report += "❌ **Status:** No forum participation\n\n"
                    report += "**Action Required:** Student needs to submit video transcript following assignment guidelines.\n\n"
                elif not data['has_transcript']:
                    report += "⚠️ **Status:** Participated but no transcript submitted\n\n"
                    report += "**Action Required:** Student needs to submit actual video transcript (may have only posted template).\n\n"
                else:
                    report += "✅ **Status:** Transcript submitted\n\n"
                    
                    # Find this student in existing analysis and include their transcript + comments
                    student_analysis = self.extract_student_analysis(student_name, existing_analysis)
                    if student_analysis:
                        report += student_analysis
                    else:
                        # Get transcript from forum data
                        forum_name = self.find_forum_name(student_name)
                        if forum_name and forum_name in self.forum_participants:
                            participant = self.forum_participants[forum_name]
                            clean_transcript = self.extract_clean_transcript(participant.message)
                            if clean_transcript:
                                report += "#### Student's Transcript:\n\n"
                                report += f'"{clean_transcript}"\n\n'
                                report += "**Note:** Detailed analysis pending.\n\n"
                
                report += "---\n\n"
        
        # Save the report
        output_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback/section_based_reports.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Section-based report saved to: {output_file}")
        
    def find_forum_name(self, class_name: str) -> str:
        """Find the forum name that matches the class name"""
        for forum_name in self.forum_participants.keys():
            if self.names_match(class_name, forum_name):
                return forum_name
        return ""
    
    def extract_student_analysis(self, student_name: str, analysis_text: str) -> str:
        """Extract existing analysis for a specific student"""
        # Look for the student's section in the analysis
        pattern = f"## {re.escape(student_name)}.*?(?=## |$)"
        match = re.search(pattern, analysis_text, re.DOTALL)
        if match:
            return match.group(0) + "\n"
        
        # Try variations of the name
        for forum_name in self.forum_participants.keys():
            if self.names_match(student_name, forum_name):
                pattern = f"## {re.escape(forum_name)}.*?(?=## |$)"
                match = re.search(pattern, analysis_text, re.DOTALL)
                if match:
                    return match.group(0) + "\n"
        
        return ""
    
    def extract_clean_transcript(self, message: str) -> str:
        """Extract clean transcript text from HTML message"""
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', ' ', message)
        
        # Look for transcript section
        patterns = [
            r"(?:step 1|raw transcript|unedited.*transcript)[:\s]+(.*?)(?:step 2|###|error analysis|$)",
            r"(?:transcript|my video)[:\s]+(.*?)(?:step|###|error|analysis|$)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, clean_text, re.IGNORECASE | re.DOTALL)
            if match:
                transcript = match.group(1).strip()
                if len(transcript) > 50:
                    return transcript[:500] + "..." if len(transcript) > 500 else transcript
        
        # If no formal section, take first part of message
        if len(clean_text) > 100:
            return clean_text[:500] + "..." if len(clean_text) > 500 else clean_text
        
        return ""

def main():
    """Main execution"""
    excel_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/0036students.xls"
    json_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback/discussion-video-transcript.json"
    
    print("🎯 LANG0026 Student Section Organizer")
    print("=" * 50)
    
    organizer = StudentSectionOrganizer(excel_file, json_file)
    
    # Load data
    df = organizer.load_student_list()
    organizer.load_forum_data()
    
    # Analyze
    organizer.analyze_participation(df)
    organizer.generate_section_report()

if __name__ == "__main__":
    main()
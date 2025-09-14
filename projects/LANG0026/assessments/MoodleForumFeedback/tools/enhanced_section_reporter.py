#!/usr/bin/env python3
"""
Enhanced Section Report Generator
=================================

Creates comprehensive section-based reports with full transcripts and analysis.
"""

import pandas as pd
import json
import re
from datetime import datetime

class EnhancedSectionReporter:
    def __init__(self, excel_file: str, json_file: str, analysis_file: str):
        self.excel_file = excel_file
        self.json_file = json_file
        self.analysis_file = analysis_file
        self.students_data = {}
        self.forum_participants = {}
        self.analysis_data = {}
        
    def load_all_data(self):
        """Load all required data files"""
        # Load Excel student list
        df = pd.read_excel(self.excel_file)
        
        # Process student data
        for _, row in df.iterrows():
            student_name = row['Student Name']
            section = row['Section Code']
            student_no = row['Student No.']
            
            self.students_data[student_name] = {
                'section': section,
                'student_no': student_no,
                'participated': False,
                'has_transcript': False,
                'forum_name': None
            }
        
        # Load forum data
        with open(self.json_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        discussions = raw_data[0] if isinstance(raw_data[0], list) else raw_data
        
        for post in discussions:
            if post.get('userfullname') == 'Dr. WANG Simon H':
                continue
                
            name = post.get('userfullname', 'Unknown')
            self.forum_participants[name] = {
                'message': post.get('message', ''),
                'user_id': post.get('userid', 0),
                'word_count': post.get('wordcount', 0),
                'created': post.get('created', 0)
            }
        
        # Load analysis data
        try:
            with open(self.analysis_file, 'r', encoding='utf-8') as f:
                analysis_content = f.read()
            self.parse_analysis_content(analysis_content)
        except:
            print("⚠️ Could not load analysis file")
        
        # Cross-reference students
        self.cross_reference_students()
        
        print(f"✅ Loaded {len(self.students_data)} students from Excel")
        print(f"✅ Loaded {len(self.forum_participants)} forum participants")
        print(f"✅ Cross-referenced {sum(1 for s in self.students_data.values() if s['participated'])} participants")
    
    def parse_analysis_content(self, content: str):
        """Parse the existing analysis file to extract student data"""
        # Split by student sections
        student_sections = re.split(r'\n## ([^\n]+)\n', content)
        
        for i in range(1, len(student_sections), 2):
            if i+1 < len(student_sections):
                student_name = student_sections[i].strip()
                student_content = student_sections[i+1]
                
                self.analysis_data[student_name] = {
                    'content': student_content,
                    'scores': self.extract_scores(student_content),
                    'strengths': self.extract_list_items(student_content, '### 🌟 Strengths'),
                    'issues': self.extract_list_items(student_content, '### ⚠️ Areas for Improvement'),
                    'recommendations': self.extract_list_items(student_content, '### 💡 Recommendations')
                }
    
    def extract_scores(self, content: str) -> dict:
        """Extract assessment scores from analysis content"""
        scores = {}
        
        patterns = {
            'content': r'Content Coherence:\*\* (\d+)/5',
            'language': r'Language Quality:\*\* (\d+)/5',
            'fluency': r'Fluency Indicators:\*\* (\d+)/5',
            'rating': r'Overall Rating:\*\* ([^\n]+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                scores[key] = match.group(1)
        
        return scores
    
    def extract_list_items(self, content: str, section_header: str) -> list:
        """Extract list items from a specific section"""
        pattern = section_header + r'\n\n(.*?)(?=\n### |\n---|\n\n##|$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            section_content = match.group(1)
            items = re.findall(r'- ([^\n]+)', section_content)
            return items
        
        return []
    
    def cross_reference_students(self):
        """Cross-reference student list with forum participants"""
        for student_name in self.students_data:
            for forum_name in self.forum_participants:
                if self.names_match(student_name, forum_name):
                    self.students_data[student_name]['participated'] = True
                    self.students_data[student_name]['forum_name'] = forum_name
                    
                    # Check if has actual transcript
                    message = self.forum_participants[forum_name]['message']
                    self.students_data[student_name]['has_transcript'] = self.has_real_transcript(message)
                    break
    
    def names_match(self, class_name: str, forum_name: str) -> bool:
        """Check if two names refer to the same student"""
        class_parts = class_name.upper().split()
        forum_parts = forum_name.upper().split()
        
        if len(class_parts) >= 2 and len(forum_parts) >= 2:
            # Check surname (last part) and given name (first part)
            if class_parts[-1] == forum_parts[-1] and class_parts[0] == forum_parts[0]:
                return True
            
            # Check if surname matches and any given name part matches
            if class_parts[-1] == forum_parts[-1]:
                for class_part in class_parts[:-1]:
                    for forum_part in forum_parts[:-1]:
                        if class_part == forum_part and len(class_part) > 2:
                            return True
        
        return False
    
    def has_real_transcript(self, message: str) -> bool:
        """Check if message contains actual transcript (not template)"""
        clean_message = re.sub(r'<[^>]+>', ' ', message)
        
        # Template indicators
        template_indicators = [
            "Here's a sample reply template",
            "adaptable, empathetic, and curious",
            "[Name]", "[location]", "[hometown/country]"
        ]
        
        for indicator in template_indicators:
            if indicator.lower() in clean_message.lower():
                return False
        
        # Look for actual content
        if len(clean_message) > 100 and any(phrase in clean_message.lower() 
                                          for phrase in ['my name is', 'hello', 'hi everyone']):
            return True
        
        return False
    
    def extract_transcript_from_message(self, message: str) -> str:
        """Extract the actual transcript text from forum message"""
        # Remove HTML tags
        clean_message = re.sub(r'<[^>]+>', ' ', message)
        
        # Look for transcript section
        patterns = [
            r'(?:step 1|raw transcript|unedited.*transcript)[:\s]+(.*?)(?:step 2|###|error analysis|$)',
            r'(?:transcript|my video)[:\s]+(.*?)(?:step|###|error|analysis|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, clean_message, re.IGNORECASE | re.DOTALL)
            if match:
                transcript = match.group(1).strip()
                if len(transcript) > 50:
                    return transcript
        
        # If no formal section found, return first substantial part
        if len(clean_message) > 100:
            # Try to find the actual speech content
            sentences = clean_message.split('.')
            transcript_parts = []
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20 and any(word in sentence.lower() 
                                           for word in ['my name', 'describe', 'global citizen', 'background']):
                    transcript_parts.append(sentence)
                    if len(' '.join(transcript_parts)) > 200:
                        break
            
            if transcript_parts:
                return '. '.join(transcript_parts) + '.'
        
        return clean_message[:400] + "..." if len(clean_message) > 400 else clean_message
    
    def generate_comprehensive_report(self):
        """Generate the comprehensive section-based report"""
        report = "# LANG0026 Comprehensive Student Reports by Section\n\n"
        report += f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Course:** LANG0036\n\n"
        
        # Overall statistics
        total_students = len(self.students_data)
        participated = sum(1 for s in self.students_data.values() if s['participated'])
        has_transcripts = sum(1 for s in self.students_data.values() if s['has_transcript'])
        
        report += "## Overall Statistics\n\n"
        report += f"- **Total Students Enrolled:** {total_students}\n"
        report += f"- **Forum Participants:** {participated}\n"
        report += f"- **Submitted Transcripts:** {has_transcripts}\n"
        report += f"- **Participation Rate:** {(participated/total_students*100):.1f}%\n"
        report += f"- **Transcript Submission Rate:** {(has_transcripts/total_students*100):.1f}%\n\n"
        
        # Group by section
        sections = {}
        for student_name, data in self.students_data.items():
            section = data['section']
            if section not in sections:
                sections[section] = []
            sections[section].append((student_name, data))
        
        # Generate section reports
        for section in sorted(sections.keys()):
            section_students = sections[section]
            section_participated = sum(1 for _, data in section_students if data['participated'])
            section_transcripts = sum(1 for _, data in section_students if data['has_transcript'])
            
            report += f"## Section {section}\n\n"
            report += f"**Statistics:** {len(section_students)} students | "
            report += f"{section_participated} participated | {section_transcripts} submitted transcripts\n\n"
            
            for student_name, data in sorted(section_students):
                report += f"### {student_name} (ID: {data['student_no']})\n\n"
                
                if not data['participated']:
                    report += "❌ **Status:** No forum participation\n\n"
                    report += "**Action Required:** Student needs to submit video transcript.\n\n"
                elif not data['has_transcript']:
                    report += "⚠️ **Status:** Participated but no valid transcript\n\n"
                    report += "**Action Required:** Student needs to submit actual video transcript (may have only posted template).\n\n"
                else:
                    report += "✅ **Status:** Transcript submitted\n\n"
                    
                    # Include analysis if available
                    forum_name = data['forum_name']
                    if forum_name in self.analysis_data:
                        analysis = self.analysis_data[forum_name]
                        
                        # Scores
                        if analysis['scores']:
                            report += "**Assessment Scores:**\n"
                            scores = analysis['scores']
                            if 'content' in scores:
                                report += f"- Content Coherence: {scores['content']}/5\n"
                            if 'language' in scores:
                                report += f"- Language Quality: {scores['language']}/5\n"
                            if 'fluency' in scores:
                                report += f"- Fluency Indicators: {scores['fluency']}/5\n"
                            if 'rating' in scores:
                                report += f"- Overall Rating: {scores['rating']}\n"
                            report += "\n"
                        
                        # Strengths
                        if analysis['strengths']:
                            report += "**Strengths:**\n"
                            for strength in analysis['strengths']:
                                report += f"- {strength}\n"
                            report += "\n"
                        
                        # Issues
                        if analysis['issues']:
                            report += "**Areas for Improvement:**\n"
                            for issue in analysis['issues']:
                                report += f"- {issue}\n"
                            report += "\n"
                        
                        # Recommendations
                        if analysis['recommendations']:
                            report += "**Recommendations:**\n"
                            for rec in analysis['recommendations']:
                                report += f"- {rec}\n"
                            report += "\n"
                    
                    # Include transcript
                    if forum_name and forum_name in self.forum_participants:
                        transcript = self.extract_transcript_from_message(
                            self.forum_participants[forum_name]['message']
                        )
                        if transcript:
                            report += "**Student's Transcript:**\n\n"
                            report += f"> {transcript}\n\n"
                
                report += "---\n\n"
        
        return report

def main():
    excel_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/0036students.xls"
    json_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback/discussion-video-transcript.json"
    analysis_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback/individual_student_reports.md"
    
    print("🎯 Enhanced Section Report Generator")
    print("=" * 50)
    
    reporter = EnhancedSectionReporter(excel_file, json_file, analysis_file)
    reporter.load_all_data()
    
    report_content = reporter.generate_comprehensive_report()
    
    # Save report
    output_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback/comprehensive_section_reports.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ Comprehensive report saved to: {output_file}")

if __name__ == "__main__":
    main()
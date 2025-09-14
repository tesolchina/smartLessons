#!/usr/bin/env python3
"""
Complete Forum Transcript Report Generator
==========================================

This script generates a comprehensive report that includes ALL forum replies
with full transcript content for every student.
"""

import json
import re
from collections import defaultdict
from datetime import datetime

class CompleteForumReporter:
    def __init__(self, json_file: str):
        self.json_file = json_file
        self.posts = []
        self.student_submissions = defaultdict(list)
        self.instructor_posts = []
        
    def load_data(self):
        """Load and organize forum data"""
        with open(self.json_file, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # Handle nested array structure
        self.posts = raw_data[0] if isinstance(raw_data[0], list) else raw_data
        
        print(f"✅ Loaded {len(self.posts)} total posts")
        
        # Organize posts by user and type
        for post in self.posts:
            username = post.get('userfullname', 'Unknown')
            
            if username == 'Dr. WANG Simon H':
                self.instructor_posts.append(post)
            else:
                self.student_submissions[username].append(post)
        
        print(f"📋 Found {len(self.student_submissions)} unique students")
        print(f"👨‍🏫 Found {len(self.instructor_posts)} instructor posts")
    
    def clean_html(self, html_content: str) -> str:
        """Remove HTML tags and clean text"""
        text = re.sub(r'<[^>]+>', ' ', html_content)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def format_timestamp(self, timestamp):
        """Convert timestamp to readable format"""
        try:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return str(timestamp)
    
    def analyze_content_type(self, text: str) -> list:
        """Determine what type of content this text contains"""
        content_types = []
        text_lower = text.lower()
        
        # Check for transcript
        transcript_indicators = [
            'raw transcript', 'unedited video transcript', 'step 1',
            'my name is', 'hello everyone', 'hi everyone',
            'describe myself', 'three words'
        ]
        if any(indicator in text_lower for indicator in transcript_indicators) and len(text) > 150:
            content_types.append("📝 Raw Transcript")
        
        # Check for error analysis
        error_indicators = [
            'step 2', 'error analysis', 'pronunciation issues',
            'transcription errors', 'unidiomatic expressions',
            'technical issues', 'grammar', 'areas for improvement'
        ]
        if any(indicator in text_lower for indicator in error_indicators) and len(text) > 50:
            content_types.append("🔍 Error Analysis")
        
        # Check for self-assessment
        assessment_indicators = [
            'step 3', 'self-assessment', 'content analysis',
            'language analysis', 'fluency and delivery',
            'connection between questions', 'thematic focus rating'
        ]
        if any(indicator in text_lower for indicator in assessment_indicators) and len(text) > 100:
            content_types.append("📊 Self-Assessment")
        
        # Check for template
        template_indicators = ['[name]', 'adaptable, empathetic, and curious', 'sample reply template']
        if any(indicator in text_lower for indicator in template_indicators):
            content_types.append("⚠️ Template/Example")
        
        return content_types if content_types else ["📄 General Reply"]
    
    def generate_complete_report(self):
        """Generate comprehensive report with all forum content"""
        report_lines = []
        report_lines.append("# Complete Forum Transcript Report")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**Total Students:** {len(self.student_submissions)}")
        report_lines.append("")
        
        # Sort students alphabetically
        sorted_students = sorted(self.student_submissions.items())
        
        for student_name, posts in sorted_students:
            report_lines.append(f"## {student_name}")
            report_lines.append("")
            report_lines.append(f"**Total Posts:** {len(posts)}")
            
            # Sort posts by creation time
            posts.sort(key=lambda x: x.get('created', 0))
            
            # Analyze completion
            has_transcript = False
            has_error_analysis = False
            has_self_assessment = False
            
            for i, post in enumerate(posts, 1):
                parent_id = post.get('parent', 0)
                subject = post.get('subject', '')
                message = post.get('message', '')
                word_count = post.get('wordcount', 0)
                created = post.get('created', 0)
                
                # Clean message for analysis
                clean_message = self.clean_html(message)
                content_types = self.analyze_content_type(clean_message)
                
                # Track completion components
                if "📝 Raw Transcript" in content_types:
                    has_transcript = True
                if "🔍 Error Analysis" in content_types:
                    has_error_analysis = True
                if "📊 Self-Assessment" in content_types:
                    has_self_assessment = True
                
                report_lines.append(f"### Post {i}: {subject}")
                report_lines.append(f"- **Posted:** {self.format_timestamp(created)}")
                report_lines.append(f"- **Word Count:** {word_count}")
                report_lines.append(f"- **Parent ID:** {parent_id}")
                report_lines.append(f"- **Content Type:** {', '.join(content_types)}")
                report_lines.append("")
                report_lines.append("**Full Content:**")
                report_lines.append("```")
                report_lines.append(clean_message)
                report_lines.append("```")
                report_lines.append("")
            
            # Summary for this student
            completion_components = []
            if has_transcript:
                completion_components.append("✅ Raw Transcript")
            else:
                completion_components.append("❌ Raw Transcript")
            
            if has_error_analysis:
                completion_components.append("✅ Error Analysis")
            else:
                completion_components.append("❌ Error Analysis")
            
            if has_self_assessment:
                completion_components.append("✅ Self-Assessment")
            else:
                completion_components.append("❌ Self-Assessment")
            
            completion_score = sum([has_transcript, has_error_analysis, has_self_assessment])
            
            report_lines.append("### Completion Summary")
            report_lines.append(f"**Score:** {completion_score}/3 components")
            for component in completion_components:
                report_lines.append(f"- {component}")
            
            if completion_score == 3:
                report_lines.append("**Status:** 🌟 COMPLETE SUBMISSION")
            elif completion_score >= 1:
                report_lines.append("**Status:** 🟡 PARTIAL SUBMISSION")
            else:
                report_lines.append("**Status:** ❌ NO VALID CONTENT")
            
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")
        
        # Overall statistics
        complete_students = 0
        partial_students = 0
        no_content_students = 0
        
        for student_name, posts in self.student_submissions.items():
            has_transcript = False
            has_error_analysis = False
            has_self_assessment = False
            
            for post in posts:
                clean_message = self.clean_html(post.get('message', ''))
                content_types = self.analyze_content_type(clean_message)
                
                if "📝 Raw Transcript" in content_types:
                    has_transcript = True
                if "🔍 Error Analysis" in content_types:
                    has_error_analysis = True
                if "📊 Self-Assessment" in content_types:
                    has_self_assessment = True
            
            completion_score = sum([has_transcript, has_error_analysis, has_self_assessment])
            
            if completion_score == 3:
                complete_students += 1
            elif completion_score >= 1:
                partial_students += 1
            else:
                no_content_students += 1
        
        report_lines.append("# Overall Statistics")
        report_lines.append("")
        report_lines.append(f"- **Total Forum Participants:** {len(self.student_submissions)}")
        report_lines.append(f"- **Complete Submissions (3/3):** {complete_students} ({complete_students/len(self.student_submissions)*100:.1f}%)")
        report_lines.append(f"- **Partial Submissions (1-2/3):** {partial_students} ({partial_students/len(self.student_submissions)*100:.1f}%)")
        report_lines.append(f"- **No Valid Content (0/3):** {no_content_students} ({no_content_students/len(self.student_submissions)*100:.1f}%)")
        
        return '\n'.join(report_lines)
    
    def save_report(self, filename: str):
        """Generate and save the complete report"""
        report_content = self.generate_complete_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Complete forum transcript report saved to: {filename}")

def main():
    analyzer = CompleteForumReporter('discussion-video-transcript.json')
    analyzer.load_data()
    analyzer.save_report('complete_forum_transcript_report.md')

if __name__ == "__main__":
    main()
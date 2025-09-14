#!/usr/bin/env python3
"""
Comprehensive Dual Forum Analysis System
========================================

This script analyzes both forum datasets (Video Transcript and Revise Outline)
with student list cross-referencing and section-based reporting.
"""

import json
import re
import pandas as pd
from collections import defaultdict
from datetime import datetime
import os

class DualForumAnalyzer:
    def __init__(self, video_transcript_json: str, revise_outline_json: str, student_list_excel: str):
        self.video_transcript_json = video_transcript_json
        self.revise_outline_json = revise_outline_json
        self.student_list_excel = student_list_excel
        
        # Data storage
        self.video_posts = []
        self.outline_posts = []
        self.enrolled_students = {}
        
        # Analysis results
        self.video_submissions = defaultdict(list)
        self.outline_submissions = defaultdict(list)
        self.instructor_posts = {'video': [], 'outline': []}
        
    def load_all_data(self):
        """Load both forum datasets and student enrollment list"""
        print("🔄 Loading all datasets...")
        
        # Load video transcript forum
        with open(self.video_transcript_json, 'r', encoding='utf-8') as f:
            video_raw = json.load(f)
        self.video_posts = video_raw[0] if isinstance(video_raw[0], list) else video_raw
        print(f"✅ Video Transcript Forum: {len(self.video_posts)} posts")
        
        # Load revise outline forum
        with open(self.revise_outline_json, 'r', encoding='utf-8') as f:
            outline_raw = json.load(f)
        self.outline_posts = outline_raw[0] if isinstance(outline_raw[0], list) else outline_raw
        print(f"✅ Revise Outline Forum: {len(self.outline_posts)} posts")
        
        # Load student enrollment data
        df = pd.read_excel(self.student_list_excel)
        for _, row in df.iterrows():
            student_id = str(row.iloc[0]).strip()
            full_name = str(row.iloc[1]).strip()
            section = str(row.iloc[2]).strip()
            self.enrolled_students[full_name] = {
                'id': student_id,
                'section': section,
                'participated_video': False,
                'participated_outline': False
            }
        print(f"✅ Student Enrollment: {len(self.enrolled_students)} students")
        
        # Organize posts by forum and user
        self._organize_posts()
        
    def _organize_posts(self):
        """Organize posts by forum type and user"""
        # Process video transcript posts
        for post in self.video_posts:
            username = post.get('userfullname', 'Unknown')
            if username == 'Dr. WANG Simon H':
                self.instructor_posts['video'].append(post)
            else:
                self.video_submissions[username].append(post)
                # Mark participation
                if username in self.enrolled_students:
                    self.enrolled_students[username]['participated_video'] = True
        
        # Process outline posts
        for post in self.outline_posts:
            username = post.get('userfullname', 'Unknown')
            if username == 'Dr. WANG Simon H':
                self.instructor_posts['outline'].append(post)
            else:
                self.outline_submissions[username].append(post)
                # Mark participation
                if username in self.enrolled_students:
                    self.enrolled_students[username]['participated_outline'] = True
        
        print(f"📊 Video Forum: {len(self.video_submissions)} students, {len(self.instructor_posts['video'])} instructor posts")
        print(f"📊 Outline Forum: {len(self.outline_submissions)} students, {len(self.instructor_posts['outline'])} instructor posts")
    
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
    
    def analyze_video_content(self, text: str) -> list:
        """Analyze video transcript content types"""
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
        
        return content_types if content_types else ["📄 General Reply"]
    
    def analyze_outline_content(self, text: str) -> list:
        """Analyze outline revision content types"""
        content_types = []
        text_lower = text.lower()
        
        # Check for original outline
        original_indicators = [
            'original outline', 'first outline', 'my first', 'basic outline'
        ]
        if any(indicator in text_lower for indicator in original_indicators):
            content_types.append("📋 Original Outline")
        
        # Check for revision planning
        planning_indicators = [
            'revision planning', 'planning notes', 'revision strategy',
            'what i learned', 'feedback points', 'ai feedback'
        ]
        if any(indicator in text_lower for indicator in planning_indicators):
            content_types.append("🔧 Revision Planning")
        
        # Check for revised outline
        revised_indicators = [
            'revised outline', 'new outline', 'improved outline',
            'final outline', 'better outline'
        ]
        if any(indicator in text_lower for indicator in revised_indicators):
            content_types.append("📝 Revised Outline")
        
        # Check for self-reflection
        reflection_indicators = [
            'self-reflection', 'what i improved', 'still need work',
            'areas for improvement', 'understanding gained'
        ]
        if any(indicator in text_lower for indicator in reflection_indicators):
            content_types.append("🤔 Self-Reflection")
        
        return content_types if content_types else ["📄 General Reply"]
    
    def generate_individual_reports(self, output_dir: str):
        """Generate individual student reports for both forums"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate video transcript individual reports
        video_report_lines = []
        video_report_lines.append("# Individual Student Reports - Video Transcript Forum")
        video_report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        video_report_lines.append(f"**Total Participants:** {len(self.video_submissions)}")
        video_report_lines.append("")
        
        for student_name, posts in sorted(self.video_submissions.items()):
            posts.sort(key=lambda x: x.get('created', 0))
            video_report_lines.append(f"## {student_name}")
            
            # Check enrollment status
            if student_name in self.enrolled_students:
                section = self.enrolled_students[student_name]['section']
                video_report_lines.append(f"**Section:** {section}")
            else:
                video_report_lines.append("**Section:** NOT IN ENROLLMENT LIST")
            
            video_report_lines.append(f"**Total Posts:** {len(posts)}")
            video_report_lines.append("")
            
            # Analyze completion
            has_transcript = False
            has_error_analysis = False
            has_self_assessment = False
            
            for i, post in enumerate(posts, 1):
                subject = post.get('subject', '')
                message = post.get('message', '')
                word_count = post.get('wordcount', 0)
                created = post.get('created', 0)
                
                clean_message = self.clean_html(message)
                content_types = self.analyze_video_content(clean_message)
                
                if "📝 Raw Transcript" in content_types:
                    has_transcript = True
                if "🔍 Error Analysis" in content_types:
                    has_error_analysis = True
                if "📊 Self-Assessment" in content_types:
                    has_self_assessment = True
                
                video_report_lines.append(f"### Post {i}: {subject}")
                video_report_lines.append(f"- **Posted:** {self.format_timestamp(created)}")
                video_report_lines.append(f"- **Word Count:** {word_count}")
                video_report_lines.append(f"- **Content Type:** {', '.join(content_types)}")
                video_report_lines.append("")
                video_report_lines.append("**Full Content:**")
                video_report_lines.append("```")
                video_report_lines.append(clean_message[:1000] + "..." if len(clean_message) > 1000 else clean_message)
                video_report_lines.append("```")
                video_report_lines.append("")
            
            # Completion summary
            completion_score = sum([has_transcript, has_error_analysis, has_self_assessment])
            video_report_lines.append("### Completion Summary")
            video_report_lines.append(f"**Score:** {completion_score}/3 components")
            video_report_lines.append(f"- {'✅' if has_transcript else '❌'} Raw Transcript")
            video_report_lines.append(f"- {'✅' if has_error_analysis else '❌'} Error Analysis")
            video_report_lines.append(f"- {'✅' if has_self_assessment else '❌'} Self-Assessment")
            
            if completion_score == 3:
                video_report_lines.append("**Status:** 🌟 COMPLETE SUBMISSION")
            elif completion_score >= 1:
                video_report_lines.append("**Status:** 🟡 PARTIAL SUBMISSION")
            else:
                video_report_lines.append("**Status:** ❌ NO VALID CONTENT")
            
            video_report_lines.append("")
            video_report_lines.append("---")
            video_report_lines.append("")
        
        # Save video transcript individual report
        with open(f"{output_dir}/video_transcript_individual_reports.md", 'w', encoding='utf-8') as f:
            f.write('\n'.join(video_report_lines))
        
        # Generate outline individual reports (similar structure)
        outline_report_lines = []
        outline_report_lines.append("# Individual Student Reports - Revise Outline Forum")
        outline_report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        outline_report_lines.append(f"**Total Participants:** {len(self.outline_submissions)}")
        outline_report_lines.append("")
        
        for student_name, posts in sorted(self.outline_submissions.items()):
            posts.sort(key=lambda x: x.get('created', 0))
            outline_report_lines.append(f"## {student_name}")
            
            # Check enrollment status
            if student_name in self.enrolled_students:
                section = self.enrolled_students[student_name]['section']
                outline_report_lines.append(f"**Section:** {section}")
            else:
                outline_report_lines.append("**Section:** NOT IN ENROLLMENT LIST")
            
            outline_report_lines.append(f"**Total Posts:** {len(posts)}")
            outline_report_lines.append("")
            
            # Analyze completion
            has_original = False
            has_planning = False
            has_revised = False
            has_reflection = False
            
            for i, post in enumerate(posts, 1):
                subject = post.get('subject', '')
                message = post.get('message', '')
                word_count = post.get('wordcount', 0)
                created = post.get('created', 0)
                
                clean_message = self.clean_html(message)
                content_types = self.analyze_outline_content(clean_message)
                
                if "📋 Original Outline" in content_types:
                    has_original = True
                if "🔧 Revision Planning" in content_types:
                    has_planning = True
                if "📝 Revised Outline" in content_types:
                    has_revised = True
                if "🤔 Self-Reflection" in content_types:
                    has_reflection = True
                
                outline_report_lines.append(f"### Post {i}: {subject}")
                outline_report_lines.append(f"- **Posted:** {self.format_timestamp(created)}")
                outline_report_lines.append(f"- **Word Count:** {word_count}")
                outline_report_lines.append(f"- **Content Type:** {', '.join(content_types)}")
                outline_report_lines.append("")
                outline_report_lines.append("**Full Content:**")
                outline_report_lines.append("```")
                outline_report_lines.append(clean_message[:1000] + "..." if len(clean_message) > 1000 else clean_message)
                outline_report_lines.append("```")
                outline_report_lines.append("")
            
            # Completion summary
            completion_score = sum([has_original, has_planning, has_revised, has_reflection])
            outline_report_lines.append("### Completion Summary")
            outline_report_lines.append(f"**Score:** {completion_score}/4 components")
            outline_report_lines.append(f"- {'✅' if has_original else '❌'} Original Outline")
            outline_report_lines.append(f"- {'✅' if has_planning else '❌'} Revision Planning")
            outline_report_lines.append(f"- {'✅' if has_revised else '❌'} Revised Outline")
            outline_report_lines.append(f"- {'✅' if has_reflection else '❌'} Self-Reflection")
            
            if completion_score == 4:
                outline_report_lines.append("**Status:** 🌟 COMPLETE SUBMISSION")
            elif completion_score >= 2:
                outline_report_lines.append("**Status:** 🟡 PARTIAL SUBMISSION")
            else:
                outline_report_lines.append("**Status:** ❌ NO VALID CONTENT")
            
            outline_report_lines.append("")
            outline_report_lines.append("---")
            outline_report_lines.append("")
        
        # Save outline individual report
        with open(f"{output_dir}/revise_outline_individual_reports.md", 'w', encoding='utf-8') as f:
            f.write('\n'.join(outline_report_lines))
        
        print(f"✅ Individual reports saved to {output_dir}/")
    
    def generate_overall_reports(self, output_dir: str):
        """Generate comprehensive overall reports with section breakdowns"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Section-based analysis
        sections = defaultdict(lambda: {
            'enrolled': [],
            'video_participants': [],
            'outline_participants': [],
            'both_participants': [],
            'no_participation': []
        })
        
        # Organize students by section
        for student_name, data in self.enrolled_students.items():
            section = data['section']
            sections[section]['enrolled'].append(student_name)
            
            if data['participated_video'] and data['participated_outline']:
                sections[section]['both_participants'].append(student_name)
            elif data['participated_video']:
                sections[section]['video_participants'].append(student_name)
            elif data['participated_outline']:
                sections[section]['outline_participants'].append(student_name)
            else:
                sections[section]['no_participation'].append(student_name)
        
        # Generate overall report
        report_lines = []
        report_lines.append("# Comprehensive Forum Analysis Report")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**Total Enrolled Students:** {len(self.enrolled_students)}")
        report_lines.append("")
        
        # Overall statistics
        video_participants = len(self.video_submissions)
        outline_participants = len(self.outline_submissions)
        both_forums = len([s for s in self.enrolled_students.values() if s['participated_video'] and s['participated_outline']])
        no_participation = len([s for s in self.enrolled_students.values() if not s['participated_video'] and not s['participated_outline']])
        
        report_lines.append("## Overall Participation Statistics")
        report_lines.append("")
        report_lines.append(f"- **Video Transcript Forum:** {video_participants} students")
        report_lines.append(f"- **Revise Outline Forum:** {outline_participants} students")
        report_lines.append(f"- **Both Forums:** {both_forums} students")
        report_lines.append(f"- **No Participation:** {no_participation} students")
        report_lines.append("")
        
        # Section breakdown
        report_lines.append("## Section-Based Analysis")
        report_lines.append("")
        
        for section in sorted(sections.keys()):
            data = sections[section]
            total_enrolled = len(data['enrolled'])
            video_only = len(data['video_participants'])
            outline_only = len(data['outline_participants'])
            both = len(data['both_participants'])
            none = len(data['no_participation'])
            
            report_lines.append(f"### Section {section}")
            report_lines.append(f"- **Total Enrolled:** {total_enrolled}")
            report_lines.append(f"- **Video Forum Only:** {video_only}")
            report_lines.append(f"- **Outline Forum Only:** {outline_only}")
            report_lines.append(f"- **Both Forums:** {both}")
            report_lines.append(f"- **No Participation:** {none}")
            report_lines.append("")
            
            if data['no_participation']:
                report_lines.append("**Students with No Participation:**")
                for student in data['no_participation']:
                    report_lines.append(f"- {student}")
                report_lines.append("")
        
        # Detailed completion analysis for video forum
        video_complete = 0
        video_partial = 0
        for student_name, posts in self.video_submissions.items():
            has_transcript = False
            has_error_analysis = False
            has_self_assessment = False
            
            for post in posts:
                clean_message = self.clean_html(post.get('message', ''))
                content_types = self.analyze_video_content(clean_message)
                
                if "📝 Raw Transcript" in content_types:
                    has_transcript = True
                if "🔍 Error Analysis" in content_types:
                    has_error_analysis = True
                if "📊 Self-Assessment" in content_types:
                    has_self_assessment = True
            
            completion_score = sum([has_transcript, has_error_analysis, has_self_assessment])
            if completion_score == 3:
                video_complete += 1
            elif completion_score >= 1:
                video_partial += 1
        
        # Detailed completion analysis for outline forum
        outline_complete = 0
        outline_partial = 0
        for student_name, posts in self.outline_submissions.items():
            has_original = False
            has_planning = False
            has_revised = False
            has_reflection = False
            
            for post in posts:
                clean_message = self.clean_html(post.get('message', ''))
                content_types = self.analyze_outline_content(clean_message)
                
                if "📋 Original Outline" in content_types:
                    has_original = True
                if "🔧 Revision Planning" in content_types:
                    has_planning = True
                if "📝 Revised Outline" in content_types:
                    has_revised = True
                if "🤔 Self-Reflection" in content_types:
                    has_reflection = True
            
            completion_score = sum([has_original, has_planning, has_revised, has_reflection])
            if completion_score == 4:
                outline_complete += 1
            elif completion_score >= 2:
                outline_partial += 1
        
        # Add completion statistics
        report_lines.append("## Assignment Completion Quality")
        report_lines.append("")
        report_lines.append("### Video Transcript Forum")
        report_lines.append(f"- **Complete Submissions (3/3):** {video_complete} ({video_complete/video_participants*100:.1f}%)")
        report_lines.append(f"- **Partial Submissions (1-2/3):** {video_partial} ({video_partial/video_participants*100:.1f}%)")
        report_lines.append("")
        report_lines.append("### Revise Outline Forum")
        report_lines.append(f"- **Complete Submissions (4/4):** {outline_complete} ({outline_complete/outline_participants*100:.1f}%)")
        report_lines.append(f"- **Partial Submissions (2-3/4):** {outline_partial} ({outline_partial/outline_participants*100:.1f}%)")
        report_lines.append("")
        
        # Save overall report
        with open(f"{output_dir}/comprehensive_overall_report.md", 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        print(f"✅ Overall report saved to {output_dir}/")

def main():
    """Main execution function"""
    print("🚀 Starting Comprehensive Dual Forum Analysis")
    print("=" * 60)
    
    # File paths
    video_json = "discussion-video-transcript.json"
    outline_json = "Revise-outline.json"
    student_excel = "../0036students.xls"
    
    # Create analyzer
    analyzer = DualForumAnalyzer(video_json, outline_json, student_excel)
    
    # Load all data
    analyzer.load_all_data()
    
    # Generate reports for both subfolders
    print("\n📊 Generating Video Transcript Analysis...")
    analyzer.generate_individual_reports("VideoTranscriptAnalysis")
    analyzer.generate_overall_reports("VideoTranscriptAnalysis")
    
    print("\n📊 Generating Revise Outline Analysis...")
    analyzer.generate_individual_reports("ReviseOutlineAnalysis")
    analyzer.generate_overall_reports("ReviseOutlineAnalysis")
    
    print("\n🎉 Analysis complete! Check the subfolder reports.")

if __name__ == "__main__":
    main()
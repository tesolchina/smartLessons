#!/usr/bin/env python3
"""
Fixed Analysis Script - Handles Nested Replies
==============================================

This script correctly processes nested forum replies to capture all student submissions,
including those posted as replies to instructor posts.
"""

import json
import re
from collections import defaultdict
from datetime import datetime

class NestedForumAnalyzer:
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
    
    def analyze_student_submissions(self):
        """Analyze each student's complete submission set"""
        print("\n🔍 DETAILED STUDENT ANALYSIS")
        print("=" * 60)
        
        for student_name, posts in self.student_submissions.items():
            print(f"\n👤 **{student_name}**")
            print(f"   Total posts: {len(posts)}")
            
            # Sort posts by creation time
            posts.sort(key=lambda x: x.get('created', 0))
            
            transcript_found = False
            error_analysis_found = False
            self_assessment_found = False
            
            for i, post in enumerate(posts, 1):
                parent_id = post.get('parent', 0)
                subject = post.get('subject', '')
                message = post.get('message', '')
                word_count = post.get('wordcount', 0)
                
                # Clean message for analysis
                clean_message = self.clean_html(message)
                
                print(f"   📝 Post {i}: {subject} ({word_count} words)")
                print(f"      Parent ID: {parent_id}")
                
                # Check content type
                if self.contains_transcript(clean_message):
                    print("      ✅ Contains transcript")
                    transcript_found = True
                    # Extract and display transcript snippet
                    transcript = self.extract_transcript_snippet(clean_message)
                    if transcript:
                        print(f"      📖 Snippet: {transcript[:100]}...")
                
                if self.contains_error_analysis(clean_message):
                    print("      ✅ Contains error analysis")
                    error_analysis_found = True
                
                if self.contains_self_assessment(clean_message):
                    print("      ✅ Contains self-assessment")
                    self_assessment_found = True
                
                if self.is_template_response(clean_message):
                    print("      ⚠️ Appears to be template response")
            
            # Summary for this student
            completion_score = sum([transcript_found, error_analysis_found, self_assessment_found])
            print(f"   📊 Completion: {completion_score}/3 components")
            
            if completion_score == 3:
                print("   🌟 COMPLETE SUBMISSION")
            elif completion_score >= 1:
                print("   🟡 PARTIAL SUBMISSION")
            else:
                print("   ❌ NO VALID CONTENT")
    
    def clean_html(self, html_content: str) -> str:
        """Remove HTML tags and clean text"""
        text = re.sub(r'<[^>]+>', ' ', html_content)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def contains_transcript(self, text: str) -> bool:
        """Check if text contains an actual transcript"""
        indicators = [
            'raw transcript', 'unedited video transcript', 'step 1',
            'my name is', 'hello everyone', 'hi everyone',
            'describe myself', 'three words'
        ]
        
        text_lower = text.lower()
        
        # Must have transcript indicators AND substantial content
        has_indicator = any(indicator in text_lower for indicator in indicators)
        has_substance = len(text) > 150
        
        # Exclude templates
        template_indicators = ['[name]', 'adaptable, empathetic, and curious', 'sample reply template']
        is_template = any(indicator in text_lower for indicator in template_indicators)
        
        return has_indicator and has_substance and not is_template
    
    def contains_error_analysis(self, text: str) -> bool:
        """Check if text contains error analysis"""
        indicators = [
            'step 2', 'error analysis', 'pronunciation issues',
            'transcription errors', 'unidiomatic expressions',
            'technical issues', 'grammar', 'areas for improvement'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in indicators) and len(text) > 50
    
    def contains_self_assessment(self, text: str) -> bool:
        """Check if text contains self-assessment"""
        indicators = [
            'step 3', 'self-assessment', 'content analysis',
            'language analysis', 'fluency and delivery',
            'connection between questions', 'thematic focus rating'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in indicators) and len(text) > 100
    
    def is_template_response(self, text: str) -> bool:
        """Check if this is a template response"""
        template_indicators = [
            "Here's a sample reply template",
            "adaptable, empathetic, and curious",
            "[Name]", "[location]", "[hometown/country]",
            "This is a template that should be substantially modified"
        ]
        
        text_lower = text.lower()
        return any(indicator.lower() in text_lower for indicator in template_indicators)
    
    def extract_transcript_snippet(self, text: str) -> str:
        """Extract a snippet of the actual transcript"""
        patterns = [
            r'(?:raw transcript|unedited.*transcript)[:\s]+(.*?)(?:step 2|###|error analysis|$)',
            r'my name is ([^.]*(?:\.[^.]*){0,3})',
            r'hello[^.]*\.([^.]*(?:\.[^.]*){0,2})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                snippet = match.group(1).strip()
                if len(snippet) > 20:
                    return snippet
        
        return ""
    
    def generate_corrected_report(self):
        """Generate a corrected participation report"""
        print("\n📊 CORRECTED PARTICIPATION REPORT")
        print("=" * 60)
        
        complete_submissions = 0
        partial_submissions = 0
        no_submissions = 0
        
        detailed_report = "\n# Corrected Student Participation Analysis\n\n"
        detailed_report += f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for student_name, posts in self.student_submissions.items():
            posts.sort(key=lambda x: x.get('created', 0))
            
            transcript_found = False
            error_analysis_found = False
            self_assessment_found = False
            
            # Analyze all posts for this student
            all_content = ""
            for post in posts:
                clean_message = self.clean_html(post.get('message', ''))
                all_content += " " + clean_message
                
                if self.contains_transcript(clean_message):
                    transcript_found = True
                if self.contains_error_analysis(clean_message):
                    error_analysis_found = True
                if self.contains_self_assessment(clean_message):
                    self_assessment_found = True
            
            completion_score = sum([transcript_found, error_analysis_found, self_assessment_found])
            
            if completion_score == 3:
                complete_submissions += 1
                status = "🌟 COMPLETE"
            elif completion_score >= 1:
                partial_submissions += 1
                status = "🟡 PARTIAL"
            else:
                no_submissions += 1
                status = "❌ NO VALID CONTENT"
            
            detailed_report += f"## {student_name}\n\n"
            detailed_report += f"**Status:** {status} ({completion_score}/3 components)\n"
            detailed_report += f"**Total Posts:** {len(posts)}\n"
            
            if transcript_found:
                # Find the best transcript content
                for post in posts:
                    clean_message = self.clean_html(post.get('message', ''))
                    if self.contains_transcript(clean_message):
                        transcript = self.extract_full_transcript(clean_message)
                        if transcript:
                            detailed_report += f"\n**Transcript:**\n> {transcript[:300]}...\n"
                        break
            
            components = []
            if transcript_found:
                components.append("✅ Transcript")
            if error_analysis_found:
                components.append("✅ Error Analysis")
            if self_assessment_found:
                components.append("✅ Self-Assessment")
            
            if components:
                detailed_report += f"\n**Components Found:** {', '.join(components)}\n"
            
            detailed_report += "\n---\n\n"
        
        # Summary statistics
        total_students = len(self.student_submissions)
        print(f"📈 SUMMARY STATISTICS:")
        print(f"   Total Students: {total_students}")
        print(f"   Complete Submissions: {complete_submissions} ({complete_submissions/total_students*100:.1f}%)")
        print(f"   Partial Submissions: {partial_submissions} ({partial_submissions/total_students*100:.1f}%)")
        print(f"   No Valid Content: {no_submissions} ({no_submissions/total_students*100:.1f}%)")
        
        # Save the corrected report
        output_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback/corrected_participation_report.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(detailed_report)
        
        print(f"\n💾 Detailed report saved to: {output_file}")
    
    def extract_full_transcript(self, text: str) -> str:
        """Extract the full transcript text"""
        patterns = [
            r'(?:raw transcript|unedited.*transcript)[:\s]+(.*?)(?:step 2|###|error analysis|$)',
            r'(Hello[^.]*(?:\.[^.]*)*?)(?:step|###|error analysis|$)',
            r'(Hi[^.]*(?:\.[^.]*)*?)(?:step|###|error analysis|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                transcript = match.group(1).strip()
                if len(transcript) > 50:
                    return transcript
        
        return text[:400] if len(text) > 50 else text

def main():
    json_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback/discussion-video-transcript.json"
    
    print("🔍 NESTED FORUM REPLY ANALYZER")
    print("=" * 50)
    
    analyzer = NestedForumAnalyzer(json_file)
    analyzer.load_data()
    analyzer.analyze_student_submissions()
    analyzer.generate_corrected_report()
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
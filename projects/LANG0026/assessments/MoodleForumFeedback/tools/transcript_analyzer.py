#!/usr/bin/env python3
"""
LANG0026 Moodle Forum Transcript Analyzer
==========================================

This script analyzes student video transcripts from Moodle forum discussions
to evaluate their participation and assess content quality, coherence, and language use.

Key Assessment Areas:
1. Participation Check: Has the student posted their transcript?
2. Content Analysis: Coherence between the three questions (identity, background, global citizenship)
3. Language Assessment: Vocabulary range, accuracy, module-specific terminology
4. Fluency Evaluation: Speech flow, pronunciation clarity, delivery

The analysis focuses on the logic of coherence:
- Question 1: Identity (three descriptive words)
- Question 2: How background shapes global citizenship view
- Question 3: Personal definition of global citizenship

Expected: Identity and background should logically connect to and support 
the view of global citizenship.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import html

@dataclass
class StudentResponse:
    """Data structure for a single student's forum response"""
    user_id: int
    full_name: str
    subject: str
    message: str
    word_count: int
    created: int
    is_template: bool = False
    has_transcript: bool = False
    transcript_text: str = ""

@dataclass
class TranscriptAnalysis:
    """Analysis results for a student's transcript"""
    student: StudentResponse
    has_submitted_transcript: bool
    content_score: int  # 1-5
    language_score: int  # 1-5
    fluency_score: int  # 1-5
    coherence_rating: str  # Excellent/Good/Fair/Poor
    issues_found: List[str]
    strengths: List[str]
    recommendations: List[str]

class MoodleTranscriptAnalyzer:
    """Main analyzer class for processing Moodle forum transcripts"""
    
    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path
        self.discussions = []
        self.student_responses = []
        self.template_responses = []
        self.analysis_results = []
        
    def load_data(self) -> bool:
        """Load and parse the JSON data from Moodle export"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # The JSON appears to be a nested array structure
            if isinstance(raw_data, list) and len(raw_data) > 0:
                self.discussions = raw_data[0] if isinstance(raw_data[0], list) else raw_data
            else:
                self.discussions = raw_data
                
            print(f"✅ Loaded {len(self.discussions)} forum posts")
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def clean_html_message(self, html_content: str) -> str:
        """Extract plain text from HTML message content"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', html_content)
        # Decode HTML entities
        text = html.unescape(text)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_student_responses(self):
        """Extract and categorize student responses from forum data"""
        for post in self.discussions:
            # Skip instructor posts (Dr. WANG Simon H)
            if post.get('userfullname') == 'Dr. WANG Simon H':
                continue
            
            clean_message = self.clean_html_message(post.get('message', ''))
            
            student = StudentResponse(
                user_id=post.get('userid', 0),
                full_name=post.get('userfullname', 'Unknown'),
                subject=post.get('subject', ''),
                message=clean_message,
                word_count=post.get('wordcount', 0),
                created=post.get('created', 0)
            )
            
            # Check if this is a template response or actual student work
            if self.is_template_response(clean_message):
                student.is_template = True
                self.template_responses.append(student)
            else:
                student.has_transcript = self.extract_transcript(student)
                self.student_responses.append(student)
        
        print(f"📊 Found {len(self.student_responses)} student responses")
        print(f"📋 Found {len(self.template_responses)} template responses")
    
    def is_template_response(self, message: str) -> bool:
        """Check if a response appears to be the template provided by instructor"""
        template_indicators = [
            "Here's a sample reply template",
            "adaptable, empathetic, and curious",
            "[Name]", "[location]", "[hometown/country]",
            "This is a template that should be substantially modified",
            "Remember to:"
        ]
        
        for indicator in template_indicators:
            if indicator.lower() in message.lower():
                return True
        return False
    
    def extract_transcript(self, student: StudentResponse) -> bool:
        """Extract transcript text from student response and check if it's complete"""
        message = student.message
        
        # Look for transcript indicators
        transcript_patterns = [
            r"(?:step 1|raw transcript|unedited.*transcript)[:\s]+(.*?)(?:step 2|###|error analysis|$)",
            r"(?:transcript|my video)[:\s]+(.*?)(?:step|###|error|analysis|$)",
        ]
        
        for pattern in transcript_patterns:
            match = re.search(pattern, message, re.IGNORECASE | re.DOTALL)
            if match:
                transcript = match.group(1).strip()
                # Check if it's substantial (more than just a placeholder)
                if len(transcript) > 100 and not any(placeholder in transcript.lower() 
                                                  for placeholder in ['[name]', 'template', 'sample']):
                    student.transcript_text = transcript
                    return True
        
        # If no formal transcript section, check if the whole message is a transcript
        if len(message) > 100 and any(indicator in message.lower() 
                                    for indicator in ['my name is', 'hello', 'hi everyone', 'describe myself']):
            student.transcript_text = message
            return True
        
        return False
    
    def analyze_transcript_content(self, student: StudentResponse) -> TranscriptAnalysis:
        """Analyze the content quality and coherence of a student's transcript"""
        if not student.has_transcript:
            return TranscriptAnalysis(
                student=student,
                has_submitted_transcript=False,
                content_score=0,
                language_score=0,
                fluency_score=0,
                coherence_rating="No Transcript",
                issues_found=["No transcript submitted"],
                strengths=[],
                recommendations=["Submit video transcript as required"]
            )
        
        transcript = student.transcript_text.lower()
        issues = []
        strengths = []
        recommendations = []
        
        # Content Analysis
        content_score = self.analyze_content_coherence(transcript, issues, strengths)
        
        # Language Analysis  
        language_score = self.analyze_language_quality(transcript, issues, strengths)
        
        # Fluency Analysis (based on self-reported issues and transcript quality)
        fluency_score = self.analyze_fluency_indicators(student.message, issues, strengths)
        
        # Overall coherence rating
        avg_score = (content_score + language_score + fluency_score) / 3
        if avg_score >= 4.5:
            coherence_rating = "Excellent"
        elif avg_score >= 3.5:
            coherence_rating = "Good"
        elif avg_score >= 2.5:
            coherence_rating = "Fair"
        else:
            coherence_rating = "Poor"
        
        # Generate recommendations
        recommendations = self.generate_recommendations(content_score, language_score, fluency_score)
        
        return TranscriptAnalysis(
            student=student,
            has_submitted_transcript=True,
            content_score=content_score,
            language_score=language_score,
            fluency_score=fluency_score,
            coherence_rating=coherence_rating,
            issues_found=issues,
            strengths=strengths,
            recommendations=recommendations
        )
    
    def analyze_content_coherence(self, transcript: str, issues: List[str], strengths: List[str]) -> int:
        """Analyze how well the three questions are connected into a coherent narrative"""
        score = 3  # Start with average
        
        # Check for presence of the three required elements
        has_self_description = any(word in transcript for word in ['describe', 'three words', 'myself'])
        has_background_discussion = any(word in transcript for word in ['background', 'shaped', 'growing up', 'experience'])
        has_citizenship_view = any(word in transcript for word in ['global citizen', 'citizenship', 'global'])
        
        element_count = sum([has_self_description, has_background_discussion, has_citizenship_view])
        
        if element_count == 3:
            strengths.append("Addresses all three required questions")
            score += 1
        elif element_count == 2:
            strengths.append("Addresses most required questions")
        else:
            issues.append("Missing key components of the assignment")
            score -= 1
        
        # Check for logical connections
        connection_indicators = [
            'because', 'therefore', 'this helped me', 'shaped my view', 
            'connects to', 'led me to', 'influenced my'
        ]
        
        connection_count = sum(1 for indicator in connection_indicators if indicator in transcript)
        if connection_count >= 3:
            strengths.append("Shows strong logical connections between ideas")
            score += 1
        elif connection_count == 0:
            issues.append("Lacks clear connections between the three questions")
            score -= 1
        
        # Check for specific examples
        if any(phrase in transcript for phrase in ['for example', 'such as', 'like when', 'specifically']):
            strengths.append("Provides concrete examples")
            score += 0.5
        
        return max(1, min(5, int(score)))
    
    def analyze_language_quality(self, transcript: str, issues: List[str], strengths: List[str]) -> int:
        """Analyze vocabulary range, accuracy, and module-specific terminology"""
        score = 3  # Start with average
        
        # Check for module-specific vocabulary
        global_citizenship_terms = [
            'global citizenship', 'interconnected', 'sustainable', 'collaborative',
            'cultural diversity', 'empathy', 'responsibility', 'international',
            'cross-cultural', 'community', 'borders', 'perspective'
        ]
        
        term_count = sum(1 for term in global_citizenship_terms if term in transcript)
        if term_count >= 4:
            strengths.append("Uses rich vocabulary related to global citizenship")
            score += 1
        elif term_count >= 2:
            strengths.append("Uses some relevant terminology")
        else:
            issues.append("Limited use of module-specific vocabulary")
            score -= 1
        
        # Check for vocabulary variety (rough measure)
        unique_words = len(set(transcript.split()))
        total_words = len(transcript.split())
        
        if total_words > 0:
            diversity_ratio = unique_words / total_words
            if diversity_ratio > 0.7:
                strengths.append("Shows good vocabulary diversity")
                score += 0.5
            elif diversity_ratio < 0.5:
                issues.append("Limited vocabulary range")
                score -= 0.5
        
        # Check for complex sentence structures
        complex_indicators = [' which ', ' that ', ' although ', ' however ', ' moreover ', ' furthermore ']
        if sum(1 for ind in complex_indicators if ind in transcript) >= 2:
            strengths.append("Uses complex sentence structures")
            score += 0.5
        
        return max(1, min(5, int(score)))
    
    def analyze_fluency_indicators(self, full_message: str, issues: List[str], strengths: List[str]) -> int:
        """Analyze fluency based on self-reported issues and transcript characteristics"""
        score = 3  # Start with average
        
        # Look for self-reported pronunciation issues
        if any(word in full_message.lower() for word in ['pronunciation', 'unclear', 'mispronunciation']):
            issues.append("Self-reported pronunciation difficulties")
            score -= 0.5
        
        # Look for self-reported fluency issues
        if any(word in full_message.lower() for word in ['hesitation', 'pause', 'filler', 'uh', 'um']):
            issues.append("Self-reported fluency issues")
            score -= 0.5
        
        # Look for positive self-assessment
        if any(phrase in full_message.lower() for phrase in ['smooth', 'clear', 'confident', 'good flow']):
            strengths.append("Positive self-assessment of delivery")
            score += 0.5
        
        # Check transcript for fluency markers
        if 'thank you' in full_message.lower() and any(greeting in full_message.lower() 
                                                     for greeting in ['hello', 'hi', 'good morning']):
            strengths.append("Well-structured presentation format")
            score += 0.5
        
        return max(1, min(5, int(score)))
    
    def generate_recommendations(self, content_score: int, language_score: int, fluency_score: int) -> List[str]:
        """Generate personalized recommendations based on analysis scores"""
        recommendations = []
        
        if content_score < 3:
            recommendations.append("Focus on creating stronger logical connections between your identity, background, and global citizenship views")
            recommendations.append("Include specific examples to support your points")
        
        if language_score < 3:
            recommendations.append("Expand your use of module-specific vocabulary related to global citizenship")
            recommendations.append("Practice using more complex sentence structures")
        
        if fluency_score < 3:
            recommendations.append("Work on reducing hesitations and filler words")
            recommendations.append("Practice pronunciation of key terms before recording")
        
        # Positive reinforcement for strong areas
        if content_score >= 4:
            recommendations.append("Continue developing your strong narrative coherence skills")
        if language_score >= 4:
            recommendations.append("Your vocabulary use is strong - consider teaching peer study groups")
        if fluency_score >= 4:
            recommendations.append("Your delivery confidence is excellent - maintain this standard")
        
        return recommendations
    
    def analyze_all_students(self):
        """Run analysis on all student responses"""
        print("\n🔍 Analyzing student transcripts...")
        
        for student in self.student_responses:
            analysis = self.analyze_transcript_content(student)
            self.analysis_results.append(analysis)
        
        print(f"✅ Completed analysis for {len(self.analysis_results)} students")
    
    def generate_individual_reports(self) -> str:
        """Generate detailed reports for each student"""
        report = "# Individual Student Transcript Analysis Reports\n\n"
        report += f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Total Students Analyzed:** {len(self.analysis_results)}\n\n"
        
        for analysis in self.analysis_results:
            student = analysis.student
            report += f"## {student.full_name}\n\n"
            
            if not analysis.has_submitted_transcript:
                report += "❌ **Status:** No transcript submitted\n\n"
                report += "**Recommendation:** Please submit your video transcript following the assignment guidelines.\n\n"
                continue
            
            report += f"✅ **Status:** Transcript submitted ({student.word_count} words)\n\n"
            
            # Scores section
            report += "### Assessment Scores\n\n"
            report += f"- **Content Coherence:** {analysis.content_score}/5\n"
            report += f"- **Language Quality:** {analysis.language_score}/5\n"
            report += f"- **Fluency Indicators:** {analysis.fluency_score}/5\n"
            report += f"- **Overall Rating:** {analysis.coherence_rating}\n\n"
            
            # Strengths
            if analysis.strengths:
                report += "### 🌟 Strengths\n\n"
                for strength in analysis.strengths:
                    report += f"- {strength}\n"
                report += "\n"
            
            # Issues to address
            if analysis.issues_found:
                report += "### ⚠️ Areas for Improvement\n\n"
                for issue in analysis.issues_found:
                    report += f"- {issue}\n"
                report += "\n"
            
            # Recommendations
            if analysis.recommendations:
                report += "### 💡 Recommendations\n\n"
                for rec in analysis.recommendations:
                    report += f"- {rec}\n"
                report += "\n"
            
            report += "---\n\n"
        
        return report
    
    def generate_class_overview_report(self) -> str:
        """Generate overall class analysis report"""
        total_students = len(self.student_responses)
        submitted_transcripts = len([a for a in self.analysis_results if a.has_submitted_transcript])
        
        # Calculate average scores
        valid_analyses = [a for a in self.analysis_results if a.has_submitted_transcript]
        if valid_analyses:
            avg_content = sum(a.content_score for a in valid_analyses) / len(valid_analyses)
            avg_language = sum(a.language_score for a in valid_analyses) / len(valid_analyses)
            avg_fluency = sum(a.fluency_score for a in valid_analyses) / len(valid_analyses)
        else:
            avg_content = avg_language = avg_fluency = 0
        
        report = "# Class Overview: Video Transcript Analysis\n\n"
        report += f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Participation overview
        report += "## Participation Summary\n\n"
        report += f"- **Total Students:** {total_students}\n"
        report += f"- **Submitted Transcripts:** {submitted_transcripts}\n"
        report += f"- **Participation Rate:** {(submitted_transcripts/total_students*100):.1f}%\n\n"
        
        if submitted_transcripts == 0:
            report += "⚠️ **Alert:** No students have submitted transcripts yet.\n\n"
            return report
        
        # Performance overview
        report += "## Class Performance Overview\n\n"
        report += f"- **Average Content Score:** {avg_content:.1f}/5\n"
        report += f"- **Average Language Score:** {avg_language:.1f}/5\n"
        report += f"- **Average Fluency Score:** {avg_fluency:.1f}/5\n\n"
        
        # Common issues analysis
        all_issues = []
        all_strengths = []
        for analysis in valid_analyses:
            all_issues.extend(analysis.issues_found)
            all_strengths.extend(analysis.strengths)
        
        # Count frequency of issues
        issue_counts = {}
        for issue in all_issues:
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        strength_counts = {}
        for strength in all_strengths:
            strength_counts[strength] = strength_counts.get(strength, 0) + 1
        
        if issue_counts:
            report += "## Common Issues Identified\n\n"
            sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
            for issue, count in sorted_issues[:5]:  # Top 5 issues
                percentage = (count / submitted_transcripts) * 100
                report += f"- **{issue}** ({count} students, {percentage:.1f}%)\n"
            report += "\n"
        
        if strength_counts:
            report += "## Common Strengths Observed\n\n"
            sorted_strengths = sorted(strength_counts.items(), key=lambda x: x[1], reverse=True)
            for strength, count in sorted_strengths[:5]:  # Top 5 strengths
                percentage = (count / submitted_transcripts) * 100
                report += f"- **{strength}** ({count} students, {percentage:.1f}%)\n"
            report += "\n"
        
        # Class-level recommendations
        report += "## Recommendations for Future Instruction\n\n"
        
        if avg_content < 3:
            report += "- **Content Focus:** Provide more guidance on connecting personal identity to global citizenship concepts\n"
            report += "- **Coherence Training:** Include exercises on logical narrative development\n"
        
        if avg_language < 3:
            report += "- **Vocabulary Development:** Introduce more module-specific terminology exercises\n"
            report += "- **Language Practice:** Consider additional speaking practice sessions\n"
        
        if avg_fluency < 3:
            report += "- **Fluency Support:** Provide pronunciation guides for key terms\n"
            report += "- **Practice Opportunities:** Offer more low-stakes speaking practice\n"
        
        # Students needing additional support
        struggling_students = [a for a in valid_analyses if 
                             (a.content_score + a.language_score + a.fluency_score) / 3 < 2.5]
        
        if struggling_students:
            report += f"\n## Students Requiring Additional Support ({len(struggling_students)} students)\n\n"
            for analysis in struggling_students:
                report += f"- **{analysis.student.full_name}:** Consider individual consultation\n"
        
        return report
    
    def save_reports(self, output_dir: Optional[str] = None):
        """Save all generated reports to files"""
        if output_dir is None:
            output_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback"
        
        # Individual reports
        individual_report = self.generate_individual_reports()
        with open(f"{output_dir}/individual_student_reports.md", 'w', encoding='utf-8') as f:
            f.write(individual_report)
        
        # Class overview
        class_report = self.generate_class_overview_report()
        with open(f"{output_dir}/class_overview_report.md", 'w', encoding='utf-8') as f:
            f.write(class_report)
        
        print(f"📄 Reports saved to {output_dir}")
        print("   - individual_student_reports.md")
        print("   - class_overview_report.md")

def main():
    """Main execution function"""
    json_file = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LANG0026/assessments/MoodleForumFeedback/discussion-video-transcript.json"
    
    print("🎯 LANG0026 Video Transcript Analyzer")
    print("=" * 50)
    
    analyzer = MoodleTranscriptAnalyzer(json_file)
    
    # Load and process data
    if not analyzer.load_data():
        return
    
    analyzer.extract_student_responses()
    analyzer.analyze_all_students()
    
    # Generate and save reports
    analyzer.save_reports()
    
    print("\n✅ Analysis complete! Check the generated report files.")

if __name__ == "__main__":
    main()
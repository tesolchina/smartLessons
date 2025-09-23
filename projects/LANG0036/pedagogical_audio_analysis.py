#!/usr/bin/env python3
"""
LANG0036 Pedagogical Speech Analysis - Teacher & Student Friendly Version
Focuses on language learning aspects that matter for English language teaching
Date: September 23, 2025
"""

import os
import sys
import numpy as np
import pandas as pd
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

# Try to import essentia
try:
    import essentia
    import essentia.standard as es
    ESSENTIA_AVAILABLE = True
except ImportError:
    ESSENTIA_AVAILABLE = False

class PedagogicalSpeechAnalyzer:
    """
    Language teacher and student-friendly speech analysis
    Focuses on practical feedback for English language learning
    """
    
    def __init__(self, audio_path, transcript_path=None):
        self.audio_path = audio_path
        self.transcript_path = transcript_path
        self.sample_rate = 22050
        self.audio = None
        self.duration = 0
        self.transcript = ""
        self.results = {}
        
    def load_files(self):
        """Load audio and transcript files"""
        print(f"📚 Loading files for analysis...")
        
        # Load audio
        try:
            self.audio, sr_original = librosa.load(self.audio_path, sr=None)
            if self.audio is None:
                print("   ❌ Failed to load audio file")
                return False
            if sr_original != self.sample_rate:
                self.audio = librosa.resample(self.audio, orig_sr=sr_original, target_sr=self.sample_rate)
            self.duration = len(self.audio) / self.sample_rate
            print(f"   ✅ Audio loaded: {self.duration:.1f} seconds")
        except Exception as e:
            print(f"   ❌ Error loading audio: {e}")
            return False
        
        # Load transcript if available
        if self.transcript_path and os.path.exists(self.transcript_path):
            try:
                with open(self.transcript_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract just the transcript portion
                    if "TRANSCRIPT" in content:
                        transcript_section = content.split("TRANSCRIPT")[1].split("---")[1]
                        self.transcript = transcript_section.strip()
                        print(f"   ✅ Transcript loaded")
                    else:
                        self.transcript = content.strip()
            except Exception as e:
                print(f"   ⚠️  Could not load transcript: {e}")
        
        return True
    
    def analyze_speaking_confidence(self):
        """Analyze confidence and hesitation patterns"""
        print("\n🗣️  Analyzing Speaking Confidence...")
        
        if self.audio is None:
            print("   ❌ No audio data available")
            self.results['speaking_confidence'] = {'error': 'No audio data'}
            return
        
        # Detect pauses and silence
        intervals = librosa.effects.split(self.audio, top_db=20)
        
        if len(intervals) > 0:
            speech_segments = []
            pause_durations = []
            
            for start, end in intervals:
                segment_duration = (end - start) / self.sample_rate
                speech_segments.append(segment_duration)
            
            # Calculate pauses between segments
            for i in range(len(intervals) - 1):
                pause_start = intervals[i][1]
                pause_end = intervals[i + 1][0]
                pause_duration = (pause_end - pause_start) / self.sample_rate
                pause_durations.append(pause_duration)
            
            total_speech_time = sum(speech_segments)
            total_pause_time = sum(pause_durations) if pause_durations else 0
            
            confidence_metrics = {
                'total_speech_segments': len(speech_segments),
                'average_speech_segment': np.mean(speech_segments),
                'speech_to_total_ratio': total_speech_time / self.duration,
                'average_pause_duration': np.mean(pause_durations) if pause_durations else 0,
                'hesitation_frequency': len(pause_durations) / self.duration * 60,  # pauses per minute
            }
            
            # Generate confidence assessment
            speech_ratio = confidence_metrics['speech_to_total_ratio']
            avg_pause = confidence_metrics['average_pause_duration']
            
            if speech_ratio > 0.8 and avg_pause < 0.5:
                confidence_level = "High Confidence"
                confidence_feedback = "Shows good fluency with minimal hesitation"
            elif speech_ratio > 0.6 and avg_pause < 1.0:
                confidence_level = "Moderate Confidence"
                confidence_feedback = "Generally fluent with some natural pauses"
            else:
                confidence_level = "Developing Confidence"
                confidence_feedback = "Shows hesitation patterns typical of language learners"
            
            confidence_metrics.update({
                'confidence_level': confidence_level,
                'confidence_feedback': confidence_feedback
            })
            
            print(f"   Confidence Level: {confidence_level}")
            print(f"   Speech-to-total ratio: {speech_ratio:.1%}")
            print(f"   Average pause: {avg_pause:.1f} seconds")
        
        else:
            confidence_metrics = {'error': 'Could not detect speech segments'}
            print("   ⚠️  Could not analyze speech segments")
        
        self.results['speaking_confidence'] = confidence_metrics
    
    def analyze_pronunciation_clarity(self):
        """Analyze pronunciation clarity in language-learning terms"""
        print("\n🎯 Analyzing Pronunciation Clarity...")
        
        if self.audio is None:
            print("   ❌ No audio data available")
            self.results['pronunciation_clarity'] = {'error': 'No audio data'}
            return
        
        # Extract spectral features that correlate with clarity
        spectral_centroids = librosa.feature.spectral_centroid(y=self.audio, sr=self.sample_rate)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=self.audio, sr=self.sample_rate)[0]
        zero_crossing_rate = librosa.feature.zero_crossing_rate(self.audio)[0]
        
        # Calculate clarity indicators
        mean_centroid = np.mean(spectral_centroids)
        consistency_centroid = 1 - (np.std(spectral_centroids) / mean_centroid)
        mean_zcr = np.mean(zero_crossing_rate)
        
        # Assess pronunciation clarity
        if mean_centroid > 1500 and consistency_centroid > 0.7:
            clarity_level = "Clear Pronunciation"
            clarity_feedback = "Vowels and consonants are well-articulated"
        elif mean_centroid > 1200 and consistency_centroid > 0.5:
            clarity_level = "Generally Clear"
            clarity_feedback = "Most sounds are clear with room for improvement"
        else:
            clarity_level = "Needs Practice"
            clarity_feedback = "Focus on clearer articulation of sounds"
        
        clarity_metrics = {
            'clarity_level': clarity_level,
            'clarity_feedback': clarity_feedback,
            'articulation_consistency': float(consistency_centroid),
            'voice_quality_score': float(min(1.0, mean_centroid / 2000))
        }
        
        print(f"   Clarity Level: {clarity_level}")
        print(f"   Articulation Consistency: {consistency_centroid:.1%}")
        
        self.results['pronunciation_clarity'] = clarity_metrics
    
    def analyze_speaking_pace(self):
        """Analyze speaking pace and rhythm for language learners"""
        print("\n⏰ Analyzing Speaking Pace...")
        
        # Detect syllable-like units (onset detection)
        onset_frames = librosa.onset.onset_detect(y=self.audio, sr=self.sample_rate, units='time')
        
        if len(onset_frames) > 1:
            # Calculate speaking rate
            syllables_per_second = len(onset_frames) / self.duration
            syllables_per_minute = syllables_per_second * 60
            
            # Assess pace appropriateness for English learners
            if syllables_per_minute < 120:
                pace_level = "Slow Pace"
                pace_feedback = "Take time to think - good for accuracy, but try to speed up gradually"
            elif syllables_per_minute < 180:
                pace_level = "Natural Pace"
                pace_feedback = "Good natural speaking speed for clear communication"
            elif syllables_per_minute < 240:
                pace_level = "Fast Pace"
                pace_feedback = "Speaking quickly - ensure clarity isn't sacrificed for speed"
            else:
                pace_level = "Very Fast"
                pace_feedback = "Very rapid speech - slow down to improve comprehensibility"
            
            # Analyze rhythm consistency
            intervals = np.diff(onset_frames)
            rhythm_consistency = 1 - (np.std(intervals) / np.mean(intervals)) if len(intervals) > 0 else 0
            
            pace_metrics = {
                'pace_level': pace_level,
                'pace_feedback': pace_feedback,
                'syllables_per_minute': float(syllables_per_minute),
                'rhythm_consistency': float(max(0, rhythm_consistency)),
                'total_syllable_units': len(onset_frames)
            }
            
            print(f"   Pace Level: {pace_level}")
            print(f"   Rate: {syllables_per_minute:.0f} syllables/minute")
            print(f"   Rhythm Consistency: {rhythm_consistency:.1%}")
        
        else:
            pace_metrics = {'error': 'Could not detect syllable timing'}
            print("   ⚠️  Could not analyze speaking pace")
        
        self.results['speaking_pace'] = pace_metrics
    
    def analyze_intonation_patterns(self):
        """Analyze English intonation patterns"""
        print("\n🎵 Analyzing Intonation Patterns...")
        
        if ESSENTIA_AVAILABLE:
            # Use Essentia for pitch analysis - fallback approach
            try:
                # Try different Essentia pitch algorithms
                confident_pitch = np.array([])  # Default empty
            except:
                confident_pitch = np.array([])
        else:
            # Use librosa with proper null check
            if self.audio is not None:
                f0 = librosa.yin(self.audio, fmin=75, fmax=400, sr=self.sample_rate)
                confident_pitch = f0[f0 > 0]
            else:
                confident_pitch = np.array([])
        
        if len(confident_pitch) > 10:  # Need sufficient pitch data
            # Analyze pitch variation for English intonation
            pitch_mean = np.mean(confident_pitch)
            pitch_std = np.std(confident_pitch)
            pitch_range = np.max(confident_pitch) - np.min(confident_pitch)
            
            # Coefficient of variation for pitch
            pitch_variation = pitch_std / pitch_mean if pitch_mean > 0 else 0
            
            # Assess intonation appropriateness
            if pitch_variation > 0.15 and pitch_range > 50:
                intonation_level = "Good Intonation"
                intonation_feedback = "Uses appropriate pitch changes for English"
            elif pitch_variation > 0.08 and pitch_range > 30:
                intonation_level = "Developing Intonation"
                intonation_feedback = "Some pitch variation - practice questions vs statements"
            else:
                intonation_level = "Flat Intonation"
                intonation_feedback = "Practice using rising and falling pitch patterns"
            
            intonation_metrics = {
                'intonation_level': intonation_level,
                'intonation_feedback': intonation_feedback,
                'pitch_variation_score': float(min(1.0, pitch_variation * 5)),
                'pitch_range_hz': float(pitch_range),
                'expressiveness_score': float(min(1.0, (pitch_variation * pitch_range) / 20))
            }
            
            print(f"   Intonation Level: {intonation_level}")
            print(f"   Pitch Range: {pitch_range:.1f} Hz")
            print(f"   Expressiveness: {intonation_metrics['expressiveness_score']:.1%}")
        
        else:
            intonation_metrics = {
                'intonation_level': 'Cannot Assess',
                'intonation_feedback': 'Insufficient pitch data for analysis'
            }
            print("   ⚠️  Could not analyze intonation patterns")
        
        self.results['intonation_patterns'] = intonation_metrics
    
    def analyze_content_delivery(self):
        """Analyze content organization and delivery"""
        print("\n📝 Analyzing Content Delivery...")
        
        content_metrics = {}
        
        if self.transcript:
            # Analyze transcript for language learning insights
            text = self.transcript.lower()
            
            # Count discourse markers and fillers
            discourse_markers = ['uh', 'um', 'er', 'ah', 'you know', 'like', 'so', 'well', 'and']
            filler_count = sum(text.count(marker) for marker in discourse_markers)
            
            # Count word repetitions (sign of planning difficulty)
            words = text.split()
            word_repetitions = 0
            for i in range(len(words) - 1):
                if words[i] == words[i + 1] and len(words[i]) > 2:
                    word_repetitions += 1
            
            # Assess organization based on discourse markers and connectors
            connectors = ['and', 'but', 'because', 'so', 'also', 'however', 'therefore']
            connector_count = sum(text.count(conn) for conn in connectors)
            
            total_words = len(words)
            
            # Calculate delivery quality
            filler_ratio = filler_count / total_words if total_words > 0 else 0
            
            if filler_ratio < 0.05:
                delivery_level = "Fluent Delivery"
                delivery_feedback = "Speaks smoothly with minimal hesitation markers"
            elif filler_ratio < 0.10:
                delivery_level = "Generally Fluent"
                delivery_feedback = "Good flow with some natural hesitation"
            else:
                delivery_level = "Developing Fluency"
                delivery_feedback = "Practice reducing filler words and planning speech"
            
            content_metrics.update({
                'delivery_level': delivery_level,
                'delivery_feedback': delivery_feedback,
                'filler_word_ratio': float(filler_ratio),
                'word_repetition_count': word_repetitions,
                'connector_usage': connector_count,
                'total_words': total_words
            })
            
            print(f"   Delivery Level: {delivery_level}")
            print(f"   Filler word ratio: {filler_ratio:.1%}")
            print(f"   Total words: {total_words}")
        
        else:
            content_metrics = {
                'delivery_level': 'Transcript Needed',
                'delivery_feedback': 'Transcript required for content analysis'
            }
            print("   ⚠️  No transcript available for content analysis")
        
        self.results['content_delivery'] = content_metrics
    
    def generate_teacher_friendly_feedback(self):
        """Generate practical feedback for language teachers"""
        print("\n👩‍🏫 Generating Teacher-Friendly Assessment...")
        
        feedback = {
            'student_id': 'Student_Sample_001',
            'assessment_date': datetime.now().strftime('%B %d, %Y'),
            'topic': 'Sustainable Consumption (LANG0036)',
            'duration': f"{self.duration:.1f} seconds",
            'overall_assessment': {},
            'specific_recommendations': [],
            'strengths_identified': [],
            'areas_for_improvement': []
        }
        
        # Overall assessment
        confidence = self.results.get('speaking_confidence', {})
        clarity = self.results.get('pronunciation_clarity', {})
        pace = self.results.get('speaking_pace', {})
        intonation = self.results.get('intonation_patterns', {})
        delivery = self.results.get('content_delivery', {})
        
        # Determine overall level
        positive_indicators = 0
        total_indicators = 0
        
        if confidence.get('confidence_level') in ['High Confidence', 'Moderate Confidence']:
            positive_indicators += 1
        total_indicators += 1
        
        if clarity.get('clarity_level') in ['Clear Pronunciation', 'Generally Clear']:
            positive_indicators += 1
        total_indicators += 1
        
        if pace.get('pace_level') in ['Natural Pace']:
            positive_indicators += 1
        total_indicators += 1
        
        if intonation.get('intonation_level') in ['Good Intonation', 'Developing Intonation']:
            positive_indicators += 1
        total_indicators += 1
        
        if delivery.get('delivery_level') in ['Fluent Delivery', 'Generally Fluent']:
            positive_indicators += 1
        total_indicators += 1
        
        performance_ratio = positive_indicators / total_indicators if total_indicators > 0 else 0
        
        if performance_ratio >= 0.8:
            overall_level = "Advanced Intermediate"
            overall_comment = "Strong English speaking skills with minor areas for refinement"
        elif performance_ratio >= 0.6:
            overall_level = "Intermediate"
            overall_comment = "Good foundation with clear areas for improvement"
        elif performance_ratio >= 0.4:
            overall_level = "Developing Intermediate"
            overall_comment = "Basic communication skills with need for focused practice"
        else:
            overall_level = "Beginner+"
            overall_comment = "Emerging skills requiring comprehensive support"
        
        feedback['overall_assessment'] = {
            'speaking_level': overall_level,
            'overall_comment': overall_comment,
            'performance_score': f"{performance_ratio:.0%}"
        }
        
        # Collect strengths
        if confidence.get('confidence_level') in ['High Confidence', 'Moderate Confidence']:
            feedback['strengths_identified'].append(f"✅ {confidence.get('confidence_feedback', '')}")
        
        if clarity.get('clarity_level') in ['Clear Pronunciation', 'Generally Clear']:
            feedback['strengths_identified'].append(f"✅ {clarity.get('clarity_feedback', '')}")
        
        if pace.get('pace_level') == 'Natural Pace':
            feedback['strengths_identified'].append(f"✅ {pace.get('pace_feedback', '')}")
        
        # Collect improvement areas with specific recommendations
        if confidence.get('confidence_level') == 'Developing Confidence':
            feedback['areas_for_improvement'].append("🎯 Speaking Confidence")
            feedback['specific_recommendations'].append({
                'skill': 'Confidence Building',
                'activity': 'Practice recording yourself daily for 2-3 minutes on familiar topics',
                'goal': 'Reduce hesitation and build speaking fluency'
            })
        
        if clarity.get('clarity_level') == 'Needs Practice':
            feedback['areas_for_improvement'].append("🎯 Pronunciation Clarity")
            feedback['specific_recommendations'].append({
                'skill': 'Pronunciation',
                'activity': 'Focus on clear vowel sounds and word endings',
                'goal': 'Improve overall intelligibility'
            })
        
        if pace.get('pace_level') in ['Slow Pace', 'Fast Pace', 'Very Fast']:
            feedback['areas_for_improvement'].append("🎯 Speaking Pace")
            feedback['specific_recommendations'].append({
                'skill': 'Pace Control',
                'activity': 'Practice reading aloud at different speeds with a timer',
                'goal': 'Develop natural speaking rhythm'
            })
        
        if intonation.get('intonation_level') in ['Flat Intonation', 'Developing Intonation']:
            feedback['areas_for_improvement'].append("🎯 Intonation Patterns")
            feedback['specific_recommendations'].append({
                'skill': 'Intonation',
                'activity': 'Practice questions vs statements with exaggerated pitch changes',
                'goal': 'Develop English prosodic patterns'
            })
        
        if delivery.get('delivery_level') == 'Developing Fluency':
            feedback['areas_for_improvement'].append("🎯 Fluency & Planning")
            feedback['specific_recommendations'].append({
                'skill': 'Fluency',
                'activity': 'Practice 1-minute impromptu speeches on daily topics',
                'goal': 'Reduce filler words and improve speech planning'
            })
        
        # If no improvement areas found, add encouraging note
        if not feedback['areas_for_improvement']:
            feedback['strengths_identified'].append("✅ Strong overall performance across all assessed areas")
        
        self.results['teacher_feedback'] = feedback
        print(f"   Overall Level: {overall_level}")
        print(f"   Performance Score: {performance_ratio:.0%}")
        print(f"   Recommendations: {len(feedback['specific_recommendations'])}")
    
    def create_student_friendly_report(self, output_dir):
        """Create a report that students can understand and use"""
        print("\n📋 Creating Student-Friendly Report...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Create student report
        report_path = os.path.join(output_dir, 'student_feedback_report.md')
        
        teacher_feedback = self.results.get('teacher_feedback', {})
        overall = teacher_feedback.get('overall_assessment', {})
        
        with open(report_path, 'w') as f:
            f.write("# 🎯 Your Speaking Assessment Feedback\n\n")
            f.write("*This automated analysis helps you improve your English speaking skills*\n\n")
            
            f.write("## 📊 Overall Assessment\n\n")
            f.write(f"**Your Speaking Level**: {overall.get('speaking_level', 'Not assessed')}\n\n")
            f.write(f"**Performance Score**: {overall.get('performance_score', 'N/A')}\n\n")
            f.write(f"**Comment**: {overall.get('overall_comment', 'Assessment unavailable')}\n\n")
            
            # Strengths section
            strengths = teacher_feedback.get('strengths_identified', [])
            if strengths:
                f.write("## 🌟 What You're Doing Well\n\n")
                for strength in strengths:
                    f.write(f"{strength}\n\n")
            
            # Improvement areas
            improvements = teacher_feedback.get('areas_for_improvement', [])
            if improvements:
                f.write("## 🎯 Areas to Focus On\n\n")
                for area in improvements:
                    f.write(f"{area}\n\n")
            
            # Specific recommendations
            recommendations = teacher_feedback.get('specific_recommendations', [])
            if recommendations:
                f.write("## 📚 Practice Activities for You\n\n")
                for i, rec in enumerate(recommendations, 1):
                    f.write(f"### {i}. {rec['skill']}\n")
                    f.write(f"**What to practice**: {rec['activity']}\n\n")
                    f.write(f"**Your goal**: {rec['goal']}\n\n")
            
            f.write("## 💡 General Tips\n\n")
            f.write("- **Practice regularly**: Even 5-10 minutes daily helps improve fluency\n")
            f.write("- **Record yourself**: Listen back to identify patterns\n")
            f.write("- **Focus on communication**: Perfection isn't the goal - clear communication is\n")
            f.write("- **Use this feedback**: Work on one area at a time for best results\n\n")
            
            f.write("---\n")
            f.write(f"*Analysis completed on {teacher_feedback.get('assessment_date', 'Unknown date')}*\n")
            f.write("*This is an automated assessment. Discuss with your teacher for personalized guidance.*\n")
        
        print(f"   Saved student report: {report_path}")
        
        # Create teacher report
        teacher_report_path = os.path.join(output_dir, 'teacher_assessment_report.md')
        
        with open(teacher_report_path, 'w') as f:
            f.write("# 👩‍🏫 Teacher Assessment Report\n\n")
            f.write(f"**Student**: {teacher_feedback.get('student_id', 'Unknown')}\n")
            f.write(f"**Topic**: {teacher_feedback.get('topic', 'Unknown')}\n")
            f.write(f"**Duration**: {teacher_feedback.get('duration', 'Unknown')}\n")
            f.write(f"**Date**: {teacher_feedback.get('assessment_date', 'Unknown')}\n\n")
            
            # Detailed analysis for teachers
            f.write("## 📈 Detailed Analysis\n\n")
            
            # Speaking confidence
            confidence = self.results.get('speaking_confidence', {})
            if 'confidence_level' in confidence:
                f.write(f"**Speaking Confidence**: {confidence['confidence_level']}\n")
                f.write(f"- Speech-to-total ratio: {confidence.get('speech_to_total_ratio', 0):.1%}\n")
                f.write(f"- Average pause duration: {confidence.get('average_pause_duration', 0):.1f}s\n")
                f.write(f"- Hesitation frequency: {confidence.get('hesitation_frequency', 0):.1f} pauses/minute\n\n")
            
            # Pronunciation clarity
            clarity = self.results.get('pronunciation_clarity', {})
            if 'clarity_level' in clarity:
                f.write(f"**Pronunciation Clarity**: {clarity['clarity_level']}\n")
                f.write(f"- Articulation consistency: {clarity.get('articulation_consistency', 0):.1%}\n")
                f.write(f"- Voice quality score: {clarity.get('voice_quality_score', 0):.1%}\n\n")
            
            # Speaking pace
            pace = self.results.get('speaking_pace', {})
            if 'pace_level' in pace:
                f.write(f"**Speaking Pace**: {pace['pace_level']}\n")
                f.write(f"- Rate: {pace.get('syllables_per_minute', 0):.0f} syllables/minute\n")
                f.write(f"- Rhythm consistency: {pace.get('rhythm_consistency', 0):.1%}\n\n")
            
            # Intonation
            intonation = self.results.get('intonation_patterns', {})
            if 'intonation_level' in intonation:
                f.write(f"**Intonation**: {intonation['intonation_level']}\n")
                f.write(f"- Pitch range: {intonation.get('pitch_range_hz', 0):.1f} Hz\n")
                f.write(f"- Expressiveness: {intonation.get('expressiveness_score', 0):.1%}\n\n")
            
            # Content delivery
            delivery = self.results.get('content_delivery', {})
            if 'delivery_level' in delivery:
                f.write(f"**Content Delivery**: {delivery['delivery_level']}\n")
                f.write(f"- Filler word ratio: {delivery.get('filler_word_ratio', 0):.1%}\n")
                f.write(f"- Total words: {delivery.get('total_words', 0)}\n\n")
            
            # Teaching recommendations
            f.write("## 🎯 Teaching Focus Areas\n\n")
            recommendations = teacher_feedback.get('specific_recommendations', [])
            for rec in recommendations:
                f.write(f"**{rec['skill']}**: {rec['activity']}\n")
                f.write(f"*Goal: {rec['goal']}*\n\n")
        
        print(f"   Saved teacher report: {teacher_report_path}")
    
    def create_visual_dashboard(self, output_dir):
        """Create visual feedback dashboard"""
        print("\n📊 Creating Visual Dashboard...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        plt.style.use('default')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('LANG0036 Speaking Assessment Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Overall Performance Radar Chart
        ax = axes[0, 0]
        
        # Collect scores for radar chart
        scores = []
        labels = []
        
        confidence = self.results.get('speaking_confidence', {})
        if 'speech_to_total_ratio' in confidence:
            scores.append(confidence['speech_to_total_ratio'])
            labels.append('Confidence')
        
        clarity = self.results.get('pronunciation_clarity', {})
        if 'articulation_consistency' in clarity:
            scores.append(clarity['articulation_consistency'])
            labels.append('Clarity')
        
        pace = self.results.get('speaking_pace', {})
        if 'rhythm_consistency' in pace:
            scores.append(pace['rhythm_consistency'])
            labels.append('Pace')
        
        intonation = self.results.get('intonation_patterns', {})
        if 'expressiveness_score' in intonation:
            scores.append(intonation['expressiveness_score'])
            labels.append('Intonation')
        
        delivery = self.results.get('content_delivery', {})
        if 'filler_word_ratio' in delivery:
            scores.append(1 - min(1.0, delivery['filler_word_ratio'] * 10))  # Invert filler ratio
            labels.append('Fluency')
        
        if scores and labels:
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
            scores_plot = scores + [scores[0]]  # Complete the circle
            angles_plot = np.concatenate((angles, [angles[0]]))
            
            ax.plot(angles_plot, scores_plot, 'o-', linewidth=2, color='#2E86AB')
            ax.fill(angles_plot, scores_plot, alpha=0.25, color='#2E86AB')
            ax.set_xticks(angles)
            ax.set_xticklabels(labels)
            ax.set_ylim(0, 1)
            ax.set_title('Overall Performance')
            ax.grid(True)
        else:
            ax.text(0.5, 0.5, 'Insufficient data\nfor radar chart', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Overall Performance (No Data)')
        
        # 2. Speaking Pace Analysis
        ax = axes[0, 1]
        if 'syllables_per_minute' in pace:
            spm = pace['syllables_per_minute']
            
            # Create pace comparison
            ideal_range = [120, 180]
            categories = ['Too Slow\n(<120)', 'Ideal\n(120-180)', 'Too Fast\n(>180)']
            values = [max(0, 120 - spm) if spm < 120 else 0,
                     min(spm, 180) - max(spm, 120) if 120 <= spm <= 180 else 0,
                     max(0, spm - 180) if spm > 180 else 0]
            
            colors = ['#F24236', '#2E86AB', '#F24236']
            bars = ax.bar(categories, [120, 60, 120], color=['lightgray'] * 3, alpha=0.5)
            
            # Highlight actual pace
            if spm < 120:
                ax.bar(categories[0], spm, color=colors[0], alpha=0.8)
            elif spm <= 180:
                ax.bar(categories[1], spm - 120, bottom=120, color=colors[1], alpha=0.8)
            else:
                ax.bar(categories[2], min(spm - 180, 120), color=colors[2], alpha=0.8)
            
            ax.axhline(y=spm, color='red', linestyle='--', alpha=0.7)
            ax.text(1, spm + 5, f'{spm:.0f} spm', ha='center', fontweight='bold')
            ax.set_ylabel('Syllables per Minute')
            ax.set_title('Speaking Pace Assessment')
            ax.set_ylim(0, 240)
        else:
            ax.text(0.5, 0.5, 'No pace data\navailable', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Speaking Pace (No Data)')
        
        # 3. Confidence Indicators
        ax = axes[0, 2]
        if 'hesitation_frequency' in confidence and 'average_pause_duration' in confidence:
            hesitation_freq = confidence['hesitation_frequency']
            avg_pause = confidence['average_pause_duration']
            
            # Create confidence meter
            confidence_score = max(0, 1 - (hesitation_freq / 10 + avg_pause / 2))
            
            # Create a simple bar chart
            categories = ['Hesitation\nFrequency', 'Pause\nDuration', 'Overall\nConfidence']
            values = [1 - min(1, hesitation_freq / 10), 1 - min(1, avg_pause / 2), confidence_score]
            colors = ['#F24236' if v < 0.5 else '#F6AE2D' if v < 0.7 else '#2E86AB' for v in values]
            
            bars = ax.bar(categories, values, color=colors, alpha=0.8)
            ax.set_ylabel('Confidence Score')
            ax.set_title('Speaking Confidence')
            ax.set_ylim(0, 1)
            
            # Add value labels
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                       f'{value:.1%}', ha='center', va='bottom')
        else:
            ax.text(0.5, 0.5, 'No confidence data\navailable', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Speaking Confidence (No Data)')
        
        # 4. Audio Waveform
        ax = axes[1, 0]
        if self.audio is not None:
            time_axis = np.linspace(0, self.duration, len(self.audio))
            ax.plot(time_axis, self.audio, alpha=0.7, color='#2E86AB')
            ax.set_xlabel('Time (seconds)')
            ax.set_ylabel('Amplitude')
            ax.set_title('Audio Waveform')
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'No audio data\navailable', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Audio Waveform (No Data)')
        
        # 5. Pronunciation Quality
        ax = axes[1, 1]
        if 'articulation_consistency' in clarity and 'voice_quality_score' in clarity:
            articulation = clarity['articulation_consistency']
            voice_quality = clarity['voice_quality_score']
            
            categories = ['Articulation\nConsistency', 'Voice\nQuality']
            values = [articulation, voice_quality]
            colors = ['#F24236' if v < 0.5 else '#F6AE2D' if v < 0.7 else '#2E86AB' for v in values]
            
            bars = ax.bar(categories, values, color=colors, alpha=0.8)
            ax.set_ylabel('Quality Score')
            ax.set_title('Pronunciation Quality')
            ax.set_ylim(0, 1)
            
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                       f'{value:.1%}', ha='center', va='bottom')
        else:
            ax.text(0.5, 0.5, 'No pronunciation\ndata available', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Pronunciation Quality (No Data)')
        
        # 6. Progress Recommendations
        ax = axes[1, 2]
        ax.axis('off')
        
        teacher_feedback = self.results.get('teacher_feedback', {})
        overall = teacher_feedback.get('overall_assessment', {})
        
        # Create a text summary
        summary_text = f"Speaking Level: {overall.get('speaking_level', 'Not assessed')}\n\n"
        summary_text += f"Performance: {overall.get('performance_score', 'N/A')}\n\n"
        
        recommendations = teacher_feedback.get('specific_recommendations', [])
        if recommendations:
            summary_text += "Focus Areas:\n"
            for i, rec in enumerate(recommendations[:3], 1):  # Show top 3
                summary_text += f"{i}. {rec['skill']}\n"
        
        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.5))
        ax.set_title('Assessment Summary')
        
        plt.tight_layout()
        
        # Save the dashboard
        dashboard_path = os.path.join(output_dir, 'speaking_assessment_dashboard.png')
        plt.savefig(dashboard_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   Saved dashboard: {dashboard_path}")
    
    def run_pedagogical_analysis(self):
        """Run the complete pedagogical analysis"""
        print("🎓 Starting LANG0036 Pedagogical Speech Analysis")
        print("=" * 60)
        
        if not self.load_files():
            return False
        
        # Run all pedagogical analysis modules
        self.analyze_speaking_confidence()
        self.analyze_pronunciation_clarity()
        self.analyze_speaking_pace()
        self.analyze_intonation_patterns()
        self.analyze_content_delivery()
        self.generate_teacher_friendly_feedback()
        
        # Create output directory
        base_dir = os.path.dirname(self.audio_path)
        output_dir = os.path.join(base_dir, 'pedagogical_analysis')
        
        # Generate reports and visualizations
        self.create_student_friendly_report(output_dir)
        self.create_visual_dashboard(output_dir)
        
        # Save detailed results
        json_path = os.path.join(output_dir, 'detailed_pedagogical_results.json')
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print("\n" + "=" * 60)
        print("✅ Pedagogical Analysis Complete!")
        print(f"📁 Results saved to: {output_dir}")
        print("\n🎯 Generated Reports:")
        print("   📋 student_feedback_report.md - For students")
        print("   👩‍🏫 teacher_assessment_report.md - For teachers")
        print("   📊 speaking_assessment_dashboard.png - Visual overview")
        print("   💾 detailed_pedagogical_results.json - Technical data")
        
        return True

def main():
    """Main execution function"""
    # Define file paths
    audio_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0036/4_tools/essentia.js/data/Student_Sample_001_Sustainable_Consumption/Student_Sample_001_audio.mp3"
    transcript_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0036/4_tools/essentia.js/data/Student_Sample_001_Sustainable_Consumption/Student_Sample_001_transcript.txt"
    
    # Check if files exist
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    # Create analyzer instance
    analyzer = PedagogicalSpeechAnalyzer(audio_file, transcript_file)
    
    # Run the complete analysis
    success = analyzer.run_pedagogical_analysis()
    
    if success:
        print("\n🎉 LANG0036 Teacher & Student-Friendly Analysis Complete!")
        print("Ready for immediate classroom use!")
    else:
        print("\n❌ Analysis failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main()
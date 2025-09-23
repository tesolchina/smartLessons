#!/usr/bin/env python3
"""
LANG0036 Student Speech Analysis Implementation
Using Essentia and Librosa for comprehensive audio analysis
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
    print("✅ Essentia available - using advanced audio analysis")
except ImportError:
    ESSENTIA_AVAILABLE = False
    print("⚠️  Essentia not available - using Librosa-based analysis")

class StudentSpeechAnalyzer:
    """
    Comprehensive speech analysis for LANG0036 students
    Focuses on pronunciation, fluency, and prosodic features
    """
    
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.sample_rate = 22050  # Standard rate for speech analysis
        self.audio = None
        self.duration = 0
        self.results = {}
        
    def load_audio(self):
        """Load and prepare audio file for analysis"""
        try:
            print(f"🎵 Loading audio: {os.path.basename(self.audio_path)}")
            
            # Load with librosa (handles various formats)
            self.audio, sr_original = librosa.load(self.audio_path, sr=None)
            
            # Resample if needed
            if sr_original != self.sample_rate:
                self.audio = librosa.resample(self.audio, orig_sr=sr_original, target_sr=self.sample_rate)
                print(f"   Resampled from {sr_original}Hz to {self.sample_rate}Hz")
            
            self.duration = len(self.audio) / self.sample_rate
            print(f"   Duration: {self.duration:.2f} seconds")
            print(f"   Samples: {len(self.audio):,}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading audio: {e}")
            return False
    
    def analyze_pitch(self):
        """Extract pitch features for pronunciation assessment"""
        print("\n🎼 Analyzing Pitch Features...")
        
        if ESSENTIA_AVAILABLE:
            # Use Essentia's advanced pitch detection
            pitch_extractor = es.PitchYinProbabilistic(frameSize=2048, hopSize=256)
            pitch_values, confidence = pitch_extractor(self.audio)
            
            # Filter confident pitch values
            confident_pitch = pitch_values[confidence > 0.8]
            
        else:
            # Use librosa for pitch estimation
            f0 = librosa.yin(self.audio, fmin=75, fmax=600, sr=self.sample_rate)
            confident_pitch = f0[f0 > 0]  # Remove unvoiced segments
        
        if len(confident_pitch) > 0:
            pitch_stats = {
                'mean_f0': float(np.mean(confident_pitch)),
                'std_f0': float(np.std(confident_pitch)),
                'min_f0': float(np.min(confident_pitch)),
                'max_f0': float(np.max(confident_pitch)),
                'pitch_range': float(np.max(confident_pitch) - np.min(confident_pitch)),
                'voiced_percentage': float(len(confident_pitch) / len(self.audio) * 100)
            }
            
            # Assess pitch variation (important for English prosody)
            pitch_variation = np.std(confident_pitch) / np.mean(confident_pitch)
            pitch_stats['pitch_variation_coefficient'] = float(pitch_variation)
            
            # Pitch contour smoothness
            pitch_changes = np.diff(confident_pitch)
            pitch_stats['pitch_stability'] = float(1 / (1 + np.std(pitch_changes)))
            
            print(f"   Mean F0: {pitch_stats['mean_f0']:.1f} Hz")
            print(f"   Pitch Range: {pitch_stats['pitch_range']:.1f} Hz")
            print(f"   Voiced: {pitch_stats['voiced_percentage']:.1f}%")
            
        else:
            pitch_stats = {'error': 'No confident pitch detected'}
            print("   ⚠️  No confident pitch detected")
        
        self.results['pitch'] = pitch_stats
        
    def analyze_spectral_features(self):
        """Extract spectral features for pronunciation quality"""
        print("\n🌈 Analyzing Spectral Features...")
        
        # Extract MFCCs (Mel-frequency cepstral coefficients)
        mfccs = librosa.feature.mfcc(y=self.audio, sr=self.sample_rate, n_mfcc=13)
        
        # Spectral centroid (brightness)
        spectral_centroids = librosa.feature.spectral_centroid(y=self.audio, sr=self.sample_rate)[0]
        
        # Spectral rolloff (energy distribution)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=self.audio, sr=self.sample_rate)[0]
        
        # Zero crossing rate (voice quality indicator)
        zcr = librosa.feature.zero_crossing_rate(self.audio)[0]
        
        spectral_stats = {
            'mfcc_means': [float(np.mean(mfcc)) for mfcc in mfccs],
            'mfcc_stds': [float(np.std(mfcc)) for mfcc in mfccs],
            'spectral_centroid_mean': float(np.mean(spectral_centroids)),
            'spectral_centroid_std': float(np.std(spectral_centroids)),
            'spectral_rolloff_mean': float(np.mean(spectral_rolloff)),
            'spectral_rolloff_std': float(np.std(spectral_rolloff)),
            'zcr_mean': float(np.mean(zcr)),
            'zcr_std': float(np.std(zcr))
        }
        
        print(f"   Spectral Centroid: {spectral_stats['spectral_centroid_mean']:.1f} Hz")
        print(f"   Zero Crossing Rate: {spectral_stats['zcr_mean']:.4f}")
        
        self.results['spectral'] = spectral_stats
        
    def analyze_rhythm_and_timing(self):
        """Analyze speech rhythm and timing patterns"""
        print("\n⏱️  Analyzing Rhythm and Timing...")
        
        # Detect onset times (syllable/word boundaries)
        onset_frames = librosa.onset.onset_detect(y=self.audio, sr=self.sample_rate)
        onset_times = librosa.frames_to_time(onset_frames, sr=self.sample_rate)
        
        if len(onset_times) > 1:
            # Inter-onset intervals (syllable timing)
            intervals = np.diff(onset_times)
            
            rhythm_stats = {
                'num_onsets': len(onset_times),
                'speech_rate': float(len(onset_times) / self.duration),  # onsets per second
                'mean_interval': float(np.mean(intervals)),
                'interval_variability': float(np.std(intervals) / np.mean(intervals)),
                'rhythm_regularity': float(1 / (1 + np.std(intervals)))
            }
            
            print(f"   Speech Rate: {rhythm_stats['speech_rate']:.1f} onsets/sec")
            print(f"   Rhythm Regularity: {rhythm_stats['rhythm_regularity']:.3f}")
            
        else:
            rhythm_stats = {'error': 'Insufficient onsets detected'}
            print("   ⚠️  Insufficient onsets for rhythm analysis")
        
        self.results['rhythm'] = rhythm_stats
        
    def analyze_volume_dynamics(self):
        """Analyze volume and energy patterns"""
        print("\n🔊 Analyzing Volume Dynamics...")
        
        # RMS energy
        rms = librosa.feature.rms(y=self.audio)[0]
        
        # Dynamic range
        db_values = librosa.amplitude_to_db(rms)
        
        volume_stats = {
            'mean_rms': float(np.mean(rms)),
            'rms_variability': float(np.std(rms) / np.mean(rms)),
            'dynamic_range_db': float(np.max(db_values) - np.min(db_values)),
            'volume_consistency': float(1 / (1 + np.std(rms)))
        }
        
        print(f"   Dynamic Range: {volume_stats['dynamic_range_db']:.1f} dB")
        print(f"   Volume Consistency: {volume_stats['volume_consistency']:.3f}")
        
        self.results['volume'] = volume_stats
        
    def analyze_voice_quality(self):
        """Analyze voice quality indicators"""
        print("\n🎙️  Analyzing Voice Quality...")
        
        # Harmonic-to-noise ratio estimation
        try:
            # Simple HNR estimation using spectral features
            stft = librosa.stft(self.audio)
            magnitude = np.abs(stft)
            
            # Estimate harmonic vs noise content
            harmonic_strength = np.mean(np.max(magnitude, axis=0))
            noise_floor = np.mean(np.min(magnitude, axis=0))
            hnr_estimate = 20 * np.log10(harmonic_strength / (noise_floor + 1e-10))
            
            voice_quality = {
                'estimated_hnr_db': float(hnr_estimate),
                'voice_clarity': float(min(1.0, max(0.0, (hnr_estimate + 10) / 30)))  # Normalized 0-1
            }
            
            print(f"   Estimated HNR: {voice_quality['estimated_hnr_db']:.1f} dB")
            print(f"   Voice Clarity: {voice_quality['voice_clarity']:.3f}")
            
        except Exception as e:
            voice_quality = {'error': f'Voice quality analysis failed: {e}'}
            print("   ⚠️  Voice quality analysis failed")
        
        self.results['voice_quality'] = voice_quality
        
    def generate_educational_feedback(self):
        """Generate pedagogical feedback for LANG0036"""
        print("\n🎓 Generating Educational Feedback...")
        
        feedback = {
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'LANG0036_Student_Speech_Assessment',
            'recommendations': []
        }
        
        # Pitch-based feedback
        if 'pitch' in self.results and 'mean_f0' in self.results['pitch']:
            pitch_data = self.results['pitch']
            
            if pitch_data['pitch_variation_coefficient'] < 0.1:
                feedback['recommendations'].append({
                    'category': 'Prosody',
                    'issue': 'Limited pitch variation',
                    'suggestion': 'Practice using rising and falling intonation for questions and statements',
                    'priority': 'Medium'
                })
            
            if pitch_data['voiced_percentage'] < 60:
                feedback['recommendations'].append({
                    'category': 'Fluency',
                    'issue': 'Frequent silent pauses',
                    'suggestion': 'Work on connecting words smoothly and reducing hesitation',
                    'priority': 'High'
                })
        
        # Rhythm-based feedback
        if 'rhythm' in self.results and 'speech_rate' in self.results['rhythm']:
            rhythm_data = self.results['rhythm']
            
            if rhythm_data['speech_rate'] < 2.0:
                feedback['recommendations'].append({
                    'category': 'Fluency',
                    'issue': 'Slow speech rate',
                    'suggestion': 'Practice speaking at a more natural pace to improve fluency',
                    'priority': 'Medium'
                })
            elif rhythm_data['speech_rate'] > 5.0:
                feedback['recommendations'].append({
                    'category': 'Clarity',
                    'issue': 'Very fast speech rate',
                    'suggestion': 'Slow down slightly to ensure clear pronunciation',
                    'priority': 'Medium'
                })
        
        # Volume-based feedback
        if 'volume' in self.results and 'volume_consistency' in self.results['volume']:
            volume_data = self.results['volume']
            
            if volume_data['volume_consistency'] < 0.7:
                feedback['recommendations'].append({
                    'category': 'Delivery',
                    'issue': 'Inconsistent volume',
                    'suggestion': 'Practice maintaining steady volume for better audience engagement',
                    'priority': 'Low'
                })
        
        if not feedback['recommendations']:
            feedback['recommendations'].append({
                'category': 'Overall',
                'issue': 'No major issues detected',
                'suggestion': 'Continue practicing to maintain good speaking skills',
                'priority': 'Positive'
            })
        
        self.results['educational_feedback'] = feedback
        print(f"   Generated {len(feedback['recommendations'])} recommendations")
        
    def create_visualizations(self, output_dir):
        """Create visualization plots for the analysis"""
        print("\n📊 Creating Visualizations...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('LANG0036 Student Speech Analysis Report', fontsize=16, fontweight='bold')
        
        # Plot 1: Waveform
        axes[0, 0].plot(np.linspace(0, self.duration, len(self.audio)), self.audio)
        axes[0, 0].set_title('Audio Waveform')
        axes[0, 0].set_xlabel('Time (seconds)')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Spectrogram
        D = librosa.amplitude_to_db(np.abs(librosa.stft(self.audio)), ref=np.max)
        img = librosa.display.specshow(D, y_axis='hz', x_axis='time', sr=self.sample_rate, ax=axes[0, 1])
        axes[0, 1].set_title('Spectrogram')
        plt.colorbar(img, ax=axes[0, 1], format='%+2.0f dB')
        
        # Plot 3: Pitch contour (if available)
        if 'pitch' in self.results and 'mean_f0' in self.results['pitch']:
            # Create a simple pitch visualization
            if ESSENTIA_AVAILABLE:
                pitch_extractor = es.PitchYinProbabilistic(frameSize=2048, hopSize=256)
                pitch_values, confidence = pitch_extractor(self.audio)
                time_frames = np.linspace(0, self.duration, len(pitch_values))
                confident_indices = confidence > 0.8
                
                axes[1, 0].plot(time_frames[confident_indices], pitch_values[confident_indices], 'b-', alpha=0.7)
                axes[1, 0].set_title('Pitch Contour (F0)')
                axes[1, 0].set_xlabel('Time (seconds)')
                axes[1, 0].set_ylabel('Frequency (Hz)')
                axes[1, 0].grid(True, alpha=0.3)
            else:
                axes[1, 0].text(0.5, 0.5, 'Pitch analysis\nrequires Essentia', 
                               ha='center', va='center', transform=axes[1, 0].transAxes)
                axes[1, 0].set_title('Pitch Contour (Not Available)')
        else:
            axes[1, 0].text(0.5, 0.5, 'No pitch data\navailable', 
                           ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('Pitch Contour (No Data)')
        
        # Plot 4: Feature summary
        if 'spectral' in self.results:
            mfcc_means = self.results['spectral']['mfcc_means'][:12]  # First 12 MFCCs
            axes[1, 1].bar(range(len(mfcc_means)), mfcc_means)
            axes[1, 1].set_title('MFCC Features (Pronunciation Quality)')
            axes[1, 1].set_xlabel('MFCC Coefficient')
            axes[1, 1].set_ylabel('Mean Value')
            axes[1, 1].grid(True, alpha=0.3)
        else:
            axes[1, 1].text(0.5, 0.5, 'No spectral data\navailable', 
                           ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Spectral Features (No Data)')
        
        plt.tight_layout()
        
        # Save the plot
        plot_path = os.path.join(output_dir, 'speech_analysis_report.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   Saved visualization: {plot_path}")
        
    def save_results(self, output_dir):
        """Save analysis results to files"""
        print("\n💾 Saving Analysis Results...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save detailed JSON results
        json_path = os.path.join(output_dir, 'detailed_analysis_results.json')
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"   Saved JSON results: {json_path}")
        
        # Create a human-readable report
        report_path = os.path.join(output_dir, 'speech_analysis_report.md')
        with open(report_path, 'w') as f:
            f.write("# LANG0036 Student Speech Analysis Report\n\n")
            f.write(f"**Analysis Date**: {datetime.now().strftime('%B %d, %Y at %H:%M')}\n")
            f.write(f"**Audio File**: {os.path.basename(self.audio_path)}\n")
            f.write(f"**Duration**: {self.duration:.2f} seconds\n\n")
            
            # Pitch Analysis
            if 'pitch' in self.results and 'mean_f0' in self.results['pitch']:
                pitch = self.results['pitch']
                f.write("## 🎼 Pitch Analysis\n")
                f.write(f"- **Mean F0**: {pitch['mean_f0']:.1f} Hz\n")
                f.write(f"- **Pitch Range**: {pitch['pitch_range']:.1f} Hz\n")
                f.write(f"- **Voiced Speech**: {pitch['voiced_percentage']:.1f}%\n")
                f.write(f"- **Pitch Variation**: {pitch['pitch_variation_coefficient']:.3f}\n")
                f.write(f"- **Pitch Stability**: {pitch['pitch_stability']:.3f}\n\n")
            
            # Rhythm Analysis
            if 'rhythm' in self.results and 'speech_rate' in self.results['rhythm']:
                rhythm = self.results['rhythm']
                f.write("## ⏱️ Rhythm and Timing\n")
                f.write(f"- **Speech Rate**: {rhythm['speech_rate']:.1f} onsets/second\n")
                f.write(f"- **Number of Onsets**: {rhythm['num_onsets']}\n")
                f.write(f"- **Rhythm Regularity**: {rhythm['rhythm_regularity']:.3f}\n\n")
            
            # Volume Analysis
            if 'volume' in self.results:
                volume = self.results['volume']
                f.write("## 🔊 Volume Dynamics\n")
                f.write(f"- **Dynamic Range**: {volume['dynamic_range_db']:.1f} dB\n")
                f.write(f"- **Volume Consistency**: {volume['volume_consistency']:.3f}\n\n")
            
            # Educational Feedback
            if 'educational_feedback' in self.results:
                feedback = self.results['educational_feedback']
                f.write("## 🎓 Educational Recommendations\n\n")
                for i, rec in enumerate(feedback['recommendations'], 1):
                    f.write(f"### {i}. {rec['category']} - {rec['priority']} Priority\n")
                    f.write(f"**Issue**: {rec['issue']}\n\n")
                    f.write(f"**Suggestion**: {rec['suggestion']}\n\n")
        
        print(f"   Saved readable report: {report_path}")
        
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("🚀 Starting LANG0036 Student Speech Analysis")
        print("=" * 50)
        
        if not self.load_audio():
            return False
        
        # Run all analysis modules
        self.analyze_pitch()
        self.analyze_spectral_features()
        self.analyze_rhythm_and_timing()
        self.analyze_volume_dynamics()
        self.analyze_voice_quality()
        self.generate_educational_feedback()
        
        # Create output directory
        base_dir = os.path.dirname(self.audio_path)
        output_dir = os.path.join(base_dir, 'analysis_results')
        
        # Save results and visualizations
        self.save_results(output_dir)
        self.create_visualizations(output_dir)
        
        print("\n" + "=" * 50)
        print("✅ Analysis Complete!")
        print(f"📁 Results saved to: {output_dir}")
        
        return True

def main():
    """Main execution function"""
    # Define the audio file path
    audio_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/LANG0036/4_tools/essentia.js/data/Student_Sample_001_Sustainable_Consumption/Student_Sample_001_audio.mp3"
    
    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    # Create analyzer instance
    analyzer = StudentSpeechAnalyzer(audio_file)
    
    # Run the complete analysis
    success = analyzer.run_complete_analysis()
    
    if success:
        print("\n🎉 LANG0036 Speech Analysis Implementation Complete!")
        print("Ready for integration into Critical Dialogue Practice sessions.")
    else:
        print("\n❌ Analysis failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    main()
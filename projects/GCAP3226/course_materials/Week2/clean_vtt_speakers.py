#!/usr/bin/env python3
"""
VTT File Cleaner with Speaker Separation
This script cleans VTT files and optionally separates content by speakers.
"""

import re
import os

def clean_vtt_with_speakers(input_file, output_file):
    """
    Clean VTT file and separate by speakers
    
    Args:
        input_file (str): Path to input VTT file
        output_file (str): Path to output cleaned text file
    """
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        speakers = {}
        current_speaker = None
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines, WEBVTT, numbers, timestamps
            if not line or line == 'WEBVTT' or line.isdigit() or '-->' in line:
                continue
            
            # Skip pure timestamp lines
            if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}$', line):
                continue
            
            # Check if line contains speaker label
            if ':' in line and len(line) > 10:
                # Extract speaker name
                speaker_match = re.match(r'^([^:]+):\s*(.*)', line)
                if speaker_match:
                    speaker_name = speaker_match.group(1).strip()
                    text = speaker_match.group(2).strip()
                    
                    # Initialize speaker if new
                    if speaker_name not in speakers:
                        speakers[speaker_name] = []
                    
                    # Add text if there's content
                    if text:
                        speakers[speaker_name].append(text)
                    
                    current_speaker = speaker_name
                else:
                    # If no clear speaker pattern, add to current speaker
                    if current_speaker and line:
                        speakers[current_speaker].append(line)
            else:
                # Add to current speaker if we have one
                if current_speaker and line:
                    speakers[current_speaker].append(line)
        
        # Write cleaned text with speaker separation
        with open(output_file, 'w', encoding='utf-8') as f:
            for speaker, texts in speakers.items():
                f.write(f"\n{'='*50}\n")
                f.write(f"SPEAKER: {speaker.upper()}\n")
                f.write(f"{'='*50}\n\n")
                
                # Join all texts for this speaker and clean up
                full_text = ' '.join(texts)
                full_text = re.sub(r'\s+', ' ', full_text)
                
                # Split into sentences for readability
                sentences = re.split(r'(?<=[.!?])\s+', full_text)
                
                for sentence in sentences:
                    if sentence.strip():
                        f.write(sentence.strip() + '\n\n')
        
        print(f"✅ Successfully cleaned VTT file with speaker separation!")
        print(f"📁 Input: {input_file}")
        print(f"📁 Output: {output_file}")
        print(f"👥 Speakers found: {', '.join(speakers.keys())}")
        for speaker, texts in speakers.items():
            word_count = len(' '.join(texts).split())
            print(f"   - {speaker}: {word_count} words")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find file '{input_file}'")
    except Exception as e:
        print(f"❌ Error processing file: {e}")

def main():
    """Main function"""
    
    input_file = "c:/usage/VibeCoding/DailyAssistant/DailyAssistant/projects/GCAP3226/course_materials/Week2/week2.vtt"
    output_file = "c:/usage/VibeCoding/DailyAssistant/DailyAssistant/projects/GCAP3226/course_materials/Week2/week2_by_speakers.txt"
    
    print("🧹 VTT File Cleaner with Speaker Separation")
    print("=" * 60)
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return
    
    clean_vtt_with_speakers(input_file, output_file)

if __name__ == "__main__":
    main()

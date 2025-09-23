#!/usr/bin/env python3
"""
VTT Transcript Processor for GCAP3226 Week 4 Lecture
Converts WebVTT subtitle file into properly formatted transcript
"""

import re
import os
from datetime import datetime

def parse_vtt_file(vtt_file_path):
    """Parse VTT file and extract transcript content"""
    transcript_entries = []
    
    with open(vtt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split content into blocks (separated by double newlines)
    blocks = content.split('\n\n')
    
    for block in blocks:
        lines = block.strip().split('\n')
        
        # Skip header and empty blocks
        if len(lines) < 3 or lines[0] == 'WEBVTT':
            continue
            
        # Extract timestamp and text
        if '-->' in lines[1]:  # Second line should contain timestamp
            timestamp_line = lines[1]
            text_lines = lines[2:]
            
            # Parse timestamp
            start_time, end_time = timestamp_line.split(' --> ')
            start_time = start_time.strip()
            end_time = end_time.strip()
            
            # Combine text lines
            text = ' '.join(text_lines).strip()
            
            # Extract speaker name if present
            speaker = "Unknown Speaker"
            if ':' in text:
                parts = text.split(':', 1)
                if len(parts) == 2:
                    speaker = parts[0].strip()
                    text = parts[1].strip()
            
            transcript_entries.append({
                'start_time': start_time,
                'end_time': end_time,
                'speaker': speaker,
                'text': text
            })
    
    return transcript_entries

def format_transcript(transcript_entries):
    """Format transcript entries into readable text"""
    formatted_transcript = []
    current_speaker = None
    current_text_block = []
    
    for entry in transcript_entries:
        speaker = entry['speaker']
        text = entry['text']
        start_time = entry['start_time']
        
        # If speaker changes, finalize previous block
        if current_speaker and current_speaker != speaker:
            # Add previous speaker's text block
            full_text = ' '.join(current_text_block)
            formatted_transcript.append(f"\n**{current_speaker}:**\n{full_text}\n")
            current_text_block = []
        
        current_speaker = speaker
        current_text_block.append(text)
    
    # Add final block
    if current_text_block:
        full_text = ' '.join(current_text_block)
        formatted_transcript.append(f"\n**{current_speaker}:**\n{full_text}\n")
    
    return ''.join(formatted_transcript)

def create_structured_transcript(transcript_entries):
    """Create a structured transcript with timestamps"""
    structured_content = []
    
    structured_content.append("# GCAP3226 Week 4 Lecture Transcript")
    structured_content.append("## Simulation Methods in Public Administration")
    structured_content.append(f"**Date:** September 20, 2025")
    structured_content.append(f"**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    structured_content.append(f"**Total Entries:** {len(transcript_entries)}")
    structured_content.append("\n---\n")
    
    # Group by speaker and time segments
    structured_content.append("## Lecture Content\n")
    
    current_speaker = None
    segment_count = 0
    
    for i, entry in enumerate(transcript_entries):
        speaker = entry['speaker']
        text = entry['text']
        start_time = entry['start_time']
        
        # Start new section for speaker changes or every 10 entries
        if current_speaker != speaker or i % 10 == 0:
            segment_count += 1
            structured_content.append(f"\n### Segment {segment_count} - {speaker} ({start_time})\n")
            current_speaker = speaker
        
        # Add text with timestamp reference
        structured_content.append(f"[{start_time}] {text}\n")
    
    return '\n'.join(structured_content)

def main():
    """Main processing function"""
    # File paths
    vtt_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/01_course_content/week04_simulation/lectures/week4.vtt"
    
    # Output file paths
    clean_transcript_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/01_course_content/week04_simulation/lectures/GCAP3226_week4_lecture_transcript_clean.md"
    structured_transcript_file = "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/01_course_content/week04_simulation/lectures/GCAP3226_week4_lecture_transcript_structured.md"
    
    print("🔄 Processing VTT transcript file...")
    
    # Parse VTT file
    transcript_entries = parse_vtt_file(vtt_file)
    print(f"✅ Parsed {len(transcript_entries)} transcript entries")
    
    # Create clean transcript
    clean_transcript = format_transcript(transcript_entries)
    with open(clean_transcript_file, 'w', encoding='utf-8') as f:
        f.write("# GCAP3226 Week 4 Lecture Transcript (Clean Version)\n")
        f.write("## Simulation Methods in Public Administration\n\n")
        f.write(f"**Date:** September 20, 2025\n")
        f.write(f"**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n")
        f.write(clean_transcript)
    
    print(f"✅ Created clean transcript: {clean_transcript_file}")
    
    # Create structured transcript
    structured_transcript = create_structured_transcript(transcript_entries)
    with open(structured_transcript_file, 'w', encoding='utf-8') as f:
        f.write(structured_transcript)
    
    print(f"✅ Created structured transcript: {structured_transcript_file}")
    
    # Create summary
    total_duration = transcript_entries[-1]['end_time'] if transcript_entries else "Unknown"
    speakers = set(entry['speaker'] for entry in transcript_entries)
    
    print("\n📊 Processing Summary:")
    print(f"   • Total transcript entries: {len(transcript_entries)}")
    print(f"   • Speakers identified: {len(speakers)}")
    print(f"   • Speaker names: {', '.join(sorted(speakers))}")
    print(f"   • Lecture duration: {total_duration}")
    print(f"   • Output files created in: week04_simulation/lectures/")

if __name__ == "__main__":
    main()
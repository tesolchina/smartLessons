#!/usr/bin/env python3
"""
VTT File Cleaner
This script removes timestamps, sequence numbers, and cleans up a VTT file
to produce clean transcript text.
"""

import re
import os

def clean_vtt_file(input_file, output_file):
    """
    Clean VTT file by removing timestamps and formatting
    
    Args:
        input_file (str): Path to input VTT file
        output_file (str): Path to output cleaned text file
    """
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip WEBVTT header
            if line == 'WEBVTT':
                continue
            
            # Skip sequence numbers (just digits)
            if line.isdigit():
                continue
            
            # Skip timestamp lines (contain -->)
            if '-->' in line:
                continue
            
            # Skip lines that are just timestamps (like "00:00:00.710")
            if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}$', line):
                continue
            
            # Clean up speaker labels and add the text
            if ':' in line and len(line) > 10:  # Likely contains speaker label
                # Remove speaker name at the beginning (everything before first colon)
                text = re.sub(r'^[^:]+:\s*', '', line)
                if text.strip():  # Only add if there's actual text after cleaning
                    cleaned_lines.append(text.strip())
            elif line:  # Any other non-empty line
                cleaned_lines.append(line)
        
        # Join all lines with spaces and clean up multiple spaces
        cleaned_text = ' '.join(cleaned_lines)
        
        # Clean up multiple spaces and normalize whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        # Split into sentences for better readability (optional)
        sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)
        
        # Write cleaned text to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for sentence in sentences:
                if sentence.strip():
                    f.write(sentence.strip() + '\n')
        
        print(f"✅ Successfully cleaned VTT file!")
        print(f"📁 Input: {input_file}")
        print(f"📁 Output: {output_file}")
        print(f"📊 Original lines: {len(lines)}")
        print(f"📊 Cleaned sentences: {len([s for s in sentences if s.strip()])}")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find file '{input_file}'")
    except Exception as e:
        print(f"❌ Error processing file: {e}")

def main():
    """Main function to run the VTT cleaner"""
    
    # File paths
    input_file = "c:/usage/VibeCoding/DailyAssistant/DailyAssistant/projects/GCAP3226/course_materials/Week2/week2.vtt"
    output_file = "c:/usage/VibeCoding/DailyAssistant/DailyAssistant/projects/GCAP3226/course_materials/Week2/week2_cleaned.txt"
    
    print("🧹 VTT File Cleaner")
    print("=" * 50)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return
    
    # Clean the VTT file
    clean_vtt_file(input_file, output_file)

if __name__ == "__main__":
    main()

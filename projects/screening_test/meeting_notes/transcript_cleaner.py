#!/usr/bin/env python3
"""
VTT Transcript Cleaner

This script processes VTT transcript files to:
1. Remove timestamps and speaker labels
2. Organize content into logical paragraphs
3. Fix minor spelling and grammatical errors
4. Output clean markdown format

Usage: python transcript_cleaner.py input.vtt output.md
"""

import re
import sys
from pathlib import Path


class TranscriptCleaner:
    def __init__(self):
        # Common spelling corrections specific to this transcript
        self.spelling_corrections = {
            'MVPI': 'MBTI',
            'testPLatform': 'test platform',
            'blah blah blah blah': '[details]',
            'dis…': 'distinguish',
            'kind of differentiate': 'differentiate',
            'right?': 'right?',
            'okay?': 'okay?',
            'you know,': 'you know',
            'I mean,': 'I mean',
            'like,': 'like',
        }
        
        # Patterns for sentence ending detection
        self.sentence_endings = re.compile(r'[.!?]\s+')
        
        # Words that indicate topic changes for paragraph breaks
        self.topic_change_indicators = [
            'now', 'another thing', 'but then', 'okay so', 'alright so',
            'yeah so', 'so actually', 'and also', 'but anyway',
            'moving on', 'next', 'another', 'however', 'meanwhile'
        ]

    def read_vtt_file(self, file_path):
        """Read VTT file and extract transcript text."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def extract_transcript_text(self, vtt_content):
        """Extract only the spoken text from VTT format."""
        lines = vtt_content.split('\n')
        transcript_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip VTT header, empty lines, timestamps, and sequence numbers
            if (line == 'WEBVTT' or 
                not line or 
                line.isdigit() or 
                '-->' in line):
                continue
            
            # Extract text after speaker label (format: "Speaker Name: text")
            if ':' in line and any(name in line for name in ['Simon Wang:', 'Speaker:']):
                # Find the first colon and take everything after it
                colon_index = line.find(':')
                if colon_index != -1:
                    text = line[colon_index + 1:].strip()
                    if text:  # Only add non-empty text
                        transcript_lines.append(text)
            else:
                # If no speaker label found, treat as continuation
                if line:
                    transcript_lines.append(line)
        
        return transcript_lines

    def clean_text(self, text):
        """Clean up spelling and grammatical errors."""
        # Apply spelling corrections
        for wrong, correct in self.spelling_corrections.items():
            text = text.replace(wrong, correct)
        
        # Fix common grammar issues
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
        text = re.sub(r'\.{2,}', '...', text)  # Multiple dots to ellipsis
        text = re.sub(r',\s*,', ',', text)  # Double commas
        text = re.sub(r'\s+([,.!?])', r'\1', text)  # Space before punctuation
        text = re.sub(r'([,.!?])([A-Za-z])', r'\1 \2', text)  # Missing space after punctuation
        
        # Fix sentence capitalization
        sentences = self.sentence_endings.split(text)
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # Capitalize first letter of sentence
                sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
                cleaned_sentences.append(sentence)
        
        return '. '.join(cleaned_sentences) if cleaned_sentences else text

    def create_paragraphs(self, transcript_lines):
        """Organize transcript lines into logical paragraphs."""
        if not transcript_lines:
            return []
        
        paragraphs = []
        current_paragraph = []
        
        for line in transcript_lines:
            cleaned_line = self.clean_text(line)
            
            # Check if this line indicates a topic change
            line_lower = cleaned_line.lower()
            is_topic_change = any(indicator in line_lower for indicator in self.topic_change_indicators)
            
            # Start new paragraph if topic change detected and current paragraph exists
            if is_topic_change and current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = [cleaned_line]
            else:
                current_paragraph.append(cleaned_line)
            
            # Also break paragraph if it gets too long (more than 5 sentences)
            if len(current_paragraph) > 5:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        
        # Add remaining content as final paragraph
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
        
        return paragraphs

    def format_as_markdown(self, paragraphs, original_filename):
        """Format cleaned paragraphs as markdown."""
        if not paragraphs:
            return "# Transcript\n\nNo content found."
        
        # Create title from filename
        title = original_filename.replace('.vtt', '').replace('_', ' ').replace('-', ' ').title()
        
        markdown_content = [
            f"# Clean Transcript: {title}",
            "",
            "*Note: This transcript has been cleaned for readability. Timestamps and speaker labels have been removed, and minor spelling/grammatical errors have been corrected while preserving the original content and meaning.*",
            "",
            "---",
            ""
        ]
        
        # Add paragraphs
        for i, paragraph in enumerate(paragraphs, 1):
            if paragraph.strip():
                markdown_content.append(paragraph.strip())
                markdown_content.append("")  # Empty line between paragraphs
        
        return '\n'.join(markdown_content)

    def process_transcript(self, input_path, output_path):
        """Main processing function."""
        try:
            # Read VTT file
            vtt_content = self.read_vtt_file(input_path)
            
            # Extract transcript text
            transcript_lines = self.extract_transcript_text(vtt_content)
            
            if not transcript_lines:
                print("Warning: No transcript content found in the file.")
                return False
            
            # Create paragraphs
            paragraphs = self.create_paragraphs(transcript_lines)
            
            # Format as markdown
            markdown_content = self.format_as_markdown(paragraphs, Path(input_path).name)
            
            # Write output file
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(markdown_content)
            
            print(f"Successfully processed transcript:")
            print(f"  Input:  {input_path}")
            print(f"  Output: {output_path}")
            print(f"  Paragraphs created: {len(paragraphs)}")
            
            return True
            
        except Exception as e:
            print(f"Error processing transcript: {e}")
            return False


def main():
    """Main function to run the transcript cleaner."""
    if len(sys.argv) != 3:
        print("Usage: python transcript_cleaner.py input.vtt output.md")
        print("Example: python transcript_cleaner.py transcript.vtt clean_transcript.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    # Create cleaner and process
    cleaner = TranscriptCleaner()
    success = cleaner.process_transcript(input_file, output_file)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
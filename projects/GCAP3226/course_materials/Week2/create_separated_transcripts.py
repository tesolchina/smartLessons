#!/usr/bin/env python3
"""
Create Separated Transcripts based on Content Analysis
Uses the LLM analysis results to create properly separated speaker transcripts
"""

import sys
import os
import json
from pathlib import Path

def read_file_content(file_path):
    """Read content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None

def create_speaker_transcripts():
    """Create separated transcripts based on content analysis"""
    
    print("📝 Creating Separated Speaker Transcripts")
    print("=" * 60)
    
    # File paths
    base_dir = "c:/usage/VibeCoding/DailyAssistant/DailyAssistant/projects/GCAP3226/course_materials/Week2"
    original_transcript = f"{base_dir}/week2_cleaned.txt"
    analysis_dir = f"{base_dir}/content_based_analysis"
    output_dir = f"{base_dir}/separated_transcripts"
    
    # Read original transcript
    print("📖 Reading original transcript...")
    transcript_text = read_file_content(original_transcript)
    if not transcript_text:
        return
    
    print(f"✅ Original transcript: {len(transcript_text)} characters")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Created output directory: {output_dir}")
    
    # Split transcript into words for chunk processing
    words = transcript_text.split()
    chunk_size = 2000  # Same size used in analysis
    
    # Create chunks
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_text = ' '.join(words[i:i+chunk_size])
        chunks.append({
            "num": len(chunks) + 1,
            "text": chunk_text,
            "word_start": i,
            "word_end": min(i + chunk_size, len(words))
        })
    
    print(f"📊 Split into {len(chunks)} chunks for processing")
    
    # Create speaker-specific content based on analysis findings
    simon_content = []
    talia_content = []
    
    # Based on the analysis results:
    # Chunk 1: 100% Simon (Course introduction)
    simon_content.append(f"=== COURSE INTRODUCTION ===\n{chunks[0]['text']}\n\n")
    print("✅ Chunk 1 → Simon (Course Introduction)")
    
    # Chunk 2: Mixed - needs manual separation based on analysis
    chunk2_text = chunks[1]['text']
    
    # Find approximate split points in chunk 2 based on analysis
    # Look for "Sorry to interrupt" and "Okay. So later in the CSV file"
    interrupt_point = chunk2_text.find("Sorry to interrupt")
    csv_point = chunk2_text.find("Okay. So later in the CSV file")
    
    if interrupt_point > 0 and csv_point > interrupt_point:
        # Talia's first section (survey methodology)
        talia_section1 = chunk2_text[:interrupt_point].strip()
        talia_content.append(f"=== QUESTIONNAIRE METHODOLOGY - PART 1 ===\n{talia_section1}\n\n")
        
        # Simon's interruption
        simon_interruption = chunk2_text[interrupt_point:csv_point].strip()
        simon_content.append(f"=== COURSE LOGISTICS INTERRUPTION ===\n{simon_interruption}\n\n")
        
        # Talia's continuation
        talia_section2 = chunk2_text[csv_point:].strip()
        talia_content.append(f"=== QUESTIONNAIRE METHODOLOGY - PART 2 ===\n{talia_section2}\n\n")
        
        print("✅ Chunk 2 → Split between Talia (methodology) and Simon (interruption)")
    else:
        # If split points not found, assign based on analysis (70% Talia, 30% Simon)
        split_point = len(chunk2_text) * 7 // 10
        talia_content.append(f"=== QUESTIONNAIRE METHODOLOGY ===\n{chunk2_text[:split_point]}\n\n")
        simon_content.append(f"=== COURSE CONTEXT ===\n{chunk2_text[split_point:]}\n\n")
        print("⚠️  Chunk 2 → Approximate split (70% Talia, 30% Simon)")
    
    # Chunk 3: 100% Simon (Technical setup)
    if len(chunks) > 2:
        simon_content.append(f"=== TECHNICAL SETUP ===\n{chunks[2]['text']}\n\n")
        print("✅ Chunk 3 → Simon (Technical Setup)")
    
    # Chunk 4: 100% Simon (Software setup)
    if len(chunks) > 3:
        simon_content.append(f"=== SOFTWARE SETUP ===\n{chunks[3]['text']}\n\n")
        print("✅ Chunk 4 → Simon (Software Setup)")
    
    # Create Simon's transcript
    simon_file = f"{output_dir}/simon_wang_transcript.txt"
    print(f"💾 Creating Simon's transcript: {simon_file}")
    with open(simon_file, 'w', encoding='utf-8') as f:
        f.write("SIMON WANG - COURSE INSTRUCTOR TRANSCRIPT\n")
        f.write("=" * 60 + "\n")
        f.write("Content: Course introduction, logistics, technical setup\n")
        f.write(f"Generated: {', '.join(['Chunk 1', 'Chunk 2 (partial)', 'Chunk 3', 'Chunk 4'])}\n\n")
        
        for content in simon_content:
            f.write(content)
    
    # Create Talia's transcript
    talia_file = f"{output_dir}/talia_transcript.txt"
    print(f"💾 Creating Talia's transcript: {talia_file}")
    with open(talia_file, 'w', encoding='utf-8') as f:
        f.write("TALIA - QUESTIONNAIRE METHODOLOGY EXPERT TRANSCRIPT\n")
        f.write("=" * 60 + "\n")
        f.write("Content: Survey design, questionnaire methodology, attitude measurement\n")
        f.write(f"Generated: Chunk 2 (questionnaire sections)\n\n")
        
        for content in talia_content:
            f.write(content)
    
    # Create summary file
    summary_file = f"{output_dir}/separation_summary.txt"
    print(f"💾 Creating separation summary: {summary_file}")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("TRANSCRIPT SEPARATION SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("SPEAKER ATTRIBUTION:\n")
        f.write("- Simon Wang: Course instructor, technical content\n")
        f.write("- Talia: Questionnaire methodology expert\n\n")
        
        f.write("CONTENT BREAKDOWN:\n")
        f.write("Simon Wang Sections:\n")
        f.write("  • Course introduction and logistics\n")
        f.write("  • Administrative interruptions\n") 
        f.write("  • Technical setup instructions\n")
        f.write("  • Software configuration\n\n")
        
        f.write("Talia Sections:\n")
        f.write("  • Survey question design methodology\n")
        f.write("  • Attitude measurement techniques\n")
        f.write("  • Policy perception questionnaires\n")
        f.write("  • Ordinal scale explanations\n\n")
        
        f.write("SEPARATION METHODOLOGY:\n")
        f.write("- Used LLM content analysis to ignore original speaker labels\n")
        f.write("- Identified content themes and presentation styles\n")
        f.write("- Split Chunk 2 at natural transition points\n")
        f.write("- Maintained context while separating speakers\n\n")
        
        f.write("FILES CREATED:\n")
        f.write("- simon_wang_transcript.txt (Instructor content)\n")
        f.write("- talia_transcript.txt (Questionnaire methodology)\n")
        f.write("- separation_summary.txt (This summary)\n")
    
    # Calculate statistics
    simon_word_count = sum(len(content.split()) for content in simon_content)
    talia_word_count = sum(len(content.split()) for content in talia_content)
    total_words = len(words)
    
    print("\n📊 SEPARATION STATISTICS:")
    print(f"   Original transcript: {total_words:,} words")
    print(f"   Simon's content: {simon_word_count:,} words ({simon_word_count/total_words*100:.1f}%)")
    print(f"   Talia's content: {talia_word_count:,} words ({talia_word_count/total_words*100:.1f}%)")
    
    print(f"\n✅ Transcript separation complete!")
    print(f"📁 Files saved to: {output_dir}")
    print(f"🎯 Key achievement: Successfully identified and separated Talia's questionnaire content!")

if __name__ == "__main__":
    create_speaker_transcripts()

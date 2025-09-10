#!/usr/bin/env python3
"""
LLM-based Speaker Separation for VTT Transcript
Uses OpenRouter API to intelligently identify speaker changes and separate content.
"""

import sys
import os
import json
from pathlib import Path

# Add the modules path to import openRouterAI
modules_path = Path(__file__).resolve().parent.parent.parent.parent.parent / "modules"
sys.path.insert(0, str(modules_path))

print(f"🔧 Added to Python path: {modules_path}")
print(f"🔧 Path exists: {modules_path.exists()}")

try:
    from openRouterAI.client import post_chat_completions
    print("✅ Successfully imported openRouterAI.client")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"🔍 Available paths: {sys.path[:3]}...")
    sys.exit(1)

def read_transcript(file_path):
    """Read the cleaned transcript file"""
    print(f"📂 Attempting to read transcript from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"✅ Successfully read transcript: {len(content)} characters")
            return content
    except FileNotFoundError:
        print(f"❌ Error: Could not find file '{file_path}'")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def analyze_speakers_with_llm(transcript_text):
    """
    Use LLM to analyze transcript and identify speaker changes
    """
    
    print("🤖 Preparing LLM analysis request...")
    print(f"📊 Transcript sample length: {len(transcript_text[:8000])} characters")
    
    prompt = f"""
Please analyze this academic lecture transcript and identify speaker changes. Based on the context, there are likely two main speakers:

1. **Simon Wang** - The main instructor who introduces the course and provides context
2. **Talia** - A second speaker who talks specifically about a questionnaire/survey

Please:
1. Identify where speaker changes occur in the transcript
2. Separate the content by speaker
3. Pay special attention to the section about the questionnaire/survey methodology - this is likely Talia's part
4. Note any interruptions where Simon explains things during Talia's presentation
5. Format the output as clearly separated sections

Here is the transcript:

---
{transcript_text[:8000]}...

[Note: This is a truncated version for analysis. The full transcript contains discussion of course materials, data visualization, and a detailed explanation of a Hong Kong waste management policy questionnaire.]

Please provide your analysis in the following format:

**ANALYSIS:**
- Brief description of speaker change patterns you identified
- Key topics covered by each speaker

**SEPARATED CONTENT:**

**SPEAKER 1: [Name]**
[Content from speaker 1]

**SPEAKER 2: [Name]**  
[Content from speaker 2]

**MIXED SECTIONS/INTERRUPTIONS:**
[Any sections where speakers alternate or interrupt]
"""

    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 4000,
        "temperature": 0.1
    }
    
    print("📡 Sending request to OpenRouter API...")
    try:
        response = post_chat_completions(payload)
        print("✅ Received response from OpenRouter API")
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Error calling OpenRouter API: {e}")
        return None

def analyze_full_transcript_sections(transcript_text):
    """
    Analyze the full transcript by sending it in sections to identify the questionnaire part
    """
    
    print("📋 Preparing transcript for chunk-based analysis...")
    
    # Split transcript into manageable chunks
    words = transcript_text.split()
    chunk_size = 1500  # words per chunk
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    
    print(f"📊 Split transcript into {len(chunks)} chunks of ~{chunk_size} words each")
    
    prompt_template = """
Analyze this section of an academic lecture transcript. Look for:

1. **Speaker transitions** - When does the speaker change from Simon Wang to someone else (likely Talia)?
2. **Questionnaire discussion** - Which parts discuss survey methodology, questionnaire design, or data collection?
3. **Context clues** - References to "Talia", "questionnaire", "survey", "data visualization"

For this chunk, identify:
- Primary speaker
- Main topics discussed  
- Any speaker change indicators
- Relevance to questionnaire/survey discussion (HIGH/MEDIUM/LOW)

Chunk {chunk_num}/{total_chunks}:
---
{chunk_text}
---

Respond with:
**SPEAKER:** [Primary speaker name or "MIXED" if multiple]
**TOPICS:** [Main topics in this section]
**QUESTIONNAIRE_RELEVANCE:** [HIGH/MEDIUM/LOW]
**SPEAKER_CHANGES:** [Any transitions noted]
**KEY_QUOTES:** [Important phrases that indicate speaker or topic changes]
"""

    chunk_analyses = []
    
    for i, chunk in enumerate(chunks):
        prompt = prompt_template.format(
            chunk_num=i+1,
            total_chunks=len(chunks),
            chunk_text=chunk[:3000]  # Limit chunk size for API
        )
        
        payload = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.1
        }
        
        try:
            print(f"🔍 Analyzing chunk {i+1}/{len(chunks)}... ({len(chunk.split())} words)")
            response = post_chat_completions(payload)
            analysis = response["choices"][0]["message"]["content"]
            print(f"✅ Chunk {i+1} analysis complete")
            chunk_analyses.append({
                "chunk_num": i+1,
                "analysis": analysis,
                "text": chunk
            })
        except Exception as e:
            print(f"❌ Error analyzing chunk {i+1}: {e}")
            chunk_analyses.append({
                "chunk_num": i+1,
                "analysis": f"Error: {e}",
                "text": chunk
            })
    
    return chunk_analyses

def create_separated_transcript(chunk_analyses, original_transcript):
    """
    Create separated transcript based on chunk analysis
    """
    
    print("🧠 Creating synthesis from chunk analyses...")
    print(f"📊 Synthesizing {len(chunk_analyses)} chunk analyses")
    
    # Synthesize the analysis
    synthesis_prompt = f"""
Based on the following chunk-by-chunk analysis of a lecture transcript, create a final speaker-separated version.

The lecture appears to have:
1. Simon Wang - main instructor 
2. Talia - who discusses questionnaire methodology
3. Possible interruptions where Simon explains things during Talia's presentation

Here are the analyses:

{json.dumps([{"chunk": a["chunk_num"], "analysis": a["analysis"]} for a in chunk_analyses], indent=2)}

Please provide:

**FINAL SPEAKER SEPARATION PLAN:**
- Which chunks belong to which speaker
- Identification of the questionnaire discussion section
- Any mixed/interruption sections

**SEPARATED CONTENT:**

**SIMON WANG SECTIONS:**
[List chunk numbers and brief description]

**TALIA SECTIONS (QUESTIONNAIRE DISCUSSION):**
[List chunk numbers and brief description] 

**MIXED/INTERRUPTION SECTIONS:**
[List chunk numbers and brief description]
"""

    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [{"role": "user", "content": synthesis_prompt}],
        "max_tokens": 2000,
        "temperature": 0.1
    }
    
    print("📡 Sending synthesis request to OpenRouter API...")
    try:
        response = post_chat_completions(payload)
        print("✅ Synthesis complete")
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Error creating synthesis: {e}")
        return None

def save_analysis_results(chunk_analyses, synthesis, output_dir):
    """Save all analysis results to files"""
    
    print(f"💾 Creating output directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save detailed chunk analysis
    chunk_file = f"{output_dir}/chunk_analysis.json"
    print(f"💾 Saving chunk analysis to: {chunk_file}")
    with open(chunk_file, 'w', encoding='utf-8') as f:
        json.dump(chunk_analyses, f, indent=2, ensure_ascii=False)
    
    # Save synthesis
    if synthesis:
        synthesis_file = f"{output_dir}/speaker_separation_analysis.txt"
        print(f"💾 Saving synthesis to: {synthesis_file}")
        with open(synthesis_file, 'w', encoding='utf-8') as f:
            f.write(synthesis)
    
    # Create a readable summary
    summary_file = f"{output_dir}/analysis_summary.txt"
    print(f"💾 Saving readable summary to: {summary_file}")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("SPEAKER SEPARATION ANALYSIS SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        
        for analysis in chunk_analyses:
            f.write(f"CHUNK {analysis['chunk_num']}:\n")
            f.write(f"{analysis['analysis']}\n")
            f.write("-" * 30 + "\n\n")
        
        if synthesis:
            f.write("\nFINAL SYNTHESIS:\n")
            f.write("=" * 20 + "\n")
            f.write(synthesis)
    
    print("✅ All analysis files saved successfully")

def main():
    """Main function"""
    
    # File paths
    transcript_file = "c:/usage/VibeCoding/DailyAssistant/DailyAssistant/projects/GCAP3226/course_materials/Week2/week2_cleaned.txt"
    output_dir = "c:/usage/VibeCoding/DailyAssistant/DailyAssistant/projects/GCAP3226/course_materials/Week2/speaker_analysis"
    
    print("🤖 LLM-based Speaker Separation Analysis")
    print("=" * 60)
    
    # Read transcript
    print("📖 Reading transcript...")
    transcript = read_transcript(transcript_file)
    if not transcript:
        return
    
    print(f"📊 Transcript length: {len(transcript)} characters, {len(transcript.split())} words")
    
    # Analyze transcript in chunks
    print("🔍 Analyzing transcript with LLM...")
    chunk_analyses = analyze_full_transcript_sections(transcript)
    
    # Create synthesis
    print("🧠 Creating final synthesis...")
    synthesis = create_separated_transcript(chunk_analyses, transcript)
    
    # Save results
    print("💾 Saving analysis results...")
    save_analysis_results(chunk_analyses, synthesis, output_dir)
    
    print(f"✅ Analysis complete!")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📝 Check the following files:")
    print(f"   - chunk_analysis.json (detailed analysis)")
    print(f"   - speaker_separation_analysis.txt (final synthesis)")
    print(f"   - analysis_summary.txt (readable summary)")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Content-based Speaker Separation for VTT Transcript
Ignores speaker labels and identifies content that should be attributed to different speakers
based on topic analysis, specifically focusing on questionnaire methodology sections.
"""

import sys
import os
import json
from pathlib import Path

# Add the modules path
modules_path = Path(__file__).resolve().parent.parent.parent.parent.parent / "modules"
sys.path.insert(0, str(modules_path))

print(f"🔧 Added to Python path: {modules_path}")
print(f"🔧 Path exists: {modules_path.exists()}")

try:
    from openRouterAI.client import post_chat_completions
    print("✅ Successfully imported openRouterAI.client")
except ImportError as e:
    print(f"❌ Import error: {e}")
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

def analyze_content_for_speakers(transcript_text):
    """
    Analyze transcript content to identify sections that should be attributed to different speakers
    based on topic and presentation style, ignoring existing speaker labels
    """
    
    print("🤖 Analyzing content to identify speaker attribution based on topics...")
    print(f"📊 Full transcript length: {len(transcript_text)} characters")
    
    # Split transcript into manageable chunks for analysis
    words = transcript_text.split()
    chunk_size = 2000  # Larger chunks for better context
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    
    print(f"📊 Split transcript into {len(chunks)} chunks of ~{chunk_size} words each")
    
    chunk_analyses = []
    
    for i, chunk in enumerate(chunks):
        print(f"🔍 Analyzing chunk {i+1}/{len(chunks)} for content attribution... ({len(chunk.split())} words)")
        
        prompt = f"""
IGNORE ALL EXISTING SPEAKER LABELS. Analyze this academic lecture content to determine who should be presenting each section based on topic and presentation style.

Context: This is from a course lecture that should have two main presenters:
1. **Simon Wang** - The main instructor (course logistics, general teaching)
2. **Talia** - A guest presenter who should be discussing questionnaire methodology and survey research

Your task: Determine which sections should be attributed to which speaker based on CONTENT ANALYSIS, not existing labels.

Look for these indicators:

**SIMON WANG indicators:**
- Course administration and logistics
- General programming/technical setup
- Course introduction and structure
- References to "this course", "our course"
- Instructor-style explanations

**TALIA indicators:**
- Detailed questionnaire methodology discussion
- Survey design principles and best practices
- Research methodology explanations
- Statistical analysis of survey data
- Academic research presentation style
- Discussion of specific research studies or data collection methods

**CONTENT TO ANALYZE (Chunk {i+1}/{len(chunks)}):**
---
{chunk[:4000]}
---

Provide your analysis in this format:

**PRIMARY_ATTRIBUTION:** [SIMON_WANG/TALIA/MIXED]

**CONTENT_BREAKDOWN:**
- [Percentage or description of content that should be Simon's]
- [Percentage or description of content that should be Talia's]

**KEY_INDICATORS:**
- [Specific phrases/topics that indicate Simon's content]
- [Specific phrases/topics that indicate Talia's content]

**QUESTIONNAIRE_RELEVANCE:** [HIGH/MEDIUM/LOW/NONE]

**RECOMMENDED_SPEAKER_TRANSITIONS:**
[If this chunk should have speaker changes, indicate where and why]

**CONFIDENCE_LEVEL:** [HIGH/MEDIUM/LOW] - How confident you are in this attribution
"""

        payload = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1200,
            "temperature": 0.1
        }
        
        try:
            response = post_chat_completions(payload)
            analysis = response["choices"][0]["message"]["content"]
            print(f"✅ Chunk {i+1} content analysis complete")
            
            chunk_analyses.append({
                "chunk_num": i+1,
                "analysis": analysis,
                "text": chunk[:1000] + "..." if len(chunk) > 1000 else chunk  # Store truncated text
            })
        except Exception as e:
            print(f"❌ Error analyzing chunk {i+1}: {e}")
            chunk_analyses.append({
                "chunk_num": i+1,
                "analysis": f"Error: {e}",
                "text": chunk[:1000] + "..." if len(chunk) > 1000 else chunk
            })
    
    return chunk_analyses

def create_content_based_separation(chunk_analyses, original_transcript):
    """
    Create final speaker separation based on content analysis
    """
    
    print("🧠 Creating content-based speaker separation...")
    print(f"📊 Synthesizing {len(chunk_analyses)} content analyses")
    
    synthesis_prompt = f"""
Based on the detailed content analysis of each chunk, create a comprehensive speaker separation plan that ignores original speaker labels and focuses on content attribution.

ANALYSIS RESULTS:
{json.dumps([{"chunk": a["chunk_num"], "analysis": a["analysis"]} for a in chunk_analyses], indent=2)}

Create a final separation plan with:

1. **CONTENT-BASED SPEAKER ATTRIBUTION:**
   - Which chunks or sections should be attributed to Simon Wang
   - Which chunks or sections should be attributed to Talia
   - Any mixed sections that need manual separation

2. **QUESTIONNAIRE METHODOLOGY SECTIONS:**
   - Specifically identify all content related to questionnaire design, survey methodology, and research practices
   - These sections should likely be attributed to Talia regardless of original speaker labels

3. **TRANSITION POINTS:**
   - Identify natural points where speaker transitions should occur
   - Suggest where handoffs between Simon and Talia would make sense

4. **FINAL RECOMMENDATIONS:**
   - Confidence level in the separation
   - Any sections that need manual review
   - Suggested approach for creating separated transcripts

Format your response with clear sections and actionable recommendations.
"""

    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [{"role": "user", "content": synthesis_prompt}],
        "max_tokens": 2500,
        "temperature": 0.1
    }
    
    print("📡 Sending content synthesis request to OpenRouter API...")
    try:
        response = post_chat_completions(payload)
        print("✅ Content-based synthesis complete")
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Error creating content synthesis: {e}")
        return None

def extract_talia_sections(chunk_analyses, synthesis, original_transcript):
    """
    Extract and create separate files for content that should be attributed to Talia
    """
    
    print("📝 Extracting Talia's content sections...")
    
    # Analyze which chunks are high-confidence Talia content
    talia_chunks = []
    mixed_chunks = []
    
    for analysis in chunk_analyses:
        analysis_text = analysis["analysis"].lower()
        if "talia" in analysis_text and ("high" in analysis_text or "questionnaire_relevance: high" in analysis_text):
            talia_chunks.append(analysis)
        elif "mixed" in analysis_text or "talia" in analysis_text:
            mixed_chunks.append(analysis)
    
    print(f"🎯 Found {len(talia_chunks)} high-confidence Talia chunks")
    print(f"🤔 Found {len(mixed_chunks)} mixed/uncertain chunks")
    
    return talia_chunks, mixed_chunks

def save_content_analysis_results(chunk_analyses, synthesis, talia_chunks, mixed_chunks, output_dir):
    """Save all content analysis results to files"""
    
    print(f"💾 Creating output directory: {output_dir}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save detailed chunk analysis
    chunk_file = f"{output_dir}/content_analysis.json"
    print(f"💾 Saving content analysis to: {chunk_file}")
    with open(chunk_file, 'w', encoding='utf-8') as f:
        json.dump(chunk_analyses, f, indent=2, ensure_ascii=False)
    
    # Save synthesis
    if synthesis:
        synthesis_file = f"{output_dir}/content_based_separation.txt"
        print(f"💾 Saving content synthesis to: {synthesis_file}")
        with open(synthesis_file, 'w', encoding='utf-8') as f:
            f.write(synthesis)
    
    # Save Talia's content sections
    talia_file = f"{output_dir}/talia_content_sections.txt"
    print(f"💾 Saving Talia's content to: {talia_file}")
    with open(talia_file, 'w', encoding='utf-8') as f:
        f.write("TALIA'S CONTENT SECTIONS\n")
        f.write("=" * 50 + "\n\n")
        f.write("Based on content analysis, these sections should be attributed to Talia:\n\n")
        
        for chunk in talia_chunks:
            f.write(f"CHUNK {chunk['chunk_num']}:\n")
            f.write(f"{chunk['analysis']}\n")
            f.write("-" * 40 + "\n\n")
        
        f.write("\nMIXED/UNCERTAIN SECTIONS:\n")
        f.write("=" * 30 + "\n\n")
        
        for chunk in mixed_chunks:
            f.write(f"CHUNK {chunk['chunk_num']}:\n")
            f.write(f"{chunk['analysis']}\n")
            f.write("-" * 40 + "\n\n")
    
    # Create a readable summary
    summary_file = f"{output_dir}/content_analysis_summary.txt"
    print(f"💾 Saving readable summary to: {summary_file}")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("CONTENT-BASED SPEAKER SEPARATION ANALYSIS\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"ANALYSIS OVERVIEW:\n")
        f.write(f"- Total chunks analyzed: {len(chunk_analyses)}\n")
        f.write(f"- High-confidence Talia sections: {len(talia_chunks)}\n")
        f.write(f"- Mixed/uncertain sections: {len(mixed_chunks)}\n")
        f.write(f"- Simon-attributed sections: {len(chunk_analyses) - len(talia_chunks) - len(mixed_chunks)}\n\n")
        
        for analysis in chunk_analyses:
            f.write(f"CHUNK {analysis['chunk_num']}:\n")
            f.write(f"{analysis['analysis']}\n")
            f.write("-" * 50 + "\n\n")
        
        if synthesis:
            f.write("\nFINAL CONTENT-BASED SYNTHESIS:\n")
            f.write("=" * 40 + "\n")
            f.write(synthesis)
    
    print("✅ All content analysis files saved successfully")

def main():
    """Main function"""
    
    # File paths
    transcript_file = "c:/usage/VibeCoding/DailyAssistant/DailyAssistant/projects/GCAP3226/course_materials/Week2/week2_cleaned.txt"
    output_dir = "c:/usage/VibeCoding/DailyAssistant/DailyAssistant/projects/GCAP3226/course_materials/Week2/content_based_analysis"
    
    print("🎯 Content-Based Speaker Separation Analysis")
    print("=" * 70)
    print("🎯 IGNORING speaker labels - focusing on content attribution")
    print("🎯 Identifying questionnaire content for Talia attribution")
    print()
    
    # Read transcript
    print("📖 Reading transcript...")
    transcript = read_transcript(transcript_file)
    if not transcript:
        return
    
    print(f"📊 Transcript length: {len(transcript)} characters, {len(transcript.split())} words")
    
    # Analyze content for speaker attribution
    print("🔍 Analyzing content for speaker attribution...")
    chunk_analyses = analyze_content_for_speakers(transcript)
    
    # Create content-based synthesis
    print("🧠 Creating content-based separation...")
    synthesis = create_content_based_separation(chunk_analyses, transcript)
    
    # Extract Talia sections
    print("📝 Extracting Talia's content sections...")
    talia_chunks, mixed_chunks = extract_talia_sections(chunk_analyses, synthesis, transcript)
    
    # Save results
    print("💾 Saving content analysis results...")
    save_content_analysis_results(chunk_analyses, synthesis, talia_chunks, mixed_chunks, output_dir)
    
    print(f"✅ Content-based analysis complete!")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📝 Key files created:")
    print(f"   - content_analysis.json (detailed chunk analysis)")
    print(f"   - content_based_separation.txt (final synthesis)")
    print(f"   - talia_content_sections.txt (Talia's attributed content)")
    print(f"   - content_analysis_summary.txt (readable summary)")
    print()
    print("🎯 Next steps:")
    print("   1. Review talia_content_sections.txt for questionnaire content")
    print("   2. Check content_based_separation.txt for transition points")
    print("   3. Use findings to create properly separated transcripts")

if __name__ == "__main__":
    main()

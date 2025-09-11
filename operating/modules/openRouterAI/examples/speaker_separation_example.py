#!/usr/bin/env python3
"""
Speaker Separation Analysis Example

This example demonstrates how to use the LLM Text Analyzer for speaker separation
in transcripts, based on content analysis rather than speaker labels.

Usage:
    python speaker_separation_example.py path/to/transcript.txt output_directory

Features demonstrated:
- Content-based speaker identification
- Topic-driven speaker attribution
- Mixed section handling
- Confidence assessment
- Result compilation and export
"""

import sys
import os
from pathlib import Path

# Add parent directory to import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from llm_text_analyzer import LLMTextAnalyzer

def create_speaker_analysis_prompts(expected_speakers: list = None):
    """
    Create prompts specifically for speaker separation analysis
    
    Args:
        expected_speakers: List of expected speaker descriptions
                          e.g., ["Simon - Main instructor", "Talia - Guest speaker on methodology"]
    """
    
    if expected_speakers is None:
        expected_speakers = ["Primary Speaker", "Secondary Speaker"]
    
    speaker_descriptions = "\\n".join([f"- {speaker}" for speaker in expected_speakers])
    
    analysis_prompt = f"""
CONTENT-BASED SPEAKER IDENTIFICATION

Analyze this transcript chunk to determine speaker attribution based on CONTENT and PRESENTATION STYLE, 
ignoring any existing speaker labels.

Expected speakers in this content:
{speaker_descriptions}

Chunk {{chunk_num}} ({{word_count}} words):
---
{{chunk_text}}
---

Analyze for:

**CONTENT INDICATORS:**
- Topic expertise and knowledge depth
- Teaching vs. presenting vs. discussing styles
- Administrative vs. academic content
- Formal vs. informal language patterns

**SPEAKER ATTRIBUTION:**
- Which speaker(s) should present this content based on expertise
- Confidence level: HIGH/MEDIUM/LOW
- Percentage breakdown if mixed content

**TRANSITION POINTS:**
- Any clear speaker change indicators
- Natural handoff points
- Topic shift markers

**TOPIC CLASSIFICATION:**
- Main subject matter
- Expertise level required
- Presentation context (intro/main/conclusion)

Provide structured analysis with clear attribution recommendations.
"""
    
    synthesis_prompt = f"""
SPEAKER SEPARATION SYNTHESIS

Based on analysis of {{total_chunks}} transcript chunks, create a comprehensive speaker separation plan.

Expected speakers:
{speaker_descriptions}

Chunk analyses:
{{analyses}}

Create a detailed separation strategy:

**1. SPEAKER ATTRIBUTION SUMMARY:**
- Which chunks belong to which speaker
- Confidence levels for each attribution
- Mixed sections requiring manual separation

**2. CONTENT DISTRIBUTION:**
- Topic breakdown by speaker
- Expertise alignment assessment
- Natural flow evaluation

**3. SEPARATION STRATEGY:**
- Recommended chunk boundaries
- Transition point identification  
- Manual review requirements

**4. QUALITY ASSESSMENT:**
- Overall confidence in separation
- Potential issues or ambiguities
- Validation recommendations

**5. IMPLEMENTATION PLAN:**
- Step-by-step separation process
- File organization suggestions
- Quality control checkpoints

Provide actionable recommendations for creating separated transcripts.
"""
    
    return analysis_prompt, synthesis_prompt

def analyze_transcript_for_speakers(transcript_path: str, 
                                  output_dir: str,
                                  expected_speakers: list = None,
                                  model: str = "anthropic/claude-3.5-sonnet"):
    """
    Complete speaker separation analysis workflow
    
    Args:
        transcript_path: Path to transcript file
        output_dir: Output directory for results
        expected_speakers: List of expected speaker descriptions
        model: LLM model to use
    """
    
    print("🎯 Speaker Separation Analysis")
    print("=" * 60)
    
    if expected_speakers:
        print("Expected speakers:")
        for i, speaker in enumerate(expected_speakers, 1):
            print(f"  {i}. {speaker}")
        print()
    
    # Initialize analyzer
    analyzer = LLMTextAnalyzer(model=model, chunk_size=2000)
    
    # Create speaker-specific prompts
    analysis_prompt, synthesis_prompt = create_speaker_analysis_prompts(expected_speakers)
    
    # Run analysis
    results = analyzer.analyze_file(
        file_path=transcript_path,
        analysis_prompt=analysis_prompt,
        synthesis_prompt=synthesis_prompt,
        output_dir=output_dir,
        filename_prefix="speaker_separation"
    )
    
    if results["success"]:
        print("\\n🎯 SPEAKER SEPARATION RESULTS:")
        print(f"📁 All results saved to: {results['output_dir']}")
        print("📝 Key files:")
        print("   - speaker_separation_synthesis.txt (separation plan)")
        print("   - speaker_separation_chunks.json (detailed analysis)")
        print("   - speaker_separation_summary.txt (readable summary)")
        print("\\n💡 Next steps:")
        print("   1. Review the synthesis file for separation strategy")
        print("   2. Check chunk analyses for confidence levels")
        print("   3. Implement recommended separation based on findings")
    
    return results

def create_separated_transcripts_from_analysis(analysis_results: dict, 
                                             original_transcript_path: str,
                                             speaker_names: list):
    """
    Create separated transcript files based on analysis results
    
    Args:
        analysis_results: Results from analyze_transcript_for_speakers
        original_transcript_path: Path to original transcript
        speaker_names: List of speaker names for output files
    """
    
    print("📝 Creating separated transcript files...")
    
    # This would implement the separation logic based on the analysis
    # Similar to what we did in the create_separated_transcripts.py script
    # But using the structured analysis results
    
    print("💡 Implementation note:")
    print("   This function would parse the analysis results and")
    print("   create separated transcript files based on the")
    print("   speaker attribution recommendations from the LLM.")

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) >= 2:
        transcript_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) >= 3 else f"{Path(transcript_path).stem}_speaker_analysis"
        
        # Example with specific speakers
        expected_speakers = [
            "Simon Wang - Course instructor (technical setup, administration)",
            "Talia - Guest expert (questionnaire methodology, research methods)"
        ]
        
        results = analyze_transcript_for_speakers(
            transcript_path=transcript_path,
            output_dir=output_dir,
            expected_speakers=expected_speakers
        )
        
    else:
        print("🧪 Speaker Separation Analysis Example")
        print("=" * 50)
        print()
        print("Usage:")
        print("  python speaker_separation_example.py <transcript_file> [output_dir]")
        print()
        print("Example:")
        print("  python speaker_separation_example.py transcript.txt analysis_output")
        print()
        print("This will:")
        print("  1. Analyze the transcript for speaker patterns")
        print("  2. Identify content-based speaker attribution")  
        print("  3. Create separation recommendations")
        print("  4. Export detailed analysis results")
        print()
        print("📝 The analysis ignores existing speaker labels and focuses")
        print("   on content expertise and presentation style to determine")
        print("   which speaker should present each section.")

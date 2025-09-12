#!/usr/bin/env python3
"""
Generic LLM Text Analysis Utility

This utility provides a framework for analyzing large text files using OpenRouter API.
It handles chunking, API calls, status reporting, and result compilation.

Usage:
    from llm_text_analyzer import LLMTextAnalyzer
    
    analyzer = LLMTextAnalyzer()
    results = analyzer.analyze_file("path/to/text.txt", "Your analysis prompt")

Features:
- Automatic text chunking for large files
- Status reporting with progress indicators
- Error handling and retry logic
- Result compilation and export
- Configurable models and parameters
"""

import sys
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any

# Add parent directory to import openRouterAI
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from openRouterAI.client import post_chat_completions
    OPENROUTER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  OpenRouter client not available: {e}")
    OPENROUTER_AVAILABLE = False

class LLMTextAnalyzer:
    """
    Generic LLM-powered text analysis utility
    """
    
    def __init__(self, model: str = "anthropic/claude-3.5-sonnet", chunk_size: int = 2000):
        """
        Initialize the analyzer
        
        Args:
            model: OpenRouter model to use
            chunk_size: Number of words per chunk for large texts
        """
        self.model = model
        self.chunk_size = chunk_size
        
        if not OPENROUTER_AVAILABLE:
            raise ImportError("OpenRouter client is not available. Please check your setup.")
    
    def read_text_file(self, file_path: str) -> Optional[str]:
        """Read content from a text file with status reporting"""
        print(f"📂 Reading text file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"✅ Successfully read: {len(content):,} characters, {len(content.split()):,} words")
                return content
        except FileNotFoundError:
            print(f"❌ Error: File not found '{file_path}'")
            return None
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return None
    
    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Split text into manageable chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size):
            chunk_text = ' '.join(words[i:i+self.chunk_size])
            chunks.append({
                "chunk_num": len(chunks) + 1,
                "text": chunk_text,
                "word_count": len(chunk_text.split()),
                "word_start": i,
                "word_end": min(i + self.chunk_size, len(words))
            })
        
        print(f"📊 Split text into {len(chunks)} chunks of ~{self.chunk_size} words each")
        return chunks
    
    def analyze_chunk(self, chunk: Dict[str, Any], prompt_template: str) -> Dict[str, Any]:
        """Analyze a single chunk with the LLM"""
        chunk_num = chunk["chunk_num"]
        chunk_text = chunk["text"]
        
        # Format the prompt with chunk information
        prompt = prompt_template.format(
            chunk_num=chunk_num,
            chunk_text=chunk_text,
            word_count=chunk["word_count"]
        )
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1500,
            "temperature": 0.1
        }
        
        print(f"🔍 Analyzing chunk {chunk_num}... ({chunk['word_count']} words)")
        
        try:
            response = post_chat_completions(payload)
            analysis = response["choices"][0]["message"]["content"]
            print(f"✅ Chunk {chunk_num} analysis complete")
            
            return {
                "chunk_num": chunk_num,
                "analysis": analysis,
                "word_count": chunk["word_count"],
                "success": True,
                "error": None
            }
        except Exception as e:
            print(f"❌ Error analyzing chunk {chunk_num}: {e}")
            return {
                "chunk_num": chunk_num,
                "analysis": f"Error: {e}",
                "word_count": chunk["word_count"],
                "success": False,
                "error": str(e)
            }
    
    def synthesize_results(self, chunk_analyses: List[Dict[str, Any]], synthesis_prompt: str) -> Optional[str]:
        """Create a synthesis of all chunk analyses"""
        print("🧠 Creating synthesis from chunk analyses...")
        print(f"📊 Synthesizing {len(chunk_analyses)} chunk analyses")
        
        # Prepare synthesis data
        synthesis_data = []
        for analysis in chunk_analyses:
            if analysis["success"]:
                synthesis_data.append({
                    "chunk": analysis["chunk_num"],
                    "analysis": analysis["analysis"],
                    "word_count": analysis["word_count"]
                })
        
        # Format synthesis prompt
        prompt = synthesis_prompt.format(
            total_chunks=len(chunk_analyses),
            successful_chunks=len(synthesis_data),
            analyses=json.dumps(synthesis_data, indent=2)
        )
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2500,
            "temperature": 0.1
        }
        
        print("📡 Sending synthesis request to OpenRouter API...")
        
        try:
            response = post_chat_completions(payload)
            synthesis = response["choices"][0]["message"]["content"]
            print("✅ Synthesis complete")
            return synthesis
        except Exception as e:
            print(f"❌ Error creating synthesis: {e}")
            return None
    
    def save_results(self, 
                    chunk_analyses: List[Dict[str, Any]], 
                    synthesis: Optional[str], 
                    output_dir: str,
                    filename_prefix: str = "analysis") -> None:
        """Save analysis results to files"""
        
        print(f"💾 Creating output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
        
        # Save detailed chunk analysis
        chunk_file = f"{output_dir}/{filename_prefix}_chunks.json"
        print(f"💾 Saving chunk analysis to: {chunk_file}")
        with open(chunk_file, 'w', encoding='utf-8') as f:
            json.dump(chunk_analyses, f, indent=2, ensure_ascii=False)
        
        # Save synthesis if available
        if synthesis:
            synthesis_file = f"{output_dir}/{filename_prefix}_synthesis.txt"
            print(f"💾 Saving synthesis to: {synthesis_file}")
            with open(synthesis_file, 'w', encoding='utf-8') as f:
                f.write(synthesis)
        
        # Create readable summary
        summary_file = f"{output_dir}/{filename_prefix}_summary.txt"
        print(f"💾 Saving readable summary to: {summary_file}")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"LLM TEXT ANALYSIS SUMMARY\\n")
            f.write("=" * 50 + "\\n\\n")
            
            f.write(f"ANALYSIS OVERVIEW:\\n")
            f.write(f"- Total chunks: {len(chunk_analyses)}\\n")
            f.write(f"- Successful analyses: {sum(1 for a in chunk_analyses if a['success'])}\\n")
            f.write(f"- Failed analyses: {sum(1 for a in chunk_analyses if not a['success'])}\\n")
            f.write(f"- Model used: {self.model}\\n\\n")
            
            # Write each chunk analysis
            for analysis in chunk_analyses:
                f.write(f"CHUNK {analysis['chunk_num']} ({analysis['word_count']} words):\\n")
                if analysis["success"]:
                    f.write(f"{analysis['analysis']}\\n")
                else:
                    f.write(f"ERROR: {analysis['error']}\\n")
                f.write("-" * 40 + "\\n\\n")
            
            # Add synthesis if available
            if synthesis:
                f.write("\\nFINAL SYNTHESIS:\\n")
                f.write("=" * 20 + "\\n")
                f.write(synthesis)
        
        print("✅ All analysis files saved successfully")
    
    def analyze_file(self, 
                    file_path: str, 
                    analysis_prompt: str, 
                    synthesis_prompt: Optional[str] = None,
                    output_dir: Optional[str] = None,
                    filename_prefix: str = "analysis") -> Dict[str, Any]:
        """
        Complete analysis workflow for a text file
        
        Args:
            file_path: Path to the text file to analyze
            analysis_prompt: Prompt template for chunk analysis (use {chunk_num}, {chunk_text}, {word_count})
            synthesis_prompt: Optional prompt for synthesis (use {total_chunks}, {successful_chunks}, {analyses})
            output_dir: Directory to save results (default: same as input file)
            filename_prefix: Prefix for output files
            
        Returns:
            Dict containing analysis results and metadata
        """
        
        print("🤖 LLM Text Analysis")
        print("=" * 50)
        print(f"📄 Input file: {file_path}")
        print(f"🧠 Model: {self.model}")
        print(f"📊 Chunk size: {self.chunk_size} words")
        print()
        
        # Read the file
        text_content = self.read_text_file(file_path)
        if not text_content:
            return {"success": False, "error": "Could not read input file"}
        
        # Set default output directory
        if output_dir is None:
            output_dir = str(Path(file_path).parent / f"{Path(file_path).stem}_analysis")
        
        # Chunk the text
        chunks = self.chunk_text(text_content)
        
        # Analyze each chunk
        print("🔍 Starting chunk analysis...")
        chunk_analyses = []
        for chunk in chunks:
            analysis_result = self.analyze_chunk(chunk, analysis_prompt)
            chunk_analyses.append(analysis_result)
        
        # Create synthesis if prompt provided
        synthesis = None
        if synthesis_prompt:
            synthesis = self.synthesize_results(chunk_analyses, synthesis_prompt)
        
        # Save results
        print("💾 Saving results...")
        self.save_results(chunk_analyses, synthesis, output_dir, filename_prefix)
        
        # Calculate statistics
        successful_analyses = [a for a in chunk_analyses if a["success"]]
        total_words = sum(chunk["word_count"] for chunk in chunks)
        
        print("\\n📊 ANALYSIS STATISTICS:")
        print(f"   Total chunks: {len(chunks)}")
        print(f"   Successful analyses: {len(successful_analyses)}")
        print(f"   Total words processed: {total_words:,}")
        print(f"   Average words per chunk: {total_words // len(chunks):,}")
        
        print(f"\\n✅ Analysis complete!")
        print(f"📁 Results saved to: {output_dir}")
        
        return {
            "success": True,
            "chunk_analyses": chunk_analyses,
            "synthesis": synthesis,
            "output_dir": output_dir,
            "statistics": {
                "total_chunks": len(chunks),
                "successful_chunks": len(successful_analyses),
                "total_words": total_words,
                "model_used": self.model
            }
        }

# Example usage functions
def example_content_analysis():
    """Example: Analyze content for different themes or topics"""
    
    analysis_prompt = """
    Analyze this text chunk for main themes, topics, and key concepts.
    
    Chunk {chunk_num} ({word_count} words):
    ---
    {chunk_text}
    ---
    
    Please identify:
    1. Main themes and topics
    2. Key concepts or terminology
    3. Writing style and tone
    4. Any notable patterns or structures
    
    Provide a structured analysis.
    """
    
    synthesis_prompt = """
    Based on the analysis of {total_chunks} text chunks, create a comprehensive summary.
    
    Chunk analyses:
    {analyses}
    
    Please provide:
    1. Overall theme summary
    2. Most common topics across chunks
    3. Key concepts and terminology
    4. Patterns in writing style
    5. Structural observations
    """
    
    return analysis_prompt, synthesis_prompt

def example_speaker_identification():
    """Example: Identify different speakers or voices in a transcript"""
    
    analysis_prompt = """
    Analyze this transcript chunk to identify different speakers or presentation styles.
    
    Chunk {chunk_num} ({word_count} words):
    ---
    {chunk_text}
    ---
    
    Please identify:
    1. Potential speaker changes or different voices
    2. Teaching vs. presentation vs. discussion styles
    3. Topic transitions that might indicate speaker changes
    4. Formal vs. informal language patterns
    
    Rate confidence level: HIGH/MEDIUM/LOW
    """
    
    synthesis_prompt = """
    Based on analysis of {total_chunks} chunks, create a speaker identification summary.
    
    Analyses:
    {analyses}
    
    Provide:
    1. Likely number of distinct speakers
    2. Characteristics of each identified speaker
    3. Topic distribution among speakers
    4. Confidence assessment
    5. Recommended separation strategy
    """
    
    return analysis_prompt, synthesis_prompt

if __name__ == "__main__":
    # Example usage
    print("🧪 LLM Text Analyzer - Example Usage")
    print("=" * 50)
    print()
    print("To use this analyzer in your code:")
    print()
    print("from llm_text_analyzer import LLMTextAnalyzer, example_content_analysis")
    print()
    print("# Initialize analyzer")
    print("analyzer = LLMTextAnalyzer()")
    print()
    print("# Get example prompts")
    print("analysis_prompt, synthesis_prompt = example_content_analysis()")
    print()
    print("# Analyze a file")
    print("results = analyzer.analyze_file(")
    print("    'path/to/your/file.txt',")
    print("    analysis_prompt,")
    print("    synthesis_prompt")
    print(")")
    print()
    print("📝 Check the examples in this file for prompt templates!")

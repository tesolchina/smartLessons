#!/usr/bin/env python3
"""
Data Analysis Script for Zotero MD Files
Analyzes the structure and content of academic papers to inform RAG system design.
"""

import os
import re
from pathlib import Path
import logging
from collections import defaultdict, Counter

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_md_files(data_dir="/workspaces/ZoteroMDsMineru3/data"):
    """Analyze existing MD files to understand structure and content"""
    data_path = Path(data_dir)
    
    if not data_path.exists():
        logger.error(f"Data directory not found: {data_dir}")
        return None
    
    # Initialize statistics
    stats = {
        "total_files": 0,
        "total_size": 0,
        "has_abstract": 0,
        "has_keywords": 0,
        "has_authors": 0,
        "has_intro": 0,
        "has_conclusion": 0,
        "avg_length": 0,
        "sections_found": Counter(),
        "file_sizes": [],
        "batches": defaultdict(int),
        "sample_files": []
    }
    
    logger.info(f"Analyzing MD files in: {data_path}")
    
    # Process all .md files
    for md_file in data_path.rglob("*.md"):
        try:
            stats["total_files"] += 1
            file_size = md_file.stat().st_size
            stats["total_size"] += file_size
            stats["file_sizes"].append(file_size)
            
            # Track batches
            batch_name = md_file.parent.name
            stats["batches"][batch_name] += 1
            
            # Read content safely
            try:
                content = md_file.read_text(encoding='utf-8', errors='ignore')
            except Exception as e:
                logger.warning(f"Could not read {md_file}: {e}")
                continue
            
            # Content analysis
            content_lower = content.lower()
            
            # Check for academic sections
            if re.search(r'#\s*abstract', content, re.IGNORECASE):
                stats["has_abstract"] += 1
            if re.search(r'keywords?:', content, re.IGNORECASE):
                stats["has_keywords"] += 1
            if re.search(r'author[s]?:', content, re.IGNORECASE):
                stats["has_authors"] += 1
            if re.search(r'#\s*(introduction|intro)', content, re.IGNORECASE):
                stats["has_intro"] += 1
            if re.search(r'#\s*(conclusion|summary)', content, re.IGNORECASE):
                stats["has_conclusion"] += 1
            
            # Extract section headers (markdown headers)
            sections = re.findall(r'^#+\s*(.+)$', content, re.MULTILINE)
            for section in sections[:10]:  # Limit to first 10 sections per file
                # Clean and normalize section names
                clean_section = re.sub(r'[^a-zA-Z\s]', '', section).strip().lower()
                if clean_section and len(clean_section) > 2:
                    stats["sections_found"][clean_section] += 1
            
            # Store sample files for detailed analysis
            if len(stats["sample_files"]) < 5:
                stats["sample_files"].append({
                    "path": str(md_file),
                    "size": file_size,
                    "preview": content[:500]  # First 500 chars
                })
                
        except Exception as e:
            logger.error(f"Error processing {md_file}: {e}")
            continue
    
    # Calculate derived statistics
    if stats["total_files"] > 0:
        stats["avg_length"] = stats["total_size"] / stats["total_files"]
        stats["min_size"] = min(stats["file_sizes"]) if stats["file_sizes"] else 0
        stats["max_size"] = max(stats["file_sizes"]) if stats["file_sizes"] else 0
    
    return stats

def print_analysis_report(stats):
    """Print a comprehensive analysis report"""
    if not stats:
        print("No analysis data available.")
        return
    
    print("=" * 80)
    print("ZOTERO MD FILES ANALYSIS REPORT")
    print("=" * 80)
    
    # Basic statistics
    print(f"\n📊 BASIC STATISTICS:")
    print(f"  Total files: {stats['total_files']:,}")
    print(f"  Total size: {stats['total_size']:,} bytes ({stats['total_size']/(1024*1024):.2f} MB)")
    print(f"  Average file size: {stats['avg_length']:,.0f} bytes")
    print(f"  Size range: {stats.get('min_size', 0):,} - {stats.get('max_size', 0):,} bytes")
    
    # Batch distribution
    print(f"\n📁 BATCH DISTRIBUTION:")
    for batch, count in sorted(stats["batches"].items()):
        print(f"  {batch}: {count} files")
    
    # Content analysis
    print(f"\n📝 CONTENT ANALYSIS:")
    print(f"  Files with Abstract: {stats['has_abstract']} ({stats['has_abstract']/stats['total_files']*100:.1f}%)")
    print(f"  Files with Keywords: {stats['has_keywords']} ({stats['has_keywords']/stats['total_files']*100:.1f}%)")
    print(f"  Files with Authors: {stats['has_authors']} ({stats['has_authors']/stats['total_files']*100:.1f}%)")
    print(f"  Files with Introduction: {stats['has_intro']} ({stats['has_intro']/stats['total_files']*100:.1f}%)")
    print(f"  Files with Conclusion: {stats['has_conclusion']} ({stats['has_conclusion']/stats['total_files']*100:.1f}%)")
    
    # Common sections
    print(f"\n📋 MOST COMMON SECTIONS (Top 20):")
    for section, count in stats["sections_found"].most_common(20):
        print(f"  {section}: {count} files")
    
    # Sample files
    print(f"\n📄 SAMPLE FILES:")
    for i, sample in enumerate(stats["sample_files"], 1):
        print(f"\n  Sample {i}: {Path(sample['path']).name}")
        print(f"    Size: {sample['size']:,} bytes")
        print(f"    Preview: {sample['preview'][:200]}...")
    
    print("=" * 80)

def generate_recommendations(stats):
    """Generate recommendations for RAG system design"""
    print("\n🎯 RAG SYSTEM RECOMMENDATIONS:")
    print("-" * 50)
    
    # File size recommendations
    avg_size = stats.get('avg_length', 0)
    if avg_size < 5000:
        print("  📄 Small files detected - Consider larger chunk sizes (1500-2000 tokens)")
    elif avg_size > 50000:
        print("  📚 Large files detected - Use hierarchical chunking strategy")
    else:
        print("  📃 Medium files - Standard chunking (1000 tokens) should work well")
    
    # Content structure recommendations
    abstract_ratio = stats['has_abstract'] / max(stats['total_files'], 1)
    if abstract_ratio > 0.7:
        print("  📋 High abstract coverage - Prioritize abstract extraction for metadata")
    if abstract_ratio < 0.3:
        print("  ⚠️  Low abstract coverage - Use first paragraph as summary fallback")
    
    # Section-based recommendations
    common_sections = [s for s, c in stats["sections_found"].most_common(10)]
    if any("method" in s or "approach" in s for s in common_sections):
        print("  🔬 Methodology sections found - Add methodology classification")
    if any("result" in s or "finding" in s for s in common_sections):
        print("  📊 Results sections found - Enable results-focused queries")
    if any("discussion" in s or "conclusion" in s for s in common_sections):
        print("  💭 Discussion sections found - Good for synthesis queries")
    
    # Batch recommendations
    batch_count = len(stats["batches"])
    if batch_count > 1:
        print(f"  📦 Multiple batches ({batch_count}) - Consider batch-based filtering")
    
    print(f"\n  🎯 Recommended chunk size: 1000-1500 tokens")
    print(f"  🎯 Recommended overlap: 200 tokens")
    print(f"  🎯 Recommended metadata fields: title, authors, abstract, section_type")

if __name__ == "__main__":
    # Run analysis
    logger.info("Starting data analysis...")
    
    results = analyze_md_files()
    
    if results:
        print_analysis_report(results)
        generate_recommendations(results)
        
        # Save results to file
        output_file = Path("logs/data_analysis_results.txt")
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            import json
            # Convert Counter objects to regular dicts for JSON serialization
            json_results = dict(results)
            json_results["sections_found"] = dict(json_results["sections_found"])
            json.dump(json_results, f, indent=2)
        
        logger.info(f"Analysis complete! Results saved to {output_file}")
    else:
        logger.error("Analysis failed!")

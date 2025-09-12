#!/usr/bin/env python3
"""
Scale-up Analysis for RAG System
Analyzes processing time and content annotation requirements for all 1,927 documents
"""

import os
import glob
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple
import re
from datetime import datetime, timedelta

class ScaleAnalyzer:
    def __init__(self, data_dir: str = "/workspaces/ZoteroMDsMineru3/data"):
        self.data_dir = data_dir
        self.results = {}
        
    def analyze_file_statistics(self) -> Dict:
        """Analyze all MD files for processing estimates"""
        print("🔍 Analyzing file statistics...")
        
        all_files = []
        total_size = 0
        total_lines = 0
        word_counts = []
        section_patterns = []
        
        # Find all markdown files
        for batch_dir in glob.glob(f"{self.data_dir}/batch_*"):
            md_files = glob.glob(f"{batch_dir}/*.md")
            all_files.extend(md_files)
        
        print(f"Found {len(all_files)} files to process")
        
        # Sample analysis on first 50 files for speed
        sample_files = all_files[:50] if len(all_files) > 50 else all_files
        
        for file_path in sample_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                    words = len(content.split())
                    
                    total_size += len(content)
                    total_lines += lines
                    word_counts.append(words)
                    
                    # Analyze content structure
                    sections = self._extract_sections(content)
                    section_patterns.extend(sections)
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        # Calculate statistics
        avg_file_size = total_size / len(sample_files) if sample_files else 0
        avg_lines = total_lines / len(sample_files) if sample_files else 0
        avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
        
        return {
            "total_files": len(all_files),
            "sample_analyzed": len(sample_files),
            "avg_file_size_bytes": avg_file_size,
            "avg_lines_per_file": avg_lines,
            "avg_words_per_file": avg_words,
            "estimated_total_size_mb": (avg_file_size * len(all_files)) / (1024 * 1024),
            "section_types_found": len(set(section_patterns)),
            "common_sections": self._get_common_sections(section_patterns)
        }
    
    def _extract_sections(self, content: str) -> List[str]:
        """Extract section headers from markdown content"""
        # Find markdown headers
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        
        # Also look for common academic patterns
        patterns = [
            r'\b(abstract|introduction|methodology|results|discussion|conclusion)\b',
            r'\b(literature review|background|related work)\b',
            r'\b(data|analysis|findings|implications)\b'
        ]
        
        sections = headers.copy()
        for pattern in patterns:
            matches = re.findall(pattern, content.lower())
            sections.extend(matches)
        
        return sections
    
    def _get_common_sections(self, sections: List[str]) -> Dict[str, int]:
        """Get most common section types"""
        from collections import Counter
        counter = Counter(sections)
        return dict(counter.most_common(10))
    
    def estimate_processing_time(self, stats: Dict) -> Dict:
        """Estimate processing times for different operations"""
        
        # Based on our experience with 3 files
        annotation_time_per_file = 3  # seconds (LLM call + processing)
        indexing_time_per_file = 0.5  # seconds (embedding + FAISS)
        
        total_files = stats["total_files"]
        
        # Annotation estimates
        total_annotation_time = total_files * annotation_time_per_file
        annotation_hours = total_annotation_time / 3600
        
        # Indexing estimates  
        total_indexing_time = total_files * indexing_time_per_file
        indexing_minutes = total_indexing_time / 60
        
        # API cost estimates (OpenRouter Claude 3 Haiku)
        # ~$0.25 per 1M input tokens, ~$1.25 per 1M output tokens
        avg_input_tokens = stats["avg_words_per_file"] * 1.3  # ~1.3 tokens per word
        avg_output_tokens = 200  # metadata output
        
        total_input_tokens = total_files * avg_input_tokens
        total_output_tokens = total_files * avg_output_tokens
        
        input_cost = (total_input_tokens / 1_000_000) * 0.25
        output_cost = (total_output_tokens / 1_000_000) * 1.25
        total_api_cost = input_cost + output_cost
        
        return {
            "annotation": {
                "total_time_seconds": total_annotation_time,
                "total_time_hours": annotation_hours,
                "estimated_completion": self._format_duration(annotation_hours),
                "api_cost_usd": round(total_api_cost, 2),
                "rate_limiting": "OpenRouter: ~60 req/min",
                "batch_recommendation": f"Process in batches of 100-200 files"
            },
            "indexing": {
                "total_time_seconds": total_indexing_time,
                "total_time_minutes": indexing_minutes,
                "estimated_completion": self._format_duration(indexing_minutes / 60),
                "memory_requirement": f"~{stats['estimated_total_size_mb']:.1f}MB RAM",
                "storage_requirement": f"~{total_files * 0.5:.1f}MB for FAISS index"
            },
            "full_pipeline": {
                "sequential_hours": annotation_hours + (indexing_minutes / 60),
                "parallel_hours": annotation_hours,  # Indexing can happen after each batch
                "recommended_approach": "Batch processing with incremental indexing"
            }
        }
    
    def _format_duration(self, hours: float) -> str:
        """Format duration in human-readable format"""
        if hours < 1:
            minutes = hours * 60
            return f"{minutes:.1f} minutes"
        elif hours < 24:
            return f"{hours:.1f} hours"
        else:
            days = hours / 24
            return f"{days:.1f} days"
    
    def analyze_content_annotation_opportunities(self, stats: Dict) -> Dict:
        """Analyze what additional content annotations we could extract"""
        
        opportunities = {
            "current_metadata": [
                "title", "authors", "publication_year", "category",
                "subject_area", "methodology", "tags", "key_findings"
            ],
            "content_analysis_opportunities": {
                "semantic_sections": {
                    "description": "Extract and classify document sections (intro, methods, results, etc.)",
                    "value": "Better retrieval granularity - search within specific sections",
                    "implementation": "Use LLM to identify section boundaries and classify content",
                    "effort": "Medium - add to existing annotation pipeline"
                },
                "key_concepts": {
                    "description": "Extract domain-specific terminology and concepts",
                    "value": "Enhanced semantic search and concept-based filtering",
                    "implementation": "Named Entity Recognition + domain knowledge",
                    "effort": "Medium-High - requires academic domain models"
                },
                "citation_network": {
                    "description": "Extract cited works and build citation graph",
                    "value": "Find related papers, track research lineage",
                    "implementation": "Parse references, match with existing corpus",
                    "effort": "High - complex text parsing and matching"
                },
                "research_methodology": {
                    "description": "Detailed methodology classification (qualitative, quantitative, mixed)",
                    "value": "Filter papers by research approach",
                    "implementation": "LLM classification with methodology taxonomy",
                    "effort": "Low - extend current metadata schema"
                },
                "evidence_quality": {
                    "description": "Assess study quality, sample size, statistical significance",
                    "value": "Evidence-based ranking and filtering",
                    "implementation": "LLM analysis + statistical pattern recognition",
                    "effort": "High - requires domain expertise validation"
                },
                "geographical_context": {
                    "description": "Extract study location, cultural context",
                    "value": "Regional analysis and cultural comparison",
                    "implementation": "Named Entity Recognition for locations",
                    "effort": "Low-Medium - straightforward NER task"
                },
                "temporal_analysis": {
                    "description": "Track research trends over time",
                    "value": "Historical analysis and trend prediction",
                    "implementation": "Time-series analysis of extracted concepts",
                    "effort": "Medium - requires aggregation and visualization"
                }
            },
            "advanced_rag_features": {
                "multi_modal_search": {
                    "description": "Search by methodology + topic + timeframe simultaneously",
                    "value": "Highly specific academic queries",
                    "effort": "Medium - combine existing metadata"
                },
                "contradiction_detection": {
                    "description": "Find papers with conflicting findings",
                    "value": "Identify research debates and gaps",
                    "effort": "High - requires sophisticated comparison"
                },
                "research_gap_identification": {
                    "description": "Automatically identify understudied areas",
                    "value": "Guide future research directions",
                    "effort": "High - requires comprehensive analysis"
                }
            }
        }
        
        return opportunities
    
    def generate_sprint_recommendations(self, stats: Dict, timing: Dict) -> Dict:
        """Generate detailed sprint plans based on analysis"""
        
        return {
            "sprint_3_scale_up": {
                "duration": "3-5 days",
                "primary_goal": "Annotate all 1,927 documents",
                "tasks": [
                    "Implement batch processing (100-200 files per batch)",
                    "Add progress tracking and resume capability",
                    "Create parallel processing for annotation + indexing",
                    "Build monitoring dashboard for API usage/costs",
                    "Validate annotation quality on larger sample"
                ],
                "deliverables": [
                    "Fully annotated corpus (1,927 files)",
                    "Complete FAISS index with all documents",
                    "Quality metrics and validation report"
                ],
                "estimated_cost": f"${timing['annotation']['api_cost_usd']} (OpenRouter API)",
                "success_criteria": [
                    ">95% annotation success rate",
                    "Average query response time <2 seconds",
                    "Comprehensive metadata coverage"
                ]
            },
            "sprint_4_content_enhancement": {
                "duration": "2-3 days",
                "primary_goal": "Deep content analysis and semantic enrichment",
                "tasks": [
                    "Implement section-level annotation",
                    "Extract key concepts and terminology",
                    "Build citation network analysis",
                    "Add research methodology classification",
                    "Create geographical and temporal metadata"
                ],
                "deliverables": [
                    "Enhanced metadata schema with content analysis",
                    "Section-level search capabilities",
                    "Citation network visualization",
                    "Research trend analysis dashboard"
                ],
                "estimated_effort": "Medium-High",
                "success_criteria": [
                    "Search within specific paper sections",
                    "Find papers by methodology type",
                    "Track research evolution over time"
                ]
            },
            "sprint_5_production_interface": {
                "duration": "2-3 days", 
                "primary_goal": "User-friendly interface and advanced features",
                "tasks": [
                    "Build Streamlit web interface",
                    "Implement advanced filtering (author, year, methodology)",
                    "Add batch query processing",
                    "Create export functionality (citations, summaries)",
                    "Deploy to cloud platform"
                ],
                "deliverables": [
                    "Professional web interface",
                    "Multi-filter search capabilities",
                    "Batch processing interface",
                    "Citation export tools",
                    "Cloud deployment"
                ],
                "success_criteria": [
                    "Intuitive user interface",
                    "Handle multiple simultaneous users",
                    "Export publication-ready citations"
                ]
            }
        }

def main():
    """Run complete scale-up analysis"""
    analyzer = ScaleAnalyzer()
    
    print("🚀 SCALE-UP ANALYSIS FOR RAG SYSTEM")
    print("=" * 50)
    
    # File statistics
    stats = analyzer.analyze_file_statistics()
    print("\n📊 FILE STATISTICS:")
    print(f"  Total files to process: {stats['total_files']:,}")
    print(f"  Sample analyzed: {stats['sample_analyzed']}")
    print(f"  Average file size: {stats['avg_file_size_bytes']:,.0f} bytes")
    print(f"  Average words per file: {stats['avg_words_per_file']:,.0f}")
    print(f"  Total estimated corpus: {stats['estimated_total_size_mb']:.1f} MB")
    print(f"  Section types found: {stats['section_types_found']}")
    
    # Processing time estimates
    timing = analyzer.estimate_processing_time(stats)
    print("\n⏱️ PROCESSING TIME ESTIMATES:")
    
    print("\n  📝 Annotation (LLM metadata extraction):")
    print(f"    Duration: {timing['annotation']['estimated_completion']}")
    print(f"    API Cost: ${timing['annotation']['api_cost_usd']}")
    print(f"    Rate limit: {timing['annotation']['rate_limiting']}")
    print(f"    Recommendation: {timing['annotation']['batch_recommendation']}")
    
    print("\n  🔍 Indexing (FAISS vector database):")
    print(f"    Duration: {timing['indexing']['estimated_completion']}")
    print(f"    Memory needed: {timing['indexing']['memory_requirement']}")
    print(f"    Storage needed: {timing['indexing']['storage_requirement']}")
    
    print("\n  🎯 Full Pipeline:")
    print(f"    Sequential processing: {timing['full_pipeline']['sequential_hours']:.1f} hours")
    print(f"    Optimized parallel: {timing['full_pipeline']['parallel_hours']:.1f} hours")
    print(f"    Strategy: {timing['full_pipeline']['recommended_approach']}")
    
    # Content analysis opportunities
    opportunities = analyzer.analyze_content_annotation_opportunities(stats)
    print("\n🔬 CONTENT ANNOTATION OPPORTUNITIES:")
    
    for category, features in opportunities["content_analysis_opportunities"].items():
        print(f"\n  📌 {category.replace('_', ' ').title()}:")
        print(f"    Value: {features['value']}")
        print(f"    Effort: {features['effort']}")
    
    # Sprint recommendations
    sprints = analyzer.generate_sprint_recommendations(stats, timing)
    print("\n🏃‍♂️ RECOMMENDED SPRINT PLAN:")
    
    for sprint_name, details in sprints.items():
        print(f"\n  🎯 {sprint_name.replace('_', ' ').title()}:")
        print(f"    Duration: {details['duration']}")
        print(f"    Goal: {details['primary_goal']}")
        print(f"    Key Tasks: {len(details['tasks'])} items")
        if 'estimated_cost' in details:
            print(f"    Cost: {details['estimated_cost']}")
    
    print("\n✨ SUMMARY:")
    print(f"  • Scale to {stats['total_files']:,} documents: ~{timing['full_pipeline']['parallel_hours']:.1f} hours")
    print(f"  • API cost: ${timing['annotation']['api_cost_usd']}")
    print(f"  • Enhanced content analysis: 7 additional annotation types available")
    print(f"  • Production ready: 3 sprints (7-11 days total)")
    
    # Save results
    results = {
        "analysis_date": datetime.now().isoformat(),
        "file_statistics": stats,
        "timing_estimates": timing,
        "content_opportunities": opportunities,
        "sprint_recommendations": sprints
    }
    
    output_file = "/workspaces/ZoteroMDsMineru3/logs/scale_analysis_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Full analysis saved to: {output_file}")

if __name__ == "__main__":
    main()

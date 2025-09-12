#!/usr/bin/env python3
"""
Citation Review and Improvement System
Helps authors analyze how their manuscript cites reference papers and suggests improvements.

Usage:
  python scripts/citation_reviewer.py \
    --manuscript manuscript.md \
    --references faiss_index \
    --output citation_review.md
"""

import argparse
import re
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
import sys

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent))
from openRouterAI.client import post_chat_completions
from scripts.index import AcademicIndexer
from scripts.rag import AcademicRAG

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CitationReviewer:
    """Analyzes manuscript citations and suggests improvements"""
    
    def __init__(self, index_dir: Path, model: str = "anthropic/claude-3-haiku"):
        self.indexer = AcademicIndexer()
        self.indexer.load_index(index_dir)
        self.rag_system = AcademicRAG(index_dir, model)
        self.model = model
        
    def extract_citations(self, manuscript_text: str) -> List[Dict[str, Any]]:
        """Extract citations from manuscript text"""
        citations = []
        
        # Pattern for various citation formats
        patterns = [
            r'\(([^)]*\d{4}[^)]*)\)',  # (Author, 2023) or (Author et al., 2023)
            r'([A-Z][a-z]+ et al\.?,? \d{4})',  # Author et al., 2023
            r'([A-Z][a-z]+ & [A-Z][a-z]+,? \d{4})',  # Author & Author, 2023
            r'([A-Z][a-z]+,? \d{4})',  # Author, 2023
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, manuscript_text)
            for match in matches:
                citation_text = match.group(1) if pattern.startswith(r'\(') else match.group(0)
                start_pos = match.start()
                
                # Get context (50 chars before and after)
                context_start = max(0, start_pos - 50)
                context_end = min(len(manuscript_text), match.end() + 50)
                context = manuscript_text[context_start:context_end]
                
                citations.append({
                    "citation": citation_text,
                    "position": start_pos,
                    "context": context.strip(),
                    "pattern": pattern
                })
        
        # Remove duplicates and sort by position
        unique_citations = []
        seen = set()
        for cite in citations:
            if cite["citation"] not in seen:
                unique_citations.append(cite)
                seen.add(cite["citation"])
        
        return sorted(unique_citations, key=lambda x: x["position"])
    
    def find_related_papers(self, citation_context: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Find papers related to citation context"""
        return self.indexer.search(citation_context, k=top_k, min_score=0.1)
    
    def analyze_citation_usage(self, citation: Dict[str, Any], related_papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how a citation is used and suggest improvements"""
        
        # Create prompt for citation analysis
        papers_context = "\n\n".join([
            f"Paper {i+1}: {paper['title']}\nAuthors: {', '.join(paper.get('authors', []))}\nContent: {paper['document']['content'][:500]}..."
            for i, paper in enumerate(related_papers[:3])
        ])
        
        prompt = f"""
Analyze this citation usage in an academic manuscript and provide improvement suggestions:

Citation: {citation['citation']}
Context: ...{citation['context']}...

Related papers from reference corpus:
{papers_context}

Please provide:
1. Citation appropriateness (is it used correctly?)
2. Missing aspects (what important points from the paper aren't mentioned?)
3. Suggested improvements (how to better integrate this citation?)
4. Additional citations (what other papers from the corpus could strengthen this point?)

Format as JSON:
{{
  "appropriateness": "appropriate|partially_appropriate|inappropriate",
  "appropriateness_reason": "explanation",
  "missing_aspects": ["aspect1", "aspect2"],
  "suggested_improvements": "detailed suggestion",
  "additional_citations": ["paper title 1", "paper title 2"]
}}
"""
        
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            response = post_chat_completions(payload)
            response_text = response["choices"][0]["message"]["content"].strip()
            
            # Try to parse JSON response
            try:
                analysis = json.loads(response_text)
                return analysis
            except json.JSONDecodeError:
                return {
                    "appropriateness": "unknown",
                    "appropriateness_reason": "Could not parse LLM response",
                    "missing_aspects": [],
                    "suggested_improvements": response_text,
                    "additional_citations": []
                }
                
        except Exception as e:
            logger.error(f"Error analyzing citation: {e}")
            return {
                "appropriateness": "error",
                "appropriateness_reason": str(e),
                "missing_aspects": [],
                "suggested_improvements": "Error occurred during analysis",
                "additional_citations": []
            }
    
    def generate_section_suggestions(self, manuscript_text: str, section_title: str) -> Dict[str, Any]:
        """Generate suggestions for improving citations in a specific section"""
        
        # Extract the section
        section_pattern = rf"#+\s*{re.escape(section_title)}.*?(?=#+|\Z)"
        section_match = re.search(section_pattern, manuscript_text, re.DOTALL | re.IGNORECASE)
        
        if not section_match:
            return {"error": f"Section '{section_title}' not found"}
        
        section_text = section_match.group(0)
        
        # Find relevant papers for this section
        relevant_papers = self.indexer.search(section_text, k=10, min_score=0.15)
        
        # Generate improvement suggestions
        prompt = f"""
Analyze this manuscript section and suggest citation improvements based on the reference corpus:

Section: {section_title}
Content: {section_text}

Available reference papers:
{chr(10).join([f"- {paper['title']} ({', '.join(paper.get('authors', []))})" for paper in relevant_papers[:10]])}

Please suggest:
1. Missing citations that should be added
2. Areas that need stronger support
3. Gaps in the literature coverage
4. Specific papers to cite for each recommendation

Provide actionable suggestions for improving this section's citations.
"""
        
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 1500
            }
            
            response = post_chat_completions(payload)
            
            return {
                "section": section_title,
                "suggestions": response["choices"][0]["message"]["content"],
                "relevant_papers": relevant_papers[:5]
            }
            
        except Exception as e:
            logger.error(f"Error generating section suggestions: {e}")
            return {"error": str(e)}
    
    def review_manuscript(self, manuscript_path: Path) -> Dict[str, Any]:
        """Complete citation review of a manuscript"""
        
        # Load manuscript
        manuscript_text = manuscript_path.read_text(encoding='utf-8')
        
        # Extract citations
        logger.info("Extracting citations from manuscript...")
        citations = self.extract_citations(manuscript_text)
        logger.info(f"Found {len(citations)} citations")
        
        # Analyze each citation
        citation_analyses = []
        for i, citation in enumerate(citations):
            logger.info(f"Analyzing citation {i+1}/{len(citations)}: {citation['citation']}")
            
            # Find related papers
            related_papers = self.find_related_papers(citation['context'], top_k=5)
            
            # Analyze citation usage
            analysis = self.analyze_citation_usage(citation, related_papers)
            analysis['citation'] = citation
            analysis['related_papers'] = related_papers
            
            citation_analyses.append(analysis)
        
        # Generate overall review
        overall_suggestions = self.generate_overall_suggestions(manuscript_text, citation_analyses)
        
        return {
            "manuscript_path": str(manuscript_path),
            "total_citations": len(citations),
            "citation_analyses": citation_analyses,
            "overall_suggestions": overall_suggestions
        }
    
    def generate_overall_suggestions(self, manuscript_text: str, citation_analyses: List[Dict[str, Any]]) -> str:
        """Generate overall manuscript citation suggestions"""
        
        # Summarize citation issues
        inappropriate_citations = [ca for ca in citation_analyses if ca.get('appropriateness') == 'inappropriate']
        partial_citations = [ca for ca in citation_analyses if ca.get('appropriateness') == 'partially_appropriate']
        
        # Get most frequently mentioned papers
        all_additional_papers = []
        for ca in citation_analyses:
            all_additional_papers.extend(ca.get('additional_citations', []))
        
        paper_counts = {}
        for paper in all_additional_papers:
            paper_counts[paper] = paper_counts.get(paper, 0) + 1
        
        frequent_suggestions = sorted(paper_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        prompt = f"""
Provide an overall citation review summary for this manuscript:

Total citations analyzed: {len(citation_analyses)}
Inappropriate citations: {len(inappropriate_citations)}
Partially appropriate citations: {len(partial_citations)}

Most frequently suggested additional papers:
{chr(10).join([f"- {paper} (mentioned {count} times)" for paper, count in frequent_suggestions])}

Key issues found:
{chr(10).join([f"- {ca['citation']['citation']}: {ca.get('appropriateness_reason', 'Unknown')}" for ca in inappropriate_citations + partial_citations])}

Please provide:
1. Overall assessment of citation quality
2. Priority recommendations for improvement
3. Systematic gaps in literature coverage
4. Specific action items for the author
"""
        
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            response = post_chat_completions(payload)
            return response["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"Error generating overall suggestions: {e}")
            return f"Error generating suggestions: {e}"

def generate_review_report(review_results: Dict[str, Any], output_path: Path):
    """Generate a markdown report of the citation review"""
    
    report = f"""# Citation Review Report

**Manuscript**: {review_results['manuscript_path']}
**Total Citations**: {review_results['total_citations']}
**Review Date**: {Path(__file__).stat().st_mtime}

## Overall Assessment

{review_results['overall_suggestions']}

## Individual Citation Analysis

"""
    
    for i, analysis in enumerate(review_results['citation_analyses'], 1):
        citation = analysis['citation']
        report += f"""### Citation {i}: {citation['citation']}

**Context**: ...{citation['context']}...

**Appropriateness**: {analysis.get('appropriateness', 'Unknown')}
**Reason**: {analysis.get('appropriateness_reason', 'No reason provided')}

**Missing Aspects**:
{chr(10).join([f"- {aspect}" for aspect in analysis.get('missing_aspects', [])])}

**Suggested Improvements**:
{analysis.get('suggested_improvements', 'No suggestions')}

**Additional Citations to Consider**:
{chr(10).join([f"- {paper}" for paper in analysis.get('additional_citations', [])])}

**Related Papers from Corpus**:
{chr(10).join([f"- {paper['title']}" for paper in analysis.get('related_papers', [])[:3]])}

---

"""
    
    output_path.write_text(report, encoding='utf-8')
    logger.info(f"Review report saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Review manuscript citations and suggest improvements")
    parser.add_argument("--manuscript", required=True, help="Path to manuscript file")
    parser.add_argument("--references", required=True, help="Path to reference corpus index")
    parser.add_argument("--output", default="citation_review.md", help="Output report file")
    parser.add_argument("--model", default="anthropic/claude-3-haiku", help="LLM model to use")
    parser.add_argument("--section", help="Analyze specific section only")
    
    args = parser.parse_args()
    
    # Initialize reviewer
    reviewer = CitationReviewer(Path(args.references), args.model)
    
    # Load manuscript
    manuscript_path = Path(args.manuscript)
    if not manuscript_path.exists():
        logger.error(f"Manuscript file not found: {args.manuscript}")
        return
    
    if args.section:
        # Analyze specific section
        logger.info(f"Analyzing section: {args.section}")
        manuscript_text = manuscript_path.read_text(encoding='utf-8')
        results = reviewer.generate_section_suggestions(manuscript_text, args.section)
        
        output_path = Path(args.output)
        report = f"""# Section Analysis: {args.section}

## Suggestions
{results.get('suggestions', 'No suggestions generated')}

## Relevant Papers
{chr(10).join([f"- {paper['title']}" for paper in results.get('relevant_papers', [])])}
"""
        output_path.write_text(report, encoding='utf-8')
        logger.info(f"Section analysis saved to {output_path}")
        
    else:
        # Full manuscript review
        logger.info("Starting full manuscript citation review...")
        results = reviewer.review_manuscript(manuscript_path)
        
        # Generate report
        output_path = Path(args.output)
        generate_review_report(results, output_path)
        
        logger.info("Citation review complete!")
        logger.info(f"Total citations analyzed: {results['total_citations']}")

if __name__ == "__main__":
    main()

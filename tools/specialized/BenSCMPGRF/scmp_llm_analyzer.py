# SCMP Corpus LLM Analysis Implementation

## Core Analysis Engine for Citizenship Discourse Research

import os
import json
import csv
from datetime import datetime
from pathlib import Path
import re
from typing import Dict, List, Tuple, Optional

class SCMPLettersAnalyzer:
    """
    LLM-enhanced analysis engine for SCMP letters corpus
    Based on Ben Rowlett & Simon Wang's GRF research framework
    """
    
    def __init__(self, corpus_dir: str = "./GRF_SCMP_letters/corpus/processed"):
        self.corpus_dir = Path(corpus_dir)
        self.analysis_output_dir = Path("./analysis_output")
        self.analysis_output_dir.mkdir(exist_ok=True)
        
        # Research framework from GRF application
        self.research_questions = {
            "RQ1": "Public debate subjects and socio-political connections",
            "RQ2": "Linguistic resources for citizenship communication", 
            "RQ3": "Epistemologies informing citizenship communication",
            "RQ4": "Validation of letter writing as participatory citizenship"
        }
        
        # Citizenship discourse categories (from CDA framework)
        self.citizenship_types = [
            "civic_duty",           # Following rules, helping community
            "democratic_participation", # Voting, protest, advocacy  
            "cultural_belonging",   # Identity, heritage, local values
            "patriotic_loyalty",    # Support for government, nation
            "oppositional_critique" # Dissent, criticism, resistance
        ]
        
        # Hong Kong political timeline (2018-2023)
        self.political_events = {
            "2018": "Pre-extradition bill period",
            "2019-06": "Extradition bill protests begin", 
            "2019-11": "District council elections",
            "2020-06": "National Security Law implemented",
            "2021-03": "Electoral system reform",
            "2022-07": "25th anniversary of handover", 
            "2023": "Post-COVID normalization"
        }
    
    def load_corpus_files(self) -> List[Dict]:
        """Load and parse all SCMP letters from corpus directory"""
        letters = []
        
        # Process each year's letters file
        for year_file in self.corpus_dir.glob("SCMP_letters_*.csv"):
            year_match = re.search(r'(\d{4})', year_file.name)
            if not year_match:
                continue
            year = year_match.group(1)
            
            with open(year_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    letter = {
                        'id': f"{year}_{row.get('letter_id', len(letters))}",
                        'year': year,
                        'date': row.get('date'),
                        'author': row.get('author', 'Anonymous'), 
                        'title': row.get('title', ''),
                        'content': row.get('content', ''),
                        'word_count': len(row.get('content', '').split())
                    }
                    letters.append(letter)
        
        print(f"Loaded {len(letters)} letters from {len(list(self.corpus_dir.glob('*.csv')))} files")
        return letters
    
    def prepare_llm_prompts(self) -> Dict[str, str]:
        """Generate LLM analysis prompts based on GRF research framework"""
        
        prompts = {
            "citizenship_classification": """
Analyze this SCMP letter for citizenship discourse patterns:

TASK: Classify the primary citizenship type being communicated:
1. CIVIC DUTY (following rules, community service, responsible behavior)
2. DEMOCRATIC PARTICIPATION (voting, protests, advocacy, political engagement)  
3. CULTURAL BELONGING (Hong Kong identity, heritage, local values)
4. PATRIOTIC LOYALTY (support for government, nation, establishment)
5. OPPOSITIONAL CRITIQUE (dissent, criticism, resistance to authority)

LETTER DETAILS:
Date: {date}
Title: {title}
Content: {content}

ANALYSIS FORMAT:
Primary citizenship type: [TYPE]
Confidence level: [HIGH/MEDIUM/LOW]
Key phrases supporting classification: [List 2-3 quotes]
Secondary citizenship elements: [If any]
Political context references: [Government policies, events, movements mentioned]

RESPONSE:
""",
            
            "argumentation_analysis": """
Examine the argumentative structure and linguistic resources in this SCMP letter:

LETTER CONTENT:
Date: {date}  
Title: {title}
Text: {content}

ANALYSIS FRAMEWORK:
1. CLAIM STRUCTURE:
   - Main argument/position
   - Supporting sub-claims
   
2. EVIDENCE TYPES:
   - Personal experience
   - Statistics/data
   - Expert opinion  
   - Historical examples
   - Government documents
   
3. LINGUISTIC FEATURES:
   - Positioning language (I am, we should, citizens must)
   - Modal verbs (should, could, must, might)
   - Inclusive/exclusive pronouns (we/us vs they/them)
   - Emotional language and appeals
   
4. RHETORICAL STRATEGIES:
   - Problem-solution structure
   - Comparison/contrast
   - Cause-effect reasoning
   - Appeals to values/principles

PROVIDE SPECIFIC QUOTES AND ANALYSIS FOR EACH CATEGORY.

RESPONSE:
""",
            
            "temporal_discourse_shifts": """
Analyze this letter for discourse patterns related to Hong Kong's political timeline:

LETTER CONTEXT:
Date: {date}
Political Period: {political_context}
Content: {content}

TEMPORAL ANALYSIS:
1. EXPLICIT EVENT REFERENCES:
   - Direct mentions of protests, laws, elections
   - Government policy references
   - Social movements or political figures
   
2. IMPLICIT DISCOURSE MARKERS:
   - Language reflecting political tensions
   - Coded references to sensitive topics
   - Shifts in terminology (citizen vs resident vs Hong Konger)
   
3. COMPARED TO BASELINE:
   - How does language/tone differ from earlier periods?
   - New themes or concerns emerging?
   - Changes in argumentation strategies?

4. BROADER DISCOURSE CONNECTIONS:
   - Links to official government discourse
   - Media narrative influences  
   - International context references

PROVIDE EVIDENCE WITH SPECIFIC QUOTES.

RESPONSE:
""",
            
            "issue_classification": """
Classify and analyze the main issues discussed in this SCMP letter:

LETTER: 
Date: {date}
Title: {title} 
Content: {content}

ISSUE CLASSIFICATION:
Primary Issue Category:
□ POLITICS (elections, governance, democracy, rights)
□ ECONOMY (employment, housing, business, taxation)  
□ PANDEMIC (COVID policies, health measures, social restrictions)
□ EDUCATION (school policies, language, curriculum)
□ ENVIRONMENT (climate, pollution, urban development)
□ TRANSPORT (MTR, roads, cross-border travel)
□ SOCIAL WELFARE (elderly care, social services, inequality)
□ CULTURAL/IDENTITY (language, heritage, local values)
□ LAW/SECURITY (legal system, police, national security)
□ OTHER: [specify]

DETAILED ANALYSIS:
1. Specific sub-issues within main category
2. Proposed solutions or recommendations
3. Target audience (government, citizens, specific groups)
4. Urgency level expressed (immediate, medium-term, long-term)
5. Connection to broader Hong Kong debates
6. Evidence or examples provided

RESPONSE WITH REASONING:
"""
        }
        
        return prompts
    
    def analyze_single_letter(self, letter: Dict, analysis_type: str = "full") -> Dict:
        """
        Analyze individual letter using LLM prompts
        
        Args:
            letter: Letter dictionary with content, date, etc.
            analysis_type: Type of analysis ("citizenship", "argumentation", "temporal", "issues", "full")
        """
        
        # This would integrate with OpenRouter API
        # For now, return structured placeholder for testing
        
        analysis_result = {
            "letter_id": letter['id'],
            "date": letter['date'],
            "year": letter['year'],
            "word_count": letter['word_count'],
            "analysis_timestamp": datetime.now().isoformat(),
            "citizenship_classification": {
                "primary_type": "civic_duty",  # Would come from LLM
                "confidence": "HIGH",
                "key_phrases": ["citizens should", "our responsibility"],
                "secondary_elements": ["democratic_participation"],
                "political_references": ["government policy", "Legislative Council"]
            },
            "argumentation_structure": {
                "main_claim": "Government should increase housing supply",
                "evidence_types": ["statistics", "personal_experience"],
                "linguistic_features": ["inclusive_pronouns", "modal_verbs"],
                "rhetorical_strategies": ["problem_solution"]
            },
            "temporal_analysis": {
                "explicit_events": ["National Security Law"],
                "implicit_markers": ["increased caution in language"],
                "discourse_shifts": ["less direct criticism"]
            },
            "issue_classification": {
                "primary_category": "POLITICS",
                "sub_issues": ["electoral reform", "democratic participation"],
                "urgency_level": "immediate",
                "target_audience": "government"
            }
        }
        
        return analysis_result
    
    def batch_analyze_corpus(self, letters: List[Dict], batch_size: int = 100) -> List[Dict]:
        """Process entire corpus through LLM analysis pipeline"""
        
        results = []
        total_letters = len(letters)
        
        print(f"Starting batch analysis of {total_letters} letters...")
        
        for i in range(0, total_letters, batch_size):
            batch = letters[i:i+batch_size]
            batch_num = i // batch_size + 1
            
            print(f"Processing batch {batch_num} ({len(batch)} letters)...")
            
            for letter in batch:
                try:
                    analysis = self.analyze_single_letter(letter)
                    results.append(analysis)
                except Exception as e:
                    print(f"Error analyzing letter {letter['id']}: {e}")
                    continue
        
        print(f"Completed analysis of {len(results)} letters")
        return results
    
    def generate_summary_report(self, analysis_results: List[Dict]) -> Dict:
        """Generate quantitative summary of analysis results"""
        
        # Aggregate citizenship types
        citizenship_counts = {}
        for result in analysis_results:
            ctype = result['citizenship_classification']['primary_type']
            citizenship_counts[ctype] = citizenship_counts.get(ctype, 0) + 1
        
        # Temporal patterns
        yearly_counts = {}
        for result in analysis_results:
            year = result['year']
            yearly_counts[year] = yearly_counts.get(year, 0) + 1
        
        # Issue categories
        issue_counts = {}
        for result in analysis_results:
            issue = result['issue_classification']['primary_category']
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        summary = {
            "total_letters_analyzed": len(analysis_results),
            "analysis_period": f"{min(r['year'] for r in analysis_results)}-{max(r['year'] for r in analysis_results)}",
            "citizenship_distribution": citizenship_counts,
            "yearly_distribution": yearly_counts, 
            "issue_distribution": issue_counts,
            "average_word_count": sum(r['word_count'] for r in analysis_results) / len(analysis_results),
            "generated_timestamp": datetime.now().isoformat()
        }
        
        return summary
    
    def export_results(self, analysis_results: List[Dict], summary: Dict):
        """Export analysis results in multiple formats"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Detailed results as JSON
        results_file = self.analysis_output_dir / f"scmp_analysis_detailed_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        # Summary report as JSON
        summary_file = self.analysis_output_dir / f"scmp_analysis_summary_{timestamp}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # CSV export for further analysis
        csv_file = self.analysis_output_dir / f"scmp_analysis_results_{timestamp}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if analysis_results:
                # Flatten nested results for CSV
                fieldnames = [
                    'letter_id', 'date', 'year', 'word_count',
                    'primary_citizenship_type', 'citizenship_confidence',
                    'main_claim', 'primary_issue_category', 'urgency_level'
                ]
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for result in analysis_results:
                    row = {
                        'letter_id': result['letter_id'],
                        'date': result['date'],
                        'year': result['year'],
                        'word_count': result['word_count'],
                        'primary_citizenship_type': result['citizenship_classification']['primary_type'],
                        'citizenship_confidence': result['citizenship_classification']['confidence'],
                        'main_claim': result['argumentation_structure']['main_claim'],
                        'primary_issue_category': result['issue_classification']['primary_category'],
                        'urgency_level': result['issue_classification']['urgency_level']
                    }
                    writer.writerow(row)
        
        print(f"Results exported to:")
        print(f"  - Detailed: {results_file}")
        print(f"  - Summary: {summary_file}")  
        print(f"  - CSV: {csv_file}")

def main():
    """Main execution function for SCMP letters analysis"""
    
    print("=== SCMP Letters Citizenship Discourse Analysis ===")
    print("Based on Ben Rowlett & Simon Wang GRF Research Framework")
    print()
    
    # Initialize analyzer
    analyzer = SCMPLettersAnalyzer()
    
    # Load corpus (placeholder - would load actual processed files)
    print("1. Loading SCMP letters corpus...")
    # letters = analyzer.load_corpus_files()
    
    # For testing, create sample data structure
    letters = [
        {
            'id': '2020_001',
            'year': '2020',
            'date': '2020-07-01',
            'author': 'John Citizen',
            'title': 'Supporting the National Security Law',
            'content': 'As responsible citizens, we should support the National Security Law...',
            'word_count': 250
        },
        {
            'id': '2019_045', 
            'year': '2019',
            'date': '2019-06-15',
            'author': 'Democracy Advocate',
            'title': 'Protecting Hong Kong Values',
            'content': 'We must protect our democratic values and freedoms...',
            'word_count': 300
        }
    ]
    
    print(f"   Loaded {len(letters)} letters for analysis")
    
    # Generate LLM prompts
    print("2. Preparing LLM analysis prompts...")
    prompts = analyzer.prepare_llm_prompts()
    print(f"   Generated {len(prompts)} analysis prompt templates")
    
    # Analyze corpus  
    print("3. Analyzing corpus through LLM pipeline...")
    analysis_results = analyzer.batch_analyze_corpus(letters)
    print(f"   Completed analysis of {len(analysis_results)} letters")
    
    # Generate summary
    print("4. Generating summary report...")
    summary = analyzer.generate_summary_report(analysis_results)
    
    # Export results
    print("5. Exporting results...")
    analyzer.export_results(analysis_results, summary)
    
    print()
    print("=== Analysis Complete ===")
    print(f"Total letters: {summary['total_letters_analyzed']}")
    print(f"Period: {summary['analysis_period']}")
    print("Citizenship types found:")
    for ctype, count in summary['citizenship_distribution'].items():
        print(f"  - {ctype}: {count}")
    
    print()
    print("Next steps:")
    print("1. Integrate with OpenRouter API for actual LLM analysis")
    print("2. Process complete 6-year corpus (~250,000 lines)")  
    print("3. Generate academic paper draft from results")
    print("4. Create educational resources for student letter writing")

if __name__ == "__main__":
    main()

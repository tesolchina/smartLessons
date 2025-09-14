#!/usr/bin/env python3
"""
RAG-based Citation Annotation System
Analyzes the manuscript and suggests citations from the LitonGoalChatbot papers
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
import difflib

class RAGCitationAnnotator:
    def __init__(self, manuscript_path, papers_directory):
        self.manuscript_path = manuscript_path
        self.papers_directory = papers_directory
        self.manuscript_text = ""
        self.papers_database = {}
        self.citation_suggestions = []
        
        # Key concepts and their related papers from our previous analysis
        self.concept_paper_mapping = {
            "self-regulated learning": [
                "Winne & Hadwin (1998)", "Pintrich (2000)", "Zimmerman (2013)",
                "Kizilcec et al. (2017)", "Panadero (2017)", "Winne (2022)"
            ],
            "goal setting": [
                "Doran (1981)", "Latham & Locke (2007)", "Schunk (1990)",
                "Bandura & Schunk (1981)", "McCardle et al. (2016)"
            ],
            "chatbots": [
                "Hew et al. (2022)", "Singh et al. (2019)", "Ng et al. (2024)",
                "Guan et al. (2024)", "Wollny et al. (2021)"
            ],
            "AI-based chatbots": [
                "Ng et al. (2024)", "Guan et al. (2024)", "Hew et al. (2025)",
                "Lai (2024)"
            ],
            "educational technology": [
                "Chang et al. (2013)", "Scholl et al. (2009)", "Davis (1989)"
            ],
            "learning outcomes": [
                "Brady et al. (2024)", "Garavalia & Gredler (2002)",
                "Kizilcec et al. (2017)"
            ]
        }
    
    def load_manuscript(self):
        """Load the manuscript content"""
        try:
            with open(self.manuscript_path, 'r', encoding='utf-8') as f:
                self.manuscript_text = f.read()
            print(f"Loaded manuscript: {len(self.manuscript_text)} characters")
        except Exception as e:
            print(f"Error loading manuscript: {e}")
            return False
        return True
    
    def analyze_manuscript_sections(self):
        """Break down manuscript into sections for targeted analysis"""
        sections = {}
        
        # Split by major headers
        section_patterns = [
            (r'# Introduction', 'Introduction'),
            (r'# Literature Review|# Review of the related literature', 'Literature Review'),
            (r'# Methods?|# Methodology', 'Methods'),
            (r'# Results?', 'Results'),
            (r'# Discussion', 'Discussion'),
            (r'# Conclusion', 'Conclusion')
        ]
        
        current_section = "Introduction"
        current_content = []
        
        lines = self.manuscript_text.split('\n')
        
        for line in lines:
            # Check if this line starts a new section
            section_found = False
            for pattern, section_name in section_patterns:
                if re.match(pattern, line.strip(), re.IGNORECASE):
                    # Save previous section
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    
                    # Start new section
                    current_section = section_name
                    current_content = [line]
                    section_found = True
                    break
            
            if not section_found:
                current_content.append(line)
        
        # Don't forget the last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def find_citation_opportunities(self, text, section_name):
        """Find opportunities to add citations using RAG approach"""
        opportunities = []
        
        # Look for claims that need citations
        citation_patterns = [
            # Statements about SRL
            (r'(Self-regulated learning.*?is.*?process)', 'SRL_definition'),
            (r'(SRL.*?encompasses.*?processes)', 'SRL_components'),
            (r'(goal[- ]setting.*?critical.*?process)', 'goal_setting_importance'),
            (r'(SMART.*?framework)', 'SMART_framework'),
            (r'(chatbots.*?support.*?learning)', 'chatbot_education'),
            (r'(AI[- ]based.*?chatbots)', 'AI_chatbots'),
            (r'(students.*?set.*?goals)', 'student_goal_setting'),
            (r'(effective.*?goal[- ]setting)', 'effective_goals'),
            (r'(educational.*?technology)', 'ed_tech'),
            (r'(learning.*?outcomes)', 'learning_outcomes')
        ]
        
        for pattern, category in citation_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                context = match.group(1)
                start_pos = match.start()
                
                # Get surrounding context (50 chars before and after)
                context_start = max(0, start_pos - 50)
                context_end = min(len(text), match.end() + 50)
                full_context = text[context_start:context_end]
                
                # Suggest relevant papers based on category
                suggested_papers = self.get_relevant_papers(category)
                
                opportunities.append({
                    'section': section_name,
                    'text': context,
                    'full_context': full_context,
                    'category': category,
                    'position': start_pos,
                    'suggested_papers': suggested_papers
                })
        
        return opportunities
    
    def get_relevant_papers(self, category):
        """Get relevant papers for a specific category"""
        category_mapping = {
            'SRL_definition': self.concept_paper_mapping.get("self-regulated learning", []),
            'SRL_components': self.concept_paper_mapping.get("self-regulated learning", []),
            'goal_setting_importance': self.concept_paper_mapping.get("goal setting", []),
            'SMART_framework': ["Doran (1981)", "Bjerke & Renger (2017)"],
            'chatbot_education': self.concept_paper_mapping.get("chatbots", []),
            'AI_chatbots': self.concept_paper_mapping.get("AI-based chatbots", []),
            'student_goal_setting': self.concept_paper_mapping.get("goal setting", []),
            'effective_goals': self.concept_paper_mapping.get("goal setting", []),
            'ed_tech': self.concept_paper_mapping.get("educational technology", []),
            'learning_outcomes': self.concept_paper_mapping.get("learning outcomes", [])
        }
        
        return category_mapping.get(category, [])
    
    def generate_annotated_manuscript(self):
        """Generate an annotated version of the manuscript with citation suggestions"""
        sections = self.analyze_manuscript_sections()
        annotated_content = []
        
        annotated_content.append("# RAG-Annotated Manuscript with Citation Suggestions\n")
        annotated_content.append("*This version includes inline citation suggestions based on RAG analysis*\n\n")
        
        for section_name, section_text in sections.items():
            annotated_content.append(f"## {section_name}\n")
            
            # Find citation opportunities in this section
            opportunities = self.find_citation_opportunities(section_text, section_name)
            
            if opportunities:
                annotated_content.append(f"**🎯 Citation Opportunities Found: {len(opportunities)}**\n")
                
                # Process the text and add inline suggestions
                processed_text = section_text
                
                # Sort opportunities by position (reverse order to maintain positions)
                opportunities.sort(key=lambda x: x['position'], reverse=True)
                
                for i, opp in enumerate(opportunities):
                    citation_note = f" **[CITE: {', '.join(opp['suggested_papers'][:3])}]**"
                    
                    # Find the end of the sentence containing the opportunity
                    sentence_end = processed_text.find('.', opp['position'])
                    if sentence_end == -1:
                        sentence_end = opp['position'] + len(opp['text'])
                    
                    # Insert citation suggestion after the sentence
                    processed_text = (processed_text[:sentence_end] + 
                                    citation_note + 
                                    processed_text[sentence_end:])
                
                annotated_content.append(processed_text)
                annotated_content.append("\n---\n")
                
                # Add detailed suggestions at the end of the section
                annotated_content.append("### 📚 Detailed Citation Suggestions for this Section:\n")
                for i, opp in enumerate(opportunities, 1):
                    annotated_content.append(f"**{i}. {opp['category'].replace('_', ' ').title()}**")
                    annotated_content.append(f"- **Text:** \"{opp['text']}\"")
                    annotated_content.append(f"- **Suggested Citations:** {', '.join(opp['suggested_papers'])}")
                    annotated_content.append(f"- **Context:** {opp['full_context'][:100]}...")
                    annotated_content.append("")
            else:
                annotated_content.append(section_text)
            
            annotated_content.append("\n\n")
        
        return '\n'.join(annotated_content)
    
    def create_citation_summary(self):
        """Create a summary of all citation suggestions"""
        sections = self.analyze_manuscript_sections()
        all_opportunities = []
        
        for section_name, section_text in sections.items():
            opportunities = self.find_citation_opportunities(section_text, section_name)
            all_opportunities.extend(opportunities)
        
        summary = []
        summary.append("# RAG Citation Analysis Summary\n")
        summary.append(f"**Total Citation Opportunities Found:** {len(all_opportunities)}\n")
        
        # Group by section
        by_section = defaultdict(list)
        for opp in all_opportunities:
            by_section[opp['section']].append(opp)
        
        summary.append("## By Section:\n")
        for section, opps in by_section.items():
            summary.append(f"### {section} ({len(opps)} opportunities)")
            for i, opp in enumerate(opps, 1):
                summary.append(f"{i}. **{opp['category'].replace('_', ' ').title()}:** {opp['text'][:50]}...")
                summary.append(f"   - Suggested: {', '.join(opp['suggested_papers'][:2])}")
            summary.append("")
        
        # Group by paper frequency
        paper_frequency = defaultdict(int)
        for opp in all_opportunities:
            for paper in opp['suggested_papers']:
                paper_frequency[paper] += 1
        
        summary.append("## Most Frequently Suggested Papers:\n")
        sorted_papers = sorted(paper_frequency.items(), key=lambda x: x[1], reverse=True)
        for paper, count in sorted_papers[:10]:
            summary.append(f"- **{paper}:** {count} suggestions")
        
        return '\n'.join(summary)

def main():
    # Set up paths
    manuscript_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/citationAdvice/manuscript_0902.md'
    papers_dir = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/ZoteroPDF/LitonGoalChatbot'
    
    # Initialize annotator
    annotator = RAGCitationAnnotator(manuscript_path, papers_dir)
    
    # Load manuscript
    if not annotator.load_manuscript():
        return 1
    
    print("Generating RAG-based citation annotations...")
    
    # Generate annotated manuscript
    annotated_content = annotator.generate_annotated_manuscript()
    
    # Save annotated manuscript
    output_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/citationAdvice/RAG_Annotated_Manuscript.md'
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(annotated_content)
        print(f"✅ Annotated manuscript saved to: {output_path}")
    except Exception as e:
        print(f"Error saving annotated manuscript: {e}")
        return 1
    
    # Generate citation summary
    summary_content = annotator.create_citation_summary()
    
    # Save summary
    summary_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/citationAdvice/RAG_Citation_Summary.md'
    try:
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        print(f"✅ Citation summary saved to: {summary_path}")
    except Exception as e:
        print(f"Error saving citation summary: {e}")
        return 1
    
    print(f"\n🎯 RAG Analysis Complete!")
    print(f"📄 Annotated manuscript: {output_path}")
    print(f"📊 Citation summary: {summary_path}")
    
    return 0

if __name__ == "__main__":
    exit(main())
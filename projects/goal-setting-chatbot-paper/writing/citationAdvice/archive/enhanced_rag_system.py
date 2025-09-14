#!/usr/bin/env python3
"""
Enhanced RAG Citation Enhancement Script
Creates a comprehensive implementation guide with specific insertion points
"""

import os
import re
from pathlib import Path

class EnhancedRAGCitationSystem:
    def __init__(self, manuscript_path):
        self.manuscript_path = manuscript_path
        self.manuscript_text = ""
        
        # Enhanced paper mapping with more specific contexts
        self.citation_database = {
            "srl_theory": {
                "papers": ["Winne & Hadwin (1998)", "Pintrich (2000)", "Zimmerman (2013)", "Panadero (2017)"],
                "keywords": ["self-regulated learning", "SRL", "metacognitive", "self-regulation"],
                "context": "theoretical foundations of SRL"
            },
            "goal_setting_theory": {
                "papers": ["Doran (1981)", "Latham & Locke (2007)", "Schunk (1990)", "Bandura & Schunk (1981)"],
                "keywords": ["goal setting", "SMART goals", "proximal goals", "goal effectiveness"],
                "context": "goal setting theory and effectiveness"
            },
            "chatbot_education": {
                "papers": ["Hew et al. (2022)", "Singh et al. (2019)", "Wollny et al. (2021)", "Guan et al. (2024)"],
                "keywords": ["chatbot", "educational chatbot", "conversational agent"],
                "context": "educational chatbot applications"
            },
            "ai_chatbots": {
                "papers": ["Ng et al. (2024)", "Guan et al. (2024)", "Hew et al. (2025)", "Lai (2024)"],
                "keywords": ["AI-based chatbot", "LLM", "artificial intelligence", "generative AI"],
                "context": "AI-powered educational tools"
            },
            "student_goal_quality": {
                "papers": ["McCardle et al. (2016)", "Raluy & Mislang (2022)", "Brady et al. (2024)"],
                "keywords": ["student goals", "goal quality", "vague goals", "goal setting challenges"],
                "context": "challenges in student goal setting"
            },
            "educational_technology": {
                "papers": ["Chang et al. (2013)", "Scholl et al. (2009)", "Davis (1989)"],
                "keywords": ["educational technology", "web-based", "technology acceptance"],
                "context": "educational technology effectiveness"
            }
        }
    
    def load_manuscript(self):
        """Load the manuscript content"""
        try:
            with open(self.manuscript_path, 'r', encoding='utf-8') as f:
                self.manuscript_text = f.read()
            return True
        except Exception as e:
            print(f"Error loading manuscript: {e}")
            return False
    
    def find_specific_citation_points(self):
        """Find specific points where citations should be added"""
        citation_points = []
        
        # Define specific patterns that need citations
        citation_needs = [
            {
                "pattern": r"(Self-regulated learning.*?is.*?dynamic process)",
                "category": "srl_theory",
                "priority": "HIGH",
                "suggestion": "Add foundational SRL citations after defining SRL"
            },
            {
                "pattern": r"(SMART.*?framework.*?introduced.*?by.*?Doran)",
                "category": "goal_setting_theory", 
                "priority": "HIGH",
                "suggestion": "Verify Doran (1981) citation and add supporting goal-setting research"
            },
            {
                "pattern": r"(students.*?goals.*?often.*?vague)",
                "category": "student_goal_quality",
                "priority": "HIGH", 
                "suggestion": "Support claim about vague student goals with research evidence"
            },
            {
                "pattern": r"(chatbots.*?support.*?learning)",
                "category": "chatbot_education",
                "priority": "MEDIUM",
                "suggestion": "Add comprehensive chatbot education review citations"
            },
            {
                "pattern": r"(AI[- ]based.*?chatbots.*?leverage.*?large language models)",
                "category": "ai_chatbots",
                "priority": "HIGH",
                "suggestion": "Support AI chatbot capabilities claim with recent research"
            },
            {
                "pattern": r"(perceived usefulness.*?ease of use)",
                "category": "educational_technology",
                "priority": "MEDIUM",
                "suggestion": "Reference Technology Acceptance Model (Davis, 1989)"
            }
        ]
        
        for need in citation_needs:
            matches = list(re.finditer(need["pattern"], self.manuscript_text, re.IGNORECASE | re.DOTALL))
            for match in matches:
                # Get surrounding context
                start = max(0, match.start() - 100)
                end = min(len(self.manuscript_text), match.end() + 100)
                context = self.manuscript_text[start:end]
                
                citation_points.append({
                    "text": match.group(1),
                    "position": match.start(),
                    "category": need["category"],
                    "priority": need["priority"],
                    "suggestion": need["suggestion"],
                    "papers": self.citation_database[need["category"]]["papers"],
                    "context": context
                })
        
        return sorted(citation_points, key=lambda x: x["position"])
    
    def create_implementation_guide(self):
        """Create a detailed implementation guide"""
        citation_points = self.find_specific_citation_points()
        
        guide = []
        guide.append("# Enhanced RAG Citation Implementation Guide\n")
        guide.append("*Precise citation recommendations with exact insertion points*\n\n")
        
        # Priority-based grouping
        high_priority = [cp for cp in citation_points if cp["priority"] == "HIGH"]
        medium_priority = [cp for cp in citation_points if cp["priority"] == "MEDIUM"]
        
        guide.append("## 🚨 HIGH PRIORITY Citations (Implement First)\n")
        for i, cp in enumerate(high_priority, 1):
            guide.append(f"### {i}. {cp['category'].replace('_', ' ').title()}")
            guide.append(f"**Text to enhance:** \"{cp['text'][:100]}...\"")
            guide.append(f"**Recommended action:** {cp['suggestion']}")
            guide.append(f"**Suggested citations:** {', '.join(cp['papers'])}")
            guide.append(f"**Context window:**")
            guide.append(f"```")
            guide.append(f"{cp['context']}")
            guide.append(f"```")
            guide.append("")
        
        guide.append("## ⚠️ MEDIUM PRIORITY Citations (Implement Second)\n")
        for i, cp in enumerate(medium_priority, 1):
            guide.append(f"### {i}. {cp['category'].replace('_', ' ').title()}")
            guide.append(f"**Text to enhance:** \"{cp['text'][:100]}...\"")
            guide.append(f"**Recommended action:** {cp['suggestion']}")
            guide.append(f"**Suggested citations:** {', '.join(cp['papers'])}")
            guide.append("")
        
        # Add specific implementation instructions
        guide.append("## 📝 Implementation Instructions\n")
        guide.append("### Phase 1: Critical Citations (Do First)")
        guide.append("1. **SRL Definition Enhancement**")
        guide.append("   - Locate: First mention of 'Self-regulated learning is a dynamic process'")
        guide.append("   - Action: Add '(Winne & Hadwin, 1998; Pintrich, 2000; Zimmerman, 2013)' after the definition")
        guide.append("   - Why: Establishes theoretical foundation immediately")
        guide.append("")
        
        guide.append("2. **Student Goal Quality Claims**")
        guide.append("   - Locate: Claims about students setting 'vague goals'")
        guide.append("   - Action: Add '(McCardle et al., 2016; Raluy & Mislang, 2022)' to support empirical claims")
        guide.append("   - Why: Provides evidence for the problem statement")
        guide.append("")
        
        guide.append("3. **AI Chatbot Capabilities**")
        guide.append("   - Locate: Claims about AI chatbot advantages over rule-based systems")
        guide.append("   - Action: Add '(Ng et al., 2024; Guan et al., 2024; Hew et al., 2025)' for recent evidence")
        guide.append("   - Why: Supports technological claims with current research")
        guide.append("")
        
        guide.append("### Phase 2: Supporting Citations")
        guide.append("- Add Davis (1989) for Technology Acceptance Model references")
        guide.append("- Add comprehensive chatbot education reviews where appropriate")
        guide.append("- Enhance goal-setting theory sections with additional supporting research")
        guide.append("")
        
        guide.append("## 🎯 Quality Assurance Checklist")
        guide.append("- [ ] All high-priority citations implemented")
        guide.append("- [ ] Claims about student behavior supported by research")
        guide.append("- [ ] Theoretical frameworks properly cited")
        guide.append("- [ ] Technology claims backed by recent studies")
        guide.append("- [ ] Methodology appropriately referenced")
        guide.append("")
        
        return '\n'.join(guide)
    
    def create_quick_reference(self):
        """Create a quick reference for the most important citations"""
        quick_ref = []
        quick_ref.append("# Quick Citation Reference\n")
        quick_ref.append("## Essential Citations by Topic\n")
        
        for category, data in self.citation_database.items():
            quick_ref.append(f"### {category.replace('_', ' ').title()}")
            quick_ref.append(f"**Context:** {data['context']}")
            quick_ref.append(f"**Key papers:** {', '.join(data['papers'][:3])}")
            quick_ref.append(f"**Keywords:** {', '.join(data['keywords'])}")
            quick_ref.append("")
        
        quick_ref.append("## Most Critical Additions")
        quick_ref.append("1. **Winne & Hadwin (1998)** - SRL theoretical foundation")
        quick_ref.append("2. **McCardle et al. (2016)** - Student goal quality issues")
        quick_ref.append("3. **Ng et al. (2024)** - AI chatbot effectiveness")
        quick_ref.append("4. **Guan et al. (2024)** - Chatbot SRL support review")
        quick_ref.append("5. **Hew et al. (2025)** - LLM-based chatbot system")
        
        return '\n'.join(quick_ref)

def main():
    manuscript_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/citationAdvice/manuscript_0902.md'
    
    system = EnhancedRAGCitationSystem(manuscript_path)
    
    if not system.load_manuscript():
        return 1
    
    print("Generating enhanced RAG citation recommendations...")
    
    # Create implementation guide
    implementation_guide = system.create_implementation_guide()
    guide_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/citationAdvice/Enhanced_RAG_Implementation_Guide.md'
    
    try:
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(implementation_guide)
        print(f"✅ Implementation guide saved: {guide_path}")
    except Exception as e:
        print(f"Error saving implementation guide: {e}")
        return 1
    
    # Create quick reference
    quick_reference = system.create_quick_reference()
    ref_path = '/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/citationAdvice/Quick_Citation_Reference.md'
    
    try:
        with open(ref_path, 'w', encoding='utf-8') as f:
            f.write(quick_reference)
        print(f"✅ Quick reference saved: {ref_path}")
    except Exception as e:
        print(f"Error saving quick reference: {e}")
        return 1
    
    print(f"\n🎯 Enhanced RAG Analysis Complete!")
    print(f"📋 Implementation guide: {guide_path}")
    print(f"📖 Quick reference: {ref_path}")
    
    return 0

if __name__ == "__main__":
    exit(main())
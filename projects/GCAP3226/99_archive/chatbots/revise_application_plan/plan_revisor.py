#!/usr/bin/env python3
"""
Regression Analysis Revision Chatbot
====================================

This chatbot takes an original regression analysis document and AI assessment feedback
to generate an improved version with detailed change tracking.

Usage:
    python plan_revisor.py [original_file] [feedback_file] [output_file]

Features:
    - Integrates original analysis with expert feedback
    - Generates revised version with enhanced methodology
    - Provides detailed change tracking and justification
    - Maintains policy relevance while improving technical rigor
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
import argparse
from datetime import datetime


class RegressionPlanRevisor:
    """Main chatbot class for revising regression analysis plans."""
    
    def __init__(self, config_path: str = "revision_config.json"):
        """Initialize the revisor with configuration."""
        self.config_path = config_path
        self.config = self._load_config()
        self.api_key = self._load_api_key()
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def _load_config(self) -> Dict:
        """Load revision configuration."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in config file: {self.config_path}")
    
    def _load_api_key(self) -> str:
        """Load OpenRouter API key from .env file."""
        env_path = Path("../.env")
        if not env_path.exists():
            raise FileNotFoundError("API key file (.env) not found")
        
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("OpenRouter Key="):
                    return line.split("=", 1)[1].strip()
        
        raise ValueError("OpenRouter API key not found in .env file")
    
    def _read_document(self, file_path: str) -> str:
        """Read a document file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Document file not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading document: {e}")
    
    def _make_api_request(self, messages: List[Dict]) -> str:
        """Make request to OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://hkbu.edu.hk",
            "X-Title": "GCAP3226 Regression Plan Revisor"
        }
        
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": messages,
            "temperature": 0.2,  # Lower temperature for more consistent revisions
            "max_tokens": 8000   # Larger token limit for comprehensive revisions
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=data,
                timeout=120  # Longer timeout for complex revisions
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: {e}")
    
    def revise_plan(self, original_file: str, feedback_file: str, 
                   revision_focus: str = "comprehensive") -> str:
        """Generate revised regression analysis plan."""
        
        # Read input documents
        original_content = self._read_document(original_file)
        feedback_content = self._read_document(feedback_file)
        
        # Prepare revision prompt
        revision_prompt = self._create_revision_prompt(
            original_content, feedback_content, revision_focus
        )
        
        # Prepare system message
        system_message = {
            "role": "system",
            "content": self.config["system_prompt"]
        }
        
        # Prepare user message
        user_message = {
            "role": "user",
            "content": revision_prompt
        }
        
        print(f"🔄 Generating revised regression analysis plan...")
        print(f"📊 Revision focus: {revision_focus}")
        print(f"📝 Processing documents...")
        print("=" * 60)
        
        try:
            # Make API request
            messages = [system_message, user_message]
            revised_content = self._make_api_request(messages)
            
            print("✅ Revision completed successfully!")
            return revised_content
            
        except Exception as e:
            error_msg = f"Error generating revision: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def _create_revision_prompt(self, original: str, feedback: str, 
                               focus: str) -> str:
        """Create the revision prompt for the API."""
        
        focus_instructions = self._get_focus_instructions(focus)
        
        prompt = f"""You are tasked with revising a regression analysis framework based on expert feedback. Please create an enhanced version that addresses all major concerns while maintaining practical applicability.

REVISION GUIDELINES:
{json.dumps(self.config['revision_instructions'], indent=2)}

FOCUS AREA: {focus}
{focus_instructions}

OUTPUT FORMAT REQUIREMENTS:
{json.dumps(self.config['output_formatting'], indent=2)}

QUALITY STANDARDS:
{json.dumps(self.config['quality_standards'], indent=2)}

---

ORIGINAL REGRESSION ANALYSIS DOCUMENT:
{original}

---

EXPERT FEEDBACK TO ADDRESS:
{feedback}

---

TASK: Create a comprehensive revision that:

1. **ADDRESSES ALL MAJOR FEEDBACK POINTS** with specific solutions
2. **MAINTAINS POLICY RELEVANCE** and practical applicability
3. **ENHANCES STATISTICAL RIGOR** with proper methodology
4. **PROVIDES CLEAR CHANGE TRACKING** with rationale for each modification
5. **INCLUDES IMPLEMENTATION GUIDANCE** for practical deployment

Please structure your response with:

## EXECUTIVE SUMMARY OF CHANGES
- Brief overview of major revisions
- Key improvements made
- Impact on overall framework quality

## DETAILED REVISION LOG
For each significant change, use this format:
**CHANGE:** [Section] - [Brief description]
**RATIONALE:** [Why this change was made based on feedback]
**IMPACT:** [How this improves the analysis]

## ENHANCED REGRESSION FRAMEWORK
[The complete revised document with all improvements integrated]

## IMPLEMENTATION ROADMAP
- Specific steps for deploying the revised framework
- Timeline and resource requirements
- Risk mitigation strategies

## VALIDATION AND QUALITY ASSURANCE
- Methods for testing the revised framework
- Success metrics and evaluation criteria
- Continuous improvement procedures

Ensure all changes are clearly justified and the revised framework represents a significant improvement over the original while remaining practically implementable."""

        return prompt
    
    def _get_focus_instructions(self, focus: str) -> str:
        """Get specific instructions based on revision focus."""
        focus_map = {
            "comprehensive": "Address all feedback categories with equal attention to methodology, technical aspects, policy integration, and practical feasibility.",
            
            "methodology": "Prioritize statistical methodology improvements, including endogeneity solutions, model specifications, and validation procedures.",
            
            "technical": "Focus on technical enhancements like diagnostic tests, robustness checks, and statistical assumptions.",
            
            "policy": "Emphasize policy integration, implementation planning, and stakeholder considerations.",
            
            "practical": "Concentrate on practical feasibility, data collection improvements, and implementation constraints."
        }
        
        return focus_map.get(focus, focus_map["comprehensive"])
    
    def save_revision(self, revised_content: str, output_path: str, 
                     original_file: str, feedback_file: str):
        """Save the revised plan with metadata."""
        
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create header with metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"""# Revised Regression Analysis Framework

**Revision Generated:** {timestamp}  
**Original Document:** {Path(original_file).name}  
**Feedback Source:** {Path(feedback_file).name}  
**Revision Tool:** GCAP3226 Regression Plan Revisor  

---

"""
        
        # Write the complete revision
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(header)
            f.write(revised_content)
        
        print(f"💾 Revised plan saved to: {output_path}")
        print(f"📄 Document length: {len(revised_content.split())} words")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Revise regression analysis documents based on expert feedback",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python plan_revisor.py original.md feedback.md revised.md
  python plan_revisor.py original.md feedback.md revised.md --focus methodology
  python plan_revisor.py original.md feedback.md revised.md --focus technical
        """
    )
    
    parser.add_argument(
        "original_file", 
        help="Path to the original regression analysis document"
    )
    
    parser.add_argument(
        "feedback_file", 
        help="Path to the AI assessment feedback document"
    )
    
    parser.add_argument(
        "output_file", 
        help="Path for the revised document output"
    )
    
    parser.add_argument(
        "--focus", "-f",
        choices=["comprehensive", "methodology", "technical", "policy", "practical"],
        default="comprehensive",
        help="Focus area for revision (default: comprehensive)"
    )
    
    parser.add_argument(
        "--config", "-c",
        default="revision_config.json",
        help="Path to configuration file (default: revision_config.json)"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize revisor
        revisor = RegressionPlanRevisor(config_path=args.config)
        
        # Generate revision
        revised_content = revisor.revise_plan(
            args.original_file, 
            args.feedback_file, 
            args.focus
        )
        
        # Save revision
        revisor.save_revision(
            revised_content, 
            args.output_file, 
            args.original_file, 
            args.feedback_file
        )
        
        print("\\n✅ Revision process completed successfully!")
        print(f"📋 Check the revised document at: {args.output_file}")
        
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
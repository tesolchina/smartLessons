#!/usr/bin/env python3
"""
Regression Analysis Assessment Chatbot
======================================

This chatbot uses OpenRouter API to assess the quality and reliability of 
regression analysis documents for policy research.

Usage:
    python regression_assessor.py [file_path] [assessment_type]

Assessment types:
    - full: Complete assessment using all prompts
    - quick: Basic methodology and policy relevance assessment
    - technical: Focus on statistical methodology
    - policy: Focus on policy applicability
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
import argparse


class RegressionAssessor:
    """Main chatbot class for assessing regression analysis documents."""
    
    def __init__(self, config_path: str = "mathGuru/mathGuru.json"):
        """Initialize the assessor with configuration."""
        self.config_path = config_path
        self.config = self._load_config()
        self.api_key = self._load_api_key()
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def _load_config(self) -> Dict:
        """Load assessment prompts and configuration."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in config file: {self.config_path}")
    
    def _load_api_key(self) -> str:
        """Load OpenRouter API key from .env file."""
        env_path = Path(".env")
        if not env_path.exists():
            raise FileNotFoundError("API key file (.env) not found")
        
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("OpenRouter Key="):
                    return line.split("=", 1)[1].strip()
        
        raise ValueError("OpenRouter API key not found in .env file")
    
    def _read_document(self, file_path: str) -> str:
        """Read the document to be assessed."""
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
            "X-Title": "GCAP3226 Regression Assessment Tool"
        }
        
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=data,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: {e}")
    
    def assess_document(self, file_path: str, assessment_type: str = "full") -> Dict[str, str]:
        """Assess a regression analysis document."""
        # Read the document
        document_content = self._read_document(file_path)
        
        # Prepare system message
        system_message = {
            "role": "system",
            "content": self.config["system_prompt"]
        }
        
        # Select assessment prompts based on type
        assessment_prompts = self._select_prompts(assessment_type)
        
        results = {}
        
        print(f"🔍 Assessing document: {Path(file_path).name}")
        print(f"📊 Assessment type: {assessment_type}")
        print("=" * 60)
        
        for prompt_name, prompt_text in assessment_prompts.items():
            print(f"\\n📋 Running assessment: {prompt_name.replace('_', ' ').title()}")
            
            # Prepare messages for this assessment
            messages = [
                system_message,
                {
                    "role": "user",
                    "content": f"""Please assess the following regression analysis document:

DOCUMENT TO ASSESS:
{document_content}

ASSESSMENT PROMPT:
{prompt_text}

Please provide a detailed, constructive assessment with specific examples from the document where relevant."""
                }
            ]
            
            try:
                assessment_result = self._make_api_request(messages)
                results[prompt_name] = assessment_result
                
                # Display result
                print("\\n" + "─" * 50)
                print(assessment_result)
                print("─" * 50)
                
            except Exception as e:
                error_msg = f"Error in {prompt_name}: {str(e)}"
                results[prompt_name] = error_msg
                print(f"\\n❌ {error_msg}")
        
        return results
    
    def _select_prompts(self, assessment_type: str) -> Dict[str, str]:
        """Select appropriate prompts based on assessment type."""
        all_prompts = self.config["assessment_prompts"]
        
        if assessment_type == "full":
            return all_prompts
        elif assessment_type == "quick":
            return {
                "methodology_assessment": all_prompts["methodology_assessment"],
                "policy_relevance": all_prompts["policy_relevance"],
                "overall_assessment": all_prompts["overall_assessment"]
            }
        elif assessment_type == "technical":
            return {
                "methodology_assessment": all_prompts["methodology_assessment"],
                "technical_soundness": all_prompts["technical_soundness"],
                "improvement_suggestions": all_prompts["improvement_suggestions"]
            }
        elif assessment_type == "policy":
            return {
                "policy_relevance": all_prompts["policy_relevance"],
                "data_feasibility": all_prompts["data_feasibility"],
                "overall_assessment": all_prompts["overall_assessment"]
            }
        else:
            raise ValueError(f"Unknown assessment type: {assessment_type}")
    
    def save_assessment(self, results: Dict[str, str], output_path: str):
        """Save assessment results to file."""
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Regression Analysis Assessment Report\\n\\n")
            f.write(f"**Generated on:** {Path().cwd()}\\n")
            f.write(f"**Assessment tool:** GCAP3226 Regression Assessor\\n\\n")
            
            for prompt_name, result in results.items():
                f.write(f"## {prompt_name.replace('_', ' ').title()}\\n\\n")
                f.write(f"{result}\\n\\n")
                f.write("---\\n\\n")
        
        print(f"\\n💾 Assessment saved to: {output_path}")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Assess regression analysis documents using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python regression_assessor.py topic2_regression.md
  python regression_assessor.py topic2_regression.md --type technical
  python regression_assessor.py topic2_regression.md --type quick --output assessment.md
        """
    )
    
    parser.add_argument(
        "file_path", 
        help="Path to the regression analysis document to assess"
    )
    
    parser.add_argument(
        "--type", "-t",
        choices=["full", "quick", "technical", "policy"],
        default="full",
        help="Type of assessment to perform (default: full)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file path for assessment results (optional)"
    )
    
    parser.add_argument(
        "--config", "-c",
        default="mathGuru/mathGuru.json",
        help="Path to configuration file (default: mathGuru/mathGuru.json)"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize assessor
        assessor = RegressionAssessor(config_path=args.config)
        
        # Perform assessment
        results = assessor.assess_document(args.file_path, args.type)
        
        # Save results if output path provided
        if args.output:
            assessor.save_assessment(results, args.output)
        
        print("\\n✅ Assessment completed successfully!")
        
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
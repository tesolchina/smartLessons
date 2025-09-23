#!/usr/bin/env python3
"""
Update Mathematical Models Section
Focuses on regression and simulation models only, adds teacher consultation reminder
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from google_api_client import GoogleAPIClient

class ModelSectionUpdater:
    def __init__(self):
        """Initialize the model section updater"""
        self.client = GoogleAPIClient()
        self.docs_service = self.client.get_docs_service()
        self.instructor_doc_id = "1Vd98A1bFDgJrMj8UiKLrOYdIauP0rr-Ca7kz4A6Hu80"

    def get_updated_models_for_topic(self, topic):
        """Get regression and simulation models for each topic"""
        
        model_suggestions = {
            'Flu Shot Participation Analysis': [
                "Linear Regression: Analyze relationships between demographic factors and vaccination rates",
                "Logistic Regression: Predict vaccination participation (yes/no) based on barriers and demographics", 
                "Multiple Regression: Model multiple factors affecting participation simultaneously",
                "Monte Carlo Simulation: Simulate vaccination program outcomes under different scenarios",
                "Policy Simulation: Model impact of different intervention strategies on participation rates"
            ],
            'Inter-Company Bus Route Coordination': [
                "Linear Regression: Analyze relationships between coordination strategies and waiting times",
                "Multiple Regression: Model passenger satisfaction based on multiple coordination factors",
                "Time Series Regression: Analyze patterns in bus arrival times and coordination effectiveness",
                "Discrete Event Simulation: Simulate bus coordination scenarios and passenger flows",
                "Agent-Based Simulation: Model operator behavior and passenger responses to coordination"
            ],
            'Typhoon Signal Data Analysis': [
                "Linear Regression: Analyze relationships between weather data and signal timing decisions",
                "Logistic Regression: Predict signal issuance decisions based on meteorological factors",
                "Time Series Regression: Model signal timing patterns and forecast accuracy",
                "Weather Event Simulation: Simulate typhoon scenarios and warning system responses",
                "Decision Impact Simulation: Model outcomes of different warning timing strategies"
            ],
            'Municipal Solid Waste Charging Scheme': [
                "Linear Regression: Analyze relationships between charging rates and waste reduction",
                "Multiple Regression: Model waste generation based on multiple demographic and policy factors",
                "Price Elasticity Regression: Estimate demand response to different charging levels",
                "Policy Implementation Simulation: Model waste charging scheme rollout scenarios",
                "Behavioral Change Simulation: Simulate community responses to different charging structures"
            ],
            'Green@Community Recycling Network Analysis': [
                "Linear Regression: Analyze relationships between center characteristics and recycling rates",
                "Multiple Regression: Model participation based on accessibility and community factors",
                "Efficiency Regression: Analyze factors affecting recycling center performance",
                "Network Optimization Simulation: Simulate different recycling center configurations",
                "Community Engagement Simulation: Model participation growth under different outreach strategies"
            ],
            'Bus Stop Merger Optimization': [
                "Linear Regression: Analyze relationships between stop spacing and passenger convenience",
                "Multiple Regression: Model ridership changes based on merger characteristics",
                "Accessibility Regression: Analyze walking distance impacts on different population groups",
                "Service Impact Simulation: Simulate merger scenarios and passenger flow changes",
                "Cost-Benefit Simulation: Model financial and social impacts of different merger strategies"
            ]
        }
        
        return model_suggestions.get(topic, ["Regression and simulation models to be determined with instructor guidance"])

    def read_current_document(self):
        """Read the current instructor collaboration document"""
        try:
            doc = self.docs_service.documents().get(documentId=self.instructor_doc_id).execute()
            content = doc.get('body', {}).get('content', [])
            
            # Extract text content
            full_text = ""
            for element in content:
                if 'paragraph' in element:
                    paragraph = element['paragraph']
                    for text_element in paragraph.get('elements', []):
                        if 'textRun' in text_element:
                            full_text += text_element['textRun']['content']
            
            return full_text
        except Exception as e:
            print(f"❌ Error reading document: {str(e)}")
            return None

    def update_models_section(self):
        """Update the mathematical models sections for all teams"""
        print("📝 Updating mathematical models sections...")
        
        try:
            # Read current document
            current_content = self.read_current_document()
            if not current_content:
                return False
            
            # Update models for each team
            updated_content = current_content
            
            teams_topics = {
                'TEAM_1': 'Flu Shot Participation Analysis',
                'TEAM_2': 'Inter-Company Bus Route Coordination', 
                'TEAM_3': 'Typhoon Signal Data Analysis',
                'TEAM_4': 'Municipal Solid Waste Charging Scheme',
                'TEAM_5': 'Green@Community Recycling Network Analysis',
                'TEAM_6': 'Bus Stop Merger Optimization'
            }
            
            for team_key, topic in teams_topics.items():
                # Find the mathematical models section for this team
                models_start = updated_content.find(f"🔢 MATHEMATICAL MODELS TO EXPLORE:\nRecommended analytical approaches for this project:")
                if models_start == -1:
                    continue
                
                # Find the team section
                team_start = updated_content.find(f"{team_key} -")
                if team_start == -1:
                    continue
                
                # Find the models section within this team
                team_models_start = updated_content.find("🔢 MATHEMATICAL MODELS TO EXPLORE:", team_start)
                if team_models_start == -1:
                    continue
                
                # Find the end of the models section (next 📋 or next team)
                models_end = updated_content.find("📋 AVAILABLE RESOURCES:", team_models_start)
                if models_end == -1:
                    models_end = updated_content.find("TEAM_", team_models_start + 1)
                    if models_end == -1:
                        models_end = len(updated_content)
                
                # Get new models for this topic
                new_models = self.get_updated_models_for_topic(topic)
                
                # Create the replacement text
                models_section = "🔢 MATHEMATICAL MODELS TO EXPLORE:\n"
                models_section += "⚠️ IMPORTANT: Focus on REGRESSION and SIMULATION models only for this course.\n"
                models_section += "Please consult with instructors before selecting your final analytical approach.\n\n"
                models_section += "Recommended regression and simulation approaches for this project:\n"
                
                for i, model in enumerate(new_models, 1):
                    models_section += f"{i}. {model}\n"
                
                models_section += "\n💡 INSTRUCTOR CONSULTATION REQUIRED:\n"
                models_section += "• Discuss model selection with Dr. Wang or Dr. Wu before implementation\n"
                models_section += "• Consider data availability and complexity when choosing approaches\n"
                models_section += "• Start with simpler regression models before advancing to simulation\n"
                models_section += "• Ensure selected models align with your research questions and data\n\n"
                
                # Replace the section
                old_section = updated_content[team_models_start:models_end]
                old_models_end = old_section.find("📋 AVAILABLE RESOURCES:")
                if old_models_end == -1:
                    old_models_end = old_section.find("TEAM_")
                    if old_models_end == -1:
                        old_models_end = len(old_section)
                
                old_models_section = old_section[:old_models_end]
                replacement = models_section
                
                updated_content = updated_content.replace(old_models_section, replacement)
            
            # Add general guidance update
            general_section_start = updated_content.find("GENERAL PROJECT GUIDANCE FOR ALL TEAMS")
            if general_section_start != -1:
                week_priorities_start = updated_content.find("WEEK 1-2 PRIORITIES:", general_section_start)
                if week_priorities_start != -1:
                    model_line_start = updated_content.find("□ Model Selection:", week_priorities_start)
                    if model_line_start != -1:
                        model_line_end = updated_content.find("\n", model_line_start)
                        old_line = updated_content[model_line_start:model_line_end]
                        new_line = "□ Model Selection: Choose 1-2 regression or simulation approaches WITH INSTRUCTOR CONSULTATION"
                        updated_content = updated_content.replace(old_line, new_line)
            
            # Update the document
            doc = self.docs_service.documents().get(documentId=self.instructor_doc_id).execute()
            content = doc.get('body', {}).get('content', [])
            
            # Calculate document length
            doc_length = 1
            for element in content:
                if 'paragraph' in element:
                    for text_element in element['paragraph'].get('elements', []):
                        if 'textRun' in text_element:
                            doc_length += len(text_element['textRun']['content'])
            
            # Clear and replace content
            requests = [
                {
                    'deleteContentRange': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': doc_length - 1
                        }
                    }
                },
                {
                    'insertText': {
                        'location': {'index': 1},
                        'text': updated_content
                    }
                }
            ]
            
            self.docs_service.documents().batchUpdate(
                documentId=self.instructor_doc_id,
                body={'requests': requests}
            ).execute()
            
            print("✅ Successfully updated mathematical models sections")
            print("🔗 Updated document: https://docs.google.com/document/d/1Vd98A1bFDgJrMj8UiKLrOYdIauP0rr-Ca7kz4A6Hu80")
            return True
            
        except Exception as e:
            print(f"❌ Error updating models section: {str(e)}")
            return False

    def run_update(self):
        """Execute the models section update"""
        print("🔄 Updating Mathematical Models to Focus on Regression and Simulation")
        print("="*70)
        
        success = self.update_models_section()
        
        if success:
            print("\n🎉 Mathematical models sections updated successfully!")
            print("\n📋 Changes made:")
            print("• Limited models to regression and simulation approaches only")
            print("• Added instructor consultation requirements")
            print("• Updated guidance to emphasize teacher consultation for model selection")
            print("• Added warnings about complexity and data requirements")
            
            print(f"\n📄 Next steps:")
            print("1. Review the updated document")
            print("2. Sync notes to team folders if needed")
            print("3. Inform students about the updated model requirements")
        else:
            print("\n❌ Failed to update mathematical models sections")

def main():
    """Main execution function"""
    try:
        updater = ModelSectionUpdater()
        updater.run_update()
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
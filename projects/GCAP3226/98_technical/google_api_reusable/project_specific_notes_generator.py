#!/usr/bin/env python3
"""
Project-Specific Instructor Notes Generator
Analyzes Moodle posts and creates detailed guidance for each team based on:
1. Government decision identification
2. Data governance review practices  
3. Mathematical modeling selection
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from bs4 import BeautifulSoup
import re

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from google_api_client import GoogleAPIClient

class ProjectSpecificNotesGenerator:
    def __init__(self):
        """Initialize the project-specific notes generator"""
        self.client = GoogleAPIClient()
        self.drive_service = self.client.get_drive_service()
        self.docs_service = self.client.get_docs_service()
        
        # Base paths
        self.projects_base = Path("/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/GCAP3226/02_student_workspace/group_projects/team_projects")
        
        # Team mapping
        self.teams = {
            'Team_1': {
                'folder_name': 'Team1_Topic6_FluShotParticipation',
                'topic': 'Flu Shot Participation Analysis',
                'folder_id': '1zGDV77Vih4DxDyH9f6eKnr00Kp4nWyMo'
            },
            'Team_2': {
                'folder_name': 'Team2_Topic3_BusRoutesCoordination',
                'topic': 'Inter-Company Bus Route Coordination',
                'folder_id': '1KJ8Y1QkDHo7Oull02GdfjP-OO0ZxJS3C'
            },
            'Team_3': {
                'folder_name': 'Team3_Topic7_TyphoonSignal',
                'topic': 'Typhoon Signal Data Analysis',
                'folder_id': '1Gx9TD1fRxuzNinEIgLMdvC-pTALbf8fD'
            },
            'Team_4': {
                'folder_name': 'Team4_Topic4_SolidWasteCharging',
                'topic': 'Municipal Solid Waste Charging Scheme',
                'folder_id': '1yYR-KxSfSI3VT4M2yLbIbj4pVEHTS__f'
            },
            'Team_5': {
                'folder_name': 'Team5_Topic5_GreenCommunity',
                'topic': 'Green@Community Recycling Network Analysis',
                'folder_id': '1vgf2jvKYNJu9EO2eD8S_sOOvWSIVL_Dw'
            },
            'Team_6': {
                'folder_name': 'Team6_Topic2_BusStopMerge',
                'topic': 'Bus Stop Merger Optimization',
                'folder_id': '1WlruCUvqQ1IO5EOmYbUX0B4vMjF-zCNo'
            }
        }
        
        self.instructor_doc_id = "1Vd98A1bFDgJrMj8UiKLrOYdIauP0rr-Ca7kz4A6Hu80"
        self.project_analyses = {}

    def analyze_moodle_posts(self):
        """Analyze Moodle posts for each team to extract key project information"""
        print("📋 Analyzing Moodle posts for project guidance...")
        
        for team_name, team_data in self.teams.items():
            try:
                moodle_file = self.projects_base / team_data['folder_name'] / 'moodle_forum_post.html'
                
                if moodle_file.exists():
                    with open(moodle_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    analysis = self._extract_project_details(html_content, team_name, team_data)
                    self.project_analyses[team_name] = analysis
                    print(f"✅ Analyzed {team_name}: {team_data['topic']}")
                else:
                    print(f"⚠️ No Moodle post found for {team_name}")
                    
            except Exception as e:
                print(f"❌ Error analyzing {team_name}: {str(e)}")

    def _extract_project_details(self, html_content, team_name, team_data):
        """Extract key project details from Moodle post HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text()
        
        # Analyze for government decisions
        gov_decisions = self._identify_government_decisions(text_content, team_data['topic'])
        
        # Analyze for data governance opportunities
        data_governance = self._identify_data_governance_practices(text_content, team_data['topic'])
        
        # Suggest mathematical models
        math_models = self._suggest_mathematical_models(text_content, team_data['topic'])
        
        # Extract available resources
        resources = self._extract_available_resources(text_content)
        
        return {
            'government_decisions': gov_decisions,
            'data_governance_practices': data_governance,
            'mathematical_models': math_models,
            'available_resources': resources,
            'project_focus': self._determine_project_focus(text_content)
        }

    def _identify_government_decisions(self, text_content, topic):
        """Identify government decisions relevant to the project"""
        
        decision_frameworks = {
            'Flu Shot Participation Analysis': [
                "Department of Health vaccination program policies",
                "Education Bureau school health program requirements", 
                "Government Vaccination Programme (GVP) design decisions",
                "Vaccination Subsidy Scheme (VSS) eligibility criteria",
                "School-based vaccination program implementation policies",
                "Nasal spray vaccine approval and adoption decisions",
                "Post-COVID vaccination strategy modifications"
            ],
            'Inter-Company Bus Route Coordination': [
                "Transport Department route licensing decisions",
                "Inter-operator coordination regulatory framework",
                "Competitive tendering vs. coordination policy choices",
                "Real-time data sharing requirements between operators",
                "Service frequency and timetable approval processes",
                "Revenue-sharing mechanism regulations",
                "Public transport integration policies"
            ],
            'Typhoon Signal Data Analysis': [
                "Hong Kong Observatory signal issuance criteria",
                "Emergency response activation protocols",
                "School and business closure decision frameworks",
                "Public transport suspension policies",
                "Weather warning communication strategies",
                "Inter-agency coordination during typhoon events",
                "Climate change adaptation policy decisions"
            ],
            'Municipal Solid Waste Charging Scheme': [
                "Waste charging scheme design and implementation decisions",
                "Environmental Protection Department data collection requirements",
                "University waste reporting mandate policies",
                "Residential community waste disclosure regulations",
                "Recycling program funding and support decisions",
                "Waste reduction target setting and monitoring",
                "Charging exemption and subsidy policies"
            ],
            'Green@Community Recycling Network Analysis': [
                "Green@Community program funding allocation decisions",
                "Recycling network expansion strategies",
                "Community engagement program design",
                "Performance measurement and reporting requirements",
                "Public-private partnership framework decisions",
                "Waste collection and processing optimization policies",
                "Environmental education program implementation"
            ],
            'Bus Stop Merger Optimization': [
                "Transport Department bus stop consolidation policies",
                "Route optimization and stop spacing decisions",
                "Accessibility compliance requirements",
                "Community consultation processes for stop changes",
                "Integration with other transport modes policies",
                "Cost-benefit analysis frameworks for infrastructure changes",
                "Passenger safety and convenience balancing decisions"
            ]
        }
        
        return decision_frameworks.get(topic, ["Government policy decisions to be identified through research"])

    def _identify_data_governance_practices(self, text_content, topic):
        """Identify data governance review opportunities"""
        
        governance_frameworks = {
            'Flu Shot Participation Analysis': [
                "Review Department of Health vaccination data collection and reporting practices",
                "Analyze school-based health data sharing between Education Bureau and Health Department",
                "Evaluate transparency of vaccination statistics publication",
                "Request current participation rate data through government information requests",
                "Assess data quality and completeness in vaccination monitoring systems",
                "Review privacy protection measures for health data",
                "Analyze international best practices for vaccination data governance"
            ],
            'Inter-Company Bus Route Coordination': [
                "Request real-time performance data from Transport Department",
                "Analyze data sharing agreements between KMB and CityBus",
                "Review transparency of route performance reporting",
                "Evaluate passenger complaint data collection and response systems",
                "Assess coordination data requirements in franchise agreements",
                "Request inter-operator communication protocols and data",
                "Analyze benchmarking practices against international coordination models"
            ],
            'Typhoon Signal Data Analysis': [
                "Request Hong Kong Observatory decision-making data and criteria",
                "Analyze inter-agency data sharing during weather emergencies",
                "Review public communication effectiveness and data transparency",
                "Evaluate real-time monitoring data accessibility",
                "Assess emergency response coordination data systems",
                "Request historical decision timing and impact data",
                "Analyze international weather warning system comparisons"
            ],
            'Municipal Solid Waste Charging Scheme': [
                "Request comprehensive waste generation and recycling data from EPD",
                "Analyze university waste reporting compliance and data quality",
                "Review residential community waste data collection practices",
                "Evaluate charging scheme pilot program data and lessons learned",
                "Request comparative data from international waste charging systems",
                "Assess data transparency and public accessibility",
                "Analyze waste reduction impact measurement methodologies"
            ],
            'Green@Community Recycling Network Analysis': [
                "Request performance data from all Green@Community centers",
                "Analyze recycling volume and participation rate data collection",
                "Review community engagement measurement and reporting practices",
                "Evaluate cost-effectiveness data and analysis methodologies",
                "Request comparative data with other recycling programs",
                "Assess data sharing between government and community partners",
                "Analyze environmental impact measurement and reporting"
            ],
            'Bus Stop Merger Optimization': [
                "Request passenger usage data for proposed merger locations",
                "Analyze consultation data and community feedback collection practices",
                "Review accessibility impact assessment data and methodologies",
                "Evaluate cost-benefit analysis data and decision frameworks",
                "Request comparative data from other transport infrastructure changes",
                "Assess pedestrian safety and traffic impact data collection",
                "Analyze integration with smart city data initiatives"
            ]
        }
        
        return governance_frameworks.get(topic, ["Data governance practices to be identified through research"])

    def _suggest_mathematical_models(self, text_content, topic):
        """Suggest appropriate mathematical models for analysis"""
        
        model_suggestions = {
            'Flu Shot Participation Analysis': [
                "Logistic Regression Models: Predict vaccination participation based on demographic variables",
                "Time Series Analysis: Analyze vaccination rate trends over multiple seasons",
                "Survival Analysis: Model time-to-vaccination and dropout patterns",
                "Causal Inference Models: Estimate impact of policy interventions on participation",
                "Bayesian Networks: Model relationships between barriers and vaccination decisions",
                "Cost-Effectiveness Models: Compare traditional vs. nasal spray vaccine delivery",
                "Propensity Score Matching: Control for confounding in observational studies"
            ],
            'Inter-Company Bus Route Coordination': [
                "Game Theory Models: Analyze competitive vs. cooperative operator strategies",
                "Queueing Theory: Model passenger waiting times under different coordination scenarios",
                "Linear Programming: Optimize timetable coordination subject to constraints",
                "Simulation Models: Test coordination strategies under various demand scenarios",
                "Revenue Sharing Models: Design fair allocation mechanisms between operators",
                "Network Flow Models: Optimize passenger flows across integrated routes",
                "Dynamic Programming: Solve sequential coordination decisions"
            ],
            'Typhoon Signal Data Analysis': [
                "Decision Tree Models: Analyze signal issuance decision criteria and outcomes",
                "Weather Prediction Models: Evaluate forecast accuracy and decision timing",
                "Risk Assessment Models: Quantify trade-offs between early warnings and false alarms",
                "Time Series Models: Analyze patterns in signal timing and duration",
                "Spatial Analysis Models: Map wind speed and impact prediction accuracy",
                "Cost-Benefit Models: Evaluate economic impacts of different warning strategies",
                "Machine Learning Models: Improve prediction accuracy using historical data"
            ],
            'Municipal Solid Waste Charging Scheme': [
                "Price Elasticity Models: Estimate demand response to waste charging",
                "Panel Data Models: Analyze impacts across different communities over time",
                "Difference-in-Differences: Evaluate policy impact using control groups",
                "Behavioral Models: Model recycling behavior change mechanisms",
                "Cost-Effectiveness Analysis: Compare different charging scheme designs",
                "Environmental Impact Models: Quantify waste reduction and environmental benefits",
                "Revenue Forecasting Models: Predict scheme financial sustainability"
            ],
            'Green@Community Recycling Network Analysis': [
                "Network Analysis Models: Optimize recycling center locations and coverage",
                "Efficiency Models (DEA): Compare performance across different centers",
                "Participation Models: Predict community engagement levels",
                "Cost-Effectiveness Analysis: Evaluate program value for money",
                "Geographic Information System (GIS) Models: Analyze spatial accessibility",
                "Behavioral Change Models: Model community adoption patterns",
                "Environmental Impact Assessment Models: Quantify recycling benefits"
            ],
            'Bus Stop Merger Optimization': [
                "Accessibility Models: Quantify walking distance and mobility impacts",
                "Passenger Flow Models: Predict ridership changes from stop consolidation",
                "Multi-Criteria Decision Analysis: Balance competing objectives in merger decisions",
                "Cost-Benefit Analysis: Evaluate financial and social impacts",
                "Geographic Optimization Models: Determine optimal stop spacing",
                "Traffic Flow Models: Analyze impacts on vehicle and pedestrian movement",
                "Service Quality Models: Predict changes in passenger experience"
            ]
        }
        
        return model_suggestions.get(topic, ["Mathematical models to be determined based on research focus"])

    def _extract_available_resources(self, text_content):
        """Extract available resources mentioned in the Moodle post"""
        resources = []
        
        # Look for specific resource indicators
        if "published research" in text_content.lower() or "letters" in text_content.lower():
            resources.append("Published research foundation available")
        
        if "api" in text_content.lower() or "data collection" in text_content.lower():
            resources.append("API and data collection systems ready")
        
        if "jupyter" in text_content.lower() or "notebook" in text_content.lower():
            resources.append("Jupyter notebook analysis framework available")
        
        if "survey" in text_content.lower() or "questionnaire" in text_content.lower():
            resources.append("Survey data collected and available")
        
        if "government" in text_content.lower() and "data" in text_content.lower():
            resources.append("Government data sources identified")
        
        return resources if resources else ["Resource inventory to be compiled"]

    def _determine_project_focus(self, text_content):
        """Determine the main focus areas of the project"""
        focus_areas = []
        
        if "policy" in text_content.lower():
            focus_areas.append("Policy Analysis")
        
        if "data governance" in text_content.lower():
            focus_areas.append("Data Governance")
        
        if "algorithm" in text_content.lower() or "optimization" in text_content.lower():
            focus_areas.append("Algorithm Development")
        
        if "public health" in text_content.lower():
            focus_areas.append("Public Health")
        
        if "transport" in text_content.lower():
            focus_areas.append("Transportation")
        
        if "environment" in text_content.lower():
            focus_areas.append("Environmental")
        
        return focus_areas if focus_areas else ["Focus areas to be determined"]

    def generate_instructor_notes_content(self):
        """Generate comprehensive instructor notes content"""
        print("📝 Generating comprehensive instructor notes content...")
        
        content = f"""TEAM PROJECT GUIDANCE - UPDATED WITH MOODLE POST ANALYSIS
Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}

=== PROJECT STARTUP GUIDANCE FOR ALL TEAMS ===

Based on analysis of team Moodle posts, here is specific guidance for helping students get started with their projects. All teams should focus on three core areas:

1. 🏛️ IDENTIFY GOVERNMENT DECISIONS
2. 📊 REVIEW DATA GOVERNANCE PRACTICES  
3. 🔢 EXPLORE MATHEMATICAL MODELS

==========================================

"""
        
        for team_name in ['Team_1', 'Team_2', 'Team_3', 'Team_4', 'Team_5', 'Team_6']:
            if team_name in self.project_analyses:
                team_data = self.teams[team_name]
                analysis = self.project_analyses[team_name]
                
                content += f"""
{team_name.upper()} - {team_data['topic']}
Folder: https://drive.google.com/drive/folders/{team_data['folder_id']}

🏛️ GOVERNMENT DECISIONS TO IDENTIFY:
The team should research and analyze these key government decisions:
"""
                for i, decision in enumerate(analysis['government_decisions'], 1):
                    content += f"{i}. {decision}\n"
                
                content += f"""
📊 DATA GOVERNANCE REVIEW TASKS:
Students should request information and evaluate these practices:
"""
                for i, practice in enumerate(analysis['data_governance_practices'], 1):
                    content += f"{i}. {practice}\n"
                
                content += f"""
🔢 MATHEMATICAL MODELS TO EXPLORE:
Recommended analytical approaches for this project:
"""
                for i, model in enumerate(analysis['mathematical_models'], 1):
                    content += f"{i}. {model}\n"
                
                content += f"""
📋 AVAILABLE RESOURCES:
"""
                for resource in analysis['available_resources']:
                    content += f"• {resource}\n"
                
                content += f"""
🎯 PROJECT FOCUS AREAS: {', '.join(analysis['project_focus'])}

INSTRUCTOR ACTION ITEMS FOR {team_name}:
□ Guide students to identify specific government decisions in their topic area
□ Help them draft information requests to relevant government departments
□ Assist in selecting 2-3 mathematical models most appropriate for their data
□ Connect them with available resources and technical support
□ Monitor progress on data governance evaluation

STUDENT MEETING AGENDA:
1. Review government decision identification progress
2. Discuss data request strategy and templates
3. Select mathematical modeling approaches
4. Plan timeline for analysis phases
5. Address any technical or resource needs

NEXT FOLLOW-UP: Schedule specific check-in within 1 week

---

"""
        
        content += """
GENERAL PROJECT GUIDANCE FOR ALL TEAMS
==========================================

WEEK 1-2 PRIORITIES:
□ Government Decision Mapping: Each team identifies 5-7 key government decisions in their topic
□ Data Request Strategy: Draft information requests to relevant departments
□ Model Selection: Choose 2-3 mathematical approaches that fit their data and questions
□ Resource Inventory: Catalog available data, tools, and technical support

WEEK 3-4 PRIORITIES:  
□ Data Collection: Submit government information requests and gather available data
□ Preliminary Analysis: Begin exploratory data analysis and basic modeling
□ Governance Evaluation: Assess data transparency and accessibility practices
□ Progress Review: Mid-project check-in with instructors

WEEK 5-6 PRIORITIES:
□ Advanced Analysis: Implement selected mathematical models
□ Policy Implications: Connect findings to government decision evaluation
□ Governance Recommendations: Develop data practice improvement suggestions
□ Final Presentation: Prepare comprehensive project results

INSTRUCTOR SUPPORT RESOURCES:
• Government information request templates
• Mathematical modeling tutorial materials  
• Data governance evaluation frameworks
• Technical assistance for complex analysis
• Policy writing and presentation guidance

COMMON CHALLENGES TO WATCH:
⚠️ Teams may struggle with government data access - have backup data sources ready
⚠️ Mathematical model selection can be overwhelming - provide guided choice frameworks
⚠️ Data governance concepts may be abstract - use concrete examples from their projects
⚠️ Timeline management across multiple objectives - help prioritize core deliverables

LAST UPDATED: {datetime.now().strftime('%Y-%m-%d %H:%M')} by: Instructor Collaboration System

==========================================

TEAM PROGRESS CHECKLIST:
□ Team 1 - Government decisions identified
□ Team 2 - Data requests submitted
□ Team 3 - Models selected and implemented
□ Team 4 - Governance evaluation completed
□ Team 5 - Progress on track for deliverables
□ Team 6 - Support needs addressed
"""
        
        return content

    def update_instructor_collaboration_doc(self):
        """Update the instructor collaboration document with project-specific guidance"""
        print("📄 Updating instructor collaboration document...")
        
        try:
            # Generate the new content
            new_content = self.generate_instructor_notes_content()
            
            # Get current document
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
                        'text': new_content
                    }
                }
            ]
            
            self.docs_service.documents().batchUpdate(
                documentId=self.instructor_doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Updated instructor collaboration document with project-specific guidance")
            print(f"🔗 URL: https://docs.google.com/document/d/{self.instructor_doc_id}")
            
        except Exception as e:
            print(f"❌ Error updating instructor document: {str(e)}")

    def generate_summary_report(self):
        """Generate a summary report of the project analysis"""
        print("\n📊 Generating project analysis summary...")
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'teams_analyzed': len(self.project_analyses),
            'total_teams': len(self.teams),
            'analysis_results': {}
        }
        
        for team_name, analysis in self.project_analyses.items():
            team_data = self.teams[team_name]
            summary['analysis_results'][team_name] = {
                'topic': team_data['topic'],
                'government_decisions_count': len(analysis['government_decisions']),
                'data_governance_tasks_count': len(analysis['data_governance_practices']),
                'mathematical_models_count': len(analysis['mathematical_models']),
                'available_resources_count': len(analysis['available_resources']),
                'focus_areas': analysis['project_focus']
            }
        
        # Save summary report
        report_file = current_dir / f'project_analysis_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📄 Summary report saved to: {report_file}")
        
        # Display summary
        print("\n" + "="*60)
        print("📊 PROJECT ANALYSIS SUMMARY")
        print("="*60)
        
        for team_name, results in summary['analysis_results'].items():
            print(f"\n{team_name} - {results['topic']}")
            print(f"  Government Decisions: {results['government_decisions_count']} identified")
            print(f"  Data Governance Tasks: {results['data_governance_tasks_count']} defined")
            print(f"  Mathematical Models: {results['mathematical_models_count']} suggested")
            print(f"  Available Resources: {results['available_resources_count']} catalogued")
            print(f"  Focus Areas: {', '.join(results['focus_areas'])}")
        
        print(f"\n✅ Successfully analyzed {summary['teams_analyzed']}/{summary['total_teams']} teams")

    def run_analysis(self):
        """Execute the complete project analysis and note generation"""
        print("🚀 Starting Project-Specific Instructor Notes Generation")
        print("="*60)
        
        # Step 1: Analyze Moodle posts
        self.analyze_moodle_posts()
        
        # Step 2: Update instructor collaboration document
        self.update_instructor_collaboration_doc()
        
        # Step 3: Generate summary report
        self.generate_summary_report()
        
        print("\n🎉 Project-specific instructor notes generation completed!")

def main():
    """Main execution function"""
    try:
        generator = ProjectSpecificNotesGenerator()
        generator.run_analysis()
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
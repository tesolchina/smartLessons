#!/usr/bin/env python3
"""
Quick Afternoon Edits for Innovation Officer
Provides specific line numbers, exact text changes, and reasons for maximum impact in minimal time
"""

from pathlib import Path
import re

class AfternoonEditGenerator:
    """Generate specific line-by-line edits for busy managers"""
    
    def __init__(self):
        self.base_dir = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/LC_admin/PMC")
        self.priority_edits = []
    
    def analyze_file_for_quick_wins(self, filename: str) -> list:
        """Find highest-impact, lowest-effort edits in specific file"""
        filepath = self.base_dir / filename
        
        if not filepath.exists():
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        edits = []
        
        # Scan each line for enhancement opportunities
        for i, line in enumerate(lines):
            line_num = i + 1
            line_text = line.strip()
            
            # Look for AI mentions that can be strengthened
            if 'AI competency' in line_text and 'measurable' not in line_text:
                edits.append({
                    'file': filename,
                    'line': line_num,
                    'current_text': line_text,
                    'suggested_change': line_text.replace('AI competency', 'measurable AI competency with rubric-based assessment'),
                    'reason': 'Makes AI competency concrete and assessable',
                    'effort': 'LOW',
                    'impact': 'HIGH',
                    'time_estimate': '30 seconds'
                })
            
            # Look for vague implementation language
            if 'will be' in line_text and 'by' not in line_text and ('AI' in line_text or 'integrate' in line_text):
                enhanced_text = line_text.replace('will be', 'will be completed by AY 2025-26')
                edits.append({
                    'file': filename,
                    'line': line_num,
                    'current_text': line_text,
                    'suggested_change': enhanced_text,
                    'reason': 'Adds specific timeline for accountability',
                    'effort': 'LOW',
                    'impact': 'MEDIUM',
                    'time_estimate': '20 seconds'
                })
            
            # Look for training mentions without specifics
            if 'training' in line_text.lower() and 'monthly' not in line_text and 'workshop' not in line_text:
                if 'AI' in line_text:
                    enhanced_text = line_text.replace('training', 'monthly AI innovation workshops')
                    edits.append({
                        'file': filename,
                        'line': line_num,
                        'current_text': line_text,
                        'suggested_change': enhanced_text,
                        'reason': 'Specifies regular AI training schedule',
                        'effort': 'LOW',
                        'impact': 'HIGH',
                        'time_estimate': '25 seconds'
                    })
            
            # Look for assessment mentions without AI enhancement
            if 'assessment' in line_text.lower() and 'AI' not in line_text and len(line_text) > 30:
                enhanced_text = line_text.rstrip() + ' with AI-assisted feedback systems'
                edits.append({
                    'file': filename,
                    'line': line_num,
                    'current_text': line_text,
                    'suggested_change': enhanced_text,
                    'reason': 'Integrates AI innovation into core assessment',
                    'effort': 'LOW',
                    'impact': 'MEDIUM',
                    'time_estimate': '30 seconds'
                })
        
        return edits
    
    def find_strategic_insertion_points(self, filename: str) -> list:
        """Find places where single line additions create maximum impact"""
        filepath = self.base_dir / filename
        
        if not filepath.exists():
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        insertions = []
        
        for i, line in enumerate(lines):
            line_text = line.strip()
            
            # After headings, suggest strategic additions
            if line_text.startswith('##') and 'AI' not in line_text:
                if 'Strategic' in line_text or 'Direction' in line_text:
                    insertions.append({
                        'file': filename,
                        'insert_after_line': i + 1,
                        'text_to_insert': '**AI Innovation Priority:** Integrate AI competency development across all LC programs by AY 2025-26.',
                        'reason': 'Establishes Innovation Officer leadership visibility',
                        'effort': 'LOW',
                        'impact': 'HIGH',
                        'time_estimate': '45 seconds'
                    })
                
                elif 'Assessment' in line_text:
                    insertions.append({
                        'file': filename,
                        'insert_after_line': i + 1,
                        'text_to_insert': '**AI Assessment Pilot:** 50% of courses will trial AI-enhanced feedback systems by end of AY 2025-26.',
                        'reason': 'Concrete AI initiative with measurable target',
                        'effort': 'LOW',
                        'impact': 'HIGH',
                        'time_estimate': '50 seconds'
                    })
                
                elif 'Professional Development' in line_text or 'Staff' in line_text:
                    insertions.append({
                        'file': filename,
                        'insert_after_line': i + 1,
                        'text_to_insert': '**AI Faculty Training:** Monthly workshops on AI tool integration, assessment methods, and ethical usage.',
                        'reason': 'Shows systematic approach to AI capacity building',
                        'effort': 'LOW',
                        'impact': 'MEDIUM',
                        'time_estimate': '40 seconds'
                    })
        
        return insertions
    
    def generate_afternoon_action_plan(self) -> dict:
        """Generate prioritized edit plan for one afternoon session"""
        
        files_to_check = [
            'enhanced_01_scope_strategic_direction.md',
            'enhanced_02_staffing.md',
            'enhanced_03_teaching_learning.md'
        ]
        
        all_edits = []
        all_insertions = []
        
        for filename in files_to_check:
            all_edits.extend(self.analyze_file_for_quick_wins(filename))
            all_insertions.extend(self.find_strategic_insertion_points(filename))
        
        # Sort by impact and effort
        high_impact_edits = [e for e in all_edits if e['impact'] == 'HIGH']
        medium_impact_edits = [e for e in all_edits if e['impact'] == 'MEDIUM']
        
        high_impact_insertions = [i for i in all_insertions if i['impact'] == 'HIGH']
        medium_impact_insertions = [i for i in all_insertions if i['impact'] == 'MEDIUM']
        
        action_plan = {
            'session_overview': {
                'total_time_needed': '2-3 hours',
                'high_priority_items': len(high_impact_edits) + len(high_impact_insertions),
                'total_items': len(all_edits) + len(all_insertions),
                'focus': 'AI competency integration and measurable outcomes'
            },
            'immediate_actions': high_impact_edits[:5] + high_impact_insertions[:3],
            'secondary_actions': medium_impact_edits[:5] + medium_impact_insertions[:2],
            'time_breakdown': {
                'immediate_actions_time': '30-45 minutes',
                'secondary_actions_time': '45-60 minutes',
                'review_and_finalize_time': '30 minutes'
            }
        }
        
        return action_plan
    
    def create_copy_paste_guide(self, action_plan: dict) -> str:
        """Create ready-to-use edit instructions"""
        
        guide = f"""# Innovation Officer Afternoon Edit Session

## Session Overview
- **Total Time:** {action_plan['session_overview']['total_time_needed']}
- **High Priority Items:** {action_plan['session_overview']['high_priority_items']}
- **Focus:** {action_plan['session_overview']['focus']}

## Phase 1: Immediate Actions (30-45 minutes)

"""
        
        for i, action in enumerate(action_plan['immediate_actions'], 1):
            if 'line' in action:  # This is an edit
                guide += f"""### Edit {i}: {action['file']}
**Line {action['line']}**
- **Current:** `{action['current_text']}`
- **Change to:** `{action['suggested_change']}`
- **Why:** {action['reason']}
- **Time:** {action['time_estimate']}

"""
            else:  # This is an insertion
                guide += f"""### Insert {i}: {action['file']}  
**After line {action['insert_after_line']}**
- **Add:** `{action['text_to_insert']}`
- **Why:** {action['reason']}
- **Time:** {action['time_estimate']}

"""
        
        guide += "## Phase 2: Secondary Actions (45-60 minutes)\n\n"
        
        for i, action in enumerate(action_plan['secondary_actions'], 1):
            if 'line' in action:
                guide += f"""### Edit {i}: {action['file']}
**Line {action['line']}** - {action['reason']}
- Current: `{action['current_text'][:50]}...`
- Change to: `{action['suggested_change'][:50]}...`

"""
            else:
                guide += f"""### Insert {i}: {action['file']}
**After line {action['insert_after_line']}** - {action['reason']}
- Add: `{action['text_to_insert'][:50]}...`

"""
        
        guide += f"""
## Time Management
- **Phase 1:** {action_plan['time_breakdown']['immediate_actions_time']}
- **Phase 2:** {action_plan['time_breakdown']['secondary_actions_time']}  
- **Review:** {action_plan['time_breakdown']['review_and_finalize_time']}

## Success Checklist
- [ ] All HIGH impact edits completed
- [ ] AI competency mentions made measurable
- [ ] Timelines added to implementation items
- [ ] Innovation Officer visibility established
- [ ] Files saved and ready for use

*Estimated total session time: {action_plan['session_overview']['total_time_needed']}*
"""
        
        return guide
    
    def save_afternoon_plan(self):
        """Generate and save the afternoon edit plan"""
        
        print("🔍 Analyzing files for quick-win edits...")
        action_plan = self.generate_afternoon_action_plan()
        
        print("📝 Creating copy-paste edit guide...")
        guide_content = self.create_copy_paste_guide(action_plan)
        
        # Save the guide
        output_path = self.base_dir / 'Afternoon_Edit_Session_Guide.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        # Save JSON for programmatic access
        import json
        json_path = self.base_dir / 'Afternoon_Edit_Plan.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(action_plan, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Afternoon edit guide saved: {output_path}")
        print(f"✅ JSON plan saved: {json_path}")
        
        # Print summary
        print(f"\n🎯 Session Summary:")
        print(f"   • {action_plan['session_overview']['high_priority_items']} high-priority items")
        print(f"   • Total time: {action_plan['session_overview']['total_time_needed']}")
        print(f"   • Focus: {action_plan['session_overview']['focus']}")

def main():
    """Generate afternoon edit session plan"""
    
    print("⏰ Creating manageable afternoon edit session for Innovation Officer...")
    
    generator = AfternoonEditGenerator()
    generator.save_afternoon_plan()
    
    print("\n📋 Next Steps:")
    print("1. Open 'Afternoon_Edit_Session_Guide.md' for step-by-step instructions")
    print("2. Start with Phase 1 (HIGH impact items)")
    print("3. Use copy-paste text provided for each edit")
    print("4. Complete session in 2-3 hours maximum")

if __name__ == "__main__":
    main()

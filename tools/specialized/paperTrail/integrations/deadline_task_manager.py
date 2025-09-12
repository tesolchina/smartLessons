#!/usr/bin/env python3
"""
Deadline Task Manager - Analyze and manage deadline files
"""

import os
import re
from pathlib import Path
from datetime import datetime, timedelta
import json

def analyze_deadline_urgency(deadline_files_dir):
    """Analyze deadlines and categorize by urgency"""
    
    deadline_dir = Path(deadline_files_dir)
    if not deadline_dir.exists():
        print(f"❌ Deadline directory not found: {deadline_files_dir}")
        return
    
    # Date patterns to look for
    date_patterns = [
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{4}-\d{2}-\d{2}\b',
        r'\b\d{1,2}/\d{1,2}/\d{4}\b',
        r'\b(today|tomorrow|next week|next month)\b',
        r'\b(urgent|asap|immediate)\b'
    ]
    
    # Urgency keywords
    urgency_keywords = {
        'high': ['urgent', 'asap', 'immediate', 'critical', 'today', 'tomorrow'],
        'medium': ['soon', 'next week', 'this month', 'deadline'],
        'low': ['eventually', 'when possible', 'future', 'later']
    }
    
    tasks = []
    
    for md_file in deadline_dir.glob('*.md'):
        if md_file.name in ['DEADLINE_OVERVIEW.md', 'README_DEADLINE_INDEX.md']:
            continue
            
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find deadline contexts
            lines = content.split('\n')
            for line_num, line in enumerate(lines):
                if re.search(r'#deadline\b', line, re.IGNORECASE):
                    
                    # Determine urgency
                    urgency = 'medium'  # default
                    line_lower = line.lower()
                    
                    for level, keywords in urgency_keywords.items():
                        if any(keyword in line_lower for keyword in keywords):
                            urgency = level
                            break
                    
                    # Look for dates
                    found_dates = []
                    for pattern in date_patterns:
                        dates = re.findall(pattern, line, re.IGNORECASE)
                        found_dates.extend(dates)
                    
                    tasks.append({
                        'file': md_file.name,
                        'line_num': line_num + 1,
                        'content': line.strip(),
                        'urgency': urgency,
                        'dates_found': found_dates,
                        'full_context': content
                    })
                    
        except Exception as e:
            print(f"❌ Error reading {md_file.name}: {e}")
    
    return tasks

def create_task_dashboard(tasks, deadline_files_dir):
    """Create a task management dashboard"""
    
    high_priority = [t for t in tasks if t['urgency'] == 'high']
    medium_priority = [t for t in tasks if t['urgency'] == 'medium']
    low_priority = [t for t in tasks if t['urgency'] == 'low']
    
    dashboard_content = [
        f"# 🚨 Deadline Task Dashboard",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"",
        f"## 📊 Task Overview",
        f"- **🔴 High Priority:** {len(high_priority)} tasks",
        f"- **🟡 Medium Priority:** {len(medium_priority)} tasks", 
        f"- **🟢 Low Priority:** {len(low_priority)} tasks",
        f"- **📝 Total Tasks:** {len(tasks)} across {len(set(t['file'] for t in tasks))} files",
        f"",
        f"---",
        f""
    ]
    
    # High priority tasks
    if high_priority:
        dashboard_content.extend([
            f"## 🔴 HIGH PRIORITY TASKS (Act Today!)",
            f""
        ])
        
        for i, task in enumerate(high_priority, 1):
            dashboard_content.extend([
                f"### {i}. [{task['file']}](./{task['file']}#L{task['line_num']})",
                f"**Line {task['line_num']}:** `{task['content']}`",
                f"",
                f"**Dates found:** {', '.join(task['dates_found']) if task['dates_found'] else 'None'}",
                f"",
                f"**Action Items:**",
                f"- [ ] Review this task immediately",
                f"- [ ] Set specific deadline date",
                f"- [ ] Add to calendar/reminders",
                f"- [ ] Break down into smaller steps",
                f"",
                f"---",
                f""
            ])
    
    # Medium priority tasks  
    if medium_priority:
        dashboard_content.extend([
            f"## 🟡 MEDIUM PRIORITY TASKS (This Week)",
            f""
        ])
        
        for i, task in enumerate(medium_priority, 1):
            dashboard_content.extend([
                f"### {i}. [{task['file']}](./{task['file']}#L{task['line_num']})",
                f"**Line {task['line_num']}:** `{task['content']}`",
                f"",
                f"- [ ] Schedule time to work on this",
                f"",
            ])
    
    # Low priority tasks
    if low_priority:
        dashboard_content.extend([
            f"## 🟢 LOW PRIORITY TASKS (When Time Permits)",
            f"",
            f"<details>",
            f"<summary>Click to expand low priority tasks ({len(low_priority)} items)</summary>",
            f""
        ])
        
        for i, task in enumerate(low_priority, 1):
            dashboard_content.extend([
                f"{i}. **[{task['file']}](./{task['file']})** - {task['content'][:50]}{'...' if len(task['content']) > 50 else ''}",
                f""
            ])
        
        dashboard_content.extend([
            f"</details>",
            f""
        ])
    
    # File-based summary
    file_summary = {}
    for task in tasks:
        if task['file'] not in file_summary:
            file_summary[task['file']] = []
        file_summary[task['file']].append(task)
    
    dashboard_content.extend([
        f"---",
        f"",
        f"## 📁 Summary by File",
        f""
    ])
    
    for filename, file_tasks in sorted(file_summary.items()):
        high_count = len([t for t in file_tasks if t['urgency'] == 'high'])
        med_count = len([t for t in file_tasks if t['urgency'] == 'medium'])
        low_count = len([t for t in file_tasks if t['urgency'] == 'low'])
        
        priority_str = []
        if high_count: priority_str.append(f"🔴{high_count}")
        if med_count: priority_str.append(f"🟡{med_count}")
        if low_count: priority_str.append(f"🟢{low_count}")
        
        dashboard_content.extend([
            f"- **[{filename}](./{filename})** - {len(file_tasks)} task{'s' if len(file_tasks) > 1 else ''} ({' '.join(priority_str)})",
            f""
        ])
    
    # Write dashboard
    dashboard_path = Path(deadline_files_dir) / "TASK_DASHBOARD.md"
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(dashboard_content))
    
    return dashboard_path

def main():
    deadline_files_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/deadline_files"
    
    print("🔍 Analyzing deadline tasks...")
    tasks = analyze_deadline_urgency(deadline_files_dir)
    
    if not tasks:
        print("❌ No deadline tasks found!")
        return
    
    print(f"✅ Found {len(tasks)} deadline tasks")
    
    dashboard_path = create_task_dashboard(tasks, deadline_files_dir)
    print(f"📊 Created task dashboard: {dashboard_path}")
    
    # Quick summary
    high_priority = len([t for t in tasks if t['urgency'] == 'high'])
    medium_priority = len([t for t in tasks if t['urgency'] == 'medium'])
    low_priority = len([t for t in tasks if t['urgency'] == 'low'])
    
    print(f"\n🎯 **Priority Summary:**")
    print(f"   🔴 High Priority: {high_priority} tasks (needs immediate attention!)")
    print(f"   🟡 Medium Priority: {medium_priority} tasks")
    print(f"   🟢 Low Priority: {low_priority} tasks")

if __name__ == "__main__":
    main()

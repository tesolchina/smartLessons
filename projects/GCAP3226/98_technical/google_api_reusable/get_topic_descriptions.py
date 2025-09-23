#!/usr/bin/env python3
"""
Update team assignments with specific topic descriptions from Moodle posts
"""

def get_topic_descriptions():
    """Get the specific topic descriptions from the Moodle posts"""
    return {
        "2": "Bus Stop Merger Optimization Project",
        "3": "Inter-Company Bus Route Coordination Project", 
        "4": "Municipal Solid Waste Charging Scheme",
        "5": "Green@Community Recycling Network Analysis",
        "6": "Flu Shot Participation Analysis",
        "7": "Typhoon Signal Data Analysis"
    }

def update_team_assignments():
    """Update the team assignments with specific topic descriptions"""
    print("🔄 Updating team assignments with specific topic descriptions")
    print("=" * 80)
    
    topic_descriptions = get_topic_descriptions()
    
    # Team assignments with topics
    teams = {
        "Team 1": "6",
        "Team 2": "3", 
        "Team 3": "7",
        "Team 4": "4",
        "Team 5": "5",
        "Team 6": "2"
    }
    
    print("📋 UPDATED TEAM ASSIGNMENTS:")
    print("-" * 80)
    
    for team, topic_num in teams.items():
        topic_title = topic_descriptions.get(topic_num, f"Topic {topic_num}")
        print(f"✅ {team}: Topic {topic_num} - {topic_title}")
    
    print(f"\n📊 TOPICS ASSIGNED:")
    print("-" * 80)
    
    assigned_topics = sorted([int(topic) for topic in teams.values()])
    available_topics = [2, 3, 4, 5, 6, 7]
    
    for topic_num in available_topics:
        status = "✅ ASSIGNED" if topic_num in assigned_topics else "❌ AVAILABLE"
        topic_title = topic_descriptions.get(str(topic_num), f"Topic {topic_num}")
        assigned_team = None
        
        for team, assigned_topic in teams.items():
            if assigned_topic == str(topic_num):
                assigned_team = team
                break
        
        if assigned_team:
            print(f"Topic {topic_num}: {topic_title} → {assigned_team}")
        else:
            print(f"Topic {topic_num}: {topic_title} → NOT ASSIGNED")
    
    # Generate the updated topic mappings for documents
    print(f"\n📄 FOR DOCUMENT UPDATES:")
    print("-" * 80)
    
    return {
        "Team_1": {
            "topic_num": "6",
            "topic_title": "Flu Shot Participation Analysis",
            "full_description": "Topic 6 - Flu Shot Participation Analysis"
        },
        "Team_2": {
            "topic_num": "3", 
            "topic_title": "Inter-Company Bus Route Coordination Project",
            "full_description": "Topic 3 - Inter-Company Bus Route Coordination Project"
        },
        "Team_3": {
            "topic_num": "7",
            "topic_title": "Typhoon Signal Data Analysis", 
            "full_description": "Topic 7 - Typhoon Signal Data Analysis"
        },
        "Team_4": {
            "topic_num": "4",
            "topic_title": "Municipal Solid Waste Charging Scheme",
            "full_description": "Topic 4 - Municipal Solid Waste Charging Scheme"
        },
        "Team_5": {
            "topic_num": "5",
            "topic_title": "Green@Community Recycling Network Analysis",
            "full_description": "Topic 5 - Green@Community Recycling Network Analysis"
        },
        "Team_6": {
            "topic_num": "2",
            "topic_title": "Bus Stop Merger Optimization Project",
            "full_description": "Topic 2 - Bus Stop Merger Optimization Project"
        }
    }

if __name__ == "__main__":
    team_topics = update_team_assignments()
    
    print("\n📝 READY TO UPDATE DOCUMENTS:")
    for team, info in team_topics.items():
        print(f"{team}: {info['full_description']}")
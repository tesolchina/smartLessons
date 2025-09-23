#!/usr/bin/env python3
"""
Analyze which students are not assigned to any group
using the data from studentGroupsTopics.md
"""

def find_unassigned_students():
    """Find students who are not assigned to any group"""
    print("🔍 Analyzing student group assignments")
    print("=" * 60)
    
    # Complete enrolled students list from the markdown file
    enrolled_students = [
        ("23233885", "CHAN Chi Ki", "陳沚其"),
        ("22224009", "CHAN Ching Yin", "陳政然"),
        ("23230851", "CHAN Dik On", "陳荻安"),
        ("23232099", "CHAN Hei Tung", "陳晞同"),
        ("25200135", "CHAN Tsz Ying", "陳芷瑩"),
        ("23232781", "CHEN Man Ching", "陳文靜"),
        ("24219169", "CHEUNG Kwun Ho", "張冠豪"),
        ("24202495", "HO Chun Chit", "何俊捷"),
        ("25227394", "HONG Kam Yin", "洪錦妍"),
        ("25223305", "HUI Man Hei", "許文曦"),
        ("25221035", "HUNG Chin Ting", "洪千婷"),
        ("23234997", "KO Man Wai", "高敏蕙"),
        ("25206354", "KUNG Tsz Lok", "龔芷樂"),
        ("25215833", "KWOK Lai Ki", "郭麗棋"),
        ("22234020", "KWOK Tsz Yau", "郭祉佑"),
        ("24222577", "LEUNG Hoi Ying", "梁愷礽"),
        ("24221872", "LIU Wai Man", "廖慧雯"),
        ("23213078", "LYU Junhan", "吕君涵"),
        ("23200278", "MA Zi Xing", ""),
        ("24202509", "MAN Wai Yin", "文慧研"),
        ("22256946", "SU Jialu", "蘇嘉鷺"),
        ("23236353", "TAM Tin Chun", "譚天竣"),
        ("23230371", "TANG Tsz Tung", "鄧芷彤"),  # Note: Listed as "Tag Tsz Tung" in groups
        ("23229101", "TSOI Tsz Yan", "蔡子欣"),
        ("22232192", "TSOI Yik Hon", "蔡奕翰"),
        ("23213116", "WONG Chun Hang", "王俊恆"),
        ("23233168", "WONG Ling Yan Cassy", "王翎欣"),
        ("25221310", "WONG Wai Lun", "黃偉倫"),
        ("24205397", "XU Jingyi", "徐婧儀"),
        ("23238283", "YEUNG Wing Yu", "楊詠諭"),
        ("23229543", "YIP Tsz Ying", "葉芷縈"),
        ("22231153", "ZHENG Zian", "鄭子安")
    ]
    
    # Students assigned to groups (from the tables)
    assigned_students = [
        # Team 1
        ("23238283", "Yeung Wing Yu"),
        ("22234020", "Kwok Tsz Yau"),
        ("22232192", "Tsoi Yik Hon"),
        ("22256946", "SuJiaLu"),
        
        # Team 2
        ("23232099", "Chan Hei Tung"),
        ("23229543", "Yip Tsz Ying"),
        ("23234997", "Ko Man Wai"),
        ("23233168", "Wong Ling Yan Cassy"),
        ("23229101", "Tsoi Tsz Yan"),
        ("23200278", "Zi Xing Saul Ma"),  # Listed as "MA Zi Xing" in enrollment
        
        # Team 3
        ("23232781", "Chen Man Ching"),
        ("25223305", "Hui Man Hei"),
        ("25227394", "HONG KAM YIN"),
        ("25206354", "Kung Tsz Lok"),
        ("", "ZHENG ZIAN"),  # Missing student ID
        ("22224009", "Chan Ching Yin"),
        
        # Team 4
        ("24221872", "Liu Wai Man"),
        ("25215833", "Kwok Lai Ki"),
        ("25200135", "Chan Tsz Ying"),
        ("25221310", "Wong Wai Lun"),
        
        # Team 5
        ("24202509", "MAN Wai Yin"),
        ("23233885", "Chan Chi Ki"),
        ("23230371", "Tag Tsz Tung"),  # Listed as "TANG Tsz Tung" in enrollment
        ("24202495", "HO Chun Chit"),
        ("24205397", "Xu Jingyi"),
        ("24219169", "Cheung Kwun Ho"),
        
        # Team 6
        ("23236353", "Tam Tin Chun"),
        ("23230851", "Chan Dik On"),
        ("23213116", "Wong Chun Hang"),
    ]
    
    # Get assigned student IDs (excluding the one with missing ID)
    assigned_ids = set([student_id for student_id, name in assigned_students if student_id.strip()])
    
    print(f"📊 Total enrolled students: {len(enrolled_students)}")
    print(f"👥 Students assigned to teams: {len(assigned_ids)}")
    print(f"❓ Students with missing/unclear assignment: {len(enrolled_students) - len(assigned_ids)}")
    
    # Find unassigned students
    unassigned_students = []
    
    for student_id, name, chinese_name in enrolled_students:
        if student_id not in assigned_ids:
            unassigned_students.append((student_id, name, chinese_name))
    
    print(f"\n🚨 STUDENTS NOT ASSIGNED TO ANY TEAM ({len(unassigned_students)}):")
    print("-" * 60)
    
    if unassigned_students:
        for student_id, name, chinese_name in unassigned_students:
            print(f"📝 {name} (ID: {student_id})")
            if chinese_name:
                print(f"   Chinese Name: {chinese_name}")
            print()
    else:
        print("✅ All enrolled students are assigned to teams!")
    
    # Check for potential name mismatches or issues
    print("\n🔍 POTENTIAL ISSUES DETECTED:")
    print("-" * 60)
    
    issues = []
    
    # Check for ZHENG ZIAN issue
    zheng_in_enrollment = any(name == "ZHENG Zian" for _, name, _ in enrolled_students)
    zheng_in_team = any(name == "ZHENG ZIAN" for _, name in assigned_students)
    
    if zheng_in_enrollment and zheng_in_team:
        issues.append("⚠️  ZHENG ZIAN in Team 3 is missing student ID (should be 22231153)")
    
    # Check for name variations
    name_variations = [
        ("TANG Tsz Tung", "Tag Tsz Tung", "Same person, name variation in team list")
    ]
    
    for enrollment_name, team_name, note in name_variations:
        issues.append(f"ℹ️  {note}: '{enrollment_name}' vs '{team_name}'")
    
    if issues:
        for issue in issues:
            print(issue)
    else:
        print("✅ No issues detected")
    
    # Summary
    print(f"\n📋 SUMMARY:")
    print(f"• Total enrolled: {len(enrolled_students)} students")
    print(f"• Assigned to teams: {len(assigned_ids)} students")
    print(f"• Unassigned: {len(unassigned_students)} students")
    print(f"• Teams formed: 6 teams")
    print(f"• Average team size: {len(assigned_ids) / 6:.1f} students per team")
    
    return unassigned_students

if __name__ == "__main__":
    unassigned = find_unassigned_students()
    
    if unassigned:
        print(f"\n🎯 ACTION REQUIRED:")
        print("These students need to be assigned to teams:")
        for student_id, name, chinese_name in unassigned:
            print(f"  - {name} (ID: {student_id})")
#!/usr/bin/env python3
"""
Create comprehensive GCAP 3056 semester structure with weekly folders and planning documents
"""

import os
from pathlib import Path
from datetime import datetime

def create_week_folder(week_num: int, week_title: str, week_description: str, learning_objectives: list, activities: list, readings: list = None):
    """Create individual week folder with planning document"""
    
    folder_name = f"week{week_num:02d}_{week_title.lower().replace(' ', '_').replace('/', '_')}"
    week_folder = Path(f"./weekly_plan/{folder_name}")
    week_folder.mkdir(parents=True, exist_ok=True)
    
    # Create week planning document
    planning_doc = week_folder / f"week{week_num:02d}_planning.md"
    
    content = f"""# Week {week_num}: {week_title}

**Date Range:** Week {week_num} of Semester
**Duration:** 3 hours
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

## 📋 Week Overview

{week_description}

## 🎯 Learning Objectives

"""
    
    for obj in learning_objectives:
        content += f"- {obj}\n"
    
    content += f"""

## 📚 Planned Activities

"""
    
    for activity in activities:
        content += f"- {activity}\n"
    
    if readings:
        content += f"""

## 📖 Required Readings

"""
        for reading in readings:
            content += f"- {reading}\n"
    
    content += f"""

## 🛠️ Materials Needed

- [ ] Presentation slides
- [ ] Handouts/worksheets  
- [ ] Guest speaker coordination (if applicable)
- [ ] Technology setup
- [ ] Assessment materials

## 📝 Preparation Checklist

### Before Class:
- [ ] Review previous week's outcomes
- [ ] Prepare discussion questions
- [ ] Set up digital tools/platforms
- [ ] Coordinate with guest speakers
- [ ] Prepare assessment rubrics

### During Class:
- [ ] Take attendance
- [ ] Review previous week briefly
- [ ] Conduct main activities
- [ ] Monitor group work progress
- [ ] Address questions and concerns

### After Class:
- [ ] Update student progress records
- [ ] Prepare feedback for assignments
- [ ] Plan follow-up activities
- [ ] Coordinate with next week's requirements

## 🎯 Assessment Integration

### Related to Major Assessments:
- **Research Paper:** {week_title} contributes to research foundation
- **Portfolio:** Document week's activities and insights  
- **Learning Journal:** Reflect on key concepts and applications

## 📊 Success Metrics

- Student engagement level during activities
- Quality of discussion and questions
- Progress toward project milestones
- Understanding demonstrated through activities

## 🔗 Connections

### Previous Weeks:
- Builds on concepts from previous weeks

### Future Weeks:  
- Prepares foundation for upcoming topics
- Supports ongoing project development

## 📌 Notes & Reflections

*[Space for instructor notes, modifications, and reflections after each class]*

---

**Instructor:** Simon Wang  
**Course:** GCAP 3056 - Taking a Stand  
**Academic Year:** 2025-2026
"""
    
    with open(planning_doc, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {planning_doc}")
    return week_folder

def create_assessment_folder(assessment_name: str, weighting: str, description: str, requirements: list, cilo_alignment: list):
    """Create assessment folder with detailed instructions"""
    
    folder_name = f"assessment_{assessment_name.lower().replace(' ', '_')}"
    assessment_folder = Path(f"./assessments/{folder_name}")
    assessment_folder.mkdir(parents=True, exist_ok=True)
    
    # Create instructions document
    instructions_doc = assessment_folder / f"{assessment_name.lower().replace(' ', '_')}_instructions.md"
    
    content = f"""# {assessment_name} - Instructions & Guidelines

**Weighting:** {weighting}
**Type:** {"Group" if "group" in description.lower() else "Individual"} Assessment
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

## 📋 Assessment Overview

{description}

## 🎯 Course Learning Outcomes (CILOs) Addressed

"""
    
    for cilo in cilo_alignment:
        content += f"- **CILO {cilo}:** {get_cilo_description(cilo)}\n"
    
    content += f"""

## 📝 Requirements

"""
    
    for requirement in requirements:
        content += f"- {requirement}\n"
    
    content += f"""

## 📅 Timeline & Deadlines

### Key Milestones:
- [ ] **Week 3-4:** Topic selection and initial planning
- [ ] **Week 5:** Data collection begins
- [ ] **Week 8:** Mid-semester progress check
- [ ] **Week 11-12:** Community engagement activities
- [ ] **Week 13:** Final submission and reflection

### Submission Details:
- **Due Date:** [To be announced based on semester schedule]
- **Submission Format:** Digital submission via Moodle
- **Late Penalty:** [Standard university policy applies]

## 🏆 Assessment Criteria

### Excellent (A-A+):
- Demonstrates exceptional understanding of course concepts
- Shows sophisticated analysis and critical thinking
- Excellent communication and presentation skills
- Goes beyond minimum requirements

### Good (B-B+):
- Shows good understanding of course concepts  
- Adequate analysis with some critical insights
- Clear communication and organization
- Meets all requirements competently

### Satisfactory (C-C+):
- Basic understanding of course concepts
- Limited analysis or critical thinking
- Communication needs improvement
- Meets minimum requirements

### Needs Improvement (D or below):
- Insufficient understanding of course concepts
- Lacks analysis or critical thinking
- Poor communication and organization
- Fails to meet minimum requirements

## 📊 Detailed Rubric

*[Specific rubric to be developed based on assessment type]*

## 💡 Tips for Success

1. **Start Early:** Begin planning and research immediately
2. **Use Course Resources:** Leverage guest speakers, readings, and workshops
3. **Engage with Community:** Make use of government information requests
4. **Document Everything:** Keep detailed records for portfolio development
5. **Seek Feedback:** Use consultation sessions with instructor
6. **Collaborate Effectively:** If group work, establish clear roles and communication

## 🆘 Support Resources

### Academic Support:
- Instructor consultation hours
- Writing center support
- Library research assistance
- Peer collaboration groups

### Technical Support:
- Moodle platform guidance
- Digital tool tutorials
- Media production resources

## 📚 Relevant Course Materials

- Week-specific readings and resources
- Guest speaker presentations
- Government information request templates
- Previous student examples (with permission)

## ❓ Frequently Asked Questions

**Q: Can I change my topic after initial submission?**
A: Topic changes should be discussed with instructor and approved in writing.

**Q: How do I request information from the government?**
A: Use the Code on Access to Information templates and guidelines provided in class.

**Q: What if my group member is not contributing?**
A: Contact instructor immediately to discuss group dynamics and potential solutions.

**Q: Can I use AI tools for this assessment?**
A: [Policy to be clarified based on university guidelines and course requirements]

---

**For questions or clarification, please contact:**  
**Instructor:** Simon Wang  
**Email:** [Contact information]  
**Office Hours:** [Schedule to be announced]
"""
    
    with open(instructions_doc, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Create rubric document
    rubric_doc = assessment_folder / f"{assessment_name.lower().replace(' ', '_')}_rubric.md"
    
    rubric_content = create_assessment_rubric(assessment_name, cilo_alignment)
    
    with open(rubric_doc, 'w', encoding='utf-8') as f:
        f.write(rubric_content)
    
    print(f"✅ Created: {instructions_doc}")
    print(f"✅ Created: {rubric_doc}")
    return assessment_folder

def get_cilo_description(cilo_num: int) -> str:
    """Return CILO descriptions"""
    cilo_descriptions = {
        1: "Synthesise and critically analyse data/information/viewpoints from various stakeholders to develop actionable policy recommendations",
        2: "Collaborate with peers from multiple backgrounds and draw on multidisciplinary research to develop insights into social problems",
        3: "Recognise and evaluate value principles in public discourse to develop rhetorical strategies for arguments on social issues",
        4: "Apply knowledge from research activities by writing for the public as informed citizen-scholars"
    }
    return cilo_descriptions.get(cilo_num, f"CILO {cilo_num}")

def create_assessment_rubric(assessment_name: str, cilo_alignment: list) -> str:
    """Create detailed rubric for assessment"""
    
    rubric = f"""# {assessment_name} - Detailed Rubric

**Assessment Type:** {assessment_name}
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}

## 📊 Assessment Rubric

### Overall Grade Distribution:
- **Excellent (85-100%):** A- to A+
- **Good (70-84%):** B- to B+  
- **Satisfactory (55-69%):** C- to C+
- **Needs Improvement (0-54%):** D+ and below

---

"""
    
    if "research paper" in assessment_name.lower():
        rubric += create_research_paper_rubric()
    elif "portfolio" in assessment_name.lower():
        rubric += create_portfolio_rubric()
    elif "journal" in assessment_name.lower():
        rubric += create_journal_rubric()
    else:
        rubric += create_generic_rubric()
    
    rubric += f"""

## 🎯 CILO Alignment Assessment

"""
    
    for cilo in cilo_alignment:
        rubric += f"""
### CILO {cilo} Evaluation:
- **Excellent (A):** Demonstrates sophisticated understanding and application
- **Good (B):** Shows competent understanding with good application  
- **Satisfactory (C):** Basic understanding with adequate application
- **Needs Improvement (D/F):** Insufficient understanding or poor application
"""
    
    rubric += f"""

## 📝 Feedback Guidelines

### Strengths to Highlight:
- Critical thinking and analysis quality
- Research depth and breadth
- Communication effectiveness
- Innovation and creativity
- Collaboration skills (if applicable)

### Areas for Improvement:
- Analytical depth
- Research methodology
- Writing clarity and organization
- Evidence integration
- Public engagement effectiveness

### Constructive Feedback Structure:
1. **What worked well:** Specific positive observations
2. **Areas for development:** Specific improvement suggestions
3. **Next steps:** Actionable recommendations for future work

---

**Grading Completed By:** [Instructor Name]  
**Date:** [Grading Date]  
**Student Feedback Session:** [If applicable]
"""
    
    return rubric

def create_research_paper_rubric() -> str:
    """Create specific rubric for research paper"""
    return """
## Research Paper Specific Criteria

| Criteria | Excellent (A) | Good (B) | Satisfactory (C) | Needs Improvement (D/F) |
|----------|---------------|----------|------------------|-------------------------|
| **Research Quality (25%)** | Comprehensive, credible sources; innovative data collection | Good sources with adequate depth | Basic sources meeting requirements | Insufficient or unreliable sources |
| **Critical Analysis (25%)** | Sophisticated analysis with nuanced insights | Good analysis with clear reasoning | Basic analysis meeting requirements | Weak analysis lacking depth |
| **Policy Recommendations (25%)** | Innovative, feasible, well-supported recommendations | Clear recommendations with good justification | Basic recommendations adequately supported | Weak or impractical recommendations |
| **Writing & Organization (25%)** | Exceptional clarity, organization, and style | Clear writing with good organization | Adequate writing meeting standards | Poor writing affecting comprehension |

### Additional Considerations:
- Use of government information requests (CAIP)
- Integration of course concepts and guest speaker insights
- Evidence of community engagement in research process
- Adaptability to different formats (reports, letters, social media)
"""

def create_portfolio_rubric() -> str:
    """Create specific rubric for community engagement portfolio"""
    return """
## Community Engagement Portfolio Specific Criteria

| Criteria | Excellent (A) | Good (B) | Satisfactory (C) | Needs Improvement (D/F) |
|----------|---------------|----------|------------------|-------------------------|
| **Information Requests (20%)** | Multiple, strategic requests with excellent responses | Good requests with adequate responses | Basic requests meeting requirements | Insufficient or poorly executed requests |
| **Public Writing (30%)** | Published/high-quality writing for multiple audiences | Clear writing for public consumption | Adequate public writing meeting standards | Poor quality or inappropriate for audience |
| **Media Creation (25%)** | Professional, compelling infographic/video | Good quality media with clear message | Adequate media meeting requirements | Poor quality or unclear media |
| **Documentation (15%)** | Comprehensive, reflective documentation | Good documentation with clear organization | Basic documentation meeting standards | Incomplete or poorly organized |
| **Community Impact (10%)** | Measurable engagement and feedback | Evidence of community interaction | Some community engagement shown | Little to no community engagement |

### Compulsory Components Checklist:
- [ ] Evidence of government/community information requests
- [ ] Evidence of public writing (newspaper, reports, social media)
- [ ] Infographic OR video clip making the argument
- [ ] Reflection on community engagement process
- [ ] Documentation of team collaboration
"""

def create_journal_rubric() -> str:
    """Create specific rubric for reflective learning journal"""
    return """
## Reflective Learning Journal Specific Criteria

| Criteria | Excellent (A) | Good (B) | Satisfactory (C) | Needs Improvement (D/F) |
|----------|---------------|----------|------------------|-------------------------|
| **Reflection Depth (40%)** | Sophisticated, insightful reflection on learning | Good reflection with clear insights | Basic reflection meeting requirements | Superficial reflection lacking depth |
| **Multimodal Integration (25%)** | Creative use of writing, audio, video elements | Good integration of different modes | Basic multimodal approach | Poor use of different modes |
| **Moodle Participation (20%)** | Exceptional contribution to discussion board | Good participation with helpful comments | Adequate participation meeting requirements | Minimal or poor participation |
| **Learning Connection (15%)** | Clear connections between theory and practice | Good integration of course concepts | Basic connection to course material | Weak connection to course learning |

### Journal Components:
- **Written Reflection:** Regular entries documenting learning journey
- **Audio/Video Elements:** Voice recordings or video reflections
- **Discussion Board Participation:** Meaningful engagement with peers
- **Learning Synthesis:** Integration of course concepts with personal insights
- **Growth Documentation:** Evidence of learning progression over semester
"""

def create_generic_rubric() -> str:
    """Create generic rubric template"""
    return """
## Assessment Criteria

| Criteria | Excellent (A) | Good (B) | Satisfactory (C) | Needs Improvement (D/F) |
|----------|---------------|----------|------------------|-------------------------|
| **Understanding (25%)** | Demonstrates exceptional understanding | Shows good understanding | Basic understanding evident | Insufficient understanding |
| **Application (25%)** | Sophisticated application of concepts | Good application with some insight | Basic application meeting requirements | Poor application of concepts |
| **Communication (25%)** | Exceptional clarity and effectiveness | Clear and well-organized | Adequate communication | Poor communication skills |
| **Critical Thinking (25%)** | Sophisticated analysis and evaluation | Good analytical skills | Basic critical thinking | Weak analytical skills |
"""

def main():
    """Create complete semester structure"""
    
    print("=== Creating GCAP 3056 Semester Structure ===")
    print()
    
    # Week definitions based on syllabus
    weeks_data = [
        (1, "Hong Kong SAR Government", "Introduction to HK government structure, transparency, accountability, Code on Access to Information, and complaint channels. Students begin identifying social issues for projects.", 
         ["Understand HK government structure and accountability principles", "Learn to use Code on Access to Information", "Begin social issue identification and project planning"],
         ["Introduce government structure and organization", "Demonstrate CAIP request process", "Group formation and topic brainstorming", "Plan semester timeline"],
         ["Reif, L. (2014). The Ombudsman, Good Governance, and the International Human Rights System", "Head, B. W. (2007). Community Engagement: Participation on Whose Terms?", "Wadham, J., Harris, K., & Peretz, G. (2011). Blackstone's Guide to the Freedom of Information Act 2000"]),
        
        (2, "Media and Research Literature", "Explore relationships between public and academic communities, media representation of social issues, and strategies for communicating research to public audiences.",
         ["Understand media-research-public relationships", "Develop strategies for public communication", "Explore challenges of research communication"],
         ["Analyze media coverage of social issues", "Workshop on public communication strategies", "Review academic vs. popular writing styles"],
         ["Irwin, A., & Wynne, B. (2003). Misunderstanding Science?", "Simon, D., et al. (2019). Handbook on Science and Public Policy", "Hillier, D. (2016). Communicating Health Risks to the Public"]),
        
        (3, "Education and Cultural Affairs", "Focus on HK government's education reform, public library services enhancement, and museum renovation in the digital age.",
         ["Analyze education policy reforms", "Evaluate cultural institution digitization", "Connect policy to public service delivery"],
         ["Seminar on education policy changes", "Case study analysis of library/museum reforms", "Group work on education-related projects"],
         ["Hille, R. T. (2018). The New Public Library: Design Innovation", "Tse, T. K.-C., & Lee, M. H. (2016). Making Sense of Education in Post-Handover Hong Kong", "Hossaini, A., & Blankenberg, N. (2017). Manual of Digital Museum Planning"]),
        
        (4, "Public Health and Environment", "Examine HK's public healthcare policies for aging population and long-term decarbonization strategies under Paris Climate Agreement.",
         ["Analyze healthcare policy for aging population", "Evaluate environmental and climate policies", "Understand resource allocation challenges"],
         ["Seminar on healthcare policy", "Workshop on environmental policy analysis", "Guest speaker from health/environment sector"],
         ["Heston, T. F. (Ed.). (2018). eHealth: Making Health Care Smarter", "Harvey, H., Orvis, R., & Rissman, J. (2018). Designing Climate Solutions"]),
        
        (5, "Data Analysis Workshop 1", "Apply skills for analyzing and interpreting quantitative and qualitative data from government and other sources for projects. Include Forum One with guest speakers.",
         ["Master data analysis techniques", "Apply analysis to project data", "Engage with community stakeholders"],
         ["Data analysis workshop session", "Forum One with guest speakers (NGOs, political groups, government)", "Project data analysis application"],
         []),
        
        (6, "Housing and Transportation", "Explore HK's housing and transportation policies, critically reviewing buses, MTR, taxis, transitional housing, and land supply issues.",
         ["Analyze housing policy challenges", "Evaluate transportation system policies", "Understand urban planning connections"],
         ["Housing policy seminar", "Transportation policy analysis", "Case study on land supply issues"],
         ["Wong, Y. C. R. (2015). Hong Kong Land for Hong Kong People", "Finger, M., & Audouin, M. (Eds.). (2018). The Governance of Smart Transportation Systems"]),
        
        (7, "Smart Cities and Constitutional Affairs", "Explore HK's smart city evolution amid political movements, focusing on law enforcement technology, protest organization, and privacy concerns.",
         ["Understand smart city development", "Analyze technology in governance", "Evaluate privacy and rights implications"],
         ["Smart cities seminar", "Constitutional affairs discussion", "Technology and rights workshop"],
         ["Forrest, G. C. (2016). Police Technology: 21st-Century Crime-Fighting Tools", "Cropf, R. A. (2016). Ethical Issues and Citizen Rights in Digital Government"]),
        
        (8, "Writing Workshop", "Introduction to rhetorical strategies in media discourse, persuasive communication in social media, and value principles in argumentation. Include Forum Two.",
         ["Master rhetorical strategies for public writing", "Develop persuasive communication skills", "Apply argumentation principles"],
         ["Writing workshop on rhetorical strategies", "Social media communication training", "Forum Two with guest speakers"],
         []),
        
        (9, "Consultations", "Groups meet with instructor to bring final projects into presentable state through individual consultations.",
         ["Refine project presentations", "Address project challenges", "Prepare for community outreach"],
         ["Individual group consultations", "Project refinement sessions", "Presentation preparation"],
         []),
        
        (10, "Consultations", "Continued individual group consultations to finalize projects and prepare for community engagement.",
         ["Finalize project deliverables", "Prepare outreach materials", "Practice presentations"],
         ["Continued group consultations", "Final project preparation", "Outreach planning"],
         []),
        
        (11, "Community Outreach", "Students set up and manage on-campus outreach booths about their projects to engage with peers and the public.",
         ["Implement community engagement", "Present projects to public", "Gather feedback and responses"],
         ["Set up on-campus outreach booths", "Public engagement activities", "Document community responses"],
         []),
        
        (12, "Community Outreach", "Continued on-campus outreach activities, expanding public engagement with project outcomes.",
         ["Continue public engagement", "Refine presentations based on feedback", "Document outreach impact"],
         ["Continue outreach booth activities", "Expand community engagement", "Collect feedback and testimonials"],
         []),
        
        (13, "Course Reflection", "Final seminar to reflect on course experiences and outcomes, synthesizing learning and project results.",
         ["Synthesize course learning", "Reflect on project outcomes", "Evaluate community impact"],
         ["Reflection seminar", "Project outcome presentations", "Course evaluation and feedback"],
         [])
    ]
    
    # Create weekly folders
    for week_data in weeks_data:
        create_week_folder(*week_data)
    
    print()
    print("=== Creating Assessment Folders ===")
    print()
    
    # Assessment definitions
    assessments = [
        ("Argumentative Research Paper", "25%", 
         "Small groups work together to write a short argumentative research paper that critically reviews government policies and offers policy recommendations. The paper can be adapted into different forms as reports to the government, letters to the editor, social media posts and oral presentations.",
         ["Critically review specific government policies", "Offer evidence-based policy recommendations", "Adapt content for multiple formats (reports, letters, social media)", "Collaborate effectively in small groups", "Integrate research from multiple sources"],
         [1, 2, 3]),
         
        ("Community Engagement Portfolio", "40%",
         "Students work in groups to engage the community in different ways including writing for newspapers, preparing government reports, and designing social media campaigns. Portfolio documents team efforts in community engagement.",
         ["Evidence of requesting information from government and/or community leaders/members", "Evidence of writing for the public (newspaper articles, government reports, social media posts)", "An infographic OR video clip making the argument", "Documentation of team collaboration and individual contributions", "Reflection on community engagement process and outcomes"],
         [1, 2, 4]),
         
        ("Reflective Learning Journal", "35%",
         "Students keep a multimodal learning journal through writing, voice-recording and/or filming to reflect on learning processes. Journal drafts are shared on Moodle discussion board for peer learning.",
         ["Regular written reflection entries documenting learning journey", "Integration of multimodal elements (voice recordings, video reflections)", "Active participation in Moodle discussion board with meaningful peer engagement", "Connection of course concepts to personal insights and growth", "Evidence of learning progression throughout the semester"],
         [2, 3, 4])
    ]
    
    # Create assessment folders
    for assessment_data in assessments:
        create_assessment_folder(*assessment_data)
    
    # Create main overview document
    overview_doc = Path("./GCAP3056_Semester_Overview.md")
    
    overview_content = f"""# GCAP 3056: Taking a Stand - Complete Semester Structure

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Course:** Taking a Stand: Turning Research Insights into Policy Recommendations
**Instructor:** Simon Wang

## 📁 Folder Structure Created

### Weekly Planning Folders (13 weeks):
```
weekly_plan/
├── week01_hong_kong_sar_government/
├── week02_media_and_research_literature/
├── week03_education_and_cultural_affairs/
├── week04_public_health_and_environment/
├── week05_data_analysis_workshop_1/
├── week06_housing_and_transportation/
├── week07_smart_cities_and_constitutional_affairs/
├── week08_writing_workshop/
├── week09_consultations/
├── week10_consultations/
├── week11_community_outreach/
├── week12_community_outreach/
└── week13_course_reflection/
```

### Assessment Management Folders:
```
assessments/
├── assessment_argumentative_research_paper/
│   ├── argumentative_research_paper_instructions.md
│   └── argumentative_research_paper_rubric.md
├── assessment_community_engagement_portfolio/
│   ├── community_engagement_portfolio_instructions.md
│   └── community_engagement_portfolio_rubric.md
└── assessment_reflective_learning_journal/
    ├── reflective_learning_journal_instructions.md
    └── reflective_learning_journal_rubric.md
```

## 🎯 Course Overview

### Course Learning Outcomes (CILOs):
1. **CILO 1:** Synthesise and critically analyse data from various stakeholders to develop actionable policy recommendations
2. **CILO 2:** Collaborate with peers from multiple backgrounds drawing on multidisciplinary research insights
3. **CILO 3:** Recognise and evaluate value principles in public discourse for rhetorical strategy development  
4. **CILO 4:** Apply research knowledge by writing for the public as informed citizen-scholars

### Assessment Distribution:
- **Research Paper (Group):** 25% - Focus on policy analysis and recommendations
- **Community Engagement Portfolio (Group):** 40% - Public writing and engagement documentation
- **Reflective Learning Journal (Individual):** 35% - Multimodal reflection and peer discussion

### Key Course Features:
- **Code on Access to Information (CAIP):** Core methodology for government data requests
- **Community Engagement:** Real public outreach and media engagement
- **Multidisciplinary Approach:** Integration of multiple academic disciplines
- **Experiential Learning:** Hands-on policy research and public communication
- **Guest Speaker Forums:** Direct interaction with NGOs, government, and political groups

## 📅 Semester Timeline

### Weeks 1-2: Introduction
- Government structure and CAIP training
- Media and research communication strategies

### Weeks 3-8: Core Content Seminars
- Education, health, environment, housing, transportation, smart cities
- Data analysis and writing workshops
- Two guest speaker forums

### Weeks 9-13: Project Implementation
- Individual consultations
- Community outreach activities  
- Course reflection and synthesis

## 🛠️ Implementation Notes

### Each Weekly Folder Contains:
- Detailed planning document with learning objectives
- Activity descriptions and preparation checklists
- Reading assignments and material requirements
- Assessment integration notes
- Success metrics and reflection space

### Each Assessment Folder Contains:
- Comprehensive instructions with timeline and requirements
- Detailed rubric with CILO alignment
- Support resources and FAQ sections
- Feedback guidelines for instructors

## 🚀 Ready for Semester Launch

All planning documents are created and ready for customization based on:
- Specific semester dates and deadlines
- Guest speaker availability and coordination
- Resource allocation and material preparation
- Student group compositions and project topics

---

**Next Steps:**
1. Review and customize weekly planning documents
2. Confirm guest speaker availability for forums
3. Prepare CAIP request templates and examples
4. Set up Moodle discussion boards for learning journals
5. Coordinate community outreach logistics

**Semester Success Factors:**
- Early CAIP request submission (Weeks 3-4)
- Active guest speaker engagement
- Strong group collaboration support
- Regular project milestone monitoring
- Meaningful community outreach coordination
"""
    
    with open(overview_doc, 'w', encoding='utf-8') as f:
        f.write(overview_content)
    
    print(f"✅ Created: {overview_doc}")
    print()
    print("🎉 Complete semester structure created!")
    print(f"📂 Weekly folders: 13 weeks with planning documents")
    print(f"📋 Assessment folders: 3 assessments with instructions and rubrics")
    print(f"📄 Semester overview: Complete structure documentation")
    print()
    print("🚀 Ready for GCAP 3056 semester implementation!")

if __name__ == "__main__":
    main()

# GCAP3226 Course Repository - Reorganized Structure

## 📁 **New Folder Organization for Teaching**

This repository has been reorganized to provide a clear, pedagogical structure for the GCAP3226 course. The new structure separates content delivery, student work areas, instructor tools, and resources.

---

## 🗂️ **Directory Structure**

### **📚 01_course_content/**
*Primary location for all course delivery materials*

```
01_course_content/
├── week01_introduction/
│   ├── lectures/
│   ├── assignments/
│   ├── resources/
│   └── extracted_materials/
├── week02_foundations/
├── week03_methods/
├── week04_simulation/
│   ├── lectures/
│   │   ├── GCAP3226_week4_Simulation_20250920.pptx
│   │   ├── GCAP3226_week4_Simulation_20250920.pdf
│   │   ├── GCAP3226_week4_Simulation_20250920.md
│   │   └── notesSimon.md
│   ├── assignments/
│   ├── resources/
│   └── extracted_materials/
│       └── extracted_ppt_content/
│           ├── extracted_text.txt
│           └── [12 images from PPT]
├── week05_advanced/
└── ...
```

### **👥 02_student_workspace/**
*Dedicated areas for student work and collaboration*

```
02_student_workspace/
├── individual_work/          # Individual assignments and projects
├── group_projects/           # Collaborative group work
├── submissions/              # Assignment submissions
└── practice_exercises/       # Practice problems and solutions
```

### **🎓 03_instructor_tools/**
*Administrative and teaching support tools*

```
03_instructor_tools/
├── grading_rubrics/          # Assessment criteria and rubrics
├── student_management/       # Student lists, attendance, grades
├── budget_planning/          # Course budget and expenses
└── ai_assistants/            # AI chatbots and teaching aids
    ├── course_assistant/
    ├── data_analysis_bot/
    ├── mathGuru/
    ├── policy_research_bot/
    └── image/
```

### **📊 04_data_resources/**
*Data sources and analysis materials*

```
04_data_resources/
├── open_data_inventory/      # Hong Kong open data catalog
│   ├── datasets_catalog.json
│   ├── figures/
│   └── samples/
├── datasets/                 # Course-specific datasets
└── external_apis/           # API documentation and examples
```

### **⚙️ 05_scripts_utilities/**
*Code utilities and automation scripts*

```
05_scripts_utilities/
├── data_processing/          # Data analysis and processing scripts
├── content_extraction/       # PPT/document extraction tools
│   ├── extract_ppt_content.py
│   ├── simple_ppt_extractor.py
│   └── requirements_ppt.txt
└── automation/              # Course automation tools
```

### **🗃️ 99_archive/**
*Backup and archived materials*

---

## 🚀 **Getting Started**

### **For Students:**
1. Navigate to `02_student_workspace/` for your work areas
2. Check `01_course_content/weekXX_*/` for weekly materials
3. Use `01_course_content/weekXX_*/resources/` for additional reading

### **For Instructors:**
1. Course content management: `01_course_content/`
2. Teaching tools: `03_instructor_tools/`
3. Data resources: `04_data_resources/`
4. Utility scripts: `05_scripts_utilities/`

### **For Week 4 (Current):**
- **Lecture Materials:** `01_course_content/week04_simulation/lectures/`
- **Extracted PPT Content:** `01_course_content/week04_simulation/extracted_materials/`
- **Student Notes:** `01_course_content/week04_simulation/lectures/notesSimon.md`

---

## 🛠️ **Key Tools & Scripts**

### **PowerPoint Extraction:**
- **Location:** `05_scripts_utilities/content_extraction/`
- **Usage:** Extract images and text from course presentations
- **Run:** `python simple_ppt_extractor.py`

### **Data Analysis:**
- **Location:** `04_data_resources/open_data_inventory/`
- **Content:** Hong Kong open data analysis and visualization

### **AI Teaching Assistants:**
- **Location:** `03_instructor_tools/ai_assistants/`
- **Tools:** Course assistant, math guru, policy research bot

---

## 📋 **Weekly Structure Template**

Each week follows this consistent structure:
```
weekXX_topic_name/
├── lectures/          # PowerPoint, PDF, markdown notes
├── assignments/       # Problem sets, projects
├── resources/         # Readings, references, datasets
└── extracted_materials/ # Processed content from lectures
```

---

## 🔄 **Workflow for Content Creation**

1. **Lecture Preparation:**
   - Create materials in `01_course_content/weekXX_*/lectures/`
   - Use extraction scripts to process presentations
   - Store extracted content in `extracted_materials/`

2. **Assignment Setup:**
   - Place assignments in `01_course_content/weekXX_*/assignments/`
   - Create templates in `02_student_workspace/practice_exercises/`

3. **Data Integration:**
   - Store datasets in `04_data_resources/datasets/`
   - Document APIs in `04_data_resources/external_apis/`

---

## 📈 **Course Progress Tracking**

- **Current Week:** Week 4 - Simulation Methods (Bus Route Case Study)
- **Completed Setup:** PowerPoint extraction, note organization
- **Next Steps:** Organize weeks 1-3 materials, create assignment templates

---

## 🆘 **Quick Navigation**

| Task | Location |
|------|----------|
| View lecture slides | `01_course_content/week04_simulation/lectures/` |
| Check extracted PPT content | `01_course_content/week04_simulation/extracted_materials/` |
| Student workspace | `02_student_workspace/` |
| Run PPT extraction | `05_scripts_utilities/content_extraction/` |
| Access AI tools | `03_instructor_tools/ai_assistants/` |
| View data catalog | `04_data_resources/open_data_inventory/` |

---

*Repository reorganized on September 22, 2025*
*Structure optimized for GCAP3226 course delivery and management*
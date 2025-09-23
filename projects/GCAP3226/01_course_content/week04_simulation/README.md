# Week 4: Simulation Methods - Bus Route Case Study

## 📍 **Current Location**
`01_course_content/week04_simulation/`

## 📚 **Materials in This Week**

### **📖 Lectures** (`lectures/`)
- `GCAP3226_week4_Simulation_20250920.pptx` - Main presentation
- `GCAP3226_week4_Simulation_20250920.pdf` - PDF version
- `GCAP3226_week4_Simulation_20250920.md` - Markdown notes
- `notesSimon.md` - Enhanced notes with data governance insights

### **🔍 Extracted Materials** (`extracted_materials/`)
- `extracted_ppt_content/` - Complete PPT extraction
  - `extracted_text.txt` - All slide text content
  - 12 PNG images from presentation slides

### **📝 Assignments** (`assignments/`)
- *To be organized*

### **📊 Resources** (`resources/`)
- *Additional reading materials to be added*

---

## 🎯 **Learning Objectives**

1. **Understand simulation methodology:**
   - Mathematical model selection
   - Field data integration
   - Multiple simulation runs for statistical confidence

2. **Master three key probability distributions:**
   - **Normal Distribution** - Travel times between stops
   - **Poisson Distribution** - Passenger arrivals at stops  
   - **Binomial Distribution** - Passenger alighting behavior

3. **Apply simulation to policy analysis:**
   - Evaluate bus route efficiency
   - Assess policy interventions
   - Develop data governance arguments

---

## 🚌 **Case Study: City Bus No. 56**

### **Problem Context**
- Current passenger load factor: 32% during busiest hour
- Question: Is frequency increase justified?
- Need evidence-based policy recommendations

### **Simulation Approach**
1. **Data Collection:** 30 trips via Hong Kong government API
2. **Model Building:** Three statistical distributions for different processes
3. **Simulation Runs:** 1000 iterations for statistical confidence
4. **Results Analysis:** Compare before/after route adjustments

### **Key Finding**
Route adjustments **reduced** overall seat utilization:
- **Before:** 18-56% (forward), 8-58% (return)
- **After:** 12-34% (forward), 5-34% (return)

---

## 💡 **Data Governance Insights**

### **Current Data Gaps**
- Unclear load factor definitions
- Limited temporal data (30 trips only)
- Missing passenger flow details

### **Simulation-Driven Improvements**
- Better data → more accurate models
- Real-time data → dynamic optimization
- Open data → independent validation

---

## 🛠️ **Technical Tools Used**

### **Python Libraries**
- `python-pptx` - PowerPoint processing
- `SimPy` - Discrete event simulation
- Standard statistical libraries

### **Data Sources**
- Hong Kong Open Data API (`https://data.gov.hk/en/`)
- Real-time bus arrival data
- Route and stop information

---

## 📈 **Next Steps**

1. **For Students:**
   - Review simulation methodology
   - Practice with distribution selection
   - Apply to your own policy problems

2. **For Instructors:**
   - Prepare hands-on simulation exercises
   - Develop data governance case studies
   - Create assessment rubrics

---

## 🔗 **Related Materials**

- **Data Resources:** `../../../04_data_resources/open_data_inventory/`
- **Extraction Scripts:** `../../../05_scripts_utilities/content_extraction/`
- **AI Teaching Aids:** `../../../03_instructor_tools/ai_assistants/`

---

*Week 4 materials organized and enhanced on September 22, 2025*
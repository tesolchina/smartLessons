# GCAP 3226 Week 2 Materials Guide
## Data Visualization for Hong Kong Policy Analysis

**Created:** September 6, 2025  
**For:** Students with zero programming experience  
**Focus:** Understanding Week 2 materials with GitHub Copilot assistance

---

## 📁 **What's in Week 2 Materials?**

The Week 2 folder contains three essential files that introduce you to **data visualization** - a core skill for policy analysis:

### 1. **week2.csv** - Hong Kong Garbage Bag Policy Data 📊
- **What it is:** Real survey data about Hong Kong's garbage bag charging policy
- **Size:** 98 respondents, 28 data columns
- **Focus:** Public opinions on waste management policy (SDG 12: Responsible Consumption)

### 2. **GCAP3226_week2_full.ipynb** - Complete Tutorial 📚
- **What it is:** Step-by-step data visualization tutorial with all answers
- **Purpose:** Teacher reference and complete example
- **Content:** Fully working Python code for all visualization tasks

### 3. **GCAP3226_week2_student.ipynb** - Your Learning Notebook ✍️
- **What it is:** Guided practice notebook for students
- **Purpose:** Learn by doing with GitHub Copilot assistance
- **Content:** Tasks with prompts but code cells left empty for you to complete

---

## 🎯 **Learning Objectives: Why This Matters for Policy Analysis**

Based on the course syllabus, this week builds essential skills for your semester-long **team policy analysis project**:

### **Data Skills You'll Develop:**
- **Load and examine datasets** → Understand policy-relevant data
- **Create visualizations** → Communicate findings clearly to policymakers
- **Analyze patterns** → Identify trends that inform policy recommendations
- **Save professional charts** → Include in policy reports and presentations

### **Policy Connection:**
- **Real Hong Kong data** → Practice with actual government policy issues
- **Public opinion analysis** → Understand citizen perspectives on policy
- **Evidence-based insights** → Learn to support policy arguments with data
- **Communication skills** → Present data findings to non-technical audiences

---

## 🔍 **Understanding the Data: Hong Kong Garbage Bag Policy Survey**

### **What the Survey Measures:**

#### **Opinion Variables (1-5 Scale):**
- `support_info` → Support **before** policy information (1=Strongly oppose, 5=Strongly support)
- `support_after_info` → Support **after** policy information 
- `fairness` → How fair is the policy? (1=Very unfair, 5=Very fair)
- `government_consideration` → Did government consider citizen needs? (1=Not at all, 5=Very fully)
- `policy_helpfulness` → How helpful is this policy? (1=Not helpful, 4=Very helpful)
- `waste_severity` → How severe is Hong Kong's waste problem? (1=Not severe, 4=Highly severe)

#### **Behavior Variables:**
- `recycling_effort` → Personal recycling effort level
- `food_waste_behavior` → Experience with food waste bins (never_seen, seen_not_used, seen_and_used)

#### **Geographic Variables:**
- `HongKongDistrict_[Name]` → Which district do you live in? (coded as 0/1)
- `Distance_artificial` → Distance to nearest recycling facility (meters)

#### **Housing Variable:**
- `HousingType_Publicrentalhousing` → Do you live in public housing? (0/1)

### **Why This Data Matters:**
This represents **real citizen feedback** on Hong Kong policy - exactly the type of data you'll analyze in your team projects!

---

## 🚀 **For Students with ZERO Programming Experience: Don't Panic!**

### **💡 Key Insight: You Don't Need to Learn Programming - You Need to Learn Prompting!**

**Traditional Learning:**
- ❌ Memorize Python syntax
- ❌ Debug complex errors
- ❌ Struggle with technical details

**Modern Learning with GitHub Copilot:**
- ✅ Write clear English requests (prompts)
- ✅ Let AI generate the code
- ✅ Focus on understanding results
- ✅ Learn by asking questions

---

## 🤖 **GitHub Copilot: Your AI Programming Assistant**

### **What GitHub Copilot Does:**
- **Reads your comments** (prompts starting with `#`)
- **Generates Python code** automatically
- **Suggests complete solutions** to data analysis tasks
- **Explains code** when you ask

### **How to Use Copilot Effectively:**

#### **1. Write Clear Prompts:**
```python
# Write code to load week2.csv into a pandas DataFrame and show the first five rows
```
✅ **Good:** Specific, clear task
❌ **Bad:** `# do data stuff`

#### **2. Use Step-by-Step Instructions:**
```python
# Write code to create bar charts for support_info and support_after_info
# Put the plots in a 1x2 grid
# Label the 1-5 scale as 1=Strongly oppose, 5=Strongly support
```

#### **3. Ask for Modifications:**
```python
# Modify the chart above to use different colors and add a title
```

---

## 📚 **Essential Tools & Skills for This Course**

### **Python Libraries (Don't Worry - Copilot Handles This!):**

#### **1. Pandas** 🐼
- **What it does:** Loads and manipulates data (like Excel, but more powerful)
- **Your role:** Write prompts like "load the CSV file" or "show summary statistics"
- **Copilot's role:** Generates `pd.read_csv()`, `df.describe()`, etc.

#### **2. Matplotlib** 📊
- **What it does:** Creates charts and graphs
- **Your role:** Request "create a bar chart" or "make a pie chart"
- **Copilot's role:** Generates `plt.figure()`, `plt.bar()`, etc.

#### **3. Seaborn** 🎨
- **What it does:** Makes beautiful, professional visualizations
- **Your role:** Ask for "attractive bar chart" or "professional styling"
- **Copilot's role:** Generates `sns.countplot()`, `sns.scatterplot()`, etc.

### **Key Visualization Types You'll Master:**

#### **📊 Bar Charts** - Compare categories
- **When to use:** Comparing support levels across districts
- **Policy value:** Show public opinion differences by area

#### **🥧 Pie Charts** - Show proportions
- **When to use:** Overall support distribution
- **Policy value:** Communicate simple percentages to officials

#### **📈 Scatter Plots** - Show relationships
- **When to use:** Distance vs. recycling behavior
- **Policy value:** Identify factors that influence policy success

#### **📦 Box Plots** - Show data distribution
- **When to use:** Understanding range of distances to facilities
- **Policy value:** Identify service gaps and inequalities

---

## 🎯 **How This Connects to Your Team Project (Based on Syllabus)**

### **Week 2 Skills → Semester Project Applications:**

#### **Phase 1: Data Collection (Weeks 4-6)**
- Use pandas skills to load government datasets
- Apply data examination techniques to understand structure
- Create preliminary visualizations to explore patterns

#### **Phase 2: Analysis (Weeks 7-9)**  
- Use advanced visualization techniques for deeper analysis
- Create cross-tabulations like district vs. behavior analysis
- Generate statistical summaries for policy insights

#### **Phase 3: Reporting (Weeks 10-12)**
- Save professional charts for policy reports
- Create compelling visualizations for presentations
- Use data storytelling to support policy recommendations

#### **Phase 4: Presentation (Weeks 13-14)**
- Present visual findings to "policymaker" audience
- Demonstrate evidence-based policy insights
- Show how data supports your team's recommendations

---

## 🛠️ **Step-by-Step Guide: How to Approach Week 2**

### **Before You Start:**
1. **Install required packages** (instructions provided in notebook)
2. **Open GitHub Copilot** in VS Code
3. **Download the CSV file** to your working directory

### **Working Through the Notebook:**

#### **Section 0: Import Libraries**
```python
# Write code to import pandas, matplotlib, and seaborn
```
**What happens:** Copilot generates import statements
**Your focus:** Understanding what each library does

#### **Section 1: Load Data**  
```python
# Write code to load week2.csv into a pandas DataFrame and show the first five rows
```
**What happens:** Copilot loads the CSV and displays data
**Your focus:** Understanding the data structure and variables

#### **Section 2: Examine Data**
```python
# Write code to display dataset info and summary statistics  
```
**What happens:** Copilot shows data types and numerical summaries
**Your focus:** Interpreting what the numbers mean for policy

#### **Section 3: Categorical Visualizations**
```python
# Write code to create a frequency table for support_level
# Write code to create a bar chart for support_info with proper labels
```
**What happens:** Copilot creates professional charts
**Your focus:** Reading the charts and understanding public opinion patterns

#### **Section 4: Continuous Data Analysis**
```python
# Write code to display summary statistics for Distance_artificial
# Write code to create box plot and histogram for distance data
```
**What happens:** Copilot analyzes the distance variable
**Your focus:** Understanding geographic access to recycling facilities

#### **Section 5: Relationship Analysis**
```python
# Write code to create scatter plot of distance vs recycling effort
```
**What happens:** Copilot explores if distance affects behavior  
**Your focus:** Identifying policy-relevant relationships

---

## 💡 **Pro Tips for Success with Zero Programming Experience**

### **1. Focus on Questions, Not Code**
- **Ask:** "What does this chart tell us about Hong Kong policy?"
- **Don't worry about:** Python syntax or technical details

### **2. Use Copilot Chat for Explanations**
- **Type:** "Explain what this scatter plot shows"
- **Or:** "What policy insights can we draw from this bar chart?"

### **3. Think Like a Policy Analyst**
- **For each chart ask:** 
  - What does this tell us about citizen opinions?
  - How could this inform policy decisions?
  - What additional questions does this raise?

### **4. Practice with Variations**
```python
# Create the same chart but with different colors
# Add a title that explains the policy relevance  
# Save this chart as a PNG file for a report
```

### **5. Connect to Real Policy Issues**
- **Think:** "How would I present this to the Hong Kong government?"
- **Consider:** "What policy changes does this data suggest?"

---

## 🎯 **Assessment Connection: How This Prepares You**

Based on the course syllabus, Week 2 skills directly support your assessment components:

### **Individual Assessments (50%):**
- **In-class exercises (10%)** → Practice with similar datasets
- **Reflective essays (20%)** → Analyze what visualizations reveal about policy
- **Human-AI report (20%)** → Document how you use Copilot for analysis

### **Group Project (50%):**
- **Presentations (20%)** → Use professional visualizations from your team data
- **Final report (30%)** → Include charts that support policy recommendations

---

## 🚀 **Beyond Week 2: Building Your Policy Analysis Skills**

### **Skills That Transfer to Any Policy Topic:**
1. **Data loading and examination** → Works with any government dataset
2. **Visualization creation** → Essential for all policy reports
3. **Pattern interpretation** → Core analytical thinking skill
4. **Professional presentation** → Critical for policy communication

### **Next Steps in the Course:**
- **Week 3-4:** Apply these skills to your chosen policy area
- **Week 5-6:** Collect and analyze your team's policy data
- **Week 7-9:** Create advanced visualizations for deeper insights
- **Week 10+:** Use charts to support policy recommendations

---

## 🎊 **Conclusion: You're Ready for Data-Driven Policy Analysis!**

### **Remember:**
- ✅ **You don't need to become a programmer** - you need to become a skilled prompter
- ✅ **GitHub Copilot handles the technical details** - you focus on policy insights
- ✅ **These visualization skills are essential** for modern policy analysis
- ✅ **Practice with Hong Kong data prepares you** for your team project

### **Your Success Formula:**
1. **Clear prompts** → Copilot generates code
2. **Focus on interpretation** → What do the charts mean?
3. **Connect to policy** → How does this inform decisions?
4. **Practice regularly** → Build confidence with AI assistance

**You're not just learning data visualization - you're learning to be a modern policy analyst who can harness AI tools to create evidence-based recommendations for Hong Kong's future!** 🚀

---

*Ready to start? Open the student notebook and begin your journey into data-driven policy analysis with your AI assistant!*

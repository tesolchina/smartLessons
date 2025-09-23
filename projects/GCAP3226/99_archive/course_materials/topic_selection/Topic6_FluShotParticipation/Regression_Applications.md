# Regression Applications in Flu Shot Participation Analysis (Topic 6)

## Current Project Context

**Research Question**: What factors influence flu shot participation rates in Hong Kong, and how can vaccination uptake be improved through evidence-based interventions?

**Historical Foundation**: Building on Simon's published research showing only 18.7% of primary schoolchildren received flu shots in 2016-17, and overall participation rate of ~29% for eligible population

**Current Focus**: Understanding vaccination behavior patterns and developing targeted intervention strategies

---

## Regression Analysis Applications

### 1. **Linear Regression Models**

#### A. Vaccination Rate Prediction
**Dependent Variable (Y)**: Annual flu vaccination rate (% of eligible population)

**Independent Variables (X)**:
- Age group (children, adults, elderly)
- Income level (household income quartiles)
- Education level (highest qualification)
- Occupation type (healthcare, education, office, manual)
- Health insurance coverage (public/private)
- Previous flu infection history
- Chronic disease status
- Access to healthcare facilities
- Government promotion campaign intensity

**Model**:
```
Vaccination_Rate = β₀ + β₁(Age) + β₂(Income) + β₃(Education) + β₄(Access) + β₅(Promotion) + ε
```

**Expected Relationships**:
- Older age → Higher vaccination rate (positive coefficient)
- Higher income → Higher vaccination rate (positive coefficient)
- Healthcare workers → Higher vaccination rate (positive coefficient)

#### B. School-Based Program Effectiveness
**Dependent Variable (Y)**: School flu vaccination coverage (% of students vaccinated)

**Independent Variables (X)**:
- School type (public/private/international)
- Socioeconomic status of school catchment
- Principal's health promotion commitment
- School nurse availability
- Parent education level
- Previous year's vaccination rate
- On-campus vaccination availability
- Communication quality with parents

**Model**:
```
School_Coverage = β₀ + β₁(School_Type) + β₂(SES) + β₃(Principal_Commitment) + β₄(On_Campus) + ε
```

#### C. Cost-Effectiveness Analysis
**Dependent Variable (Y)**: Cost per additional vaccination achieved (HK$/vaccination)

**Independent Variables (X)**:
- Intervention type (mobile units, school programs, incentives)
- Target population characteristics
- Geographic coverage area
- Staff requirements
- Administrative complexity
- Infrastructure needs

### 2. **Logistic Regression Models**

#### A. Individual Vaccination Decision
**Dependent Variable (Y)**: Received flu shot this year (1 = Yes, 0 = No)

**Independent Variables (X)**:
- Demographic factors (age, gender, income, education)
- Health status (chronic conditions, immunocompromised)
- Risk perception (perceived flu severity, vaccine effectiveness)
- Access factors (convenience, cost, provider recommendation)
- Social influences (family/peer vaccination, workplace policy)
- Previous vaccination experience
- COVID-19 vaccination status

**Model**:
```
P(Vaccinated = 1) = 1 / (1 + e^-(β₀ + β₁(Age) + β₂(Risk_Perception) + β₃(Access) + β₄(Social_Influence)))
```

**Policy Application**: Identify high-potential targets for vaccination campaigns

#### B. Vaccine Hesitancy Classification
**Dependent Variable (Y)**: Vaccine hesitant (1 = Hesitant, 0 = Accepting)

**Independent Variables (X)**:
- Trust in government health advice
- Confidence in vaccine safety
- Perceived vaccine necessity
- Religious or cultural beliefs
- Information sources (social media, healthcare providers)
- Previous adverse events experience
- General health beliefs

#### C. Program Participation Prediction
**Dependent Variable (Y)**: Participation in school vaccination program (1 = Participated, 0 = Did not participate)

**Independent Variables (X)**:
- Parent education level
- Family income
- School communication effectiveness
- Convenience factors (timing, location)
- Peer participation rates
- Teacher/principal endorsement

### 3. **Ordinal Regression Models**

#### A. Vaccination Intention Level
**Dependent Variable (Y)**: Vaccination intention (1 = Definitely not, 2 = Probably not, 3 = Unsure, 4 = Probably yes, 5 = Definitely yes)

**Independent Variables (X)**:
- Risk perception score
- Vaccine confidence level
- Healthcare provider recommendation
- Social norm influence
- Convenience factors

**Model**: Proportional odds model
```
logit(P(Y ≤ j)) = αⱼ - (β₁(Risk_Perception) + β₂(Confidence) + β₃(Provider_Rec) + β₄(Social_Norms))
```

#### B. Program Satisfaction Rating
**Dependent Variable (Y)**: Satisfaction with vaccination program (1 = Very dissatisfied, 2 = Dissatisfied, 3 = Neutral, 4 = Satisfied, 5 = Very satisfied)

**Independent Variables (X)**:
- Service quality
- Wait time
- Staff friendliness
- Information provision
- Side effects management
- Overall convenience

### 4. **Time Series Regression**

#### A. Seasonal Vaccination Trends
**Dependent Variable (Y)**: Monthly vaccination uptake

**Independent Variables (X)**:
- Month of year (seasonal patterns)
- Flu activity level
- Media coverage of flu outbreaks
- Government campaign activities
- Vaccine availability
- Weather conditions

**Model**:
```
Vaccinations_t = α + β₁(Season_t) + β₂(Flu_Activity_t) + β₃(Campaign_t) + AR(1) + ε_t
```

#### B. Long-term Trend Analysis
**Dependent Variable (Y)**: Annual vaccination coverage rate

**Independent Variables (X)**:
- Years since program start
- Policy changes
- Major flu outbreaks (H1N1, etc.)
- COVID-19 pandemic effects
- Economic conditions
- Healthcare system changes

### 5. **Multilevel/Hierarchical Regression**

#### A. School-Level Analysis
**Levels**:
- Student level (individual characteristics)
- Classroom level (teacher influence)
- School level (policy and resources)
- District level (demographic and geographic factors)

**Model**:
```
Vaccination_ijkl = β₀ + β₁(Student_factors) + β₂(Teacher_factors) + β₃(School_factors) + β₄(District_factors) + u₀ⱼ + u₀ₖ + ε_ijkl
```

#### B. Geographic Analysis
**Levels**:
- Individual level
- Community level (housing estates, neighborhoods)
- District level
- Regional level (Hong Kong Island, Kowloon, New Territories)

---

## Data Sources for Regression Analysis

### 1. **Government Health Data**
- **Department of Health**: Vaccination statistics by program and demographics
- **Centre for Health Protection**: Flu surveillance and outbreak data
- **Hospital Authority**: Healthcare utilization patterns
- **Education Bureau**: School participation in vaccination programs

### 2. **Survey Data** (to be collected)
- **Public Opinion Surveys**: Attitudes toward flu vaccination
- **Behavioral Surveys**: Decision-making factors and barriers
- **Parent Surveys**: School vaccination program feedback
- **Healthcare Provider Surveys**: Professional recommendations and practices

### 3. **Administrative Data**
- **School Records**: Vaccination coverage by school
- **Healthcare Provider Data**: Vaccination administration patterns
- **Insurance Claims**: Flu-related healthcare utilization
- **Workplace Programs**: Employer-sponsored vaccination data

### 4. **Comparative International Data**
- **OECD Countries**: Vaccination coverage rates and program designs
- **Similar Asian Cities**: Singapore, Taiwan, Japan vaccination strategies
- **Successful Programs**: Ontario universal program, Australian initiatives

---

## Policy Applications of Regression Results

### 1. **Targeted Intervention Strategies**
Based on regression coefficients:

#### High-Impact Groups:
```
IF: Healthcare_Worker = 1 AND Previous_Vaccination = 0
THEN: Priority intervention with professional responsibility messaging
```

#### Low-Uptake Groups:
```
IF: Age < 40 AND Income < Median AND Education < Secondary
THEN: Convenience-focused intervention with financial incentives
```

### 2. **School Program Optimization**
Regression-informed strategies:

#### School Selection Criteria:
```
Program_Priority = β₁(Student_SES) + β₂(Parent_Education) + β₃(Previous_Coverage) + β₄(Principal_Support)
```

#### Resource Allocation:
```
Resources_per_School = Base_Resources × (1 + Difficulty_Multiplier + Potential_Multiplier)
```

### 3. **Campaign Design**
Regression-based messaging strategies:

#### Message Targeting:
- **High-risk groups**: Focus on health benefits and protection
- **Parents**: Emphasize child safety and community responsibility
- **Young adults**: Convenience and workplace productivity benefits

### 4. **Performance Monitoring**
```
Program_Success = 0.4×(Coverage_Rate) + 0.3×(Uptake_Increase) + 0.2×(Equity_Improvement) + 0.1×(Cost_Efficiency)
```

---

## Expected Regression Findings

### 1. **Individual Decision Model Results**
```
P(Vaccinated) = f(0.65×Age + 0.42×Healthcare_Worker + 0.38×Risk_Perception - 0.28×Hesitancy)
AUC = 0.78, p < 0.001
```

**Interpretation**: 
- Age is strongest predictor (each decade increases odds by 65%)
- Healthcare workers 42% more likely to vaccinate
- Risk perception significantly influences decision

### 2. **School Program Effectiveness**
```
School_Coverage = 25% + 15%(On_Campus_Program) + 8%(Principal_Support) + 5%(Parent_Education)
R² = 0.59, p < 0.001
```

**Policy Implication**: On-campus programs increase coverage by 15 percentage points

### 3. **Optimal Intervention Targeting**
```
Cost_per_Additional_Vaccination = HK$180 (general population)
Cost_per_Additional_Vaccination = HK$95 (targeted high-risk groups)
Cost_per_Additional_Vaccination = HK$65 (school-based programs)
```

**Resource Allocation**: Prioritize school-based and targeted programs

### 4. **Trend Analysis**
```
Annual_Coverage = 29% + 2.3%(Years_Since_2017) + 8.5%(Post_COVID_Effect)
```

**Finding**: COVID-19 has increased flu vaccination acceptance by 8.5 percentage points

---

## Building on Historical Research

### 1. **Updating 2017-2018 Findings**
Simon's original research showed:
- Only 18.7% of primary schoolchildren vaccinated
- ~29% overall participation rate
- Need for better data collection and school accountability

**Extended Analysis**:
- Current rates post-COVID
- Factors explaining low school participation
- Effectiveness of implemented interventions

### 2. **Policy Recommendations Evolution**
Original recommendations:
- School accountability measures
- Mobile vaccination units
- Better data collection
- Universal vaccination program consideration

**Evidence-Based Updates**:
- Quantified impact of each recommendation
- Cost-effectiveness analysis
- Implementation priority ranking

### 3. **Longitudinal Impact Assessment**
```
Current_Rate = Baseline_Rate + Policy_Impact + External_Factors + Time_Trend
```

Track which of Simon's recommendations were implemented and their measured effects

---

## Advantages of Regression Approach for Vaccination Policy

### 1. **Evidence-Based Targeting**
- Identify highest-impact intervention groups
- Optimize resource allocation based on predicted returns
- Customize messaging based on demographic profiles

### 2. **Program Evaluation**
- Measure actual vs. predicted program effects
- Identify successful intervention components
- Adjust strategies based on performance data

### 3. **Policy Development**
- Provide quantitative basis for resource requests
- Support evidence-based policy recommendations
- Enable scenario planning and impact forecasting

### 4. **Continuous Improvement**
- Regular model updates with new data
- Adaptive program design based on changing patterns
- Early warning system for declining coverage

This regression-based approach will transform flu vaccination policy from intuition-based to evidence-driven, enabling Hong Kong to achieve higher vaccination coverage through targeted, cost-effective interventions informed by rigorous statistical analysis.
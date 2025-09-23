# GCAP3226 Week 3: Regression Analysis - Key Points

## Course Context: Municipal Solid Waste (MSW) Charging Policy Case Study

**Objective**: Using linear regression models to analyse public willingness toward MSW charging policy in Hong Kong

**Policy Background**: "Polluter Pays" Principle - waste producers bear disposal costs based on quantity generated

---

## 1. Types of Regression Models

### Linear Regression
- **Purpose**: Model continuous response variable (e.g., amount willing to pay) vs explanatory variables
- **Key Features**:
  - Assumes a linear relationship
  - Estimates effects based on observed data
  - Quantifies expected change in response for one-unit increase in explanatory variable, holding other variables constant
- **Important Note**: Not for causal inference!

### Logistic Regression
- **Purpose**: Model binary response variable (e.g., support vs. oppose)
- **Mathematical Foundation**:
  ```
  P(Y = 1) = 1 / (1 + e^(-(β₀ + β₁X)))
  ```
- **Logit Form**:
  ```
  ln(p/(1-p)) = β₀ + β₁X
  ```
- **Why Use It**: Transforms probabilities to ensure outputs stay between 0 and 1

### Ordinal Regression
- **Purpose**: Model ordinal categorical response variable (e.g., oppose, neutral, support)
- **Application**: When response variable has natural ordering but unequal intervals

---

## 2. Key Concepts in Logistic Regression

### Odds and Odds Ratios
- **Odds**: p/(1-p) ratio
  - Example: If probability of winning = 0.5, then odds = 1:1
- **Log Odds**: Natural logarithm of odds
- **Coefficient Interpretation**:
  - β₀: Log odds of y=1 when x=0
  - β₁: Change in log odds for 1-unit change in x
  - For binary x: β₁ is log odds ratio comparing x=1 vs x=0 groups

### Odds Ratio Interpretation
- **Odds Ratio = 1**: Exposure doesn't affect odds
- **Odds Ratio > 1**: Associated with higher odds of y=1
- **Odds Ratio < 1**: Associated with lower odds of y=1

---

## 3. Study Design Framework

### Research Process
1. **Research Questions** → Define what you want to investigate
2. **Questionnaire Construction** → Specify response variable (y) and exploratory variables (x)
3. **Sampling Methods** → Choose appropriate sampling strategy
4. **Data Collection** → Gather survey responses
5. **Analysis & Reporting** → Process data and interpret results

### Sampling Methods
#### Probability Sampling
- **Method**: Randomly selecting samples
- **Advantage**: Representative sample; results generalizable to entire population
- **Preferred for**: Definitive policy recommendations

#### Non-probability Sampling
- **Method**: Samples selected based on criteria other than random chance
- **Types**:
  - *Convenience sampling*: Based on ease of access
  - *Snowball sampling*: Respondents refer acquaintances
- **Use for**: Exploratory analyses

---

## 4. Case Study Results Summary

### Sample Characteristics
- **Sample Size**: 97 respondents (non-probability sample)
- **Limitation**: Small, non-representative sample with selection bias risk

### Key Findings
- **Perceived Government Responsiveness**:
  - Coefficient ≈ 0.54 (p < 0.01)
  - Increases odds of higher willingness to support policy
- **Perceived Policy Fairness**:
  - Coefficient ≈ 0.42 (p < 0.01)
  - Positive association with support
- **Model Performance**: R² ≈ 0.61 (adequate but exploratory)

### Limitations
- Small sample size limits generalizability
- Non-representative sampling may have selection bias
- Over-representation of educated respondents
- Needs validation with larger probability-based surveys (n=500+ with stratified random sampling)

---

## 5. Policy Recommendations Based on Regression Analysis

### Primary Strategy: Enhance Government Responsiveness
- **Action**: Improve public engagement through town halls and online portals
- **Expected Impact**: Potentially boost willingness by 0.5 points
- **Caveat**: Pending validation in larger, probability-based samples

### Secondary Strategy: Address Fairness Concerns
- **Action**: Implement transparent equity measures (e.g., low-income subsidies)
- **Rationale**: Based on significant positive coefficient for perceived fairness

### Supporting Evidence
- Pre-post analysis suggests targeted information about waste crisis severity and policy benefits may enhance public support

---

## 6. Critical Considerations

### Statistical vs. Causal Inference
- **Important**: Regression shows associations, not causation
- **Implication**: Results suggest relationships but don't prove that changing variables will cause desired outcomes

### Sample Size and Representativeness
- **Current Study**: Exploratory due to small, non-probability sample
- **Recommendation**: Conduct larger probability-based survey for definitive policy guidance
- **Target**: n=500+ with stratified random sampling

### Model Validation
- **Need**: Validate findings with different samples and methods
- **Purpose**: Ensure robustness before implementing policy changes

---

## 7. Technical Notes

### When to Use Each Model Type
- **Linear Regression**: Continuous outcomes (e.g., amount willing to pay)
- **Logistic Regression**: Binary outcomes (e.g., support/oppose)
- **Ordinal Regression**: Ordered categorical outcomes (e.g., strongly oppose/oppose/neutral/support/strongly support)

### Model Interpretation Best Practices
1. Always report confidence intervals with coefficients
2. Consider practical significance alongside statistical significance
3. Acknowledge limitations of sample and methodology
4. Distinguish between association and causation
5. Validate findings with additional studies when possible
Case Study I: Public Willingness 
Toward the Municipal Solid Waste 
(MSW) Charging Policy
GCAP3226 2025/09/16
1


---

Recap of week 2
Public willingness to support MSW charging policy is assessed by data visualization.
72% against policy (Sing Tao News Corporation; Source URL : Survey: 72pc against reviving waste-charging, 
fear costs amid better recycling habits | The Standardhttps://www.thestandard.com.hk/hong-kong-
news/article/311098/
2


---

Objectives of Case Study I
◦ To equip students with analytical tools for data-informed policymaking in 
Hong Kong (CILO 1)
◦ To explore using linear regression models to analyse public willingness 
◦ Policy recommendation
3


---

Structure of Case Study I
◦ Background
◦ Study design
◦ Linear Regression models
◦ Results Interpretation
◦ Recommendations
◦ In-class Exercise
4


---

Background
◦ Hong Kong’s waste amount: 3.97 million tonnes of MSW in 2023 (EPD, 2023)
◦ 2 landfills projected to be exhausted in 2026 (Government Press Releases, 2024)
Solid waste
Municipal solid 
waste (MSW)
Domestic waste
Commercial and 
industrial (C&I) 
waste
Overall 
construction 
waste
Special waste
5


---

Policy Background
o“Polluter Pays” Principle: requires waste producers to bear the cost of disposal 
based on the quantity generated, incentivizing waste reduction and recycling. 
oApplies to all sectors producing MSW, including residential (domestic) and non-
residential (commercial and industrial) premises.
6


---

Study design
Research 
questions
Questionnaire 
construction
Sampling 
methods
Collect data
Process, 
analyse data, 
and report
Questionnaire construction
•Specify response variable (y) and exploratory variables (x)
Sampling methods
•Probability sampling: randomly selecting samples
o Representative sample; results can be generalized to the entire population
•Nonprobability sampling: samples are selected based on criteria
other than random chance -> exploratory analyses
◦ Convenience sampling: chosen based on relative ease of access
◦ Snowball sampling: respondents refer acquaintance
7


---

Statistical Background: Regression Models
◦ Linear Regression: model continuous response variable (e.g., amount willing to 
pay) vs explanatory variables
▪Assumes a linear relationship
▪Estimates the effect based on observed data
▪Quantifies the expected change in response for a one-unit increase in an 
explanatory variable, holding other variables the same
◦ Logistic Regression: model binary response variable (e.g., support vs. oppose)
◦ Ordinal Regression: model ordinal categorical response variable (e.g., oppose, 
neutral, support)
Not Causal Inference!
8


---

Model binary response
•To model the probability that Y belongs to a particular category, rather than 
modelling the response as 0 or 1 directly. 
•However, unreasonable prediction may occur.
•Transform 𝑃(𝑋��� = 1) using a function that gives 
outputs between 0 and 1 for all values of 𝑋.
𝑃(𝑋��� = 1) = 𝛼���0 + 𝛼���1𝑋?
9


---

Logistic regression model
•Many functions meet this criterion, logistic regression uses the logistic function
•The standard logistic function is 
𝑒��� 𝑥 =
1
1 + 𝑒−𝑥
•Accordingly, 
𝑃(𝑋��� = 1) =
1
1 + 𝑒−(𝛽0+𝛽1𝑋)
10


---

Logistic regression model
𝑃(𝑋��� = 1) = 𝑛��� =
1
1 + 𝑒−(𝛽0+𝛽1𝑋)
ln
𝑛���
1 − 𝑛���
= 𝛼���0 + 𝛼���1𝑋
𝑙𝑛���𝑒���𝑖𝑡(𝑛���)
11


---

Interpretation of model coefficients
•
𝑝
1−𝑝 is called odds.
•E.g., 𝑛��� is the probability of winning a game. If 𝑛��� = ½, the odds of winning is 1:1.
•ln
𝑝
1−𝑝 = 𝛼���0 + 𝛼���1𝑋
•𝛼���0 is the log odds of y = 1 when x = 0
•𝛼���1 is the change of log odds of y = 1 with 1 unit change of x. If x is binary, 𝛼���1 is the 
log odds ratio of y = 1 of the x = 1 group vs the x = 0 group.
•Odds ratio = 1 (>1,<1) means exposure does not affect (associated with higher, 
lower) odds of y = 1
12


---

Ordinal logistic regression model
𝑃 𝑋��� ≤ 1 = 𝜋1, 𝑃 𝑋��� ≤ 2 = 𝜋1 + 𝜋2, 𝜋1+ 𝜋2 + 𝜋3= 1
𝑙𝑛���𝑒���𝑖𝑡 𝑃 𝑋��� ≤ 1
= 𝑙𝑛
𝜋1
𝜋2+𝜋3
= 𝛼1 − 𝛼���𝑥
𝑙𝑛���𝑒���𝑖𝑡 𝑃 𝑋��� ≤ 2
= 𝑙𝑛
𝜋1+ 𝜋2
𝜋3
= 𝛼2 − 𝛼���𝑥
13


---

Brief summary of regression results
oRegression models on public support for Hong Kong's waste charging policy, 
based on 97 non-probability samples.
oKey predictors: Perceived government responsiveness (coefficient ≈ 0.54, 
p<0.01; increases odds of higher willingness).Perceived policy fairness 
(coefficient ≈0.42, p<0.01).Model fit: R² ≈ 0.61 (adequate but exploratory).
oLimitations: Small, non-representative sample risks selection bias (e.g., 
educated over-representation), limiting generalizability; needs validation via 
larger probability-based surveys (e.g., n=500+ stratified random samples).
14


---

Policy recommendation
oPrioritize responsiveness: Enhance public engagement (e.g., town halls, online 
portals) to build trust, potentially boosting willingness by 0.5 points 
improvement, pending validation in larger, probability-based samples.
oAddress fairness secondarily: Implement transparent equity (e.g., low-income 
subsidies).
oPreliminary evidence from the pre-post analysis suggests that targeted 
information on Hong Kong's waste crisis severity and policy benefits may 
enhance public support for MSW charging.
15


---


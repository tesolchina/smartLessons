# Regression Applications in Bus Stop Merge Analysis (Topic 2)

## Current Project Context

**Research Question**: Should two bus stops only 25 meters apart (St. Martin Road and Chong San Road stations) be merged to improve efficiency?

**Current Approach**: Discrete-event simulation comparing 4 scenarios:
1. Current setup (2 berths per station)
2. Designated routes per station
3. Merged 4-berth superstation
4. Single 2-berth station

---

## Regression Analysis Applications

### 1. **Linear Regression Models**

#### A. Passenger Waiting Time Prediction
**Dependent Variable (Y)**: Average passenger waiting time (seconds)

**Independent Variables (X)**:
- Bus arrival frequency (buses per hour)
- Passenger arrival rate (passengers per hour)
- Number of available berths
- Distance between stops (meters)
- Time of day (peak vs off-peak)
- Weather conditions
- Number of overlapping routes

**Model**: 
```
Waiting_Time = β₀ + β₁(Bus_Frequency) + β₂(Passenger_Rate) + β₃(Berths) + β₄(Distance) + ε
```

**Expected Relationships**:
- Higher bus frequency → Lower waiting time (negative coefficient)
- Higher passenger rate → Higher waiting time (positive coefficient)
- More berths → Lower waiting time (negative coefficient)

#### B. Bus Queue Time Prediction
**Dependent Variable (Y)**: Average bus queue time (seconds)

**Independent Variables (X)**:
- Number of berths available
- Passenger boarding time per bus
- Bus clearance time
- Route overlap percentage
- Peak hour intensity

**Model**:
```
Queue_Time = β₀ + β₁(Berths) + β₂(Boarding_Time) + β₃(Route_Overlap) + ε
```

#### C. Cost-Benefit Analysis
**Dependent Variable (Y)**: Total operational cost (HK$ per hour)

**Independent Variables (X)**:
- Infrastructure costs (berth construction/maintenance)
- Passenger time costs (valued in monetary terms)
- Bus operational delays
- Fuel consumption due to queuing

### 2. **Logistic Regression Models**

#### A. Merger Decision Model
**Dependent Variable (Y)**: Binary decision (1 = Merge stops, 0 = Keep separate)

**Independent Variables (X)**:
- Distance between stops (meters)
- Passenger volume difference between stops
- Route overlap percentage
- Infrastructure cost ratio
- Accessibility impact score
- Traffic congestion level

**Model**:
```
P(Merge = 1) = 1 / (1 + e^-(β₀ + β₁X₁ + β₂X₂ + ... + βₖXₖ))
```

**Interpretation**: 
- If distance < threshold AND overlap > threshold → Higher probability of merger benefit
- Odds ratio for distance: For every 10m increase in distance, odds of successful merger decrease by X%

#### B. Passenger Satisfaction Model
**Dependent Variable (Y)**: Binary satisfaction (1 = Satisfied, 0 = Not satisfied)

**Independent Variables (X)**:
- Walking distance increase due to merger
- Waiting time change
- Service frequency improvement
- Age group (elderly more sensitive to walking distance)
- Mobility status (disabled, wheelchair users)

### 3. **Ordinal Regression Models**

#### A. Service Quality Rating
**Dependent Variable (Y)**: Service quality rating (1 = Very Poor, 2 = Poor, 3 = Fair, 4 = Good, 5 = Excellent)

**Independent Variables (X)**:
- Average waiting time
- Crowding level at stops
- Weather protection availability
- Accessibility features
- Information display quality

**Model**: Cumulative link model
```
logit(P(Y ≤ j)) = αⱼ - (β₁X₁ + β₂X₂ + ... + βₖXₖ)
```

### 4. **Advanced Regression Applications**

#### A. Multi-level Regression
**Levels**: 
- Individual passenger level
- Bus stop level  
- Route level
- Time period level

**Model**:
```
Waiting_Time_ijkl = β₀ + β₁(Individual_factors) + β₂(Stop_factors) + β₃(Route_factors) + β₄(Time_factors) + random_effects
```

#### B. Time Series Regression
**Dependent Variable (Y)**: Hourly passenger volume

**Independent Variables (X)**:
- Hour of day
- Day of week
- Season
- Weather
- Special events
- Historical trends

#### C. Spatial Regression
**Account for spatial correlation** between nearby bus stops:
- Distance-based weights
- Network connectivity
- Spillover effects from stop changes

---

## Data Collection Strategy for Regression Analysis

### 1. **Primary Data Sources**
- **Real-time API data**: KMB Open Data Platform
- **Passenger surveys**: Satisfaction, walking preferences, demographics
- **Field observations**: Actual waiting times, crowding levels
- **Infrastructure data**: GPS coordinates, berth configurations

### 2. **Key Variables to Collect**

#### Continuous Variables:
- Passenger waiting time (seconds)
- Bus queue time (seconds)
- Walking distance (meters)
- Passenger arrival rate (per hour)
- Bus frequency (per hour)
- Temperature, rainfall data

#### Categorical Variables:
- Time period (peak/off-peak)
- Day type (weekday/weekend)
- Weather condition (sunny/rainy/cloudy)
- Passenger demographics (age groups, mobility status)

#### Binary Variables:
- Merger implementation (yes/no)
- Service disruption (yes/no)
- Accessibility compliance (yes/no)

### 3. **Sample Size Considerations**
- **For linear regression**: Minimum 10-20 observations per predictor
- **For logistic regression**: Minimum 10 events per predictor
- **Target sample**: 500+ passenger observations, 100+ time periods

---

## Model Implementation Strategy

### Phase 1: Exploratory Analysis
1. **Correlation analysis** between key variables
2. **Descriptive statistics** for current vs. simulated scenarios
3. **Visualization** of relationships

### Phase 2: Model Development
1. **Simple linear regression** for each key relationship
2. **Multiple regression** with interaction terms
3. **Model validation** using cross-validation

### Phase 3: Prediction and Decision Support
1. **Scenario modeling** for different merger options
2. **Sensitivity analysis** for key parameters
3. **Confidence intervals** for predictions

---

## Expected Regression Results & Interpretations

### 1. **Linear Regression Findings**
- **Bus frequency coefficient**: -2.5 seconds per additional bus/hour
  - *Interpretation*: Each additional bus per hour reduces average waiting time by 2.5 seconds
- **Distance coefficient**: +0.8 seconds per meter
  - *Interpretation*: Each meter of additional walking distance increases total journey time by 0.8 seconds

### 2. **Logistic Regression Findings**
- **Distance odds ratio**: 0.85 (95% CI: 0.78-0.92)
  - *Interpretation*: For every 10m increase in stop distance, odds of successful merger decrease by 15%
- **Route overlap odds ratio**: 3.2 (95% CI: 2.1-4.8)
  - *Interpretation*: High route overlap (>70%) increases merger success odds by 220%

### 3. **Policy Recommendations Based on Regression**
- **Merge if**: Distance ≤ 30m AND Route overlap ≥ 75% AND Peak passenger volume > 600/hour
- **Keep separate if**: Significant accessibility concerns OR Distance > 50m
- **Monitor closely**: Border cases where model confidence intervals overlap

---

## Advantages of Regression Approach

### 1. **Complementary to Simulation**
- **Simulation**: Shows what happens under specific scenarios
- **Regression**: Identifies general relationships and patterns
- **Combined**: Provides both specific predictions and general principles

### 2. **Statistical Inference**
- **Confidence intervals** for effect sizes
- **Hypothesis testing** for significance
- **Model comparison** using statistical criteria

### 3. **Generalizability**
- **Broader applicability** beyond specific case study
- **Framework development** for other stop pairs
- **Policy guidelines** based on statistical evidence

### 4. **Stakeholder Communication**
- **Clear coefficients** easier to explain than simulation code
- **Probability estimates** for decision-making
- **Risk assessment** through confidence intervals

---

## Integration with Current Simulation Work

### 1. **Use Simulation Output as Regression Input**
- Run simulations across parameter ranges
- Use simulation results as dependent variables
- Develop meta-models using regression

### 2. **Validate Regression with Simulation**
- Compare regression predictions with simulation results
- Identify where simple linear relationships break down
- Refine models based on simulation insights

### 3. **Hybrid Approach**
- Use regression for initial screening
- Apply simulation for detailed analysis of promising scenarios
- Combine both in comprehensive decision framework

This regression-based approach will provide statistical rigor to complement the existing simulation work, enabling evidence-based decision-making for the bus stop merger question.
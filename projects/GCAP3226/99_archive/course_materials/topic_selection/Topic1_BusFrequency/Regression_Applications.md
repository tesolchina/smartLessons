# Regression Applications in Bus Frequency Optimization (Topic 1)

## Current Project Context

**Research Question**: How to optimize bus frequencies based on ridership data and passenger demand patterns?

**Case Study**: Route 56 (Tuen Mun to Sheung Shui) and Route 272A frequency optimization

**Current Approach**: Discrete-event simulation modeling bus utilization, passenger boarding/alighting, and wait times across different headway scenarios

---

## Regression Analysis Applications

### 1. **Linear Regression Models**

#### A. Passenger Wait Time Prediction
**Dependent Variable (Y)**: Average passenger waiting time (minutes)

**Independent Variables (X)**:
- Headway (minutes between buses)
- Passenger arrival rate (passengers/minute at each stop)
- Bus capacity utilization (%)
- Time of day (peak vs off-peak)
- Stop position on route (early vs late stops)
- Weather conditions
- Day of week (weekday vs weekend)

**Model**:
```
Wait_Time = β₀ + β₁(Headway) + β₂(Arrival_Rate) + β₃(Utilization) + β₄(Peak_Hour) + ε
```

**Expected Relationships**:
- Longer headway → Higher waiting time (positive coefficient)
- Higher arrival rate → Higher waiting time (positive coefficient)
- Peak hours → Higher waiting time (positive coefficient)

#### B. Bus Utilization Prediction
**Dependent Variable (Y)**: Bus capacity utilization (%)

**Independent Variables (X)**:
- Headway (minutes)
- Stop number along route
- Passenger boarding/alighting rates at each stop
- Route direction (forward/backward)
- Time since route start
- Historical demand patterns

**Model**:
```
Utilization = β₀ + β₁(Headway) + β₂(Stop_Number) + β₃(Boarding_Rate) + β₄(Direction) + ε
```

#### C. Optimal Frequency Determination
**Dependent Variable (Y)**: Total system cost (passenger time cost + operational cost)

**Independent Variables (X)**:
- Service frequency (buses per hour)
- Route length (km)
- Passenger demand (passengers per hour)
- Fuel cost per bus-km
- Driver wage per hour
- Vehicle depreciation cost

**Model**:
```
Total_Cost = β₀ + β₁(Frequency) + β₂(Route_Length) + β₃(Demand) + β₄(Operational_Costs) + ε
```

### 2. **Logistic Regression Models**

#### A. Service Quality Classification
**Dependent Variable (Y)**: Service quality (1 = Acceptable, 0 = Unacceptable)

**Independent Variables (X)**:
- Average waiting time (minutes)
- Maximum waiting time (minutes)
- Bus overcrowding incidents (% of trips over 80% capacity)
- Schedule reliability (% on-time arrivals)
- Passenger complaints per 1000 trips

**Model**:
```
P(Acceptable = 1) = 1 / (1 + e^-(β₀ + β₁(Avg_Wait) + β₂(Max_Wait) + β₃(Overcrowding) + β₄(Reliability)))
```

**Policy Application**: Determine minimum service standards for frequency decisions

#### B. Route Viability Assessment
**Dependent Variable (Y)**: Route sustainability (1 = Viable, 0 = Should be modified/cancelled)

**Independent Variables (X)**:
- Daily ridership numbers
- Cost recovery ratio (fare revenue / operational cost)
- Alternative transport availability
- Community access needs score
- Environmental impact metrics

### 3. **Ordinal Regression Models**

#### A. Passenger Satisfaction Rating
**Dependent Variable (Y)**: Satisfaction level (1 = Very Dissatisfied, 2 = Dissatisfied, 3 = Neutral, 4 = Satisfied, 5 = Very Satisfied)

**Independent Variables (X)**:
- Waiting time at stops
- In-vehicle travel time
- Service reliability
- Bus cleanliness and comfort
- Frequency adequacy

**Model**: Proportional odds model
```
logit(P(Y ≤ j)) = αⱼ - (β₁(Wait_Time) + β₂(Travel_Time) + β₃(Reliability) + β₄(Frequency))
```

### 4. **Time Series Regression**

#### A. Demand Forecasting
**Dependent Variable (Y)**: Hourly passenger boardings

**Independent Variables (X)**:
- Hour of day
- Day of week
- Month/season
- Weather conditions
- Special events
- Economic indicators
- Historical trends

**Model**: ARIMA with external regressors
```
Demand_t = α + β₁(Hour) + β₂(Weather_t) + β₃(Trend_t) + AR(p) + MA(q) + ε_t
```

#### B. Dynamic Frequency Optimization
**Dependent Variable (Y)**: Optimal headway (minutes)

**Independent Variables (X)**:
- Real-time passenger arrival rates
- Current bus locations and delays
- Predicted demand for next hour
- Traffic conditions
- Resource availability (buses, drivers)

### 5. **Multilevel/Hierarchical Regression**

#### A. Multi-Route Analysis
**Levels**:
- Route level (route characteristics)
- Stop level (stop-specific factors)
- Time period level (hour/day variations)
- Individual trip level

**Model**:
```
Wait_Time_ijkl = β₀ + β₁(Route_factors) + β₂(Stop_factors) + β₃(Time_factors) + u₀ⱼ + u₀ₖ + ε_ijkl
```

Where:
- i = individual passenger trip
- j = route
- k = stop
- l = time period

---

## Data Sources for Regression Analysis

### 1. **Simulation Output Data** (from existing `05_final_code.ipynb`)
- Bus utilization by stop and time
- Passenger waiting times
- Boarding/alighting patterns
- Queue lengths at stops

### 2. **Real-World Data Sources**
- **KMB API**: Real-time bus locations and ETAs
- **Transport Department**: Official ridership data, route planning documents
- **Octopus Card Data**: Passenger journey patterns
- **Weather Data**: HKO meteorological data
- **Traffic Data**: Real-time traffic conditions

### 3. **Survey Data** (to be collected)
- Passenger satisfaction surveys
- Willingness to pay for improved frequency
- Travel behavior preferences
- Demographic characteristics

---

## Integration with Simulation Approach

### 1. **Simulation as Data Generator**
- Run simulations across different parameter combinations
- Generate large dataset of scenarios for regression analysis
- Validate regression predictions against simulation results

### 2. **Regression-Informed Simulation**
- Use regression coefficients to set realistic parameter ranges
- Incorporate regression-predicted relationships in simulation logic
- Cross-validate both approaches

### 3. **Hybrid Decision Framework**
```
Step 1: Use regression for initial parameter estimation
Step 2: Apply simulation for detailed scenario analysis
Step 3: Validate with regression on simulation outputs
Step 4: Policy recommendation based on both approaches
```

---

## Policy Applications of Regression Results

### 1. **Route Planning Programme (RPP) Enhancement**
Based on consultation paper analysis, current RPP decisions could be enhanced with:

#### Quantitative Decision Rules:
```
IF: Predicted_Wait_Time > 15 minutes 
AND: Passenger_Demand > 100/hour
THEN: Increase frequency by 1 bus/hour
```

#### Cost-Benefit Thresholds:
```
Frequency_Change = f(Demand_Elasticity, Operating_Cost, Social_Benefit)
```

### 2. **Dynamic Frequency Adjustment**
Real-time regression models for:
- Peak hour frequency optimization
- Weather-based service adjustments
- Special event planning
- Emergency response protocols

### 3. **Performance Monitoring**
Regression-based KPIs:
- Service quality indices
- Efficiency metrics
- Passenger satisfaction predictors
- Cost effectiveness measures

---

## Expected Regression Findings

### 1. **Wait Time Model Results**
```
Wait_Time = 3.2 + 0.6(Headway) + 0.3(Peak_Hour) - 0.1(Bus_Capacity)
R² = 0.75, p < 0.001
```

**Interpretation**: 
- Each additional minute of headway increases waiting time by 0.6 minutes
- Peak hours add 0.3 minutes to average waiting time
- Larger bus capacity reduces waiting time

### 2. **Optimal Frequency Results**
```
Optimal_Frequency = 12.5 - 0.02(Cost_per_km) + 0.15(Demand_rate)
```

**Policy Implication**: 
- Base frequency of 12.5 buses/hour
- Adjust downward for high operational costs
- Adjust upward for high passenger demand

### 3. **Service Quality Thresholds**
```
P(Acceptable) = 95% when Wait_Time ≤ 8 minutes
P(Acceptable) = 50% when Wait_Time = 15 minutes
```

**Standard Setting**: Maximum acceptable headway = 16 minutes for 50% satisfaction

---

## Advantages of Regression Approach for Bus Frequency

### 1. **Complement to Simulation**
- **Simulation**: Shows detailed operational dynamics
- **Regression**: Identifies key relationships and thresholds
- **Combined**: Robust evidence base for policy decisions

### 2. **Real-Time Applications**
- Quick calculations for operational adjustments
- Simple formulas for route planners
- Automated decision support systems

### 3. **Policy Communication**
- Clear, interpretable coefficients
- Statistical significance testing
- Confidence intervals for risk assessment

### 4. **Scalability**
- Apply findings to other routes
- Develop system-wide optimization rules
- Create standardized planning procedures

This regression-based approach will provide the quantitative foundation needed to transform the current consultation-based RPP process into a more data-driven, evidence-based system for bus frequency optimization.
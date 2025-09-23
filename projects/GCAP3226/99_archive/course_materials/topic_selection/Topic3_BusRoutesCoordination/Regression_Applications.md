# Regression Applications in Bus Routes Coordination (Topic 3)

## Current Project Context

**Research Question**: How can two competing bus operators (272A-KMB and 582-CityBus) coordinate schedules for 8 overlapping stops to optimize passenger experience and operational efficiency?

**Current Approach**: Multi-API analysis using real-time data from both KMB and CityBus systems to understand current service patterns and identify coordination opportunities

---

## Regression Analysis Applications

### 1. **Linear Regression Models**

#### A. Passenger Waiting Time Optimization
**Dependent Variable (Y)**: Average passenger waiting time at overlapping stops (minutes)

**Independent Variables (X)**:
- Time gap between 272A and 582 services (minutes)
- Combined service frequency (buses per hour from both routes)
- Peak/off-peak indicator
- Stop sequence position on each route
- Passenger demand level at each stop
- Weather conditions
- Day of week

**Model**:
```
Wait_Time = β₀ + β₁(Service_Gap) + β₂(Combined_Frequency) + β₃(Peak_Hour) + β₄(Stop_Position) + ε
```

**Expected Relationships**:
- Larger service gaps → Higher waiting time (positive coefficient)
- Higher combined frequency → Lower waiting time (negative coefficient)
- Optimal gap likely around 50% of headway interval

#### B. Service Efficiency Prediction
**Dependent Variable (Y)**: Combined route efficiency score (passenger-km per bus-km)

**Independent Variables (X)**:
- Coordination level (% of synchronized departures)
- Load factor difference between routes
- Route overlap percentage
- Service frequency ratio (272A vs 582)
- Transfer passenger volume
- Operational cost ratio

**Model**:
```
Efficiency = β₀ + β₁(Coordination_Level) + β₂(Load_Balance) + β₃(Overlap_Rate) + β₄(Frequency_Ratio) + ε
```

#### C. Revenue Impact Analysis
**Dependent Variable (Y)**: Total fare revenue per hour for both operators

**Independent Variables (X)**:
- Service coordination level
- Passenger redistribution between routes
- Reduced waiting time (attracting new passengers)
- Operational cost savings
- Market share changes

**Model**:
```
Revenue = β₀ + β₁(Coordination) + β₂(Passenger_Shift) + β₃(New_Passengers) + β₄(Cost_Savings) + ε
```

### 2. **Logistic Regression Models**

#### A. Coordination Success Prediction
**Dependent Variable (Y)**: Successful coordination implementation (1 = Success, 0 = Failure)

**Independent Variables (X)**:
- Revenue sharing agreement fairness score
- Operational complexity level
- Regulatory support availability
- Passenger demand stability
- Technology infrastructure readiness
- Inter-company cooperation history

**Model**:
```
P(Success = 1) = 1 / (1 + e^-(β₀ + β₁(Revenue_Fairness) + β₂(Complexity) + β₃(Regulation) + β₄(Technology)))
```

**Policy Application**: Identify conditions for successful coordination initiatives

#### B. Passenger Route Choice Model
**Dependent Variable (Y)**: Route choice (1 = 272A, 0 = 582)

**Independent Variables (X)**:
- Waiting time difference
- In-vehicle time difference
- Fare difference
- Service reliability difference
- Bus comfort/quality difference
- Passenger demographics (age, income)

**Model**:
```
P(Choose_272A = 1) = 1 / (1 + e^-(β₀ + β₁(Wait_Diff) + β₂(Time_Diff) + β₃(Fare_Diff) + β₄(Reliability_Diff)))
```

### 3. **Ordinal Regression Models**

#### A. Coordination Benefit Rating
**Dependent Variable (Y)**: Coordination benefit level (1 = No benefit, 2 = Low, 3 = Medium, 4 = High, 5 = Very High)

**Independent Variables (X)**:
- Service frequency improvement
- Waiting time reduction
- Service reliability enhancement
- Cost savings percentage
- Passenger satisfaction increase

**Model**: Proportional odds model
```
logit(P(Y ≤ j)) = αⱼ - (β₁(Frequency_Gain) + β₂(Wait_Reduction) + β₃(Reliability) + β₄(Cost_Savings))
```

### 4. **Time Series Regression**

#### A. Dynamic Service Gap Analysis
**Dependent Variable (Y)**: Optimal service gap between routes (minutes)

**Independent Variables (X)**:
- Hour of day
- Day of week
- Real-time passenger demand
- Traffic conditions
- Weather factors
- Special events

**Model**: Dynamic regression with time-varying coefficients
```
Optimal_Gap_t = α + β₁(Hour_t) + β₂(Demand_t) + β₃(Traffic_t) + AR(1) + ε_t
```

#### B. Demand Forecasting for Coordination
**Dependent Variable (Y)**: Hourly passenger volume at overlapping stops

**Independent Variables (X)**:
- Historical demand patterns
- Coordination implementation effects
- External factors (weather, events)
- Service quality improvements
- Competitive responses

### 5. **Multilevel/Hierarchical Regression**

#### A. Multi-Stop Coordination Analysis
**Levels**:
- Stop level (stop-specific characteristics)
- Route level (272A vs 582 characteristics)
- Time level (hourly/daily variations)
- Coordination scenario level

**Model**:
```
Coordination_Benefit_ijkl = β₀ + β₁(Stop_factors) + β₂(Route_factors) + β₃(Time_factors) + 
                          β₄(Scenario_factors) + u₀ⱼ + u₀ₖ + ε_ijkl
```

Where:
- i = individual measurement
- j = stop
- k = route (272A/582)
- l = time period

---

## Data Sources for Regression Analysis

### 1. **Real-Time API Data** (from existing notebook analysis)
- **KMB API**: Route 272A real-time ETAs, stop information, service patterns
- **CityBus API**: Route 582 real-time ETAs, stop information, service patterns
- **Synchronized Data**: Combined service pattern analysis across both routes

### 2. **Operational Data**
- **Timetables**: Scheduled vs actual departure times
- **Ridership**: Passenger boarding/alighting at overlapping stops
- **Revenue**: Fare collection data from both operators
- **Costs**: Operational expenses per route-km

### 3. **Passenger Behavior Data**
- **Transfer Patterns**: Inter-route transfers at overlapping stops
- **Choice Behavior**: Passenger route selection factors
- **Satisfaction Surveys**: Service quality perceptions
- **Wait Time Observations**: Actual vs perceived waiting times

### 4. **External Factors**
- **Traffic Data**: Real-time traffic conditions affecting both routes
- **Weather Data**: Impact on passenger demand and service reliability
- **Events Data**: Special events affecting ridership patterns

---

## Coordination Scenarios for Regression Analysis

### 1. **Scenario A: Complementary Scheduling**
**Strategy**: Stagger departures to minimize combined waiting time

**Regression Questions**:
- What is the optimal time offset between routes?
- How does demand level affect optimal coordination?
- What are the revenue implications for each operator?

### 2. **Scenario B: Peak/Off-Peak Division**
**Strategy**: Different operators serve different time periods

**Regression Questions**:
- Which operator should serve which time periods?
- How does demand elasticity affect division strategy?
- What are the cost implications of reduced service hours?

### 3. **Scenario C: Stop-Specific Coordination**
**Strategy**: Coordinate only at high-traffic stops

**Regression Questions**:
- Which stops benefit most from coordination?
- What is the minimum demand threshold for coordination?
- How does stop location affect coordination benefits?

---

## Policy Applications of Regression Results

### 1. **Coordination Framework Development**
Based on regression analysis:

#### Quantitative Decision Rules:
```
IF: Combined_Frequency > 8 buses/hour 
AND: Service_Gap_Variance > 15 minutes
AND: Passenger_Demand > 200/hour/stop
THEN: Implement complementary scheduling
```

#### Revenue Sharing Formula:
```
Revenue_Share_A = Base_Share + β(Coordination_Benefit) + γ(Operational_Contribution)
```

### 2. **Dynamic Coordination Strategies**
Real-time regression models for:
- Service gap optimization based on demand
- Load balancing between routes
- Response to service disruptions
- Peak hour coordination enhancement

### 3. **Regulatory Framework**
Regression-informed policies:
- Coordination incentive structures
- Performance monitoring criteria
- Competition vs cooperation balance
- Consumer protection measures

---

## Expected Regression Findings

### 1. **Optimal Service Gap Results**
```
Optimal_Gap = 12.5 - 0.8(Peak_Hour) + 0.3(Passenger_Demand/100)
R² = 0.68, p < 0.001
```

**Interpretation**: 
- Base optimal gap of 12.5 minutes
- Reduce gap by 0.8 minutes during peak hours
- Increase gap slightly for very high demand

### 2. **Coordination Success Probability**
```
P(Success) = 0.85 when Revenue_Fairness ≥ 0.7 AND Technology_Ready = 1
P(Success) = 0.45 when Revenue_Fairness < 0.5 OR Technology_Ready = 0
```

**Policy Implication**: Focus on fair revenue sharing and technology infrastructure

### 3. **Passenger Benefits**
```
Wait_Time_Reduction = 3.2 + 0.6(Coordination_Level) - 0.4(Service_Reliability)
```

**Expected Outcome**: 60% coordination level reduces waiting time by ~4 minutes

### 4. **Revenue Impact**
```
Combined_Revenue = Base_Revenue × (1 + 0.12×Coordination_Level - 0.05×Implementation_Cost)
```

**Business Case**: 50% coordination increases combined revenue by ~6%

---

## Integration with Multi-API Approach

### 1. **Real-Time Data Enhancement**
- Use regression models to predict optimal coordination in real-time
- Incorporate API data into dynamic adjustment algorithms
- Validate regression predictions against actual performance

### 2. **Performance Monitoring**
- Regression-based KPIs for coordination success
- Automated alerts for suboptimal performance
- Continuous model updating with new data

### 3. **Decision Support System**
```
Algorithm: Real-Time Coordination Optimizer
1. Collect current API data (ETAs, passenger loads)
2. Apply regression models to predict optimal gaps
3. Calculate coordination benefits for each scenario
4. Recommend adjustments to both operators
5. Monitor results and update models
```

---

## Advantages of Regression Approach for Route Coordination

### 1. **Quantitative Cooperation Framework**
- Clear metrics for measuring coordination success
- Objective basis for revenue sharing negotiations
- Performance benchmarks for both operators

### 2. **Risk Assessment**
- Probability estimates for coordination success
- Sensitivity analysis for key variables
- Confidence intervals for expected benefits

### 3. **Scalability**
- Apply framework to other overlapping route pairs
- System-wide coordination optimization
- Inter-modal coordination (bus-rail, bus-metro)

### 4. **Real-Time Optimization**
- Dynamic adjustment based on current conditions
- Automated coordination recommendations
- Continuous improvement through learning algorithms

This regression-based approach will provide the analytical foundation needed to transform competitive bus route operations into coordinated services that benefit passengers, operators, and the overall transport system.
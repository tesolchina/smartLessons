# Case Study II: Evaluating the Efficiency of Bus Route Adjustments
## City Bus No. 56

**Course:** GCAP3226  
**Date:** 2025/09/23

---

## Table of Contents

1. [Background](#background)
2. [Simulation Design](#simulation-design)
3. [Random Components in the Simulation](#random-components-in-the-simulation)
4. [Results Interpretation](#results-interpretation)
5. [Recommendations](#recommendations)
6. [In-class Exercise](#in-class-exercise)

---

## Background

### Bus Route Planning Programme

The bus route planning programme involves systematic evaluation of passenger load factors to determine optimal service frequency.

### Criteria for Increasing Bus Frequency

> "For individual bus routes, if the passenger load factor reaches 90% during the busiest half-hour and 75% during the busiest hour of peak periods, or 60% during the busiest hour of off-peak periods, the department and the franchised bus company will consider increasing the service frequency."

### Research Questions

The passenger load factor of City Bus No. 56, as reported in the proposal, is 32% during the busiest hour (before adjustment). However, several questions remain unclear:

- **How is this passenger load factor defined?**
- **When does the busiest hour occur?**
- **Does the 32% represent an average across different stops and shifts?**
- **How is an increase in bus frequency justified given a passenger load factor of 32%?**

---

## Objectives

The study aims to:

1. **Develop and analyze a simulation** of Bus Route 56 operations during the morning using field data and estimated arrival times (ETA) from [data.gov.hk](https://data.gov.hk/en/)

2. **Assess the justification** for route and frequency adjustments to Bus No.56 by estimating the seat utilization rate via simulation

3. **Provide evidence-based policy recommendations**

---

## Simulation Design

### Key Processes

To calculate the seat utilization rate, we need to count the passengers on bus at each stop:

- The bus stops at every station
- The travel time between each pair of stops is random
- At each stop, the number of waiting passengers is random
- At each stop, the number of passengers getting off is random

### SimPy Implementation

The simulation follows this structure:

1. **Initialization:** Global variables are reset for each simulation run
2. **Environment Creation:** A new SimPy environment is created
3. **Process Scheduling:** Multiple bus processes are scheduled with different departure times
4. **Concurrent Execution:** All bus processes run concurrently, each following their route
5. **Event-Driven Progression:** Each bus process yields control during travel times, allowing other buses to operate
6. **Data Collection:** Each process records utilization data as it progresses
7. **Simulation End:** Runs until all buses complete their journeys

---

## Random Components in the Simulation

### 1. Travel Time

- **Model:** Normal distribution
- **Parameters:** Mean and standard deviation estimated from sample data
- **Data Source:** ETA collected from API for 30 trips of Bus No. 56
- **Process:** Calculate mean and standard deviation of travel times between each pair of stops, then sample from corresponding normal distributions

### 2. Number of Waiting Passengers

- **Model:** Poisson distribution
- **Parameter:** λ (lambda) - the average number of occurrences in the time interval
- **Estimation:** Field observation data

### 3. Number of Passengers Getting Off

- **Model:** Binomial distribution
- **Application:** Models the probability of passengers alighting at each stop

---

## Results Interpretation

### Existing Route - Forward Direction (After Adjustment)

**Simulation runs:** 1,000
- **Median seat utilization:** 12% - 34%

### Existing Route - Return Direction (After Adjustment)

**Simulation runs:** 1,000
- **Median seat utilization:** 5% - 34%

### Forward Direction (Before Adjustment)

**Simulation runs:** 1,000
- **Median seat utilization:** 18% - 56%
- Based on estimated passenger flow at the removed bus stops

### Return Direction (Before Adjustment)

**Simulation runs:** 1,000
- **Median seat utilization:** 8% - 58%

### Summary of Results

- **Key Finding:** The adjustment appears to have **reduced overall seat utilization rate**
- **Implication:** The decision to increase bus frequency should also be analyzed from the perspective of operating costs

---

## Recommendations

### Enquiry to Department of Transportation

The following questions should be addressed to the Department of Transportation:

#### 1. Operational and Passenger Flow Data
What types of operational and passenger flow data (e.g., stop-level boarding and alighting, peak/off-peak passenger counts) were collected and analyzed when assessing the rerouting and schedule changes for Routes 56 and 56A?

#### 2. Service Quality Evaluation
What quantitative models or criteria (such as load factor thresholds, predicted waiting times, or cost-benefit analyses) were used to evaluate whether the service modifications would maintain or improve passenger service quality?

#### 3. Data Accessibility
Are the relevant operational datasets, consultation summaries, or evaluation models available for public or academic review? If so, how can these be accessed? If not, would the Transport Department consider releasing anonymized or summarized data in accordance with the Code on Access to Information?

---

## In-class Exercise

[*Exercise details to be provided during class*]

---

## Data Sources

- **Primary Data:** Field observations and ETA data from [data.gov.hk](https://data.gov.hk/en/)
- **Simulation Platform:** SimPy (Discrete Event Simulation)
- **Sample Size:** 30 trips for travel time estimation, 1,000 simulation runs for analysis

---

*This document was converted from the original PDF presentation and cleaned up for better readability and structure.*
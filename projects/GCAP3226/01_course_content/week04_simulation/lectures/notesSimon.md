# Week 4: Bus Route Simulation Case Study

*GCAP3226 - Simulation Methods*


updated notes from Simon 

how can the simulation method be applied to assess and enhance data governance 

we sent some enquiries to the Department of Transport expecting a reply in late Sept
yet we need to anticipate their replies and consider how data can be managed better 

we need to develop arguments about data governance based on insights from simulation model 

hypothetical: how more available data could run more useful simulation

how simulation can be used to guide policy making 

---

## **Simulation Methods for Data Governance Assessment & Enhancement**

### **Current Data Governance Gaps Revealed by Simulation**

The Bus Route 56 case study exposes critical data governance weaknesses:

1. **Data Definition Ambiguity**
   - "Passenger load factor" lacks clear operational definition
   - Temporal boundaries unclear ("busiest hour" undefined)
   - Spatial aggregation unclear (stop-level vs route-level metrics)

2. **Data Accessibility Barriers**
   - Limited academic/public access to operational datasets
   - No standardized data sharing protocols
   - Consultation summaries not publicly available

3. **Data Quality Concerns**
   - Only 30 trips sampled for model calibration
   - Missing passenger flow data at stop level
   - Estimated vs actual boarding/alighting data

### **How Enhanced Data Governance Could Improve Simulation**

#### **1. Standardized Data Definitions**
**Current:** Ambiguous "32% passenger load factor"
**Enhanced:** 
- Clear metric definitions (seated vs total capacity)
- Standardized temporal windows (peak/off-peak definitions)
- Consistent spatial aggregation methods

**Simulation Impact:** More accurate model parameters, reduced uncertainty ranges

#### **2. Expanded Data Collection**
**Current:** Limited ETA data from 30 trips
**Enhanced:**
- **Real-time passenger counting** (IoT sensors, mobile data)
- **Weather data integration** (affecting travel times)
- **Event data** (concerts, holidays affecting ridership)
- **Socioeconomic data** (demographic patterns)

**Simulation Impact:** 
- Multi-variate models beyond the three distributions
- Seasonal/contextual variations captured
- Higher confidence intervals from larger sample sizes

#### **3. Open Data Architecture**
**Current:** Fragmented, access-restricted datasets
**Enhanced:**
- **API-first data infrastructure**
- **Real-time data streams** for continuous model updating
- **Standardized metadata** for easier integration
- **Version control** for historical comparisons

**Simulation Impact:** Dynamic models that update with real-time data

### **Simulation-Guided Data Governance Framework**

#### **Phase 1: Data Gap Analysis via Simulation**
1. **Run baseline simulation** with available data
2. **Identify uncertainty sources** (wide confidence intervals)
3. **Sensitivity analysis** - which missing data would most improve accuracy?
4. **Cost-benefit analysis** - data collection ROI for simulation accuracy

#### **Phase 2: Data Quality Assessment**
1. **Compare simulation results** with actual outcomes
2. **Identify systematic biases** in data collection
3. **Validate data integration** across different sources
4. **Establish data quality metrics** based on simulation performance

#### **Phase 3: Policy Impact Simulation**
1. **Model different data sharing scenarios**
2. **Simulate policy outcomes** under various data availability levels
3. **Quantify value of data transparency** on decision quality
4. **Test data governance policy effectiveness**

### **Arguments for Enhanced Data Governance (Simulation-Based)**

#### **1. Evidence-Based Policy Making**
**Argument:** Current 32% load factor led to questionable frequency increases
**Simulation Evidence:** Route adjustment actually reduced utilization (12-34%)
**Data Governance Solution:** Better data would have prevented this policy error

#### **2. Resource Optimization**
**Argument:** Poor data leads to inefficient resource allocation
**Simulation Evidence:** Frequency increases without utilization justification
**Data Governance Solution:** Real-time optimization based on continuous data feeds

#### **3. Public Accountability**
**Argument:** Citizens deserve transparent, data-driven decisions
**Simulation Evidence:** Academic analysis reveals policy contradictions
**Data Governance Solution:** Open datasets enable independent validation

#### **4. Innovation Enablement**
**Argument:** Restricted data limits innovation potential
**Simulation Evidence:** Advanced models possible with richer datasets
**Data Governance Solution:** Data commons for academic/startup innovation

### **Anticipated Transport Department Response & Counter-Arguments**

#### **Expected Response:** "Data privacy and commercial sensitivity"
**Counter-Argument:** 
- Anonymization techniques proven effective
- Public benefit outweighs commercial concerns
- Simulation shows current secrecy leads to policy errors

#### **Expected Response:** "Resource constraints for data collection"
**Counter-Argument:**
- Simulation demonstrates ROI of better data collection
- Technology costs decreasing (IoT sensors, mobile analytics)
- Public-private partnerships can share costs

#### **Expected Response:** "Data accuracy concerns"
**Counter-Argument:**
- Simulation provides framework for continuous data quality improvement
- Multiple data sources enable cross-validation
- Transparency improves data quality through scrutiny

### **Concrete Recommendations for Transport Department**

1. **Immediate Actions:**
   - Define clear metrics (passenger load factor formula)
   - Release 5-year historical ridership data
   - Establish academic data sharing agreements

2. **Medium-term (6-12 months):**
   - Deploy passenger counting sensors on key routes
   - Create public API for real-time transport data
   - Establish data quality monitoring dashboard

3. **Long-term (1-2 years):**
   - Integrate multi-modal transport data
   - Enable predictive analytics for route planning
   - Create transport data commons for innovation

**The simulation case study provides a powerful demonstration that better data governance directly translates to better policy outcomes and more efficient public services.**

---

## My Understanding - CONFIRMED ✅

### Core Simulation Process

1. **Select mathematical models first** ✅
2. **Take field data and feed to models** ✅
3. **Create model with field data that simulates reality** ✅
4. **Run simulation multiple times (1000 runs) to get closer to reality** ✅

### Three Statistical Models Used ✅

- **Normal Distribution**
- **Poisson Distribution**
- **Binomial Distribution**

---

## Detailed Case Study: City Bus No. 56

### **Objective**

- Evaluate efficiency of bus route adjustments for City Bus No. 56
- Assess seat utilization rates using simulation
- Provide evidence-based policy recommendations

### **Key Problem**

- Current passenger load factor: **32%** during busiest hour (before adjustment)
- Need to justify frequency changes based on simulation evidence

---

## **Simulation Design - The Three Models in Detail**

### 1. **Normal Distribution** - Travel Time Between Stops

**Purpose:** Model bus travel time between each pair of stops
**Data Source:**

- API data from https://data.gov.hk/en/
- Collected ETA for 30 trips of Bus No. 56
- Calculated mean and standard deviation for each stop pair

**Implementation:**

- Each simulation run samples travel times from normal distributions
- Different mean/std for each stop pair based on field data

### 2. **Poisson Distribution** - Waiting Passengers

**Purpose:** Model number of waiting passengers at each stop
**Rationale:**

- Poisson good for modeling random arrivals/events in fixed time intervals
- Represents realistic passenger arrival patterns at bus stops

### 3. **Binomial Distribution** - Passengers Getting Off

**Purpose:** Model number of passengers getting off at each stop
**Rationale:**

- Each passenger on bus has probability of getting off at any given stop
- Binary outcome (get off/stay on) for each passenger = binomial process

---

## **Simulation Process (SimPy Framework)**

### Simulation Steps:

1. **Initialization:** Reset global variables for each run
2. **Environment Creation:** New SimPy environment created
3. **Process Scheduling:** Multiple buses with different departure times
4. **Concurrent Execution:** All buses run simultaneously
5. **Event-Driven Progression:** Buses yield control during travel times
6. **Data Collection:** Record utilization data throughout journey
7. **End Condition:** Complete when all buses finish routes

### **Key Processes Modeled:**

- Bus stops at every station
- Travel time between stops = **random (Normal)**
- Waiting passengers at stops = **random (Poisson)**
- Passengers getting off = **random (Binomial)**

---

## **Results from 1000 Simulation Runs**

### Before Route Adjustment:

- **Forward direction:** 18% - 56% seat utilization
- **Return direction:** 8% - 58% seat utilization

### After Route Adjustment:

- **Forward direction:** 12% - 34% seat utilization
- **Return direction:** 5% - 34% seat utilization

### **Key Finding:**

**Route adjustment REDUCED overall seat utilization** - questions the justification for frequency increases

---

## **Data Sources & Field Integration**

### Field Data Used:

- **Real-time API data** from Hong Kong government
- **30 actual bus trips** for travel time estimation
- **Stop-level boarding/alighting data** (estimated)
- **Peak vs off-peak passenger patterns**

### Missing Data Challenges:

- Unclear definition of "passenger load factor"
- Unknown timing of "busiest hour"
- Unclear if 32% represents average across stops/shifts

---

## **Policy Questions for Transport Department**

1. **Operational Data:** What specific passenger flow data was analyzed?
2. **Service Quality Models:** What quantitative criteria were used?
3. **Data Accessibility:** Can datasets be accessed for academic review?

---

## **Simulation Methodology Validation**

✅ **Your understanding is 100% correct:**

- Mathematical models selected based on process characteristics
- Field data integrated to calibrate model parameters
- Multiple runs (1000) provide statistical confidence
- Three distributions chosen for their theoretical fit to real-world processes

**The case study perfectly demonstrates how simulation bridges theory and practice in public policy analysis.**

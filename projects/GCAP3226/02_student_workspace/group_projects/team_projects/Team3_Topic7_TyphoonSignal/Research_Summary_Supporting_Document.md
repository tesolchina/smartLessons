# Research Summary: Signal No. 8 Data Analysis (September 8-9, 2025)

## Executive Summary
Academic research team at HKBU developed real-time wind monitoring system to study typhoon signal accuracy. Analysis of September 8-9, 2025 Signal No. 8 event revealed discrepancies between publicly available wind data and signal criteria decisions.

## Key Findings

### 1. Signal Maintenance Decision
- **Unusual Practice**: Early announcement of Signal No. 8 maintenance until 11:00 AM on September 9, 2025
- **Research Concern**: Earlier than usual commitment to specific signal duration
- **Impact**: Affected public planning and business operations

### 2. Wind Data Analysis
- **Monitoring Scope**: 30 weather stations via HKO public APIs
- **Observation Period**: Continuous 10-minute intervals during Signal No. 8 event
- **Key Finding**: Wind measurements frequently did not meet official Signal No. 8 criteria
- **Criteria**: Signal No. 8 requires ≥50% of reference stations recording sustained winds of 63-117 km/h

### 3. Data Sources Used
**Working HKO APIs:**
- `https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en`
- `https://portal.csdi.gov.hk/server/services/common/hko_rcd_1634953844424_88011/MapServer/WFSServer`
- RSS feeds: CurrentWeather.xml and WeatherWarningBulletin.xml

### 4. Technical Implementation
- **Real-time Dashboard**: Live monitoring of all 30 stations
- **Signal Calculation**: Automated assessment based on published HKO criteria
- **Data Logging**: CSV archives for historical analysis
- **Comparison Tool**: Official signal vs. calculated signal analysis

## Research Questions Requiring Official Data Verification

1. **Wind Threshold Compliance**: How many reference stations actually met Signal No. 8 criteria during the event?

2. **Decision Timing**: What meteorological factors justified the early maintenance announcement?

3. **Reference Station Performance**: Were all 8 reference anemometers operational and providing accurate data?

4. **Forecast Accuracy**: How did actual conditions compare to the models used for signal decisions?

## Academic Significance

### Public Interest Value
- **Transparency**: Public understanding of signal decision-making
- **Safety**: Accuracy of public warning systems
- **Research**: Contributing to meteorological science
- **Policy**: Evidence-based improvements to warning systems

### Methodology Transparency
- Open-source monitoring system
- Publicly available data sources
- Reproducible analysis methods
- Academic peer review process

## Data Request Justification

### Code on Access to Information Compliance
- **Academic Purpose**: Legitimate research at recognized institution
- **Public Interest**: Transparency in public safety decisions
- **Scientific Merit**: Contributing to meteorological research
- **Responsible Use**: Proper attribution and academic standards

### Specific Data Needs
1. **Verification Data**: Official measurements to validate our findings
2. **Decision Context**: Understanding the meteorological reasoning
3. **System Performance**: Reference station operational status
4. **Communication Timeline**: Official announcement decision points

## Research Team Credentials

**Principal Investigator**: Dr. Simon Wang, HKBU Language Centre
**Institution**: Hong Kong Baptist University
**Project**: GCAP3226 Public Policy Analysis
**Email**: simonwang@hkbu.edu.hk

## Commitment to Responsible Research

- Proper attribution of all HKO data and expertise
- Academic publication with peer review
- Public education and transparency
- Evidence-based recommendations for system improvements

---

*This research summary supports our formal request for information under the Code on Access to Information Ordinance, demonstrating the academic merit and public interest value of our typhoon signal accuracy study.*
# Datasets and Topics to Explore

This note lists candidate topics and high-potential datasets from data.gov.hk for GCAP3226.

Tip: prefer CSV/JSON resources and datasets with API access for easier analysis.

## Selected focus areas (semester plan)

The following three topics are selected for hands-on work, aligned to CILOs and suitable for regression/simulation:

1) Transport — Journey time / Speed Map (Transport Department)
- Data plan: journey time by corridor or speed map data (CSV/JSON/API)
- Starter questions: peak vs. off-peak journey times; congestion hotspots by corridor/district
- Regression target: journey_time; Features: hour_of_day, day_of_week, route_id/corridor, incident_flag (if joined), weather (optional)
- Repo path: `course_materials/resources/datasets/open_data/transport/`

2) Air Quality — AQHI / PM2.5 by station (EPD)
- Data plan: AQHI station/hourly readings, or PM2.5 concentration (CSV/JSON/API)
- Starter questions: daily/seasonal patterns across stations; forecasting next-hour AQHI/PM2.5
- Regression target: pm25 or aqhi; Features: station, hour, lags (t-1, t-2), basic weather joins (optional)
- Repo path: `course_materials/resources/datasets/open_data/air_quality/`

3) Housing — Public housing waiting time / supply (HA)
- Data plan: waiting time by application year/district; completions/supply indicators (CSV/XLSX)
- Starter questions: trend and district disparities; factors associated with waiting time
- Regression target: waiting_time_months; Features: district, year, family_size (if available)
- Repo path: `course_materials/resources/datasets/open_data/housing/`

Notes
- We’ll prefer CSV/JSON resources; API endpoints will be used where stable and well-documented.
- Scripts: `scripts/fetch_selected_open_data.py` (fetches curated datasets), `scripts/regression_sim_templates.py` (OLS/GLM + simple simulation).
- If a resource isn’t present locally, the templates will print a helpful path + tip to download/fetch.

## CILO-aligned topic ideas (draft)

These topic clusters align with the course’s intended learning outcomes (CILOs) inferred from the syllabus analysis: data access, analysis/visualization, and policy interpretation/recommendations.

- CILO A — Access and curate HK open data
  - Air Quality Health Index (AQHI) by station and time — EPD
    - Example: AQHI station readings (CSV/API)
    - Skills: API/CSV ingestion, time-indexing, station metadata join
  - Traffic speed/journey time — Transport Department
    - Example: Speed Map/journey time (CSV/API)
    - Skills: joining location metadata, time series resampling
  - Recycling facilities locations — EPD/FEHD/LCSD
    - Example: Recycling bin locations (CSV/JSON)
    - Skills: geospatial basics, deduplication, address cleaning

- CILO B — Analyze patterns and produce evidence
  - Housing: Public housing supply, waiting list time — Housing Authority
    - Data: Waiting time series, completions by year/district (CSV)
    - Analyses: trends, district disparities, correlation with demographics
  - Health: Vaccination uptake by age group (COVID-19) — Health Bureau
    - Data: vaccination-rates-over-time-by-age.csv
    - Analyses: temporal trends, cohort comparison, rolling averages
  - Water quality (drinking/beach) — WSD/EPD
    - Data: District monitoring statistics, beach grades (CSV)
    - Analyses: seasonal patterns, hotspots, threshold exceedance

- CILO C — Communicate policy insights with visuals
  - District comparisons (per-capita) — C&SD + topical datasets
    - Charts: bar/line/small multiples; map (optional)
    - Deliverable: one-page policy brief visuals
  - Provider ecosystem overview — data.gov.hk catalog analytics
    - Data: formats_counts, api_access_counts, top_providers (generated)
    - Charts: top providers, API adoption, format composition

- CILO D — Formulate recommendations grounded in evidence
  - Transport reliability: journey time variability hotspots — TD
  - Waste & recycling: facility coverage vs. population density — EPD/FEHD
  - Health readiness: vaccination uptake gaps by age/district — Health Bureau

Notes
- Prefer CSV/JSON resources and API-enabled endpoints when possible.
- Keep a small “starter pack” for Week 2 using static CSVs; add API datasets later.
- For geospatial, stick to points (facilities) or districts to keep complexity manageable.

## Topic overview

- Health: 1 candidate datasets
- Population District: 1 candidate datasets
- Water Quality: 1 candidate datasets

## Health

- Daily count of vaccination by age groups — Health Bureau
  - Resource: https://www.healthbureau.gov.hk/download/opendata/COVID19/vaccination-rates-over-time-by-age.csv
  - Formats: CSV, CSV
  - API: False

## Population District

- Annual Statistic of Enhanced Water Monitoring Programme for 18 Districts — Water Supplies Department
  - Resource: https://www.wsd.gov.hk/datagovhk/tc-data/18_dcd_annual_statistics_dec2017-dec2018_tc.csv
  - Formats: CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX
  - API: False

## Water Quality

- Water Quality Control — Water Supplies Department
  - Resource: https://www.wsd.gov.hk/datagovhk/tc-data/water-quality-control-2017-2018-c.csv
  - Formats: CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX, CSV, CSV, XLSX, XLSX
  - API: False

---

Appendix: Where we’ll place prepared datasets
- Folder: `course_materials/resources/datasets/open_data/`
- Contents (proposal):
  - air_quality/aqhi_by_station.csv (or API fetch script)
  - transport/traffic_journey_time.csv (or API fetch script)
  - recycling/recycling_bins.csv
  - housing/housing_waitlist.csv
  - water/water_quality_district.csv

If you confirm 3–4 focus areas (e.g., Air Quality, Transport, Recycling, Housing), I’ll fetch and stage the data and add starter analysis cells.


# Regression & Simulation Dataset Shortlist (CILO-aligned)

This guide proposes datasets suitable for regression analysis and simple simulations, aligned with GCAP 3226 CILOs.

Principles
- Prefer CSV/JSON with clear targets and features
- Start with OLS-ready tabular data; add time series or panel extensions later
- Keep data documentation links with each dataset

## CILO A — Access & Curate
- Transport: Journey time vs. time-of-day / incidents (TD)
  - Target: journey_time
  - Features: hour_of_day, day_of_week, route_id, weather (if joined)
  - Notes: API/CSV available; aggregation to 5–15 min bins
- Air Quality (EPD AQHI/PM2.5): pollutant concentration forecasting
  - Target: PM2.5 (or AQHI)
  - Features: hour, station, temp/humidity (if joined), lags (t-1, t-2)
- Housing: Waiting time vs. application year/district (HA)
  - Target: waiting_time_months
  - Features: district, year, family_size

## CILO B — Analyze & Model
- Health: Vaccination uptake by age group (HB)
  - Target: uptake_rate (or daily_delta)
  - Features: age_group, day, policy_phase (encoded)
  - Model: OLS / GLS; consider AR terms
- Water: District water quality indicators (WSD/EPD)
  - Target: ecoli_count or compliance_rate
  - Features: district, month, temp (if joined)
  - Model: Log-linear or Poisson/Negative Binomial if counts
- Traffic incidents vs. weather/time (TD + HKO)
  - Target: incidents_per_hour
  - Features: precipitation, visibility, hour, district
  - Model: Poisson/Quasi-Poisson

## CILO C — Communicate Insights
- Visualize coefficient effects with CI bands
- Show “what-if” scenario plots from simulations
- Provide district dashboards for policy brief

## CILO D — Recommendations
- Scenario-based recommendations based on model elasticities (e.g., impact of added recycling points on contamination rate; expected wait time changes)

---

## Candidate datasets (to fetch or already present)
- Health Bureau — vaccination-rates-over-time-by-age.csv (present)
- WSD — water-quality-control-2017-2018-c.csv (present)
- TD — journey time/traffic speed (to fetch)
- EPD — AQHI station/hourly (to fetch)
- HA — housing waitlist by time (to fetch)

A small staging plan lives in `_open_data_inventory/dataset_candidates_regression.csv`.

# Explore and Visualize Data for the Geo Project (Planning Note)

Student: Donald (15, international school, IGCSE Geography)
Folder: `projects/Donald/Geo`
Data:
- `projects/Donald/Geo/data/YR 10 DATA(GROUP 3).csv`
- `projects/Donald/Geo/data/YR 10 DATA.xlsx` (additional sheets/fields likely)

Purpose: Outline possible visualizations and analyses we can produce from the provided dataset before writing any code.

## Dataset snapshot (interpreted)
- Three field sites: SITE 1, SITE 2, SITE 3 (from CSV) — Excel file may include more sites/rows
- Variables captured per site:
  - EQS (Environmental Quality Score) e.g., `2+`, `3+`, `1+` (categorical/ordinal)
  - Building height (meters)
  - Decibels (noise level)
- Traffic count (broken down by vehicle type: Car, Taxi, Truck, Motorbike, Van)
  - Pedestrian count
  - All traffic options (transport accessibility notes)
  - Land use (e.g., commercial, dining, transit)
- Order (High/Low order — likely settlement hierarchy/centrality)
- Excel may add: timestamps, coordinates, surveyor IDs, more categories (to confirm when parsing)

## Immediate cleaning/structuring needs (no code yet)
- Normalize "EQS" to numeric (e.g., `2+ -> 2`, `3+ -> 3`, `1+ -> 1`).
- Parse the multi-line "TRAFFIC COUNT" cells into structured counts per vehicle type per site.
- Standardize category labels (e.g., `commerical` -> `commercial`).
- Confirm units for building height.
- Treat "All traffic options" as categorical text (may extract indicators: has MTR, has bus, etc.).
- If Excel contains multiple sheets: consolidate to a tidy table with columns: site, distance_from_harbour (if present), eqs_num, decibels, building_height_m, ped_count, traffic_car/taxi/truck/motorbike/van, land_use, order, access_bus, access_mtr.
- If coordinates exist in Excel: derive site distance from Victoria Harbour (straight-line) for hypothesis testing.

## Candidate visualizations (guided by Donald's draft and teacher guide)
1) Site comparison dashboard (bar charts)
   - Building height by site
   - Average noise (decibels) by site
   - Pedestrian count by site
   - Stacked bar: Traffic composition (Car/Taxi/Truck/Motorbike/Van) by site
   - Annotate each panel with "High/Low Order" and Land Use

2) Relationship plots (scatter/line) — aligned to hypotheses
   - Noise vs. traffic volume (sum of all vehicles) — per site
   - Noise vs. distance from Victoria Harbour (if distance available in Excel) — Donald's draft hypothesis
   - EQS vs. distance from CBD/Harbour (numeric EQS) — Donald's draft hypothesis
   - Pedestrian count vs. transit accessibility indicator (e.g., bus present yes/no, MTR yes/no)
   - Building height vs. EQS (after converting EQS to numeric)

3) Categorical summaries (tables/heatmaps)
   - Land use distribution across sites
   - “High or Low Order?” as a label on comparison charts
   - Transport accessibility summary table (presence of bus/MTR; notes from "All traffic options")

4) Communication-friendly visuals
   - Simple infographic-style comparison (topline metrics per site)
   - Traffic composition pie charts per site (for presentation; stacked bars better for comparison)
   - A small map inset (if coordinates added from Excel/Google Maps) showing sites relative to Victoria Harbour

## Analytical angles (IGCSE-friendly)
- Urban morphology: How building height and land use vary across the three sites.
- Environmental quality: How EQS relates to noise, traffic, and pedestrian counts.
- Accessibility and centrality: Whether sites with richer transport options correlate with higher pedestrian counts and/or higher EQS.
- Settlement hierarchy: Use “High or Low Order?” as contextual annotation on charts.
 - Distance decay: Evaluate whether noise and/or EQS show decay with distance from Victoria Harbour (per Donald's research question).

## Output plan
- One-page chart pack (3–5 visuals) focusing on: noise, pedestrian flow, traffic composition, and EQS/building height.
- Brief narrative (2–3 paragraphs) interpreting the findings and limitations.
 - Align presentation to guide (HowtoA.md): For each hypothesis include: chart → describe → explain → anomalies → link to theory.

## Current status and concrete next visuals
- Cleaned data available:
   - `cleaned/cleaned_wide.csv` with columns: group, site, distance_m, decibels_db, eqs, pedestrian_count, traffic_total, building_height_m
   - `cleaned/cleaned_long.csv` for flexible reshaping
- Initial figures generated (to be refined with labels/annotations):
   - `figures/noise_vs_distance.png` — Noise (dB) vs Distance (m) with trendline
   - `figures/eqs_vs_distance.png` — EQS vs Distance (m) with trendline
- Next 2–3 visuals to add (aligned to draft and HowtoA.md):
   - Stacked bar: Traffic composition by site (if per-vehicle data becomes available; otherwise total traffic bar by site)
   - Bar chart: Pedestrian count by site with High/Low Order annotation
   - Scatter: Building height (m) vs EQS (numeric), optional linear fit

## Next steps (when we write code)
- Load CSV, tidy mixed-format fields (traffic counts, EQS, spelling corrections).
- Compute derived metrics: total traffic per site, proportions by vehicle type, numeric EQS.
- Create selected charts with clear titles and axis labels suitable for IGCSE submission.
- Export charts as PNG and a short report (Markdown or PDF).
 - If Excel adds more sites/columns: integrate into the same pipeline; optionally calculate straight-line distance from harbour using coordinates.
 - Prepare figure numbering, titles, captions, and references per guide (scale/north arrow for maps if used).

Notes:
- If more sites/datasets are available, the same structure scales easily.
- If coordinates exist, a simple map or choropleth could be considered later.

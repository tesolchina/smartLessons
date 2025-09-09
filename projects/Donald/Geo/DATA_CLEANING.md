# Data Cleaning: YR 10 DATA.xlsx (Donald’s Geo Project)

This note explains exactly how we turned the raw Excel into tidy tables you can graph.

## Files
- Input: `data/YR 10 DATA.xlsx` (GROUP 1–13 sheets + `Distance Data`)
- Outputs (auto-created in `cleaned/`):
  - `cleaned_long.csv` — one row per (group, site, variable)
  - `cleaned_wide.csv` — one row per (group, site) with numeric columns ready for charts

## What we fixed
- Headers: Some sheets didn’t have proper headers. We auto-detected the row with `SITE 1`, `SITE 2`, `SITE 3` and used that to orient the table.
- Variable names:
  - `EQS` → numeric (removed `+` signs and converted to numbers; negatives kept as-is)
  - `BULDING HEIGHT` typo normalized → `building_height_m`
  - `DECIBELS` values like `71.6dBa` → numeric `71.6` and unit `dB`
  - `TRAFFIC COUNT` free text like `24 in 2 minutes` → numeric `24` and unit `count_2min`
  - `PEDESTRIAN COUNT` → numeric
- Distance: From `Distance Data` sheet, strings like `303m` → numeric meters; joined by (Group, Site).
- Stories to meters: If a height said “Avg 7 stories”, we estimated meters using 3m per story (documented assumption).

## Columns in outputs
- `cleaned_long.csv`
  - `group`, `site`, `variable`, `value_raw`, plus normalized fields: `norm_variable`, `value_num`, `unit`
- `cleaned_wide.csv`
  - `group`, `site`, numeric columns:
    - `eqs`
    - `building_height_m` (meters; stories converted at 3m/story if needed)
    - `decibels_db`
    - `traffic_total` (in 2 minutes where present)
    - `pedestrian_count`
    - `distance_m` (from Victoria Harbour)

## How to use this
- For hypothesis charts:
  - Noise vs Distance → use `decibels_db` vs `distance_m`
  - EQS vs Distance → use `eqs` vs `distance_m`
  - Transport Accessibility → use `traffic_total` and/or `pedestrian_count` by site; annotate with Land Use if needed (currently text in long format)
- If you need a variable that’s only in text (e.g., Land Use), pull it from `cleaned_long.csv` where `norm_variable` might be `land_use`.

## Limitations
- Some groups had missing/irregular entries; where numeric parsing failed, cells are blank (NaN).
- Traffic detail by vehicle type isn’t present in Excel (only totals in some cases). If you want composition (car/taxi/etc.), we can supplement from the CSV or recode manually.
- Distance sheet currently shows entries for some sites; missing ones remain blank.

## Re-running
You can re-run the cleaning anytime:

```bash
python3 projects/Donald/Geo/clean_data.py
```

This will regenerate the two CSVs in `projects/Donald/Geo/cleaned/`.

## Next
- Create charts aligned with your hypotheses using `cleaned_wide.csv`.
- If you want maps, we can add coordinates and compute exact distances.

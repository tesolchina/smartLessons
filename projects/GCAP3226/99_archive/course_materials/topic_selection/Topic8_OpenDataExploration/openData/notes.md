https://data.gov.hk/en/

let's write a web crawler to take a preliminary sweep to see what data is available with API access 

we focus on meta data at this stage

---

Crawler notes (2025-09-13)

- Added `crawl_data_gov_hk.py` that uses the Data.gov.hk CKAN API to fetch dataset metadata.
- Outputs JSON (full records) and CSV (flattened) under `openData/out/` by default.
- Flags `api_access` when a resource is CKAN Datastore backed or its URL contains `/api/`.

Quick run examples:

1) Fetch 50 datasets (default page size 100):

	- From repo root, run: `python openData/crawl_data_gov_hk.py --limit 50`

2) Query by keyword and save only CSV:

	- `python openData/crawl_data_gov_hk.py --limit 200 --q traffic --no-json`

3) Filter by organization (CKAN org slug):

	- `python openData/crawl_data_gov_hk.py --organization environmental-protection-department --limit 100`

Notes:

- If the base API path changes, pass `--base-url` like `--base-url https://data.gov.hk/en-data/api/3/action`.
- This tool is metadata-only. Downloading resource contents can be layered later if needed.

Providers overview (new)

- Added `crawl_providers_datasets.py` to list all providers (organizations) and their datasets with brief descriptions.
- Outputs:
  - JSON: `providers_with_datasets_*.json` (providers with embedded dataset briefs)
  - CSV: `datasets_by_provider_*.csv` (one row per dataset)
  - CSV: `providers_summary_*.csv` (one row per provider with counts)

Examples:

1) All providers, limit 5 datasets per provider:

	- `python openData/crawl_providers_datasets.py --dataset-limit 5`

2) First 10 providers, all datasets, no JSON:

	- `python openData/crawl_providers_datasets.py --org-limit 10 --no-json`

#!/usr/bin/env python3
"""
Crawler for Data.gov.hk metadata using the CKAN API.

Features
- Paginates through package_search
- Extracts key dataset + resource fields
- Heuristic api_access flag (datastore_active or resource URL includes '/api/')
- Saves JSON (full metadata) and CSV (flattened) with timestamped filenames
- Small CLI for limits/filters

Note: This fetches metadata only, not resource contents.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
import pandas as pd


DEFAULT_BASE_URLS = [
    # Primary English portal (most likely correct)
    "https://data.gov.hk/en-data/api/3/action",
    # Traditional Chinese portal (fallback)
    "https://data.gov.hk/tc-data/api/3/action",
    # Root CKAN path (fallback if above paths change)
    "https://data.gov.hk/api/3/action",
]


def pick_working_base_url(session: requests.Session, timeout: float = 15.0) -> str:
    """Return the first CKAN base URL that responds for package_search.

    Tries a small query with rows=0 to validate quickly.
    """
    for base in DEFAULT_BASE_URLS:
        url = f"{base}/package_search"
        try:
            resp = session.get(url, params={"rows": 0}, timeout=timeout)
            if resp.ok and resp.json().get("success"):
                return base
        except Exception:
            pass
    # If none validated, fall back to the first (will likely still work)
    return DEFAULT_BASE_URLS[0]


def ckan_package_search(
    session: requests.Session,
    base_url: str,
    start: int = 0,
    rows: int = 100,
    q: Optional[str] = None,
    organization: Optional[str] = None,
    timeout: float = 30.0,
    retries: int = 3,
    backoff: float = 1.5,
) -> Dict[str, Any]:
    """Call CKAN package_search with basic retry/backoff.

    Returns decoded JSON.
    """
    url = f"{base_url}/package_search"
    params: Dict[str, Any] = {"start": start, "rows": rows}
    if q:
        params["q"] = q
    if organization:
        params["fq"] = f"organization:{organization}"

    last_err: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("success"):
                raise RuntimeError(f"CKAN API success=false: {data}")
            return data
        except Exception as e:
            last_err = e
            sleep_s = backoff ** (attempt - 1)
            time.sleep(sleep_s)
    assert last_err is not None
    raise last_err


def extract_dataset_record(pkg: Dict[str, Any]) -> Dict[str, Any]:
    """Extract a normalized dataset record from CKAN package JSON."""
    org = pkg.get("organization") or {}
    tags = [t.get("name") for t in pkg.get("tags", []) if isinstance(t, dict)]
    groups = [g.get("name") for g in pkg.get("groups", []) if isinstance(g, dict)]

    resources_raw: List[Dict[str, Any]] = [r for r in pkg.get("resources", []) if isinstance(r, dict)]
    resources: List[Dict[str, Any]] = []
    api_access = False
    for r in resources_raw:
        rid = r.get("id")
        url = r.get("url")
        fmt = (r.get("format") or "").upper()
        datastore_active = bool(r.get("datastore_active"))
        if datastore_active or (isinstance(url, str) and "/api/" in url):
            api_access = True
        resources.append(
            {
                "resource_id": rid,
                "name": r.get("name"),
                "description": r.get("description") or r.get("notes"),
                "format": fmt,
                "mimetype": r.get("mimetype"),
                "url": url,
                "size": r.get("size"),
                "hash": r.get("hash"),
                "created": r.get("created"),
                "last_modified": r.get("last_modified"),
                "datastore_active": datastore_active,
                "resource_type": r.get("resource_type"),
            }
        )

    record = {
        "dataset_id": pkg.get("id"),
        "name": pkg.get("name"),
        "title": pkg.get("title"),
        "notes": pkg.get("notes"),
        "state": pkg.get("state"),
        "license_id": pkg.get("license_id"),
        "license_title": pkg.get("license_title"),
        "metadata_created": pkg.get("metadata_created"),
        "metadata_modified": pkg.get("metadata_modified"),
        "maintainer": pkg.get("maintainer"),
        "maintainer_email": pkg.get("maintainer_email"),
        "author": pkg.get("author"),
        "author_email": pkg.get("author_email"),
        "organization_id": org.get("id"),
        "organization_name": org.get("name"),
        "organization_title": org.get("title"),
        "tags": tags,
        "groups": groups,
        "num_resources": len(resources),
        "resources": resources,
        "api_access": api_access,
        "url": pkg.get("url"),
        "version": pkg.get("version"),
        "isopen": pkg.get("isopen"),
        "extras": pkg.get("extras"),  # list of {key, value}
    }
    return record


def iter_all_packages(
    session: requests.Session,
    base_url: str,
    limit: Optional[int] = None,
    q: Optional[str] = None,
    organization: Optional[str] = None,
    page_size: int = 100,
) -> Iterable[Dict[str, Any]]:
    """Iterate over packages via package_search, yielding normalized records.

    If limit is provided, stops after yielding at most 'limit' records.
    """
    yielded = 0
    start = 0
    total_known: Optional[int] = None

    while True:
        rows = page_size
        if limit is not None:
            rows = min(rows, max(0, limit - yielded))
            if rows == 0:
                break

        data = ckan_package_search(
            session=session,
            base_url=base_url,
            start=start,
            rows=rows,
            q=q,
            organization=organization,
        )

        result = data.get("result", {})
        total = int(result.get("count") or 0)
        if total_known is None:
            total_known = total

        packages = result.get("results", []) or []
        if not packages:
            break

        for pkg in packages:
            rec = extract_dataset_record(pkg)
            yield rec
            yielded += 1
            if limit is not None and yielded >= limit:
                return

        start += len(packages)
        if start >= total:
            break


def ensure_dir(path: str) -> None:
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def timestamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def save_json(records: List[Dict[str, Any]], out_dir: str) -> str:
    ensure_dir(out_dir)
    fp = os.path.join(out_dir, f"data_gov_hk_datasets_{timestamp()}.json")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    return fp


def flatten_for_csv(rec: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten a metadata record for CSV output.

    - tags/groups joined by '|'
    - resource formats joined; resource URLs joined (truncated to avoid huge cells)
    - api_access retained as bool
    """
    tags = rec.get("tags") or []
    groups = rec.get("groups") or []
    resources = rec.get("resources") or []

    res_formats = [str((r.get("format") or "")).upper() for r in resources]
    res_urls = [str(r.get("url") or "") for r in resources]
    # Prevent extremely long CSV cells
    urls_joined = " | ".join(res_urls)
    if len(urls_joined) > 32000:
        urls_joined = urls_joined[:31997] + "..."

    return {
        "dataset_id": rec.get("dataset_id"),
        "name": rec.get("name"),
        "title": rec.get("title"),
        "organization_title": rec.get("organization_title"),
        "organization_name": rec.get("organization_name"),
        "license_title": rec.get("license_title"),
        "metadata_created": rec.get("metadata_created"),
        "metadata_modified": rec.get("metadata_modified"),
        "num_resources": rec.get("num_resources"),
        "api_access": rec.get("api_access"),
        "tags": "|".join([str(t) for t in tags]),
        "groups": "|".join([str(g) for g in groups]),
        "resource_formats": "|".join(res_formats),
        "resource_urls": urls_joined,
        "url": rec.get("url"),
    }


def save_csv(records: List[Dict[str, Any]], out_dir: str) -> str:
    ensure_dir(out_dir)
    rows = [flatten_for_csv(r) for r in records]
    df = pd.DataFrame(rows)
    fp = os.path.join(out_dir, f"data_gov_hk_datasets_{timestamp()}.csv")
    df.to_csv(fp, index=False)
    return fp


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Data.gov.hk metadata crawler (CKAN)")
    p.add_argument("--limit", type=int, default=100, help="Max datasets to fetch (None for all)")
    p.add_argument("--start", type=int, default=0, help="Starting offset (for pagination)")
    p.add_argument("--page-size", type=int, default=100, help="Page size for CKAN API")
    p.add_argument("--q", type=str, default=None, help="CKAN query string")
    p.add_argument("--organization", type=str, default=None, help="Filter by organization name (CKAN id/slug)")
    p.add_argument("--out-dir", type=str, default=os.path.join(os.path.dirname(__file__), "out"), help="Output directory")
    p.add_argument("--no-json", action="store_true", help="Do not write JSON output")
    p.add_argument("--no-csv", action="store_true", help="Do not write CSV output")
    p.add_argument("--base-url", type=str, default=None, help="Override CKAN base URL (ends with /api/3/action)")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    session = requests.Session()
    session.headers.update({
        "User-Agent": "data-gov-hk-crawler/1.0 (+https://data.gov.hk/)"
    })

    base_url = args.base_url or pick_working_base_url(session)

    # Iterate and collect
    records: List[Dict[str, Any]] = []
    collected = 0
    for rec in iter_all_packages(
        session=session,
        base_url=base_url,
        limit=args.limit if args.limit is not None and args.limit >= 0 else None,
        q=args.q,
        organization=args.organization,
        page_size=args.page_size,
    ):
        # Honor --start by skipping initial records
        if collected < args.start:
            collected += 1
            continue
        records.append(rec)
        collected += 1

    if not records:
        print("No records fetched.")
        return 0

    # Write outputs
    outputs: List[Tuple[str, str]] = []  # (kind, path)
    if not args.no_json:
        jf = save_json(records, args.out_dir)
        outputs.append(("json", jf))
    if not args.no_csv:
        cf = save_csv(records, args.out_dir)
        outputs.append(("csv", cf))

    for kind, path in outputs:
        print(f"Wrote {kind.upper()}: {path}")

    # Quick summary
    api_yes = sum(1 for r in records if r.get("api_access"))
    print(f"Datasets fetched: {len(records)} | with API access (heuristic): {api_yes}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

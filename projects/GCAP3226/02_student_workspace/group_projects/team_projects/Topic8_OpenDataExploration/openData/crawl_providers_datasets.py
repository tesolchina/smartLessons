#!/usr/bin/env python3
"""
List providers (organizations) on Data.gov.hk and enumerate datasets for each provider with a brief description.

Outputs
- JSON: provider objects with datasets (id, title, notes, num_resources)
- CSV (datasets): flattened per-dataset rows with provider info
- CSV (providers): provider-level summary (counts)

Uses Data.gov.hk CKAN API. Metadata only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import time
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
import pandas as pd

# Try package-relative import first; fall back to direct import when run as a script
try:  # type: ignore
    from . import crawl_data_gov_hk as base  # reuse helpers
except Exception:  # running as a script, not a package
    import sys as _sys, os as _os
    _sys.path.append(_os.path.dirname(__file__))
    import crawl_data_gov_hk as base  # type: ignore


def ckan_organization_list(
    session: requests.Session,
    base_url: str,
    all_fields: bool = True,
    timeout: float = 30.0,
    retries: int = 3,
    backoff: float = 1.5,
) -> List[Dict[str, Any]]:
    url = f"{base_url}/organization_list"
    params = {"all_fields": json.dumps(all_fields)}
    last_err: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("success"):
                raise RuntimeError(f"CKAN API success=false: {data}")
            result = data.get("result")
            if isinstance(result, list):
                return result
            return []
        except Exception as e:
            last_err = e
            time.sleep(backoff ** (attempt - 1))
    assert last_err is not None
    raise last_err


def iter_org_datasets(
    session: requests.Session,
    base_url: str,
    org_name: str,
    limit: Optional[int] = None,
    page_size: int = 100,
) -> Iterable[Dict[str, Any]]:
    yielded = 0
    start = 0
    while True:
        rows = page_size
        if limit is not None:
            rows = min(rows, max(0, limit - yielded))
            if rows == 0:
                break
        data = base.ckan_package_search(
            session=session,
            base_url=base_url,
            start=start,
            rows=rows,
            q=None,
            organization=org_name,
        )
        result = data.get("result", {})
        total = int(result.get("count") or 0)
        packages = result.get("results", []) or []
        if not packages:
            break
        for pkg in packages:
            yield pkg
            yielded += 1
            if limit is not None and yielded >= limit:
                return
        start += len(packages)
        if start >= total:
            break


def extract_dataset_brief(pkg: Dict[str, Any]) -> Dict[str, Any]:
    org = pkg.get("organization") or {}
    return {
        "dataset_id": pkg.get("id"),
        "dataset_name": pkg.get("name"),
        "dataset_title": pkg.get("title"),
        "dataset_notes": pkg.get("notes"),
        "num_resources": len(pkg.get("resources", []) or []),
        "organization_name": org.get("name"),
        "organization_title": org.get("title"),
        "metadata_modified": pkg.get("metadata_modified"),
        "url": pkg.get("url"),
    }


def timestamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def save_json(data: Any, out_dir: str, stem: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{stem}_{timestamp()}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def save_csv(rows: List[Dict[str, Any]], out_dir: str, stem: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    df = pd.DataFrame(rows)
    path = os.path.join(out_dir, f"{stem}_{timestamp()}.csv")
    df.to_csv(path, index=False)
    return path


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="List providers and datasets from Data.gov.hk")
    p.add_argument("--org-limit", type=int, default=None, help="Max number of organizations to process (None for all)")
    p.add_argument("--dataset-limit", type=int, default=None, help="Max datasets per organization (None for all)")
    p.add_argument("--page-size", type=int, default=100, help="CKAN page size for datasets")
    p.add_argument("--out-dir", type=str, default=os.path.join(os.path.dirname(__file__), "out"), help="Output directory")
    p.add_argument("--base-url", type=str, default=None, help="Override CKAN base URL (ends with /api/3/action)")
    p.add_argument("--no-json", action="store_true", help="Do not write JSON output")
    p.add_argument("--no-csv", action="store_true", help="Do not write CSV outputs")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    session = requests.Session()
    session.headers.update({"User-Agent": "data-gov-hk-crawler/1.0"})

    base_url = args.base_url or base.pick_working_base_url(session)

    orgs = ckan_organization_list(session, base_url=base_url, all_fields=True)
    if args.org_limit is not None and args.org_limit >= 0:
        orgs = orgs[: args.org_limit]

    providers: List[Dict[str, Any]] = []
    dataset_rows: List[Dict[str, Any]] = []
    provider_rows: List[Dict[str, Any]] = []

    for org in orgs:
        oname = org.get("name")
        otitle = org.get("title")
        oid = org.get("id")
        if not oname:
            continue
        # Collect datasets for this org
        datasets: List[Dict[str, Any]] = []
        for pkg in iter_org_datasets(
            session=session,
            base_url=base_url,
            org_name=oname,
            limit=args.dataset_limit,
            page_size=args.page_size,
        ):
            brief = extract_dataset_brief(pkg)
            datasets.append(brief)
            ds = base.extract_dataset_record(pkg)
            # Flatten to a dataset row (with provider info)
            flat = base.flatten_for_csv(ds)
            flat["organization_id"] = oid
            dataset_rows.append(flat)

        providers.append(
            {
                "organization_id": oid,
                "organization_name": oname,
                "organization_title": otitle,
                "num_datasets": len(datasets),
                "datasets": datasets,
            }
        )
        provider_rows.append(
            {
                "organization_id": oid,
                "organization_name": oname,
                "organization_title": otitle,
                "num_datasets": len(datasets),
            }
        )

    outputs: List[Tuple[str, str]] = []
    if not args.no_json:
        path = save_json(providers, args.out_dir, stem="providers_with_datasets")
        outputs.append(("json", path))
    if not args.no_csv:
        dpath = save_csv(dataset_rows, args.out_dir, stem="datasets_by_provider")
        outputs.append(("csv", dpath))
        ppath = save_csv(provider_rows, args.out_dir, stem="providers_summary")
        outputs.append(("csv", ppath))

    for kind, path in outputs:
        print(f"Wrote {kind.upper()}: {path}")

    print(
        f"Providers processed: {len(providers)} | Total dataset rows: {len(dataset_rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations
from pathlib import Path
import urllib.parse
import urllib.request
import json
import time
from typing import Any, Dict, List

BASE = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
OUT_DIR = BASE / "_open_data_inventory"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_JSON = OUT_DIR / "datasets_catalog.json"
OUT_PROVIDERS = OUT_DIR / "providers_counts.csv"

CKAN_BASE = "https://data.gov.hk/en-data/api/3/action"


def ckan_request(action: str, params: dict) -> dict:
    items: list[tuple[str, str]] = []
    for k, v in params.items():
        if isinstance(v, (list, tuple)):
            for vv in v:
                items.append((k, str(vv)))
        else:
            items.append((k, str(v)))
    qs = urllib.parse.urlencode(items)
    url = f"{CKAN_BASE}/{action}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def page_packages(max_rows: int | None = None, page_size: int = 100) -> List[Dict[str, Any]]:
    """Iterate through CKAN package_search results and yield packages."""
    collected: List[Dict[str, Any]] = []
    start = 0
    while True:
        rows = page_size if max_rows is None else min(page_size, max_rows - len(collected))
        if rows <= 0:
            break
        data = ckan_request("package_search", {"q": "", "rows": rows, "start": start})
        if not data.get("success"):
            break
        result = data.get("result", {})
        pkgs = result.get("results", [])
        if not pkgs:
            break
        collected.extend(pkgs)
        start += len(pkgs)
        if max_rows is not None and len(collected) >= max_rows:
            break
        if len(pkgs) < rows:
            break
        time.sleep(0.25)
    return collected


def _get(obj: dict, *keys, default=""):
    cur = obj
    for k in keys:
        if cur is None:
            return default
        cur = cur.get(k)
    return cur if cur is not None else default


def package_to_record(pkg: dict) -> dict:
    org = pkg.get("organization") or {}
    tags = [t.get("display_name") or t.get("name") for t in pkg.get("tags", [])]
    groups = [g.get("display_name") or g.get("name") for g in pkg.get("groups", [])]
    formats = []
    for r in pkg.get("resources", []):
        fmt = (r.get("format") or "").strip()
        if fmt:
            formats.append(fmt.upper())
    formats = sorted(list({f for f in formats if f}))
    package_url = f"https://data.gov.hk/en-data/dataset/{pkg.get('name')}"
    return {
        "id": pkg.get("id"),
        "name": pkg.get("name"),
        "title": pkg.get("title"),
        "notes": pkg.get("notes") or "",
        "organization": org.get("title") or org.get("name") or "",
        "organization_id": org.get("id") or "",
        "tags": tags,
        "groups": groups,
        "formats": formats,
        "license_id": pkg.get("license_id") or "",
        "metadata_created": pkg.get("metadata_created") or "",
        "metadata_modified": pkg.get("metadata_modified") or "",
        "package_url": package_url,
    }


def build_catalog(max_rows: int | None = None) -> list[dict]:
    pkgs = page_packages(max_rows=max_rows, page_size=100)
    records = [package_to_record(p) for p in pkgs]
    return records


def save_catalog(records: list[dict]):
    # JSON for UI
    OUT_JSON.write_text(json.dumps({"datasets": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    # Provider counts CSV
    from collections import Counter
    counts = Counter([r.get("organization", "") for r in records if r.get("organization")])
    import pandas as pd
    df = (
        pd.DataFrame([(org, n) for org, n in counts.items()], columns=["organization", "count"])
        .sort_values("count", ascending=False)
    )
    df.to_csv(OUT_PROVIDERS, index=False)


def main():
    # Fetch all packages (metadata only). If the catalog is very large, you may set a cap e.g. max_rows=5000
    records = build_catalog(max_rows=None)
    save_catalog(records)
    print(f"Saved catalog: {OUT_JSON}")
    print(f"Saved provider counts: {OUT_PROVIDERS}")
    print(f"Datasets: {len(records)}")


if __name__ == "__main__":
    main()

from __future__ import annotations
from pathlib import Path
import urllib.parse
import urllib.request
import json
import pandas as pd

BASE = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
OUT_DIR = BASE / "_open_data_inventory"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CKAN_BASE = "https://data.gov.hk/en-data/api/3/action"


def ckan_request(action: str, params: dict) -> dict:
    """Call CKAN API and return parsed JSON dict. Supports repeated facet.field."""
    # Build query string, allowing multiple facet.field params
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
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_facets() -> tuple[int, dict[str, pd.DataFrame]]:
    facet_fields = [
        "organization",   # publishing organizations
        "res_format",     # resource formats
        "groups",         # CKAN groups / topics
        "tags",           # tags
        "license_id",     # license identifiers
    ]
    params = {
        "q": "",             # all datasets
        "rows": 0,            # we only need counts/facets
        "facet": "true",
        "facet.field": facet_fields,
        "facet.limit": 1000,  # increase default (typically 50)
    }
    data = ckan_request("package_search", params)
    if not data.get("success"):
        raise RuntimeError("CKAN request failed")
    result = data.get("result", {})
    total = int(result.get("count", 0))
    facets = result.get("facets", {}) or {}

    frames: dict[str, pd.DataFrame] = {}
    for field in facet_fields:
        items = facets.get(field, {}) or {}
        # items is a dict: value -> count
        df = (
            pd.DataFrame(
                [(k, int(v)) for k, v in items.items()],
                columns=[field, "count"],
            )
            .sort_values("count", ascending=False)
            .reset_index(drop=True)
        )
        frames[field] = df
    return total, frames


def save_outputs(total: int, frames: dict[str, pd.DataFrame]) -> Path:
    # Save CSVs
    for field, df in frames.items():
        out_csv = OUT_DIR / f"ckan_facets_{field}.csv"
        df.to_csv(out_csv, index=False)

    # Write Markdown overview
    md = [
        "# data.gov.hk Catalog Overview",
        "",
        f"Total datasets indexed: {total}",
        "",
    ]
    # Top 10 per facet (if available)
    pretty_titles = {
        "organization": "Top organizations",
        "res_format": "Top resource formats",
        "groups": "Top CKAN groups",
        "tags": "Top tags",
        "license_id": "Top licenses",
    }
    for field, title in pretty_titles.items():
        df = frames.get(field)
        if df is None or df.empty:
            continue
        head = df.head(10)
        md.append(f"## {title}")
        md.append("")
        for _, row in head.iterrows():
            label = str(row[field]) if pd.notna(row[field]) else "(blank)"
            md.append(f"- {label}: {int(row['count'])}")
        md.append("")

    out_md = OUT_DIR / "CKAN_CATALOG_OVERVIEW.md"
    out_md.write_text("\n".join(md), encoding="utf-8")
    return out_md


def main():
    total, frames = fetch_facets()
    out_md = save_outputs(total, frames)
    print(f"Wrote overview: {out_md}")
    for field in frames:
        print(f"Saved: {OUT_DIR / f'ckan_facets_{field}.csv'}")


if __name__ == "__main__":
    main()

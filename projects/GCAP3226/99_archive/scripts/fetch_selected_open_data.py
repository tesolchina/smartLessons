from __future__ import annotations
from pathlib import Path
import ast
import csv
import json
import sys
import re
import urllib.parse
import urllib.request

import pandas as pd

BASE = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
CATALOG_DIR = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/crawlGovWebsite/gcap 3226/openData/out")
OUT_ROOT = BASE / "course_materials/resources/datasets/open_data"
OUT_ROOT.mkdir(parents=True, exist_ok=True)

TOPIC_KEYWORDS = {
    "air_quality": ["aqhi", "air quality", "pm2", "pm10", "no2", "o3", "so2", "空氣", "空气", "污染"],
    "transport": ["journey time", "speed map", "traffic", "transport", "congestion", "bus", "mtr", "ferry"],
    "housing": ["housing", "estate", "waiting time", "allocation", "公屋", "房屋", "租金", "樓價"],
}

# Organization hints to improve recall when titles/tags are sparse
ORG_HINTS = {
    "air_quality": ["Environmental Protection Department", "EPD"],
    "transport": ["Transport Department", "TD"],
    "housing": ["Housing Authority", "Housing Department", "HA"],
}

PREFERRED_EXT = (".csv", ".json", ".geojson")


def latest_file(glob_pattern: str) -> Path | None:
    files = sorted(CATALOG_DIR.glob(glob_pattern))
    return files[-1] if files else None


def normalize_list_like(val) -> list[str]:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return []
    s = str(val)
    if (s.startswith("[") and s.endswith("]")) or (s.startswith("(") and s.endswith(")")):
        try:
            v = ast.literal_eval(s)
            if isinstance(v, (list, tuple)):
                return [str(x) for x in v]
        except Exception:
            pass
    if "|" in s:
        return [p.strip() for p in s.split("|") if p.strip()]
    return [s]


def pick_resource_url(urls: list[str]) -> str:
    # prioritize CSV/JSON/GeoJSON
    for ext in PREFERRED_EXT:
        for u in urls:
            if str(u).lower().endswith(ext):
                return u
    return urls[0] if urls else ""


def download(url: str, out_path: Path) -> bool:
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp, open(out_path, "wb") as f:
            f.write(resp.read())
        return True
    except Exception as e:
        print(f"  Download failed: {url}\n    -> {e}")
        return False


def select_and_fetch():
    cat_csv = latest_file("data_gov_hk_datasets_*.csv")
    if not cat_csv:
        print("No catalog CSV found under openData/out/")
        return pd.DataFrame()
    df = pd.read_csv(cat_csv)

    for col in ["tags", "resource_urls"]:
        if col in df.columns:
            df[col] = df[col].apply(normalize_list_like)
        else:
            df[col] = [[] for _ in range(len(df))]

    df["topic_match"] = ""
    title_series = df["title"].astype(str) if "title" in df.columns else pd.Series([""] * len(df))
    org_series = None
    if "organization_title" in df.columns:
        org_series = df["organization_title"].astype(str)
    elif "organization_name" in df.columns:
        org_series = df["organization_name"].astype(str)
    else:
        org_series = pd.Series([""] * len(df))

    for topic, keys in TOPIC_KEYWORDS.items():
        pattern = "|".join([re.escape(k.lower()) for k in keys])
        title_mask = title_series.str.lower().str.contains(pattern, regex=True, na=False)
        tags_mask = df["tags"].apply(lambda xs: any(k.lower() in " ".join(xs).lower() for k in keys))
        hints = ORG_HINTS.get(topic, [])
        org_mask = org_series.str.contains("|".join([re.escape(h) for h in hints]), case=False, regex=True, na=False) if hints else False
        mask = title_mask | tags_mask | org_mask
        df.loc[mask & (df["topic_match"] == ""), "topic_match"] = topic

    # Initial selection by keyword/topic match
    sel = df[df["topic_match"].isin(TOPIC_KEYWORDS.keys())].copy()

    # Provider-based fallback: if a topic is underrepresented, add rows by organization hints
    def add_provider_rows(topic: str, limit: int = 5):
        nonlocal sel
        if topic in sel.get("topic_match", pd.Series([], dtype=str)).values:
            return
        hints = ORG_HINTS.get(topic, [])
        if not hints:
            return
        org_series = None
        if "organization_title" in df.columns:
            org_series = df["organization_title"].astype(str)
        elif "organization_name" in df.columns:
            org_series = df["organization_name"].astype(str)
        else:
            return
        mask = org_series.str.contains("|".join([re.escape(h) for h in hints]), case=False, regex=True, na=False)
        add = df[mask].copy()
        if add.empty:
            return
        add = add.head(limit)
        add.loc[:, "topic_match"] = topic
        sel = pd.concat([sel, add], ignore_index=True)

    for t in TOPIC_KEYWORDS.keys():
        add_provider_rows(t, limit=8)

    if sel.empty:
        print("No datasets matched the selected topics; consider expanding keywords or updating the catalog export.")
        return sel

    # Pick one best resource per dataset
    sel["picked_url"] = sel["resource_urls"].apply(pick_resource_url)
    sel = sel[sel["picked_url"] != ""].copy()

    # Download to folders
    rows = []
    for _, r in sel.iterrows():
        topic = r["topic_match"]
        title = str(r.get("title", "dataset")).strip()
        url = r["picked_url"]
        org = str(r.get("organization_title", r.get("organization_name", "")))
        ext = Path(urllib.parse.urlparse(url).path).suffix.lower() or ".dat"
        safe = "".join([c if c.isalnum() or c in ("-", "_") else "_" for c in title])[:80]
        out_dir = OUT_ROOT / ({
            "air_quality": "air_quality",
            "transport": "transport",
            "housing": "housing",
        }[topic])
        out_path = out_dir / f"{safe}{ext}"
        print(f"Fetching [{topic}] {title}\n  -> {url}")
        ok = download(url, out_path)
        rows.append({
            "topic": topic,
            "title": title,
            "provider": org,
            "url": url,
            "saved_to": str(out_path),
            "status": "ok" if ok else "failed",
        })

    report = pd.DataFrame(rows)
    report.to_csv(BASE / "_open_data_inventory/selected_datasets_downloads.csv", index=False)
    return report


if __name__ == "__main__":
    rep = select_and_fetch()
    if isinstance(rep, pd.DataFrame) and not rep.empty:
        cols = [c for c in ["topic", "title", "status", "saved_to"] if c in rep.columns]
        if cols:
            print(rep[cols].head(20).to_string(index=False))
    else:
        print("No downloads completed.")

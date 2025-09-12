#!/usr/bin/env python3
"""
Clean YR 10 DATA.xlsx into tidy CSVs for analysis and charting.

Outputs (created in ./cleaned/):
- cleaned_long.csv  (group, site, variable, value_raw, value_num, unit)
- cleaned_wide.csv  (group, site, eqs, building_height_m, decibels_db, traffic_total, distance_m)

This script is designed to be robust to slightly inconsistent sheet formats.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_XLSX = ROOT / "data" / "YR 10 DATA.xlsx"
OUT_DIR = ROOT / "cleaned"


def iter_group_sheets(xl: pd.ExcelFile) -> Iterable[Tuple[str, pd.DataFrame]]:
    for name in xl.sheet_names:
        name_str = str(name)
        if name_str.strip().upper().startswith("GROUP "):
            df = xl.parse(name_str, header=None, dtype=str)
            yield name_str.strip(), df


def find_site_columns(df: pd.DataFrame) -> Tuple[int, List[Tuple[int, str]]]:
    """Locate the header row containing SITE labels and return (header_row_idx, site_cols[(col_idx, site_name)])."""
    header_row = None
    site_cols: List[Tuple[int, str]] = []
    for i in range(min(15, len(df))):  # search first rows
        row = df.iloc[i].astype(str).fillna("")
        names = [s.strip().upper() for s in row.tolist()]
        if any(s.startswith("SITE ") for s in names):
            header_row = i
            for j, s in enumerate(names):
                if s.startswith("SITE "):
                    site_cols.append((j, s.title()))  # e.g., 'Site 1'
            break
    if header_row is None or not site_cols:
        raise ValueError("Could not detect SITE columns")
    return header_row, site_cols


def first_label_in_row(row: pd.Series) -> Optional[str]:
    for v in row.tolist():
        if pd.isna(v):
            continue
        s = str(v).strip()
        if s:
            return s
    return None


def extract_long_from_group(df: pd.DataFrame, group_name: str) -> List[Dict[str, Any]]:
    hdr_idx, site_cols = find_site_columns(df)
    records: List[Dict[str, Any]] = []
    # Start from row after a blank separator if present
    start_row = hdr_idx + 1
    # skip any fully-empty rows right after header
    while start_row < len(df) and df.iloc[start_row].isna().all():
        start_row += 1

    for i in range(start_row, len(df)):
        row = df.iloc[i]
        if row.isna().all():
            continue
        label = first_label_in_row(row)
        if not label:
            continue
        label_up = label.strip().upper()
        # ignore sheet footer artifacts
        if label_up in {"GROUP", group_name.strip().upper()}:
            continue
        for col_idx, site_name in site_cols:
            raw = row.iloc[col_idx]
            if pd.isna(raw) or str(raw).strip() == "":
                continue
            records.append({
                "group": group_name.title(),
                "site": site_name.title(),
                "variable": label.strip(),
                "value_raw": str(raw).strip(),
            })
    return records


def parse_numeric(value: str) -> Optional[float]:
    if value is None:
        return None
    s = str(value).strip()
    if s == "":
        return None
    # extract numbers/ranges
    nums = re.findall(r"[-+]?\d*\.?\d+", s)
    if not nums:
        return None
    # If looks like a range "12-13", average the two
    if re.search(r"\d+\s*[-–]\s*\d+", s):
        try:
            parts = re.split(r"[-–]", s)
            vals = [float(x) for x in re.findall(r"\d*\.?\d+", " ".join(parts[:2]))]
            if len(vals) >= 2:
                return float(np.mean(vals[:2]))
        except Exception:
            pass
    # Otherwise take the first numeric sequence
    try:
        return float(nums[0])
    except Exception:
        return None


def clean_row_variable(variable: str, value_raw: str) -> Tuple[str, Optional[float], Optional[str]]:
    v = variable.strip().upper()
    s = (value_raw or "").strip()
    unit: Optional[str] = None

    if v.startswith("EQS"):
        # examples: "2+", "-17", "3", "14" -> int
        s2 = s.replace("+", "")
        val = parse_numeric(s2)
        if val is not None:
            return ("eqs", float(int(val)), unit)
        return ("eqs", None, unit)

    if "BUILD" in v:  # handles BULDING/BUILDING HEIGHT
        # may be meters or stories text (e.g., "Avg 7 stories"). If stories textual, parse number.
        val = parse_numeric(s)
        # heuristic: if the text mentions 'story' and value < 50, treat as stories and convert to meters (3m/story)
        if re.search(r"stor(y|ies)", s, flags=re.I) and val is not None:
            unit = "stories"
            return ("building_height_m", float(val * 3.0), "meters")
        unit = "meters"
        return ("building_height_m", val, unit)

    if "DECIBEL" in v:
        val = parse_numeric(s)  # strip dBa
        return ("decibels_db", val, "dB")

    if "TRAFFIC" in v:
        # may be free text like "24 in 2 minutes" -> 24
        val = parse_numeric(s)
        return ("traffic_total", val, "count_2min")

    if "PEDESTRIAN" in v:
        val = parse_numeric(s)
        return ("pedestrian_count", val, "count")

    if "LANDUSE" in v or "LAND USE" in v:
        return ("land_use", None, None)

    if "ORDER" in v:
        return ("order_label", None, None)

    # default: unknown variable
    return (v.lower(), None, None)


def build_clean_frames(long_records: List[Dict[str, Any]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    long_df = pd.DataFrame(long_records)
    if long_df.empty:
        return long_df, long_df
    fields = long_df.apply(
        lambda r: clean_row_variable(str(r["variable"]), str(r["value_raw"])), axis=1
    )
    long_df[["norm_variable", "value_num", "unit"]] = pd.DataFrame(fields.tolist(), index=long_df.index)

    # keep only recognized numeric variables for wide pivot
    keep_vars = {"eqs", "building_height_m", "decibels_db", "traffic_total", "pedestrian_count"}
    wide_df = (
        long_df[long_df["norm_variable"].isin(keep_vars)]
        .pivot_table(index=["group", "site"], columns="norm_variable", values="value_num", aggfunc="first")
        .reset_index()
    )
    # flatten columns
    wide_df.columns = [str(c) for c in wide_df.columns]
    return long_df, wide_df


def parse_distance_sheet(xl: pd.ExcelFile) -> pd.DataFrame:
    if "Distance Data" not in xl.sheet_names:
        return pd.DataFrame(columns=["group", "site", "distance_m"])
    df = xl.parse("Distance Data", header=None, dtype=str)
    df = df.fillna("")
    # Expect pattern like: row with "Group 1", then rows with "Site 1" and distance like "303m"
    records = []
    current_group = None
    for i in range(len(df)):
        row = [str(x).strip() for x in df.iloc[i].tolist()]
        if not any(row):
            continue
        # detect group row
        for cell in row:
            if re.match(r"(?i)group\s*\d+", cell):
                current_group = cell.title().strip()
        # detect site + distance in same row
        site = None
        dist = None
        for cell in row:
            if re.match(r"(?i)site\s*\d+", cell):
                site = cell.title().strip()
            if re.search(r"\d+\s*m\b", cell.lower()):
                m = re.search(r"(\d+)\s*m\b", cell.lower())
                if m:
                    dist = float(m.group(1))
        if current_group and site and dist is not None:
            records.append({"group": current_group, "site": site, "distance_m": dist})
    return pd.DataFrame(records)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    xl = pd.ExcelFile(DATA_XLSX)

    all_records: List[Dict[str, Any]] = []
    for sheet_name, df in iter_group_sheets(xl):
        try:
            recs = extract_long_from_group(df, sheet_name)
            all_records.extend(recs)
        except Exception as e:
            print(f"Warning: skipping {sheet_name}: {e}")

    long_df, wide_df = build_clean_frames(all_records)
    dist_df = parse_distance_sheet(xl)

    # join distance into wide
    if not wide_df.empty and not dist_df.empty:
        wide_df = wide_df.merge(dist_df, on=["group", "site"], how="left")

    # Save outputs
    long_out = OUT_DIR / "cleaned_long.csv"
    wide_out = OUT_DIR / "cleaned_wide.csv"
    long_df.to_csv(long_out, index=False)
    wide_df.to_csv(wide_out, index=False)
    print(f"Wrote {long_out}")
    print(f"Wrote {wide_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

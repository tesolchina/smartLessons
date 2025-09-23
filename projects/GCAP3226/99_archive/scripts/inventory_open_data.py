from pathlib import Path
import json
import pandas as pd

ROOT = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/crawlGovWebsite/gcap 3226/openData")
OUT_DIR = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226/_open_data_inventory")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def human_size(n: float) -> str:
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    for u in units:
        if n < 1024:
            return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} EB"


def read_head(p: Path, n: int = 5):
    try:
        if p.suffix.lower() == ".csv":
            return pd.read_csv(p, nrows=n, low_memory=False, on_bad_lines="skip")
        if p.suffix.lower() == ".xlsx":
            # requires openpyxl
            return pd.read_excel(p, nrows=n)
        if p.suffix.lower() in [".json", ".geojson"]:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "features" in data:
                return pd.json_normalize(data["features"])[:n]
            if isinstance(data, list):
                return pd.json_normalize(data)[:n]
            if isinstance(data, dict):
                return pd.json_normalize([data])[:n]
    except Exception as e:
        return f"Preview failed: {e}"
    return "Unsupported format"


def infer_tags(columns) -> str:
    cols = " ".join([str(c).lower() for c in columns])
    tags = []
    key_map = {
        "waste": ["waste", "recycl", "refuse", "garbage", "bin"],
        "air_quality": ["aqhi", "air", "pm2", "no2", "o3", "aqi"],
        "traffic_accidents": ["accident", "collision", "crash", "traffic"],
        "water_beach": ["beach", "water", "e.coli", "grade"],
        "population_district": ["district", "population", "constituency", "area"],
        "facilities": ["library", "park", "sports", "recreation", "facility", "centre", "center"],
        "energy": ["energy", "electric", "gas", "power"],
        "housing": ["housing", "estate", "flat", "rent", "price"],
        "finance_budget": ["budget", "expenditure", "revenue"],
    }
    for tag, keys in key_map.items():
        if any(k in cols for k in keys):
            tags.append(tag)
    return ";".join(tags)


def main():
    files = sorted([p for ext in ["*.csv", "*.xlsx", "*.json", "*.geojson"] for p in ROOT.rglob(ext)])
    rows = []
    sample_dir = OUT_DIR / "samples"
    sample_dir.mkdir(exist_ok=True)
    for p in files:
        size = p.stat().st_size
        head = read_head(p)
        if isinstance(head, pd.DataFrame):
            cols = list(head.columns)
            tags = infer_tags(cols)
            safe_name = p.stem.replace(" ", "_")[:60]
            try:
                head.to_csv(sample_dir / f"{safe_name}_head.csv", index=False)
                head_sample_path = str(sample_dir / f"{safe_name}_head.csv")
            except Exception:
                head_sample_path = ""
            rows.append(
                {
                    "file": str(p),
                    "name": p.name,
                    "ext": p.suffix.lower(),
                    "size_bytes": size,
                    "size": human_size(size),
                    "n_cols": len(cols),
                    "sample_cols": ", ".join(cols[:15]),
                    "tags": tags or "",
                    "head_sample": head_sample_path,
                }
            )
        else:
            rows.append(
                {
                    "file": str(p),
                    "name": p.name,
                    "ext": p.suffix.lower(),
                    "size_bytes": size,
                    "size": human_size(size),
                    "n_cols": "",
                    "sample_cols": str(head),
                    "tags": "",
                    "head_sample": "",
                }
            )
    inv = pd.DataFrame(rows)
    if not inv.empty:
        inv.sort_values(["tags", "name"], inplace=True)
    out_csv = OUT_DIR / "open_data_inventory.csv"
    inv.to_csv(out_csv, index=False)
    print(f"Scanned {len(files)} files")
    print(f"Inventory written to: {out_csv}")
    print(f"Head samples in: {sample_dir}")
    if not inv.empty:
        print("\nCounts by inferred topic:")
        print(inv["tags"].replace("", "unclassified").value_counts())


if __name__ == "__main__":
    main()

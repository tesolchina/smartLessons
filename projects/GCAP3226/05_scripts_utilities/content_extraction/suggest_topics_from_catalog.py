from pathlib import Path
import ast
import pandas as pd

BASE = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
CATALOG_DIR = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/crawlGovWebsite/gcap 3226/openData/out")
OUT_MD = BASE / "course_materials/topics_explore.md"
OUT_CSV = BASE / "_open_data_inventory/dataset_candidates.csv"


def latest_file(glob_pattern: str) -> Path | None:
    files = sorted(CATALOG_DIR.glob(glob_pattern))
    return files[-1] if files else None


def normalize_list_like(series: pd.Series) -> pd.Series:
    def parse(v):
        if pd.isna(v):
            return []
        s = str(v)
        # Try Python literal
        if (s.startswith("[") and s.endswith("]")) or (s.startswith("(") and s.endswith(")")):
            try:
                val = ast.literal_eval(s)
                if isinstance(val, (list, tuple)):
                    return [str(x).strip() for x in val]
            except Exception:
                pass
        if "|" in s:
            return [p.strip() for p in s.split("|") if p.strip()]
        return [s.strip()]
    return series.apply(parse)


def topic_from_text(text: str) -> list[str]:
    t = text.lower()
    topics: list[str] = []
    mapping = {
        # Air quality and environment
        "air_quality": [
            "air quality", "aqhi", "aqi", "pm2", "pm10", "no2", "o3", "so2", "污染", "空氣", "空气",
            "air pollution", "particulate",
        ],
        # Transport and traffic
        "traffic_accidents": ["traffic accident", "road traffic accident", "collision", "crash", "意外", "交通事故"],
        "transport": [
            "transport", "bus", "mtr", "rail", "ferry", "tram", "速度", "flow", "交通", "traffic speed", "traffic flow",
            "speed map", "journey time", "congestion",
        ],
        # Waste and recycling
        "waste_recycling": [
            "waste", "recycling", "refuse", "litter", "bin", "recycle", "food waste", "廢物", "回收", "垃圾",
            "wastewater", "landfill", "waste charge",
        ],
        # Public facilities and amenities
        "public_facilities": [
            "library", "park", "sports centre", "sports center", "recreation", "facility", "leisure", "場地", "設施",
            "community hall", "swimming", "sports ground",
        ],
        # Housing
        "housing": ["housing", "estate", "hdb", "flat", "rent", "property", "公屋", "房屋", "租金", "樓價", "樓市"],
        # Water quality
        "water_quality": [
            "beach", "water quality", "e. coli", "e.coli", "drinking water", "泳灘", "水質", "海灘", "beach water",
        ],
        # General environment / climate
        "environment": ["noise", "pollution", "green", "tree", "biodiversity", "climate", "carbon", "noise level", "噪音"],
        # Health
        "health": ["hospital", "clinic", "covid", "influenza", "health", "vaccination", "公共衛生", "醫院", "醫療"],
        # Finance & budget
        "finance_budget": ["budget", "expenditure", "revenue", "spending", "tax", "財政", "預算", "開支", "稅"],
        # Population & districts
        "population_district": ["district", "population", "census", "constituency", "十八區", "地區", "人口"],
        # Education
        "education": ["school", "education", "student", "學校", "教育", "學生"],
        # Crime & safety
        "crime_safety": ["crime", "police", "fire", "accident", "罪案", "消防", "警察"],
        # Land & planning
        "land_planning": ["planning", "land", "zoning", "規劃", "地政"],
        # Energy
        "energy": ["energy", "electricity", "gas", "power", "能源", "電力", "燃氣"],
        # Economy & business
        "economy_business": ["company", "business", "employment", "trade", "經濟", "商業", "公司", "就業", "貿易"],
    }
    for k, keys in mapping.items():
        if any(term in t for term in keys):
            topics.append(k)
    return topics


def build_candidates() -> pd.DataFrame:
    cat_csv = latest_file("data_gov_hk_datasets_*.csv")
    if not cat_csv:
        return pd.DataFrame()
    df = pd.read_csv(cat_csv)

    # explode tags and resource formats for filtering
    for col in ["tags", "resource_formats"]:
        if col in df.columns:
            df[col] = normalize_list_like(df[col])
        else:
            df[col] = [[] for _ in range(len(df))]

    # Create a helper text field from title + tags
    text = (
        df.get("title", pd.Series([""] * len(df))).astype(str)
        + " "
        + df["tags"].apply(lambda xs: " ".join(xs))
        + " "
        + df.get("groups", pd.Series([""] * len(df))).astype(str)
        + " "
        + df.get("organization_title", df.get("organization_name", pd.Series([""] * len(df)))).astype(str)
    )

    topic_lists = text.apply(topic_from_text)
    df["topics"] = topic_lists

    # Keep only datasets with a resource URL that is likely CSV/JSON
    if "resource_urls" in df.columns:
        df["resource_urls"] = normalize_list_like(df["resource_urls"])
    else:
        df["resource_urls"] = [[] for _ in range(len(df))]

    def pick_url(urls: list[str]) -> str:
        for u in urls:
            ul = u.lower()
            if any(ul.endswith(ext) for ext in [".csv", ".json", ".geojson", ".xlsx"]):
                return u
        return urls[0] if urls else ""

    df["sample_resource_url"] = df["resource_urls"].apply(pick_url)

    # Select a compact candidate view
    keep_cols = [
        c for c in [
            "dataset_id",
            "title",
            "organization_title",
            "organization_name",
            "api_access",
            "resource_formats",
            "sample_resource_url",
            "topics",
            "tags",
            "groups",
        ]
        if c in df.columns
    ]
    cand = df[keep_cols].copy()

    # Expand topics to one row per topic for ranking
    cand = cand.explode("topics")
    cand = cand[cand["topics"].notna() & (cand["topics"] != "")]

    # Basic ranking: prefer datasets with CSV/JSON and API access if available
    def score_row(row) -> int:
        score = 0
        fmts = set([x.upper() for x in row.get("resource_formats", [])])
        if any(f in fmts for f in ["CSV", "JSON", "GEOJSON"]):
            score += 2
        if str(row.get("api_access")).lower() == "true":
            score += 1
        if row.get("sample_resource_url"):
            score += 1
        return score

    cand["score"] = cand.apply(score_row, axis=1)

    # Drop exact dupes
    cand = cand.drop_duplicates(subset=["dataset_id", "topics"])

    # Sort by topic then score
    cand.sort_values(["topics", "score", "title"], ascending=[True, False, True], inplace=True)

    return cand


def write_markdown(cand: pd.DataFrame):
    lines = [
        "# Datasets and Topics to Explore\n",
        "\n",
        "This note lists candidate topics and high-potential datasets from data.gov.hk for GCAP3226.\n",
        "\n",
        "Tip: prefer CSV/JSON resources and datasets with API access for easier analysis.\n",
        "\n",
    ]

    if cand.empty:
        lines.append("No candidates found yet. Ensure the catalog CSV exists in the openData/out folder.\n")
    else:
        # Overview table
        counts = (
            cand.groupby("topics").size().reset_index(name="count").sort_values("count", ascending=False)
        )
        lines.append("## Topic overview\n\n")
        for _, r in counts.iterrows():
            topic_name = str(r["topics"]).replace('_',' ').title()
            lines.append(f"- {topic_name}: {int(r['count'])} candidate datasets\n")
        lines.append("\n")

        for topic, grp in cand.groupby("topics"):
            topic_header = str(topic).replace('_', ' ').title()
            lines.append(f"## {topic_header}\n\n")
            sub = grp.head(12)
            for _, r in sub.iterrows():
                title = str(r.get("title", "(no title)"))
                org = str(r.get("organization_title", r.get("organization_name", "")))
                url = str(r.get("sample_resource_url", ""))
                fmts = ", ".join([str(x) for x in r.get("resource_formats", [])])
                api = str(r.get("api_access", ""))
                lines.append(f"- {title} — {org}\n")
                if url:
                    lines.append(f"  - Resource: {url}\n")
                if fmts:
                    lines.append(f"  - Formats: {fmts}\n")
                if api:
                    lines.append(f"  - API: {api}\n")
                lines.append("\n")

    OUT_MD.write_text("".join(lines), encoding="utf-8")


def main():
    cand = build_candidates()
    if not cand.empty:
        cand.to_csv(OUT_CSV, index=False)
    write_markdown(cand)
    print(f"Wrote topics to: {OUT_MD}")
    if not cand.empty:
        print(f"Candidates CSV: {OUT_CSV} (rows={len(cand)})")


if __name__ == "__main__":
    main()

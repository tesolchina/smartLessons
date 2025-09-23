from pathlib import Path
import ast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
CATALOG_DIR = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/crawlGovWebsite/gcap 3226/openData/out")
OUT_DIR = BASE / "_open_data_inventory"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


def latest_file(glob_pattern: str) -> Path | None:
    files = sorted(CATALOG_DIR.glob(glob_pattern))
    return files[-1] if files else None


def load_catalog():
    datasets_csv = latest_file("data_gov_hk_datasets_*.csv")
    datasets_json = latest_file("data_gov_hk_datasets_*.json")
    by_provider = latest_file("datasets_by_provider_*.csv")
    providers_summary = latest_file("providers_summary_*.csv")

    df_datasets = pd.read_csv(datasets_csv) if datasets_csv else None
    df_by_provider = pd.read_csv(by_provider) if by_provider else None
    df_providers_sum = pd.read_csv(providers_summary) if providers_summary else None

    return df_datasets, df_by_provider, df_providers_sum


def clean_lists(col_series: pd.Series) -> pd.Series:
    """Normalize list-like string fields into Python lists.
    Handles cases like "['CSV','JSON']", "CSV|JSON", single values, or NaN.
    """
    def parse(v):
        if pd.isna(v):
            return []
        s = str(v).strip()
        # Try Python literal lists first
        if (s.startswith("[") and s.endswith("]")) or (s.startswith("(") and s.endswith(")")):
            try:
                val = ast.literal_eval(s)
                if isinstance(val, (list, tuple)):
                    return [str(x).strip() for x in val]
            except Exception:
                pass
        # Pipe-separated values
        if "|" in s:
            return [part.strip() for part in s.split("|") if part.strip()]
        # Fallback single value
        return [s]

    return col_series.apply(parse)


def summarize_formats(df: pd.DataFrame) -> pd.DataFrame:
    formats_expanded = (
        clean_lists(df.get("resource_formats", pd.Series([], dtype=object)))
        .explode()
        .astype(str)
        .str.upper()
        .str.strip()
    )
    formats_expanded = formats_expanded[formats_expanded.notna() & (formats_expanded != "")]
    return formats_expanded.value_counts().rename_axis("format").reset_index(name="count")


def summarize_api_access(df: pd.DataFrame) -> pd.DataFrame:
    api = df.get("api_access")
    if api is None:
        return pd.DataFrame({"api_access": ["unknown"], "count": [len(df)]})
    api_norm = api.astype(str).str.lower().map({"true": True, "false": False}).fillna("unknown")
    return api_norm.value_counts(dropna=False).rename_axis("api_access").reset_index(name="count")


def top_providers(df_by_provider: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Aggregate by provider to avoid duplicates and rank by dataset count.
    If dataset_id exists, count unique dataset_id per provider; else count rows.
    """
    prov_keys = [
        k for k in ["organization_id", "organization_name", "organization_title"]
        if k in df_by_provider.columns
    ]
    if not prov_keys:
        return pd.DataFrame()
    if "dataset_id" in df_by_provider.columns:
        agg = (
            df_by_provider.groupby(prov_keys)["dataset_id"].nunique().reset_index(name="datasets_count")
        )
    else:
        agg = df_by_provider.groupby(prov_keys).size().reset_index(name="datasets_count")
    agg.sort_values("datasets_count", ascending=False, inplace=True)
    return agg.head(n)


def barplot(df: pd.DataFrame, x: str, y: str, title: str, fname: str, height=6, width=10):
    plt.figure(figsize=(width, height))
    ax = sns.barplot(data=df, x=x, y=y)
    ax.set_title(title)
    ax.set_xlabel(x.replace("_", " ").title())
    ax.set_ylabel(y.replace("_", " ").title())
    plt.tight_layout()
    out = FIG_DIR / fname
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def main():
    df_datasets, df_by_provider, df_providers_sum = load_catalog()

    summaries = {}

    if df_datasets is not None:
        fmt_counts = summarize_formats(df_datasets)
        fmt_counts.to_csv(OUT_DIR / "formats_counts.csv", index=False)
        summaries["formats_counts.csv"] = fmt_counts.head(20)
        barplot(fmt_counts.head(15), x="format", y="count", title="Top Resource Formats", fname="formats_counts.png")

        api_counts = summarize_api_access(df_datasets)
        api_counts.to_csv(OUT_DIR / "api_access_counts.csv", index=False)
        summaries["api_access_counts.csv"] = api_counts
        barplot(api_counts, x="api_access", y="count", title="API Access (True/False/Unknown)", fname="api_access_counts.png", height=4, width=6)

    if df_by_provider is not None:
        top20 = top_providers(df_by_provider, n=20)
        if not top20.empty:
            top20.to_csv(OUT_DIR / "top_providers.csv", index=False)
            summaries["top_providers.csv"] = top20
            # choose name/title if present for readable labels
            name_col = "organization_title" if "organization_title" in top20.columns else (
                "organization_name" if "organization_name" in top20.columns else top20.columns[0]
            )
            plot_df = top20.copy()
            plot_df[name_col] = plot_df[name_col].astype(str).str.slice(0, 30)
            measure = "datasets_count"
            barplot(plot_df.iloc[::-1], x=measure, y=name_col, title="Top Providers by Datasets Count", fname="top_providers.png", height=8, width=10)

    # Save a quick README of outputs
    with open(OUT_DIR / "CATALOG_SUMMARY.md", "w", encoding="utf-8") as f:
        f.write("# Catalog Summary\n\n")
        for k, v in summaries.items():
            f.write(f"## {k}\n\n")
            f.write(v.to_string(index=False))
            f.write("\n\n")
        f.write("Figures saved in ./figures\n")

    print("Summary CSVs and figures written to:", OUT_DIR)


if __name__ == "__main__":
    main()

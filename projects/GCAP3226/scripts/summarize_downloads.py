from __future__ import annotations
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

BASE = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
MANIFEST = BASE / "_open_data_inventory/ckan_fetch_manifest.csv"
FIG_DIR = BASE / "_open_data_inventory/figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Configure CJK-capable font (macOS + common open fonts)
_CJK_FONT_CANDIDATES = [
    "PingFang HK", "PingFang TC", "PingFang SC",
    "Heiti TC", "Heiti SC", "Hiragino Sans GB",
    "Songti SC", "STHeiti",
    "Noto Sans CJK HK", "Noto Sans CJK TC", "Noto Sans CJK SC",
    "Source Han Sans HK", "Source Han Sans TC", "Source Han Sans SC",
    "Arial Unicode MS"
]
mpl.rcParams["font.family"] = ["sans-serif"]
mpl.rcParams["font.sans-serif"] = _CJK_FONT_CANDIDATES + mpl.rcParams.get("font.sans-serif", [])
mpl.rcParams["axes.unicode_minus"] = False


def load_manifest() -> pd.DataFrame:
    if not MANIFEST.exists():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST}")
    df = pd.read_csv(MANIFEST)
    for col in ["topic", "provider", "status", "format", "resource", "package"]:
        if col not in df.columns:
            df[col] = ""
    return df


def plot_counts(df: pd.DataFrame, by: str, title: str, fname: str, top_n: int | None = None):
    c = df[df["status"].str.lower() == "ok"].groupby(by).size().reset_index(name="count").sort_values("count", ascending=False)
    if top_n:
        c = c.head(top_n)
    plt.figure(figsize=(8, 4))
    sns.barplot(data=c, x="count", y=by, color="#4C78A8")
    plt.title(title)
    plt.tight_layout()
    out = FIG_DIR / fname
    plt.savefig(out)
    plt.close()
    print(f"Saved figure: {out}")


def main():
    df = load_manifest()
    # Topic counts
    plot_counts(df, by="topic", title="Downloads by Topic", fname="downloads_by_topic.png")
    # Provider counts (top 15)
    plot_counts(df, by="provider", title="Downloads by Provider (Top 15)", fname="downloads_by_provider_top15.png", top_n=15)
    # Package counts (top 20)
    plot_counts(df, by="package", title="Downloads by Package (Top 20)", fname="downloads_by_package_top20.png", top_n=20)

    # Quick table summaries printed to console
    ok = df[df["status"].str.lower() == "ok"]
    print("\nSummary:")
    print("Rows total:", len(df))
    print("Rows ok:", len(ok))
    print("By topic:\n", ok.groupby("topic").size().sort_values(ascending=False).to_string())


if __name__ == "__main__":
    main()

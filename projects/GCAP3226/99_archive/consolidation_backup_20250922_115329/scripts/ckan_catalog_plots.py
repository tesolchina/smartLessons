from __future__ import annotations
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

BASE = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
INV_DIR = BASE / "_open_data_inventory"
FIG_DIR = INV_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# CJK-capable font setup (macOS + common fonts)
_CJK_FONT_CANDIDATES = [
    "PingFang HK", "PingFang TC", "PingFang SC",
    "Heiti TC", "Heiti SC", "Hiragino Sans GB",
    "Songti SC", "STHeiti",
    "Noto Sans CJK HK", "Noto Sans CJK TC", "Noto Sans CJK SC",
    "Source Han Sans HK", "Source Han Sans TC", "Source Han Sans SC",
    "Arial Unicode MS",
]
mpl.rcParams["font.family"] = ["sans-serif"]
mpl.rcParams["font.sans-serif"] = _CJK_FONT_CANDIDATES + mpl.rcParams.get("font.sans-serif", [])
mpl.rcParams["axes.unicode_minus"] = False

sns.set_theme(style="whitegrid")


def _plot_top(csv_path: Path, label_col: str, title: str, out_name: str, top_n: int = 15):
    if not csv_path.exists():
        return None
    df = pd.read_csv(csv_path)
    if df.empty:
        return None
    df = df.head(top_n)
    plt.figure(figsize=(9, max(4, min(10, 0.35 * len(df) + 2))))
    sns.barplot(data=df, x="count", y=label_col, color="#4C78A8")
    plt.title(title)
    plt.tight_layout()
    out = FIG_DIR / out_name
    plt.savefig(out)
    plt.close()
    return out


def build_exec_summary(md_path: Path, total: int, org_csv: Path, fmt_csv: Path, grp_csv: Path, tag_csv: Path, lic_csv: Path,
                       org_fig: Path | None, fmt_fig: Path | None, grp_fig: Path | None, tag_fig: Path | None, lic_fig: Path | None):
    # Load top few lines for summary bullets
    def head_list(p: Path, col: str, k: int = 5) -> list[str]:
        try:
            df = pd.read_csv(p).head(k)
            return [f"{row[col]} ({int(row['count'])})" for _, row in df.iterrows()]
        except Exception:
            return []

    lines = [
        "# data.gov.hk Catalog Overview",
        "",
        f"Total datasets indexed: {total}",
        "",
        "## Executive summary",
        "",
        "- Most active organizations: " + ", ".join(head_list(org_csv, 'organization')),
        "- Most common formats: " + ", ".join(head_list(fmt_csv, 'res_format')),
        "- Top groups: " + ", ".join(head_list(grp_csv, 'groups')),
        "- Top tags: " + ", ".join(head_list(tag_csv, 'tags')),
        "- Licenses: " + ", ".join(head_list(lic_csv, 'license_id')),
        "",
        "## Visuals",
        "",
    ]

    def embed(fig: Path | None, caption: str):
        if fig and fig.exists():
            lines.append(f"### {caption}")
            lines.append("")
            rel = fig.relative_to(md_path.parent)
            lines.append(f"![{caption}]({rel.as_posix()})")
            lines.append("")

    embed(org_fig, "Top organizations")
    embed(fmt_fig, "Top resource formats")
    embed(grp_fig, "Top CKAN groups")
    embed(tag_fig, "Top tags")
    embed(lic_fig, "Top licenses")

    md_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    # Load total count from the existing overview markdown (first line has it) or recompute quickly from facets files length
    md_path = INV_DIR / "CKAN_CATALOG_OVERVIEW.md"
    # Determine total by summing any facet counts only for rough check; better to re-run API, but keep offline.
    total = None
    try:
        txt = md_path.read_text(encoding="utf-8")
        for line in txt.splitlines():
            if line.lower().startswith("total datasets indexed:"):
                total = int(line.split(":", 1)[1].strip())
                break
    except Exception:
        pass
    if total is None:
        # Fallback: can't infer safely offline; set to -1
        total = -1

    org_csv = INV_DIR / "ckan_facets_organization.csv"
    fmt_csv = INV_DIR / "ckan_facets_res_format.csv"
    grp_csv = INV_DIR / "ckan_facets_groups.csv"
    tag_csv = INV_DIR / "ckan_facets_tags.csv"
    lic_csv = INV_DIR / "ckan_facets_license_id.csv"

    org_fig = _plot_top(org_csv, "organization", "Top Organizations (by dataset count)", "top_organizations.png")
    fmt_fig = _plot_top(fmt_csv, "res_format", "Top Resource Formats", "top_formats.png")
    grp_fig = _plot_top(grp_csv, "groups", "Top CKAN Groups", "top_groups.png")
    tag_fig = _plot_top(tag_csv, "tags", "Top Tags", "top_tags.png")
    lic_fig = _plot_top(lic_csv, "license_id", "Top Licenses", "top_licenses.png")

    build_exec_summary(md_path, total, org_csv, fmt_csv, grp_csv, tag_csv, lic_csv,
                       org_fig, fmt_fig, grp_fig, tag_fig, lic_fig)
    print(f"Updated overview with charts: {md_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate core hypothesis charts from cleaned_wide.csv.

Outputs in ./figures/:
 - noise_vs_distance.png
 - eqs_vs_distance.png
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "cleaned" / "cleaned_wide.csv"
FIG_DIR = ROOT / "figures"


def scatter_with_trend(ax, x, y, *, xlabel: str, ylabel: str, title: str):
    ax.scatter(x, y, alpha=0.8)
    # trend line if sufficient points
    if len(x.dropna()) >= 2 and len(y.dropna()) >= 2:
        mask = x.notna() & y.notna()
        xp = x[mask].astype(float)
        yp = y[mask].astype(float)
        if len(xp) >= 2:
            m, b = np.polyfit(xp, yp, 1)
            xr = np.linspace(float(xp.min()), float(xp.max()), 100)
            yr = m * xr + b
            ax.plot(xr, yr, color='red', linewidth=2, label=f"trend: y={m:.2f}x+{b:.2f}")
            ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)

    # Noise vs Distance
    fig, ax = plt.subplots(figsize=(7,5))
    scatter_with_trend(
        ax,
        df["distance_m"],
        df["decibels_db"],
        xlabel="Distance from Victoria Harbour (m)",
        ylabel="Noise (dB)",
        title="Noise vs Distance"
    )
    out1 = FIG_DIR / "noise_vs_distance.png"
    fig.tight_layout()
    fig.savefig(str(out1), dpi=200)
    plt.close(fig)

    # EQS vs Distance
    fig, ax = plt.subplots(figsize=(7,5))
    scatter_with_trend(
        ax,
        df["distance_m"],
        df["eqs"],
        xlabel="Distance from Victoria Harbour (m)",
        ylabel="EQS (Environmental Quality Score)",
        title="EQS vs Distance"
    )
    out2 = FIG_DIR / "eqs_vs_distance.png"
    fig.tight_layout()
    fig.savefig(str(out2), dpi=200)
    plt.close(fig)

    # Traffic vs Distance
    if "traffic_total" in df.columns:
        fig, ax = plt.subplots(figsize=(7,5))
        scatter_with_trend(
            ax,
            df["distance_m"],
            df["traffic_total"],
            xlabel="Distance from Victoria Harbour (m)",
            ylabel="Total Traffic (2-min count)",
            title="Traffic vs Distance"
        )
        out3 = FIG_DIR / "traffic_vs_distance.png"
        fig.tight_layout()
        fig.savefig(str(out3), dpi=200)
        plt.close(fig)

    # Pedestrians vs Distance
    if "pedestrian_count" in df.columns:
        fig, ax = plt.subplots(figsize=(7,5))
        scatter_with_trend(
            ax,
            df["distance_m"],
            df["pedestrian_count"],
            xlabel="Distance from Victoria Harbour (m)",
            ylabel="Pedestrian Count (2-min)",
            title="Pedestrians vs Distance"
        )
        out4 = FIG_DIR / "pedestrians_vs_distance.png"
        fig.tight_layout()
        fig.savefig(str(out4), dpi=200)
        plt.close(fig)

    # Building Height vs EQS
    if "building_height_m" in df.columns:
        fig, ax = plt.subplots(figsize=(7,5))
        scatter_with_trend(
            ax,
            df["building_height_m"],
            df["eqs"],
            xlabel="Building Height (m)",
            ylabel="EQS",
            title="Building Height vs EQS"
        )
        out5 = FIG_DIR / "building_height_vs_eqs.png"
        fig.tight_layout()
        fig.savefig(str(out5), dpi=200)
        plt.close(fig)

    # Bar: Pedestrian Count by Site (sorted)
    if {"group", "site", "pedestrian_count"}.issubset(df.columns):
        fig, ax = plt.subplots(figsize=(8,6))
        tmp = df[["group", "site", "pedestrian_count"]].copy()
        tmp["label"] = tmp["group"].astype(str).str.replace("GROUP ", "G", regex=False) + "-" + tmp["site"].astype(str)
        tmp = tmp.sort_values("pedestrian_count", ascending=True)
        ax.barh(tmp["label"], tmp["pedestrian_count"], color="#4C78A8")
        ax.set_xlabel("Pedestrian Count (2-min)")
        ax.set_ylabel("Site")
        ax.set_title("Pedestrian Count by Site")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        out6 = FIG_DIR / "bar_pedestrians_by_site.png"
        fig.savefig(str(out6), dpi=200)
        plt.close(fig)

    # Correlation heatmap among numeric variables
    num_cols = [c for c in [
        "decibels_db","eqs","pedestrian_count","traffic_total","building_height_m","distance_m"
    ] if c in df.columns]
    if len(num_cols) >= 2:
        corr = df[num_cols].corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(6,5))
        im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_xticks(range(len(num_cols)))
        ax.set_yticks(range(len(num_cols)))
        ax.set_xticklabels(num_cols, rotation=45, ha="right")
        ax.set_yticklabels(num_cols)
        for i in range(len(num_cols)):
            for j in range(len(num_cols)):
                ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color="black")
        ax.set_title("Correlation Heatmap")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        fig.tight_layout()
        out7 = FIG_DIR / "corr_heatmap.png"
        fig.savefig(str(out7), dpi=200)
        plt.close(fig)

    print(f"Wrote {out1}")
    print(f"Wrote {out2}")
    if 'out3' in locals():
        print(f"Wrote {out3}")
    if 'out4' in locals():
        print(f"Wrote {out4}")
    if 'out5' in locals():
        print(f"Wrote {out5}")
    if 'out6' in locals():
        print(f"Wrote {out6}")
    if 'out7' in locals():
        print(f"Wrote {out7}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

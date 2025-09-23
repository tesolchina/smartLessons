from __future__ import annotations
from pathlib import Path
import re
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
DATA_ROOT = BASE / "course_materials/resources/datasets/open_data"
FIG_DIR = BASE / "_open_data_inventory/figures/auto_viz"
FIG_DIR.mkdir(parents=True, exist_ok=True)

_CJK_FONT_CANDIDATES = [
    "PingFang HK", "PingFang TC", "PingFang SC",
    "Heiti TC", "Heiti SC", "Hiragino Sans GB",
    "Songti SC", "STHeiti",
    "Noto Sans CJK HK", "Noto Sans CJK TC", "Noto Sans CJK SC",
    "Source Han Sans HK", "Source Han Sans TC", "Source Han Sans SC",
    "Arial Unicode MS"
]
# Prefer CJK-capable font; pick the first actually available on this system
mpl.rcParams["font.family"] = ["sans-serif"]
mpl.rcParams["font.sans-serif"] = _CJK_FONT_CANDIDATES + mpl.rcParams.get("font.sans-serif", [])
mpl.rcParams["axes.unicode_minus"] = False

sns.set_theme(style="whitegrid")

TIME_HINTS = ["date", "time", "timestamp", "datetime", "period", "year", "month", "day", "hour"]


def _choose_cjk_font() -> str | None:
    """Force-select a CJK-capable font that exists to avoid missing glyphs."""
    for name in _CJK_FONT_CANDIDATES:
        try:
            fp = font_manager.FontProperties(family=name)
            path = font_manager.findfont(fp, fallback_to_default=False)
            if path and Path(path).exists():
                mpl.rcParams["font.family"] = [name]
                mpl.rcParams["font.sans-serif"] = [name]
                # Also set for axes titles/labels explicitly
                mpl.rcParams["axes.titleweight"] = "regular"
                return name
        except Exception:
            continue
    return None


_selected_font = _choose_cjk_font()
if not _selected_font:
    print("Warning: No CJK font from candidates found; some glyphs may not render.")


def find_files() -> list[Path]:
    exts = (".csv", ".json", ".xls", ".xlsx")
    files: list[Path] = []
    for sub in ["transport", "air_quality", "housing"]:
        d = DATA_ROOT / sub
        if not d.exists():
            continue
        for ext in exts:
            files.extend(d.glob(f"*{ext}"))
    return sorted(files)


def read_any(path: Path, nrows: int | None = 20000) -> pd.DataFrame | None:
    try:
        if path.suffix.lower() == ".csv":
            # Try robust encoding fallbacks for HK datasets (Big5/CP950 etc.)
            encodings = [
                "utf-8",
                "utf-8-sig",
                "big5hkscs",
                "big5",
                "cp950",
                "latin1",
            ]
            last_err: Exception | None = None
            for enc in encodings:
                try:
                    return pd.read_csv(path, low_memory=False, nrows=nrows, encoding=enc)
                except Exception as e:
                    last_err = e
                    continue
            # If all fail, raise the last error to outer handler
            if last_err:
                raise last_err
        if path.suffix.lower() == ".json":
            return pd.read_json(path, lines=False)
        if path.suffix.lower() in {".xls", ".xlsx"}:
            return pd.read_excel(path, nrows=nrows)
    except Exception as e:
        print(f"Read failed: {path} -> {e}")
        return None
    return None


def guess_time_col(df: pd.DataFrame) -> str | None:
    cols = [c for c in df.columns if isinstance(c, str)]
    for c in cols:
        lc = c.lower()
        if any(h in lc for h in TIME_HINTS):
            return c
    return None


def ensure_datetime(s: pd.Series) -> pd.Series | None:
    try:
        return pd.to_datetime(s, errors="coerce")
    except Exception:
        return None


def plot_file(path: Path):
    df = read_any(path)
    if df is None or df.empty:
        return
    # pick up to 3 numeric columns
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()[:3]
    time_col = guess_time_col(df)
    figbase = FIG_DIR / f"{path.parent.name}__{path.stem}"

    def _slug(text: str, maxlen: int = 100) -> str:
        s = str(text).strip().replace("\n", " ").replace("\r", " ")
        s = s.replace("/", "-")
        s = re.sub(r"\s+", " ", s)
        # Keep common readable punctuation while avoiding path issues
        safe = []
        for ch in s:
            if ch.isalnum() or ch in "-_()[]{}.,+&%# ":
                safe.append(ch)
            else:
                safe.append("_")
        return ''.join(safe)[:maxlen].strip()

    # Histogram(s)
    if num_cols:
        for col in num_cols:
            plt.figure(figsize=(7, 4))
            sns.histplot(data=df, x=col, bins=30)
            plt.title(f"{path.stem} — {col}")
            plt.tight_layout()
            out = Path(f"{figbase}__hist__{_slug(col)}.png")
            plt.savefig(out)
            plt.close()
            print(f"Saved: {out}")

    # Time series if possible
    if time_col:
        ts = ensure_datetime(df[time_col])
        if ts is not None:
            df_ts = df.copy()
            df_ts["__time__"] = ts
            df_ts = df_ts.dropna(subset=["__time__"]).sort_values("__time__")
            if not df_ts.empty and num_cols:
                for col in num_cols:
                    plt.figure(figsize=(8, 4))
                    sns.lineplot(data=df_ts, x="__time__", y=col)
                    plt.title(f"{path.stem} — {col} over time")
                    plt.tight_layout()
                    out = Path(f"{figbase}__ts__{_slug(col)}.png")
                    plt.savefig(out)
                    plt.close()
                    print(f"Saved: {out}")


def main():
    files = find_files()
    if not files:
        print(f"No files found under {DATA_ROOT}")
        return
    print(f"Found {len(files)} files. Generating quick visuals...")
    for f in files:
        plot_file(f)


if __name__ == "__main__":
    main()

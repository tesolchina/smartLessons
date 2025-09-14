"""Starter templates for regression & simple simulations.
Run with: python scripts/regression_sim_templates.py
"""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats

BASE = Path("/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/GCAP3226")
DATA_HEALTH = BASE / "course_materials/resources/datasets/open_data/health/vaccination-rates-over-time-by-age.csv"
DATA_WATER = BASE / "course_materials/resources/datasets/open_data/water/water-quality-control-2017-2018-c.csv"


def ols_vaccination_example(path: Path = DATA_HEALTH):
    print("[OLS] Vaccination uptake example")
    if not path.exists():
        print(f"  Data not found: {path}\n  Tip: download the CSV to this path or update the path.")
        return
    df = pd.read_csv(path)
    # Minimal cleaning: infer date and compute daily change if counts present
    date_col = None
    for c in df.columns:
        if "date" in c.lower() or "day" in c.lower():
            date_col = c
            break
    if date_col:
        df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    # Guess target and features
    y_col = None
    for c in df.columns:
        if any(k in c.lower() for k in ["rate", "uptake", "dose"]):
            y_col = c
            break
    if y_col is None:
        print("  Could not identify a target column with 'rate/uptake/dose' in name.")
        return
    # Simple encoding for age_group if present
    X_cols = []
    if "age_group" in df.columns:
        dummies = pd.get_dummies(df["age_group"], prefix="age", drop_first=True)
        X = dummies
        X_cols = list(X.columns)
    else:
        # fallback: just intercept
        X = pd.DataFrame(index=df.index)
    X = sm.add_constant(X)
    y = df[y_col].astype(float)
    model = sm.OLS(y, X, missing="drop").fit()
    print(model.summary())
    # What-if: shift older age group share by +5% (if dummy exists)
    if any(col.startswith("age_") for col in X_cols):
        scenario = X.mean().to_frame().T
        for col in X_cols:
            scenario[col] = (scenario[col] + 0.05).clip(upper=1.0)
        pred = model.get_prediction(scenario)
        print("  Scenario predicted uptake:", float(pred.predicted_mean))


def poisson_water_example(path: Path = DATA_WATER):
    print("[GLM-Poisson] Water quality count example")
    if not path.exists():
        print(f"  Data not found: {path}\n  Tip: download the CSV to this path or update the path.")
        return
    df = pd.read_csv(path)
    # Guess a count column (e.g., ecoli)
    y_col = None
    for c in df.columns:
        cl = c.lower()
        if any(k in cl for k in ["ecoli", "count", "cases"]):
            y_col = c
            break
    if y_col is None:
        print("  Could not identify a count-like target column (ecoli/count/cases).")
        return
    # Simple district dummy encoding if present
    X = pd.DataFrame(index=df.index)
    if "district" in [c.lower() for c in df.columns]:
        # find original name case
        dcol = [c for c in df.columns if c.lower() == "district"][0]
        X = pd.get_dummies(df[dcol], prefix="dist", drop_first=True)
    X = sm.add_constant(X)
    y = df[y_col].astype(float)
    model = sm.GLM(y, X, family=sm.families.Poisson(), missing="drop").fit()
    print(model.summary())


def simple_monte_carlo():
    print("[Simulation] Simple Monte Carlo: queue waiting time")
    # M/M/1 style toy queue simulation to illustrate policy what-if
    lam = 0.8  # arrival rate
    mu = 1.0   # service rate
    runs = 10000
    waits = []
    for _ in range(runs):
        inter_arrival = np.random.exponential(1/lam)
        service = np.random.exponential(1/mu)
        wait = max(0.0, service - inter_arrival)
        waits.append(wait)
    print(f"  Mean wait: {np.mean(waits):.3f}, 95% CI: [{np.percentile(waits, 2.5):.3f}, {np.percentile(waits, 97.5):.3f}]")


if __name__ == "__main__":
    ols_vaccination_example()
    poisson_water_example()
    simple_monte_carlo()

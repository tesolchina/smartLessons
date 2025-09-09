#!/usr/bin/env python3
"""Generate additional chart types for Donald's Geography project.

Creates polynomial curves, multi-variable charts, and advanced visualizations.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "cleaned" / "cleaned_wide.csv"
FIG_DIR = ROOT / "figures"


def scatter_with_polynomial_trend(ax, x, y, *, xlabel: str, ylabel: str, title: str, degree=2):
    """Create scatter plot with both linear and polynomial trend lines."""
    ax.scatter(x, y, alpha=0.7, s=60, color='steelblue', edgecolor='white', linewidth=0.5)
    
    # Remove NaN values
    mask = x.notna() & y.notna()
    xp = x[mask].astype(float)
    yp = y[mask].astype(float)
    
    if len(xp) >= 3:
        # Linear trend
        m, b = np.polyfit(xp, yp, 1)
        xr = np.linspace(float(xp.min()), float(xp.max()), 100)
        yr_linear = m * xr + b
        ax.plot(xr, yr_linear, color='red', linewidth=2, linestyle='--', 
                label=f"Linear: y={m:.3f}x+{b:.1f}")
        
        # Polynomial trend
        if degree >= 2:
            poly_coeffs = np.polyfit(xp, yp, degree)
            yr_poly = np.polyval(poly_coeffs, xr)
            ax.plot(xr, yr_poly, color='darkred', linewidth=3, 
                    label=f"Polynomial (degree {degree})")
        
        # R-squared for linear
        try:
            r_val = np.corrcoef(xp, yp)[0, 1]
            r_squared = r_val ** 2
            ax.text(0.05, 0.95, f'R² = {r_squared:.3f}', transform=ax.transAxes, 
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        except:
            pass
        
        ax.legend()
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)


def create_multi_variable_chart(df, fig_path):
    """Create a chart showing multiple variables vs distance in subplots."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    variables = [
        ('decibels_db', 'Noise (dB)', 'Noise vs Distance'),
        ('eqs', 'EQS Score', 'Environmental Quality vs Distance'),
        ('traffic_total', 'Traffic Count', 'Traffic vs Distance'),
        ('pedestrian_count', 'Pedestrian Count', 'Pedestrians vs Distance')
    ]
    
    for i, (var, ylabel, title) in enumerate(variables):
        if var in df.columns:
            ax = axes[i//2, i%2]
            scatter_with_polynomial_trend(
                ax, df['distance_m'], df[var],
                xlabel='Distance from Victoria Harbour (m)',
                ylabel=ylabel,
                title=title
            )
    
    plt.tight_layout()
    fig.savefig(str(fig_path), dpi=200, bbox_inches='tight')
    plt.close(fig)


def create_grouped_analysis(df, fig_path):
    """Create charts showing patterns by group."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Group average distances
    group_stats = df.groupby('group').agg({
        'distance_m': 'mean',
        'decibels_db': 'mean',
        'eqs': 'mean',
        'traffic_total': 'mean'
    }).reset_index()
    
    # Chart 1: Distance by Group
    ax1 = axes[0, 0]
    group_labels = group_stats['group'].str.replace('Group ', 'G')
    ax1.bar(group_labels, group_stats['distance_m'], color='lightcoral', alpha=0.7)
    ax1.set_title('Average Distance by Group')
    ax1.set_ylabel('Distance (m)')
    ax1.tick_params(axis='x', rotation=45)
    
    # Chart 2: Noise by Group
    ax2 = axes[0, 1]
    ax2.bar(group_labels, group_stats['decibels_db'], color='lightblue', alpha=0.7)
    ax2.set_title('Average Noise by Group')
    ax2.set_ylabel('Noise (dB)')
    ax2.tick_params(axis='x', rotation=45)
    
    # Chart 3: EQS by Group
    ax3 = axes[1, 0]
    colors = ['green' if x > 0 else 'red' for x in group_stats['eqs']]
    ax3.bar(group_labels, group_stats['eqs'], color=colors, alpha=0.7)
    ax3.set_title('Average EQS by Group')
    ax3.set_ylabel('EQS Score')
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax3.tick_params(axis='x', rotation=45)
    
    # Chart 4: Traffic by Group
    ax4 = axes[1, 1]
    ax4.bar(group_labels, group_stats['traffic_total'], color='orange', alpha=0.7)
    ax4.set_title('Average Traffic by Group')
    ax4.set_ylabel('Traffic Count')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    fig.savefig(str(fig_path), dpi=200, bbox_inches='tight')
    plt.close(fig)


def create_distance_zones_analysis(df, fig_path):
    """Create analysis based on distance zones (near, medium, far from harbour)."""
    # Create distance zones
    df_copy = df.copy()
    df_copy['distance_zone'] = pd.cut(df_copy['distance_m'], 
                                     bins=[0, 500, 1000, float('inf')], 
                                     labels=['Near (0-500m)', 'Medium (500-1000m)', 'Far (>1000m)'])
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Box plots for each variable by zone
    variables = [
        ('decibels_db', 'Noise (dB)'),
        ('eqs', 'EQS Score'),
        ('traffic_total', 'Traffic Count'),
        ('pedestrian_count', 'Pedestrian Count')
    ]
    
    for i, (var, ylabel) in enumerate(variables):
        if var in df_copy.columns:
            ax = axes[i//2, i%2]
            zone_data = [df_copy[df_copy['distance_zone'] == zone][var].dropna() 
                        for zone in df_copy['distance_zone'].cat.categories]
            
            bp = ax.boxplot(zone_data, labels=df_copy['distance_zone'].cat.categories, 
                           patch_artist=True, notch=True)
            
            # Color the boxes
            colors = ['lightcoral', 'lightblue', 'lightgreen']
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            ax.set_title(f'{ylabel} by Distance Zone')
            ax.set_ylabel(ylabel)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig.savefig(str(fig_path), dpi=200, bbox_inches='tight')
    plt.close(fig)


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    
    # 1. Multi-variable chart with polynomial curves
    multi_var_path = FIG_DIR / "multi_variable_polynomial.png"
    create_multi_variable_chart(df, multi_var_path)
    print(f"Wrote {multi_var_path}")
    
    # 2. Grouped analysis
    grouped_path = FIG_DIR / "grouped_analysis.png"
    create_grouped_analysis(df, grouped_path)
    print(f"Wrote {grouped_path}")
    
    # 3. Distance zones analysis
    zones_path = FIG_DIR / "distance_zones_analysis.png"
    create_distance_zones_analysis(df, zones_path)
    print(f"Wrote {zones_path}")
    
    # 4. Individual polynomial curves for key hypotheses
    for var, name in [('decibels_db', 'noise'), ('eqs', 'eqs')]:
        if var in df.columns:
            fig, ax = plt.subplots(figsize=(8, 6))
            scatter_with_polynomial_trend(
                ax, df['distance_m'], df[var],
                xlabel='Distance from Victoria Harbour (m)',
                ylabel=name.upper() if var == 'eqs' else 'Noise (dB)',
                title=f'{name.title()} vs Distance (Linear + Polynomial Trends)',
                degree=2
            )
            poly_path = FIG_DIR / f"{name}_vs_distance_polynomial.png"
            fig.tight_layout()
            fig.savefig(str(poly_path), dpi=200, bbox_inches='tight')
            plt.close(fig)
            print(f"Wrote {poly_path}")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

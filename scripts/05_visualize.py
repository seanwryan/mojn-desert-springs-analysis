#!/usr/bin/env python3
"""
05_visualize.py

Generate static visualizations:
 1. Time series of annual conductivity for a selected spring
 2. Distribution of pH across springs in the most recent year
 3. Bar chart of how many springs show each ecological flag
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# --- PATH SETUP ---
BASE_DIR     = os.path.dirname(__file__)
ROOT_DIR     = os.path.join(BASE_DIR, '..')
TABLE_DIR    = os.path.join(ROOT_DIR, 'output', 'tables')
PLOT_DIR     = os.path.join(ROOT_DIR, 'output', 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)

def plot_conductivity_timeseries(site_code):
    df = pd.read_csv(os.path.join(TABLE_DIR, 'summary_annual_water_quality.csv'))
    sub = df[df['SiteCode'] == site_code].dropna(subset=['conductivity'])
    if sub.empty:
        print(f"No conductivity data found for {site_code}")
        return
    plt.figure()
    plt.plot(sub['Year'], sub['conductivity'], marker='o')
    plt.title(f"Annual Conductivity at {site_code}")
    plt.xlabel("Year")
    plt.ylabel("Specific Conductance (µS/cm)")
    plt.tight_layout()
    out = os.path.join(PLOT_DIR, f"conductivity_timeseries_{site_code}.png")
    plt.savefig(out)
    plt.close()
    print(f"Saved plot: {out}")

def plot_ph_distribution(latest_year):
    df = pd.read_csv(os.path.join(TABLE_DIR, 'summary_annual_water_quality.csv'))
    sub = df[df['Year'] == latest_year].dropna(subset=['pH'])
    if sub.empty:
        print(f"No pH data for {latest_year}")
        return
    plt.figure()
    plt.hist(sub['pH'], bins=15)
    plt.title(f"pH Distribution Across Springs in {latest_year}")
    plt.xlabel("pH")
    plt.ylabel("Count of Springs")
    plt.tight_layout()
    out = os.path.join(PLOT_DIR, f"ph_distribution_{latest_year}.png")
    plt.savefig(out)
    plt.close()
    print(f"Saved plot: {out}")

def plot_ecology_flags():
    eco = pd.read_csv(os.path.join(TABLE_DIR, 'ecology_site_summary.csv'))
    # Sum across all springs
    sums = {
        'Vegetation': eco['vegetation_present'].sum(),
        'Invasives':  eco['invasives_present'].sum(),
        'Disturbance':eco['disturbance_present'].sum(),
        'Wildlife':   eco['wildlife_present'].sum(),
        'Modifications':eco['flow_modification_present'].sum()
    }
    labels = list(sums.keys())
    values = list(sums.values())
    
    plt.figure()
    plt.bar(labels, values)
    plt.title("Number of Springs with Ecological Flags")
    plt.ylabel("Number of Springs")
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    out = os.path.join(PLOT_DIR, "ecology_flags_summary.png")
    plt.savefig(out)
    plt.close()
    print(f"Saved plot: {out}")

def main():
    # Example: plot conductivity for a representative spring
    plot_conductivity_timeseries("DEVA_P_BEN0606")
    
    # Plot pH distribution in the most recent year
    # determine latest year from data
    df = pd.read_csv(os.path.join(TABLE_DIR, 'summary_annual_water_quality.csv'))
    latest = int(df['Year'].max())
    plot_ph_distribution(latest)
    
    # Plot ecology flags summary
    plot_ecology_flags()

if __name__ == '__main__':
    main()
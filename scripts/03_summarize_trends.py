#!/usr/bin/env python3
"""
03_summarize_trends.py

Compute annual means and test temporal trends for key water-quality parameters
in the Mojave Desert Springs combined observations.

Produces:
 - output/tables/summary_annual_water_quality.csv
 - output/tables/trend_results.csv
"""

import os
import pandas as pd
import numpy as np
from scipy.stats import linregress

# --- PATH SETUP ---
BASE_DIR    = os.path.dirname(__file__)
ROOT_DIR    = os.path.join(BASE_DIR, '..')
COMBINED    = os.path.join(ROOT_DIR, 'output', 'tables', 'combined_observations.csv')
OUT_DIR     = os.path.join(ROOT_DIR, 'output', 'tables')
os.makedirs(OUT_DIR, exist_ok=True)

# --- PARAMETERS TO AGGREGATE & TEST ---
PARAMS = {
    'SpecificConductance_microS_per_cm': 'conductivity',
    'pH':                             'pH',
    'WaterTemperature_C':             'temperature',
    'DissolvedOxygen_mg_per_L':       'dissolved_oxygen'
}

def compute_annual_means(df):
    """ Add 'Year' column and compute per-site, per-year mean for each PARAMS key. """
    df['Year'] = df['VisitDate'].dt.year
    agg = df.groupby(['SiteCode', 'Year'])[list(PARAMS.keys())] \
            .mean() \
            .reset_index() \
            .rename(columns=PARAMS)
    return agg

def test_trends(annual_df):
    """
    For each SiteCode and each parameter, run a linear regression of value ~ Year.
    Returns a DataFrame: SiteCode, param, slope, pvalue.
    """
    records = []
    for site, group in annual_df.groupby('SiteCode'):
        years = group['Year'].values
        for col, short in PARAMS.items():
            vals = group[short].values
            # only test if at least 3 years of data
            if len(years) >= 3 and not np.isnan(vals).all():
                # drop NaN pairs
                mask = ~np.isnan(vals)
                yrs = years[mask]
                vls = vals[mask]
                if len(yrs) >= 3:
                    lr = linregress(yrs, vls)
                    records.append({
                        'SiteCode': site,
                        'parameter': short,
                        'slope_per_year': lr.slope,
                        'p_value': lr.pvalue,
                        'r_value': lr.rvalue
                    })
    return pd.DataFrame.from_records(records)

def main():
    print("Loading combined observations…")
    df = pd.read_csv(COMBINED, parse_dates=['VisitDate'])
    
    print("Computing annual means…")
    annual = compute_annual_means(df)
    out_annual = os.path.join(OUT_DIR, 'summary_annual_water_quality.csv')
    annual.to_csv(out_annual, index=False)
    print(f"→ Wrote annual means to {out_annual} ({len(annual):,} rows)")

    print("Running trend tests…")
    trends = test_trends(annual)
    out_trends = os.path.join(OUT_DIR, 'trend_results.csv')
    trends.to_csv(out_trends, index=False)
    print(f"→ Wrote trend results to {out_trends} ({len(trends):,} tests)")

if __name__ == '__main__':
    main()
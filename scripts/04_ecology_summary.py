#!/usr/bin/env python3
"""
04_ecology_summary.py

Summarize ecological observations at each spring:
 - Vegetation presence (count of visits with vegetation observed)
 - Invasive plant presence (count of visits with invasives)
 - Disturbance presence (count of visits with any disturbance)
 - Wildlife evidence (count of visits with wildlife observed)
 - Flow modifications (count of visits with modifications)

Produces:
 - output/tables/ecology_site_summary.csv
"""

import os
import pandas as pd

# --- PATH SETUP ---
BASE_DIR    = os.path.dirname(__file__)
ROOT_DIR    = os.path.join(BASE_DIR, '..')
CLEAN_DIR   = os.path.join(ROOT_DIR, 'output', 'cleaned')
OUT_DIR     = os.path.join(ROOT_DIR, 'output', 'tables')
os.makedirs(OUT_DIR, exist_ok=True)

def load_clean(name, usecols, parse_dates=None):
    path = os.path.join(CLEAN_DIR, f"{name}_cleaned.csv")
    return pd.read_csv(path, usecols=usecols, parse_dates=parse_dates or [])

def main():
    # Load visits baseline
    visits = load_clean('Visits',
                        usecols=['SiteCode','VisitDate'])
    
    # Vegetation: count visits where IsVegetationObserved == 'Y'
    veg = load_clean('Vegetation',
                     usecols=['SiteCode','VisitDate','IsVegetationObserved'],
                     parse_dates=['VisitDate'])
    veg['veg_flag'] = veg['IsVegetationObserved'].eq('Y').astype(int)
    veg_sum = veg.groupby('SiteCode')['veg_flag'].max().rename('vegetation_present')
    
    # Invasives: count visits with any invasive observation
    inv = load_clean('Invasive',
                     usecols=['SiteCode','VisitDate','USDAPlantsCode'],
                     parse_dates=['VisitDate'])
    inv['inv_flag'] = inv['USDAPlantsCode'].notna().astype(int)
    inv_sum = inv.groupby('SiteCode')['inv_flag'].max().rename('invasives_present')
    
    # Disturbance: count visits where Overall != '0' or 'None'
    dist = load_clean('Disturb',
                      usecols=['SiteCode','VisitDate','Overall'],
                      parse_dates=['VisitDate'])
    dist['dist_flag'] = dist['Overall'].replace({'0':None,'None':None}).notna().astype(int)
    dist_sum = dist.groupby('SiteCode')['dist_flag'].max().rename('disturbance_present')
    
    # Wildlife: IsWildlifeObserved == 'Yes' or 'Y'
    wild = load_clean('Wildlife',
                      usecols=['SiteCode','VisitDate','IsWildlifeObserved'],
                      parse_dates=['VisitDate'])
    wild['wild_flag'] = wild['IsWildlifeObserved'].str.upper().eq('YES').astype(int)
    wild_sum = wild.groupby('SiteCode')['wild_flag'].max().rename('wildlife_present')
    
    # Flow modifications: FlowModificationStatus contains 'Yes'
    fm = load_clean('FlowMod',
                    usecols=['SiteCode','VisitDate','FlowModificationStatus'],
                    parse_dates=['VisitDate'])
    fm['fm_flag'] = fm['FlowModificationStatus'].str.upper().str.contains('YES').fillna(False).astype(int)
    fm_sum = fm.groupby('SiteCode')['fm_flag'].max().rename('flow_modification_present')
    
    # Combine all summaries into one table
    summary = pd.concat([
        veg_sum, inv_sum, dist_sum, wild_sum, fm_sum
    ], axis=1).fillna(0).astype(int).reset_index()
    
    # Write to CSV
    out_path = os.path.join(OUT_DIR, 'ecology_site_summary.csv')
    summary.to_csv(out_path, index=False)
    print(f"Ecology summary written to {out_path}")
    print(summary.head())

if __name__ == '__main__':
    main()
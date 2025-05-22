#!/usr/bin/env python3
"""
02_merge_observations.py

Merge cleaned Mojave Desert Springs tables into one combined observations table.
Joins on SiteCode and VisitDate.
Writes combined CSV to output/tables/combined_observations.csv
"""

import os
import pandas as pd

# --- PATH SETUP ---
BASE_DIR    = os.path.dirname(__file__)
ROOT_DIR    = os.path.join(BASE_DIR, '..')
CLEAN_DIR   = os.path.join(ROOT_DIR, 'output', 'cleaned')
OUT_DIR     = os.path.join(ROOT_DIR, 'output', 'tables')
os.makedirs(OUT_DIR, exist_ok=True)

# --- LOAD FUNCTION ---
def load_table(name, cols=None, parse_dates=None):
    """
    Load a cleaned CSV by name (without _cleaned.csv suffix).
    Optionally select a subset of columns and parse date columns.
    """
    path = os.path.join(CLEAN_DIR, f"{name}_cleaned.csv")
    df = pd.read_csv(path,
                     usecols=cols if cols else None,
                     parse_dates=parse_dates or [])
    print(f"Loaded {name}: {len(df):,} rows, cols={list(df.columns)}")
    return df

def main():
    # 1) Load visits (base for merge)
    visits = load_table(
        'Visits',
        cols=['SiteCode', 'VisitDate', 'MonitoringStatus', 'SpringType', 'DPL'],
        parse_dates=['VisitDate']
    )

    # 2) Load site metadata (for coordinates)
    sites = load_table(
        'Sites',
        cols=['SiteCode', 'Lat_WGS84', 'Lon_WGS84']
    )

    # Merge visits + sites
    df = visits.merge(sites, on='SiteCode', how='left')

    # 3) Water quality measurements
    wq_spcond = load_table(
        'SpCond',
        cols=['SiteCode', 'VisitDate', 'SpecificConductance_microS_per_cm'],
        parse_dates=['VisitDate']
    )
    wq_ph = load_table(
        'pH',
        cols=['SiteCode', 'VisitDate', 'pH'],
        parse_dates=['VisitDate']
    )
    wq_temp = load_table(
        'Temp',
        cols=['SiteCode', 'VisitDate', 'WaterTemperature_C'],
        parse_dates=['VisitDate']
    )
    wq_do = load_table(
        'DO',
        cols=['SiteCode', 'VisitDate', 'DissolvedOxygen_mg_per_L'],
        parse_dates=['VisitDate']
    )

    # 4) Discharge measurements
    dis_vol = load_table(
        'DischVol',
        cols=['SiteCode', 'VisitDate', 'ContainerVolume_mL', 'FillTime_seconds'],
        parse_dates=['VisitDate']
    )
    dis_est = load_table(
        'DischEst',
        cols=['SiteCode', 'VisitDate', 'DischargeClass_L_per_s'],
        parse_dates=['VisitDate']
    )
    flow_cond = load_table(
        'FlowCond',
        cols=['SiteCode', 'VisitDate', 'FlowCondition'],
        parse_dates=['VisitDate']
    )

    # 5) Ecological disturbance/modification (optional in combined)
    flow_mod = load_table(
        'FlowMod',
        cols=['SiteCode', 'VisitDate', 'FlowModificationStatus', 'ModificationType'],
        parse_dates=['VisitDate']
    )

    # Sequentially merge all tables on SiteCode & VisitDate
    for tbl in (wq_spcond, wq_ph, wq_temp, wq_do, dis_vol, dis_est, flow_cond, flow_mod):
        df = df.merge(tbl, on=['SiteCode', 'VisitDate'], how='left')

    # 6) Write combined table
    out_path = os.path.join(OUT_DIR, 'combined_observations.csv')
    df.to_csv(out_path, index=False)
    print(f"\nCombined observations written to: {out_path}")
    print(f"Rows: {len(df):,} | Columns: {df.shape[1]}")

if __name__ == '__main__':
    main()
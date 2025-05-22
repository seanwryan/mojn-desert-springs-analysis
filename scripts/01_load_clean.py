#!/usr/bin/env python3
"""
01_load_clean.py

Load and clean all Mojave Desert Springs raw CSVs.
Writes cleaned tables to output/cleaned/.
"""

import os
import pandas as pd

# --- PATH SETUP ---
BASE_DIR     = os.path.dirname(__file__)            # scripts/
ROOT_DIR     = os.path.join(BASE_DIR, '..')         # project root
DATA_DIR     = os.path.join(ROOT_DIR, 'data')
CLEAN_DIR    = os.path.join(ROOT_DIR, 'output', 'cleaned')
os.makedirs(CLEAN_DIR, exist_ok=True)

# --- FILE NAMES & DATE COLUMNS ---
tables = {
    'Sites':        {'file': 'Sites.csv',               'date_cols': []},
    'Visits':       {'file': 'Visits.csv',              'date_cols': ['VisitDate']},
    'SpCond':       {'file': 'WaterQualitySpCond.csv',  'date_cols': ['Date']},
    'pH':           {'file': 'WaterQualitypH.csv',      'date_cols': ['Date']},
    'Temp':         {'file': 'WaterQualityTemperature.csv', 'date_cols': ['Date']},
    'DO':           {'file': 'WaterQualityDO.csv',      'date_cols': ['Date']},
    'DischVol':     {'file': 'DischargeVolumetric.csv', 'date_cols': ['Date']},
    'DischEst':     {'file': 'DischargeEstimated.csv',  'date_cols': ['Date']},
    'FlowCond':     {'file': 'DischargeFlowCondition.csv', 'date_cols': ['Date']},
    'Vegetation':   {'file': 'Vegetation.csv',          'date_cols': ['Date']},
    'Invasive':     {'file': 'InvasivePlants.csv',      'date_cols': ['Date']},
    'Disturb':      {'file': 'Disturbance.csv',         'date_cols': ['Date']},
    'FlowMod':      {'file': 'DisturbanceFlowModification.csv', 'date_cols': ['Date']},
    'Wildlife':     {'file': 'Wildlife.csv',            'date_cols': ['Date']}
}

# --- STANDARD SPRING ID COLUMN NAME ---
SPRING_ID_COL = 'SPRING_ID'  # adjust if the raw CSVs use a different name

def clean_table(name, cfg):
    in_path = os.path.join(DATA_DIR, cfg['file'])
    print(f"Loading {name} from {cfg['file']}...")
    df = pd.read_csv(in_path, dtype=str)
    
    # 1) Standardize SPRING_ID column name
    #    We'll assume raw uses either 'SiteID' or 'SpringID', so rename if present
    for raw in ['SiteID', 'SpringID', 'site_id', 'spring_id']:
        if raw in df.columns:
            df = df.rename(columns={raw: SPRING_ID_COL})
            break
    
    # 2) Parse date columns
    for col in cfg['date_cols']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # 3) Drop rows missing core measurement
    core_cols = [c for c in df.columns if c not in [SPRING_ID_COL] + cfg['date_cols']]
    # identify measurement column: the first numeric column beyond dates & ID
    meas_cols = df.select_dtypes(include='number').columns.tolist()
    if meas_cols:
        core = meas_cols[0]
        df = df.dropna(subset=[core])
    
    # 4) Save cleaned CSV
    out_file = os.path.join(CLEAN_DIR, f"{name}_cleaned.csv")
    df.to_csv(out_file, index=False)
    print(f"→ cleaned {name} → {out_file} ({len(df):,} rows)")

def main():
    for name, cfg in tables.items():
        clean_table(name, cfg)
    print("All tables loaded and cleaned.")

if __name__ == '__main__':
    main()
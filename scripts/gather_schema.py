#!/usr/bin/env python3
"""
gather_schema.py

Lists every cleaned CSV in output/cleaned/, prints out:
 • Filename
 • Columns (comma-separated)
 • Whether it contains 'SiteCode' or 'VisitDate'
 • Any other date-like columns
"""

import os
import pandas as pd

CLEAN_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'cleaned')

def is_date_col(col):
    name = col.lower()
    return 'date' in name or 'time' in name

def main():
    for fname in sorted(os.listdir(CLEAN_DIR)):
        if fname.endswith('_cleaned.csv'):
            path = os.path.join(CLEAN_DIR, fname)
            df = pd.read_csv(path, nrows=0)  # only need header
            cols = df.columns.tolist()
            has_site = 'SiteCode' in cols
            has_visit = 'VisitDate' in cols
            date_cols = [c for c in cols if is_date_col(c)]
            print(f"\n=== {fname} ===")
            print("Columns:")
            print("  " + ", ".join(cols))
            print(f"Contains SiteCode?   {'Yes' if has_site else 'No'}")
            print(f"Contains VisitDate?  {'Yes' if has_visit else 'No'}")
            if date_cols:
                print("Date-like columns:  " + ", ".join(date_cols))
            else:
                print("Date-like columns:  None")
    print("\nSchema gathering complete.")
    
if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
inspect_cleaned.py

Quickly inspect each cleaned CSV in output/cleaned/:
- Print file name
- Row count
- Column names and dtypes
- First 5 rows
"""

import os
import pandas as pd

CLEAN_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'cleaned')

def inspect_file(path):
    # Count rows (excluding header)
    with open(path, 'r') as f:
        row_count = sum(1 for _ in f) - 1

    # Read first 5 rows to inspect structure
    df_head = pd.read_csv(path, nrows=5)
    
    print(f"\n=== {os.path.basename(path)} ===")
    print(f"Rows: {row_count}")
    print(f"Columns ({len(df_head.columns)}):")
    for col, dtype in df_head.dtypes.items():
        print(f"  - {col}: {dtype}")
    print("\nFirst 5 rows:")
    print(df_head.to_string(index=False))
    print("\n" + "-"*60)

def main():
    for fname in sorted(os.listdir(CLEAN_DIR)):
        if fname.endswith('_cleaned.csv'):
            inspect_file(os.path.join(CLEAN_DIR, fname))

if __name__ == '__main__':
    main()
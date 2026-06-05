"""
Sample Data Extraction Utility
Code Authorship: Khang D. Nguyen
Description: Extracts a full 1-year continuous operational window (2020) 
             from the proprietary dataset to serve as the public CI/CD sample.
             A minimum of 1 year is strictly required to successfully execute 
             the macroscopic LOESS filters (w_354 = 91 and w_trend = 4381).
"""

import pandas as pd
import os

# 1. Define paths
FULL_DATA_PATH = "data/raw/raw_xuanhoa_2019_2024.csv"
SAMPLE_DATA_PATH = "data/sample/raw_sample.csv"

print(f"[INFO] Loading proprietary dataset...")
df_full = pd.read_csv(FULL_DATA_PATH, index_col="Date", parse_dates=True)

# 2. Extract exactly 1 year (2020-01-01 to 2020-12-31)
print(f"[PROCESS] Slicing 1-year operational window (2020-01-01 to 2020-12-31)...")
df_sample = df_full.loc['2020-01-01':'2020-12-31'].copy()

# 3. Export to the sample directory
os.makedirs(os.path.dirname(SAMPLE_DATA_PATH), exist_ok=True)
df_sample.to_csv(SAMPLE_DATA_PATH)

print(f"[SUCCESS] Public 1-year CI/CD sample created at: {SAMPLE_DATA_PATH}")
print(f"[INFO] Sample shape: {df_sample.shape}")
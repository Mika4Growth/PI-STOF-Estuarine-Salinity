"""
Data Preprocessing Pipeline for PI-STOF
Code Authorship: Khang D. Nguyen
Description: Implements a physically constrained hybrid imputation schema 
             (Linear and PCHIP) to resolve missing estuarine hydrodynamic data 
             without inducing spectral leakage or phase shifts.
"""

import pandas as pd
import numpy as np
import argparse
import os

def smart_impute(series, threshold=5):
    """
    Hybrid imputation based on gap size to preserve estuarine physical anomalies.
    - Linear interpolation for gaps <= threshold (preserves local gradients).
    - PCHIP interpolation for gaps > threshold (preserves monotonicity and High-High Water peaks).
    - limit_area='inside' prevents artificial extrapolation at the boundaries.
    
    Args:
        series (pd.Series): The time-series column with missing values.
        threshold (int): Maximum consecutive NaN count to use Linear instead of PCHIP.
        
    Returns:
        pd.Series: The imputed time-series.
    """
    # 1. Identify NaN blocks and calculate their lengths
    is_nan = series.isna()
    
    # Tag consecutive NaN blocks with a unique ID
    block_id = (is_nan != is_nan.shift()).cumsum()
    
    # Calculate the total length of each block
    block_lengths = is_nan.groupby(block_id).transform('sum')
    
    # 2. Create boolean masks for short vs. long gaps
    short_gap_mask = is_nan & (block_lengths <= threshold)
    long_gap_mask = is_nan & (block_lengths > threshold)
    
    # 3. Execute interpolations
    series_linear = series.interpolate(method='linear', limit_area='inside')
    series_pchip = series.interpolate(method='pchip', limit_area='inside')
    
    series_imputed = series.copy()
    
    # Apply the correct interpolation method based on the gap size masks
    series_imputed[short_gap_mask] = series_linear[short_gap_mask]
    series_imputed[long_gap_mask] = series_pchip[long_gap_mask]
    
    return series_imputed

def main(input_path, output_path):
    print(f"[INFO] Initiating data preprocessing pipeline...")
    print(f"[INFO] Reading raw data from: {input_path}")
    
    # Read CSV and enforce DatetimeIndex
    df = pd.read_csv(input_path, index_col="Date", parse_dates=True)
    
    print("\n--- MISSING VALUES (BEFORE IMPUTATION) ---")
    print(df.isna().sum())

    # Define target columns representing estuarine dynamics
    target_columns = ['Zxuanhoa', 'Sxuanhoa']
    
    for col in target_columns:
        if col in df.columns:
            print(f"[PROCESS] Executing hybrid imputation for {col}...")
            df[col] = smart_impute(df[col], threshold=5)
            
    # Resolve any remaining boundary NaNs via backward and forward filling
    df = df.bfill().ffill()

    print("\n--- MISSING VALUES (AFTER IMPUTATION) ---")
    print(df.isna().sum())

    # Isolate the operational timeframe (2019 onwards) to ensure data validity
    print("\n[PROCESS] Truncating dataset to the operational timeframe (>= 2019-01-01)...")
    df = df.sort_index() 
    df_experiment = df.loc['2019-01-01':].copy()

    print(f"[SUCCESS] Pre-2019 noise successfully removed.")
    print(f"[SUCCESS] Final processed tensor shape: {df_experiment.shape}")
    
    if not df_experiment.empty:
        start_date = df_experiment.index.min().strftime('%Y-%m-%d')
        end_date = df_experiment.index.max().strftime('%Y-%m-%d')
        print(f"[INFO] Operational sequence validated from {start_date} to {end_date}")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Export the final processed dataframe
    df_experiment.to_csv(output_path)
    print(f"\n[SUCCESS] Artifact generated: Processed data saved at {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PI-STOF Data Preprocessing Pipeline")
    parser.add_argument("--input", type=str, required=True, help="Path to the raw CSV input file")
    parser.add_argument("--output", type=str, required=True, help="Path to save the processed CSV output file")
    
    args = parser.parse_args()
    main(args.input, args.output)
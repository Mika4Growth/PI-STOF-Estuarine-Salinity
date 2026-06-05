"""
PI-STOF Multi-Objective Optimization Engine
Code Authorship: Khang D. Nguyen
Description: Implements the Physics-Informed Spectral-Temporal Optimization Framework.
             Executes the PGML grid search to map celestial mechanics into the MSTL 
             hyperparameter space by computing spectral leakage (FFT/PSD), absolute 
             time-domain orthogonality, and low-frequency base-flow inertia.
"""

import numpy as np
import pandas as pd
from scipy import signal
from scipy.stats import pearsonr
import argparse
import os
import itertools

import src.config as cfg
from src.mstl_decomposition import execute_physics_mstl

def calculate_psd(series: pd.Series) -> tuple:
    """
    Computes the Power Spectral Density (PSD) of a given time-series.
    Assumes a 1-hour sampling frequency (fs = 1.0 h^-1) based on the preprocessing grid.
    """
    clean_series = series.dropna().values
    # Periodogram is strictly utilized for exact spectral matching in deterministic tidal signals
    f, Pxx = signal.periodogram(clean_series, fs=1.0, scaling='density')
    return f, Pxx

def calc_leakage_penalty(s_354: pd.Series) -> float:
    """
    L_Leakage (Eq. 5): Quantifies the high-frequency diurnal kinetic energy (25h) 
    physically violating the macro-scale Spring-Neap amplitude envelope (354h).
    """
    f, Pxx = calculate_psd(s_354)
    
    # Isolate the penalty band surrounding the target diurnal frequency
    lower_bound = cfg.F_25_TARGET - cfg.F_TOLERANCE_BAND
    upper_bound = cfg.F_25_TARGET + cfg.F_TOLERANCE_BAND
    
    total_energy = np.sum(Pxx)
    if total_energy == 0:
        return 1.0
        
    # Extract PSD mass strictly within the leakage bandwidth
    band_mask = (f >= lower_bound) & (f <= upper_bound)
    leakage_energy = np.sum(Pxx[band_mask])
    
    return leakage_energy / total_energy

def calc_ortho_penalty(s_25: pd.Series, s_354: pd.Series) -> float:
    """
    L_Ortho (Eq. 6): Computes the absolute Pearson correlation to enforce 
    structural independence and prevent neural network feature confounding.
    """
    aligned_df = pd.concat([s_25, s_354], axis=1).dropna()
    if aligned_df.empty:
        return 1.0
        
    corr, _ = pearsonr(aligned_df.iloc[:, 0], aligned_df.iloc[:, 1])
    return abs(corr)

def calc_baseflow_penalty(trend: pd.Series) -> float:
    """
    L_Baseflow (Eq. 7): Acts as the physical fail-safe validator. 
    Penalizes synoptic weather ripples (frequencies faster than f_cut) polluting the base flow.
    """
    f, Pxx = calculate_psd(trend)
    
    total_energy = np.sum(Pxx)
    if total_energy == 0:
        return 1.0
        
    # Identify high-frequency volatility violating the 30-day macroscopic boundary
    high_freq_mask = f > cfg.F_CUT_BASEFLOW
    volatile_energy = np.sum(Pxx[high_freq_mask])
    
    return volatile_energy / total_energy

def run_grid_search(input_path: str, output_path: str):
    """Orchestrates the physically bounded hyperparameter grid search."""
    print(f"[INFO] Initializing PI-STOF Multi-Objective Engine...")
    print(f"[INFO] Ingesting processed continuous tensor from: {input_path}")
    
    df = pd.read_csv(input_path, index_col="Date", parse_dates=True)
    z_series = df['Zxuanhoa']
    
    cfg.set_deterministic_seeds()
    
    results = []
    best_loss = float('inf')
    best_params = None
    
    # Construct the parameter grid strictly from physical boundaries
    grid_combinations = list(itertools.product(cfg.W_25_GRID, cfg.W_354_GRID))
    print(f"[PROCESS] Commencing guided search over {len(grid_combinations)} spatial configurations...")
    print(f"[INFO] Macroscopic Catchment Prior Anchored at: w_trend = {cfg.W_TREND_PRIOR}")
    
    for w_25, w_354 in grid_combinations:
        # Enforce scale separation axiom (Micro << Macro)
        if w_25 >= w_354:
            continue 
            
        print(f"       -> Calibrating vector space (w_25={w_25:02d}, w_354={w_354:02d})...")
        
        # 1. Generate multi-scale sequences
        components = execute_physics_mstl(z_series, w_25, w_354)
        
        # 2. Extract domain-specific physical losses
        l_leakage = calc_leakage_penalty(components['s_354'])
        l_ortho = calc_ortho_penalty(components['s_25'], components['s_354'])
        l_baseflow = calc_baseflow_penalty(components['trend'])
        
        # 3. Formulate the Composite Loss Landscape (Eq. 4)
        l_pi = l_leakage + l_ortho + l_baseflow
        
        results.append({
            'Micro-filter (w_25)': w_25,
            'Macro-filter (w_354)': w_354,
            'Leakage (L_Leakage)': round(l_leakage, 6),
            'Orthogonality (L_Ortho)': round(l_ortho, 6),
            'Baseflow (L_Baseflow)': round(l_baseflow, 6),
            'Total Physical Loss (L_PI)': round(l_pi, 6)
        })
        
        if l_pi < best_loss:
            best_loss = l_pi
            best_params = (w_25, w_354)
            
    # Export artifacts for rigorous peer review
    results_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    results_df.to_csv(output_path, index=False)
    
    print("\n======================================================")
    print(f"[SUCCESS] Global Optimization Minima Isolated!")
    print(f"          Optimal Physics Configuration: w_25 = {best_params[0]}, w_354 = {best_params[1]}")
    print(f"          Minimized Composite Physical Loss: {best_loss:.6f}")
    print(f"[SUCCESS] Reviewer artifact exported to {output_path}")
    print("======================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Processed input CSV path")
    parser.add_argument("--output", type=str, required=True, help="Target path for grid search CSV results")
    args = parser.parse_args()
    
    run_grid_search(args.input, args.output)
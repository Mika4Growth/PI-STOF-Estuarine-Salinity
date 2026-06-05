"""
Global Configuration for PI-STOF (Physics-Informed Spectral-Temporal Optimization Framework)
Code Authorship: Khang D. Nguyen
Description: Defines the deterministic physical priors, hyperparameter search space, 
             and spectral boundaries required for estuarine MSTL decomposition.
"""

import numpy as np

# ==========================================
# 1. PHYSICAL PRIORS & STRUCTURAL CONSTANTS
# ==========================================

# Fixed Catchment Inertia Prior (w_trend)
# Set to exactly 6 months (4381 hours) to lock the bi-annual macroscopic monsoon trajectory
# and prevent the absorption of synoptic weather ripples.
W_TREND_PRIOR = 4381

# Base-Flow Spectral Cutoff Frequency (f_cut)
# Represents a 30-day physical boundary. Frequencies above this are penalized in L_Baseflow.
F_CUT_BASEFLOW = 1 / 720.0  # Approx 0.001389 h^-1

# Tidal Frequencies for Spectral Leakage Penalty (L_Leakage)
# Target: Diurnal frequency band to penalize 25-hour energy leaking into the 354-hour envelope.
F_25_TARGET = 1 / 25.0      # Approx 0.040000 h^-1
F_TOLERANCE_BAND = 0.005    # Narrow bandwidth to capture localized nonlinear shifts

# ==========================================
# 2. HYPERPARAMETER SEARCH SPACE (PGML Grid)
# ==========================================

# Micro-Filter Dynamics (w_25)
# Captures localized diurnal inequalities. Bounded between 7.3 and 21.8 days.
W_25_GRID = [7, 11, 15, 21]

# Macro-Filter Dynamics (w_354)
# Captures the Spring-Neap absolute amplitude modulation envelope. Bounded between 1.25 and 3.6 years.
W_354_GRID = [31, 41, 51, 71, 91]

# ==========================================
# 3. MSTL DEFAULTS (For Baseline Comparison)
# ==========================================
DEFAULT_W_25 = 11
DEFAULT_W_354 = 15
# Note: Default MSTL uses automatic trend extraction (None), but we compare it 
# against our ablated baseline with the fixed prior.

# ==========================================
# 4. DETERMINISTIC EXECUTION
# ==========================================
RANDOM_SEED = 42

def set_deterministic_seeds():
    """Ensures 100% computational reproducibility across optimization runs."""
    np.random.seed(RANDOM_SEED)
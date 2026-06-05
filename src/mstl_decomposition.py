"""
MSTL Decomposition Wrapper for Estuarine Dynamics
Code Authorship: Khang D. Nguyen
Description: Interfaces with statsmodels to execute Multiple Seasonal-Trend decomposition 
             using Loess (MSTL), enforcing strict, non-integer celestial periodicities 
             (25h and 354h) mapped to specific LOESS window configurations.
"""

import pandas as pd
from statsmodels.tsa.seasonal import MSTL
import src.config as cfg

def execute_physics_mstl(series: pd.Series, w_25: int, w_354: int, w_trend: int = cfg.W_TREND_PRIOR) -> dict:
    """
    Executes the MSTL decomposition with explicitly bounded physical parameters.
    
    Args:
        series (pd.Series): The preprocessed 1H continuous time-series (e.g., Water Level).
        w_25 (int): LOESS window parameter for the diurnal cycle (Micro-filter).
        w_354 (int): LOESS window parameter for the Spring-Neap cycle (Macro-filter).
        w_trend (int): LOESS window parameter for the base-flow catchment inertia. 
                       Defaults to the physical prior (4381 hours).
                       
    Returns:
        dict: A dictionary containing the decomposed Pandas Series:
              - 'trend': The macroscopic base-flow trajectory.
              - 's_25': The micro-tidal diurnal inequality component.
              - 's_354': The macro-scale Spring-Neap modulation envelope.
              - 'residual': The stochastic high-frequency noise.
    """
    # Enforce period constraints based on celestial mechanics
    # 25h: Lunar day proxy capturing diurnal inequality
    # 354h: 14.77-day Spring-Neap amplitude modulation envelope
    periods = (25, 354)
    
    # Map the window parameters to the respective periods
    windows = (w_25, w_354)
    
    # Initialize the MSTL engine with bounded constraints
    mstl_engine = MSTL(
        endog=series,
        periods=periods,
        windows=windows,
        stl_kwargs={'trend': w_trend} # Lock the macroscopic catchment inertia
    )
    
    # Execute the decomposition
    result = mstl_engine.fit()
    
    # Extract structural components into a reviewer-friendly dictionary
    decomposed_signals = {
        'trend': result.trend,
        's_25': result.seasonal['seasonal_25'],
        's_354': result.seasonal['seasonal_354'],
        'residual': result.resid
    }
    
    return decomposed_signals

def execute_default_baseline(series: pd.Series) -> dict:
    """
    Executes the standard, unconstrained MSTL baseline using heuristic defaults
    (w_25=11, w_354=15, auto trend) for ablation and comparative evaluation.
    """
    # Standard statsmodels defaults for multiple seasonalities
    mstl_engine = MSTL(
        endog=series,
        periods=(25, 354),
        windows=(cfg.DEFAULT_W_25, cfg.DEFAULT_W_354)
        # Note: trend_kwargs is omitted to allow unconstrained automatic derivation
    )
    
    result = mstl_engine.fit()
    
    return {
        'trend': result.trend,
        's_25': result.seasonal['seasonal_25'],
        's_354': result.seasonal['seasonal_354'],
        'residual': result.resid
    }
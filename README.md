# PI-STOF: Physics-Informed Spectral-Temporal Optimization Framework for MSTL Decomposition

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Reproducibility: Artifact Evaluated](https://img.shields.io/badge/Reproducibility-Artifact%20Evaluated-success.svg)](#)

> [cite_start]**Official Repository for the Paper:** "Knowledge Discovery in Estuarine Salinity: A Physics-Informed Spectral-Temporal Optimization Framework (PI-STOF) for MSTL Decomposition" [cite: 1650, 1651, 1652] (Submitted to **CSoNet 2026**).

## 📖 Abstract
Accurate time-series decomposition of estuarine water levels is critical for salinity intrusion modeling. [cite_start]Standard algorithms like Multiple Seasonal-Trend decomposition using Loess (MSTL) often fail in complex coastal hydrodynamics[cite: 1657]. [cite_start]Constrained by time-domain loss functions and rigid integer-period assumptions, standard MSTL induces high-frequency spectral leakage and feature entanglement[cite: 1658]. 

[cite_start]We propose **PI-STOF**, a Physics-Guided Machine Learning (PGML) framework that calibrates LOESS parameters by mapping celestial mechanics into the decomposition space[cite: 1659]. [cite_start]PI-STOF deploys a multi-objective frequency-domain loss function ($\mathcal{L}_{PI}$) using Fast Fourier Transforms (FFT) to penalize spectral leakage, enforce absolute structural orthogonality between the lunar daily cycle (25h) and the Spring-Neap modulation envelope (354h), and lock base-flow inertia[cite: 1660]. [cite_start]The framework reduces physical validation loss by 62.70% and suppresses spectral leakage from 1.72% down to 0.36% compared to unconstrained baselines[cite: 1661].

## 🗄️ Data Availability Statement
The full multi-year 1H dataset (2019–2024, 49,680 observations) was provided by the **Tien Giang Irrigation Works Operating One Member Company Limited** and is restricted due to operational security protocols. 

To ensure **100% CI/CD computational reproducibility** for reviewers, we provide a mathematically rigorous, continuous **1-year operational sample (2020)** in `data/sample/raw_sample.csv`. This 8,784-hour tensor is sufficiently long to execute the macroscopic 6-month LOESS trend filters ($w_{trend} = 4381$) without encountering array bounds errors.

## ⚙️ Setup & Installation
The environment is strictly deterministic to guarantee reproducibility. We recommend using a fresh virtual environment.

```bash
# Clone the repository
git clone [https://github.com/Mika4Growth/PI-STOF-Estuarine-Salinity.git](https://github.com/Mika4Growth/PI-STOF-Estuarine-Salinity.git)
cd PI-STOF-Estuarine-Salinity

# Install fixed dependencies
pip install -r requirements.txt
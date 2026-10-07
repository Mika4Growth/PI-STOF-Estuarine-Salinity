# PI-STOF: Physics-Informed Spectral-Temporal Optimization Framework for MSTL

[![Conference](https://img.shields.io/badge/CSoNet_2026-Accepted-success)](#-citation)
[![Springer](https://img.shields.io/badge/Springer-LNCS-orange)](#-citation)
[![Source Code](https://img.shields.io/badge/GitHub-Official_Repo-black)](https://github.com/Mika4Growth/PI-STOF-Estuarine-Salinity)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- When the Springer DOI is available, add a badge here, e.g.:
[![DOI](https://img.shields.io/badge/DOI-<doi>-blue)](https://doi.org/<doi>) -->

> **Official code repository for the paper:** "Mitigating Spectral Leakage in MSTL: A Physics-Informed Optimization Framework for Estuarine Water-Level Decomposition", accepted at **CSoNet 2026** (15th International Conference on Computational Science and Network Intelligence), to appear in Springer LNCS.

## Abstract

While accurate time-series decomposition of estuarine water levels is critical for forecasting non-stationary environmental dynamics, algorithms such as Multiple Seasonal-Trend decomposition using LOESS (MSTL) often fail in the presence of complex coastal hydrodynamics. Constrained by time-domain loss functions and rigid integer-period assumptions, standard MSTL induces high-frequency spectral leakage and feature entanglement.

To resolve this, we propose the Physics-Informed Spectral-Temporal Optimization Framework (PI-STOF), which calibrates LOESS parameters by mapping deterministic physical priors onto the discrete decomposition space. PI-STOF introduces a multi-objective frequency-domain loss function ($\mathcal{L}_{PI}$) to penalize spectral leakage, enforce near-orthogonality between the high-frequency diurnal carrier wave ($25\,\mathrm{h}$) and the macroscopic amplitude modulation envelope ($354\,\mathrm{h}$), and lock low-frequency base-flow inertia. Validated on a 49,680-hour Mekong Delta dataset (2019–2024), the optimal physics-calibrated configuration ($w_{25}=7$, $w_{354}=91$, $w_{\text{trend}}=4381$) reduces overarching physical validation loss by 57.91% compared to a baseline with an equivalent trend prior (and by 62.60% against fully unconstrained defaults), while mitigating spectral leakage from 1.72% down to 0.36%. By preserving non-linear structural asymmetry and isolating low-frequency background drift, PI-STOF yields a near-linearly uncorrelated decomposition with a 48.1% reduction in cross-correlation between tidal components (from an already negligible baseline), providing a cleaner feature representation for downstream deep sequence architectures.

## Method at a Glance

PI-STOF searches for the LOESS window triple $\theta = (w_{25}, w_{354}, w_{\text{trend}})$ that minimizes

$$\mathcal{L}_{PI}(\theta) = \mathcal{L}_{Leakage} + \mathcal{L}_{Ortho} + \mathcal{L}_{Baseflow}$$

| Term | What it measures |
|---|---|
| $\mathcal{L}_{Leakage}$ | Share of PSD energy of the $S_{354}$ (Spring-Neap) component that falls in the diurnal ($\approx 25\,\mathrm{h}$) band, $\epsilon = 0.005\,\mathrm{h}^{-1}$ |
| $\mathcal{L}_{Ortho}$ | $\lvert\mathrm{Corr}(S_{25}, S_{354})\rvert$, i.e. linear independence of the two tidal components |
| $\mathcal{L}_{Baseflow}$ | Share of trend PSD energy above $f_{cut} = 1/720\,\mathrm{h}^{-1}$ (periods shorter than 30 days) |

- **Search space (20 configurations):** $w_{25} \in \{7, 11, 15, 21\}$, $w_{354} \in \{31, 41, 51, 71, 91\}$.
- **Fixed trend prior:** $w_{\text{trend}} = 4381$ h (≈ 6 months) is anchored, not optimized, to prevent the solver from flattening the trend ($w_{\text{trend}} \to \infty$).
- **Baselines:** (i) *Pure Default* (`statsmodels` MSTL defaults: $w_{25}=11$, $w_{354}=15$, automatic trend) and (ii) *Default + Fixed Trend* (same windows, $w_{\text{trend}}=4381$).
- **Role of $\mathcal{L}_{Baseflow}$:** once the trend window is anchored, it acts as a *passive structural health monitor* rather than an active driver of the optimization (see the ablation in the paper).

### Headline results (full dataset, from the paper)

| Configuration | $w_{25}$ | $w_{354}$ | $w_{\text{trend}}$ | $\mathcal{L}_{Leakage}$ | $\mathcal{L}_{Ortho}$ | $\mathcal{L}_{Baseflow}$ | $\mathcal{L}_{PI}$ |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Pure Default Baseline | 11 | 15 | Auto | 0.0172 | 0.0208 | 0.0104 | 0.0484 |
| Default + Fixed Trend | 11 | 15 | 4381 | 0.0182 | 0.0210 | 0.0038 | 0.0430 |
| **PI-STOF (proposed)** | **7** | **91** | **4381** | **0.0036** | **0.0108** | **0.0037** | **0.0181** |

> **Scope.** This repository covers the decomposition stage (hyperparameter calibration of MSTL on estuarine water levels). Validation of the downstream deep-learning benefit, e.g. salinity forecasting, is future work and is not included here.

## Data Availability Statement

The full hourly water-level dataset (Xuan Hoa station, Tien River branch of the Mekong Delta; 01 Jan 2019 – 31 Aug 2024; 49,680 observations; manual staff-gauge readings following QCVN 47:2022/BTNMT) was provided by the [Tien Giang Irrigation Works Operating One Member Company Limited](http://thuyloitiengiang.vn/) and is **restricted** due to operational security protocols.

To allow readers to run the full pipeline, we provide a continuous **1-year operational sample (2020)** in `data/sample/raw_sample.csv` (8,784 hourly observations). The sample is long enough to run the 6-month LOESS trend filter ($w_{\text{trend}} = 4381$) without array-bound errors.

**Note on preprocessing.** In the paper, outlier candidates in the full dataset were screened *manually* by domain experts against astronomical tide tables and meteorological records. This expert step is not part of the released code. The provided script implements only the automated gap-imputation stage (linear interpolation for gaps ≤ 5 h, PCHIP for gaps > 5 h).

## Setup & Installation

Reported results were produced with **Python 3.9**, `statsmodels` 0.13.5 and `scipy` 1.10.1. We recommend a fresh virtual environment.

```bash
# Clone the repository
git clone https://github.com/Mika4Growth/PI-STOF-Estuarine-Salinity.git
cd PI-STOF-Estuarine-Salinity

# Install pinned dependencies
pip install -r requirements.txt
```

## How to Run the Pipeline

The codebase decouples data engineering from the optimization engine. Run the modules sequentially:

**1. Data preprocessing (hybrid imputation)**

Reconstructs the sequence using gap-size-dependent linear/PCHIP interpolation to preserve the diurnal inequality without introducing artificial phase shifts.

```bash
python -m src.data_preprocessing --input "data/sample/raw_sample.csv" --output "data/processed/clean_sample.csv"
```

**2. PI-STOF multi-objective grid search**

Runs the FFT/PSD-based analysis and evaluates the three loss terms over the physically bounded search space.

```bash
python -m src.pi_stof_engine --input "data/processed/clean_sample.csv" --output "results/tables/table_2_grid_search.csv"
```

**3. Generate paper artifacts (evaluation)**

Disentangles the signals with the optimal PI-STOF configuration ($w_{25}=7$, $w_{354}=91$) versus the unconstrained MSTL baselines, and generates the figures and ablation tables.

```bash
python -m src.evaluation --input "data/processed/clean_sample.csv" --figures_dir "results/figures" --tables_dir "results/tables"
```

> **Runtime.** On the full 49,680-hour series the optimization took approximately 3.5 hours (as reported in the paper). The 1-year sample is considerably faster.

## Reproducing the Paper

> **Note on table/figure numbering.** This repository was prepared alongside the submitted version of the manuscript, and the scripts export the table and figure files of that version. To meet the page limit, the **camera-ready version condenses these outputs**: the separate grid-search and ablation tables were merged into a single unified table (Table 1), and the individual result figures were combined into one multi-panel figure (Fig. 2). The code and its outputs are unchanged. The mapping is given below.

| Output generated by the code | Content | Where it appears in the camera-ready paper |
|---|---|---|
| `results/tables/` Tables 1 & 2 (incl. `table_2_grid_search.csv`) | Convergence of $\mathcal{L}_{PI}$ over the search space and isolation of the global minimum ($w_{25}=7$, $w_{354}=91$) | Summarized in Section 5.1 and in the *Pure Default*, *Default + Fixed Trend* and *Full PI-STOF* rows of Table 1 |
| `results/tables/` Table 3 (`Table_3_Ablation.csv`) | Ablation of the loss terms and the anchored base-flow prior | **Table 1** (Unified Baseline Comparison and Ablation Analysis), rows *Variant A / B / C* and *Full PI-STOF* |
| `results/figures/` Figure 2 | Mitigation of spectral leakage in the 354 h Spring-Neap envelope | **Fig. 2(b)** |
| `results/figures/` Figure 3 | Preservation of the HHW/LHW diurnal inequality | **Fig. 2(a)** |
| `results/figures/` Figure 4 | Bi-annual base-flow inertia secured by the anchored trend prior | **Fig. 2(c)** |

Fig. 1 of the paper is a plot of the raw water-level series of the full (restricted) dataset.

## Reproducibility Note

Comparing `Table_3_Ablation.csv` with Table 1 of the paper, you will observe that the absolute physical loss values ($\mathcal{L}_{PI}$) produced from the public sample are higher than those in the paper (e.g., PI-STOF yields $\approx 0.033$ here versus $\approx 0.018$ in the paper).

**Why the absolute values differ.** The paper evaluates the PSD over the full 5.5-year series ($N = 49{,}680$), whereas the public sample covers one year ($N = 8{,}784$). The shorter record has two effects:

1. **Coarser frequency resolution.** The Rayleigh resolution degrades from $\approx 2.0 \times 10^{-5}\,\mathrm{h}^{-1}$ to $\approx 1.1 \times 10^{-4}\,\mathrm{h}^{-1}$, which causes more spectral smearing in the PSD integrals.
2. **Stronger boundary effects.** The macro window $w_{354}=91$ spans far more than one year, so the LOESS fit near the edges of the shorter series is less well constrained.

Absolute values are therefore **not** directly comparable between the sample and the full dataset. The relative behaviour is preserved: on the sample, PI-STOF still achieves a reduction of more than 58% in physical loss compared with the unconstrained MSTL baseline.

## Citation

If you use this framework or the imputation schema in your research, please cite our CSoNet 2026 paper:

```bibtex
@inproceedings{Nguyen2026PISTOF,
  title     = {Mitigating Spectral Leakage in {MSTL}: A Physics-Informed Optimization Framework for Estuarine Water-Level Decomposition},
  author    = {Nguyen, Khang D. and Khuong, Nguyen-An},
  booktitle = {Computational Science and Network Intelligence (CSoNet 2026)},
  series    = {Lecture Notes in Computer Science},
  publisher = {Springer},
  year      = {2026},
  note      = {To appear}
}
```

## Acknowledgements

This research is funded by Ho Chi Minh City University of Technology (HCMUT), VNU-HCM under grant number SVOISP-2025-CK-19. We gratefully acknowledge the Tien Giang Irrigation Works Operating Company for providing the long-term hydrological dataset and domain expertise essential to this study.
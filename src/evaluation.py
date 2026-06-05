"""
PI-STOF Evaluation and Artifact Generation Module
Code Authorship: Khang D. Nguyen
Description: Executes the ablation baselines and automated generation of 
             reproducible publication-grade figures (Figs 2, 3, 4) 
             and evaluation tables (Table 3) highlighting the spectral disentanglement.
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import src.config as cfg
from src.mstl_decomposition import execute_physics_mstl, execute_default_baseline
# Import thêm các hàm tính Loss từ PI-STOF Engine để chấm điểm Ablation
from src.pi_stof_engine import calc_leakage_penalty, calc_ortho_penalty, calc_baseflow_penalty

def setup_academic_style():
    """Configures matplotlib for SCI-indexed journal standards."""
    sns.set_theme(style="ticks", context="paper")
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'legend.fontsize': 11,
        'figure.dpi': 300,
        'font.family': 'serif'
    })

def plot_figure_2_macro_envelope(res_default, res_pistof, output_dir):
    """Generates Fig 2: Macro-scale Spring-Neap Envelope (354h) comparison."""
    zoom_start, zoom_end = '2020-02-01', '2020-05-31'
    s354_default = res_default['s_354'].loc[zoom_start:zoom_end]
    s354_pistof = res_pistof['s_354'].loc[zoom_start:zoom_end]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(s354_pistof.index, s354_pistof.values, color='#1f77b4', linestyle='-', 
            linewidth=2.0, zorder=2, label='PI-STOF ($w_{354}=91$)')
    ax.plot(s354_default.index, s354_default.values, color='#d62728', linestyle='--', 
            linewidth=1.2, alpha=0.9, zorder=3, label='Default MSTL ($w_{354}=15$)')

    ax.set_title('Macro-scale Spring-Neap Envelope ($S_{354}$)', pad=15, fontweight='bold')
    ax.set_ylabel('Amplitude ($m$)')
    ax.set_xlabel('Date')
    
    handles, labels = ax.get_legend_handles_labels()
    ax.legend([handles[1], handles[0]], [labels[1], labels[0]], loc='upper right', frameon=True, edgecolor='black')
    ax.grid(True, linestyle=':', alpha=0.6, zorder=1)

    idx_target = len(s354_default) // 3
    idx_text = len(s354_default) // 5
    ax.annotate('High-frequency Leakage\n(Under-smoothed)', 
                xy=(s354_default.index[idx_target], s354_default.max() * 0.85),
                xytext=(s354_default.index[idx_text], s354_default.max() * 1.15),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=0.5), zorder=4)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig_2_S354_Envelope.png'))
    plt.close()

def plot_figure_3_micro_dynamics(res_default, res_pistof, output_dir):
    """Generates Fig 3: Micro-Tidal Dynamics (25h) preserving Diurnal Inequality."""
    zoom_micro_start, zoom_micro_end = '2020-03-01', '2020-03-07'
    s25_default = res_default['s_25'].loc[zoom_micro_start:zoom_micro_end]
    s25_pistof = res_pistof['s_25'].loc[zoom_micro_start:zoom_micro_end]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(s25_default.index, s25_default.values, color='#d62728', linestyle='--', 
            linewidth=1.5, alpha=0.8, label='Default MSTL ($w_{25}=11$)')
    ax.plot(s25_pistof.index, s25_pistof.values, color='#1f77b4', linestyle='-', 
            linewidth=2, label='PI-STOF ($w_{25}=7$)')

    ax.set_title('Micro-Tidal Dynamics ($S_{25}$): Preservation of Diurnal Inequality', pad=15, fontweight='bold')
    ax.set_ylabel('Amplitude ($m$)')
    ax.set_xlabel('Date')
    ax.legend(loc='lower right', frameon=True, edgecolor='black')
    ax.grid(True, linestyle=':', alpha=0.6)

    peak_time = s25_pistof.idxmax()
    ax.annotate('Preserved HHW Anomaly', 
                xy=(peak_time, s25_pistof.max()),
                xytext=(peak_time, s25_pistof.max() * 1.2),
                arrowprops=dict(facecolor='#1f77b4', shrink=0.05, width=1, headwidth=5),
                fontsize=10, ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig_3_S25_Dynamics.png'))
    plt.close()

def plot_figure_4_macro_trend(res_default, res_pistof, output_dir):
    """Generates Fig 4: Catchment Base-Flow Trend over the operational sample."""
    trend_default = res_default['trend']
    trend_pistof = res_pistof['trend']

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(trend_default.index, trend_default.values, color='#d62728', linestyle='--', 
            linewidth=1.2, alpha=0.8, label='Default Trend (Unconstrained)')
    ax.plot(trend_pistof.index, trend_pistof.values, color='#1f77b4', linestyle='-', 
            linewidth=2.5, label='PI-STOF Trend ($w_{trend}=4381$)')

    ax.set_title('Catchment Base-Flow: Macro-Trend Trajectory (Sample Year 2020)', pad=15, fontweight='bold')
    ax.set_ylabel('Water Level ($m$)')
    ax.set_xlabel('Date')
    ax.legend(loc='upper right', frameon=True, edgecolor='black')
    ax.grid(True, linestyle=':', alpha=0.6)

    idx_target = len(trend_default) // 3
    idx_text = len(trend_default) // 4
    ax.annotate('Synoptic Weather Ripples\n(False Volatility)', 
                xy=(trend_default.index[idx_target], trend_default.values[idx_target]),
                xytext=(trend_default.index[idx_text], trend_default.max() * 0.85),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=0.5))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'Fig_4_Macro_Trend.png'))
    plt.close()

def generate_table_3_ablation(z_series, res_default, res_pistof, output_dir):
    """Generates Table 3: Ablation study showing the impact of the physical priors."""
    print(f"[PROCESS] Executing Ablated Baseline (Default Seasonality + Fixed Trend)...")
    # Kịch bản 3: Default Seasonality nhưng ÉP Trend Window
    res_default_fixed = execute_physics_mstl(z_series, w_25=cfg.DEFAULT_W_25, w_354=cfg.DEFAULT_W_354)
    
    def get_metrics(res):
        l_leakage = calc_leakage_penalty(res['s_354'])
        l_ortho = calc_ortho_penalty(res['s_25'], res['s_354'])
        l_baseflow = calc_baseflow_penalty(res['trend'])
        l_pi = l_leakage + l_ortho + l_baseflow
        return round(l_leakage, 6), round(l_ortho, 6), round(l_baseflow, 6), round(l_pi, 6)

    data = [
        {"Model": "Baseline 1: MSTL Default (11, 15, Auto Trend)", **dict(zip(['L_Leakage', 'L_Ortho', 'L_Baseflow', 'L_PI'], get_metrics(res_default)))},
        {"Model": "Baseline 2: Ablated MSTL (11, 15, Trend=4381)", **dict(zip(['L_Leakage', 'L_Ortho', 'L_Baseflow', 'L_PI'], get_metrics(res_default_fixed)))},
        {"Model": "PI-STOF: Optimal PGML (7, 91, Trend=4381)", **dict(zip(['L_Leakage', 'L_Ortho', 'L_Baseflow', 'L_PI'], get_metrics(res_pistof)))}
    ]
    
    df = pd.DataFrame(data)
    save_path = os.path.join(output_dir, 'Table_3_Ablation.csv')
    df.to_csv(save_path, index=False)
    print(f"[SUCCESS] Table 3 (Ablation Study) generated: {save_path}")

def generate_all_artifacts(input_path: str, figures_dir: str, tables_dir: str):
    print(f"[INFO] Initializing Artifact Generation Module...")
    
    # 1. Load Preprocessed Data
    df = pd.read_csv(input_path, index_col="Date", parse_dates=True)
    z_series = df['Zxuanhoa']
    
    # 2. Execute Decompositions (Kịch bản 1 & 2)
    print(f"[PROCESS] Executing Unconstrained MSTL Baseline...")
    res_default = execute_default_baseline(z_series)
    
    print(f"[PROCESS] Executing PI-STOF Optimized Decompositions (7, 91)...")
    res_pistof = execute_physics_mstl(z_series, w_25=7, w_354=91)
    
    # 3. Establish Directories & Styles
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    setup_academic_style()
    
    # 4. Generate Table 3 (Ablation Study)
    generate_table_3_ablation(z_series, res_default, res_pistof, tables_dir)

    # 5. Generate Figures 2, 3, 4
    print(f"\n[PROCESS] Rendering publication-grade vector graphics...")
    plot_figure_2_macro_envelope(res_default, res_pistof, figures_dir)
    plot_figure_3_micro_dynamics(res_default, res_pistof, figures_dir)
    plot_figure_4_macro_trend(res_default, res_pistof, figures_dir)
    
    print("\n======================================================")
    print(f"[SUCCESS] All artifacts exported successfully!")
    print("======================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Processed input CSV path")
    parser.add_argument("--figures_dir", type=str, required=True, help="Output directory for figures")
    parser.add_argument("--tables_dir", type=str, required=True, help="Output directory for tables")
    args = parser.parse_args()
    
    generate_all_artifacts(args.input, args.figures_dir, args.tables_dir)
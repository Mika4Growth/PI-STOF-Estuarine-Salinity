#!/bin/bash

# Enforce strict error handling
set -e

echo "======================================================"
echo "    PI-STOF: AUTOMATED ARTIFACT GENERATION PIPELINE   "
echo "======================================================"

INPUT_FILE="data/processed/clean_sample.csv"
FIGURES_DIR="results/figures"
TABLES_DIR="results/tables"

# Pre-flight check
if [ ! -f "$INPUT_FILE" ]; then
    echo "[ERROR] Cleaned input data not found at: $INPUT_FILE"
    echo "Please execute 'bash scripts/run_preprocessing.sh' first."
    exit 1
fi

# Generate visualization artifacts and ablation table
python src/evaluation.py \
    --input "$INPUT_FILE" \
    --figures_dir "$FIGURES_DIR" \
    --tables_dir "$TABLES_DIR"

echo "======================================================"
echo "         ARTIFACT GENERATION COMPLETED                "
echo "======================================================"
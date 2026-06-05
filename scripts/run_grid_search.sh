#!/bin/bash

# Enforce strict error handling
set -e

echo "======================================================"
echo "      PI-STOF: EXECUTING MULTI-OBJECTIVE OPTIMIZATION "
echo "======================================================"

# Define standardized relative paths
INPUT_FILE="data/processed/clean_sample.csv"
OUTPUT_FILE="results/tables/table_2_grid_search.csv"

# Pre-flight check: Ensure preprocessing was successful
if [ ! -f "$INPUT_FILE" ]; then
    echo "[ERROR] Cleaned input data not found at: $INPUT_FILE"
    echo "Please execute 'bash scripts/run_preprocessing.sh' first."
    exit 1
fi

# Execute the physics-informed grid search
python src/pi_stof_engine.py \
    --input "$INPUT_FILE" \
    --output "$OUTPUT_FILE"

echo "======================================================"
echo "          GRID SEARCH COMPLETED SUCCESSFULLY          "
echo "======================================================"
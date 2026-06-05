#!/bin/bash

# Enforce strict error handling: exit immediately if a command exits with a non-zero status
set -e

echo "======================================================"
echo "    PI-STOF: INITIATING DATA PREPROCESSING PIPELINE   "
echo "======================================================"

# Define standardized input and output relative paths
INPUT_FILE="data/sample/raw_sample.csv"
OUTPUT_FILE="data/processed/clean_sample.csv"

# Verify the existence of the input data before execution
if [ ! -f "$INPUT_FILE" ]; then
    echo "[ERROR] Raw data file not found at: $INPUT_FILE"
    echo "Please ensure the dataset is placed correctly as per the README data availability instructions."
    exit 1
fi

# Execute the Python preprocessing module
python src/data_preprocessing.py \
    --input "$INPUT_FILE" \
    --output "$OUTPUT_FILE"

echo "======================================================"
echo "               PIPELINE EXECUTION COMPLETE            "
echo "======================================================"
"""
This script consolidates multiple JSON files into one JSONL file.

The JSON files are expected to be in the specified input directory, and the consolidated
output is written to the specified output file.

Usage:
1. Place your JSON files in the specified input directory.
2. Run this script to consolidate them into a single JSONL file.
"""

import os

JSONL_DIRECTORY = 'data/training_data/'
CONSOLIDATED_FILE_PATH = 'data/consolidated_data/consolidated_training_data.jsonl'

# Consolidate JSON files into one JSONL file
with open(CONSOLIDATED_FILE_PATH, 'w', encoding="utf-8") as outfile:
    for file_name in os.listdir(JSONL_DIRECTORY):
        if file_name.endswith('.jsonl'):
            file_path = os.path.join(JSONL_DIRECTORY, file_name)
            with open(file_path, 'r', encoding="utf-8") as infile:
                for line in infile:
                    outfile.write(line)

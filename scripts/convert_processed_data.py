"""
This script converts CSV files containing match data into JSONL format.
Each CSV file is processed to create a JSONL file with a "prompt" and a "completion."

The "prompt" includes all columns from the CSV row except 'home_goals' and 'away_goals'.
The "completion" indicates the outcome, such as 'Home team win' or 'Away team win',
based on the comparison of 'home_goals' and 'away_goals' columns.

Directory paths for input (CSV) and output (JSONL) files are specified 
at the beginning of the script.

Usage:
1. Place your CSV files in the specified input directory.
2. Run this script to convert the CSV files to JSONL format in the output directory.
"""

import csv
import json
import os

# Define the directory where your CSV files are located
CSV_DIRECTORY = 'data/processed/'
JSONL_DIRECTORY = 'data/training_data/'

# Convert each CSV file to JSONL
for file_name in os.listdir(CSV_DIRECTORY):
    if file_name.endswith('.csv'):
        csv_file_path = os.path.join(CSV_DIRECTORY, file_name)
        jsonl_file_path = os.path.join(JSONL_DIRECTORY, file_name.replace('.csv', '.jsonl'))

        with open(csv_file_path, 'r', encoding="utf-8") as csv_file, open(jsonl_file_path, 'w', encoding="utf-8") as jsonl_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Create the "prompt" from the CSV row data
                prompt = {key: row[key] for key in row if key not in ['home_goals', 'away_goals']}
                # Create the "completion" with the desired outcome, e.g., home or away team win
                home_goals = int(row['home_goals'])
                away_goals = int(row['away_goals'])
                COMPLETION = 'Home team win' if home_goals > away_goals else 'Away team win'
                # Write the JSON object to the JSONL file
                jsonl_file.write(json.dumps({'prompt': prompt, 'completion': COMPLETION}) + '\n')

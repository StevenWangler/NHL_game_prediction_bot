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

print('Starting to convert the processed data')
for file_name in os.listdir(CSV_DIRECTORY):
    if file_name.endswith('.csv'):
        csv_file_path = os.path.join(CSV_DIRECTORY, file_name)
        jsonl_file_path = os.path.join(JSONL_DIRECTORY, file_name.replace('.csv', '.jsonl'))

        with open(csv_file_path, 'r', encoding="utf-8") as csv_file, open(jsonl_file_path, 'w', encoding="utf-8") as jsonl_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Include 'home_goals' and 'away_away_goals' in the prompt
                prompt = {key: row[key] for key in row}  # No longer excluding home and away goals

                # Convert 'home_goals' and 'away_away_goals' to integers
                HOME_GOALS = int(float(row['home_goals']))
                AWAY_GOALS = int(float(row['away_away_goals']))

                # Determine the completion based on goals comparison
                COMPLETION = 'The home team has won this game due to the statistical advantages found in the data.' if HOME_GOALS > AWAY_GOALS else 'The away team has won due to the statistical advantages found in the data.'

                # Write the JSON object to the JSONL file
                jsonl_file.write(json.dumps({'prompt': prompt, 'completion': COMPLETION}) + '\n')

print('processing complete!')

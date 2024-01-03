"""
This script transforms a JSONL file containing NHL game data into a different
JSONL format that simulates a conversation between a system, a user, and an assistant.
The new format includes the system providing context, the user asking about the game
outcome, and the assistant presenting the game statistics and outcome.

The script reads each line from the input JSONL file, extracts necessary data,
and then reformats it into the new conversational structure. The transformed
data is then written to a new JSONL file.

Usage:
1. Ensure the input JSONL file is present at the specified input path.
2. Run the script to generate the transformed JSONL file at the specified output path.
"""

import json

# File paths
INPUT_FILE_PATH = 'data/consolidated_data/consolidated_training_data.jsonl'
OUTPUT_FILE_PATH = 'data/final_training_data/transformed_training_data.jsonl'

def calculate_synthetic_chance(team_stats):
    """
    Calculate the synthetic chance of winning for home and away teams.

    Parameters:
    team_stats (dict): A dictionary containing team statistics.

    Returns:
    tuple: A tuple containing the percentage chances of winning for the home and away teams.
    """
    powerplay_weight = 0.35
    faceoff_weight = 0.25
    blocks_weight = 0.15
    away_hits_weight = 0.10
    away_pim_weight = 0.10
    home_pim_weight = 0.05

    # Calculating weighted scores with new weights
    home_score = (power_play_success_rate(team_stats['powerPlayConversion']) * powerplay_weight +
                float(team_stats['faceoffWinningPctg']) * faceoff_weight +
                int(float(team_stats['blocks'])) * blocks_weight -
                int(float(team_stats['pim'])) * home_pim_weight)

    away_score = (power_play_success_rate(team_stats['away_powerPlayConversion']) * powerplay_weight +
                float(team_stats['away_faceoffWinningPctg']) * faceoff_weight +
                int(float(team_stats['away_blocks'])) * blocks_weight +
                int(float(team_stats['away_hits'])) * away_hits_weight -
                int(float(team_stats['away_pim'])) * away_pim_weight)



    # Normalizing scores to get a percentage chance of winning
    total_score = home_score + away_score
    home_chance = round((home_score / total_score) * 100, 2) if total_score != 0 else 50
    away_chance = round((away_score / total_score) * 100, 2) if total_score != 0 else 50

    return home_chance, away_chance

def power_play_success_rate(conversion):
    """
    Calculate the success rate of power plays.

    Parameters:
    conversion (str): A string representing goals over attempts in the format 'goals/attempts'.

    Returns:
    float: The success rate of power plays.
    """
    parts = conversion.split('/')
    if len(parts) != 2:
        print(f"Invalid format for conversion: {conversion}")
        return 0  # Or handle the error as needed

    goals, attempts = map(int, parts)
    return goals / attempts if attempts != 0 else 0

def transform_line(line):
    """
    Transform a line of NHL game data from JSONL format to a conversational format.

    Parameters:
    line (str): A string representing a line of JSONL data.

    Returns:
    str: A string of the transformed data in JSON format.
    """
    data = json.loads(line)
    team_info = data['prompt']
    home_chance, away_chance = calculate_synthetic_chance(team_info)

    # Placeholder for predicted goals and reason (to be refined)
    predicted_home_goals = team_info['home_goals']
    predicted_away_goals = team_info['away_away_goals']
    confidence = None

    # Dynamic confidence calculation
    chance_diff = abs(home_chance - away_chance)
    if chance_diff > 30:
        confidence = "high"
    elif chance_diff > 10:
        confidence = "medium"
    else:
        confidence = "low"

    # Constructing the new message format with enhancements
    new_data = {
        "messages": [
            {"role": "system", "content": "You are a MASTER NHL statistics assistant that accurately predicts the outcome of NHL games using comprehensive and up-to-date team and player statistics."},
            {"role": "user", "content": f"What is your prediction for the {team_info['name']} vs {team_info['away_name']} game considering recent team performances and player conditions?"},
            {"role": "assistant", "content": json.dumps({
                "venue": "(put the venue here)",
                "home team name": team_info['name'],
                "home team percentage chance of winning": f"{home_chance}%",
                "predicted home team goals": predicted_home_goals,
                "away team name": team_info['away_name'],
                "away team percentage chance of winning": f"{away_chance}%",
                "predicted away team goals": predicted_away_goals,
                "key factors influencing prediction": "(List key statistical factors here)",
                "confidence rating": confidence,
                "confidence reason": "(explain why you gave the confidence you did)",
                "opposition": "(explain why you think the game could go the opposite of what you predicted)"
            })}
        ]
    }
    return json.dumps(new_data)

# Read, transform, and write to new file
with open(INPUT_FILE_PATH, 'r', encoding='utf-8') as infile, open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as outfile:
    for line in infile:
        transformed_line = transform_line(line)
        outfile.write(transformed_line + '\n')

print("Transformation complete. Check the output file.")

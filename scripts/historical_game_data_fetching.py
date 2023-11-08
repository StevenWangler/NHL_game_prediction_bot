"""
NHL Game Data Fetching Script

This script fetches NHL game data from the NHL API for a specified 
season and stores it in CSV files.

Usage:
1. Run this script to fetch and save NHL game data for the specified season and teams.

Requirements:
- Python 3.x
- requests library

Developer: Steven Wangler

"""

import csv
import os
import requests

print('Running NHL game data fetching script')

# Define the base URL for the NHL API and the season of interest
NHL_API_BASE_URL = "https://statsapi.web.nhl.com/api/v1"
SEASON = "20222023"
DATA_DIRECTORY = 'data/raw'

def safe_request(url):
    """
    Send a request to the specified URL and handle any potential errors.

    :param url: The URL to send the request to.
    :return: The JSON response if successful, None otherwise.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_team_information():
    """
    Fetch the team information from the NHL API.

    :return: Team information in JSON format.
    """
    print("Fetching NHL teams information")
    teams_endpoint = f"{NHL_API_BASE_URL}/teams"
    return safe_request(teams_endpoint)

def get_game_results(game_id):
    """
    Fetch the game results for a specific game ID from the NHL API.

    :param game_id: The unique identifier for the game.
    :return: Game results in JSON format.
    """
    print(f"Fetching game results for game ID: {game_id}")
    game_endpoint = f"{NHL_API_BASE_URL}/game/{game_id}/boxscore"
    return safe_request(game_endpoint)

def extract_detailed_stats(game_data):
    """
    Extract detailed team statistics from game data, separating home and away team goals.

    :param game_data: Game data in JSON format.
    :return: Home team stats and away team stats as dictionaries.
    """
    # Original extraction of stats
    home_stats = game_data.get('teams', {}).get('home', {}).get('teamStats', {}).get('teamSkaterStats', {})
    away_stats = game_data.get('teams', {}).get('away', {}).get('teamStats', {}).get('teamSkaterStats', {})

    # Renaming the 'goals' field for clarity
    home_stats['home_goals'] = home_stats.pop('goals', None)
    away_stats['away_goals'] = away_stats.pop('goals', None)

    return home_stats, away_stats

def merge_stats(home_stats, away_stats, game_data):
    """
    Merge home and away team statistics with team names into one dictionary, 
    including separate goal stats.

    :param home_stats: Home team statistics.
    :param away_stats: Away team statistics.
    :param game_data: Game data in JSON format.
    :return: Merged statistics as a dictionary.
    """
    home_team_name = game_data.get('teams', {}).get('home', {}).get('team', {}).get('name', '')
    away_team_name = game_data.get('teams', {}).get('away', {}).get('team', {}).get('name', '')

    # Merge dictionaries with renamed goals keys and team names
    merged_stats = {
        'home_team': home_team_name,
        **home_stats,
        'away_team': away_team_name,
        **away_stats
    }
    return merged_stats

def write_to_csv(all_game_stats, team_name):
    """
    Write the collected game statistics to a CSV file.

    :param all_game_stats: List of game statistics as dictionaries.
    :param team_name: Name of the team for which the statistics are collected.
    """
    csv_file_path = os.path.join(DATA_DIRECTORY, f'{SEASON}_{team_name.replace(" ", "_")}_game_results.csv')
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    fieldnames = all_game_stats[0].keys() if all_game_stats else []
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for stats in all_game_stats:
            writer.writerow(stats)
    print(f"Data for {team_name} written to {csv_file_path}")

if __name__ == "__main__":
    team_info = get_team_information()
    if team_info:
        for team in team_info.get('teams', []):
            team_id = team['id']
            team_name = team['name']
            print(f"Processing data for {team_name}")        
            schedule_endpoint = f"{NHL_API_BASE_URL}/schedule?teamId={team_id}&season={SEASON}"
            schedule_response = safe_request(schedule_endpoint)

            if schedule_response:
                game_ids = [
                    game['gamePk'] for date in schedule_response.get('dates', [])
                    for game in date.get('games', [])
                ]

                all_game_stats = []
                for game_id in game_ids:
                    game_data = get_game_results(game_id)
                    if game_data:
                        home_stats, away_stats = extract_detailed_stats(game_data)
                        merged_stats = merge_stats(home_stats, away_stats, game_data)
                        all_game_stats.append(merged_stats)

                if all_game_stats:
                    write_to_csv(all_game_stats, team_name)
                else:
                    print(f"No game stats found for {team_name}")
            else:
                print(f"Failed to fetch schedule for {team_name}")
    else:
        print("Failed to fetch team information")

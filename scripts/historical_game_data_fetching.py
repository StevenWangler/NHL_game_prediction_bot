"""
NHL Game Data Fetching Script

Fetches NHL game data from the NHL API for a specified season and stores it in CSV files.

Requirements:
- Python 3.x
- requests library

Developer: Steven Wangler
"""

import time
import csv
import requests

# Constants and configuration
NHL_API_BASE_URL = "https://api-web.nhle.com/v1/"
NHL_API_TEAM_BASE_URL = "https://api.nhle.com/stats/rest/"
SEASON = "20182019"
DATA_DIRECTORY = 'data/raw'

def make_api_request(url, max_retries=3, delay=5):
    """
    Send a request to the NHL API and handle errors with retries.

    Parameters:
    url (str): The API endpoint URL.
    max_retries (int): Maximum number of retries.
    delay (int): Delay between retries in seconds.

    Returns:
    dict: JSON response from the API, or None if all retries fail.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Maximum retries reached. Unable to fetch data.")
    return None

def fetch_team_data():
    """ Fetch and return team information from the NHL API. """
    endpoint = f"{NHL_API_TEAM_BASE_URL}en/team"
    return make_api_request(endpoint)

def fetch_game_data(game_id):
    """ Fetch and return game data for a given game ID from the NHL API. """
    endpoint = f"{NHL_API_BASE_URL}gamecenter/{game_id}/boxscore"
    return make_api_request(endpoint)

def extract_stats_from_game_data(game_data):
    """ Extract and return relevant statistics from game data. """
    home_stats = game_data.get('homeTeam', {})
    away_stats = game_data.get('awayTeam', {})

    home_stats['home_goals'] = home_stats.pop('score', None)
    away_stats['away_goals'] = away_stats.pop('score', None)

    return home_stats, away_stats

def clean_stat_dict(stat_dict):
    """Clean a single statistics dictionary."""
    cleaned_stat = stat_dict.copy()

    # Remove unwanted fields from the main dictionary
    unwanted_fields = ['logo', 'radioLink', 'sog']
    for field in unwanted_fields:
        cleaned_stat.pop(field, None)

    # Extract team name
    if isinstance(cleaned_stat.get('name'), dict):
        cleaned_stat['name'] = cleaned_stat['name'].get('default', '')

    # Flatten away_team data
    away_team_data = cleaned_stat.pop('away_team', {})
    for key, value in away_team_data.items():
        new_key = f'away_{key}'
        if key == 'name' and isinstance(value, dict):
            cleaned_stat[new_key] = value.get('default', '')
        elif key not in unwanted_fields:  # Skip unwanted fields for away team
            cleaned_stat[new_key] = value

    return cleaned_stat

def clean_all_stats(all_game_stats):
    """Apply cleaning to all game statistics."""
    all_fieldnames = set()
    cleaned_stats = []

    for stats in all_game_stats:
        cleaned_stat = clean_stat_dict(stats)
        cleaned_stats.append(cleaned_stat)
        all_fieldnames.update(cleaned_stat.keys())

    return cleaned_stats, all_fieldnames

def write_stats_to_csv(cleaned_stats, fieldnames, filename):
    """Write cleaned statistics to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
        writer.writeheader()
        for stats in cleaned_stats:
            writer.writerow(stats)

def process_team_data(team):
    """ Process and save game data for a given team. """
    team_name = team['fullName']
    team_tri_code = team['triCode']
    print(f"Processing data for {team_name} (this could take a few minutes...)")

    schedule_endpoint = f"{NHL_API_BASE_URL}club-schedule-season/{team_tri_code}/{SEASON}"
    schedule_response = make_api_request(schedule_endpoint)

    if schedule_response:
        all_game_stats = []
        for game in schedule_response.get('games', []):
            game_data = fetch_game_data(game['id'])
            if game_data:
                home_stats, away_stats = extract_stats_from_game_data(game_data)
                game_stats = {**home_stats, 'away_team': away_stats}
                all_game_stats.append(game_stats)

        if all_game_stats:
            filename = f'{DATA_DIRECTORY}/{SEASON}_{team_name.replace(" ", "_")}_game_results.csv'
            cleaned_stats, all_fieldnames = clean_all_stats(all_game_stats)
            write_stats_to_csv(cleaned_stats, all_fieldnames, filename)
        else:
            print(f"No game stats found for {team_name}")
    else:
        print(f"Failed to fetch schedule for {team_name}")

def main():
    '''
    main entry point for the script
    '''
    print('Running NHL game data fetching script')
    team_data = fetch_team_data()
    if team_data and 'data' in team_data:
        for team in team_data['data']:
            process_team_data(team)
        print('*** Historical fetching completed ***')
    else:
        print("Failed to fetch team data.")

if __name__ == "__main__":
    main()

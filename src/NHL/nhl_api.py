"""
Module: nhl_data_fetch.py

This module provides functions for fetching NHL game data and standings from the NHL API.
"""

from datetime import date
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

NHL_API_BASE_URL = "https://api-web.nhle.com/v1/"

def safe_request(url, max_retries=3, backoff_factor=0.5, timeout=10):
    """
    Send a request to the specified URL and handle any potential errors.
    
    Args:
        url (str): The URL to send the request to.
        max_retries (int, optional): The maximum number of retries for failed 
        requests (default is 3).
        backoff_factor (float, optional): The factor by which 
        the retry delay increases between retries (default is 0.5).
        timeout (int, optional): The timeout for the request in seconds (default is 10).

    Returns:
        dict: The JSON response from the successful request or an 
        empty dictionary if the request fails.
    """
    session = requests.Session()
    retry = Retry(connect=max_retries, backoff_factor=backoff_factor)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}

def get_games_today():
    """
    Fetch games scheduled for the current day.
    
    Returns:
        list: A list of dictionaries containing information about today's games, 
        or an empty list if no games are scheduled.
    """
    current_date = date.today().strftime("%Y-%m-%d")
    schedule_endpoint = f"{NHL_API_BASE_URL}schedule/{current_date}"
    schedule_data = safe_request(schedule_endpoint)

    if schedule_data and 'gameWeek' in schedule_data:
        for day_info in schedule_data['gameWeek']:
            if day_info['date'] == current_date:  # Check if the date matches today's date
                games_today = day_info.get('games', [])
                return format_games_today_response(games_today)
    return []

def format_games_today_response(games_today):
    """
    Formats the response for today's games.
    
    Args:
        games_today (list): A list of game data for today's games.

    Returns:
        list: A list of dictionaries containing formatted information about today's games.
    """
    game_responses = []
    for game in games_today:
        game_id = game.get('id')
        venue = game.get('venue', {}).get('default', 'Unknown Venue')
        start_time_utc = game.get('startTimeUTC')
        away_team = game.get('awayTeam', {}).get('abbrev', 'Unknown Team')
        home_team = game.get('homeTeam', {}).get('abbrev', 'Unknown Team')

        formatted_game = {
            'game_id': game_id,
            'venue': venue,
            'start_time_utc': start_time_utc,
            'away_team': away_team,
            'home_team': home_team
        }
        game_responses.append(formatted_game)
    return game_responses

def get_current_standings():
    """
    Fetch the current NHL standings.

    Returns:
        list: A list of dictionaries containing current team standings.
    """
    standings_payload = safe_request(f"{NHL_API_BASE_URL}standings/now")
    current_standings = standings_payload['standings']
    return current_standings

"""
Module: game_predictions.py

This module provides functions for generating game predictions based on current team 
standings and game information.
"""
import datetime
from openai_actions import openai_formatting as ai_formatting
from openai_actions import openai_calls

def generate_game_predictions(games_today, current_standings):
    """
    Generate predictions for a list of games using current standings.

    Args:
        games_today (list): A list of dictionaries containing information 
        about the games to predict.
        current_standings (list): A list of dictionaries containing current team standings.

    Returns:
        list: A list of predictions for each game.
    """
    results = []
    for game in games_today:
        try:
            teams_info = get_teams_recent_info(game, current_standings)
            prediction_message = generate_game_prediction_message(game, teams_info)
            openai_message = ai_formatting.combine_contents_into_message(prediction_message)
            prediction = openai_calls.generate_chat_completions(openai_message)
            print(f'\n\n\n{prediction}')
            results.append(prediction)
        except Exception as e:
            print(f"Error predicting game: {str(e)}")
    return results

def generate_game_prediction_message(game, teams_info):
    """
    Generate a game prediction message based on game and team information.

    Args:
        game (dict): A dictionary containing information about the game.
        teams_info (tuple): A tuple containing home and away team information.

    Returns:
        str: A formatted game prediction message.
    """
    try:
        home_team_data, away_team_data = teams_info
        file_path = 'src/game_message_template.txt'

        # Read the content of the file
        with open(file_path, 'r', encoding="utf-8") as file:
            template_from_file = file.read()

        # Now format the template with the payload data
        formatted_text_from_file = template_from_file.format(
            home=game['home_team'],
            hWins=home_team_data['wins'],
            hLosses=home_team_data['losses'],
            hOTLosses=home_team_data['otLosses'],
            hL10W=home_team_data['l10Wins'],
            hL10L=home_team_data['l10Losses'],
            hGaL10=home_team_data['l10GoalsAgainst'],
            hGfL10=home_team_data['l10GoalsFor'],
            hGP=home_team_data['gamesPlayed'],
            homeGoalDiff=home_team_data['goalDifferential'],
            homeGoalDiffPerct=home_team_data['goalDifferentialPctg'],
            homeGoalsAgainst=home_team_data['goalAgainst'],
            homeGoalsFor=home_team_data['goalFor'],
            homeWinsHome=home_team_data['homeWins'],
            homeLossesHome=home_team_data['homeLosses'],
            homeStreakType=home_team_data['streakCode'],
            homeStreakLength=home_team_data['streakCount'],
            away=game['away_team'],
            aWins=away_team_data['wins'],
            aLosses=away_team_data['losses'],
            aOTLosses=away_team_data['otLosses'],
            aL10W=away_team_data['l10Wins'],
            aL10L=away_team_data['l10Losses'],
            aGaL10=away_team_data['l10GoalsAgainst'],
            aGfL10=away_team_data['l10GoalsFor'],
            aGP=away_team_data['gamesPlayed'],
            awayGoalDiff=away_team_data['goalDifferential'],
            awayGoalDiffPerct=away_team_data['goalDifferentialPctg'],
            awayGoalsAgainst=away_team_data['goalAgainst'],
            awayGoalsFor=away_team_data['goalFor'],
            awayWinsRoad=away_team_data['roadWins'],
            awayLossesRoad=away_team_data['roadLosses'],
            awayStreakType=away_team_data['streakCode'],
            awayStreakLength=away_team_data['streakCount'],
            venue=game['venue'],
            gameDate = datetime.date.today().strftime("%Y-%m-%d")
        )
        return formatted_text_from_file
    except Exception as ex:
        print(f'There was an error generating the game prediction: {ex}')
        return None

def get_teams_recent_info(game, current_standings):
    """
    Get recent information for the home and away teams from the current standings.

    Args:
        game (dict): A dictionary containing information about the game.
        current_standings (list): A list of dictionaries containing current team standings.

    Returns:
        tuple: A tuple containing information for the home and away teams.
    """
    # Find the home and away team data
    home_team_data = [item for item in current_standings if item.get('teamAbbrev', {}).get('default') == game['home_team']]
    away_team_data = [item for item in current_standings if item.get('teamAbbrev', {}).get('default') == game['away_team']]

    # Handling the case where no matching item is found for either team
    if not home_team_data:
        print("No data found for the home team.")
        home_team_info = None
    else:
        home_team_info = home_team_data[0]  # Assuming only one item is expected

    if not away_team_data:
        print("No data found for the away team.")
        away_team_info = None
    else:
        away_team_info = away_team_data[0]  # Assuming only one item is expected

    return home_team_info, away_team_info

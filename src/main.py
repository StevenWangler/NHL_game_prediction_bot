"""
Main script for generating NHL game predictions.

This script fetches today's NHL games and current team standings, and then generates predictions
for the games using the OpenAI API and other NHL data processing modules.
"""

from NHL import nhl_api as NHL
from NHL import game_processing
from general import general_functions

def main():
    """
    Main function to generate NHL game predictions.
    """
    predictions = game_processing.generate_game_predictions(
        NHL.get_games_today(),
        NHL.get_current_standings()
    )
    general_functions.write_predictions_to_file(predictions)

if __name__ == '__main__':
    main()

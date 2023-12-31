"""
This module provides functionality for processing and storing prediction data.

It includes two primary functions:

1. unique_predictions: This function is designed to remove duplicate dictionary objects 
from a given list of dictionaries. It is useful for ensuring that a collection of predictions 
does not contain any redundant data. This is achieved by serializing each dictionary to a JSON 
string and using a set to track and exclude duplicates.

2. write_predictions_to_file: This function takes a list of predictions 
(which could be in string or dictionary format) and writes them to a JSON file. 
Before writing to the file, it converts string predictions to dictionary objects, 
flattens the list if necessary, and removes any duplicates. This function is essential for
persisting prediction data in a structured and deduplicated format. It handles conversion
errors gracefully and provides user feedback through console messages.

The module is particularly useful in scenarios where prediction data needs to be collected, cleaned, 
and stored efficiently and accurately. It ensures data integrity and ease of access by storing the 
predictions in a JSON file.
"""

import json
import ast

def unique_predictions(predictions_list):
    """
    Removes duplicate dictionaries from a list of dictionaries.

    This function iterates over a list of dictionary objects, serializing
    each dictionary to a JSON string. It then checks whether the string
    representation of the dictionary has already been seen. If it has not,
    the dictionary is added to a unique list. This approach ensures that only 
    unique dictionary objects are retained.

    Args:
    predictions_list (list): A list of dictionary objects.

    Returns:
    list: A list containing only unique dictionary objects from the input list.
    """
    seen = set()
    unique_list = []
    for prediction in predictions_list:
        # Serialize the dictionary to a JSON string
        prediction_str = json.dumps(prediction, sort_keys=True)
        if prediction_str not in seen:
            seen.add(prediction_str)
            unique_list.append(prediction)
    return unique_list

def write_predictions_to_file(predictions, filename='src/predictions.json'):
    """
    Writes a list of predictions to a specified JSON file.

    This function processes a list of predictions by first attempting to convert
    each prediction into a dictionary object, if necessary. It handles any errors that occur
    during this conversion. After conversion, it flattens the list in case each element is a list.
    It then removes any duplicate dictionaries from this list and writes the unique predictions
    to a specified JSON file.

    Args:
    predictions (list): A list of predictions, which may be strings or dictionary objects.
    filename (str, optional): The name of the file to write the predictions to. Defaults to
    'predictions.json'.

    Raises:
    Exception: If an error occurs during the conversion of a prediction.

    Side Effects:
    - Prints messages to the console if conversion errors occur.
    - Creates or overwrites a JSON file with the specified filename.
    - Prints a success message upon writing to the file.
    """
    converted_predictions = []
    for prediction in predictions:
        try:
            # Attempt to convert the prediction
            converted_prediction = ast.literal_eval(prediction)
            converted_predictions.append(converted_prediction)
        except Exception as e:
            # Print the problematic prediction and the error
            print(f"Error converting prediction: {prediction}")
            print(f"Error: {e}")
            # Raise the error to stop execution or use 'continue' to skip
            raise

    # Flatten the list if each element is a list
    flat_predictions = [item for sublist in converted_predictions for item in sublist]

    # Remove duplicates
    unique_predictions_list = unique_predictions(flat_predictions)

    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(unique_predictions_list, file, ensure_ascii=False, indent=4)

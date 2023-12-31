"""
The "openai_formatting" module provides functions for formatting messages
intended for OpenAI models. Its primary purpose is to combine the contents 
of a file with a provided message and format the resulting message.
Additional functionalities related to message formatting for OpenAI may be added in the future.
"""

import os

def combine_contents_into_message(message):
    """
    Combine the contents of two strings and format the message.

    Args:
        message (str): The content of the message to be combined with the file contents.

    Returns:
        list: A list containing a dictionary with the combined and formatted message.

    This function reads the contents of a file located at a specific file path and combines 
    it with the provided 'message'. The resulting message is formatted as a list containing 
    a dictionary with a 'role' and 'content' key-value pair, suitable for use in some structured 
    communication format.
    If any errors occur during the process, the function returns None.
    """
    try:
        # Get the current working directory, which will be the project root in most cases
        base_path = os.getcwd()

        # Specify the path to your file
        file_path = os.path.join(base_path, "src", "gptInstrictions.txt")

        # Open the file in read mode ('r')
        with open(file_path, 'r', encoding="utf-8") as file:
            # Read the entire file contents into a string
            file_contents = file.read()

        # Prepare the message
        full_message = f'{file_contents}{message}'
        full_message = full_message.replace("\n", "\\n")
        full_message = full_message.strip()

        # Format the message as per the structure you showed
        message_object = [{"role": "user", "content": full_message}]

        return message_object
    except Exception as ex:
        print(f"An error occurred: {ex}")
        return None

'''
The open ai api calls file handles the chat completion
request to open ai. Also will handle any other api cals
to open ai.
'''

import os
import logging
import openai
openai.api_key = os.getenv('NHL_OPENAI_API_KEY')

MAX_RETRIES = 2
def generate_chat_completions(grading_criteria, model_name=os.getenv('NHL_ENGINE_NAME'), retries=0):
    '''
    Generate chat completions using OpenAI's chat completion endpoint.

    This function interfaces with the OpenAI API to get completions for chat messages 
    based on the provided grading criteria.

    Parameters:
    - grading_criteria (list): A list of message objects indicating the conversation 
                               history and user prompts.

    Returns:
    - str: The completed message content if successful.
    - None: If there's an error in calling the OpenAI endpoint.

    Raises:
    - openai.error.OpenAIError: If there's any issue in calling the OpenAI API.

    Example Usage:
    ```python
    criteria = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"}]
    message = generate_chat_completions(criteria)
    print(message)
    ```

    Note: Ensure that the OpenAI package is properly set up with necessary 
    API keys for this function to work.
    '''
    try:
        logging.info('Generating the chat completion message using model %s', model_name)

        #response = openai.ChatCompletion.create(
         #   model=model_name,
          #  messages=grading_criteria
        #)

        #completion_message = response.choices[0].message.content
        logging.info('Returning the completed message')
        #return completion_message

    except Exception as ex:
        logging.error('An error occurred while calling the OpenAI chat completion endpoint: %s', ex)
        if 'Rate limit reached' in str(ex) and retries < MAX_RETRIES:
            logging.info('Rate limit reached for model %s. Retrying with a different model...', model_name)
            return generate_chat_completions(grading_criteria, model_name=os.getenv('NHL_ENGINE_NAME'), retries=retries+1)

        return None

def get_assistant():
    """
    Fetches the ID of the assistant named 'NHL Game Prediction Assistant'.

    Returns:
        str: The ID of the 'NHL Game Prediction Assistant', or None if not found.
    """
    current_assistants = openai.beta.assistants.list()
    for assistant in current_assistants.data:
        if assistant.name == 'NHL Game Prediction Assistant':
            return assistant.id

    return None

def create_thread():
    """
    Creates a new conversation thread using the OpenAI Assistants API.

    Args:
        client (openai.OpenAI): The OpenAI client instance.

    Returns:
        openai.Thread: The created thread object.
    """
    thread = openai.beta.threads.create()
    return thread

def add_message_to_thread(thread_id, content):
    """
    Adds a message to a specific thread using the OpenAI Assistants API.

    Args:
        client (openai.OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread to which the message will be added.
        role (str): The role of the message sender ('user' or 'assistant').
        content (str): The content of the message.

    Returns:
        openai.ThreadMessage: The created message object.
    """
    message = openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    return message

def run_assistant_on_thread(thread_id, assistant_id, instructions=None):
    """
    Runs the assistant on a specific thread using the OpenAI Assistants API.

    Args:
        client (openai.OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread on which the assistant will run.
        assistant_id (str): The ID of the assistant to be used.
        instructions (str, optional): New instructions for this specific run, if any.

    Returns:
        openai.Run: The Run object created by executing the assistant.
    """
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions
    )
    return run

def check_run_status(thread_id, run_id):
    """
    Checks the status of a run on a specific thread using the OpenAI Assistants API.

    Args:
        client (openai.OpenAI): The OpenAI client instance.
        thread_id (str): The ID of the thread.
        run_id (str): The ID of the run to check.

    Returns:
        str: The status of the run ('queued', 'running', 'succeeded', 'failed', etc.).
    """
    run_status = openai.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    return run_status.status

def get_messages(thread_id):
    """
    Retrieves a list of messages from a specified thread using the OpenAI API.

    This function calls the OpenAI API to fetch all messages belonging to a given thread,
    identified by its unique thread ID. If the API call is successful, it returns a list of
    messages. In case of an error (such as a network issue or invalid thread ID), it catches
    the exception, prints an error message, and returns None.

    Parameters:
    thread_id (str): The unique identifier of the thread from which messages are to be retrieved.

    Returns:
    dict or None: Returns a dictionary containing the list of messages if the API call is successful.
                  Returns None if an error occurs during the API call.

    Raises:
    Exception: Outputs an error message to the console if an exception occurs during the API call.
    """
    try:
        return openai.beta.threads.messages.list(
            thread_id=thread_id
        )
    except Exception as e:
        print(f'Error getting messages! Error: {e}')
        return None

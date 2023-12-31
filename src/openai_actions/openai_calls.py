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

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=grading_criteria
        )

        completion_message = response.choices[0].message.content
        logging.info('Returning the completed message')
        return completion_message

    except Exception as ex:
        logging.error('An error occurred while calling the OpenAI chat completion endpoint: %s', ex)
        if 'Rate limit reached' in str(ex) and retries < MAX_RETRIES:
            logging.info('Rate limit reached for model %s. Retrying with a different model...', model_name)
            return generate_chat_completions(grading_criteria, model_name=os.getenv('NHL_ENGINE_NAME'), retries=retries+1)

        return None
    
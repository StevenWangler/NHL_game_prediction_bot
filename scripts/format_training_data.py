"""
This script processes an existing JSONL file, converting the data into a chat-completion 
format required for fine-tuning.
The processed data is then written to a new JSONL file.

Usage:
1. Specify the INPUT_FILE_PATH and OUTPUT_FILE_PATH.
2. Run this script to process the data and create a new JSONL file 
with the updated chat-completion format.
"""

import json

# Specify the paths to the input and output JSONL files
INPUT_FILE_PATH = 'data/consolidated_data/consolidated_training_data.jsonl'
OUTPUT_FILE_PATH = 'data/consolidated_data/final_consolidated_data_chat_format.jsonl'

# Define the desired encoding for reading and writing JSONL files
ENCODING = 'utf-8'

with open(INPUT_FILE_PATH, 'r', encoding=ENCODING) as input_file, open(OUTPUT_FILE_PATH, 'w', encoding=ENCODING) as output_file:
    for line in input_file:
        entry = json.loads(line)

        # Construct the chat-format messages
        SYSTEM_MESSAGE_CONTENT = '''You are an NHL statistics assistant that predicts the outcome
        of NHL games using your historical knowledge of the stats and outcome of games.'''

        USER_MESSAGE_CONTENT = "What was the outcome of the game?"

        # Create an assistant message that includes all the prompt data
        ASSISTANT_MESSAGE_CONTENT = ", ".join([f"{key.replace('_', ' ').title()}: {value}" for key, value in entry['prompt'].items()])

        # Add the game's outcome at the end of the assistant message
        ASSISTANT_MESSAGE_CONTENT += ". " + entry['completion']

        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE_CONTENT},
            {"role": "user", "content": USER_MESSAGE_CONTENT},
            {"role": "assistant", "content": ASSISTANT_MESSAGE_CONTENT}
        ]

        # Create the final entry with the messages array only
        final_entry = {"messages": messages}

        # Write the updated entry back to a new JSONL file
        output_file.write(json.dumps(final_entry, ensure_ascii=False) + '\n')

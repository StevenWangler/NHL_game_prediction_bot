from settings import app_secrets

# OpenAI data
OPENAI_API_KEY = app_secrets.OPENAI_API_KEY
ENGINE_NAME = f'{app_secrets.TUNED_ENGINE_NAME}'
CHAT_COMPLETIONS_URL = 'https://api.openai.com/v1/chat/completions'

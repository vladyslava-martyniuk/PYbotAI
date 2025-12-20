import os
from dotenv import load_dotenv
from settings_ai.abstract_ai import AIClient
from openai import OpenAI

load_dotenv()

class OpenAiClient(AIClient):
    def create_client(self):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY не встановлений у .env")
        return OpenAI(api_key=OPENAI_API_KEY)

import os

from dotenv import load_dotenv
from settings_ai.abstract_ai import AIClient
load_dotenv() 



from xai_sdk import Client
from xai_sdk.chat import user, system



class GroqAiClient(AIClient):
    def create_client(self):
        GROQ_API_KEY = os.getenv("XAI_API_KEY")

        if not GROQ_API_KEY:
            raise ValueError("XAI_API_KEY не встановлений у .env")

        return Client(
            api_key=GROQ_API_KEY,
            timeout=3600, # Override default timeout with longer timeout for reasoning models
        )
import os
from dotenv import load_dotenv
from openai import OpenAI

from settings_ai.abstract_ai import AIClient

# === ENV ===
load_dotenv()


class OpenAiClient(AIClient):
    def create_client(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY не встановлений у .env")

        return OpenAI(api_key=openai_api_key)

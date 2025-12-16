import os
from typing import List, Dict

from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import HTTPException
from openai import OpenAI
from abstract_ai import AIClient
# === ENV ===
load_dotenv()

class OpenAiClient(AIClient):
    def create_client(self):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY не встановлений у .env")

        return OpenAI(api_key=OPENAI_API_KEY)





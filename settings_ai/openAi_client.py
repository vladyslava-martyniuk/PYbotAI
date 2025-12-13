import os
from typing import List, Dict

from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import HTTPException
from openai import OpenAI

# === ENV ===
load_dotenv()

OPENAI_API_KEY_VALUE = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY_VALUE:
    raise ValueError("OPENAI_API_KEY не встановлений у .env")

client = OpenAI(api_key=OPENAI_API_KEY_VALUE)

BASE_URL = "https://api.openai.com/openai/v1/chat/completions"

# === ЗАПИТИ ДО ШТУЧНОГО ІНТЕЛЕКТУ ===
class AIRequest(BaseModel):
    query: str
    temperature: float = 0.7
    max_tokens: int = 150


class AIResponse(BaseModel):
    result: str


# === CHAT GPT (АКТУАЛЬНИЙ API) ===
def response_to_chatgpt(
    user_input: str,
    temperature: float = 0.7,
    max_tokens: int = 150
) -> str:
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_input,
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        return response.output_text

    except Exception as e:
        print(f"Помилка під час виклику API: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Помилка OpenAI API: {str(e)}"
        )

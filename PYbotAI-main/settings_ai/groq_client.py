import os
import requests
from dotenv import load_dotenv

load_dotenv() 

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(prompt: str, model: str = "llama3-70b-8192"):
    """
    Надсилає повідомлення до Groq API та повертає відповідь моделі.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY не знайдено у .env!")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(BASE_URL, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Groq API Error: {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]
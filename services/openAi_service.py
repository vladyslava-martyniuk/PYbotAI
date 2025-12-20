import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenAiService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY не встановлений у .env")
        # Створюємо клієнт
        self.client = OpenAI(api_key=api_key)

    def ask(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # або "gpt-4" якщо у тебе доступ
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Помилка API: {str(e)}"


import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        # Отримуємо ключ за назвою змінної з .env
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
             raise ValueError("API ключ не знайдено! Перевірте файл .env")
             
        genai.configure(api_key=api_key)
        # Використовуємо актуальну назву моделі
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def get_completion(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Помилка API: {e}")
            return f"Помилка ШІ: {str(e)}"

# ЦЕЙ КЛАС МАЄ БУТИ ОБОВ'ЯЗКОВО, ЩОБ main.py ЙОГО БАЧИВ
class AIHandleService:
    def __init__(self):
        self.client = GeminiClient()

    def process_message(self, user_text: str) -> str:
        return self.client.get_completion(user_text)
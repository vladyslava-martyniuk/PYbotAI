# services/groq_service.py
from settings_ai.groq_client import GroqAiClient

class GroqService:
    def __init__(self):
        # Ініціалізація нового Groq клієнта
        self.client = GroqAiClient().create_client()

    def send_request(self, model_name: str, prompt: str) -> str:
        try:
            # Новий формат SDK: author замість role
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[{"author": "user", "content": prompt}],
                max_output_tokens=150
            )
            # Витягуємо текст відповіді
            return response.choices[0].content[0].text
        except Exception as e:
            return f"Помилка сервера: {str(e)}"

    def ask(self, prompt: str) -> str:
        # Використовуємо модель Groq
        return self.send_request("groq-4", prompt)

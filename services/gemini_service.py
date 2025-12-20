from settings_ai.gemini_client import GeminiClient

class GeminiService:
    def __init__(self):
        self.client = GeminiClient()
    def send_request(self, model_name: str, prompt: str) -> str:
        try:
            response = self.client.responses.create(
                model=model_name,
                input=prompt
            )
            return response.output_text
        except Exception as e:
            return f"Помилка Gemini API: {str(e)}"
    def ask(self, prompt: str, model_name: str = "gemini-1", temperature: float = 0.7, max_tokens: int = 150) -> str:
        try:
            return self.client.generate(prompt)
        except Exception as e:
            return f"Помилка Gemini API: {str(e)}"

from services.ai_handle_service import AIHandleService

from settings_ai.groq_client import GroqAiClient
from xai_sdk.chat import user, system

class GroqService(AIHandleService):
    def __init__(self):
        super().__init__(GroqAiClient())

    def send_request(self, model_name: str, prompt: str) -> str:
        chat = self.client.chat.create(model="grok-4")
        chat.append(user("What is the meaning of life, the universe, and everything?"))
        response = chat.sample()
        print(response.content)

        return response.output_text
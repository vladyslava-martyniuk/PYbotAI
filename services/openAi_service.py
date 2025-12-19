from services.ai_handle_service import AIHandleService
from settings_ai.openAi_client import OpenAiClient


class OpenAiService(AIHandleService):
    def __init__(self):
        super().__init__(OpenAiClient())

    def send_request(self, model_name: str, prompt: str) -> str:
        response = self.client.responses.create(
            model=model_name,
            input=prompt
        )

        return response.output_text

from settings_ai.openAi_client import OpenAiClient

class OpenAiService:
    def __init__(self):
        self.client = OpenAiClient().create_client()

    def send_request(self, model_name: str, prompt: str) -> str:
        print("OpenAI Prompt:", prompt)
        response = self.client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        print("OpenAI Full response:", response)
        return response.choices[0].message.content

    def ask(self, prompt: str) -> str:
        return self.send_request("gpt-4", prompt)


from settings_ai.groq_client import GroqAiClient

class GroqService:
    def __init__(self):
        self.client = GroqAiClient().create_client()

    def send_request(self, model_name: str, prompt: str, temperature: float = 0.7, max_tokens: int = 150) -> str:
        print("Groq Prompt:", prompt)
        response = self.client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        print("Groq Full response:", response)
        return response.choices[0].message.content

    def ask(self, prompt: str) -> str:
        return self.send_request("groq-4", prompt)

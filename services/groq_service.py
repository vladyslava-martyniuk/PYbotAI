# from settings_ai.groq_client import GroqAiClient

# class GroqService:
#     def __init__(self):
#         self.client = GroqAiClient().create_client()

#     def send_request(self, model_name: str, prompt: str) -> str:
#         try:
#             response = self.client.chat.completions.create(
#                 model=model_name,
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": prompt}
#                 ]
#             )
#             return response.choices[0].message.content.strip()
#         except Exception as e:
#             return f"Помилка сервера: {str(e)}"

#     def ask(self, prompt: str) -> str:
#         # Використай офіційну модель Groq, наприклад:
#         return self.send_request("mixtral-8x7b-32768", prompt)

# import os
# from dotenv import load_dotenv
# from settings_ai.abstract_ai import AIClient
# from groq import Groq

# load_dotenv()

# class GroqAiClient(AIClient):
#     def create_client(self):
#         GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#         if not GROQ_API_KEY:
#             raise ValueError("GROQ_API_KEY не встановлений у .env")

#         # Офіційний клієнт Groq
#         return Groq(api_key=GROQ_API_KEY)

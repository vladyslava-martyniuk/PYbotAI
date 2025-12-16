from abc import ABC, abstractmethod
from settings_ai.abstract_ai import AIClient

class AIHandleService(ABC): 
    def __init__(self, client: AIClient) -> None:
        self.client = client

    @abstractmethod
    def send_request(self, model_name: str, prompt: str) -> str:
        pass
        
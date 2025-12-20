from abc import ABC, abstractmethod

class AIHandleService(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def send_request(self, model_name: str, prompt: str) -> str:
        pass

    def ask(self, prompt: str, model_name: str):
        return self.send_request(model_name, prompt)

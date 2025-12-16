from abc import ABC, abstractmethod

class AIClient(ABC):
    def __init__(self):
        self.__client = None

    @abstractmethod
    def create_client(self):
        pass
from abc import ABC, abstractmethod


class ILLMAgent(ABC):

    @abstractmethod
    def register_tool(self, function):
        pass

    @abstractmethod
    def handle_message(self, message):
        pass
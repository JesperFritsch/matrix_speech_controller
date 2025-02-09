from abc import ABC, abstractmethod
from typing import Dict, Any


class ILLMAgent(ABC):

    @abstractmethod
    def register_tool(self, function, **kwargs):
        """ Register a tool function to be used by the agent

        Args:
            function (function): a function with a docstring that describes what it does, its arguments and return value
            kwargs: parameter options for the function, for example: map_name=["patterns", "random"]
        """
        pass

    @abstractmethod
    def handle_message(self, message: str, system_info: Dict[str, Any]):
        """ let the agent handle a message

        Args:
            message (str): the message to handle
            system_info (dict): a dictionary with information about the system
        """
        pass

    @abstractmethod
    def reset_history(self):
        """ Reset the agent's history """
        pass
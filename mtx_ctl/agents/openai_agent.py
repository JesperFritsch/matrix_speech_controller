import logging
import os
import json

from pathlib import Path
from importlib import resources
from configparser import ConfigParser
from collections import deque
from typing import Dict, List

from openai import OpenAI

from mtx_ctl.utils import get_tool_definition
from mtx_ctl.agents.agent_interface import ILLMAgent

log = logging.getLogger(Path(__file__).stem)
config_file = resources.files("mtx_ctl").joinpath("config.ini")

# Open and read the config file
config = ConfigParser()
with config_file.open("r") as f:
    config.read_file(f)

api_key_var = config.get("openai", "api_key_var")
api_key = os.getenv(api_key_var, None)

if not api_key:
    raise ValueError(f"Environment variable '{api_key_var}' not found.")


class OpenAIAgent(ILLMAgent):
    def __init__(self, history_buffer_size=10):
        self._client = OpenAI(api_key=api_key)
        self._tools_info: Dict[str, Dict[str, Dict]] = {} # List of tool information, as openai api function schema
        self._tools_func: Dict[str, callable] = {} # Dictionary of function tools
        self._history_buffer = deque(maxlen=history_buffer_size)

    def reset_history(self):
        self._history_buffer.clear()

    def _add_to_history(self, message):
        self._history_buffer.append(message)

    def _get_history(self):
        return list(self._history_buffer)

    def _get_tools(self):
        return list(self._tools_info.values())

    def register_tool(self, function, **kwargs):
        """ Register a tool function to be used by the agent

        Args:
            function (_type_): a function with a docstring that describes what it does, its arguments and return value
            kwargs: parameter options for the function, for example: map_name=["patterns", "random"]
        """
        fn_info = get_tool_definition(function)
        for k, v in kwargs.items():
            fn_info["function"]["parameters"]["properties"][k]["enum"] = v
        self._tools_info[fn_info["function"]["name"]] = fn_info
        self._tools_func[fn_info["function"]["name"]] = function

    def process_tool_call(self, tool_call):
        fn = tool_call.function
        tool = self._tools_func[fn.name]
        call_id = tool_call.id
        result = tool(**json.loads(fn.arguments))
        result_text = result if result else ""
        tool_response = {
            "role": "tool",
            "tool_call_id": call_id,
            "content": result_text
        }
        self._add_to_history(tool_response)

    def process_tool_calls(self, tool_calls):
        tool_calls.sort(key=lambda x: "run last" in self._tools_info[x.function.name]["function"]["description"])
        for tool_call in tool_calls:
            self.process_tool_call(tool_call)

    def _create_system_message(self, system_info: Dict[str, str]):
        main_prompt = "You are a controller for a smart led screen, " \
        "the screen can run different applications, but only one at a time. " \
        "here is some information about the current state of the system:"
        return main_prompt + "\n".join([f"{k}: {v}" for k, v in system_info.items()])

    def handle_message(self, message, system_info):
        log.info("handling: %s" % message)
        system_prompt = self._create_system_message(system_info)
        messages = [{"role": "system", "content": system_prompt}]
        self._add_to_history({"role": "user", "content": message})
        messages.extend(self._get_history())
        completion = self._client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=messages,
            tools=self._get_tools(),
        )
        response = completion.choices[0].message
        self._add_to_history(response)
        if response.tool_calls:
            self.process_tool_calls(response.tool_calls)




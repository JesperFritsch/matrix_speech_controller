import os

from importlib import resources
from configparser import ConfigParser
from openai import OpenAI
from typing import Dict, List

from mtx_ctl.utils import get_func_info
from mtx_ctl.agents.agent_interface import ILLMAgent

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
    def __init__(self):
        self._client = OpenAI(api_key=api_key)
        self._tools_info: List[Dict[str, Dict]] = {} # List of tool information, as openai api function schema
        self._tools_func: Dict[str, callable] = {} # Dictionary of function tools

    def register_function(self, function):
        fn_info = get_func_info(function)
        fn_props = {}
        for param in fn_info["parameters"]:
            fn_props[param["name"]] = {
                    "type": param["type"],
                    "description": param["description"],
                }
            if "options" in param:
                fn_props[param["name"]]["options"] = param["options"]
        tool_info = {
            "name": fn_info["name"],
            "description": fn_info["description"],
            "parameters": {
                "type": "object",
                "properties": fn_props,
            }
        }
        self._tools_info[tool_info["name"]] = tool_info
        self._tools_func[tool_info["name"]] = function

    def handle_message(self, message):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[{"role": "user", "content": message}],
        )

        return completion.choices[0].message


client = OpenAI(
  api_key=api_key
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message)

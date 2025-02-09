import logging
import os
import json

from pathlib import Path
from collections import deque
from typing import Dict, List, Callable

from openai import OpenAI

from mtx_ctl.utils import get_tool_definition
from mtx_ctl.agents.agent_interface import ILLMAgent
from mtx_ctl.config import get_config

log = logging.getLogger(Path(__file__).stem)

config = get_config()

api_key_var = config.get("openai", "api_key_var")
api_key = os.getenv(api_key_var, None)

if not api_key:
    raise ValueError(f"Environment variable '{api_key_var}' not found.")


class OpenAIAgent(ILLMAgent):
    def __init__(self, history_buffer_size=30):
        self._client = OpenAI(api_key=api_key)
        self._tools_info: Dict[str, Dict[str, Dict]] = {} # List of tool information, as openai api function schema
        self._tools_func: Dict[str, Callable] = {} # Dictionary of function tools
        self._param_updaters: Dict[str, Dict[str, Callable]] = {} # Dictionary of parameter updaters for tools
        self._history_buffer = deque(maxlen=history_buffer_size)

    def reset_history(self):
        log.debug("resetting history")
        self._history_buffer.clear()

    def _add_to_history(self, message):
        self._history_buffer.appendleft(message)
        while self._history_buffer[-1]["role"] == "tool":
            self._history_buffer.pop()

    def _get_history(self):
        return list(reversed(self._history_buffer))

    def _get_tools(self):
        return list(self._tools_info.values())

    def _set_tool_param_options(self, tool_name, param_name, options):
        self._tools_info[tool_name]["function"]["parameters"]["properties"][param_name]["enum"] = options
        print(json.dumps(self._tools_info[tool_name], indent=2))

    def _normalize_message(self, message):
        if isinstance(message, dict):  # Already a dictionary
            return message
        normalized = {"role": message.role}
        normalized["content"] = message.content

        if hasattr(message, "tool_calls") and message.tool_calls:
            normalized["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                    "type": tool_call.type,
                }
                for tool_call in message.tool_calls
            ]

        return normalized

    def register_tool(self, function, **kwargs):
        """ Register a tool function to be used by the agent

        Args:
            function (_type_): a function with a docstring that describes what it does, its arguments and return value
            kwargs: key is a parameter name, value is a callable that returns the possible values for that parameter
        """
        fn_info = get_tool_definition(function)
        self._tools_info[fn_info["function"]["name"]] = fn_info
        self._tools_func[fn_info["function"]["name"]] = function
        for k, v in kwargs.items():
            if callable(v):
                self._param_updaters.setdefault(fn_info["function"]["name"], {})[k] = v
            else:
                self._set_tool_param_options(fn_info["function"]["name"], k, v)

    def _get_tool(self, tool_name):
        # Update parameter options if there are updaters
        if tool_name in self._param_updaters:
            for param_name, updater in self._param_updaters[tool_name].items():
                self._set_tool_param_options(tool_name, param_name, updater())
        return self._tools_func[tool_name]

    def process_tool_call(self, tool_call):
        fn = tool_call.function
        tool = self._get_tool(fn.name)
        print(f"tool description: {json.dumps(self._tools_info[fn.name], indent=2)}")
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
        print(f"processing tool calls: {[x.function.name for x in tool_calls]}")
        for tool_call in tool_calls:
            self.process_tool_call(tool_call)

    def _create_system_message(self, system_info: Dict[str, str]):
        main_prompt = "You are a controller for a smart led screen, " \
        "the screen can run different applications, but only one at a time. " \
        "if the current app is 'snakes', and you are asked to change somethings about the snakes, " \
        "then you should always restart the snakes unless you are told to not restart the snakes. " \
        "here is some information about the current state of the system:"
        return main_prompt + "\n".join([f"{k}: {v}" for k, v in system_info.items()])

    def handle_message(self, message, system_info):
        log.info("handling: %s" % message)
        system_prompt = self._create_system_message(system_info)
        messages = [{"role": "system", "content": system_prompt}]
        self._add_to_history({"role": "user", "content": message})
        messages.extend(self._get_history())
        print("HISTORY BEGIN")
        for m in messages:
            print(f"message:  {m}")
        print("HISTORY END")
        completion = self._client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=messages,
            tools=self._get_tools(),
        )
        response = completion.choices[0].message
        self._add_to_history(self._normalize_message(response))
        if response.tool_calls:
            self.process_tool_calls(response.tool_calls)




import logging

from pathlib import Path
from queue import Queue, Empty
from importlib import resources
from threading import Thread, Event

from configparser import ConfigParser
from mtx_ctl.speech_recognition import CommandListener
from mtx_ctl.logging_setup import log_setup
from mtx_ctl.agents.openai_agent import OpenAIAgent
from mtx_ctl.agents.agent_interface import ILLMAgent
from mtx_ctl import tools

log = logging.getLogger(Path(__file__).stem)

config_file = resources.files("mtx_ctl").joinpath("config.ini")
config = ConfigParser()
with config_file.open("r") as f:
    config.read_file(f)

def agent_worker(agent: ILLMAgent, queue: Queue, stop_event: Event):
    while not stop_event.is_set():
        cmd = queue.get()
        system_info = {
            "current_app": "pixelart",
            "nr_snakes": 4,
            "food": 10,
            "food_decay": 0,
            "map": "patterns"
        } # TODO get real system info
        agent.handle_message(cmd, system_info)

def main():
    log_setup(logging.INFO)
    agent = OpenAIAgent()
    agent.register_tool(tools.set_brightness)
    agent.register_tool(tools.set_app, app_name=["pixelart", "snakes"])
    agent.register_tool(tools.set_snake_count)
    agent.register_tool(tools.set_snake_food)
    agent.register_tool(tools.set_snake_map, map_name=["patterns", "items", "comps2", "comps"])
    agent.register_tool(tools.set_snake_food_decay)
    agent.register_tool(tools.restart_snakes)


    try:
        activates = list(map(str.strip, config["listener"]["activation_phrases"].split(',')))
        deactivates = list(map(str.strip, config["listener"]["deactivation_phrases"].split(',')))
        cmd_queue = Queue()
        listener = CommandListener(activates, deactivates)
        stop_event = Event()
        agent_thread = Thread(target=agent_worker, args=(agent, cmd_queue, stop_event))
        listener.listen(cmd_queue)
    except KeyboardInterrupt:
        print("keyboard interrupt main")
    except Exception as e:
        log.error(e, exc_info=True)
    finally:
        stop_event.set()


if __name__ == "__main__":
    main()

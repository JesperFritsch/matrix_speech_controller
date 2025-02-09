import logging

from pathlib import Path
from queue import Queue, Empty
from threading import Thread, Event

from mtx_ctl.config import get_config
from mtx_ctl.speech_recognition import CommandListener
from mtx_ctl.logging_setup import log_setup
from mtx_ctl.agents.openai_agent import OpenAIAgent
from mtx_ctl.agents.agent_interface import ILLMAgent
from mtx_ctl import tools
from mtx_ctl.matrix_conn import get_system_info, get_apps, get_snake_maps
config = get_config()


log = logging.getLogger(Path(__file__).stem)

def agent_worker(agent: ILLMAgent, queue: Queue, stop_event: Event):
    while not stop_event.is_set():
        cmd = queue.get()
        if cmd == "reset_history":
            agent.reset_history()
            continue
        system_info = get_system_info()
        agent.handle_message(cmd, system_info)

def main():
    log_setup(logging.INFO)
    agent = OpenAIAgent()
    agent.register_tool(tools.set_brightness)
    agent.register_tool(tools.set_app, app_name=get_apps)
    agent.register_tool(tools.set_snake_count)
    agent.register_tool(tools.set_snake_food)
    agent.register_tool(tools.set_snake_map, map_name=get_snake_maps)
    agent.register_tool(tools.set_snake_food_decay)
    agent.register_tool(tools.set_snakes_fps)
    agent.register_tool(tools.restart_snakes)
    agent.register_tool(tools.display_on)



    try:
        activates = list(map(str.strip, config["listener"]["activation_phrases"].split(',')))
        deactivates = list(map(str.strip, config["listener"]["deactivation_phrases"].split(',')))
        cmd_queue = Queue()
        listener = CommandListener(activates, deactivates)
        stop_event = Event()
        agent_thread = Thread(target=agent_worker, args=(agent, cmd_queue, stop_event))
        agent_thread.daemon = True
        agent_thread.start()
        listener.listen(cmd_queue)
    except KeyboardInterrupt:
        print("keyboard interrupt main")
    except Exception as e:
        log.error(e, exc_info=True)
    finally:
        stop_event.set()
        # agent_thread.join()


if __name__ == "__main__":
    main()

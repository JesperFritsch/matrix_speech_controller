
from configparser import ConfigParser
from importlib import resources

config_file = resources.files("mtx_ctl").joinpath("config.ini")

def get_config():
    config = ConfigParser()
    with config_file.open("r") as f:
        config.read_file(f)
    return config
import logging


def log_setup(log_level):
    log = logging.getLogger()
    logging.basicConfig(level=log_level)
    handler = logging.StreamHandler()
    log.addHandler(handler)

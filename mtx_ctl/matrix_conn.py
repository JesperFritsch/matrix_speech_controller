
import logging

from pathlib import Path

from mtx_ctl.utils import SingletonMeta
from mtx_ctl.config import get_config
from home_led_matrix.connection import ConnClient, Request, Response

config = get_config()

log = logging.getLogger(Path(__file__).stem)

class MatrixConn(metaclass=SingletonMeta):
    def __init__(self,
                host=config["matrix"]["host"],
                route_port=config["matrix"]["route_port"],
                sub_port=config["matrix"]["sub_port"]):
        self._conn_client = ConnClient(route_port, sub_port, host)

    def get(self, key):
        request = Request()
        request.get(key)
        resp = self._conn_client.request(request)
        if resp.errors:
            log.error("Get request had errors: %s" % resp.errors)
        else:
            return resp.gets.get(key)

    def set(self, key, value):
        request = Request()
        request.set(key, value)
        resp = self._conn_client.request(request)
        if resp.errors:
            log.error("Set request returned errors: %s" % resp.errors)
        else:
            return resp.sets.get(key)

    def action(self, key):
        request = Request()
        request.action(key)
        resp = self._conn_client.request(request)
        if resp.errors:
            log.error("Action request returned errors: %s" % resp.errors)
        else:
            return resp.actions.get(key)

    def request(self, request: Request):
        return self._conn_client.request(request)

def get_system_info():
    matrix_conn = MatrixConn()
    req = Request()
    req.get("all")
    resp = matrix_conn.request(req)
    info = resp.gets
    if info:
        info["snake_maps"].append("none")
    return info

def get_apps():
    matrix_conn = MatrixConn()
    req = Request()
    req.get("apps")
    resp = matrix_conn.request(req)
    return resp.gets.get("apps", ["snakes", "pixelart"])

def get_snake_maps():
    matrix_conn = MatrixConn()
    req = Request()
    req.get("snake_maps")
    resp = matrix_conn.request(req)
    return resp.gets.get("snake_maps", [])
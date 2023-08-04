# -*- coding: utf-8 -*-
from dataclasses import dataclass

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from kfc.configs import login_server
import json


# (host, port) |-> PoolServer
available_pool_servers = {}


@dataclass
class PoolServer:
    load: int


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kargs):
        self.render("../templates/index.html")


class LoginApplication(tornado.web.Application):
    def __init__(self):
        super().__init__(handlers=[
            (r"/", IndexHandler),
            (r"/register_pool_server", RegisterPoolServerHandler),
        ])


class RegisterPoolServerHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.authentication = False
        self.host = None
        self.port = None


    """
    {"pool_server_host": "localhost", "pool_server_port": 8080, "token": "qwerty"}
    """
    """
    {"number_of_websocket_connection": 100}
    """
    """ check jsonschema"""
    """change token"""
    def on_message(self, message):
        data = json.loads(message)
        if not self.authentication:
            if "pool_server_host" in data and \
               "pool_server_port" in data and \
               "token" in data and \
               data["token"] == "qwerty":
                available_pool_servers[(data["pool_server_host"], data["pool_server_port"])] = PoolServer(load=0)
                self.host = data["pool_server_host"]
                self.port = data["pool_server_port"]
                self.authentication = True
                self.write_message(json.dumps({ "success": True, "msg": "Authentication passed." }))
            else:
                self.write_message(json.dumps({ "success": False, "msg": "Authentication failed." }))
                self.close()

        else:
            if "number_of_websocket_connection" in data and \
               type(data["number_of_websocket_connection"]) == int:
                available_pool_servers[(self.host, self.port)].load = data["number_of_websocket_connection"]
                self.write_message(json.dumps({"success": True, "msg": "Load updated."}))
            else:
                self.write_message(json.dumps({ "success": False, "msg": "Load update failed." }))


    def on_close(self):
        del available_pool_servers[(self.host, self.port)]



def create_login_server(hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(LoginApplication())
    http_server.listen(port, address=hostname)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    create_login_server(login_server["host"], login_server["port"])


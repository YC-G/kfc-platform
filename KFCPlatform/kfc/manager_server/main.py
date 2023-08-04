# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from kfc.configs import manager_server
import json


available_session_servers = []


class ManagerHandler(tornado.web.RequestHandler):
    def get(self, *args, **kargs):
        self.write("Manager server is successfully generated.")


class RegisterSessionServerHandler(tornado.websocket.WebSocketHandler):
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
                available_session_servers[(data["pool_server_host"], data["pool_server_port"])] = PoolServer(load=0)
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
                available_session_servers[(self.host, self.port)].load = data["number_of_websocket_connection"]
                self.write_message(json.dumps({"success": True, "msg": "Load updated."}))
            else:
                self.write_message(json.dumps({ "success": False, "msg": "Load update failed." }))


    def on_close(self):
        del available_session_servers[(self.host, self.port)]


class ManagerApplication(tornado.web.Application):
    def __init__(self):
        super().__init__(handlers=[
            (r"/", ManagerHandler),
            (r"/register_session_server", RegisterSessionServerHandler),
        ])


class RegisterSessionServerHandler(tornado.web.RequestHandler):
    async def post(self, *args, **kwargs):
        # add pool server to available_pool_servers
        content_type = self.request.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            try:
                data = json.loads(self.request.body)
                # Process the JSON data as needed
                print(data)
                available_session_servers.append(data)
            except json.JSONDecodeError:
                self.set_status(400)
                self.write({'error': 'Invalid JSON data'})
        else:
            self.set_status(415)
            self.write({'error': 'Unsupported Media Type'})


def create_manager_server(hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(ManagerApplication())
    http_server.listen(port, address=hostname)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    create_manager_server(manager_server["host"], manager_server["port"])


# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from kfc.configs import manager_server, session_server
import json
import requests


class SessionServerHandler(tornado.web.RequestHandler):
    def get(self, *args, **kargs):
        self.write("Session server is successfully generated.")


class SessionApplication(tornado.web.Application):
    def __init__(self):
        super().__init__(handlers=[
            (r"/", SessionServerHandler),
        ])


def create_pool_server(hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(SessionApplication())
    http_server.listen(port, address=hostname)

    # post a http request to login_server
    url = f"http://{manager_server['host']}:{manager_server['port']}/register_session_server"
    data = {
        "hostname": manager_server['host'],
        "port": manager_server['port']
    }
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    if response.status_code == 200:
        print("POST request successful!")
        print("Response:", response.text)
    else:
        print(f"POST request failed with status code: {response.status_code}")

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    create_pool_server(session_server[0]["host"], session_server[0]["port"])

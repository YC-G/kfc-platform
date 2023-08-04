# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from kfc.configs import login_server, pool_servers
import json
import requests


class PoolServerHandler(tornado.web.RequestHandler):
    def get(self, *args, **kargs):
        self.write("Pool server is successfully generated.")


class PoolApplication(tornado.web.Application):
    def __init__(self):
        super().__init__(handlers=[
            (r"/", PoolServerHandler),
        ])


def create_pool_server(hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(PoolApplication())
    http_server.listen(port, address=hostname)

    # post a http request to login server
    url = f"http://{login_server['host']}:{login_server['port']}/register_pool_server"
    data = {
        "hostname": login_server['host'],
        "port": login_server['port']
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
    create_pool_server(pool_servers[0]["host"], pool_servers[0]["port"])

from argparse import ArgumentParser


# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import requests
import json


# parameters
available_pool_servers = []


class RegisterPoolServerHandler(tornado.web.RequestHandler):
    async def post(self, *args, **kwargs):
        # add pool server to available_pool_servers
        content_type = self.request.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            try:
                data = json.loads(self.request.body)
                # Process the JSON data as needed
                print(data)
                available_pool_servers.append(data)
            except json.JSONDecodeError:
                self.set_status(400)
                self.write({'error': 'Invalid JSON data'})
        else:
            self.set_status(415)
            self.write({'error': 'Unsupported Media Type'})


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kargs):
        self.render("templates/index.html")

# localhost:3030/


class PoolServerHandler(tornado.web.RequestHandler):
    def get(self, *args, **kargs):
        self.write("Pool server is successfully generated.")


class LoginApplication(tornado.web.Application):
    def __init__(self):
        super().__init__(handlers=[
            (r"/", IndexHandler),
            (r"/register_pool_server", RegisterPoolServerHandler),
        ])


class PoolApplication(tornado.web.Application):
    def __init__(self):
        super().__init__(handlers=[
            (r"/", PoolServerHandler),
        ])


def create_login_server(hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(LoginApplication())
    http_server.listen(port, address=hostname)
    tornado.ioloop.IOLoop.instance().start()


def create_pool_server(login_hostname, login_port, hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(PoolApplication())
    http_server.listen(port, address=hostname)

    # post a http request to login_hostname
    url = f"http://{login_hostname}:{login_port}/register_pool_server"
    data = {
        "hostname": hostname,
        "port": port
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


def create_manager_server(pool_servers, hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(ManagerApplication())
    http_server.listen(port, address=hostname)

    # post a http request to login_hostname
    url = f"http://{login_hostname}:{login_port}/register_pool_server"
    data = {
        "hostname": hostname,
        "port": port
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


def main():
    parser = ArgumentParser()
    parser.add_argument("server_type")
    parser.add_argument("hostname")
    parser.add_argument("port", type=int)

    parser.add_argument("--login-server-hostname")
    parser.add_argument("--login-server-port")

    args = parser.parse_args()

    if args.server_type == "login":
        create_login_server(args.hostname, args.port)

    elif args.server_type == "pool":
        create_pool_server(args.login_server_hostname, args.login_server_port, args.hostname, args.port)


if __name__ == "__main__":
    main()


# Run login server
# python3 main.py login localhost 3030
# Run pool server
# python3 main.py pool localhost 3031 --login-server-hostname localhost --login-server-port 3030

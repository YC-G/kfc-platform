# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

from tornado.options import define, options
from app.urls import login_urls
from app.configs import login_configs
from app.views.views_login import LoginHandler


# Define the port on which the service starts
define("login_port", type=int, default=8008)


class LoginApplication(tornado.web.Application):
    def __init__(self):
        handlers = login_urls
        settings = login_configs
        super(LoginApplication, self).__init__(handlers=[LoginHandler], **settings)





def create_login_server(hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(LoginApplication())
    http_server.listen(port, address=hostname)
    tornado.ioloop.IOLoop.instance().start()


def create_pool_server(hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(UserApplication())
    http_server.listen(port, address=hostname)
    tornado.ioloop.IOLoop.instance().start()


def create_manager_server(hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(UserApplication())
    http_server.listen(port, address=hostname)
    tornado.ioloop.IOLoop.instance().start()


def create_session_server(hostname, port):
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(UserApplication())
    http_server.listen(port, address=hostname)
    tornado.ioloop.IOLoop.instance().start()
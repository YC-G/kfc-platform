# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import requests
import json


if __name__ == "__main__":
    pass


# Run login server
# python3 main.py login localhost 3030
# Run pool server
# python3 main.py pool localhost 3031 --login-server-hostname localhost --login-server-port 3030

# -*- coding: utf-8 -*-
import os

root_path = os.path.dirname(__file__)
configs = dict(
    debug = True,
    template_path=os.path.join(root_path, "templates"),
    static_path=os.path.join(root_path, "static"),
    xsrf_cookies=True,
    # $ uuidgen
    cookie_secret="C6E4B14D-B9EE-48B1-8390-24C66948E677"
)

mysql_configs = dict(
    db_host="127.0.0.1",
    db_name="kfcplatform",
    db_port=3306,
    db_user="root",
    db_pwd="Gyc072503"
)
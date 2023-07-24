# -*- coding: utf-8 -*-
from app.views.views_login import LoginHandler as login

login_urls = [
    (r"/", login)
]

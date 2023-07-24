# -*- coding: utf-8 -*-

import tornado.web

class CommonHandler(tornado.web.RequestHandler):
    # clients-sent params
    @property
    def params(self):
        data = self.request.arguments
        data = {
            k: list(
                map(
                    lambda val: str(val, encoding="utf-8"),
                    v
                )
            )
            for k, v in data.items()
        }
        return data


    """
    # Return account name after log in
    @property
    def name(self):
        return self.get_secure_cookie('name', None)

    
    # Return user info
    @property
    def user(self):
        return CRUD.user(self.name)

    # 公共参数
    @property
    def common_data(self):
        return cdata
    """
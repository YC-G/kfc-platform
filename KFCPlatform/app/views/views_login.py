# -*- coding: utf-8 -*-
from app.views.views_common import CommonHandler
from app.tools.forms import LoginForm
from werkzeug.datastructures import MultiDict

class LoginHandler(CommonHandler):
    def get(self, *args, **kargs):
        data = dict(
            title="login"
        )
        self.render("login.html", data=data)

    # clients connect to the login server
    def on_open(self, request):
        try:
            self.waiters.add(self)
        except Exception as e:
            print(e)


    # full-duplex communication
    def on_message(self, message):
        # broadcast the message to all clients
        try:
            data = json.loads(message)
            data["dt"] = datetime.datetime_now().strftime("%Y-%m-%d %H:%M:%S")
            content = json.dumps(data)
            self.broadcast(self.waiters, content)
        except Exception as e:
            print(e)


    # disconnect
    def on_close(self):
        try:
            self.waiters.add(self)
        except Exception as e:
            print(e)
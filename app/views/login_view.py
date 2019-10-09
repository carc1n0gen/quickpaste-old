from flask import render_template
from app.views import BaseView


class LoginView(BaseView):
    methods = ['GET']

    def dispatch_request(self):
        return render_template('login.html')

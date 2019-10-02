from flask import render_template
from app.views import BaseView


class NotFoundView(BaseView):
    methods = ['GET']

    def dispatch_request(self, error):
        return render_template(
            '4xx.html', title='Not found',
            message='There doesn\'t seem to be a paste here',
            disabled=['clone', 'save'], body_class='about'
        ), 404

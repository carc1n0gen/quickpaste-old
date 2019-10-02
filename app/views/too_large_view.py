from flask import render_template, current_app
from app.views import BaseView


class TooLargeView(BaseView):
    methods = ['GET']

    def dispatch_request(self, error):
        return render_template(
            '4xx.html', title='Too many characters',
            message='Limit: {}'.format(current_app.config['MAX_PASTE_LENGTH']),
            disabled=['clone', 'save'], body_class='about'
        ), 413

from flask import render_template, current_app
from app.views import BaseView


class RateLimitView(BaseView):

    def dispatch_request(self, error):
        return render_template(
            '4xx.html', title='Too many requests',
            message='Limit: {}'.format(
                current_app.config.get('RATELIMIT_DEFAULT')
            ),
            disabled=['clone', 'save'], body_class='about'
        ), 429

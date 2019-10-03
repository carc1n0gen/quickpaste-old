import traceback
from flask import render_template, current_app, request
from flask_mail import Message
from app.create_app import mail
from app.views import BaseView


class UnknownErrorView(BaseView):

    def dispatch_request(self, error):
        tb = traceback.format_exc()
        try:
            mail.send(Message(
                subject='Error From {}'.format(request.host_url),
                recipients=[current_app.config['MAIL_RECIPIENT']],
                body=render_template('email/error.txt.jinja', tb=tb),
                html=render_template('email/error.html.jinja', tb=tb)
            ))
        except Exception:
            current_app.logger.error(f'Failed to send error email {tb}')

        return render_template(
            '5xx.html', title='Uh oh', message='Shit really hit the fan',
            disabled=['clone', 'save'], body_class='about'
        ), 500

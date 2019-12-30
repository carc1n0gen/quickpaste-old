import traceback
from pygments import highlight
from flask import render_template, current_app, request
from flask_mail import Message
from app.create_app import mail
from app.views import BaseView

text = """
# Uh Oh!

**Shit really hit the fan.  Some sort of unknown error just happened.**"""


class UnknownErrorView(BaseView):
    def __init__(self):
        super().__init__()
        self.text = highlight(text, self.markdown_lexer, self.html_formatter)
        self.count = text.count('\n') + 1

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
            pass  # Ignore, we're going to log it anyway

        current_app.logger.error(f'Unknown error: {tb}')
        return render_template(
            'view.html',
            text=self.text,
            lines=self.count
        ), 500

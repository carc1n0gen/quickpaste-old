import traceback
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import MarkdownLexer
from flask import url_for, render_template, request
from flask_wtf.csrf import CSRFError
from flask_mail import Message
from app.util import mail, text_or_redirect


unknown_error_text = """# Uh Oh!

**Shit really hit the fan.  Some sort of unknown error just happened.**"""


not_found_text = """# Not Found

**There doesn't seem to be anything here.**"""

rate_limit_text = """# Too Many Requests

**Limit: {}**"""

csrf_message = """# Bad Request

**{}**"""


def setup_handlers(app):
    @app.errorhandler(400)
    @text_or_redirect
    def bad_request(ex):
        return dict(
            status=400,
            message='400 missing text',
            url=url_for('paste.edit', _external=True)
        )

    @app.errorhandler(CSRFError)
    def missing_csrf(e):
        return render_template(
            'paste_show.html',
            text=highlight(csrf_message.format(e.description), MarkdownLexer(), HtmlFormatter()),
            lines=csrf_message.count('\n') + 1
        ), 400

    @app.errorhandler(404)
    def not_found(ex):
        return render_template(
            'paste_show.html',
            text=highlight(not_found_text, MarkdownLexer(), HtmlFormatter()),
            lines=not_found_text.count('\n') + 1,
        ), 404

    @app.errorhandler(429)
    def rate_limit(ex):
        text = rate_limit_text.format(app.config.get('RATELIMIT_DEFAULT'))
        return render_template(
            'paste_show.html',
            text=highlight(text, MarkdownLexer(), HtmlFormatter()),
            lines=text.count('\n') + 1
        ), 429

    if not app.debug:
        @app.errorhandler(500)
        @app.errorhandler(Exception)
        def unknown_error(ex):
            tb = traceback.format_exc()
            try:
                mail.send(Message(
                    subject=f'Error From {request.host_url}',
                    recipients=[app.config['MAIL_RECIPIENT']],
                    body=render_template('email/error.txt.jinja', tb=tb),
                    html=render_template('email/error.html.jinja', tb=tb)
                ))
            except Exception:
                pass  # Ignore, we're going to log it anyway

            app.logger.exception(f'Unknown error at endpoint: {request.full_path}')
            return render_template(
                'paste_show.html',
                text=highlight(unknown_error_text, MarkdownLexer(), HtmlFormatter()),
                lines=unknown_error_text.count('\n') + 1
            ), 500

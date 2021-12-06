import threading
import traceback
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import MarkdownLexer
from flask import url_for, render_template, request, redirect, copy_current_request_context
from flask_wtf.csrf import CSRFError
from flask_mail import Message
from app.util import mail


unknown_error_text = """# Uh Oh!

**Shit really hit the fan.  Some sort of unknown error just happened.**"""


not_found_text = """# Not Found

**There doesn't seem to be anything here.**"""

method_not_allowed_text = """# Method Not Allowed

**You can't do that here.**"""

rate_limit_text = """# Too Many Requests

**Limit: {}**"""

csrf_message = """# Bad Request

**{}**"""


def setup_handlers(app):
    @app.errorhandler(400)
    def bad_request(ex):
        if request.headers.get('Accept'):
            return '400 missing text', 400, {'Content-type': 'text/plain; charset=utf-8'}
        return redirect(url_for('paste.edit', _external=True))

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

    @app.errorhandler(405)
    def method_not_allowed(ex):
        return render_template(
            'paste_show.html',
            text=highlight(method_not_allowed_text, MarkdownLexer(), HtmlFormatter()),
            lines=method_not_allowed_text.count('\n') + 1,
        ), 405

    @app.errorhandler(429)
    def rate_limit(ex):
        text = rate_limit_text.format(app.config.get('RATELIMIT_DEFAULT'))
        return render_template(
            'paste_show.html',
            text=highlight(text, MarkdownLexer(), HtmlFormatter()),
            lines=text.count('\n') + 1
        ), 429

    @app.errorhandler(500)
    @app.errorhandler(Exception)
    def unknown_error(ex):
        @copy_current_request_context
        def send_message(message):
            try:
                mail.send(message)
            except Exception:
                pass  # Ignore, we're going to log it anyway

        tb = traceback.format_exc()
        message = Message(
            subject=f'Error From {request.host_url}',
            recipients=[app.config['MAIL_RECIPIENT']],
            body=render_template('email/error.txt.jinja', tb=tb),
            html=render_template('email/error.html.jinja', tb=tb)
        )
        thread = threading.Thread(target=send_message, args=(message,))
        thread.start()

        app.logger.exception(f'Unknown error at endpoint: {request.method} {request.full_path}')
        return render_template(
            'paste_show.html',
            text=highlight(unknown_error_text, MarkdownLexer(), HtmlFormatter()),
            lines=unknown_error_text.count('\n') + 1
        ), 500

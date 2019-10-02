
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_htmlmin import HTMLMIN
from werkzeug.contrib.fixers import ProxyFix
from app.util import mail, alembic, limiter
from app.repositories import db
from app.views import (
    EditView,
    PasteView,
    DownloadView,
    BadRequestView,
    NotFoundView,
    TooLargeView,
    RateLimitView,
    UnknownErrorView,
)
from app.commands import cleanup


def create_app():
    app = Flask('quickpaste')
    app.config.from_json('config.json')

    if app.config.get('BEHIND_PROXY'):
        # DO NOT DO THIS IN PROD UNLESS YOU SERVE THE APP BEHIND A
        # REVERSE PROXY!
        app.wsgi_app = ProxyFix(app.wsgi_app)

    handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=1024 * 1024)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.logger.addHandler(handler)

    HTMLMIN(app)
    db.init_app(app)
    alembic.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    app.add_url_rule('/', view_func=EditView.as_view('paste.edit'))
    app.add_url_rule(
        '/<string:hexhash>',
        view_func=PasteView.as_view('paste.view')
    )
    app.add_url_rule(
        '/<string:hexhash>.<string:extension>',
        view_func=PasteView.as_view('paste.view.extension')
    )
    app.add_url_rule(
        '/raw/<string:hexhash>',
        view_func=PasteView.as_view('paste.view.raw')
    )
    app.add_url_rule(
        '/raw/<string:hexhash>.<string:extension>',
        view_func=PasteView.as_view('paste.view.raw.extension')
    )
    app.add_url_rule(
        '/download/<string:hexhash>',
        view_func=DownloadView.as_view('paste.download')
    )
    app.add_url_rule(
        '/download/<string:hexhash>.<string:extension>',
        view_func=DownloadView.as_view('paste.download.extension')
    )

    app.register_error_handler(400, BadRequestView.as_view('bad_request'))
    app.register_error_handler(404, NotFoundView.as_view('not_found'))
    app.register_error_handler(413, TooLargeView.as_view('too_large'))
    app.register_error_handler(429, RateLimitView.as_view('rate_limit'))
    if not app.debug:
        app.register_error_handler(
            500,
            UnknownErrorView.as_view('unknown_error')
        )

    app.cli.add_command(cleanup, 'cleanup')

    return app

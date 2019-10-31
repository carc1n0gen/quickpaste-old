import uuid
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
    # LoginView
)
from app.commands import cleanup
from app.shortlink import shortlink


def create_app():
    cache_buster = uuid.uuid4()
    app = Flask('quickpaste')
    app.config.from_json('config.json')

    if app.debug:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
    shortlink.init_app(app)

    app.add_url_rule('/', view_func=EditView.as_view('paste.edit'))
    app.add_url_rule(
        '/<string:id>',
        view_func=PasteView.as_view('paste.view')
    )
    app.add_url_rule(
        '/<string:id>.<string:extension>',
        view_func=PasteView.as_view('paste.view.extension')
    )
    app.add_url_rule(
        '/raw/<string:id>',
        view_func=PasteView.as_view('paste.view.raw')
    )
    app.add_url_rule(
        '/raw/<string:id>.<string:extension>',
        view_func=PasteView.as_view('paste.view.raw.extension')
    )
    app.add_url_rule(
        '/download/<string:id>',
        view_func=DownloadView.as_view('paste.download')
    )
    app.add_url_rule(
        '/download/<string:id>.<string:extension>',
        view_func=DownloadView.as_view('paste.download.extension')
    )

    # app.add_url_rule(
    #     '/login',
    #     view_func=LoginView.as_view('login')
    # )

    app.register_error_handler(400, BadRequestView.as_view('bad_request'))
    app.register_error_handler(404, NotFoundView.as_view('not_found'))
    app.register_error_handler(413, TooLargeView.as_view('too_large'))
    app.register_error_handler(429, RateLimitView.as_view('rate_limit'))
    if not app.debug:
        app.register_error_handler(
            500,
            UnknownErrorView.as_view('unknown_error')
        )
        app.register_error_handler(
            Exception,
            UnknownErrorView.as_view('unknown_error_catchall')
        )

    app.cli.add_command(cleanup, 'cleanup')

    @app.context_processor
    def inject_globals():
        return dict(cache_buster=cache_buster)

    return app

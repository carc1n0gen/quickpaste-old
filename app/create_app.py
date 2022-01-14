import uuid
import json
from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask import Flask, g
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
from app.util import mail, limiter
from app.errorhandlers import setup_handlers
from app.logging import init_logging, LOG_FORMAT
from app.cli import create_cli
from app.views import PasteEdit, LiveHighlight, PasteShow, PasteRaw, PasteDownload, PasteDelete, SocialBanner


def create_app():
    init_logging()
    cache_buster = uuid.uuid4()
    app = Flask('quickpaste')
    app.config.from_file('config.json', json.load)
    handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=1024 * 1024)
    handler.setFormatter(Formatter(LOG_FORMAT))
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    CSRFProtect(app)
    mail.init_app(app)
    limiter.init_app(app)

    if app.debug:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    if app.config.get('BEHIND_PROXY'):
        # DO NOT DO THIS IN PROD UNLESS YOU SERVE THE APP BEHIND A
        # REVERSE PROXY!
        app.wsgi_app = ProxyFix(app.wsgi_app)

    setup_handlers(app)
    app.add_url_rule('/', view_func=PasteEdit.as_view('paste.edit'))
    app.add_url_rule('/highlight', view_func=LiveHighlight.as_view('paste.highlight'))
    app.add_url_rule('/<string:id>', view_func=PasteShow.as_view('paste.show'))
    app.add_url_rule('/<string:id>.<string:extension>', 'paste.show')
    app.add_url_rule('/raw/<string:id>', view_func=PasteRaw.as_view('paste.raw'))
    app.add_url_rule('/raw/<string:id>.<string:extension>', 'paste.raw')
    app.add_url_rule('/download/<string:id>', view_func=PasteDownload.as_view('paste.download'))
    app.add_url_rule('/download/<string:id>.<string:extension>', 'paste.download')
    app.add_url_rule('/<string:id>/delete', view_func=PasteDelete.as_view('paste.delete'))
    app.add_url_rule('/<string:id>/social-banner.jpg', view_func=SocialBanner.as_view('paste.social_banner'))
    app.add_url_rule('/<string:id>/<string:extension>/social-banner.jpg', 'paste.social_banner')

    @app.after_request
    def after_request_func(response):
        if 'csrf_token' in g:
            response.headers['CSRF_TOKEN'] = g.csrf_token
        return response

    @app.context_processor
    def inject_globals():
        return dict(cache_buster=cache_buster)

    @app.teardown_appcontext
    def teardown(err_or_request):
        mongo_client = g.pop('mongo_client', None)
        if mongo_client:
            mongo_client.close()

    create_cli(app)

    return app

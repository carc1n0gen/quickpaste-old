import uuid
from logging.handlers import RotatingFileHandler
from flask import Flask, g
from werkzeug.middleware.proxy_fix import ProxyFix
from app.util import mail, limiter, configure_mongo
from app.errorhandlers import setup_handlers
from app.cli import create_cli
from app.views import PasteEdit, LiveHighlight, PasteShow, PasteRaw, PasteDownload


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

    mail.init_app(app)
    limiter.init_app(app)

    setup_handlers(app)

    app.add_url_rule('/', view_func=PasteEdit.as_view('paste.edit'))
    app.add_url_rule('/highlight', view_func=LiveHighlight.as_view('paste.highlight'))
    app.add_url_rule('/<string:id>', view_func=PasteShow.as_view('paste.show'))
    app.add_url_rule('/<string:id>.<string:extension>', 'paste.show')
    app.add_url_rule('/raw/<string:id>', view_func=PasteRaw.as_view('paste.raw'))
    app.add_url_rule('/raw/<string:id>.<string:extension>', 'paste.raw')
    app.add_url_rule('/download/<string:id>', view_func=PasteDownload.as_view('paste.download'))
    app.add_url_rule('/download/<string:id>.<string:extension>', 'paste.download')

    @app.context_processor
    def inject_globals():
        return dict(cache_buster=cache_buster)

    @app.teardown_appcontext
    def teardown(err_or_request):
        mongo = g.pop('mongo', None)
        if mongo:
            mongo.close()

    with app.app_context():
        configure_mongo(app)

    create_cli(app)

    return app

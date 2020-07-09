from logging.config import dictConfig

LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'

LOG_CONFIG = {
    'version': 1,
    'formatters': {'default': {
        'format': LOG_FORMAT,
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}


def init_logging():
    dictConfig(LOG_CONFIG)

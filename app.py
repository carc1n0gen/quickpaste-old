import time
import sqlite3
import hashlib
from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_htmlmin import HTMLMIN
from flask_assets import Environment, Bundle
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import guess_lexer, get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from werkzeug.contrib.fixers import ProxyFix


app = Flask('quickpaste')
app.config.from_pyfile('config.py')

if app.config.get('BEHIND_PROXY'):
    # DO NOT DO THIS IN PROD UNLESS YOU SERVE THE APP BEHIND A REVERSE PROXY!
    app.wsgi_app = ProxyFix(app.wsgi_app)

HTMLMIN(app)
assets = Environment(app)
limiter = Limiter(
    app,
    key_func=get_remote_address
)

js = Bundle('js/main.js', output='bundle.js')
css = Bundle('css/normalize.css', 'css/highlight.css', 'css/fontello.css', 'css/styles.css', output='bundle.css')
assets.register('js_all', js)
assets.register('css_all', css)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DB_PATH'])
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def respond_with_redirect_or_text(redirect, text, status=200):
    respond_with = request.headers.get('X-Respondwith')
    if (respond_with == 'link'):
        return (text, status)
    return redirect


def insert_text(text):
    hash = hashlib.md5(text.encode('utf-8'))
    conn = get_db()
    result = conn.execute("SELECT * FROM pastes WHERE hash = :hash", {
        'hash': hash.digest()
    })
    if result.fetchone() is None:
        conn.execute("INSERT INTO pastes VALUES (:hash, :text, :timestamp)", {
            'hash': hash.digest(),
            'text': text,
            'timestamp': time.time()
        })
        conn.commit()
    return hash.hexdigest()


def get_text(hexhash):
    try:
        binhash = bytes.fromhex(hexhash)
    except ValueError:
        return None

    conn = get_db()
    result = conn.execute('SELECT * FROM pastes WHERE hash = :hash', {
        'hash': binhash
    })
    item = result.fetchone()
    if item is None:
        return None
    return item[1]


@app.errorhandler(429)
def ratelimit_handler(e):
    respond_with = request.headers.get('X-Respondwith')
    if respond_with == 'link':
        return ('Too many requests. Limit 1 per 1 second.\n', 429)
    return render_template('4xx.html', title='Too many requests', message='Limit 1 per 1 second'), 429


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        if text is None or text.strip() == '':
            return respond_with_redirect_or_text(redirect(url_for('index')),
                '400 Missing text\n', 400)
        hexhash = insert_text(text)
        return respond_with_redirect_or_text(
            redirect(url_for('view', hash=hexhash)), '{}{}\n'.format(request.host_url, hexhash), 200)
    return render_template('index.html')


@app.route('/<string:hash>', methods=['GET'])
@app.route('/<string:hash>.<string:extension>', methods=['GET'])
def view(hash, extension=None):
    text = get_text(hash)
    if text is None:
        return render_template('4xx.html', title='Not found', message='There doesn\'t seem to be a paste here'), 404
    try: 
        lexer = get_lexer_for_filename('foo.{}'.format(extension))
    except ClassNotFound:
        lexer = guess_lexer(text)
    lines = len(text.splitlines())
    return render_template('view.html', text=highlight(text, lexer, HtmlFormatter()), lines=lines)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', host_url=request.host_url)


if __name__ == '__main__':
    app.run()

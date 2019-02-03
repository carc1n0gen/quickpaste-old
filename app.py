import time
import sqlite3
import hashlib
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
from werkzeug.exceptions import NotFound, BadRequest, RequestEntityTooLarge


app = Flask('quickpaste')
app.config.from_pyfile('config.py')

if app.config.get('BEHIND_PROXY'):
    # DO NOT DO THIS IN PROD UNLESS YOU SERVE THE APP BEHIND A REVERSE PROXY!
    app.wsgi_app = ProxyFix(app.wsgi_app)

HTMLMIN(app)
assets = Environment(app)
limiter = Limiter(app, key_func=get_remote_address)
assets.register('js_all', Bundle(
    'js/main.js', filters='jsmin', output='bundle.js'))
assets.register('css_all', Bundle(
    'css/normalize.css', 'css/highlight.css', 'css/fontello.css',
    'css/styles.css', filters='cssmin', output='bundle.css'))


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


def insert_text(text):
    hash = hashlib.md5(text.encode('utf-8'))
    conn = get_db()
    result = conn.execute(
        "SELECT * FROM pastes WHERE hash = ?", [hash.digest()])
    if result.fetchone() is None:
        conn.execute("INSERT INTO pastes VALUES (?, ?, ?)",
                     [hash.digest(), text, time.time()])
        conn.commit()
    return hash.hexdigest()


def get_text(hexhash):
    try:
        binhash = bytes.fromhex(hexhash)
    except ValueError:
        raise NotFound()
    conn = get_db()
    result = conn.execute('SELECT * FROM pastes WHERE hash=?', [binhash])
    item = result.fetchone()
    if item is None:
        return None
    return item[1]


def respond_with_redirect_or_text(redirect, text, status=200):
    respond_with = request.headers.get('X-Respondwith')
    if (respond_with == 'link'):
        return (text, status, {'Content-type': 'text/plain'})
    return redirect


@app.errorhandler(400)
def bad_request(e):
    respond_with_redirect_or_text(redirect('/'), '400 missing text\n', 400)


@app.errorhandler(404)
def not_found(e):
    render_template(
        '4xx.html', title='Not found',
        message='There doesn\'t seem to be a paste here'), 404


@app.errorhandler(413)
def too_large(e):
    render_template(
        '4xx.html', title='Too many characters',
        message='Limit: {}'.format(app.config['MAX_PASTE_LENGTH'])), 413


@app.errorhandler(429)
def rate_limit(e):
    render_template(
        '4xx.html', title='Too many requests',
        message='Limit: {}'.format(app.config.get('RATELIMIT_DEFAULT'))), 429


@app.errorhandler(500)
def internal_error(e):
    render_template(
        '5xx.html', title='Uh oh', message='Shit really hit the fan'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        maxlength = app.config.get('MAX_PASTE_LENGTH')
        text = request.form.get('text')
        if text is None or text.strip() == '':
            raise BadRequest()
        elif maxlength is not None and len(text) > maxlength:
            raise RequestEntityTooLarge()
        hexhash = insert_text(text)
        return respond_with_redirect_or_text(
            redirect(url_for('view', hexhash=hexhash)), '{}{}\n'.format(
                request.host_url, hexhash), 200)
    return render_template('index.html')


@app.route('/<string:hexhash>', methods=['GET'])
@app.route('/<string:hexhash>.<string:extension>', methods=['GET'])
def view(hexhash, extension=None):
    text = get_text(hexhash)
    try:
        lexer = get_lexer_for_filename('foo.{}'.format(extension))
    except ClassNotFound:
        lexer = guess_lexer(text)
    lines = len(text.splitlines())
    return render_template(
        'view.html', text=highlight(text, lexer, HtmlFormatter()), lines=lines)


@app.route('/about', methods=['GET'])
def about():
    return render_template(
        'about.html', host_url=request.host_url, body_class='about')

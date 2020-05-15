from urllib.parse import urlencode
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_for_filename
from pygments.util import ClassNotFound
from flask import Blueprint, abort, make_response, request
from app.util import templated, about_text
from app.repositories import paste


view_bp = Blueprint('view', __name__)


@view_bp.route('/<string:id>')
@view_bp.route('/<string:id>.<string:extension>')
@templated()
def view(id, extension=None):
    if id == 'about':
        doc = {'text': about_text}
    else:
        doc = paste.get_paste(id)

    if doc is None:
        abort(404)

    highlighted = request.args.get('h')
    if highlighted:
        highlighted = highlighted.split(' ')

    try:
        lexer = get_lexer_for_filename('foo.{}'.format(extension))
    except ClassNotFound:
        lexer = guess_lexer(doc['text'])

    if id == 'about':
        title = '/about.md'
        days_left = None
    elif doc['delete_at'] is None:
        title = f'{request.path}{urlencode(request.args)}'
        days_left = None
    else:
        title = f'{request.path}{urlencode(request.args)}'
        days_left = (doc['delete_at'] - doc['created_at']).days

    return dict(
        id=id,
        text=highlight(doc['text'], lexer, HtmlFormatter()),
        text_raw=doc['text'],
        days_left=days_left,
        extension=extension,
        lines=doc['text'].count('\n') + 1,
        highlighted=highlighted,
        title=title,
        title_link=request.url
    )


@view_bp.route('/raw/<string:id>')
@view_bp.route('/raw/<string:id>.<string:extension>')
def view_raw(id, extension=None):
    if id == 'about':
        doc = {'text': about_text}
    else:
        doc = paste.get_paste(id)

    if doc is None:
        abort(404)

    return (doc['text'], 200, {
        'Content-type': 'text/plain; charset=utf-8',
        'X-Content-Type-Options': 'nosniff'
    })


@view_bp.route('/download/<string:id>')
@view_bp.route('/download/<string:id>.<string:extension>')
def view_download(id, extension='txt'):
    if id == 'about':
        doc = {'text': about_text}
    else:
        doc = paste.get_paste(id)

    if doc is None:
        abort(404)

    res = make_response(doc['text'])
    res.headers['Content-Disposition'] = \
        f'attachment; filename={id}.{extension}'
    res.headers['Content-type'] = 'text/plain; charset=utf-8'
    return res

from urllib.parse import urlencode
from datetime import datetime, timedelta
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, get_lexer_for_filename
from pygments.util import ClassNotFound
from flask import Blueprint, abort, make_response, request, current_app
from app.util import templated, about_text
from app.repositories import paste


view_bp = Blueprint('view', __name__)


@view_bp.route('/<string:id>')
@view_bp.route('/<string:id>.<string:extension>')
@templated()
def view(id, extension=None):
    if id == 'about':
        text = about_text
    else:
        text, created_at = paste.get_paste(id)

    if text is None:
        abort(404)

    highlighted = request.args.get('h')
    if highlighted:
        highlighted = highlighted.split(' ')

    try:
        lexer = get_lexer_for_filename('foo.{}'.format(extension))
    except ClassNotFound:
        lexer = guess_lexer(text)

    if id == 'about':
        title = '/about.md'
        days_left = None
    else:
        title = f'{request.path}{urlencode(request.args)}'
        seconds = current_app.config.get('PASTE_EXPIRE_AFTER_SECONDS', 604800)
        now = datetime.utcnow()
        delete_time = datetime.utcnow() + timedelta(seconds=seconds)
        days_left = (delete_time - now).days

    return dict(
        id=id,
        text=highlight(text, lexer, HtmlFormatter()),
        text_raw=text,
        days_left=days_left,
        extension=extension,
        lines=text.count('\n') + 1,
        highlighted=highlighted,
        title=title,
        title_link=request.url
    )


@view_bp.route('/raw/<string:id>')
@view_bp.route('/raw/<string:id>.<string:extension>')
def view_raw(id, extension=None):
    if id == 'about':
        text = about_text
    else:
        text, _ = paste.get_paste(id)

    if text is None:
        abort(404)

    return (text, 200, {
        'Content-type': 'text/plain; charset=utf-8',
        'X-Content-Type-Options': 'nosniff'
    })


@view_bp.route('/download/<string:id>')
@view_bp.route('/download/<string:id>.<string:extension>')
def view_download(id, extension='txt'):
    if id == 'about':
        text = about_text
    else:
        text, _ = paste.get_paste(id)
    res = make_response(text)
    res.headers['Content-Disposition'] = f'attachment; filename={id}.{extension}'
    res.headers['Content-type'] = 'text/plain; charset=utf-8'
    return res

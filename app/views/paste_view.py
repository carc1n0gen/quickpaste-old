from flask import request, abort, render_template
from werkzeug.exceptions import NotFound
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from app.views import BaseView
from app.repositories import paste


class PasteView(BaseView):
    methods = ['GET']

    def dispatch_request(self, hexhash, extension=None):
        text = paste.get_paste(hexhash)
        if text is None:
            raise NotFound()

        if 'raw' in request.endpoint:
            return (text, 200, {'Content-type': 'text/plain; charset=utf-8'})

        highlighted = request.args.get('h')
        if highlighted:
            highlighted = highlighted.split(',')

        try:
            lexer = get_lexer_for_filename('foo.{}'.format(extension))
        except ClassNotFound:
            lexer = guess_lexer(text)
        lines = text.count('\n') + 1
        return render_template(
            'view.html',
            hexhash=hexhash,
            extension=extension,
            text=highlight(text, lexer, HtmlFormatter()),
            lines=lines,
            disabled=['save'], highlighted=highlighted
        )
import datetime
from urllib.parse import urlencode
from flask import request, abort, render_template, current_app
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_for_filename
from pygments.util import ClassNotFound
from app.views import BaseView
from app.repositories import paste
from app.shortlink import shortlink
from app.util import about_text


class PasteView(BaseView):
    methods = ['GET']

    def dispatch_request(self, id, extension=None):
        if id == 'about':
            text = about_text
            timestamp = None
        else:
            try:
                int_id = shortlink.decode(id)
            except ValueError:
                current_app.logger.info('Invalid shortlink found.')
                abort(404)
            text, timestamp = paste.get_paste(int_id)

        if text is None:
            abort(404)

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

        days_left = None
        if timestamp:
            now = datetime.datetime.now()
            created = datetime.datetime.fromtimestamp(timestamp)
            will_delete_at = created + datetime.timedelta(weeks=1)
            days_left = (will_delete_at - now).days

        if id == 'about':
            title = 'quickpaste'
            title_link = '/about.md'
        else:
            title = request.host + request.path + urlencode(request.args)
            title_link = request.url

        return render_template(
            'view.html',
            id=id,
            extension=extension,
            text=highlight(text, lexer, self.html_formatter),
            text_raw=text,
            lines=lines,
            highlighted=highlighted,
            days_left=days_left,
            title=title,
            title_link=title_link
        )

from urllib.parse import urlencode
from flask import request, render_template
from flask.views import View
from app.repositories import paste
from app.util import highlight
from app.helpers import abort_if


class PasteShow(View):
    methods = ['GET']

    def dispatch_request(self, id, extension=None):
        doc = paste.get_paste(id)
        abort_if(doc is None, 404)
        highlighted = request.args.get('h')
        if highlighted:
            highlighted = highlighted.split(' ')

        if doc['delete_at'] is None:
            title = f'{request.path}{urlencode(request.args)}'
            days_left = None
        else:
            title = f'{request.path}{urlencode(request.args)}'
            days_left = (doc['delete_at'] - doc['created_at']).days

        return render_template(
            'paste_show.html',
            id=id,
            text=highlight(doc['text'], extension),
            text_raw=doc['text'],
            days_left=days_left,
            extension=extension,
            lines=doc['text'].count('\n') + 1,
            highlighted=highlighted,
            title=title,
            title_link=request.url
        )

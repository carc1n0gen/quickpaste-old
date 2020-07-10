from flask import abort, make_response
from flask.views import View
from app.repositories import paste
from app.util import about_text


class PasteDownload(View):
    methods = ['GET']

    def dispatch_request(self, id, extension='txt'):
        if id == 'about':
            doc = {'text': about_text}
        else:
            doc = paste.get_paste(id)

        if doc is None:
            abort(404)

        res = make_response(doc['text'])
        res.headers['Content-Disposition'] = f'attachment; filename={id}.{extension}'
        res.headers['Content-type'] = 'text/plain; charset=utf-8'
        return res

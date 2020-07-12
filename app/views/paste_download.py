from flask import abort, make_response
from flask.views import View
from app.repositories import paste


class PasteDownload(View):
    methods = ['GET']

    def dispatch_request(self, id, extension='txt'):
        doc = paste.get_paste(id)
        if doc is None:
            abort(404)

        res = make_response(doc['text'])
        res.headers['Content-Disposition'] = f'attachment; filename={id}.{extension}'
        res.headers['Content-type'] = 'text/plain; charset=utf-8'
        return res

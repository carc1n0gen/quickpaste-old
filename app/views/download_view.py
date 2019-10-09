from flask import make_response, abort
from app.views import BaseView
from app.repositories import paste


class DownloadView(BaseView):
    methods = ['GET']

    def dispatch_request(self, hexhash, extension='txt'):
        text, _ = paste.get_paste(hexhash)
        if text is None:
            abort(404)

        res = make_response(text)
        res.headers['Content-Disposition'] = \
            f'attachment; filename={hexhash}.{extension}'
        res.headers['Content-type'] = 'text/plain; charset=utf-8'
        return res

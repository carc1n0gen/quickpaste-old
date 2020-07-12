from flask import abort
from flask.views import View
from app.repositories import paste


class PasteRaw(View):
    methods = ['GET']

    def dispatch_request(self, id, extension=None):
        doc = paste.get_paste(id)
        if doc is None:
            abort(404)

        return (doc['text'], 200, {
            'Content-type': 'text/plain; charset=utf-8',
            'X-Content-Type-Options': 'nosniff'
        })

from flask import url_for
from app.views import BaseView


class BadRequestView(BaseView):
    methods = ['GET']

    def dispatch_request(self, error):
        return self.redirect_or_text(
            url_for('paste.edit'),
            '400 missing text\n',
            400
        )

from flask import url_for
from app.views import BaseView


class BadRequestView(BaseView):

    def dispatch_request(self, error):
        return self.redirect_or_text(
            url_for('paste.edit', _external=True),
            400,
            '400 missing text',
        )

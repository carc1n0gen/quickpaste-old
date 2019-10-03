from flask import request, current_app, url_for, render_template
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
from app.views import BaseView
import app.repositories.paste as paste


class EditView(BaseView):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            maxlength = current_app.config.get('MAX_PASTE_LENGTH')
            text = request.form.get('text')

            if text is None or text.strip() == '':
                raise BadRequest()
            elif maxlength is not None and len(text) > maxlength:
                raise RequestEntityTooLarge()

            hexhash = paste.insert_paste(text)
            return self.redirect_or_text(
                url_for('paste.view', hexhash=hexhash, _external=True),
                200
            )

        text = paste.get_paste(request.args.get('clone'))
        return render_template(
            'index.html',
            text=text,
            disabled=['clone', 'new', 'raw', 'download']
        )

from flask import request, current_app, abort, url_for, render_template
from app.views import BaseView
import app.repositories.paste as paste


class EditView(BaseView):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        if request.method == 'POST':
            maxlength = current_app.config.get('MAX_PASTE_LENGTH')
            text = request.form.get('text')

            if text is None or text.strip() == '':
                abort(400)
            elif maxlength is not None and len(text) > maxlength:
                abort(413)

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

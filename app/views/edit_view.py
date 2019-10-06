from flask import request, current_app, url_for, render_template, abort
from pygments.lexers import get_all_lexers
from app.views import BaseView
import app.repositories.paste as paste


class EditView(BaseView):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        languages = [{
            'name': lexer[0],
            'extension': lexer[1][0]
        } for lexer in get_all_lexers()]

        if request.method == 'POST':
            maxlength = current_app.config.get('MAX_PASTE_LENGTH')
            text = request.form.get('text')
            extension = request.form.get('extension')

            if text is None or text.strip() == '':
                abort(400)
            elif maxlength is not None and len(text) > maxlength:
                abort(413)

            hexhash = paste.insert_paste(text)
            if extension:
                url = url_for(
                    'paste.view.extension',
                    hexhash=hexhash,
                    extension=extension,
                    _external=True
                )
            else:
                url = url_for('paste.view', hexhash=hexhash, _external=True)
            return self.redirect_or_text(
                url,
                200
            )

        text = paste.get_paste(request.args.get('clone'))
        return render_template(
            'index.html',
            text=text,
            languages=languages,
            disabled=['clone', 'new', 'raw', 'download']
        )

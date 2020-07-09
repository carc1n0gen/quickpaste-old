from flask import request, redirect, url_for, render_template
from flask.views import View
from app.forms import EditForm
from app.repositories import paste
from app.util import about_text, highlight, LANGUAGES


class PasteEdit(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = EditForm()
        if form.validate_on_submit():
            return self.post(form)
        return self.get(form)

    def get(self, form):
        clone = request.args.get('clone')
        lang = request.args.get('lang')
        if clone == 'about':
            doc = {'text': about_text}
        else:
            doc = paste.get_paste(clone)

        text = ""
        if doc is not None and form.text.data is None:
            form.text.data = doc['text']
            form.extension.data = lang
            text = highlight(doc['text'], request.args.get('lang'))

        return render_template(
            'paste_edit.html',
            hide_new=True,
            languages=LANGUAGES,
            form=form,
            text=text,
            body_class='edit-height-fix',
        )

    def post(self, form):
        text = form.text.data
        extension = form.extension.data or None
        id = paste.insert_paste(text)
        return redirect(url_for('paste.show', id=id, extension=extension, _external=True))

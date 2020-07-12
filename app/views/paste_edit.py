from flask import request, redirect, url_for, render_template, session
from flask.views import View
from app.forms import EditForm
from app.repositories import paste
from app.util import highlight, LANGUAGES


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
        created_ids = session.get('created_ids', [])
        created_ids.append(id)
        session['created_ids'] = created_ids
        accept = request.headers.get('Accept')
        if accept == 'text/plain':
            return url_for('paste.show', id=id, extension=extension, _external=True), 200, {'Content-Type': 'text/plain'}
        return redirect(url_for('paste.show', id=id, extension=extension, _external=True))

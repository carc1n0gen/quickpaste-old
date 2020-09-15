import math
from datetime import datetime, timedelta
from flask import request, redirect, url_for, render_template, session, flash
from flask.views import View
from app.forms import EditForm
from app.repositories import paste
from app.util import highlight, LANGUAGES
from app.helpers import abort_if


class PasteEdit(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = EditForm()
        if form.validate_on_submit():
            return self.post(form)
        return self.get(form)

    def get(self, form):
        lang = request.args.get('lang')
        edit = request.args.get('edit')
        if edit and edit not in session.get('created_ids', []):
            flash(f'You don\'t have permission to edit this paste [{edit}].', category='error')
            return redirect(url_for('paste.show', id=edit, extension=lang))

        clone = request.args.get('clone')

        if edit:
            doc = paste.get_paste(edit)
            abort_if(doc is None, 404)
        elif clone:
            doc = paste.get_paste(clone)
            abort_if(doc is None, 404)
        else:
            doc = None

        text = ''
        delete_after = '7'
        if doc is not None and form.text.data is None:
            form.text.data = doc['text']
            if doc['delete_at']:
                form.delete_after.data = str(math.ceil((doc['delete_at'] - datetime.utcnow()).total_seconds() / 86400))
            else:
                form.delete_after.data = delete_after
            form.extension.data = lang
            form.id.data = edit if edit else None
            text = highlight(doc['text'], request.args.get('lang'))
        else:
            form.text.data = text
            form.delete_after.data = delete_after

        return render_template(
            'paste_edit.html',
            hide_new=True,
            languages=LANGUAGES,
            form=form,
            text=text,
            body_class='edit-height-fix',
        )

    def post(self, form):
        id = form.id.data
        text = form.text.data
        delete_after_days = int(form.delete_after.data)
        extension = form.extension.data or None

        if id:
            doc = paste.get_paste(id)
            abort_if(doc is None, 404)
            doc['text'] = text
            doc['delete_at'] = doc['created_at'] + timedelta(days=delete_after_days)
        else:
            doc = {
                'text': text,
                'delete_at': datetime.utcnow() + timedelta(days=delete_after_days)
            }

        upserted_id = paste.upsert_paste(doc)
        created_ids = session.get('created_ids', [])

        if upserted_id not in created_ids:
            created_ids.append(upserted_id)

        session['created_ids'] = created_ids

        accept = request.headers.get('Accept')
        if accept == 'text/plain':
            return url_for('paste.show', id=upserted_id, extension=extension, _external=True), 200, {'Content-Type': 'text/plain'}
        return redirect(url_for('paste.show', id=upserted_id, extension=extension, _external=True))

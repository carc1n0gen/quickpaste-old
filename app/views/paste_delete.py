from flask import session, flash, redirect, url_for
from flask.views import View
from app.repositories import paste


class PasteDelete(View):
    methods = ['POST']

    def dispatch_request(self, id, extension=None):
        if id in session.get('created_ids', []):
            paste.delete_paste(id)
            flash('Paste has been deleted.', category='success')
            return redirect(url_for('paste.edit'))

        flash(f'You don\'t have permission to delete this paste [{id}].', category='error')
        return redirect(url_for('paste.show', id=id, extension=extension))

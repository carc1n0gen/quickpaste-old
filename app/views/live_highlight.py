from flask import jsonify
from flask.views import View
from app.forms import EditForm
from app.util import highlight


class LiveHighlight(View):
    methods = ['POST']

    def dispatch_request(self):
        form = EditForm()
        if form.validate_on_submit():
            result = highlight(form.text.data, form.extension.data)
            return jsonify(extension=form.extension.data, data=result)
        return jsonify(form.errors), 400

from werkzeug.datastructures import MultiDict
from app.forms import EditForm


def test_should_fail_validation_all(app):
    with app.app_context():
        form = EditForm({})
        assert form.validate() is False
        assert len(form.errors) == 2


def test_should_fail_validation_text_length(app):
    app.config['MAX_PASTE_LENGTH'] = 4
    with app.app_context():
        form = EditForm(MultiDict([('text', 'abcde'), ('extension', '')]))
        assert form.validate() is False
        assert len(form.errors) == 1
        assert form.text.errors[0] == 'Your snippet is too long.  Max 4 characters.'

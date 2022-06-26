from flask import current_app
from flask_wtf import FlaskForm
from wtforms import ValidationError, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired
from app.util import LANGUAGES


delete_after_choices = [
    ('1', 'delete after 1 day'),
    ('2', 'delete after 2 days'),
    ('3', 'delete after 3 days'),
    ('4', 'delete after 4 days'),
    ('5', 'delete after 5 days'),
    ('6', 'delete after 6 days'),
    ('7', 'delete after 7 days'),
]


class EditForm(FlaskForm):
    id = HiddenField()
    text = TextAreaField('Code', [DataRequired('Some text is required.')])
    delete_after = SelectField('Delete After (days)', choices=delete_after_choices)
    extension = SelectField('Language', choices=LANGUAGES)

    def validate_text(self, field):
        maxlength = current_app.config.get('MAX_PASTE_LENGTH')
        if maxlength and len(field.data) > maxlength:
            raise ValidationError(
                f'Your snippet is too long.  Max {maxlength} characters.')

    def validate_delete_after(self, field):
        try:
            value = int(field.data)
            if value < 1 or value > 7:
                raise ValidationError('Delete after must be from 1 to 7.')
        except TypeError:
            raise ValidationError('Delete after must be from 1 to 7.')

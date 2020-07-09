from flask import current_app
from flask_wtf import FlaskForm
from wtforms import ValidationError, TextAreaField, SelectField
from wtforms.validators import DataRequired
from app.util import LANGUAGES


class EditForm(FlaskForm):
    text = TextAreaField('Code', [DataRequired()])
    extension = SelectField('Language', choices=LANGUAGES)

    def validate_text(self, field):
        maxlength = current_app.config.get('MAX_PASTE_LENGTH')
        if maxlength and len(field.data) > maxlength:
            raise ValidationError(
                f'Your snippet is too long.  Max {maxlength} characters.')

from flask import Blueprint, current_app, request, url_for, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import ValidationError, TextAreaField, SelectField
from wtforms.validators import DataRequired
from app.repositories import paste
from app.util import about_text

edit_bp = Blueprint('edit', __name__)


LANGUAGES = [
    (None, 'select language'),
    ('ada', 'Ada'),
    ('sh', 'Bash'),
    ('c', 'C'),
    ('cs', 'C#'),
    ('cpp', 'C++'),
    ('clj', 'Clojure'),
    ('cljs', 'ClojureScript'),
    ('coffee', 'CoffeeScript'),
    ('cr', 'Crystal'),
    ('css', 'CSS'),
    ('d', 'D'),
    ('dart', 'Dart'),
    ('django', 'Django Template'),
    ('ex', 'Elixir'),
    ('erl', 'Erlang'),
    ('fs', 'F#'),
    ('fish', 'Fish'),
    ('f', 'Fortran'),
    ('go', 'Go'),
    ('groovy', 'Groovy'),
    ('haml', 'Haml'),
    ('hbs', 'Handlebars'),
    ('hs', 'Haskell'),
    ('html', 'HTML'),
    ('ini', 'INI'),
    ('java', 'Java'),
    ('jsp', 'Java Server Page'),
    ('js', 'JavaScript'),
    ('json', 'JSON'),
    ('jinja', 'Jinja Template'),
    ('kt', 'Kotlin'),
    ('less', 'Less'),
    ('liquid', 'Liquid Template'),
    ('lua', 'Lua'),
    ('md', 'Markdown'),
    ('moon', 'MoonScript'),
    ('nim', 'Nim'),
    ('m', 'Objective-C'),
    ('ml', 'OCaml'),
    ('pl', 'Perl'),
    ('php', 'PHP'),
    ('txt', 'Plain Text'),
    ('py', 'Python'),
    ('rb', 'Ruby'),
    ('rs', 'Rust'),
    ('scss', 'SASS'),
    ('sql', 'SQL'),
    ('swift', 'Swift'),
    ('toml', 'TOML'),
    ('twig', 'Twig Template'),
    ('ts', 'TypeScript'),
    ('vala', 'Vala'),
    ('xml', 'XML'),
    ('yaml', 'YAML', ),
]


class EditForm(FlaskForm):
    text = TextAreaField('Code', [DataRequired()])
    extension = SelectField('Language', choices=LANGUAGES)

    def validate_text(self, field):
        maxlength = current_app.config.get('MAX_PASTE_LENGTH')
        if maxlength and len(field.data) > maxlength:
            raise ValidationError(f'Your snippet is too long.  Max {maxlength} characters.')


@edit_bp.route('/', methods=['GET', 'POST'])
def edit():
    form = EditForm()
    if form.validate_on_submit():
        text = form.text.data
        extension = form.extension.data
        id = paste.insert_paste(text)
        return redirect(url_for('view.view', id=id, extension=extension, _external=True))

    clone = request.args.get('clone')
    if clone == 'about':
        doc = {'text': about_text}
    else:
        doc = paste.get_paste(clone)

    if doc is not None and form.text.data is None:
        form.text.data = doc['text']

    return render_template(
        'edit/edit.html',
        hide_new=True,
        languages=LANGUAGES,
        lang=request.args.get('lang'),
        form=form,
        body_class='edit-height-fix',
    )
